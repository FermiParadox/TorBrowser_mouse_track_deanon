from typing import Iterator

from analysis.itxye_base import ITXYE
from analysis.point_types import EXIT_TYPE, ENTRY_TYPE, EntryOrExitType

from analysis.points import ExitHandler, EntryHandler, ENTRY_OR_EXIT_HANDLER, MetricValueUndefined


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
