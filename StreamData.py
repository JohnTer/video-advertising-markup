
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, List, ByteString


@dataclass
class AdData(object):
    path_to_ad: str
    start_time: datetime
    data: ByteString


    def __post_init__(self):
        self.loaded = False




@dataclass
class StreamData(object):
    local_path: str

    def __post_init__(self):
        self.binary_data_parts = []
        self.loaded = False
        self.ads_proccessed = False
        self.ads_list = []

    def add_ads(self, ads_path, timecode):
        with open(ads_path, 'rb') as f:
            data = f.read()
        self.ads_list.append(AdData(ads_path, timecode, data))
        

    def contain_path(self, path):
        return path == self.local_path