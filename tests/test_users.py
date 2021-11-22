from ipaddress import ip_address
from unittest import TestCase

from users import User, TimeXY, TimeKeys, AllUsers, IDGenerator, UserHandler


class TestUser(TestCase):
    def setUp(self) -> None:
        user_id = 1525
        self.u1_0000 = User(id=user_id,
                            ip=ip_address("0.0.0.0"),
                            mouse_txy=TimeXY([1, 2], [11, 22], [111, 222]),
                            time_keys=TimeKeys([4, 5], [44, 55]))

        self.u2_5000 = User(id=user_id,
                            ip=ip_address("5.0.0.0"),
                            mouse_txy=TimeXY([1, 2, 3], [11, 22, 33], [111, 222, 333]),
                            time_keys=TimeKeys([4, 5], [44, 55]))

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


class TestAllUsers(TestCase):
    def setUp(self) -> None:
        self.u1 = User(id=111,
                       ip=ip_address("0.42.0.0"),
                       mouse_txy=TimeXY(),
                       time_keys=TimeKeys([4, 5], [44, 55]))

        self.u2 = User(id=3333,
                       ip=ip_address("0.0.7.0"),
                       mouse_txy=TimeXY(),
                       time_keys=TimeKeys([4, 5], [44, 55]))

        self.u3_initial = User(id=5252525,
                               ip=ip_address("52.0.0.0"),
                               mouse_txy=TimeXY(),
                               time_keys=TimeKeys())

        self.txy_updated = TimeXY([1, 2], [11, 22], [111, 222])
        self.u3_updated = User(id=5252525,
                               ip=ip_address("52.0.0.0"),
                               mouse_txy=self.txy_updated,
                               time_keys=TimeKeys([4, 5], [44, 55]))

    def test_displayed_id_exists_when_adding_user(self):
        stored_user = self.u1

        users_list = AllUsers()
        users_list.add(stored_user)

        self.assertEqual(users_list.ids.pop(), str(stored_user.id))

    def test_displayed_ip_exists_when_adding_user(self):
        stored_user = self.u1

        users_list = AllUsers()
        users_list.add(stored_user)

        self.assertEqual(users_list.ips.pop(), str(stored_user.ip))

    def test_all_ids_added_when_unique(self):
        users_list = AllUsers()

        users_list.add(self.u1)
        users_list.add(self.u2)
        users_list.add(self.u3_initial)

        self.assertEqual(len(users_list), 3)

    def test_no_duplicate_ids(self):
        users_list = AllUsers()

        users_list.add(self.u3_initial)
        users_list.add(self.u3_updated)

        self.assertEqual(len(users_list), 1)

    def test_previous_user_data_replaced(self):
        users_list = AllUsers()

        users_list.add(self.u3_initial)
        users_list.add(self.u3_updated)

        user = users_list.pop()
        self.assertEqual(user.mouse_txy, self.txy_updated)


class TestUserHandler(TestCase):
    ...