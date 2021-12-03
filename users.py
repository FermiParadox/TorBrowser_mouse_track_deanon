import secrets
from ipaddress import IPv4Address, IPv6Address
from dataclasses import dataclass
from typing import Union, List

from data_converter import MouseDataExtractor
from metrics_dataclasses import TimesXY, TimeKeys, XY
from plotting import Plotter
from points import Metrics
from point_types import ExitType, EntryType

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
    # Mouse
    mouse_txy: TimesXY
    exit_txy_lists: TimesXY  # last point of mouse position stored, before browser switching
    entry_txy_lists: TimesXY  # first point after refocusing browser
    exit_indices: List[int]
    entry_indices: List[int]
    # Keyboard
    time_keys: TimeKeys

    def __post_init__(self):
        self.mouse_exit_times = self.exit_txy_lists.time
        self.mouse_entry_times = self.entry_txy_lists.time

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def exit_angles(self):
        metrics = Metrics(mouse_txy=self.mouse_txy,
                          crit_type=ExitType,
                          crit_indices=self.exit_indices)
        return metrics.critical_angles()

    def entry_angles(self):
        metrics = Metrics(mouse_txy=self.mouse_txy,
                          crit_type=EntryType,
                          crit_indices=self.entry_indices)
        return metrics.critical_angles()

    def exit_speeds(self):
        metrics = Metrics(mouse_txy=self.mouse_txy,
                          crit_type=ExitType,
                          crit_indices=self.exit_indices)
        return metrics.critical_speeds()

    def entry_speeds(self):
        metrics = Metrics(mouse_txy=self.mouse_txy,
                          crit_type=EntryType,
                          crit_indices=self.entry_indices)
        return metrics.critical_speeds()

    def exit_accelerations(self):
        metrics = Metrics(mouse_txy=self.mouse_txy,
                          crit_type=ExitType,
                          crit_indices=self.exit_indices)
        return metrics.critical_accelerations()

    def entry_accelerations(self):
        metrics = Metrics(mouse_txy=self.mouse_txy,
                          crit_type=EntryType,
                          crit_indices=self.entry_indices)
        return metrics.critical_accelerations()

    def plot_and_show_mouse_movement(self):
        x_all = self.mouse_txy.x
        y_all = self.mouse_txy.y

        plotter = Plotter(user_id=self.id)
        plotter.plot_all_x_y(x=x_all, y=y_all)

        entry_x_list = self.entry_txy_lists.x
        entry_y_list = self.entry_txy_lists.y
        plotter.plot_entry_xy(x=entry_x_list, y=entry_y_list)

        exit_x_list = self.exit_txy_lists.x
        exit_y_list = self.exit_txy_lists.y
        plotter.plot_exit_xy(x=exit_x_list, y=exit_y_list)

        plotter.decorate_graphs_and_show()


class AllUsers(set):
    @property
    def ips(self):
        return {str(u.ip) for u in self}

    @property
    def ids(self):
        return {str(u.id) for u in self}

    def add(self, other: User):
        """When added element is already present, it replaces the existing one,
        instead of "editing" it.
        Not very efficient, but should be ok for testing.

        By default `add` has no effect if the element is already present,
        meaning new data points wouldn't be stored."""
        self.discard(other)
        super().add(other)


all_users = AllUsers()


class UserHandler:
    def __init__(self, req):
        self.req = req
        self.user: User

    def _created_user(self):
        extractor = MouseDataExtractor(req=self.req)

        return User(id=extractor.user_id,
                    ip=extractor.user_ip,
                    mouse_txy=extractor.txy_lists,
                    entry_txy_lists=extractor.entry_txy,
                    exit_txy_lists=extractor.exit_txy,
                    exit_indices=extractor.exit_indices(),
                    entry_indices=extractor.entry_indices(),
                    time_keys=TimeKeys())

    def create_and_insert_user(self):
        self.user = self._created_user()
        all_users.add(self.user)
