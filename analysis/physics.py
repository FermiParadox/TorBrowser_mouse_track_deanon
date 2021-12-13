from math import degrees, atan2
from typing import List

from scipy.spatial import distance
from numpy import average

from analysis.itxyek_base import XYPoint, XYFloatPoint


class AngleCalc:
    @staticmethod
    def dy(xy1: XYPoint, xy2: XYPoint) -> float:
        return xy2.y - xy1.y

    @staticmethod
    def dx(xy1: XYPoint, xy2: XYPoint) -> float:
        return xy2.x - xy1.x

    def angle(self, xy1: XYPoint, xy2: XYPoint) -> float:
        return degrees(atan2(self.dy(xy1=xy1, xy2=xy2), self.dx(xy1=xy1, xy2=xy2)))


class Velocity:
    """Velocity is defined as "pixels between 2 points",
    assuming the points are recorded on equal intervals.

    The assumption might be false if affected by browser or PC workload.
    """

    # The distance between 2 diagonal pixels is sqrt(2)
    # Below that the angles are inaccurate.
    SLOW_SPEED = 3
    SMALL_DISTANCE_THRESHOLD = SLOW_SPEED

    @staticmethod
    def distance(xy1: XYPoint, xy2: XYPoint) -> float:
        return distance.euclidean([xy1.x, xy1.y], [xy2.x, xy2.y])

    def distance_too_small(self, xy1: XYPoint, xy2: XYPoint) -> bool:
        return self.distance(xy1=xy1, xy2=xy2) < self.SMALL_DISTANCE_THRESHOLD

    def v(self, xy1: XYPoint, xy2: XYPoint) -> float:
        return self.distance(xy1=xy1, xy2=xy2)


class Acceleration:
    @staticmethod
    def dv(xy1: XYPoint, xy2: XYPoint, xy3: XYPoint) -> float:
        speed_1 = Velocity().v(xy1=xy1, xy2=xy2)
        speed_2 = Velocity().v(xy1=xy2, xy2=xy3)
        return speed_2 - speed_1

    def a(self, xy1: XYPoint, xy2: XYPoint, xy3: XYPoint) -> float:
        return self.dv(xy1=xy1, xy2=xy2, xy3=xy3)


def center_point(x_array: List[int], y_array: List[int]) -> XYFloatPoint:
    len_x = len(x_array)
    len_y = len(y_array)
    if len_x != len_y:
        raise ValueError(f"Arrays of different dims. {len_x} != {len_y}")
    x_average = average(x_array)
    y_average = average(y_array)
    return XYFloatPoint(x=x_average, y=y_average)
