from math import atan2


class ArcTan2Points:
    def __init__(self, p1, p2):
        self.p2 = p2
        self.p1 = p1

    @property
    def angle(self):
        dy = self.p2[1] - self.p1[1]
        dx = self.p2[0] - self.p1[0]
        return atan2(dy, dx)
