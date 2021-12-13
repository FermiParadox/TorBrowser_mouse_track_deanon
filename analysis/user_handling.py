from dataclasses import dataclass, field
from itertools import combinations
from typing import List, Iterator, Tuple, Collection

from scipy.spatial import distance

import analysis.p_types as p_types
from analysis.metrics import ExitMetricsCalc, EntryMetricsCalc
from analysis.physics import center_point
from analysis.str_parser import DataExtractor
from analysis.iwvaek_base import IWVAEK
from analysis.itxyek_base import ITXYEKPoint, XYFloatPoint
from analysis.plotting import Plotter

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
                    all_itxyek=extractor.itxyek_lists(),
                    exit_metrics=IWVAEK(),
                    entry_metrics=IWVAEK())


class UserHandler:
    def __init__(self, user: User):
        self.user = user

    def insert_user(self) -> None:
        all_users.add(self.user)

    def _exit_angles(self) -> Iterator[float]:
        metrics = ExitMetricsCalc(all_itxyek=self.user.all_itxyek,
                                  crit_indices=self.user.exit_indices)
        return metrics.critical_angles()

    def _entry_angles(self) -> Iterator[float]:
        metrics = EntryMetricsCalc(all_itxyek=self.user.all_itxyek,
                                   crit_indices=self.user.entry_indices)
        return metrics.critical_angles()

    def _exit_speeds(self) -> Iterator[float]:
        metrics = ExitMetricsCalc(all_itxyek=self.user.all_itxyek,
                                  crit_indices=self.user.exit_indices)
        return metrics.critical_speeds()

    def _entry_speeds(self) -> Iterator[float]:
        metrics = EntryMetricsCalc(all_itxyek=self.user.all_itxyek,
                                   crit_indices=self.user.entry_indices)
        return metrics.critical_speeds()

    def _exit_accelerations(self) -> Iterator[float]:
        metrics = ExitMetricsCalc(all_itxyek=self.user.all_itxyek,
                                  crit_indices=self.user.exit_indices)
        return metrics.critical_accelerations()

    def _entry_accelerations(self) -> Iterator[float]:
        metrics = EntryMetricsCalc(all_itxyek=self.user.all_itxyek,
                                   crit_indices=self.user.entry_indices)
        return metrics.critical_accelerations()

    def calc_and_store_metrics(self) -> None:
        exit_metrics: IWVAEK
        exit_metrics = self.user.exit_metrics
        exit_metrics.indices = [p.index for p in self.user.all_itxyek.as_points() if p.e == p_types.EXIT]
        exit_metrics.v = self._exit_speeds()
        exit_metrics.w = self._exit_angles()
        exit_metrics.a = self._exit_accelerations()
        exit_metrics.e = [p_types.EXIT for _ in exit_metrics.indices]
        exit_metrics.k = [self.user.all_itxyek.point_by_index(index=i).k for i in exit_metrics.indices]

        entry_metrics: IWVAEK
        entry_metrics = self.user.entry_metrics
        entry_metrics.indices = [p.index for p in self.user.all_itxyek.as_points() if p.e == p_types.ENTRY]
        entry_metrics.v = self._entry_speeds()
        entry_metrics.w = self._entry_angles()
        entry_metrics.a = self._entry_accelerations()
        entry_metrics.e = [p_types.ENTRY for _ in entry_metrics.indices]
        entry_metrics.k = [self.user.all_itxyek.point_by_index(index=i).k for i in entry_metrics.indices]

        exit_metrics.clean_undefined_metrics()
        entry_metrics.clean_undefined_metrics()

    def plot_and_show_mouse_movement(self) -> None:
        x_all = self.user.all_itxyek.x
        y_all = self.user.all_itxyek.y

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
    all_modulo = (i % 100 for i in user.all_itxyek.time)
    if any(all_modulo):
        return False
    return True


def are_tor_users(users: Collection[User]) -> bool:
    return all(is_tor_user(u) for u in users)


class Combinations:
    USER_COMBS_TYPE = Iterator[Tuple[User, User]]

    @staticmethod
    def all_user_combs(users_iter: Collection[User]) -> USER_COMBS_TYPE:
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
        # TODO re-activate tor
        if 1:
            all_combs = Combinations.all_user_combs(users_iter=users_iter)
            return all_combs
        return Combinations._tor_user_combs(all_combs=all_combs)


