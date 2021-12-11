from unittest import TestCase


class TestXdotoolAngle(TestCase):
    def test_90deg(self):
        from calibration.angle_conversion import _xdotool_angle

        normal_angle = 90
        self.assertEqual(0, _xdotool_angle(angle=normal_angle))

    def test_0deg(self):
        from calibration.angle_conversion import _xdotool_angle

        normal_angle = 0
        self.assertEqual(90, _xdotool_angle(angle=normal_angle))

    def test_270deg(self):
        from calibration.angle_conversion import _xdotool_angle

        normal_angle = 270
        self.assertEqual(180, _xdotool_angle(angle=normal_angle))

    def test_minus_10deg(self):
        from calibration.angle_conversion import _xdotool_angle

        normal_angle = -10
        self.assertEqual(100, _xdotool_angle(angle=normal_angle))

    def test_disallow_more_than_360(self):
        from calibration.angle_conversion import _xdotool_angle

        normal_angle = 370
        self.assertRaises(ValueError, _xdotool_angle, normal_angle)
