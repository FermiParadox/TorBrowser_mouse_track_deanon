from ipaddress import ip_address

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

    @property
    def entry_times(self):
        entry_times = [self.t_list[0]]  # first point is always an entry point
        for exit_index in self.exit_indices():
            # the next point is always an entry point
            entry_point_index = exit_index + 1
            if self.entry_point_index_out_of_range(index=entry_point_index):
                break
            entry_t = self.t_list[entry_point_index]
            entry_times.append(entry_t)
        return entry_times

    @property
    def entry_xy_lists(self):
        entry_x_list = []
        entry_y_list = []

        for t in self.entry_times:
            point_index = self.t_list.index(t)
            x = self.x_list[point_index]
            y = self.y_list[point_index]
            entry_x_list.append(x)
            entry_y_list.append(y)
        return entry_x_list, entry_y_list

    @property
    def exit_xy_lists(self):
        t_list, x_list, y_list = self.txy_lists

        exit_x_list = []
        exit_y_list = []

        for t in self.exit_times:
            point_index = t_list[::-1].index(t)
            point_index = len(t_list) - point_index - 1
            x = x_list[point_index]
            y = y_list[point_index]
            exit_x_list.append(x)
            exit_y_list.append(y)
        return exit_x_list, exit_y_list

    @property
    def _mouse_txy_str(self):
        return self.json["mouse_txy"]
