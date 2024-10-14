import re
from collections import defaultdict

import pandas as pd
import tdm_loader
from PySide6.QtCore import QObject, QRunnable, Signal

from signal_browser.utils import TimeConversionUtils


class OpenFile(tdm_loader.OpenFile):
    def __init__(self, filename):
        super().__init__(filename)

    def channel_search(self, search_term):
        """
        Reimplementation of the channel_search method to return the description of the channel as well.
        """
        search_term = str(search_term).upper().replace(" ", "")

        matched_channels = []
        channel_group_ids = {v: i for i, v in enumerate(x.get("id") for x in self._xml_chgs)}

        for channel in self._root.findall(".//tdm_channel"):
            channel_name = channel.find("name").text
            channel_description = channel.find("description").text

            channel_name += f" ({channel_description})" if channel_description else ""

            if channel_name:
                group_uri = re.findall(r'id\("(.+?)"\)', channel.find("group").text)
                group_id = channel_group_ids.get(group_uri[0])
                channels = self._get_channels(group_id)

                channel_id = channels.get(channel.get("id"))

                if channel_name.upper().replace(" ", "").find(search_term) >= 0:
                    matched_channels.append((channel_name, group_id, channel_id))

        return matched_channels



class TDMLogReader:
    @staticmethod
    def get_all_channels(file):
        tdm_file = OpenFile(file)
        channels = tdm_file.channel_search("")
        return channels

    @staticmethod
    def get_all_groups(file):
        tdm_file = OpenFile(file)
        groups = tdm_file.channel_group_search("")

        new = []
        group_count = defaultdict(int)
        for group in groups:
            group_count[group[0]] += 1
            if group_count[group[0]] > 1:
                name = f"{group[0]} (#{group_count[group[0]]})"
            else:
                name = group[0]
            new.append((name, group[1]))
        return new




    @staticmethod
    def get_data(file, group, channel):
        tdm_file = OpenFile(file)

        try:
            timestamp = list(map(TimeConversionUtils.epoch_timestamp_to_datetime, tdm_file.channel(group, channel=0)))
        except IndexError as e:
            timestamp = []

        try:
            data = tdm_file.channel(group, channel)
        except IndexError:
            data = []
        df = pd.Series(data, timestamp, name=tdm_file.channel_name(group, channel))
        df.sort_index(inplace=True)
        return df


class TDM_WorkerSignals(QObject):
    Groups_Signal = Signal(list)
    Channels_Signal = Signal(list)
    Data_Signal = Signal(pd.Series)




class TdmGetAllChannelsWorker(QRunnable):
    def __init__(self, filename: str):
        super().__init__()
        self.signals = TDM_WorkerSignals()

        self.filename = filename

    def run(self):
        groups = TDMLogReader.get_all_groups(self.filename)
        channels = TDMLogReader.get_all_channels(self.filename)
        self.signals.Channels_Signal.emit([groups, channels])


class TdmGetDataWorker(QRunnable):
    def __init__(self, filename, group, channel, item):
        super().__init__()
        self.signals = TDM_WorkerSignals()

        self.filename = filename
        self.group = group
        self.channel = channel
        self.item = item

    def run(self):
        data = TDMLogReader.get_data(self.filename, self.group, self.channel)
        self.signals.Data_Signal.emit((self.item, data))

