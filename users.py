import secrets
from ipaddress import IPv4Address, IPv6Address, ip_address
from dataclasses import dataclass, field
from typing import Union, List

from data_converter import TXYConverter

# WARNING
# Dataclasses are problematic (refactoring names fails),
# TODO: consider using pydantic, or use normal init


IPv6_or_IPv4_obj = Union[IPv4Address, IPv6Address]


@dataclass
class TimeXY(list):
    time: List[int] = field(default_factory=list)
    x: List[int] = field(default_factory=list)
    y: List[int] = field(default_factory=list)


@dataclass
class TimeKeys(list):
    time: List[int] = field(default_factory=list)
    keys_pressed: List[int] = field(default_factory=list)


class IDGenerator:
    MAX_ID_NUM = 10 ** 50
    IDs_Used = {}

    @staticmethod
    def unique_id():
        while 1:
            generated_id = secrets.randbelow(IDGenerator.MAX_ID_NUM)
            if generated_id not in IDGenerator.IDs_Used:
                return generated_id


@dataclass
class User:
    id: str = field(init=False)
    ip: IPv6_or_IPv4_obj
    mouse_txy: TimeXY
    time_keys: TimeKeys

    def __post_init__(self):
        self.id = IDGenerator.unique_id()

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class AllUsers(set):
    @property
    def ips(self):
        return [str(u.ip) for u in self]

    def add(self, other):
        """When added element is already present, it replaces the existing one.
        Not very efficient, but should be ok.

        By default `add` has no effect if the element is already present,
        meaning new data points wouldn't be stored."""
        self.discard(other)
        super().add(other)


all_users = AllUsers()


# TODO un-dataclass it
@dataclass
class UserHandler:
    ip_str: str
    mouse_txy_str: str

    user: User = field(default_factory=list, init=False)
    ip: IPv6_or_IPv4_obj = field(init=False)

    def __post_init__(self):
        self.create_ip()
        self.create_user()
        self.add_user()

    def create_ip(self):
        self.ip = ip_address(self.ip_str)

    def create_user(self):
        t, x, y = TXYConverter(data_string=self.mouse_txy_str).txy_lists()
        mouse_txy = TimeXY(time=t, x=x, y=y)

        self.user = User(ip=self.ip,
                         mouse_txy=mouse_txy,
                         time_keys=TimeKeys())

    def add_user(self):
        # Simply replace a user with its updated self
        all_users.add(self.user)


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
                           time_keys=TimeKeys([4], [4])))

    print(all_users)
    for i in all_users:
        print(i)
