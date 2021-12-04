import secrets
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address
from typing import Union, List

from analysis.analysis import EntryMetrics, ExitMetrics
from analysis.metrics_dataclasses import TimesXY
from analysis.plotting import Plotter

IPv6_or_IPv4_obj = Union[IPv4Address, IPv6Address]


class IDGenerator:
    MAX_ID_NUM = 10 ** 9
    IDs_Used = set()

    @staticmethod
    def unique_id():
        while 1:
            generated_id = secrets.randbelow(IDGenerator.MAX_ID_NUM)
            if generated_id not in IDGenerator.IDs_Used:
                return generated_id


@dataclass
class User:
    id: int
    ip: IPv6_or_IPv4_obj
    all_txy: TimesXY
    exit_txy_lists: TimesXY  # last point of position stored, before browser switching
    entry_txy_lists: TimesXY  # first point after refocusing browser
    exit_indices: List[int]
    entry_indices: List[int]

    def __post_init__(self):
        self.exit_times = self.exit_txy_lists.time
        self.entry_times = self.entry_txy_lists.time

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def _exit_angles(self):
        metrics = ExitMetrics(all_txy=self.all_txy,
                              crit_indices=self.exit_indices)
        return metrics.critical_angles()

    def _entry_angles(self):
        metrics = EntryMetrics(all_txy=self.all_txy,
                               crit_indices=self.entry_indices)
        return metrics.critical_angles()

    def _exit_speeds(self):
        metrics = ExitMetrics(all_txy=self.all_txy,
                              crit_indices=self.exit_indices)
        return metrics.critical_speeds()

    def _entry_speeds(self):
        metrics = EntryMetrics(all_txy=self.all_txy,
                               crit_indices=self.entry_indices)
        return metrics.critical_speeds()

    def _exit_accelerations(self):
        metrics = ExitMetrics(all_txy=self.all_txy,
                              crit_indices=self.exit_indices)
        return metrics.critical_accelerations()

    def _entry_accelerations(self):
        metrics = EntryMetrics(all_txy=self.all_txy,
                               crit_indices=self.entry_indices)
        return metrics.critical_accelerations()

    def calc_and_store_metrics(self):
        self.exit_angles = self._exit_angles()
        self.entry_angles = self._entry_angles()
        self.exit_speeds = self._exit_speeds()
        self.entry_speeds = self._entry_speeds()
        self.exit_accelerations = self._exit_accelerations()
        self.entry_accelerations = self._entry_accelerations()

    def plot_and_show_mouse_movement(self):
        x_all = self.all_txy.x
        y_all = self.all_txy.y

        plotter = Plotter(user_id=self.id)
        plotter.plot_all_x_y(x=x_all, y=y_all)

        exit_x_list = self.exit_txy_lists.x
        exit_y_list = self.exit_txy_lists.y
        plotter.plot_exit_xy(x=exit_x_list, y=exit_y_list)

        entry_x_list = self.entry_txy_lists.x
        entry_y_list = self.entry_txy_lists.y
        plotter.plot_entry_xy(x=entry_x_list, y=entry_y_list)

        plotter.decorate_graphs_and_show()
