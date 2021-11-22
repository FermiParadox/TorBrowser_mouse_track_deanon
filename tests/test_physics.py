from unittest import TestCase
from math import pi
from random import random


class TestSlope2Points(TestCase):
    def setUp(self) -> None:
        from physics import Slope2Points
        self.Slope2Points = Slope2Points

    def test_dx_0(self):
        x = random()
        p1 = (x, 5)
        p2 = (x, 12)
        dx = self.Slope2Points(p1=p1, p2=p2).dx
        self.assertEqual(0, dx)

    def test_dy_0(self):
        y = random()
        p1 = (7, y)
        p2 = (6, y)
        dy = self.Slope2Points(p1=p1, p2=p2).dy
        self.assertEqual(0, dy)

    def test_dx_any(self):
        random_dx = random() * 100
        x1 = 4
        x2 = random_dx + x1
        p1 = (x1, 5)
        p2 = (x2, 12)
        dx = self.Slope2Points(p1=p1, p2=p2).dx
        self.assertAlmostEqual(random_dx, dx)

    def test_dy_any(self):
        random_dy = random() * 100
        y1 = 4
        y2 = random_dy + y1
        p1 = (5, y1)
        p2 = (12, y2)
        dy = self.Slope2Points(p1=p1, p2=p2).dy
        self.assertAlmostEqual(random_dy, dy)

    def test_angle_0_when_points_same_y(self):
        y = random()
        p1 = (4, y)
        p2 = (518, y)
        angle = self.Slope2Points(p1=p1, p2=p2).angle
        self.assertEqual(0, angle)

    def test_angle_45deg(self):
        p1 = (1, 1)
        p2 = (22, 22)
        angle = self.Slope2Points(p1=p1, p2=p2).angle
        self.assertAlmostEqual(pi / 4, angle)

    def test_angle_90deg(self):
        p1 = (1, 1)
        p2 = (1, 2)
        angle = self.Slope2Points(p1=p1, p2=p2).angle
        self.assertAlmostEqual(pi / 2, angle)


class TestSpeed2Points(TestCase):
    def setUp(self) -> None:
        from physics import Speed2Points
        self.Speed2Points = Speed2Points

    def test_dt_0(self):
        p1 = (1, 7)
        p2 = (5, 2)
        t = random()
        dt = self.Speed2Points(p1=p1, p2=p2, t1=t, t2=t).dt
        self.assertEqual(0, dt)

    def test_distance_is_sqrt2(self):
        from math import sqrt
        p1 = (1, 1)
        p2 = (2, 2)
        distance = self.Speed2Points(p1=p1, p2=p2, t1=6, t2=237).distance
        self.assertAlmostEqual(sqrt(2), distance)

    def test_speed_0(self):
        p1 = (4, 1)
        p2 = (4, 1)
        speed = self.Speed2Points(p1=p1, p2=p2, t1=6, t2=237).speed
        self.assertEqual(0, speed)

    def test_speed_20(self):
        p1 = (1, 1)
        p2 = (1, 21)
        speed = self.Speed2Points(p1=p1, p2=p2, t1=6, t2=7).speed
        self.assertEqual(20, speed)


class TestAcceleration3Points(TestCase):
    def setUp(self) -> None:
        from physics import Acceleration3Points
        self.Acceleration3Points = Acceleration3Points

    def test_dt(self):
        dt_expected = random()
        p1 = (1, 1)
        p2 = (2, 6)
        p3 = (7, 3)
        t1 = 1
        t2 = 4
        t3 = t1 + dt_expected
        dt = self.Acceleration3Points(p1=p1, p2=p2, p3=p3, t1=t1, t2=t2, t3=t3).dt
        self.assertAlmostEqual(dt_expected, dt)

    def test_dv(self):
        from scipy.spatial import distance
        p1 = (1, 1)
        p2 = (2, 6)
        p3 = (7, 3)
        t1 = 1
        t2 = 4
        t3 = 25
        v1 = distance.euclidean(p2, p1) / (t2 - t1)
        v2 = distance.euclidean(p3, p2) / (t3 - t2)
        dv_expected = v2 - v1
        dv = self.Acceleration3Points(p1=p1, p2=p2, p3=p3, t1=t1, t2=t2, t3=t3).dv
        self.assertAlmostEqual(dv_expected, dv)

    def test_acceleration_0(self):
        p1 = (1, 2)
        p2 = (2, 3)
        p3 = (3, 4)
        t1 = 1
        t2 = 2
        t3 = 3
        acceleration = self.Acceleration3Points(p1=p1, p2=p2, p3=p3, t1=t1, t2=t2, t3=t3).acceleration
        self.assertAlmostEqual(0, acceleration)

    def test_acceleration(self):
        from scipy.spatial import distance
        p1 = (6, 2)
        p2 = (47, 6)
        p3 = (85, 25)
        t1 = 1
        t2 = 4
        t3 = 8
        v1 = distance.euclidean(p2, p1) / (t2 - t1)
        v2 = distance.euclidean(p3, p2) / (t3 - t2)
        acceleration_expected = (v2 - v1) / (t3 - t1)
        acceleration = self.Acceleration3Points(p1=p1, p2=p2, p3=p3, t1=t1, t2=t2, t3=t3).acceleration
        self.assertAlmostEqual(acceleration_expected, acceleration)
