from dataclasses import dataclass, field
from itertools import combinations
from typing import List, Iterator, Tuple

from analysis.analysis import ExitMetricsCalc, EntryMetricsCalc
from analysis.conversion import DataExtractor
from analysis.itxy_base import ITXY, ITXYPoint
from analysis.plotting import Plotter
from analysis.point_types import ENTRY_OR_EXIT_TYPE, ExitType, EntryType
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
    def __init__(self, user: User):
        self.user = user

    def _exit_angles(self):
        metrics = ExitMetricsCalc(all_itxy=self.user.all_itxy,
                                  crit_indices=self.user.exit_itxy.indices)
        return metrics.critical_angles()

    def _entry_angles(self):
        metrics = EntryMetricsCalc(all_itxy=self.user.all_itxy,
                                   crit_indices=self.user.entry_itxy.indices)
        return metrics.critical_angles()

    def _exit_speeds(self):
        metrics = ExitMetricsCalc(all_itxy=self.user.all_itxy,
                                  crit_indices=self.user.exit_itxy.indices)
        return metrics.critical_speeds()

    def _entry_speeds(self):
        metrics = EntryMetricsCalc(all_itxy=self.user.all_itxy,
                                   crit_indices=self.user.entry_itxy.indices)
        return metrics.critical_speeds()

    def _exit_accelerations(self):
        metrics = ExitMetricsCalc(all_itxy=self.user.all_itxy,
                                  crit_indices=self.user.exit_itxy.indices)
        return metrics.critical_accelerations()

    def _entry_accelerations(self):
        metrics = EntryMetricsCalc(all_itxy=self.user.all_itxy,
                                   crit_indices=self.user.entry_itxy.indices)
        return metrics.critical_accelerations()

    def calc_and_store_metrics(self) -> None:
        self.user.exit_angles = self._exit_angles()
        self.user.entry_angles = self._entry_angles()
        self.user.exit_speeds = self._exit_speeds()
        self.user.entry_speeds = self._entry_speeds()
        self.user.exit_accelerations = self._exit_accelerations()
        self.user.entry_accelerations = self._entry_accelerations()

    def insert_user(self) -> None:
        all_users.add(self.user)

    def plot_and_show_mouse_movement(self) -> None:
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
class SingleMatch:
    p1: ITXYPoint
    p2: ITXYPoint
    type_p1: ENTRY_OR_EXIT_TYPE
    exit_angle: float
    entry_angle: float
    angles_diff: float = field(init=False)

    def __post_init__(self):
        self.store_angles_diff(self.entry_angle, self.exit_angle)

    def store_angles_diff(self, entry_angle, exit_angle) -> None:
        self.angles_diff = abs(entry_angle - exit_angle)


@dataclass
class Matches:
    user1: User
    user2: User
    exit_to_entry_matches: List[SingleMatch]
    entry_to_exit_matches: List[SingleMatch]


def user_combinations() -> Iterator[Tuple[User, User]]:
    return combinations(all_users, 2)


def is_tor_user(user: User) -> bool:
    """Tor-user times always end in '00'
    because of the 100ms time-resolution imposed in JS."""
    all_modulo = (i % 100 for i in user.all_itxy.time)
    if any(all_modulo):
        return False
    return True


def user_combinations_containing_tor() -> Iterator[Tuple[User, User]]:
    comps = []
    for comp in user_combinations():
        if is_tor_user(comp[0]) or is_tor_user(comp[1]):
            comps.append(comp)
    return comps


class MatchesCreator:
    TOR_RESOLUTION = 100
    MAX_DELTA_T = TOR_RESOLUTION + 20  # milliseconds

    def __init__(self, user1: User, user2: User):
        self.user1 = user1
        self.user2 = user2

    @staticmethod
    def time_diff_in_bounds(p1: ITXYPoint, p2: ITXYPoint) -> float:
        return abs(p1.time - p2.time) <= MatchesCreator.MAX_DELTA_T

    def _single_point_match(self, p1: ITXYPoint, p2: ITXYPoint, type_p1: ENTRY_OR_EXIT_TYPE) -> SingleMatch:
        if self.time_diff_in_bounds(p1, p2):
            # TODO
            p1_angle = self.user1.exit_angles
            return SingleMatch(p1=p1, p2=p2, type_p1=type_p1, entry_angle=..., exit_angle=...)

    def _exit_to_entry_matches(self) -> List[SingleMatch]:
        matches = []
        for p1 in self.user1.exit_itxy.as_points():
            for p2 in self.user2.entry_itxy.as_points():
                matches.append(self._single_point_match(p1=p1, p2=p2, type_p1=ExitType))
        return matches

    def _entry_to_exit_matches(self) -> List[SingleMatch]:
        matches = []
        for p1 in self.user1.entry_itxy.as_points():
            for p2 in self.user2.exit_itxy.as_points():
                matches.append(self._single_point_match(p1=p1, p2=p2, type_p1=EntryType))
        return matches

    def point_matches(self) -> Matches:
        return Matches(user1=self.user1, user2=self.user2,
                       exit_to_entry_matches=self._exit_to_entry_matches(),
                       entry_to_exit_matches=self._entry_to_exit_matches())


def compare_all_users():
    for comp in user_combinations_containing_tor():
        u1, u2 = comp
