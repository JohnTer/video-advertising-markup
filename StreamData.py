
from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class StreamData(object):
    local_path: str
    ads_list: List[Tuple[str, str]]

    def __post_init__(self):
        self.ads_iter = iter(self.ads_list)

    def get_next_ad(self):
        try:
            return next(self.ads_iter)
        except StopIteration:
            return None

    def __contains__(self, key):
        return key.strip() == self.local_path.strip()
