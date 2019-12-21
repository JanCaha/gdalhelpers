import unittest
import gdalhelpers.checks.values_checks as values_check
import math


class ValuesCheckTests(unittest.TestCase):

    def test_check_value_is_zero_or_positive(self):
        with self.assertRaisesRegex(TypeError, "must be number"):
            values_check.check_value_is_zero_or_positive("test", "val")

        with self.assertRaisesRegex(ValueError, "must be higher than 0"):
            values_check.check_value_is_zero_or_positive(-5, "val")

        self.assertIsInstance(values_check.check_value_is_zero_or_positive(5, "val"),
                              type(None))

    def test_check_return_value_is_angle(self):
        with self.assertRaisesRegex(TypeError, "must be number"):
            values_check.check_return_value_is_angle("test", "val")

        self.assertAlmostEqual(values_check.check_return_value_is_angle(math.pi + 0.1, "val"),
                               0.1, places=6)
        self.assertAlmostEqual(values_check.check_return_value_is_angle(-math.pi - 0.5, "val"),
                               -0.5, places=6)
        self.assertAlmostEqual(values_check.check_return_value_is_angle(0, "val"),
                               0, places=6)
        self.assertAlmostEqual(values_check.check_return_value_is_angle(0.2345, "val"),
                               0.2345, places=6)
        self.assertAlmostEqual(values_check.check_return_value_is_angle(-1.2345, "val"),
                               -1.2345, places=6)
