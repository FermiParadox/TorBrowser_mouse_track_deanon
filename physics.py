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


class Acceleration3Points:
    def __init__(self, p1, p2, p3, t1, t2, t3):
        self.t3 = t3
        self.p3 = p3
        self.t2 = t2
        self.t1 = t1
        self.p2 = p2
        self.p1 = p1

    @property
    def dt(self):
        return self.t3 - self.t1

    @property
    def du(self):
        speed_1 = Speed2Points(p1=self.p1, p2=self.p2, t1=self.t1, t2=self.t2).speed
        speed_2 = Speed2Points(p1=self.p2, p2=self.p3, t1=self.t2, t2=self.t3).speed
        return speed_2 - speed_1

    @property
    def acceleration(self):
        return self.du / self.dt
