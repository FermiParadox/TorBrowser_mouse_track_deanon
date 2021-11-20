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
    IDs_Used = set()

    @staticmethod
    def unique_id():
        while 1:
            generated_id = secrets.randbelow(IDGenerator.MAX_ID_NUM)
            if generated_id not in IDGenerator.IDs_Used:
                return generated_id


@dataclass
class User:
    id: int
    ip: IPv6_or_IPv4_obj    # TODO turn into dict with ip:time
    mouse_txy: TimeXY
    time_keys: TimeKeys

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class AllUsers(set):
    @property
    def ips(self):
        return {str(u.ip) for u in self}

    @property
    def ids(self):
        return {str(u.id) for u in self}

    def add(self, other):
        """When added element is already present, it replaces the existing one.
        Not very efficient, but should be ok for testing.

        By default `add` has no effect if the element is already present,
        meaning new data points wouldn't be stored."""
        self.discard(other)
        super().add(other)


all_users = AllUsers()


class UserHandler:
    def __init__(self, user_id: int, ip_str: str, mouse_txy_str: str):
        self.user_id = user_id
        self.mouse_txy_str = mouse_txy_str
        self.ip_str = ip_str
        self.user = None
        self.ip = None
        self.create_or_update_user()

    def _create_ip_obj(self):
        self.ip = ip_address(self.ip_str)

    def _create_user(self):
        t, x, y = TXYConverter(data_string=self.mouse_txy_str).txy_lists()
        mouse_txy = TimeXY(time=t, x=x, y=y)

        self.user = User(id=self.user_id,
                         ip=self.ip,
                         mouse_txy=mouse_txy,
                         time_keys=TimeKeys())

    def create_or_update_user(self):
        self._create_ip_obj()
        self._create_user()
