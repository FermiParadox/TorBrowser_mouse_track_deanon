from abc import ABC
from typing import Iterator, Union, Type

import analysis.p_types as p_types
from analysis.itxyek_base import ITXYEK, XYPoint
from analysis.metrics_base import MetricValueUndefined, METRIC_TYPE
from analysis.physics import AngleCalc, Velocity, Acceleration

"""
When calculating angle, speed, etc. using only the last 2 points 
causes huge errors at low mouse speeds, 
due to pixels being chessboard-like boxes.
"""


class _EntryOrExitHandler(ABC):
    MAX_EXTRA_INDEX = 5

    def __init__(self, crit_index: int, all_itxyek: ITXYEK):
        self.x_list = all_itxyek.x
        self.y_list = all_itxyek.y
        self.t_list = all_itxyek.time
        self.crit_index = crit_index
        self.max_index = all_itxyek.indices[-1]

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

    def velocity(self) -> METRIC_TYPE:
        if self.index_too_small():
            return MetricValueUndefined
        return Velocity(xy1=self.point_n(-1), xy2=self.point_n(0), xy_extra=self.point_n(-5)).v()

    def acceleration(self) -> METRIC_TYPE:
        if self.index_too_small():
            return MetricValueUndefined
        xy1 = self.point_n(-2)
        xy2 = self.point_n(-1)
        xy3 = self.point_n(0)
        xy_extra = self.point_n(-5)
        return Acceleration(xy1=xy1, xy2=xy2, xy3=xy3, xy_extra=xy_extra).a()


class EntryHandler(_EntryOrExitHandler):
    def angle(self) -> METRIC_TYPE:
        """Return approximate angle when exiting browser."""
        if self.index_too_large():
            return MetricValueUndefined
        return AngleCalc(xy1=self.point_n(0), xy2=self.point_n(1)).angle()

    def velocity(self) -> METRIC_TYPE:
        if self.index_too_large():
            return MetricValueUndefined
        xy1 = self.point_n(0)
        xy2 = self.point_n(1)
        xy_extra = self.point_n(5)
        return Velocity(xy1=xy1, xy2=xy2, xy_extra=xy_extra).v()

    def acceleration(self) -> METRIC_TYPE:
        if self.index_too_large():
            return MetricValueUndefined
        xy1 = self.point_n(0)
        xy2 = self.point_n(1)
        xy3 = self.point_n(2)
        xy_extra = self.point_n(5)
        return Acceleration(xy1=xy1, xy2=xy2, xy3=xy3, xy_extra=xy_extra).a()


ENTRY_OR_EXIT_HANDLER = Type[Union[ExitHandler, EntryHandler]]


class _MetricsCalculator:
    def __init__(self, all_itxyek: ITXYEK, crit_type: p_types.EntryOrExit, crit_indices: Iterator[int]):
        self.crit_indices = crit_indices
        self.crit_type = crit_type
        self.all_itxyek = all_itxyek
        self.point_handler: ENTRY_OR_EXIT_HANDLER = self._point_handler()

    def _point_handler(self):
        if self.crit_type == p_types.Exit():
            return ExitHandler
        else:
            return EntryHandler

    def critical_angles(self) -> Iterator[float]:
        angles = []
        for i in self.crit_indices:
            handler = self.point_handler(crit_index=i, all_itxyek=self.all_itxyek)
            angle = handler.angle()
            if angle != MetricValueUndefined:
                angles.append(angle)
        return angles

    def critical_speeds(self) -> Iterator[float]:
        speeds = []
        for i in self.crit_indices:
            handler = self.point_handler(crit_index=i, all_itxyek=self.all_itxyek)
            speed = handler.velocity()
            if speed != MetricValueUndefined:
                speeds.append(speed)
        return speeds

    def critical_accelerations(self) -> Iterator[float]:
        accelerations = []
        for i in self.crit_indices:
            handler = self.point_handler(crit_index=i, all_itxyek=self.all_itxyek)
            acceleration = handler.acceleration()
            if acceleration != MetricValueUndefined:
                accelerations.append(acceleration)
        return accelerations


class ExitMetricsCalc(_MetricsCalculator):
    def __init__(self, all_itxyek: ITXYEK, crit_indices: Iterator[int]):
        super().__init__(all_itxyek=all_itxyek, crit_type=p_types.Exit(), crit_indices=crit_indices)


class EntryMetricsCalc(_MetricsCalculator):
    def __init__(self, all_itxyek: ITXYEK, crit_indices: Iterator[int]):
        super().__init__(all_itxyek=all_itxyek, crit_type=p_types.Entry(), crit_indices=crit_indices)
