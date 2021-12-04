from dataclasses import dataclass, field

from analysis.analysis import ExitMetrics, EntryMetrics
from analysis.conversion import DataExtractor
from analysis.metrics_base import ITXY
from analysis.plotting import Plotter
from analysis.user_base import User


def is_tor_user(user: User):
    """Tor-user times always end in '00'
    because of the 100ms time-resolution imposed in JS."""
    all_modulo = (i % 100 for i in user.all_itxy.time)
    if any(all_modulo):
        return False
    return True


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
class Similarity:
    user1: User
    user2: User
    times_diff: int
    angles_diff: float = field(init=False)

    exit_itxy: ITXY
    exit_angle: float

    entry_itxy: ITXY
    entry_angle: float

    def __post_init__(self):
        self.angles_diff = abs(self.entry_angle - self.exit_angle)


all_similarities = []


def add_similarities(user):
    for u in all_users:
        ...


def tor_users():
    return (user for user in all_users if is_tor_user(user=user))


for u in tor_users():
    add_similarities(u)
