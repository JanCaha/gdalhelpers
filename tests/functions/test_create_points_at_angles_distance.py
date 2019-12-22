import unittest
import os
import math
from osgeo import ogr
import numpy as np
from gdalhelpers.functions.create_points_at_angles_distance import create_points_at_angles_distance

POINTS_PATH = os.path.join(os.path.dirname(__file__), "..", "test_data", "points.gpkg")


class CreatePointsAtAnglesDistanceTestCase(unittest.TestCase):

    def setUp(self):
        self.points_ds = ogr.Open(POINTS_PATH)

    def tearDown(self):
        self.points_ds = None

    def test_create_points_at_angles_distance(self):

        angles = np.arange(-math.pi, math.pi, (2*math.pi)/36).tolist()
        result = create_points_at_angles_distance(self.points_ds, angles, distance=10)

        self.assertIsInstance(result, ogr.DataSource)

        self.assertEqual(result.GetLayer().GetFeatureCount(), self.points_ds.GetLayer().GetFeatureCount() * len(angles))

        with self.assertRaisesRegex(TypeError, "must be number"):
            angles_wrong = ["string"] + angles
            result = create_points_at_angles_distance(self.points_ds, angles_wrong, distance=20)
