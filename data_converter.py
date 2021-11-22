from ipaddress import ip_address

POINT_SPLITTER = ":"
COORDINATE_SPLITTER = ","


class TXYStrToArray:
    def __init__(self, data_string):
        self.data_string = data_string
        self.t = []
        self.x = []
        self.y = []
        self.create_txy_lists()

    def points_as_str(self):
        return [s for s in self.data_string.split(POINT_SPLITTER) if s]

    def create_txy_lists(self):
        t_list = []
        x_list = []
        y_list = []
        for p in self.points_as_str():
            t, x, y = p.split(',')
            t_list.append(int(t))
            x_list.append(int(x))
            y_list.append(-int(y))

        self.t = t_list
        self.x = x_list
        self.y = y_list

    @property
    def txy_lists(self):
        return self.t, self.x, self.y


class ActionDataExtractor:
    def __init__(self, req):
        self.req = req
        self.json = req.json

    @property
    def mouse_txy_str(self):
        return self.json["mouse_txy"]

    @property
    def user_id_str(self):
        return self.json["userID"]

    @property
    def user_ip_str(self):
        return ip_address(self.req.remote_addr)

    @property
    def mouse_crit_t_str(self):
        return self.json["mouse_crit_t"]
