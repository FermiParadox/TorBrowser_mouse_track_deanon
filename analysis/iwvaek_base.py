from dataclasses import dataclass, field
from typing import List

from analysis.itxyek_base import ITXYEKPoint
import analysis.p_types as p_types


@dataclass
class IWVAEKPoint:
    """
    `index`:    Index of the full trajectory object.
    `w`:        Angle in relation to previous point(s) (if this point is an exit point)
                    or the next point(s) (if this point is an entry point).
    `v`:        Velocity (the above for entry-exit applies).
    `a`:        Acceleration (the above for entry-exit applies)
    `e`:        Exit or entry type of critical point.
    `k`:        Mouse or key triggered exit/entry.
    """
    index: int
    w: float  # angle
    v: float  # velocity
    a: float  # acceleration
    e: p_types.EntryOrExit
    k: p_types.KeyOrMouse


@dataclass
class IWVAEK:
    indices: List[int] = field(default_factory=list)
    w: List[float] = field(default_factory=list)
    v: List[float] = field(default_factory=list)
    a: List[float] = field(default_factory=list)
    e: List[p_types.EntryOrExit] = field(default_factory=list)
    k: List[p_types.KeyOrMouse] = field(default_factory=list)

    def get_metrics_by_point(self, p: ITXYEKPoint):
        return self.get_point_by_index(index=p.index)

    def get_point_by_index(self, index):
        n = self.indices.index(index)
        return IWVAEKPoint(index=n,
                           w=self.w[n],
                           v=self.v[n],
                           a=self.a[n],
                           e=self.e[n],
                           k=self.k[n],
                           )

    def append_point(self, p: IWVAEKPoint):
        self.indices.append(p.index)
        self.w.append(p.w)
        self.v.append(p.v)
        self.a.append(p.a)
        self.e.append(p.e)
        self.k.append(p.k)

    def as_points(self):
        return zip(self.indices, self.w, self.v, self.a, self.e, self.k)
