from ipaddress import ip_address

from metrics_dataclasses import XY, TimeXY

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
    def txy_lists(self) -> TimeXY:
        txy_lists = TimeXY()
        for p in self.points_as_list_of_strings():
            t, x, y = p.split(',')
            txy_lists.time.append(int(t))
            txy_lists.x.append(int(x))
            txy_lists.y.append(-int(y))     # y axis goes downwards in browsers unlike cartesian

        return txy_lists


class MouseDataExtractor:
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

    @property
    def exit_times(self):
        return [self.t_list[i] for i in self.exit_indices()]

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
    def entry_times(self):
        entry_times = []
        for entry_index in self.entry_indices():
            t = self.t_list[entry_index]
            entry_times.append(t)
        return entry_times

    @property
    def entry_txy(self) -> TimeXY:
        entry_txy = TimeXY()

        for entry_i in self.entry_indices():
            x = self.x_list[entry_i]
            y = self.y_list[entry_i]
            t = self.t_list[entry_i]
            entry_txy.x.append(x)
            entry_txy.y.append(y)
            entry_txy.time.append(t)
        return entry_txy

    @property
    def exit_txy(self) -> TimeXY:
        exit_txy = TimeXY()

        for exit_i in self.exit_indices():
            x = self.x_list[exit_i]
            y = self.y_list[exit_i]
            t = self.t_list[exit_i]
            exit_txy.x.append(x)
            exit_txy.y.append(y)
            exit_txy.time.append(t)
        return exit_txy
