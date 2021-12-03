from ipaddress import ip_address

from analysis.metrics_dataclasses import TimesXY

POINT_SPLITTER = ":"
COORDINATE_SPLITTER = ","


class TXYStrToArray:
    """The client provides a string like
    "1520095100,25,690:1520095100, 30, 650:"
    """
    def __init__(self, data_string):
        self.txy_string = data_string

    def points_as_list_of_strings(self):
        return [s for s in self.txy_string.split(POINT_SPLITTER) if s]

    @property
    def txy_lists(self) -> TimesXY:
        txy_lists = TimesXY()
        for p in self.points_as_list_of_strings():
            t, x, y = p.split(',')
            txy_lists.time.append(int(t))
            txy_lists.x.append(int(x))
            txy_lists.y.append(-int(y))     # y axis goes downwards in browsers unlike cartesian

        return txy_lists


class DataExtractor:
    def __init__(self, req):
        self.req = req
        self.json = req.json
        self.txy_lists = TXYStrToArray(data_string=self._mouse_txy_str).txy_lists
        self.t_list = self.txy_lists.time
        self.x_list = self.txy_lists.x
        self.y_list = self.txy_lists.y
        self.lists_len = len(self.t_list)
        self.maximum_txy_index = self.lists_len - 1

    @property
    def _mouse_txy_str(self) -> str:
        return self.json["mouse_txy"]

    @property
    def user_id(self):
        return int(self.json["userID"])

    @property
    def user_ip(self):
        return ip_address(self.req.remote_addr)

    def _exit_indices_str(self) -> str:
        return self.json["mouse_exit_txy_indices"]

    def exit_indices(self):
        return [int(s) for s in self._exit_indices_str().split(POINT_SPLITTER) if s]

    def entry_point_index_out_of_range(self, index) -> bool:
        return index > self.maximum_txy_index

    def entry_indices(self):
        entry_i_list = [0, ]  # first point in TXY, is always an entry point

        for exit_i in self.exit_indices():
            # the next point after an exit point, is always an entry point
            entry_i = exit_i + 1
            if self.entry_point_index_out_of_range(index=entry_i):
                break
            entry_i_list.append(entry_i)
        return entry_i_list

    @property
    def entry_txy(self) -> TimesXY:
        entry_txy = TimesXY()

        for entry_i in self.entry_indices():
            txy_point = self.txy_lists.get_point_by_index(index=entry_i)
            entry_txy.append_point(txy_point)
        return entry_txy

    @property
    def exit_txy(self) -> TimesXY:
        exit_txy = TimesXY()

        for exit_i in self.exit_indices():
            txy_point = self.txy_lists.get_point_by_index(index=exit_i)
            exit_txy.append_point(txy_point)
        return exit_txy
