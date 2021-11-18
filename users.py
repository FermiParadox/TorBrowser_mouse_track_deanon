from ipaddress import IPv4Address, IPv6Address, ip_address
from dataclasses import dataclass
from typing import Union, List


# WARNING
# Dataclasses are problematic (refactoring names fails),
# TODO: consider using pydantic, or use normal init

@dataclass
class TimeXY(list):
    time: List[int]
    x: List[int]
    y: List[int]


@dataclass
class TimeKeys(list):
    time: List[int]
    keys_pressed: List[int]


@dataclass
class User:
    ip: Union[IPv4Address, IPv6Address]
    mouse_txy: TimeXY
    time_keys: TimeKeys

    def __eq__(self, other):
        return self.ip == other.ip

    def __hash__(self):
        return hash(self.ip)


class AllUsers(set):
    @property
    def ips(self):
        return [str(u.ip) for u in self]

    def __repr__(self):
        ips_as_str = ', '.join(self.ips)
        return f"{self.__class__.__name__}({ips_as_str})"

    def add(self, other):
        self.discard(other)
        super().add(other)


all_users = AllUsers()


def update_user(user: User):
    # Simply replace a user with its updated self
    all_users.add(user)


if __name__ == "__main__":
    ip1 = ip_address("0.0.0.0")
    mouse_txy = TimeXY([], [], [])
    time_keys = TimeKeys([], [])
    u1 = User(ip=ip1,
              mouse_txy=mouse_txy,
              time_keys=time_keys)

    u2 = User(ip=ip_address("0.0.0.1"),
              mouse_txy=mouse_txy,
              time_keys=time_keys)

    print(u1 == u1)
    print(u1 == u2)

    all_users.add(u1)
    all_users.add(u1)
    all_users.add(u2)
    for _ in range(10 ** 0):
        all_users.add(User(ip=ip_address("0.0.0.1"),
                           mouse_txy=mouse_txy,
                           t_keys=TimeKeys([4], [4])))

    print(all_users)
    for i in all_users:
        print(i)
