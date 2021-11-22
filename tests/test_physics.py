from unittest import TestCase

from physics import ArcTan2Points


class TestArcTan2Points(TestCase):
    def test_0_when_parallel_to_x_axis(self):
        p1 = (4, 2)
        p2 = (518, 2)
        angle = ArcTan2Points(p1=p1, p2=p2).angle
        self.assertEqual(0, angle)
