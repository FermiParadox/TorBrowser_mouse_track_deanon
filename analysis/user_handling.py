from dataclasses import dataclass, field
from itertools import combinations
from typing import List, Iterator, Tuple, Set, Union, Collection

from analysis.metrics import ExitMetricsCalc, EntryMetricsCalc
from analysis.conversion import DataExtractor
from analysis.itwva_base import IWVAE
from analysis.itxye_base import ITXYEPoint
from analysis.plotting import Plotter
from analysis.point_types import EntryOrExitType, EXIT_TYPE, ENTRY_TYPE
from analysis.user_base import User


class AllUsers(set):
    @property
    def ips(self):
        return {str(u.ip) for u in self}

    @property
    def ids(self):
        return {str(u.id) for u in self}

    def add(self, other: User) -> None:
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

    def user(self) -> User:
        extractor = DataExtractor(req=self.req)
        return User(id=extractor.user_id(),
                    ip=extractor.user_ip(),
                    all_itxye=extractor.itxye_lists(),
                    exit_metrics=IWVAE(),
                    entry_metrics=IWVAE())


class UserHandler:
    def __init__(self, user: User):
        self.user = user

    def insert_user(self) -> None:
        all_users.add(self.user)

    def _exit_angles(self) -> Iterator[float]:
        metrics = ExitMetricsCalc(all_itxye=self.user.all_itxye,
                                  crit_indices=self.user.exit_indices)
        return metrics.critical_angles()

    def _entry_angles(self) -> Iterator[float]:
        metrics = EntryMetricsCalc(all_itxye=self.user.all_itxye,
                                   crit_indices=self.user.entry_indices)
        return metrics.critical_angles()

    def _exit_speeds(self) -> Iterator[float]:
        metrics = ExitMetricsCalc(all_itxye=self.user.all_itxye,
                                  crit_indices=self.user.exit_indices)
        return metrics.critical_speeds()

    def _entry_speeds(self) -> Iterator[float]:
        metrics = EntryMetricsCalc(all_itxye=self.user.all_itxye,
                                   crit_indices=self.user.entry_indices)
        return metrics.critical_speeds()

    def _exit_accelerations(self) -> Iterator[float]:
        metrics = ExitMetricsCalc(all_itxye=self.user.all_itxye,
                                  crit_indices=self.user.exit_indices)
        return metrics.critical_accelerations()

    def _entry_accelerations(self) -> Iterator[float]:
        metrics = EntryMetricsCalc(all_itxye=self.user.all_itxye,
                                   crit_indices=self.user.entry_indices)
        return metrics.critical_accelerations()

    def calc_and_store_metrics(self) -> None:
        exit_metrics = self.user.exit_metrics
        exit_metrics.indices = [p.index for p in self.user.all_itxye.as_points() if p.e == EXIT_TYPE]
        exit_metrics.v = self._exit_speeds()
        exit_metrics.w = self._exit_angles()
        exit_metrics.a = self._exit_accelerations()
        exit_metrics.e = [EXIT_TYPE for _ in exit_metrics.indices]

        entry_metrics = self.user.entry_metrics
        entry_metrics.indices = [p.index for p in self.user.all_itxye.as_points() if p.e == ENTRY_TYPE]
        entry_metrics.v = self._entry_speeds()
        entry_metrics.w = self._entry_angles()
        entry_metrics.a = self._entry_accelerations()
        entry_metrics.e = [ENTRY_TYPE for _ in entry_metrics.indices]

    def plot_and_show_mouse_movement(self) -> None:
        x_all = self.user.all_itxye.x
        y_all = self.user.all_itxye.y

        plotter = Plotter(user_id=self.user.id)
        plotter.plot_all_x_y(x=x_all, y=y_all)

        exit_x_list = self.user.exit_x
        exit_y_list = self.user.exit_y
        plotter.plot_exit_xy(x=exit_x_list, y=exit_y_list)

        entry_x_list = self.user.entry_x
        entry_y_list = self.user.entry_y
        plotter.plot_entry_xy(x=entry_x_list, y=entry_y_list)

        plotter.decorate_graphs_and_show()


