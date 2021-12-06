from abc import ABC
from typing import Type, Union

from analysis.itxye_base import ITXYE
from analysis.physics import Speed2Points, AngleCalc, Acceleration

"""
When calculating angle, speed, etc. using only the last 2 points 
causes huge errors at low mouse speeds, 
due to pixels being chessboard-like boxes.
A better solution would be (linear) fitting of more than 2 points.
"""


class _EntryOrExitHandler(ABC):
    # Currently, up to two extra points are needed from a critical point
    MAX_EXTRA_INDEX = 2

    def __init__(self, crit_index: int, all_itxye: ITXYE):
        self.x_list = all_itxye.x
        self.y_list = all_itxye.y
        self.t_list = all_itxye.time
        self.crit_index = crit_index
        self.max_index = all_itxye.indices[-1]

    def index_too_small(self):
        return ...

    def index_too_large(self):
        return ...

    def index_exceeds_max_array(self):
        return self.crit_index + self.MAX_EXTRA_INDEX > self.max_index

    def index_total_less_than_0(self):
        return self.crit_index - self.MAX_EXTRA_INDEX < 0

    def point_n(self, extra_index):
        index = self.crit_index + extra_index
        return self.x_list[index], self.y_list[index]

    def space_n(self, extra_index):
        pass

    def velocity_n(self, extra_index):
        pass

    def acceleration_n(self, extra_index):
        pass


class ExitHandler(_EntryOrExitHandler):
    @property
    def angle(self):
        if self.index_too_small:
            return None
        return AngleCalc(xy1=self.p2, xy2=self.p3).angle

    @property
    def speed(self):
        if self.index_too_small:
            return None
        return Speed2Points(xy1=self.p2, xy2=self.p3).velocity

    @property
    def acceleration(self):
        if self.index_too_small:
            return None
        return Acceleration(p1=self.p1, p2=self.p2, p3=self.p3).acceleration


class EntryHandler(_EntryOrExitHandler):
    @property
    def angle(self):
        """Return approximate angle when exiting browser."""
        if self.index_too_large:
            return None
        return AngleCalc(xy1=self.p1, xy2=self.p2).angle

    @property
    def speed(self):
        if self.index_too_large:
            return None
        return Speed2Points(xy1=self.p1, xy2=self.p2).velocity

    @property
    def acceleration(self):
        if self.index_too_large:
            return None
        return Acceleration(
            p1=self.p1, p2=self.p2, p3=self.p3,
            t1=self.t1, t2=self.t2, t3=self.t3).acceleration


ENTRY_OR_EXIT_HANDLER = Type[Union[ExitHandler, EntryHandler]]
