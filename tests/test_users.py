from ipaddress import ip_address
from unittest import TestCase

from analysis.user_base import IDGenerator, User
from analysis.itxye_base import ITXYE


class TestUser(TestCase):
    def setUp(self) -> None:
        user_id = 1525
        self.u1_0000 = User(id=user_id,
                            ip=ip_address("0.0.0.0"),
                            all_itxye=ITXYE([1, 2], [11, 22], [111, 222]))

        self.u2_5000 = User(id=user_id,
                            ip=ip_address("5.0.0.0"),
                            all_itxye=ITXYE([1, 2, 3], [11, 22, 33], [111, 222, 333]))

    def test_same_id_considered_same_user(self):
        self.assertEqual(self.u1_0000, self.u2_5000)

    def test_same_id_stored_once_in_sets(self):
        set_size = len({self.u1_0000, self.u1_0000, self.u2_5000})
        self.assertEqual(set_size, 1)


class TestIDGenerator(TestCase):
    def test_unique_id(self):
        generator = IDGenerator
        generator.IDs_Used = {0, 1, 2}
        generator.MAX_ID_NUM = 4  # Only value available will be 3

        self.assertEqual(generator.unique_id(), 3)


