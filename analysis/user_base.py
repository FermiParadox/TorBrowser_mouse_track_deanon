import secrets
from dataclasses import dataclass, field
from typing import Iterator

import analysis.p_types as p_types
from analysis.ip_base import IPv6_or_IPv4_obj
from analysis.iwvaek_base import IWVAEK
from analysis.itxyek_base import ITXYEK, ITXYEKPoint


class IDGenerator:
    MAX_ID_NUM = 10 ** 3
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
    all_itxyek: ITXYEK

    exit_itxyek: ITXYEK = field(default_factory=ITXYEK)
    entry_itxyek: ITXYEK = field(default_factory=ITXYEK)
    exit_metrics: IWVAEK = field(default_factory=IWVAEK)
    entry_metrics: IWVAEK = field(default_factory=IWVAEK)

    def __post_init__(self):
        self.exit_itxyek = self._exit_itxyek()
        self.entry_itxyek = self._entry_itxyek()

        self.exit_times = self.exit_itxyek.time
        self.exit_indices = self.exit_itxyek.indices
        self.exit_x = self.exit_itxyek.x
        self.exit_y = self.exit_itxyek.y

        self.entry_times = self.entry_itxyek.time
        self.entry_indices = self.entry_itxyek.indices
        self.entry_x = self.entry_itxyek.x
        self.entry_y = self.entry_itxyek.y

    def all_itxyek_as_points(self) -> Iterator[ITXYEKPoint]:
        return [p for p in self.all_itxyek.as_points()]

    def exit_points(self) -> Iterator[ITXYEKPoint]:
        return (p for p in self.all_itxyek_as_points() if p.e == p_types.EXIT)

    def entry_points(self) -> Iterator[ITXYEKPoint]:
        return (p for p in self.all_itxyek_as_points() if p.e == p_types.ENTRY)

    def _exit_itxyek(self) -> ITXYEK:
        itxyek = ITXYEK()
        for p in self.exit_points():
            itxyek.append_point(p=p)
        return itxyek

    def _entry_itxyek(self) -> ITXYEK:
        itxyek = ITXYEK()
        for p in self.entry_points():
            itxyek.append_point(p=p)
        return itxyek

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
