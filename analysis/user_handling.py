from dataclasses import dataclass, field
from itertools import combinations
from typing import List, Iterator, Tuple, Collection

from scipy.spatial import distance

from analysis.metrics import ExitMetricsCalc, EntryMetricsCalc
from analysis.str_parser import DataExtractor
from analysis.iwvae_base import IWVAE
from analysis.itxye_base import ITXYEPoint, XYPoint
from analysis.plotting import Plotter
from analysis.point_types import EntryExitType, EXIT_TYPE, ENTRY_TYPE
from analysis.user_base import User


class ReAddingSet(set):
    def add(self, other) -> None:
        """When added element is already present, it replaces the existing one,
        instead of "editing" it.
        Not very efficient, but should be ok for testing.

        By default, `add` has no effect if the element is already present,
        meaning new data points wouldn't be stored."""
        self.discard(other)
        super().add(other)


class AllUsers(ReAddingSet):
    @property
    def ips(self):
        return {str(u.ip) for u in self}

    @property
    def ids(self):
        return {str(u.id) for u in self}

    def add(self, other: User) -> None:
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


def is_tor_user(user: User) -> bool:
    """Tor-user times always end in '00'
    because of the 100ms time-resolution imposed in JS."""
    all_modulo = (i % 100 for i in user.all_itxye.time)
    if any(all_modulo):
        return False
    return True


def are_tor_users(users: Collection[User]) -> bool:
    return all(is_tor_user(u) for u in users)


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
    def tor_users_combs(users_iter: Collection[User]) -> USER_COMBS_TYPE:
        # all_combs = Combinations.user_combs(users_iter=users_iter)
        # TODO temp disable, revert.   v
        return Combinations.user_combs(users_iter=users_iter)


class PointMatchLimits:
    MAX_DW = 30
    # Velocity and acceleration differences
    #   are probably not very relevant.
    MAX_DV = 50
    MAX_DA = 50
    # Assuming the user usually stops moving during CTR TAB
    #   this can be set to 1 (it would reduce false positives).
    MAX_DS_FOR_TOR_USERS = 10


@dataclass
class PointMatch:
    """
    Stores data related an exit and entry point of two user_IDs,
    when they appear to be coming from the same user.
    """
    p1: ITXYEPoint
    p2: ITXYEPoint
    dt: float
    exit_w: float
    entry_w: float
    exit_v: float
    entry_v: float
    exit_a: float
    entry_a: float
    both_tor_users: bool
    dw: float = field(init=False, default=None)
    dv: float = field(init=False, default=None)
    da: float = field(init=False, default=None)
    # dx, dy meaningful only when using CTR TAB in Tor.
    #   That is, both userIDs belong to the same Tor browser.
    dx: float = field(init=False, default=None)
    dy: float = field(init=False, default=None)

    valid_match: bool = field(init=False, default=False)

    def __post_init__(self):
        self.store_dw(self.entry_w, self.exit_w)
        self.store_dv(self.entry_v, self.exit_v)
        self.store_da(self.entry_a, self.exit_a)
        self.dx = self._dx()
        self.dy = self._dy()
        self.valid_match = self._valid_match()

    def store_dw(self, entry_w, exit_w) -> None:
        self.dw = exit_w - entry_w

    def store_dv(self, entry_v, exit_v) -> None:
        self.dv = exit_v - entry_v

    def _dx(self):
        return self.p2.x - self.p1.x

    def _dy(self):
        return self.p2.y - self.p1.y

    def store_da(self, entry_a, exit_a) -> None:
        self.da = exit_a - entry_a

    def _valid_match_tor_plus_normal(self) -> bool:
        if abs(self.dw) <= PointMatchLimits.MAX_DW:
            if abs(self.dv) <= PointMatchLimits.MAX_DV:
                if abs(self.da) <= PointMatchLimits.MAX_DA:
                    return True
        return False

    def _valid_match_both_tor(self) -> bool:
        """
        When both userIDs belong to the same Tor Browser
        the x,y-axis of both tabs are nearly identical.

        There might be a small difference if the mouse was moving
        during the key press.
        """
        ds = distance.euclidean(self.dx, self.dy)
        if ds <= PointMatchLimits.MAX_DS_FOR_TOR_USERS:
            return True
        return False

    def _valid_match(self) -> bool:
        if self.both_tor_users:
            return self._valid_match_both_tor()
        return self._valid_match_tor_plus_normal()


@dataclass
class UsersPair:
    user1: User
    user2: User
    exit_to_entry_matches: List[PointMatch]
    entry_to_exit_matches: List[PointMatch]

    center_mass1: XYPoint = field(init=False, default=None)
    center_mass2: XYPoint = field(init=False, default=None)
    match_id: str = field(init=False, default=None)

    def __post_init__(self):
        self.match_id = f"{self.user1.id},{self.user2.id}"

    def __eq__(self, other):
        return self.match_id == other.match_id

    def __hash__(self):
        return hash(self.match_id)


class UserPairsSet(ReAddingSet):
    def add(self, other: UsersPair) -> None:
        super().add(other)

    def print_pairs(self) -> None:
        print("=" * 60)
        print("All pairs matched:")
        for m in self:
            print("=" * 30)
            print("Exit points matched")
            for p in m.exit_to_entry_matches:
                print("-" * 15)
                print(f"dt = {p.dt}")
                print(f"dw = {p.dw}")
                print(f"dv = {p.dv}")
                print(f"da = {p.da}")
            print("=" * 30)
            print("Entry points matched")
            for p in m.entry_to_exit_matches:
                print("-" * 15)
                print(f"dt = {p.dt}")
                print(f"dw = {p.dw}")
                print(f"dv = {p.dv}")
                print(f"da = {p.da}")


