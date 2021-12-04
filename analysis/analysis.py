from typing import Type, Union

from analysis.metrics_base import ITXY
from analysis.point_types import ExitOrEntryType, ExitType, EntryType
from analysis.points import ExitHandler, EntryHandler

TOR_RESOLUTION = 100
MAX_DELTA_TIME = TOR_RESOLUTION + 20


class _Metrics:
    def __init__(self, all_itxy: ITXY, crit_type: Type[ExitOrEntryType], crit_indices):
        self.crit_indices = crit_indices
        self.crit_type = crit_type
        self.all_itxy = all_itxy
        self.point_handler: Type[Union[ExitHandler, EntryHandler]] = self._point_handler()

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


class ExitMetrics(_Metrics):
    def __init__(self, all_itxy: ITXY, crit_indices):
        super().__init__(all_itxy=all_itxy, crit_type=ExitType, crit_indices=crit_indices)


class EntryMetrics(_Metrics):
    def __init__(self, all_itxy: ITXY, crit_indices):
        super().__init__(all_itxy=all_itxy, crit_type=EntryType, crit_indices=crit_indices)