@dataclass
class PointMatch:
    """
    Stores data related an exit and entry point of two user_IDs,
    when they appear to be coming from the same user.
    """
    p1: ITXYEPoint
    p2: ITXYEPoint
    type_p1: EntryOrExitType
    dt: float
    exit_w: float
    entry_w: float
    dw: float = field(init=False)

    def __post_init__(self):
        self.store_dw(self.entry_w, self.exit_w)

    def store_dw(self, entry_w, exit_w) -> None:
        self.dw = exit_w - entry_w


def is_tor_user(user: User) -> bool:
    """Tor-user times always end in '00'
    because of the 100ms time-resolution imposed in JS."""
    all_modulo = (i % 100 for i in user.all_itxye.time)
    if any(all_modulo):
        return False
    return True


class Combinations:
    USER_COMBS_TYPE = Iterator[Tuple[User, User]]

    @staticmethod
    def user_combs(users_iter: Collection[User]) -> USER_COMBS_TYPE:
        return combinations(users_iter, 2)

    @staticmethod
    def _tor_user_combs(all_combs: USER_COMBS_TYPE) -> USER_COMBS_TYPE:
        combs = []
        for pair in all_combs:
            u1, u2 = list(pair)
            if is_tor_user(u1):
                combs.append(pair)
            elif is_tor_user(u2):
                combs.append(pair[::-1])
        return combs

    @staticmethod
    def tor_user_combs(users_iter: Collection[User]) -> USER_COMBS_TYPE:
        all_combs = Combinations.user_combs(users_iter=users_iter)
        return Combinations._tor_user_combs(all_combs=all_combs)


@dataclass
class UserMatch:
    user1: User
    user2: User
    exit_to_entry_matches: List[PointMatch]
    entry_to_exit_matches: List[PointMatch]


all_matches: Set[UserMatch] = set()
matches_within_range: Set[UserMatch] = set()


class UserMatchCreator:
    # In milliseconds
    TOR_RESOLUTION = 100
    MAX_DELTA_T = TOR_RESOLUTION + 20
    MIN_DELTA_T = -20

    def __init__(self, user1: User, user2: User):
        self.user1 = user1
        self.user2 = user2

    @staticmethod
    def dt(p1: ITXYEPoint, p2: ITXYEPoint) -> int:
        return p2.time - p1.time

    @staticmethod
    def dt_in_bounds(dt: int) -> bool:
        return UserMatchCreator.MIN_DELTA_T <= dt <= UserMatchCreator.MAX_DELTA_T

    def _single_point_match(self, p1: ITXYEPoint, p2: ITXYEPoint, type_p1: EntryOrExitType) -> PointMatch:
        dt = self.dt(p1=p1, p2=p2)
        if self.dt_in_bounds(dt=dt):
            p1_i = p1.index
            p2_i = p2.index
            if type_p1 == EXIT_TYPE:
                exit_w = self.user1.exit_metrics.w[p1_i]
                entry_w = self.user2.entry_metrics.w[p2_i]
            else:
                entry_w = self.user1.entry_metrics.w[p1_i]
                exit_w = self.user2.exit_metrics.w[p2_i]
            return PointMatch(p1=p1, p2=p2, type_p1=type_p1, dt=dt, entry_w=entry_w, exit_w=exit_w)

    def _exit_to_entry_matches(self) -> List[PointMatch]:
        matches = []
        for p1 in self.user1.exit_itxye.as_points():
            for p2 in self.user2.entry_itxye.as_points():
                matches.append(self._single_point_match(p1=p1, p2=p2, type_p1=EXIT_TYPE))
        return matches

    def _entry_to_exit_matches(self) -> List[PointMatch]:
        matches = []
        for p1 in self.user1.entry_itxye.as_points():
            for p2 in self.user2.exit_itxye.as_points():
                matches.append(self._single_point_match(p1=p1, p2=p2, type_p1=ENTRY_TYPE))
        return matches

    def user_match(self) -> UserMatch:
        return UserMatch(user1=self.user1, user2=self.user2,
                         exit_to_entry_matches=self._exit_to_entry_matches(),
                         entry_to_exit_matches=self._entry_to_exit_matches())

    def insert_match(self) -> None:
        all_matches.add(self.user_match())


class UserMatchHandler:

    @staticmethod
    def insert_all_matches() -> None:
        for comb in Combinations.tor_user_combs(users_iter=all_users):
            tor_u1, u2 = comb
            match_creator = UserMatchCreator(user1=tor_u1, user2=u2)
            match_creator.insert_match()

    def insert_matches_within_range(self) -> None:
        pass