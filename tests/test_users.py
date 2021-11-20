from ipaddress import ip_address
from unittest import TestCase

from users import User, TimeXY, TimeKeys, AllUsers


class TestUser(TestCase):
    def setUp(self) -> None:
        self.u1_0000 = User(ip=ip_address("0.0.0.0"),
                            mouse_txy=TimeXY([1, 2], [11, 22], [111, 222]),
                            time_keys=TimeKeys([4, 5], [44, 55]))

        self.u2_0000 = User(ip=ip_address("0.0.0.0"),
                            mouse_txy=TimeXY([1, 2, 3], [11, 22, 33], [111, 222, 333]),
                            time_keys=TimeKeys([4, 5], [44, 55]))

    def test_same_ip_considered_same_user(self):
        self.assertEqual(self.u1_0000, self.u2_0000)

    def test_same_ip_stored_once_in_sets(self):
        set_size = len({self.u1_0000, self.u1_0000, self.u2_0000})
        self.assertEqual(set_size, 1)


class TestAllUsers(TestCase):

    def test_ips(self):
        self.fail()

    def test_add_removes_previous_duplicate_user(self):
        self.fail()
