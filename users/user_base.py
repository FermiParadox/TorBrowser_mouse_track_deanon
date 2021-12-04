import secrets
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address
from typing import Union, List

from analysis.analysis import EntryMetrics, ExitMetrics
from analysis.metrics_dataclasses import TimesXY
from analysis.plotting import Plotter

IPv6_or_IPv4_obj = Union[IPv4Address, IPv6Address]


class IDGenerator:
    MAX_ID_NUM = 10 ** 9
    IDs_Used = set()

    @staticmethod
    def unique_id():
        while 1:
            generated_id = secrets.randbelow(IDGenerator.MAX_ID_NUM)
            if generated_id not in IDGenerator.IDs_Used:
                return generated_id


@dataclass
class User:
    id: int
    ip: IPv6_or_IPv4_obj
    all_txy: TimesXY
    exit_txy_lists: TimesXY  # last point of position stored, before browser switching
    entry_txy_lists: TimesXY  # first point after refocusing browser
    exit_indices: List[int]
    entry_indices: List[int]

    def __post_init__(self):
        self.exit_times = self.exit_txy_lists.time
        self.entry_times = self.entry_txy_lists.time

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
