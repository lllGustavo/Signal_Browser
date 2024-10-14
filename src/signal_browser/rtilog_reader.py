import ast
import json
import pathlib
import sqlite3
import time

import pandas as pd
from PySide6 import QtCore
from PySide6.QtCore import QMutex, QObject, QRunnable, Signal

from signal_browser.utils import TimeConversionUtils


class RTILogReader:
    pathToAppUUID = pathlib.Path(__file__).absolute().parent.joinpath("App UUID's.csv")
    appUUIDTable = pd.read_csv(pathToAppUUID, delimiter=";",
                               names=["app_name", "company", "app_version", "sdk", "category", "app_uuid"],
                               index_col=False)
    appUUIDTable["app_uuid"] = appUUIDTable["app_uuid"].apply(lambda x: x.replace("-", ""))

    @classmethod
    def get_all_tables(cls, cur: sqlite3.Cursor):
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        return [table[0] for table in tables]

    @classmethod
    def get_tables_contains(cls, cur: sqlite3.Cursor, filter: str):
        tables = []
        for table in cls.get_all_tables(cur):
            cur.execute(f"PRAGMA table_info('{table}')")
            columns = cur.fetchall()
            for column in columns:
                if column[1] == filter:
                    tables.append(table)
        return tables

    @classmethod
    def get_channels_from_rti_json_sample(cls, cur: sqlite3.Cursor, table: str):
        query = f"SELECT rti_json_sample FROM '{table}';"
        cur.execute(query)
        data = cur.fetchone()
        if data is not None and data[0] is not None:
            channels = json.loads(data[0])
            for key, value in channels.items():
                channels[key] = type(value)
            return channels
        else:
            return {}

    @classmethod
    def get_channel_trace(cls, dbcon: sqlite3.Connection, table: str, channel: str):
        query = f"""SELECT json_extract(rti_json_sample, '$.timestamp'),
                json_extract(rti_json_sample, '$.{channel}'),
                SampleInfo_reception_timestamp
                FROM '{table}' WHERE json_extract(rti_json_sample, '$.{channel}') IS NOT NULL;"""

        df = pd.read_sql_query(query, dbcon, parse_dates={"SampleInfo_reception_timestamp": "ns"})

        if channel in ["id", "activityId", "requestId"]:
            column = f"json_extract(rti_json_sample, '$.{channel}')"
            df[column] = df[column].apply(ast.literal_eval)
            df[column] = df[column].apply(lambda x: cls.convert_UUID_to_name(x))


        if not df[df.columns[0]].isna().all():
            df["json_extract(rti_json_sample, '$.timestamp')"] = df[
                "json_extract(rti_json_sample, '$.timestamp')"
            ].apply(json.loads)
            df["json_extract(rti_json_sample, '$.timestamp')"] = df[
                "json_extract(rti_json_sample, '$.timestamp')"
            ].apply(TimeConversionUtils.json_to_datetime)

        return df

    @staticmethod
    def convert_UUID_to_name(lst_uuid):
        hex_list = []

        if lst_uuid[0] == "":
            return "".join(lst_uuid).strip()



        for char in lst_uuid:
            if char.startswith("\\u"):
                char = char.encode("utf-8").decode("unicode_escape")
            hex_value = hex(ord(char))
            hex_list.append(hex_value)
        hex_string = "".join(f"{int(h, 16):02X}" for h in hex_list)


        name = RTILogReader.appUUIDTable["app_name"].where(RTILogReader.appUUIDTable["app_uuid"] == hex_string.lower()).dropna().unique()
        if len(name) == 0:
            return hex_string
        else:
            return name[0]





    @staticmethod
    def _validate_rti_json_sample(cur: sqlite3.Cursor, table: str):
        query = f"SELECT json_extract(rti_json_sample, '$') FROM '{table}';"
        cur.execute(query)
        channel = cur.fetchone()

        if channel is not None and len(channel) > 0:
            return True
        else:
            return False


class SingleFile_RTI_DataReader(QRunnable):

    def __init__(self, filename, table, item_name, df_list, mutex):
        super().__init__()
        self.df_list = df_list
        self.filename = filename
        self.table = table
        self.item_name = item_name
        self.mutex = mutex

    def run(self):
        with sqlite3.connect(self.filename) as dbcon:
            cur = dbcon.cursor()
            tables = RTILogReader.get_all_tables(cur)
            if self.table in tables:
                df = RTILogReader.get_channel_trace(dbcon, self.table, self.item_name)

                self.mutex.lock()
                self.df_list.append(df)
                self.mutex.unlock()


class MultiThreaded_RTI_Reader(QRunnable):
    def __init__(self, filenames: list, item):
        super().__init__()
        self.signals = RTI_WorkerSignals()
        self.threadpool = QtCore.QThreadPool()
        self.threadpool.setMaxThreadCount(100)
        self.filenames = filenames
        self.item = item
        self.item_name = item.itemData.id
        self.table = item.parent().itemData.id

        self.mutex = QMutex()
        self.df_list = []

    def run(self):
        for filename in self.filenames:
            worker = SingleFile_RTI_DataReader(filename, self.table, self.item_name, self.df_list, self.mutex)
            self.threadpool.start(worker)
        time.sleep(1)  # needed to add in sleep so waitForDone do not trigger on small files

        self.threadpool.waitForDone()

        if len(self.df_list) == 0:
            self.df = pd.Series()
        elif len(self.df_list) == 1:
            self.df = self.df_list[0]
            self.df = self._dat_select_index(self.df)
        else:
            self.df = pd.concat(self.df_list)
            self.df = self._dat_select_index(self.df)
        self.df.sort_index(inplace=True)

        self.signals.Data_Signal.emit((self.item, self.df))

    def _dat_select_index(self, df):
        if not df[df.columns[0]].isna().all():
            df.drop("SampleInfo_reception_timestamp", axis=1, inplace=True)
            df.set_index("json_extract(rti_json_sample, '$.timestamp')", inplace=True)
        else:
            df.drop("json_extract(rti_json_sample, '$.timestamp')", axis=1, inplace=True)
            df.set_index("SampleInfo_reception_timestamp", inplace=True)

        if df.size == 1:
            return df

        df = df.squeeze()
        df.sort_index(inplace=True)
        return df


class RTI_WorkerSignals(QObject):
    Groups_Signal = Signal(list)
    Channels_Signal = Signal(list)
    Data_Signal = Signal(pd.Series)
