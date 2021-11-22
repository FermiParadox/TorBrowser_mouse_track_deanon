import string
from ipaddress import ip_address

POINT_SPLITTER = ":"
COORDINATE_SPLITTER = ","


ALLOWED_CHARS = POINT_SPLITTER + COORDINATE_SPLITTER + string.digits


class TXYStrToArray:
    def __init__(self, data_string):
        self.data_string = data_string

    def points_as_str(self):
        return [s for s in self.data_string.split(POINT_SPLITTER) if s]

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

    @property
    def mouse_txy_str(self):
        return self.json["mouse_trajectory"]

    @property
    def user_id_str(self):
        return self.json["userID"]

    @property
    def user_ip_str(self):
        return ip_address(self.req.remote_addr)
