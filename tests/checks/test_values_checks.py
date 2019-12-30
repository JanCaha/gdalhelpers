import unittest
import gdalhelpers.checks.values_checks as values_check
import math


class ValuesCheckTests(unittest.TestCase):

    def test_check_value_is_zero_or_positive(self):
        with self.assertRaisesRegex(TypeError, "must be either `int` or `float`"):
            values_check.check_value_is_zero_or_positive("test", "val")

        with self.assertRaisesRegex(ValueError, "must be higher than 0"):
            values_check.check_value_is_zero_or_positive(-5, "val")

        self.assertIsInstance(values_check.check_value_is_zero_or_positive(5, "val"),
                              type(None))

    def test_check_return_value_is_angle(self):
        with self.assertRaisesRegex(TypeError, "must be either `int` or `float`"):
            values_check.check_return_value_is_angle("test", "val")

        self.assertAlmostEqual(values_check.check_return_value_is_angle(math.pi*1.1, "val"),
                               -math.pi*0.9, places=6)
        self.assertAlmostEqual(values_check.check_return_value_is_angle(-math.pi*1.5, "val"),
                               math.pi*0.5, places=6)
        self.assertAlmostEqual(values_check.check_return_value_is_angle(0, "val"),
                               0, places=6)
        self.assertAlmostEqual(values_check.check_return_value_is_angle(0.2345, "val"),
                               0.2345, places=6)
        self.assertAlmostEqual(values_check.check_return_value_is_angle(-1.2345, "val"),
                               -1.2345, places=6)

    def test_check_return_value_is_angle_degrees(self):
        with self.assertRaisesRegex(TypeError, "must be either `int` or `float`"):
            values_check.check_return_value_is_angle_degrees("test", "val")

        self.assertEqual(values_check.check_return_value_is_angle_degrees(0, "val"), 0)
        self.assertEqual(values_check.check_return_value_is_angle_degrees(90, "val"), 90)
        self.assertEqual(values_check.check_return_value_is_angle_degrees(180, "val"), 180)
        self.assertEqual(values_check.check_return_value_is_angle_degrees(360, "val"), 360)
        self.assertEqual(values_check.check_return_value_is_angle_degrees(370, "val"), 10)
        self.assertEqual(values_check.check_return_value_is_angle_degrees(-10, "val"), 350)

    def test_check_number(self):
        self.assertIsNone(values_check.check_number(5, "val"))
        self.assertIsNone(values_check.check_number(3.5, "val"))
        self.assertIsNone(values_check.check_number(4e-5, "val"))

        with self.assertRaisesRegex(TypeError, "must be either `int` or `float`"):
            values_check.check_number("test", "val")