all_matches = UserPairsSet()


class UserMatchCreator:
    # In milliseconds
    TOR_RESOLUTION = 100
    POSSIBLE_BROWSER_ERROR_ON_SAME_MACHINE = 5
    DEAD_ZONE_TIME = 20  # mouse between the two browsers
    MAX_DELTA_T = TOR_RESOLUTION + POSSIBLE_BROWSER_ERROR_ON_SAME_MACHINE + DEAD_ZONE_TIME
    MIN_DELTA_T = - POSSIBLE_BROWSER_ERROR_ON_SAME_MACHINE

    def __init__(self, user1: User, user2: User):
        self.user1 = user1
        self.user2 = user2
        self.both_tor_users = are_tor_users([user1, user2])

    @staticmethod
    def dt(p1: ITXYEPoint, p2: ITXYEPoint, type_p1: EntryExitType) -> int:
        if type_p1 == EXIT_TYPE:
            p_out = p1
            p_in = p2
        else:
            p_out = p2
            p_in = p1
        return p_in.time - p_out.time

    @staticmethod
    def dt_in_bounds(dt: int) -> bool:
        return UserMatchCreator.MIN_DELTA_T <= dt <= UserMatchCreator.MAX_DELTA_T

    def _single_point_match(self, p1: ITXYEPoint, p2: ITXYEPoint, type_p1: EntryExitType) -> PointMatch:
        dt = self.dt(p1=p1, p2=p2, type_p1=type_p1)
        if self.dt_in_bounds(dt=dt):
            p1_i = p1.index
            p2_i = p2.index
            if type_p1 == EXIT_TYPE:
                exit_p = self.user1.exit_metrics.get_point_by_index(index=p1_i)
                entry_p = self.user2.entry_metrics.get_point_by_index(index=p2_i)
            else:
                entry_p = self.user1.entry_metrics.get_point_by_index(index=p1_i)
                exit_p = self.user2.exit_metrics.get_point_by_index(index=p2_i)

            return PointMatch(p1=p1, p2=p2, dt=dt,
                              entry_w=entry_p.w, exit_w=exit_p.w,
                              entry_v=entry_p.v, exit_v=exit_p.v,
                              entry_a=entry_p.a, exit_a=exit_p.a,
                              both_tor_users=self.both_tor_users)

    def _exit_to_entry_matches(self) -> List[PointMatch]:
        matches = []
        for p1 in self.user1.exit_itxye.as_points():
            for p2 in self.user2.entry_itxye.as_points():
                point_match = self._single_point_match(p1=p1, p2=p2, type_p1=EXIT_TYPE)
                if point_match:
                    matches.append(point_match)
        return matches

    def _entry_to_exit_matches(self) -> List[PointMatch]:
        matches = []
        for p1 in self.user1.entry_itxye.as_points():
            for p2 in self.user2.exit_itxye.as_points():
                point_match = self._single_point_match(p1=p1, p2=p2, type_p1=ENTRY_TYPE)
                if point_match:
                    matches.append(point_match)
        return matches

    def user_match(self) -> UsersPair:
        return UsersPair(user1=self.user1, user2=self.user2,
                         exit_to_entry_matches=self._exit_to_entry_matches(),
                         entry_to_exit_matches=self._entry_to_exit_matches())


class UserPairHandler:
    MIN_VALID_POINTS = 3
    MIN_VALID_POINTS_PERCENTAGE = 0.2

    @staticmethod
    def _all_user_pairs() -> UserPairsSet:
        matches = UserPairsSet()
        for comb in Combinations.tor_users_combs(users_iter=all_users):
            tor_u1, u2 = comb
            match_creator = UserMatchCreator(user1=tor_u1, user2=u2)
            matches.add(match_creator.user_match())
        return matches

    def _matches_due_to_luck(self, percent_valid) -> bool:
        return percent_valid < self.MIN_VALID_POINTS_PERCENTAGE

    def _not_enough_valid(self, total_valid_points) -> bool:
        return total_valid_points < self.MIN_VALID_POINTS

    @staticmethod
    def _zero_matches(matched_points) -> bool:
        return not matched_points

    def _is_valid_pair(self, user_pair: UsersPair) -> bool:
        matched_points = user_pair.entry_to_exit_matches + user_pair.exit_to_entry_matches
        if self._zero_matches(matched_points):
            return False

        valid_points = []
        for p in matched_points:
            if p.valid_match:
                valid_points.append(p)

        total_valid_points = len(valid_points)
        total_points = len(valid_points)
        percent_valid = total_valid_points / total_points

        if self._matches_due_to_luck(percent_valid):
            return False
        if self._not_enough_valid(total_valid_points):
            return False

        return True

    def _valid_user_pairs(self) -> UserPairsSet:
        valid_pairs = UserPairsSet()

        user_pair: UsersPair
        for user_pair in self._all_user_pairs():
            if not self._is_valid_pair(user_pair=user_pair):
                continue
            valid_pairs.add(user_pair)
        return valid_pairs

    def insert_valid_user_pairs(self) -> None:
        for pair in self._valid_user_pairs():
            all_matches.add(pair)
