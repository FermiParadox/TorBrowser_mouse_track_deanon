from unittest import TestCase

from analysis.itxye_base import ITXYEPoint
from analysis.point_types import EntryOrExitType


class TestMatchesCreator(TestCase):
    def setUp(self) -> None:
        from analysis.user_handling import UserMatchCreator
        self.MatchesCreator = UserMatchCreator

        self.p1 = ITXYEPoint(index=0, time=0, x=1, y=512, e=EntryOrExitType(''))
        self.p2 = ITXYEPoint(index=1, time=623, x=512535, y=623, e=EntryOrExitType(''))

    def test_dt_0(self):
        self.p1.time = self.p2.time
        self.assertEqual(0, self.MatchesCreator.dt(p1=self.p1, p2=self.p2))

    def test_dt_5(self):
        dt = 5
        self.p1.time = self.p2.time
        self.p2.time += dt
        self.assertEqual(dt, self.MatchesCreator.dt(p1=self.p1, p2=self.p2))

    def test_dt_minus_5(self):
        dt = -5
        self.p1.time = self.p2.time
        self.p2.time += dt
        self.assertEqual(dt, self.MatchesCreator.dt(p1=self.p1, p2=self.p2))

    def test_dt_in_bounds_less_than_max(self):
        self.assertTrue(self.MatchesCreator.dt_in_bounds(dt=110))

    def test_dt_in_bounds_more_than_min(self):
        self.assertTrue(self.MatchesCreator.dt_in_bounds(dt=-10))

    def test_dt_in_bounds_more_than_max(self):
        self.assertFalse(self.MatchesCreator.dt_in_bounds(dt=150))

    def test_dt_in_bounds_less_than_min(self):
        self.assertFalse(self.MatchesCreator.dt_in_bounds(-50))
