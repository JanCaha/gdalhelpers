from osgeo import ogr, osr
import unittest
import tempfile
import os
import gdalhelpers.helpers.layer_helpers as layer_helpers
import gdalhelpers.checks.layer_checks as layer_checks

POINTS_PATH = os.path.join(os.path.dirname(__file__), "..", "test_data", "points.gpkg")


class LayerHelpersTests(unittest.TestCase):

    def setUp(self):
        # point layer
        tf = tempfile.NamedTemporaryFile(suffix=".gpkg")
        file_name = tf.name
        tf.close()

        self.ds = ogr.GetDriverByName("GPKG").CreateDataSource(file_name)

        self.srs = osr.SpatialReference()
        self.srs.ImportFromEPSG(4326)

        self.ds_points = ogr.Open(POINTS_PATH)

    def tearDown(self):
        self.ds = None
        self.ds_points = None

    def test_create_layer_points(self):
        layer = layer_helpers.create_layer_points(self.ds, self.srs, "points")

        self.assertIsNone(layer_checks.check_is_layer(layer, "layer"))
        self.assertIsNone(layer_checks.check_is_layer_geometry_type(layer, "layer", ogr.wkbPoint))

    def test_create_layer_points_25d(self):
        layer = layer_helpers.create_layer_points_25d(self.ds, self.srs, "points25d")

        self.assertIsNone(layer_checks.check_is_layer(layer, "layer"))
        self.assertIsNone(layer_checks.check_is_layer_geometry_type(layer, "layer", ogr.wkbPoint25D))

    def test_create_layer_lines_25d(self):
        layer = layer_helpers.create_layer_lines_25d(self.ds, self.srs, "lines25d")

        self.assertIsNone(layer_checks.check_is_layer(layer, "layer"))
        self.assertIsNone(layer_checks.check_is_layer_geometry_type(layer, "layer", ogr.wkbLineString25D))

    # TODO add tests for adding values from dictionaries

    def test_get_geometry_list(self):
        layer = self.ds_points.GetLayer()
        feature_count = layer.GetFeatureCount()
        geom_list = layer_helpers.get_geometry_list(layer)
        layer = None

        self.assertIsInstance(geom_list, list)
        self.assertEqual(len(geom_list), feature_count)
        self.assertIsInstance(geom_list[0], ogr.Geometry)
