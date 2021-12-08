import secrets
from dataclasses import dataclass, field
from typing import Iterator

from analysis.ip_base import IPv6_or_IPv4_obj
from analysis.iwvae_base import IWVAE
from analysis.itxye_base import ITXYE, ITXYEPoint
from analysis.point_types import EXIT_TYPE, ENTRY_TYPE


class IDGenerator:
    MAX_ID_NUM = 10 ** 9
    IDs_Used = set()

    @staticmethod
    def unique_id() -> int:
        while 1:
            generated_id = secrets.randbelow(IDGenerator.MAX_ID_NUM)
            if generated_id not in IDGenerator.IDs_Used:
                return generated_id


@dataclass
class User:
    id: int
    ip: IPv6_or_IPv4_obj
    all_itxye: ITXYE

    exit_itxye: ITXYE = field(default_factory=ITXYE)
    entry_itxye: ITXYE = field(default_factory=ITXYE)
    exit_metrics: IWVAE = field(default_factory=IWVAE)
    entry_metrics: IWVAE = field(default_factory=IWVAE)

    def __post_init__(self):
        self.exit_itxye = self._exit_itxye()
        self.entry_itxye = self._entry_itxye()

        self.exit_times = self.exit_itxye.time
        self.exit_indices = self.exit_itxye.indices
        self.exit_x = self.exit_itxye.x
        self.exit_y = self.exit_itxye.y

        self.entry_times = self.entry_itxye.time
        self.entry_indices = self.entry_itxye.indices
        self.entry_x = self.entry_itxye.x
        self.entry_y = self.entry_itxye.y

    def all_itxye_as_points(self) -> Iterator[ITXYEPoint]:
        return [p for p in self.all_itxye.as_points()]

    def exit_points(self) -> Iterator[ITXYEPoint]:
        return (p for p in self.all_itxye_as_points() if p.e == EXIT_TYPE)

    def entry_points(self) -> Iterator[ITXYEPoint]:
        return (p for p in self.all_itxye_as_points() if p.e == ENTRY_TYPE)

    def _exit_itxye(self) -> ITXYE:
        return ITXYE(indices=[p.index for p in self.exit_points()],
                     time=[p.time for p in self.exit_points()],
                     x=[p.x for p in self.exit_points()],
                     y=[p.y for p in self.exit_points()],
                     e=[p.e for p in self.exit_points()])

    def _entry_itxye(self) -> ITXYE:
        return ITXYE(indices=[p.index for p in self.entry_points()],
                     time=[p.time for p in self.entry_points()],
                     x=[p.x for p in self.entry_points()],
                     y=[p.y for p in self.entry_points()],
                     e=[p.e for p in self.entry_points()])

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
