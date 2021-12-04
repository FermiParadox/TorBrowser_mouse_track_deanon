from ipaddress import ip_address
from unittest import TestCase

from analysis.metrics_dataclasses import TimesXY


class Test_is_tor_user(TestCase):
    def setUp(self) -> None:
        from users.user_base import User
        self.user = User(id=93847629346,
                         ip=ip_address("0.0.0.0"),
                         all_txy=TimesXY([1, 2, 3], [11, 22, 33], [111, 222, 333]),
                         exit_txy_lists=TimesXY(),
                         entry_txy_lists=TimesXY(),
                         exit_indices=[],
                         entry_indices=[])

    def test_false(self):
        from analysis.user_handling import is_tor_user

        # non-tor data
        times = [1638636689730, 1638636689747, 1638636689764, 1638636689781, 1638636689797, 1638636689814,
                 1638636689830, 1638636689846, 1638636689863, 1638636689880, 1638636689897, 1638636689913,
                 1638636689930, 1638636689946, 1638636689964, 1638636689979, 1638636689997, 1638636690013,
                 1638636690029, 1638636690046, 1638636690063, 1638636690080, 1638636690097, 1638636690113,
                 1638636690130, 1638636690163, 1638636690180, 1638636690196, 1638636690213, 1638636690230,
                 1638636690310, 1638636690330, 1638636690346, 1638636690363, 1638636690380, 1638636690398]
        self.user.all_txy.time = times
        self.assertFalse(is_tor_user(user=self.user))

    def test_true(self):
        from analysis.user_handling import is_tor_user

        # tor data
        times = [1638636528300, 1638636528300, 1638636528300, 1638636528400, 1638636528400, 1638636528400,
                 1638636528400, 1638636528400, 1638636528400, 1638636528500, 1638636528500, 1638636528500,
                 1638636528500, 1638636528500, 1638636528500, 1638636528600, 1638636528600, 1638636528600,
                 1638636528600, 1638636528600, 1638636528600, 1638636528600, 1638636528700, 1638636528700,
                 1638636528700, 1638636528700]
        self.user.all_txy.time = times
        self.assertTrue(is_tor_user(user=self.user))
