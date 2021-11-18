class TXYConverter:
    def __init__(self, data_string):
        self.data_string = data_string

    def points_as_str(self):
        return [s for s in self.data_string.split(':') if s]

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
