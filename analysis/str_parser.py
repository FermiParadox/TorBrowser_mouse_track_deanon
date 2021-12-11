from ipaddress import ip_address
from typing import List

from analysis.ip_base import IPv6_or_IPv4_obj
from analysis.itxye_base import ITXYE
from analysis.point_types import NON_CRIT_TYPE, ENTRY_TYPE, EXIT_TYPE

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
    def itxye_lists(self) -> ITXYE:
        itxye_lists = ITXYE()
        for i, p in enumerate(self.points_as_list_of_strings()):
            t, x, y = p.split(',')
            itxye_lists.indices.append(i)
            itxye_lists.time.append(int(t))
            itxye_lists.x.append(int(x))
            itxye_lists.y.append(-int(y))  # y-axis goes downwards in browsers unlike cartesian
            itxye_lists.e.append(NON_CRIT_TYPE)

        return itxye_lists


class DataExtractor:
    def __init__(self, req):
        self.req = req
        self.json = req.json
        self._itxye_lists = ITXYStrToArray(data_string=self._mouse_txy_str()).itxye_lists
        self.maximum_itxye_index = self._itxye_lists.indices[-1]

    def _mouse_txy_str(self) -> str:
        return self.json["mouse_txy"]

    def user_id(self) -> int:
        return int(self.json["userID"])

    def user_ip(self) -> IPv6_or_IPv4_obj:
        return ip_address(self.req.remote_addr)

    def _exit_indices_str(self) -> str:
        return self.json["mouse_exit_txy_indices"]

    def _exit_indices(self) -> list:
        return [int(s) for s in self._exit_indices_str().split(POINT_SPLITTER) if s]

    def exit_indices(self) -> list:
        indices_list = self._exit_indices() + AltTabPoints.exit_indices(itxye=self._itxye_lists)
        indices_list.sort()
        return indices_list

    def entry_point_index_out_of_range(self, index) -> bool:
        return index > self.maximum_itxye_index

    def entry_indices(self) -> list:
        entry_i_list = [0, ]  # first point in TXY, is always an entry point

        for exit_i in self.exit_indices():
            # the next point after an exit point, is always an entry point
            entry_i = exit_i + 1
            if self.entry_point_index_out_of_range(index=entry_i):
                break
            entry_i_list.append(entry_i)
        return entry_i_list

    def itxye_lists(self) -> ITXYE:
        itxye_lists_with_e = self._itxye_lists
        for exit_index in self.exit_indices():
            itxye_lists_with_e.e[exit_index] = EXIT_TYPE
        for exit_index in self.entry_indices():
            itxye_lists_with_e.e[exit_index] = ENTRY_TYPE
        return itxye_lists_with_e


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

    def __init__(self, itxye_lists: ITXYE):
        self.itxye_lists = itxye_lists

    @staticmethod
    def exit_indices(itxye: ITXYE) -> List[int]:
        extra_indices = []
        times = itxye.time
        for i, t in enumerate(times):
            if i + 1 not in itxye.indices:
                break

            t_next = times[i + 1]
            if t_next - t > AltTabPoints.TIME_INACTIVE_THRESHOLD:
                extra_indices.append(i)
        return extra_indices
