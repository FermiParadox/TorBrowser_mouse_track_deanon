import string

POINT_SPLITTER = ":"
COORDINATE_SPLITTER = ","

ALLOWED_CHARS = POINT_SPLITTER + COORDINATE_SPLITTER + string.digits


class TXYConverter:
    def __init__(self, data_string):
        self.data_string = data_string
        self.sanitize_data()

    def not_allowed_chars(self):
        final_str = self.data_string
        for c in ALLOWED_CHARS:
            final_str = final_str.replace(c, '')

    def warn_not_allowed_chars(self):
        raise Warning(f"Not allowed characters in {self.data_string}.")

    def set_data_to_empty(self):
        self.data_string = ''

    def sanitize_data(self):
        if self.not_allowed_chars():
            self.warn_not_allowed_chars()
            self.set_data_to_empty()

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
