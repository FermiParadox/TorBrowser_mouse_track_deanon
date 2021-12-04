from dataclasses import dataclass, field
from typing import List


@dataclass
class XY:
    x: List[int] = field(default_factory=list)
    y: List[int] = field(default_factory=list)


@dataclass
class TXYPoint:
    time: int
    x: int
    y: int


@dataclass
class ITXYPoint:
    index: int
    time: int
    x: int
    y: int


@dataclass
class TXY:
    time: List[int] = field(default_factory=list)
    x: List[int] = field(default_factory=list)
    y: List[int] = field(default_factory=list)

    def get_point_by_index(self, index):
        return TXYPoint(time=self.time[index],
                        x=self.x[index],
                        y=self.y[index])

    def append_point(self, txy_point: TXYPoint):
        self.time.append(txy_point.time)
        self.x.append(txy_point.x)
        self.y.append(txy_point.y)


@dataclass
class ITXY:
    indices: List[int] = field(default_factory=list)
    time: List[int] = field(default_factory=list)
    x: List[int] = field(default_factory=list)
    y: List[int] = field(default_factory=list)

    def get_point_by_index(self, index):
        return ITXYPoint(index=index,
                         time=self.time[index],
                         x=self.x[index],
                         y=self.y[index])

    def append_point(self, itxy_point: ITXYPoint):
        self.indices.append(itxy_point.index)
        self.time.append(itxy_point.time)
        self.x.append(itxy_point.x)
        self.y.append(itxy_point.y)
