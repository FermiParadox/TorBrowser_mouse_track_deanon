from dataclasses import dataclass, field
from itertools import combinations

from analysis.analysis import ExitMetrics, EntryMetrics
from analysis.conversion import DataExtractor
from analysis.metrics_base import ITXY, ITXYPoint
from analysis.plotting import Plotter
from analysis.point_types import ENTRY_OR_EXIT_TYPE
from analysis.user_base import User


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

        By default, `add` has no effect if the element is already present,
        meaning new data points wouldn't be stored."""
        self.discard(other)
        super().add(other)


all_users = AllUsers()


class UserCreator:
    def __init__(self, req):
        self.req = req
        self.user: User

    def user(self):
        extractor = DataExtractor(req=self.req)

        return User(id=extractor.user_id,
                    ip=extractor.user_ip,
                    all_itxy=extractor.itxy_lists,
                    entry_itxy=extractor.entry_itxy,
                    exit_itxy=extractor.exit_itxy)


class UserHandler:
    def __init__(self, user):
        self.user: User = user

    def _exit_angles(self):
        metrics = ExitMetrics(all_itxy=self.user.all_itxy,
                              crit_indices=self.user.exit_itxy.indices)
        return metrics.critical_angles()

    def _entry_angles(self):
        metrics = EntryMetrics(all_itxy=self.user.all_itxy,
                               crit_indices=self.user.entry_itxy.indices)
        return metrics.critical_angles()

    def _exit_speeds(self):
        metrics = ExitMetrics(all_itxy=self.user.all_itxy,
                              crit_indices=self.user.exit_itxy.indices)
        return metrics.critical_speeds()

    def _entry_speeds(self):
        metrics = EntryMetrics(all_itxy=self.user.all_itxy,
                               crit_indices=self.user.entry_itxy.indices)
        return metrics.critical_speeds()

    def _exit_accelerations(self):
        metrics = ExitMetrics(all_itxy=self.user.all_itxy,
                              crit_indices=self.user.exit_itxy.indices)
        return metrics.critical_accelerations()

    def _entry_accelerations(self):
        metrics = EntryMetrics(all_itxy=self.user.all_itxy,
                               crit_indices=self.user.entry_itxy.indices)
        return metrics.critical_accelerations()

    def calc_and_store_metrics(self):
        self.user.exit_angles = self._exit_angles()
        self.user.entry_angles = self._entry_angles()
        self.user.exit_speeds = self._exit_speeds()
        self.user.entry_speeds = self._entry_speeds()
        self.user.exit_accelerations = self._exit_accelerations()
        self.user.entry_accelerations = self._entry_accelerations()

    def insert_user(self):
        all_users.add(self.user)

    def plot_and_show_mouse_movement(self):
        x_all = self.user.all_itxy.x
        y_all = self.user.all_itxy.y

        plotter = Plotter(user_id=self.user.id)
        plotter.plot_all_x_y(x=x_all, y=y_all)

        exit_x_list = self.user.exit_itxy.x
        exit_y_list = self.user.exit_itxy.y
        plotter.plot_exit_xy(x=exit_x_list, y=exit_y_list)

        entry_x_list = self.user.entry_itxy.x
        entry_y_list = self.user.entry_itxy.y
        plotter.plot_entry_xy(x=entry_x_list, y=entry_y_list)

        plotter.decorate_graphs_and_show()


@dataclass
class Comparison:
    user1: User
    user2: User
    matched_exits: int
    matched_entries: int


@dataclass
class PointMatch:
    p1: ITXYPoint
    p2: ITXYPoint
    type_p1: ENTRY_OR_EXIT_TYPE

    exit_angle: float = field(init=False)
    entry_angle: float = field(init=False)
    angles_diff: float = field(init=False)

    def store_angles_diff(self, entry_angle, exit_angle):
        self.angles_diff = abs(entry_angle - exit_angle)


@dataclass
class PointMatches:
    user1: User
    user2: User
    exit_to_entry_matches: list
    entry_to_exit_matches: list


def user_combinations():
    return combinations(all_users, 2)


def is_tor_user(user: User):
    """Tor-user times always end in '00'
    because of the 100ms time-resolution imposed in JS."""
    all_modulo = (i % 100 for i in user.all_itxy.time)
    if any(all_modulo):
        return False
    return True


def user_combinations_containing_tor():
    comps = []
    for comp in user_combinations():
        if is_tor_user(comp[0]) or is_tor_user(comp[1]):
            comps.append(comp)
    return comps


class PointMatchCreator:
    MAX_DELTA_T = 120  # milliseconds

    def __init__(self, user1: User, user2: User, index: int, entry_or_exit_type: ENTRY_OR_EXIT_TYPE):
        self.index = index
        self.entry_or_exit_type = entry_or_exit_type
        self.user2 = user2
        self.user1 = user1

    @staticmethod
    def time_diff_in_bounds(p1: ITXYPoint, p2: ITXYPoint):
        return abs(p1.time - p2.time) <= PointMatchCreator.MAX_DELTA_T

    def single_point_match(self, p1, p2):
        if self.time_diff_in_bounds(p1, p2):
            return PointMatch(p1=p1, p2=p2, type_p1=self.entry_or_exit_type)

    def point_matches(self):
        exit_to_entry_matches = []
        for p1 in self.user1.exit_itxy.as_points():
            for p2 in self.user2.entry_itxy.as_points():
                exit_to_entry_matches.append(self.single_point_match(p1=p1, p2=p2))

        entry_to_exit_matches = []
        for p1 in self.user1.entry_itxy.as_points():
            for p2 in self.user2.exit_itxy.as_points():
                entry_to_exit_matches.append(self.single_point_match(p1=p1, p2=p2))

        all_matches = PointMatches(user1=self.user1, user2=self.user2,
                                   exit_to_entry_matches=exit_to_entry_matches,
                                   entry_to_exit_matches=entry_to_exit_matches)

        return all_matches

