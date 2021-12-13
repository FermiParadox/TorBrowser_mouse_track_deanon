from ipaddress import ip_address
from typing import List
from scipy.spatial import distance

import analysis.p_types as p_types
from analysis.ip_base import IPv6_or_IPv4_obj
from analysis.itxyek_base import ITXYEK

POINT_SPLITTER = ":"
COORDINATE_SPLITTER = ","


class ITXYStrToArray:
    """The client provides a string like
    "1520095100,25,690:1520095100, 30, 650:"
    """

    def __init__(self, data_string: str):
        self.txy_string = data_string

    def points_as_list_of_strings(self) -> list:
        return [s for s in self.txy_string.split(POINT_SPLITTER) if s]

    @property
    def itxyek_lists(self) -> ITXYEK:
        itxyek_lists = ITXYEK()
        for i, p in enumerate(self.points_as_list_of_strings()):
            t, x, y = p.split(',')
            itxyek_lists.indices.append(i)
            itxyek_lists.time.append(int(t))
            itxyek_lists.x.append(int(x))
            itxyek_lists.y.append(-int(y))  # y-axis goes downwards in browsers unlike cartesian
            itxyek_lists.e.append(p_types.EntryOrExit())
            itxyek_lists.k.append(p_types.KeyOrMouse())

        return itxyek_lists


class DataExtractor:
    def __init__(self, req):
        self.req = req
        self.json = req.json
        self._itxyek_lists = ITXYStrToArray(data_string=self._mouse_txy_str()).itxyek_lists
        self.maximum_itxyek_index = self._itxyek_lists.indices[-1]

    def _mouse_txy_str(self) -> str:
        return self.json["mouse_txy"]

    def user_id(self) -> int:
        return int(self.json["userID"])

    def user_ip(self) -> IPv6_or_IPv4_obj:
        return ip_address(self.req.remote_addr)

    def _exit_indices_str(self) -> str:
        return self.json["mouse_exit_txy_indices"]

    def _mouse_exit_indices(self) -> List[int]:
        return [int(s) for s in self._exit_indices_str().split(POINT_SPLITTER) if s]

    def _key_exit_indices(self) -> List[int]:
        return AltTabPoints().exit_indices(itxyek=self._itxyek_lists)

    def exit_indices(self) -> List[int]:
        indices_list = self._mouse_exit_indices() + self._key_exit_indices()
        indices_list.sort()
        return indices_list

    def entry_point_index_out_of_range(self, index) -> bool:
        return index > self.maximum_itxyek_index

    def _entry_indices_base(self, exit_indices) -> List[int]:
        entry_i_list = [0, ]  # first point in TXY, is always an entry point

        for exit_i in exit_indices:
            # the next point after an exit point, is always an entry point
            entry_i = exit_i + 1
            if self.entry_point_index_out_of_range(index=entry_i):
                break
            entry_i_list.append(entry_i)
        return entry_i_list

    def _mouse_entry_indices(self) -> List[int]:
        return self._entry_indices_base(exit_indices=self._mouse_exit_indices())

    def _key_entry_indices(self) -> List[int]:
        return self._entry_indices_base(exit_indices=self._key_exit_indices())

    def itxyek_lists(self) -> ITXYEK:
        full_itxyek_lists = self._itxyek_lists

        for mouse_exit_i in self._mouse_exit_indices():
            full_itxyek_lists.e[mouse_exit_i] = p_types.Exit()
            full_itxyek_lists.k[mouse_exit_i] = p_types.Mouse()

        for key_exit_i in self._key_exit_indices():
            full_itxyek_lists.e[key_exit_i] = p_types.Exit()
            full_itxyek_lists.k[key_exit_i] = p_types.Key()

        for mouse_entry_i in self._mouse_entry_indices():
            full_itxyek_lists.e[mouse_entry_i] = p_types.Entry()
            full_itxyek_lists.k[mouse_entry_i] = p_types.Mouse()

        for key_entry_i in self._key_entry_indices():
            full_itxyek_lists.e[key_entry_i] = p_types.Entry()
            full_itxyek_lists.k[key_entry_i] = p_types.Key()

        return full_itxyek_lists


class AltTabPoints:
    """
    When pressing ALT TAB in Tor, the ALT key isn't registered.

    It could be deduced from seeing the mouse stationary for a while,
    then suddenly appearing in a distant location.

    WARNING: prone to false positives.
    The same pattern is probably observed when:
        - using CTR SHIFT PRINTSCREEN.
        - a popup window appears
        - ALT TABs to a non browser window
    Thankfully, it has to coincide with respective critical point in the other browser
    to become a false positive.
    """

    TIME_INACTIVE_THRESHOLD = 2000
    DISTANCE_THRESHOLD = 200

    @staticmethod
    def _inactivity_adequate(t2: int, t1: int) -> bool:
        return t2 - t1 > AltTabPoints.TIME_INACTIVE_THRESHOLD

    @staticmethod
    def _distance_adequate(s: float) -> bool:
        return s > AltTabPoints.DISTANCE_THRESHOLD

    def exit_indices(self, itxyek: ITXYEK) -> List[int]:
        extra_indices = []
        for i, t1, x1, y1, *_ in itxyek.as_iterator():
            if i + 1 not in itxyek.indices:
                break

            t2 = itxyek.time[i + 1]

            x2 = itxyek.x[i + 1]
            y2 = itxyek.y[i + 1]

            space = distance.euclidean([x1, y1], [x2, y2])
            if self._inactivity_adequate(t2=t2, t1=t1) and self._distance_adequate(s=space):
                extra_indices.append(i)
        return extra_indices
