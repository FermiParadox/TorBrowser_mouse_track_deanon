from ipaddress import ip_address

from analysis.ip_base import IPv6_or_IPv4_obj
from analysis.itxye_base import ITXYE
from analysis.point_types import UndefinedCritType, EntryType, ExitType

POINT_SPLITTER = ":"
COORDINATE_SPLITTER = ","


class ITXYStrToArray:
    """The client provides a string like
    "1520095100,25,690:1520095100, 30, 650:"
    """

    def __init__(self, data_string):
        self.txy_string = data_string

    def points_as_list_of_strings(self):
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
            itxye_lists.e.append(UndefinedCritType)

        return itxye_lists


class DataExtractor:
    def __init__(self, req):
        self.req = req
        self.json = req.json
        self.itxye_lists = ITXYStrToArray(data_string=self._mouse_txy_str).itxye_lists
        self.maximum_itxye_index = self.itxye_lists.indices[-1]
        self.insert_exit_entry()

    @property
    def _mouse_txy_str(self) -> str:
        return self.json["mouse_txy"]

    @property
    def user_id(self):
        return int(self.json["userID"])

    @property
    def user_ip(self) -> IPv6_or_IPv4_obj:
        return ip_address(self.req.remote_addr)

    def _exit_indices_str(self) -> str:
        return self.json["mouse_exit_txy_indices"]

    def exit_indices(self) -> list:
        return [int(s) for s in self._exit_indices_str().split(POINT_SPLITTER) if s]

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

    @property
    def entry_itxye(self) -> ITXYE:
        entry_itxye = ITXYE()

        for entry_i in self.entry_indices():
            txy_point = self.itxye_lists.get_point_by_index(index=entry_i)
            entry_itxye.append_point(txy_point)
        return entry_itxye

    @property
    def exit_itxye(self) -> ITXYE:
        exit_itxye = ITXYE()

        for exit_i in self.exit_indices():
            itxye_point = self.itxye_lists.get_point_by_index(index=exit_i)
            exit_itxye.append_point(itxye_point)
        return exit_itxye

    def insert_exit_entry(self) -> None:
        for exit_index in self.exit_indices():
            self.itxye_lists.e[exit_index] = ExitType
        for exit_index in self.entry_indices():
            self.itxye_lists.e[exit_index] = EntryType
