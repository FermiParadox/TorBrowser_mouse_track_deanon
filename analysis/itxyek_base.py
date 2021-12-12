from dataclasses import dataclass, field
from typing import List

from analysis.p_types import EntryOrExit, KeyOrMouse


@dataclass
class XYPoint:
    x: int
    y: int

    def as_tuple(self):
        return self.x, self.y


@dataclass
class XYFloatPoint:
    x: float
    y: float

    def as_tuple(self):
        return self.x, self.y


@dataclass
class XY:
    x: List[int] = field(default_factory=list)
    y: List[int] = field(default_factory=list)


@dataclass
class ITXYEKPoint:
    """The index of a point in the full data arrays.

    e.g. an ITXYEK object that stores only exits
    has I as the index of the point in the initial ITXYEK object that contains all points.

    This allows easy mapping of all data points and their respective metrics.
    """
    index: int
    time: int
    x: int
    y: int
    e: EntryOrExit
    k: KeyOrMouse


@dataclass
class ITXYEK:
    indices: List[int] = field(default_factory=list)
    time: List[int] = field(default_factory=list)
    x: List[int] = field(default_factory=list)
    y: List[int] = field(default_factory=list)
    e: List[EntryOrExit] = field(default_factory=list)
    k: List[KeyOrMouse] = field(default_factory=list)

    def point_by_index(self, index):
        return ITXYEKPoint(index=index,
                           time=self.time[index],
                           x=self.x[index],
                           y=self.y[index],
                           e=self.e[index],
                           k=self.k[index]
                           )

    def append_point(self, p: ITXYEKPoint):
        self.indices.append(p.index)
        self.time.append(p.time)
        self.x.append(p.x)
        self.y.append(p.y)
        self.e.append(p.e)
        self.k.append(p.k)

    def as_iterator(self):
        return zip(self.indices, self.time, self.x, self.y, self.e, self.k)

    def as_points(self):
        iterator = self.as_iterator()
        for point in iterator:
            yield ITXYEKPoint(index=point[0],
                              time=point[1],
                              x=point[2],
                              y=point[3],
                              e=point[4],
                              k=point[5]
                              )
