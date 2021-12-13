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


class ExitHandler(_EntryOrExitHandler):

    def angle(self) -> METRIC_TYPE:
        if self.index_too_small():
            return MetricValueUndefined
        xy1 = self.point_n(-1)
        xy2 = self.point_n(0)
        if Velocity().distance_too_small(xy1=xy1, xy2=xy2):
            xy1 = self.point_n(-4)
        return AngleCalc().angle(xy1=xy1, xy2=xy2)

    def velocity(self) -> METRIC_TYPE:
        if self.index_too_small():
            return MetricValueUndefined
        xy1 = self.point_n(-1)
        xy2 = self.point_n(0)
        if Velocity().distance_too_small(xy1=xy1, xy2=xy2):
            xy1 = self.point_n(-4)
        return Velocity().v(xy1=xy1, xy2=xy2)

    def acceleration(self) -> METRIC_TYPE:
        if self.index_too_small():
            return MetricValueUndefined
        xy1 = self.point_n(-2)
        xy2 = self.point_n(-1)
        xy3 = self.point_n(0)
        return Acceleration().a(xy1=xy1, xy2=xy2, xy3=xy3)


class EntryHandler(_EntryOrExitHandler):
    def angle(self) -> METRIC_TYPE:
        if self.index_too_large():
            return MetricValueUndefined
        xy1 = self.point_n(0)
        xy2 = self.point_n(1)
        if Velocity().distance_too_small(xy1=xy1, xy2=xy2):
            xy2 = self.point_n(4)
        return AngleCalc().angle(xy1=xy1, xy2=xy2)

    def velocity(self) -> METRIC_TYPE:
        if self.index_too_large():
            return MetricValueUndefined
        xy1 = self.point_n(0)
        xy2 = self.point_n(1)
        if Velocity().distance_too_small(xy1=xy1, xy2=xy2):
            xy2 = self.point_n(4)
        return Velocity().v(xy1=xy1, xy2=xy2)

    def acceleration(self) -> METRIC_TYPE:
        if self.index_too_large():
            return MetricValueUndefined
        xy1 = self.point_n(0)
        xy2 = self.point_n(1)
        xy3 = self.point_n(2)
        return Acceleration().a(xy1=xy1, xy2=xy2, xy3=xy3)


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
            angles.append(angle)
        return angles

    def critical_speeds(self) -> Iterator[float]:
        speeds = []
        for i in self.crit_indices:
            handler = self.point_handler(crit_index=i, all_itxyek=self.all_itxyek)
            speed = handler.velocity()
            speeds.append(speed)
        return speeds

    def critical_accelerations(self) -> Iterator[float]:
        accelerations = []
        for i in self.crit_indices:
            handler = self.point_handler(crit_index=i, all_itxyek=self.all_itxyek)
            acceleration = handler.acceleration()
            accelerations.append(acceleration)
        return accelerations


class ExitMetricsCalc(_MetricsCalculator):
    def __init__(self, all_itxyek: ITXYEK, crit_indices: Iterator[int]):
        super().__init__(all_itxyek=all_itxyek, crit_type=p_types.Exit(), crit_indices=crit_indices)


class EntryMetricsCalc(_MetricsCalculator):
    def __init__(self, all_itxyek: ITXYEK, crit_indices: Iterator[int]):
        super().__init__(all_itxyek=all_itxyek, crit_type=p_types.Entry(), crit_indices=crit_indices)
