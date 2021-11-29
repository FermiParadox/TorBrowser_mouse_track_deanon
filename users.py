import secrets
from ipaddress import IPv4Address, IPv6Address
from dataclasses import dataclass
from typing import Union

from data_converter import MouseDataExtractor
from metrics_dataclasses import TimeXY, TimeKeys, XY
from plotting import Plotter
from points import PointsHandler, CriticalPointType

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
    mouse_txy: TimeXY
    mouse_exit_txy_lists: TimeXY  # last point of mouse position stored, before browser switching
    mouse_entry_txy_lists: TimeXY  # first point after refocusing browser
    time_keys: TimeKeys

    def __post_init__(self):
        self.mouse_exit_times = self.mouse_exit_txy_lists.time
        self.mouse_entry_times = self.mouse_entry_txy_lists.time

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def exit_angles(self):
        handler = PointsHandler(mouse_txy=self.mouse_txy,
                                crit_type=CriticalPointType.EXIT,
                                mouse_crit_t=self.mouse_exit_times)
        return handler.critical_angles()

    def entry_angles(self):
        handler = PointsHandler(mouse_txy=self.mouse_txy,
                                crit_type=CriticalPointType.ENTRY,
                                mouse_crit_t=self.mouse_entry_times)
        return handler.critical_angles()

    def exit_speeds(self):
        handler = PointsHandler(mouse_txy=self.mouse_txy,
                                crit_type=CriticalPointType.EXIT,
                                mouse_crit_t=self.mouse_exit_times)
        return handler.critical_speeds()

    def entry_speeds(self):
        handler = PointsHandler(mouse_txy=self.mouse_txy,
                                crit_type=CriticalPointType.ENTRY,
                                mouse_crit_t=self.mouse_entry_times)
        return handler.critical_speeds()

    def exit_accelerations(self):
        handler = PointsHandler(mouse_txy=self.mouse_txy,
                                crit_type=CriticalPointType.EXIT,
                                mouse_crit_t=self.mouse_exit_times)
        return handler.critical_accelerations()

    def entry_accelerations(self):
        handler = PointsHandler(mouse_txy=self.mouse_txy,
                                crit_type=CriticalPointType.ENTRY,
                                mouse_crit_t=self.mouse_entry_times)
        return handler.critical_accelerations()

    def plot_and_show_mouse_movement(self):
        x_all = self.mouse_txy.x
        y_all = self.mouse_txy.y

        plotter = Plotter(user_id=self.id)
        plotter.plot_all_x_y(x=x_all, y=y_all)

        entry_x_list = self.mouse_entry_txy_lists.x
        entry_y_list = self.mouse_entry_txy_lists.y
        plotter.plot_entry_x_y(x=entry_x_list, y=entry_y_list)

        exit_x_list = self.mouse_exit_txy_lists.x
        exit_y_list = self.mouse_exit_txy_lists.y
        plotter.plot_exit_x_y(x=exit_x_list, y=exit_y_list)

        plotter.decorate_graphs_and_show()


class AllUsers(set):
    @property
    def ips(self):
        return {str(u.ip) for u in self}

    @property
    def ids(self):
        return {str(u.id) for u in self}

    def add(self, other: User):
        """When added element is already present, it replaces the existing one.
        Not very efficient, but should be ok for testing.

        By default `add` has no effect if the element is already present,
        meaning new data points wouldn't be stored."""
        self.discard(other)
        super().add(other)


all_users = AllUsers()


class UserHandler:
    def __init__(self, req):
        self.req = req
        self.user_id = None
        self.mouse_exit_t = None
        self.mouse_exit_xy_lists: XY
        self.mouse_entry_xy_lists: XY
        self.user: User
        self.ip = None

    def _extract_data(self):
        extractor = MouseDataExtractor(req=self.req)
        self.ip = extractor.user_ip
        self.mouse_exit_t = extractor.exit_times
        self.mouse_entry_t = extractor.entry_times
        self.mouse_exit_xy_lists = extractor.exit_xy_lists
        self.mouse_entry_xy_lists = extractor.entry_xy_lists
        self.user_id = extractor.user_id
        self.txy_lists = extractor.txy_lists

    def _create_user(self):
        t, x, y = self.txy_lists
        mouse_txy = TimeXY(time=t, x=x, y=y)

        exit_xy = self.mouse_exit_xy_lists
        mouse_exit_txy_lists = TimeXY(time=self.mouse_exit_t, x=exit_xy[0], y=exit_xy[1])

        entry_xy = self.mouse_entry_xy_lists
        mouse_entry_txy_lists = TimeXY(time=self.mouse_entry_t, x=entry_xy[0], y=entry_xy[1])

        self.user = User(id=self.user_id,
                         ip=self.ip,
                         mouse_txy=mouse_txy,
                         mouse_entry_txy_lists=mouse_entry_txy_lists,
                         mouse_exit_txy_lists=mouse_exit_txy_lists,
                         time_keys=TimeKeys())

    def create_user(self):
        self._extract_data()
        self._create_user()

    def create_and_insert_user(self):
        all_users.add(self.user)
