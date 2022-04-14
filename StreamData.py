
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
    ads_list: List[Tuple[AdData]]

    def __post_init__(self):
        self.binary_data_parts = []
        self.loaded = False
        self.ads_proccessed = False

    def contain_path(self, path):
        return path == self.local_path