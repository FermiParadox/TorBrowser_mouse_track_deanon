from ipaddress import ip_address, IPv4Address, IPv6Address
from dataclasses import dataclass
from typing import Union, List


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
    txy: TimeXY
    t_keys: TimeKeys


