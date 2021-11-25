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


class ActionDataExtractor:
    def __init__(self, req):
        self.req = req
        self.json = req.json
        self.txy_lists = TXYStrToArray(data_string=self._mouse_txy_str).txy_lists

    @property
    def user_id(self):
        return int(self.json["userID"])

    @property
    def user_ip(self):
        return ip_address(self.req.remote_addr)

    @property
    def _mouse_crit_t_str(self):
        return self.json["mouse_exit_t"]

    @property
    def mouse_exit_t(self):
        return [int(s) for s in self._mouse_crit_t_str.split(POINT_SPLITTER) if s]

    @property
    def mouse_entry_crit_xy(self):
        t_list, x_list, y_list = self.txy_lists
        list_size = len(t_list)

        critical_entry_x = []
        critical_entry_y = []

        for t in self.mouse_exit_t:
            point_index = t_list.index(t) + 1
            if point_index >= list_size - 1:
                break
            x = x_list[point_index]
            y = y_list[point_index]
            critical_entry_x.append(x)
            critical_entry_y.append(y)
        return critical_entry_x, critical_entry_y

    @property
    def mouse_exit_crit_xy(self):
        t_list, x_list, y_list = self.txy_lists

        critical_exit_x = []
        critical_exit_y = []

        for t in self.mouse_exit_t:
            point_index = t_list.index(t)
            x = x_list[point_index]
            y = y_list[point_index]
            critical_exit_x.append(x)
            critical_exit_y.append(y)
        return critical_exit_x, critical_exit_y

    @property
    def _mouse_txy_str(self):
        return self.json["mouse_txy"]
