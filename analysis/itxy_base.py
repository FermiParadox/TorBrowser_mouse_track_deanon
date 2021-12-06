from dataclasses import dataclass, field
from typing import List


@dataclass
class ITXYPoint:
    """The index of a point in the full data arrays.

    e.g. an ITXY object that stores only exits
    has I as the index of the point in the initial ITXY object that contains all points.

    This allows easy mapping of all data points and their respective metrics.
    """
    index: int
    time: int
    x: int
    y: int


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

    def as_points(self):
        return zip(self.indices, self.time, self.x, self.y)

