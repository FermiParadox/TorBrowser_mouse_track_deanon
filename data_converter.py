from ipaddress import ip_address

from metrics_dataclasses import XY

POINT_SPLITTER = ":"
COORDINATE_SPLITTER = ","


class TXYStrToArray:
    def __init__(self, data_string):
        self.txy_string = data_string

    def points_as_str(self):
        return [s for s in self.txy_string.split(POINT_SPLITTER) if s]

    @property
    def txy_lists(self):
        t_list = []
        x_list = []
        y_list = []
        for p in self.points_as_str():
            t, x, y = p.split(',')
            t_list.append(int(t))
            x_list.append(int(x))
            y_list.append(-int(y))

        return t_list, x_list, y_list


class MouseDataExtractor:
    def __init__(self, req):
        self.req = req
        self.json = req.json
        self.txy_lists = TXYStrToArray(data_string=self._mouse_txy_str).txy_lists
        self.t_list, self.x_list, self.y_list = self.txy_lists
        self.lists_len = len(self.t_list)
        self.maximum_txy_index = self.lists_len - 1

    @property
    def _mouse_txy_str(self):
        return self.json["mouse_txy"]

    @property
    def user_id(self):
        return int(self.json["userID"])

    @property
    def user_ip(self):
        return ip_address(self.req.remote_addr)

    def _exit_indices_str(self):
        return self.json["mouse_exit_txy_indices"]

    def exit_indices(self):
        return [int(s) for s in self._exit_indices_str().split(POINT_SPLITTER) if s]

    @property
    def exit_times(self):
        return [self.t_list[i] for i in self.exit_indices()]

    def entry_point_index_out_of_range(self, index) -> bool:
        return index > self.maximum_txy_index

    def entry_indices(self):
        i_list = []
        for exit_i in self.exit_indices():
            # the next point is always an entry point
            entry_i = exit_i + 1
            if self.entry_point_index_out_of_range(index=entry_i):
                break
            i_list.append(entry_i)
        return i_list

    @property
    def entry_times(self):
        entry_times = [self.t_list[0]]  # first point is always an entry point
        for entry_index in self.entry_indices():
            t = self.t_list[entry_index]
            entry_times.append(t)
        return entry_times

    @property
    def entry_xy_lists(self) -> XY:
        entry_xy = XY()

        for t in self.entry_times:
            point_index = self.t_list.index(t)
            x = self.x_list[point_index]
            y = self.y_list[point_index]
            entry_xy.x.append(x)
            entry_xy.y.append(y)
        print(entry_xy)
        return entry_xy

    @property
    def exit_xy_lists(self):
        exit_x_list = []
        exit_y_list = []

        for i in self.exit_indices():
            exit_x_list.append(self.x_list[i])
            exit_y_list.append(self.y_list[i])
        return exit_x_list, exit_y_list
