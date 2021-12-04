from dataclasses import dataclass, field

from analysis.analysis import ExitMetrics, EntryMetrics
from analysis.conversion import DataExtractor
from analysis.metrics_dataclasses import ITXY
from analysis.plotting import Plotter
from users.user_base import User


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
                    all_txy=extractor.txy_lists,
                    entry_txy_lists=extractor.entry_txy,
                    exit_txy_lists=extractor.exit_txy,
                    exit_indices=extractor.exit_indices(),
                    entry_indices=extractor.entry_indices())


class UserHandler:
    def __init__(self, user):
        self.user: User = user

    def _exit_angles(self):
        metrics = ExitMetrics(all_txy=self.user.all_txy,
                              crit_indices=self.user.exit_indices)
        return metrics.critical_angles()

    def _entry_angles(self):
        metrics = EntryMetrics(all_txy=self.user.all_txy,
                               crit_indices=self.user.entry_indices)
        return metrics.critical_angles()

    def _exit_speeds(self):
        metrics = ExitMetrics(all_txy=self.user.all_txy,
                              crit_indices=self.user.exit_indices)
        return metrics.critical_speeds()

    def _entry_speeds(self):
        metrics = EntryMetrics(all_txy=self.user.all_txy,
                               crit_indices=self.user.entry_indices)
        return metrics.critical_speeds()

    def _exit_accelerations(self):
        metrics = ExitMetrics(all_txy=self.user.all_txy,
                              crit_indices=self.user.exit_indices)
        return metrics.critical_accelerations()

    def _entry_accelerations(self):
        metrics = EntryMetrics(all_txy=self.user.all_txy,
                               crit_indices=self.user.entry_indices)
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
        x_all = self.user.all_txy.x
        y_all = self.user.all_txy.y

        plotter = Plotter(user_id=self.user.id)
        plotter.plot_all_x_y(x=x_all, y=y_all)

        exit_x_list = self.user.exit_txy_lists.x
        exit_y_list = self.user.exit_txy_lists.y
        plotter.plot_exit_xy(x=exit_x_list, y=exit_y_list)

        entry_x_list = self.user.entry_txy_lists.x
        entry_y_list = self.user.entry_txy_lists.y
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


def is_tor_user(user: User):
    """Tor-user times always end in '00'
    because of the 100ms time-resolution imposed in JS."""
    all_modulo = (i % 100 for i in user.all_txy.time)
    if any(all_modulo):
        return False
    return True
