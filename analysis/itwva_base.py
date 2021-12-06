from dataclasses import dataclass, field
from typing import List

from analysis.point_types import ENTRY_OR_EXIT_TYPE


@dataclass
class ITWVAPoint:
    """
    `index`:    Index of the full trajectory object.
    `type`:     Exit or entry type of critical point.
    `w`:        Angle in relation to previous point(s) (if this point is an exit point)
                    or the next point(s) (if this point is an entry point).
    `v`:        Velocity (the above for entry-exit applies).
    `a`:        Acceleration (the above for entry-exit applies)
    """
    index: int
    type: ENTRY_OR_EXIT_TYPE
    w: float  # angle
    v: float  # velocity
    a: float  # acceleration


@dataclass
class ITWVA:
    indices: List[int] = field(default_factory=list)
    type: List[ENTRY_OR_EXIT_TYPE] = field(default_factory=list)
    w: List[float] = field(default_factory=list)
    v: List[float] = field(default_factory=list)
    a: List[float] = field(default_factory=list)

    def get_point_by_index(self, index):
        return ITWVAPoint(index=index,
                          type=self.type[index],
                          w=self.w[index],
                          v=self.v[index],
                          a=self.a[index])

    def append_point(self, iwva_point: ITWVAPoint):
        self.indices.append(iwva_point.index)
        self.w.append(iwva_point.w)
        self.v.append(iwva_point.v)
        self.a.append(iwva_point.a)

    def as_points(self):
        return zip(self.indices, self.type, self.w, self.v, self.a)