class PointMatchLimits:
    MAX_DW = 30
    # Velocity and acceleration differences
    #   are probably not very relevant.
    MAX_DV = 50
    MAX_DA = 50
    # Assuming the user usually stops moving during CTR TAB
    #   this can be set to 1 (it would reduce false positives).
    MAX_DS_2TOR = 10


@dataclass
class PointMatch:
    """
    Stores data related an exit and entry point of two user_IDs,
    when they appear to be coming from the same user.
    """
    p1: ITXYEKPoint
    p2: ITXYEKPoint
    type_p1: p_types.EntryOrExit
    trigger: p_types.KEY_OR_MOUSE
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
    ds: float = field(init=False, default=None)  # distance p1-p2 relative to the centers

    valid_match: bool = field(init=False, default=False)

    def __post_init__(self):
        self._store_dw(self.entry_w, self.exit_w)
        self._store_dv(self.entry_v, self.exit_v)
        self._store_da(self.entry_a, self.exit_a)
        self.valid_match = self._valid_match()

    def _store_dw(self, entry_w, exit_w) -> None:
        self.dw = exit_w - entry_w

    def _store_dv(self, entry_v, exit_v) -> None:
        self.dv = exit_v - entry_v

    def _store_da(self, entry_a, exit_a) -> None:
        self.da = exit_a - entry_a

    def _dw_in_range(self) -> bool:
        return abs(self.dw) <= PointMatchLimits.MAX_DW

    def _dv_in_range(self) -> bool:
        return abs(self.dv) <= PointMatchLimits.MAX_DV

    def _da_in_range(self) -> bool:
        return abs(self.da) <= PointMatchLimits.MAX_DA

    def _valid_match_tor_plus_normal(self) -> bool:
        if self._dw_in_range() and self._dv_in_range() and self._da_in_range():
            return True
        if self.trigger == p_types.KEY:
            return True
        return False

    def _ds_tor_to_tor_in_range(self) -> bool:
        """
        When both userIDs belong to the same Tor Browser
        the x,y-axis of both tabs are nearly identical.

        There might be a small difference if the mouse was moving
        during the key press.
        """
        xy1 = [self.p1.x, self.p1.y]
        xy2 = [self.p2.x, self.p2.y]
        return distance.euclidean(xy1, xy2) <= PointMatchLimits.MAX_DS_2TOR

    def _valid_match_both_tor(self) -> bool:
        if self._ds_tor_to_tor_in_range():
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

    center1: XYFloatPoint = field(init=False, default=None)
    center2: XYFloatPoint = field(init=False, default=None)
    deviation: float = field(init=False, default=None)
    match_id: str = field(init=False, default=None)

    @staticmethod
    def is_invalid_point_match(p_match: PointMatch) -> bool:
        return not p_match.valid_match

    @staticmethod
    def _center(point_matches: List[PointMatch], user_1or2: int) -> XYFloatPoint:
        x_array = []
        y_array = []
        p_match: PointMatch
        for p_match in point_matches:
            if UsersPair.is_invalid_point_match(p_match=p_match):
                continue

            if user_1or2 == 1:
                p = p_match.p1
            elif user_1or2 == 2:
                p = p_match.p2
            else:
                raise ValueError(f"User num must be 1 or 2. Not {user_1or2}.")

            x_array.append(p.x)
            y_array.append(p.y)
        return center_point(x_array=x_array, y_array=y_array)

    def _center1(self, point_matches) -> XYFloatPoint:
        return self._center(point_matches=point_matches, user_1or2=1)

    def _center2(self, point_matches) -> XYFloatPoint:
        return self._center(point_matches=point_matches, user_1or2=2)

    def set_centers(self) -> None:
        self.center1 = self._center1(point_matches=self.all_point_matches)
        self.center2 = self._center2(point_matches=self.all_point_matches)

    @staticmethod
    def _ds_relative_to_center(p_pair: PointMatch, center1: XYFloatPoint, center2: XYFloatPoint) -> float:
        xy1_rel = [p_pair.p1.x - center1.x, p_pair.p1.y - center1.y]
        xy2_rel = [p_pair.p2.x - center2.x, p_pair.p2.y - center2.y]
        return distance.euclidean(xy1_rel, xy2_rel)

    @staticmethod
    def _set_point_pair_deviation(ds: float, p_pair: PointMatch):
        p_pair.ds = ds

    def all_valid_point_matches(self) -> List[PointMatch]:
        return [p_match for p_match in self.all_point_matches if p_match.valid_match]

    def _total_deviation(self):
        """
        This is a metric of the deviation of all point-pairs from one another.
        In an (unrealistic) perfect match the ds of p1 and p2 would be 0.
        """
        tot_dev = 0
        p_pair: PointMatch
        for p_pair in self.all_valid_point_matches():
            ds = self._ds_relative_to_center(p_pair=p_pair, center1=self.center1, center2=self.center2)
            self._set_point_pair_deviation(ds=ds, p_pair=p_pair)
            tot_dev += ds
        tot_dev /= len(self.all_valid_point_matches())
        return tot_dev

    def set_point_pair_ds(self):
        p_pair: PointMatch
        for p_pair in self.all_point_matches:
            ds = self._ds_relative_to_center(p_pair=p_pair, center1=self.center1, center2=self.center2)
            p_pair.ds = ds

    def set_deviation(self):
        self.deviation = self._total_deviation()

    def __post_init__(self):
        self.match_id = f"{self.user1.id},{self.user2.id}"
        self.all_point_matches = self.exit_to_entry_matches + self.entry_to_exit_matches

    def invalidate_point_pairs_by_deviation(self):
        p_pair: PointMatch
        for p_pair in self.all_point_matches:
            if self.is_invalid_point_match(p_pair):
                continue
            if p_pair.ds > 70:
                p_pair.valid_match = False

    def __eq__(self, other):
        return self.match_id == other.match_id

    def __hash__(self):
        return hash(self.match_id)


