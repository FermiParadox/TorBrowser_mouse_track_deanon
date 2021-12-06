import secrets
from dataclasses import dataclass

from analysis.ip_base import IPv6_or_IPv4_obj
from analysis.itwva_base import IWVAE
from analysis.itxy_base import ITXYE


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
    all_itxye: ITXYE
    exit_itxye: ITXYE  # last point of position stored, before browser switching
    entry_itxye: ITXYE  # first point after refocusing browser

    metrics: IWVAE

    def __post_init__(self):
        self.exit_times = self.exit_itxye.time
        self.entry_times = self.entry_itxye.time

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
