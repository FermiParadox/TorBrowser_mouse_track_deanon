from math import atan, degrees, atan2
from typing import List

from scipy.spatial import distance
from scipy.stats import linregress
from numpy import average

from analysis.itxye_base import XYPoint, XY, XYFloatPoint


class AngleCalc:
    def __init__(self, xy1: XYPoint, xy2: XYPoint, xy_bundle: XY = None):
        self.xy2 = xy2
        self.xy1 = xy1
        self.xy_bundle = xy_bundle

    def dy(self) -> float:
        return self.xy2.y - self.xy1.y

    def dx(self) -> float:
        if self.xy_bundle:
            return self.xy_bundle.x[-1] - self.xy_bundle.x[-2]
        return self.xy2.x - self.xy1.x

    def slope(self) -> float:
        return linregress(self.xy_bundle.x, self.xy_bundle.y).slope

    @staticmethod
    def angle_from_slope(dx, slope) -> float:
        w = degrees(atan(slope))
        if dx < 0:
            w += 180
        return w

    def angle_from_2_points(self) -> float:
        return degrees(atan2(self.dy(), self.dx()))

    def angle(self) -> float:
        if self.xy_bundle:
            return self.angle_from_slope(dx=self.dx(), slope=self.slope())
        return self.angle_from_2_points()


class Speed2Points:
    """Velocity is defined as "pixels between 2 points",
    assuming the points are recorded on equal intervals.

    The assumption might be false if affected by browser or PC workload.
    """

    # The distance between 2 diagonal pixels is sqrt(2)
    # Below that the angles are inaccurate.
    SLOW_SPEED = 2

    def __init__(self, xy1, xy2):
        self.xy1 = xy1
        self.xy2 = xy2

    def distance(self) -> float:
        return distance.euclidean([self.xy1.x, self.xy1.y], [self.xy2.x, self.xy2.y])

    def velocity(self) -> float:
        return self.distance()


class Acceleration:
    def __init__(self, xy1: XYPoint, xy2: XYPoint, xy3: XYPoint):
        self.xy3 = xy3
        self.xy2 = xy2
        self.xy1 = xy1

    def dv(self) -> float:
        speed_1 = Speed2Points(xy1=self.xy1, xy2=self.xy2).velocity()
        speed_2 = Speed2Points(xy1=self.xy2, xy2=self.xy3).velocity()
        return speed_2 - speed_1

    def acceleration(self) -> float:
        return self.dv()


def center_point(x_array: List[int], y_array: List[int]) -> XYFloatPoint:
    len_x = len(x_array)
    len_y = len(y_array)
    if len_x != len_y:
        raise ValueError(f"Arrays of different dims. {len_x} != {len_y}")
    x_average = average(x_array)
    y_average = average(y_array)
    return XYFloatPoint(x=x_average, y=y_average)
