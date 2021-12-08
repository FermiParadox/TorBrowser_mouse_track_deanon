from dataclasses import dataclass, field
from typing import List

from analysis.point_types import EntryOrExitType


@dataclass
class IWVAEPoint:
    """
    `index`:    Index of the full trajectory object.
    `w`:        Angle in relation to previous point(s) (if this point is an exit point)
                    or the next point(s) (if this point is an entry point).
    `v`:        Velocity (the above for entry-exit applies).
    `a`:        Acceleration (the above for entry-exit applies)
    `e`:        Exit or entry type of critical point.
    """
    index: int
    w: float  # angle
    v: float  # velocity
    a: float  # acceleration
    e: EntryOrExitType


@dataclass
class IWVAE:
    indices: List[int] = field(default_factory=list)
    w: List[float] = field(default_factory=list)
    v: List[float] = field(default_factory=list)
    a: List[float] = field(default_factory=list)
    e: List[EntryOrExitType] = field(default_factory=list)

    def get_point_by_index(self, index):
        n = self.indices.index(index)
        return IWVAEPoint(index=n,
                          w=self.w[n],
                          v=self.v[n],
                          a=self.a[n],
                          e=self.e[n])

    def append_point(self, iwvae_point: IWVAEPoint):
        self.indices.append(iwvae_point.index)
        self.w.append(iwvae_point.w)
        self.v.append(iwvae_point.v)
        self.a.append(iwvae_point.a)
        self.e.append(iwvae_point.e)

    def as_points(self):
        return zip(self.indices, self.w, self.v, self.a, self.e)
