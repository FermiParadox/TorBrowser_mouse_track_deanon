import secrets
from ipaddress import IPv4Address, IPv6Address, ip_address
from dataclasses import dataclass, field
from typing import Union, List


from data_converter import TXYStrToArray, ActionDataExtractor
from utils import plot_x_y

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
    ip: IPv6_or_IPv4_obj  # TODO turn into dict with ip:time
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
    def __init__(self, req):
        self.req = req
        self.user_id = None
        self.mouse_txy_str = None
        self.user = None
        self.ip = None

    def _create_action_arrays(self):
        extractor = ActionDataExtractor(req=self.req)
        self.ip = ip_address(extractor.user_ip_str)
        self.mouse_txy_str = extractor.mouse_txy_str
        self.user_id = int(extractor.user_id_str)

    @property
    def _txy_lists(self):
        t, x, y = TXYStrToArray(data_string=self.mouse_txy_str).txy_lists()
        return t, x, y

    def _create_user(self):
        t, x, y = self._txy_lists
        mouse_txy = TimeXY(time=t, x=x, y=y)

        self.user = User(id=self.user_id,
                         ip=self.ip,
                         mouse_txy=mouse_txy,
                         time_keys=TimeKeys())

    def create_user(self):
        self._create_action_arrays()
        self._create_user()

    def create_and_insert_user(self):
        all_users.add(self.user)

    def plot_mouse_movement(self):
        plot_x_y(x=self.user.mouse_txy.x, y=self.user.mouse_txy.y)
