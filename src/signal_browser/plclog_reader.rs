use flate2::read::GzDecoder;
use std::collections::HashMap;
use std::fs::File;
use std::io::Read;
use std::path::Path;
use ndarray::prelude::*;
use ndarray_csv::Array2Reader;
use futures::stream::FuturesOrdered;
use tokio::task;
use std::collections::HashSet;
use chrono::prelude::*;
use num_traits::FromPrimitive;

struct PlcLogReader;

impl PlcLogReader {
    async fn read_file_async(file_path: &Path) -> Vec<ndarray::Array1<f32>> {
        let fut = task::spawn_blocking(move || Self::read_file(file_path));
        fut.await.unwrap()
    }

    fn read_file(file_path: &Path) -> Vec<ndarray::Array1<f32>> {
        let file = File::open(file_path).unwrap();
        let mut decoder = GzDecoder::new(file);
        let mut data = Vec::new();
        decoder.read_to_end(&mut data).unwrap();
        let mut rdr = csv::ReaderBuilder::new()
            .has_headers(false)
            .from_reader(data.as_slice());
        let mut arrays = Vec::new();
        for result in rdr.deserialize_array2_dynamic().unwrap() {
            let array: Array2<f32> = result.unwrap();
            arrays.push(array);
        }
        arrays
    }

    async fn read_multiple_files_async(file_paths: &[&Path]) -> Vec<Vec<ndarray::Array1<f32>>> {
        let mut tasks = (0..file_paths.len())
            .into_iter()
            .map(|idx| Self::read_file_async(file_paths[idx]))
            .collect::<FuturesOrdered<_>>()
            .collect::<Vec<_>>()
            .await;
        tasks
    }

    fn read_logfile(file_paths: &[&Path]) -> Vec<Vec<ndarray::Array1<f32>>> {
        let mut handles = FuturesUnordered::new();
        for &file in file_paths {
            handles.push(task::spawn(Self::read_file(file)));
        }
        let mut result = Vec::new();
        while let Some(Ok(val)) = handles.next().await {
            result.push(val);
        }
        result
    }
}

struct TimeConversionUtils;

impl TimeConversionUtils {
    fn oledatetime_to_datetime(oledatetime: f64) -> DateTime<Utc> {
        let d = NaiveDateTime::from_timestamp(
            (oledatetime - 25569f64) * 86400f64,
            0,
        );
        DateTime::<Utc>::from_utc(d, Utc)
    }
}