class UserPairsSet(ReAddingSet):
    def add(self, other: UsersPair) -> None:
        super().add(other)

    def print_user_pairs(self) -> None:
        print("=" * 60)
        print("All pairs matched:")
        m: UsersPair
        for m in self:
            print("=" * 30)
            print(f"User1: {m.user1.id}")
            print(f"User2: {m.user2.id}")
            print(f"Center: {m.center1}")
            print(f"Center: {m.center2}")
            print(f"Deviation: {m.deviation}")
            print("Exit points matched:")
            for p in m.exit_to_entry_matches:
                print("-" * 15)
                print(f"dt = {p.dt}")
                print(f"dw = {p.dw}")
                print(f"dv = {p.dv}")
                print(f"da = {p.da}")
                print(f"ds = {p.ds}")
                print(f"valid = {p.valid_match}")
            print("=" * 30)
            print("Entry points matched:")
            for p in m.entry_to_exit_matches:
                print("-" * 15)
                print(f"dt = {p.dt}")
                print(f"dw = {p.dw}")
                print(f"dv = {p.dv}")
                print(f"da = {p.da}")
                print(f"ds = {p.ds}")
                print(f"valid = {p.valid_match}")


all_matches = UserPairsSet()


class UserMatchCreator:
    # In milliseconds
    TOR_RESOLUTION = 100
    POSSIBLE_BROWSER_ERROR_ON_SAME_MACHINE = 5
    DEAD_ZONE_TIME = 20  # mouse between the two browsers
    MAX_DELTA_T = TOR_RESOLUTION + POSSIBLE_BROWSER_ERROR_ON_SAME_MACHINE + DEAD_ZONE_TIME
    MIN_DELTA_T = - POSSIBLE_BROWSER_ERROR_ON_SAME_MACHINE

    ALT_TAB_MOVE_DELAY = 2000

    def __init__(self, user1: User, user2: User):
        self.user1 = user1
        self.user2 = user2
        self.both_tor_users = are_tor_users([user1, user2])
        self.exit_to_entry_matches = self._exit_to_entry_matches()
        self.entry_to_exit_matches = self._entry_to_exit_matches()
        self.exit_and_entry_matches = self.exit_to_entry_matches + self.entry_to_exit_matches

    @staticmethod
    def dt(p1: ITXYEKPoint, p2: ITXYEKPoint, type_p1: p_types.EntryOrExit) -> int:
        if type_p1 == p_types.EXIT:
            p_out = p1
            p_in = p2
        else:
            p_out = p2
            p_in = p1
        return p_in.time - p_out.time

    @staticmethod
    def dt_of_mouse_in_bounds(dt: int) -> bool:
        return UserMatchCreator.MIN_DELTA_T <= dt <= UserMatchCreator.MAX_DELTA_T

    @staticmethod
    def is_key_triggered(p1: ITXYEKPoint) -> bool:
        return p1.k == p_types.KEY

    @staticmethod
    def is_mouse_triggered(p1: ITXYEKPoint) -> bool:
        return p1.k == p_types.MOUSE

    def dt_in_bounds(self, dt: int, p1: ITXYEKPoint) -> bool:
        if self.is_mouse_triggered(p1=p1):
            return self.dt_of_mouse_in_bounds(dt=dt)
        elif self.is_key_triggered(p1=p1):
            return -100 < dt < self.ALT_TAB_MOVE_DELAY

    def _single_point_match(self, p1: ITXYEKPoint, p2: ITXYEKPoint, type_p1: p_types.EntryOrExit) -> PointMatch:
        dt = self.dt(p1=p1, p2=p2, type_p1=type_p1)
        if self.dt_in_bounds(dt=dt, p1=p1):
            p1_i = p1.index
            p2_i = p2.index
            if type_p1 == p_types.EXIT:
                exit_p = self.user1.exit_metrics.get_point_by_index(index=p1_i)
                entry_p = self.user2.entry_metrics.get_point_by_index(index=p2_i)
            else:
                entry_p = self.user1.entry_metrics.get_point_by_index(index=p1_i)
                exit_p = self.user2.exit_metrics.get_point_by_index(index=p2_i)

            return PointMatch(p1=p1, p2=p2, dt=dt,
                              type_p1=type_p1, trigger=p1.k,
                              entry_w=entry_p.w, exit_w=exit_p.w,
                              entry_v=entry_p.v, exit_v=exit_p.v,
                              entry_a=entry_p.a, exit_a=exit_p.a,
                              both_tor_users=self.both_tor_users, )

    def _exit_to_entry_matches(self) -> List[PointMatch]:
        matches = []
        for p1 in self.user1.exit_itxyek.as_points():
            for p2 in self.user2.entry_itxyek.as_points():
                point_match = self._single_point_match(p1=p1, p2=p2, type_p1=p_types.EXIT)
                if point_match:
                    matches.append(point_match)
        return matches

    def _entry_to_exit_matches(self) -> List[PointMatch]:
        matches = []
        for p1 in self.user1.entry_itxyek.as_points():
            for p2 in self.user2.exit_itxyek.as_points():
                point_match = self._single_point_match(p1=p1, p2=p2, type_p1=p_types.ENTRY)
                if point_match:
                    matches.append(point_match)
        return matches

    def user_match(self) -> UsersPair:
        return UsersPair(user1=self.user1, user2=self.user2,
                         exit_to_entry_matches=self.exit_to_entry_matches,
                         entry_to_exit_matches=self.entry_to_exit_matches)


class UserPairHandler:
    MIN_VALID_POINTS = 3
    MIN_VALID_POINTS_PERCENTAGE = 0.05

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

    def _is_valid_user_pair(self, user_pair: UsersPair) -> bool:
        matched_points = user_pair.entry_to_exit_matches + user_pair.exit_to_entry_matches
        if self._zero_matches(matched_points):
            return False

        valid_points = []
        for p in matched_points:
            if p.valid_match:
                valid_points.append(p)

        total_valid_points = len(valid_points)
        total_points = len(valid_points)
        if not total_points:
            return False

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
            if not self._is_valid_user_pair(user_pair=user_pair):
                continue

            for _ in range(10):
                user_pair.set_centers()
                user_pair.set_deviation()
                user_pair.invalidate_point_pairs_by_deviation()

            valid_pairs.add(user_pair)

        return valid_pairs

    def insert_valid_user_pairs(self) -> None:
        pair: UsersPair
        for pair in self._valid_user_pairs():
            all_matches.add(pair)
