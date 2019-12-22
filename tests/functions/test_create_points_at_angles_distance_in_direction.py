import unittest
import os
from osgeo import ogr
from gdalhelpers.functions.create_points_at_angles_distance_in_direction import create_points_at_angles_distance_in_direction

POINTS_PATH = os.path.join(os.path.dirname(__file__), "..", "test_data", "points.gpkg")
POINT_PATH = os.path.join(os.path.dirname(__file__), "..", "test_data", "single_point.gpkg")


class CreatePointsAtAnglesDistanceInDirectionTestCase(unittest.TestCase):

    def setUp(self):
        self.points_ds = ogr.Open(POINTS_PATH)
        self.point_ds = ogr.Open(POINT_PATH)

    def tearDown(self):
        self.points_ds = None

    def test_create_points_at_angles_distance_in_direction(self):

        result = create_points_at_angles_distance_in_direction(self.points_ds,
                                                               self.point_ds,
                                                               distance=100,
                                                               angle_offset=20,
                                                               angle_density=1,
                                                               input_points_id_field="id_point")

        self.assertIsInstance(result, ogr.DataSource)
        self.assertEqual(result.GetLayer().GetFeatureCount(),
                         self.points_ds.GetLayer().GetFeatureCount()*20*2+self.points_ds.GetLayer().GetFeatureCount())
