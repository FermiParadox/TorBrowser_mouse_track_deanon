from abc import ABC, abstractmethod

from analysis.metrics_dataclasses import TimesXY
from analysis.physics import Speed2Points, Slope2Points, Acceleration

"""
When calculating angle, speed, etc. using only the last 2 points 
causes huge errors at low mouse speeds, 
due to pixels being chessboard-like boxes.
A better solution would be (linear) fitting of more than 2 points.
"""


class _SinglePointHandler(ABC):
    # Currently up to two extra points are needed from a critical point
    MAX_EXTRA_INDEX = 2

    def __init__(self, crit_index: int, all_txy: TimesXY):
        self.x_list = all_txy.x
        self.y_list = all_txy.y
        self.t_list = all_txy.time
        self.crit_index = crit_index
        self.max_index = len(self.x_list) - 1

    def index_too_small(self):
        return self.crit_index - self.MAX_EXTRA_INDEX < 0

    def index_too_large(self):
        return self.crit_index + self.MAX_EXTRA_INDEX > self.max_index

    def point_n(self, extra_index):
        index = self.crit_index + extra_index
        return self.x_list[index], self.y_list[index]

    def time_n(self, extra_index):
        index = self.crit_index + extra_index
        return self.t_list[index]

    @property
    @abstractmethod
    def p3(self):
        pass

    def space_n(self, extra_index):
        pass

    def velocity_n(self, extra_index):
        pass

    def acceleration_n(self, extra_index):
        pass


class ExitHandler(_SinglePointHandler):
    @property
    def p3(self):
        return self.point_n(extra_index=0)

    @property
    def p2(self):
        return self.point_n(extra_index=-1)

    @property
    def p1(self):
        return self.point_n(extra_index=-2)

    @property
    def t3(self):
        return self.time_n(extra_index=0)

    @property
    def t2(self):
        return self.time_n(extra_index=-1)

    @property
    def t1(self):
        return self.time_n(extra_index=-2)

    @property
    def critical_angle(self):
        if self.index_too_small:
            return None
        return Slope2Points(p1=self.p2, p2=self.p3).angle

    @property
    def critical_speed(self):
        if self.index_too_small:
            return None
        return Speed2Points(p1=self.p2, p2=self.p3,
                            t1=self.t2, t2=self.t3).speed

    @property
    def critical_acceleration(self):
        if self.index_too_small:
            return None
        return Acceleration(p1=self.p1, p2=self.p2, p3=self.p3,
                            t1=self.t1, t2=self.t2, t3=self.t3).acceleration


class EntryHandler(_SinglePointHandler):
    @property
    def p3(self):
        return self.point_n(extra_index=2)

    @property
    def p2(self):
        return self.point_n(extra_index=1)

    @property
    def p1(self):
        """First entry point"""
        return self.point_n(extra_index=0)

    @property
    def t3(self):
        return self.time_n(extra_index=2)

    @property
    def t2(self):
        return self.time_n(extra_index=1)

    @property
    def t1(self):
        return self.time_n(extra_index=0)

    @property
    def critical_angle(self):
        """Return approximate angle when exiting browser."""
        if self.index_too_large:
            return None
        return Slope2Points(p1=self.p1, p2=self.p2).angle

    @property
    def critical_speed(self):
        if self.index_too_large:
            return None
        return Speed2Points(p1=self.p1, p2=self.p2,
                            t1=self.t1, t2=self.t2).speed

    @property
    def critical_acceleration(self):
        if self.index_too_large:
            return None
        return Acceleration(
            p1=self.p1, p2=self.p2, p3=self.p3,
            t1=self.t1, t2=self.t2, t3=self.t3).acceleration
