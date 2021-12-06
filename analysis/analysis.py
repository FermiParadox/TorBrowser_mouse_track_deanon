from analysis.itxy_base import ITXY
from analysis.point_types import ExitType, EntryType, ENTRY_OR_EXIT_TYPE

from analysis.points import ExitHandler, EntryHandler, ENTRY_OR_EXIT_HANDLER


class _MetricsCalculator:
    def __init__(self, all_itxy: ITXY, crit_type: ENTRY_OR_EXIT_TYPE, crit_indices):
        self.crit_indices = crit_indices
        self.crit_type = crit_type
        self.all_itxy = all_itxy
        self.point_handler: ENTRY_OR_EXIT_HANDLER = self._point_handler()

    def _point_handler(self):
        if self.crit_type == ExitType:
            return ExitHandler
        else:
            return EntryHandler

    def critical_angles(self):
        angles = []
        for i in self.crit_indices:
            handler = self.point_handler(crit_index=i, all_itxy=self.all_itxy)
            angle = handler.angle
            if angle:
                angles.append(angle)
        return angles

    def critical_speeds(self):
        speeds = []
        for i in self.crit_indices:
            handler = self.point_handler(crit_index=i, all_itxy=self.all_itxy)
            speed = handler.speed
            speeds.append(speed)
        return speeds

    def critical_accelerations(self):
        accelerations = []
        for i in self.crit_indices:
            handler = self.point_handler(crit_index=i, all_itxy=self.all_itxy)
            acceleration = handler.acceleration
            accelerations.append(acceleration)
        return accelerations


class ExitMetricsCalc(_MetricsCalculator):
    def __init__(self, all_itxy: ITXY, crit_indices):
        super().__init__(all_itxy=all_itxy, crit_type=ExitType, crit_indices=crit_indices)


class EntryMetricsCalc(_MetricsCalculator):
    def __init__(self, all_itxy: ITXY, crit_indices):
        super().__init__(all_itxy=all_itxy, crit_type=EntryType, crit_indices=crit_indices)
