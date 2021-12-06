from dataclasses import dataclass, field
from typing import List

from analysis.point_types import ENTRY_OR_EXIT_TYPE


@dataclass
class XYPoint:
    x: int
    y: int

    def as_tuple(self):
        return self.x, self.y


@dataclass
class XY:
    x: List[int] = field(default_factory=list)
    y: List[int] = field(default_factory=list)


@dataclass
class ITXYEPoint:
    """The index of a point in the full data arrays.

    e.g. an ITXYE object that stores only exits
    has I as the index of the point in the initial ITXYE object that contains all points.

    This allows easy mapping of all data points and their respective metrics.
    """
    index: int
    time: int
    x: int
    y: int
    e: ENTRY_OR_EXIT_TYPE


@dataclass
class ITXYE:
    indices: List[int] = field(default_factory=list)
    time: List[int] = field(default_factory=list)
    x: List[int] = field(default_factory=list)
    y: List[int] = field(default_factory=list)
    e: List[ENTRY_OR_EXIT_TYPE] = field(default_factory=list)

    def get_point_by_index(self, index):
        return ITXYEPoint(index=index,
                          time=self.time[index],
                          x=self.x[index],
                          y=self.y[index],
                          e=self.e[index])

    def append_point(self, itxye_point: ITXYEPoint):
        self.indices.append(itxye_point.index)
        self.time.append(itxye_point.time)
        self.x.append(itxye_point.x)
        self.y.append(itxye_point.y)
        self.e.append(itxye_point.e)

    def as_iterator(self):
        return zip(self.indices, self.time, self.x, self.y, self.e)

    def as_points(self):
        iterator = self.as_iterator()
        for point in iterator:
            yield ITXYEPoint(index=point[0],
                             time=point[1],
                             x=point[2],
                             y=point[3],
                             e=point[4])
