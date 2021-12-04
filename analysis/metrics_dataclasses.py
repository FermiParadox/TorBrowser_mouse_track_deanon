from dataclasses import dataclass, field
from typing import List


@dataclass
class XY:
    x: List[int] = field(default_factory=list)
    y: List[int] = field(default_factory=list)


@dataclass
class TimeXYPoint:
    time: int
    x: int
    y: int


@dataclass
class TimesXY:
    time: List[int] = field(default_factory=list)
    x: List[int] = field(default_factory=list)
    y: List[int] = field(default_factory=list)

    def get_point_by_index(self, index):
        return TimeXYPoint(time=self.time[index],
                           x=self.x[index],
                           y=self.y[index])

    def append_point(self, txy_point: TimeXYPoint):
        self.time.append(txy_point.time)
        self.x.append(txy_point.x)
        self.y.append(txy_point.y)


@dataclass
class ITXY:
    index: List[int] = field(default_factory=list)
    time: List[int] = field(default_factory=list)
    x: List[int] = field(default_factory=list)
    y: List[int] = field(default_factory=list)


