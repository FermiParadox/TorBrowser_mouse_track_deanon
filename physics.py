from math import atan2
from scipy.spatial import distance


class Slope2Points:
    def __init__(self, p1, p2):
        self.p2 = p2
        self.p1 = p1

    @property
    def dy(self):
        return self.p2[1] - self.p1[1]

    @property
    def dx(self):
        return self.p2[0] - self.p1[0]

    @property
    def angle(self):
        return atan2(self.dy, self.dx)


class Speed2Points:
    def __init__(self, p1, p2, t1, t2):
        self.t2 = t2
        self.t1 = t1
        self.p2 = p2
        self.p1 = p1

    @property
    def dt(self):
        return self.t2 - self.t1

    @property
    def distance(self):
        return distance.euclidean(self.p1, self.p2)

    @property
    def speed(self):
        return self.distance / self.dt
