from unittest import TestCase
from random import randint

from analysis.itxyek_base import XYPoint
from analysis.physics import center_point


class TestAngleCalc(TestCase):
    def setUp(self) -> None:
        from analysis.physics import AngleCalc
        self.AngleCalc = AngleCalc

    def test_2points_dx_0(self):
        x = randint(-100, 100)
        xy1 = XYPoint(x=x, y=5)
        xy2 = XYPoint(x=x, y=12)
        self.assertEqual(0, self.AngleCalc(xy1=xy1, xy2=xy2).dx())

    def test_2points_dy_0(self):
        y = randint(-100, 100)
        xy1 = XYPoint(x=7, y=y)
        xy2 = XYPoint(x=6, y=y)
        self.assertEqual(0, self.AngleCalc(xy1=xy1, xy2=xy2).dy())

    def test_2points_dx_any(self):
        random_dx = randint(-100, 100)
        x1 = 4
        x2 = random_dx + x1
        xy1 = XYPoint(x=x1, y=5)
        xy2 = XYPoint(x=x2, y=12)
        self.assertAlmostEqual(random_dx, self.AngleCalc(xy1=xy1, xy2=xy2).dx())

    def test_2points_dy_any(self):
        random_dy = randint(-100, 100)
        y1 = 4
        y2 = random_dy + y1
        xy1 = XYPoint(x=5, y=y1)
        xy2 = XYPoint(x=12, y=y2)
        self.assertAlmostEqual(random_dy, self.AngleCalc(xy1=xy1, xy2=xy2).dy())

    def test_2points_same_y_angle_0(self):
        y = randint(-100, 100)
        xy1 = XYPoint(x=4, y=y)
        xy2 = XYPoint(x=518, y=y)
        self.assertEqual(0, self.AngleCalc(xy1=xy1, xy2=xy2).angle())

    def test_2points_angle_45deg(self):
        xy1 = XYPoint(x=1, y=1)
        xy2 = XYPoint(x=22, y=22)
        self.assertAlmostEqual(45, self.AngleCalc(xy1=xy1, xy2=xy2).angle())

    def test_2points_angle_90deg(self):
        xy1 = XYPoint(x=1, y=1)
        xy2 = XYPoint(x=1, y=2)
        self.assertAlmostEqual(90, self.AngleCalc(xy1=xy1, xy2=xy2).angle())


class TestSpeed2Points(TestCase):
    def setUp(self) -> None:
        from analysis.physics import Velocity
        self.Speed2Points = Velocity

    def test_distance_is_sqrt2(self):
        from math import sqrt
        xy1 = XYPoint(x=1, y=1)
        xy2 = XYPoint(x=2, y=2)
        distance = self.Speed2Points(xy1=xy1, xy2=xy2).distance()
        self.assertAlmostEqual(sqrt(2), distance)

    def test_speed_0(self):
        xy1 = XYPoint(x=4, y=1)
        xy2 = XYPoint(x=4, y=1)
        speed = self.Speed2Points(xy1=xy1, xy2=xy2).v()
        self.assertEqual(0, speed)

    def test_speed_20(self):
        xy1 = XYPoint(x=1, y=1)
        xy2 = XYPoint(x=1, y=21)
        speed = self.Speed2Points(xy1=xy1, xy2=xy2).v()
        self.assertEqual(20, speed)


class TestAcceleration3Points(TestCase):
    def setUp(self) -> None:
        from analysis.physics import Acceleration
        self.Acceleration = Acceleration

    def test_dv(self):
        from scipy.spatial import distance
        xy1 = XYPoint(x=1, y=1)
        xy2 = XYPoint(x=2, y=6)
        xy3 = XYPoint(x=7, y=3)
        v1 = distance.euclidean(xy2.as_tuple(), xy1.as_tuple())
        v2 = distance.euclidean(xy3.as_tuple(), xy2.as_tuple())
        dv_expected = v2 - v1
        dv = self.Acceleration(xy1=xy1, xy2=xy2, xy3=xy3).dv()
        self.assertAlmostEqual(dv_expected, dv)

    def test_acceleration_0(self):
        xy1 = XYPoint(x=1, y=2)
        xy2 = XYPoint(x=2, y=3)
        xy3 = XYPoint(x=3, y=4)
        acceleration = self.Acceleration(xy1=xy1, xy2=xy2, xy3=xy3).a()
        self.assertAlmostEqual(0, acceleration)

    def test_acceleration(self):
        from scipy.spatial import distance
        xy1 = XYPoint(x=6, y=2)
        xy2 = XYPoint(x=47, y=6)
        xy3 = XYPoint(x=85, y=25)
        v1 = distance.euclidean(xy2.as_tuple(), xy1.as_tuple())
        v2 = distance.euclidean(xy3.as_tuple(), xy2.as_tuple())
        acceleration_expected = (v2 - v1)
        acceleration = self.Acceleration(xy1=xy1, xy2=xy2, xy3=xy3).a()
        self.assertAlmostEqual(acceleration_expected, acceleration)


class TestCenterPoint(TestCase):
    def test_0_0(self):
        x = [-3, 0, 1, 2]
        y = [-10, 2, 4, 4]
        cp = center_point(x_array=x, y_array=y)
        self.assertEqual((cp.x, cp.y), (0, 0))

    def test_minus_1_plus_0point5(self):
        x = [-4, 2]
        y = [0, 1]
        cp = center_point(x_array=x, y_array=y)
        self.assertEqual((cp.x, cp.y), (-1, 0.5))

    def test_different_size(self):
        x = [-3, 0]
        y = [-10, 2, 4, 4]
        self.assertRaises(ValueError, center_point, x_array=x, y_array=y)

