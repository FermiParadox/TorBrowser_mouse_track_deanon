from abc import ABC
from typing import Iterator, Union, Type

from analysis.itxye_base import ITXYE, XYPoint
from analysis.physics import AngleCalc, Speed2Points, Acceleration
from analysis.point_types import EXIT_TYPE, ENTRY_TYPE, EntryOrExitType

"""
When calculating angle, speed, etc. using only the last 2 points 
causes huge errors at low mouse speeds, 
due to pixels being chessboard-like boxes.

A better solution would be (linear) fitting of more than 2 points,
when the speed is low.
"""


class MetricValueUndefined:
    """
    Some metrics can't be determined always.

    E.g. the angle of an exit point when there is only 1 point.
    """


METRIC_TYPE = Union[float, Type[MetricValueUndefined]]


class _EntryOrExitHandler(ABC):
    # Currently, up to two extra points are needed from a critical point
    MAX_EXTRA_INDEX = 2

    def __init__(self, crit_index: int, all_itxye: ITXYE):
        self.x_list = all_itxye.x
        self.y_list = all_itxye.y
        self.t_list = all_itxye.time
        self.crit_index = crit_index
        self.max_index = all_itxye.indices[-1]

    def index_too_small(self) -> bool:
        return self.index_total_less_than_0()

    def index_too_large(self) -> bool:
        return self.index_exceeds_max_array()

    def index_exceeds_max_array(self) -> bool:
        return self.crit_index + self.MAX_EXTRA_INDEX > self.max_index

    def index_total_less_than_0(self) -> bool:
        return self.crit_index - self.MAX_EXTRA_INDEX < 0

    def point_n(self, extra_index) -> XYPoint:
        index = self.crit_index + extra_index
        return XYPoint(self.x_list[index], self.y_list[index])

    def space_n(self, extra_index) -> METRIC_TYPE:
        pass

    def velocity_n(self, extra_index) -> METRIC_TYPE:
        pass

    def acceleration_n(self, extra_index) -> METRIC_TYPE:
        pass


class ExitHandler(_EntryOrExitHandler):
    def angle(self) -> METRIC_TYPE:
        if self.index_too_small():
            return MetricValueUndefined
        return AngleCalc(xy1=self.point_n(-1), xy2=self.point_n(0)).angle()

    def speed(self) -> METRIC_TYPE:
        if self.index_too_small():
            return MetricValueUndefined
        return Speed2Points(xy1=self.point_n(-1), xy2=self.point_n(0)).velocity()

    def acceleration(self) -> METRIC_TYPE:
        if self.index_too_small():
            return MetricValueUndefined
        return Acceleration(xy1=self.point_n(-2), xy2=self.point_n(-1), xy3=self.point_n(0)).acceleration()


class EntryHandler(_EntryOrExitHandler):
    def angle(self) -> METRIC_TYPE:
        """Return approximate angle when exiting browser."""
        if self.index_too_large():
            return MetricValueUndefined
        return AngleCalc(xy1=self.point_n(0), xy2=self.point_n(1)).angle()

    def speed(self) -> METRIC_TYPE:
        if self.index_too_large():
            return MetricValueUndefined
        return Speed2Points(xy1=self.point_n(0), xy2=self.point_n(1)).velocity()

    def acceleration(self) -> METRIC_TYPE:
        if self.index_too_large():
            return MetricValueUndefined
        return Acceleration(xy1=self.point_n(0), xy2=self.point_n(1), xy3=self.point_n(2)).acceleration()


ENTRY_OR_EXIT_HANDLER = Type[Union[ExitHandler, EntryHandler]]


class _MetricsCalculator:
    def __init__(self, all_itxye: ITXYE, crit_type: EntryOrExitType, crit_indices: Iterator[int]):
        self.crit_indices = crit_indices
        self.crit_type = crit_type
        self.all_itxye = all_itxye
        self.point_handler: ENTRY_OR_EXIT_HANDLER = self._point_handler()

    def _point_handler(self):
        if self.crit_type == EXIT_TYPE:
            return ExitHandler
        else:
            return EntryHandler

    def critical_angles(self) -> Iterator[float]:
        angles = []
        for i in self.crit_indices:
            handler = self.point_handler(crit_index=i, all_itxye=self.all_itxye)
            angle = handler.angle()
            if angle != MetricValueUndefined:
                angles.append(angle)
        return angles

    def critical_speeds(self) -> Iterator[float]:
        speeds = []
        for i in self.crit_indices:
            handler = self.point_handler(crit_index=i, all_itxye=self.all_itxye)
            speed = handler.speed()
            if speed != MetricValueUndefined:
                speeds.append(speed)
        return speeds

    def critical_accelerations(self) -> Iterator[float]:
        accelerations = []
        for i in self.crit_indices:
            handler = self.point_handler(crit_index=i, all_itxye=self.all_itxye)
            acceleration = handler.acceleration()
            if acceleration != MetricValueUndefined:
                accelerations.append(acceleration)
        return accelerations


class ExitMetricsCalc(_MetricsCalculator):
    def __init__(self, all_itxye: ITXYE, crit_indices: Iterator[int]):
        super().__init__(all_itxye=all_itxye, crit_type=EXIT_TYPE, crit_indices=crit_indices)


class EntryMetricsCalc(_MetricsCalculator):
    def __init__(self, all_itxye: ITXYE, crit_indices: Iterator[int]):
        super().__init__(all_itxye=all_itxye, crit_type=ENTRY_TYPE, crit_indices=crit_indices)
