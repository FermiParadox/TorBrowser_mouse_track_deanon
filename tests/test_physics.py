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

    def test_dx_(self):
        random_dx = random() * 100
        x1 = 4
        x2 = random_dx + x1
        p1 = (x1, 5)
        p2 = (x2, 12)
        dx = self.Slope2Points(p1=p1, p2=p2).dx
        self.assertEqual(random_dx, dx)

    def test_dy_76(self):
        random_dy = random() * 100
        y1 = 4
        y2 = random_dy + y1
        p1 = (5, y1)
        p2 = (12, y2)
        dy = self.Slope2Points(p1=p1, p2=p2).dy
        self.assertEqual(random_dy, dy)

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

    def test_distance(self):
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
