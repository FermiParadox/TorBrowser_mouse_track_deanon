from typing import Type, Union

from analysis.metrics_dataclasses import TimesXY
from analysis.point_types import ExitOrEntryType, ExitType, EntryType
from analysis.points import ExitHandler, EntryHandler

TOR_RESOLUTION_MILLISECONDS = 100
MAX_DELTA_MILLISECONDS = TOR_RESOLUTION_MILLISECONDS + 20


class _Metrics:
    def __init__(self, all_txy: TimesXY, crit_type: Type[ExitOrEntryType], crit_indices):
        self.crit_indices = crit_indices
        self.crit_type = crit_type
        self.all_txy = all_txy
        self.point_handler: Type[Union[ExitHandler, EntryHandler]] = self._point_handler()

    def _point_handler(self):
        if self.crit_type == ExitType:
            return ExitHandler
        else:
            return EntryHandler

    def critical_angles(self):
        angles = []
        for i in self.crit_indices:
            handler = self.point_handler(crit_index=i, all_txy=self.all_txy)
            angle = handler.critical_angle
            if angle:
                angles.append(angle)
        return angles

    def critical_speeds(self):
        speeds = []
        for i in self.crit_indices:
            handler = self.point_handler(crit_index=i, all_txy=self.all_txy)
            speed = handler.critical_speed
            speeds.append(speed)
        return speeds

    def critical_accelerations(self):
        accelerations = []
        for i in self.crit_indices:
            handler = self.point_handler(crit_index=i, all_txy=self.all_txy)
            acceleration = handler.critical_acceleration
            accelerations.append(acceleration)
        return accelerations


class ExitMetrics(_Metrics):
    def __init__(self, all_txy: TimesXY, crit_indices):
        super().__init__(all_txy=all_txy, crit_type=ExitType, crit_indices=crit_indices)


class EntryMetrics(_Metrics):
    def __init__(self, all_txy: TimesXY, crit_indices):
        super().__init__(all_txy=all_txy, crit_type=EntryType, crit_indices=crit_indices)


class TimeDifferences:
    def __init__(self, exit_user, entry_user):
        self.exit_user = exit_user
        self.entry_user = entry_user
