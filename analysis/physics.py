from math import atan, degrees, atan2
from scipy.spatial import distance
from scipy.stats import linregress

from analysis.itxye_base import XYPoint, XY


class AngleCalc:
    def __init__(self, xy1: XYPoint, xy2: XYPoint, xy_bundle: XY = None):
        self.xy2 = xy2
        self.xy1 = xy1
        self.xy_bundle = xy_bundle

    @property
    def dy(self):
        return self.xy2.y - self.xy1.y

    @property
    def dx(self):
        if self.xy_bundle:
            return self.xy_bundle.x[-1] - self.xy_bundle.x[-2]
        return self.xy2.x - self.xy1.x

    def slope(self):
        return linregress(self.xy_bundle.x, self.xy_bundle.y).slope

    @staticmethod
    def angle_from_slope(dx, slope):
        w = degrees(atan(slope))
        if dx < 0:
            w += 180
        return w

    def angle_from_2_points(self):
        return degrees(atan2(self.dy, self.dx))

    def angle(self):
        if self.xy_bundle:
            return self.angle_from_slope(dx=self.dx, slope=self.slope())
        return self.angle_from_2_points()


class Speed2Points:
    """Velocity is defined as "pixels between 2 points (or more)",
    assuming the points are recorded on equal intervals.

    The assumption might be false if affected by browser or PC workload.
    """

    # The distance between 2 diagonal pixels is sqrt(2)
    # Below that the angles are inaccurate.
    SLOW_SPEED = 2

    def __init__(self, xy1, xy2):
        self.xy1 = xy1
        self.xy2 = xy2

    @property
    def distance(self):
        return distance.euclidean([self.xy1.x, self.xy1.y], [self.xy2.x, self.xy2.y])

    @property
    def velocity(self):
        return self.distance


class Acceleration:
    def __init__(self, xy1, xy2, xy3):
        self.xy3 = xy3
        self.xy2 = xy2
        self.xy1 = xy1

    @property
    def dv(self):
        speed_1 = Speed2Points(xy1=self.xy1, xy2=self.xy2).velocity
        speed_2 = Speed2Points(xy1=self.xy2, xy2=self.xy3).velocity
        return speed_2 - speed_1

    @property
    def acceleration(self):
        return self.dv
