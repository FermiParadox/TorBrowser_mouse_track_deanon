import secrets
from dataclasses import dataclass

from analysis.ip_base import IPv6_or_IPv4_obj
from analysis.metrics_base import ITXY


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
    all_itxy: ITXY
    exit_itxy: ITXY  # last point of position stored, before browser switching
    entry_itxy: ITXY  # first point after refocusing browser

    def __post_init__(self):
        self.exit_times = self.exit_itxy.time
        self.entry_times = self.entry_itxy.time

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
