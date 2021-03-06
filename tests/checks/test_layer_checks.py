from osgeo import ogr, gdal, osr
import unittest
import tempfile
import os
import gdalhelpers.checks.layer_checks as layer_checks

POINTS_PATH = os.path.join(os.path.dirname(__file__), "..", "test_data", "points.gpkg")
POINTS_4326_PATH = os.path.join(os.path.dirname(__file__), "..", "test_data", "points_4326.gpkg")
POINT_PATH = os.path.join(os.path.dirname(__file__), "..", "test_data", "single_point.gpkg")


class LayerChecksTests(unittest.TestCase):

    def setUp(self):
        # point layer
        tf = tempfile.NamedTemporaryFile(suffix=".gpkg")
        file_name = tf.name
        tf.close()
        self.ds_points = ogr.GetDriverByName("GPKG").CreateDataSource(file_name)
        self.layer_point = self.ds_points.CreateLayer("test", geom_type=ogr.wkbPoint)
        field_def = ogr.FieldDefn("field_int", ogr.OFTInteger)
        self.layer_point.CreateField(field_def)
        field_def = ogr.FieldDefn("field_real", ogr.OFTReal)
        self.layer_point.CreateField(field_def)
        field_def = ogr.FieldDefn("field_string", ogr.OFTString)
        self.layer_point.CreateField(field_def)

        #load point layer
        self.ds_loaded = ogr.Open(POINTS_PATH)
        self.layer_loaded = self.ds_loaded.GetLayer()

        # load point layer with srs 4326
        self.ds_loaded_4326 = ogr.Open(POINTS_4326_PATH)
        self.layer_loaded_4326 = self.ds_loaded_4326.GetLayer()

    def tearDown(self):
        self.ds_points = None
        self.layer_loaded = None
        self.ds_temp = None

    def test_does_field_exist(self):

        self.assertFalse(layer_checks.does_field_exist(self.layer_point, "wrong_field"))
        self.assertTrue(layer_checks.does_field_exist(self.layer_point, "field_int"))

    def test_get_field_type(self):

        self.assertEqual(layer_checks.get_field_type(self.layer_point, "field_int"), ogr.OFTInteger)
        self.assertEqual(layer_checks.get_field_type(self.layer_point, "field_real"), ogr.OFTReal)
        self.assertEqual(layer_checks.get_field_type(self.layer_point, "field_string"), ogr.OFTString)

    def test_is_field_of_type(self):
        self.assertFalse(layer_checks.is_field_of_type(self.layer_point, "field_int", ogr.OFTString))

        self.assertTrue(layer_checks.is_field_of_type(self.layer_point, "field_int", ogr.OFTInteger))
        self.assertTrue(layer_checks.is_field_of_type(self.layer_point, "field_real", ogr.OFTReal))
        self.assertTrue(layer_checks.is_field_of_type(self.layer_point, "field_string", ogr.OFTString))

    def test_check_is_layer(self):
        self.assertIsNone(layer_checks.check_is_layer(self.layer_point, "layer"))

        with self.assertRaisesRegex(TypeError, "must be of class `ogr.Layer`"):
            layer_checks.check_is_layer(5, "layer")

    def test_check_is_layer_geometry_type(self):

        self.assertIsNone(layer_checks.check_is_layer_geometry_type(self.layer_point, "layer", ogr.wkbPoint))
        self.assertIsNone(layer_checks.check_is_layer_geometry_type(self.layer_point, "layer", [ogr.wkbPolygon,
                                                                                                ogr.wkbPoint]))

        with self.assertRaisesRegex(ValueError, "must be of geometry type"):
            layer_checks.check_is_layer_geometry_type(self.layer_point, "layer", ogr.wkbPolygon)

        with self.assertRaisesRegex(ValueError, "must be of geometry type"):
            layer_checks.check_is_layer_geometry_type(self.layer_point, "layer", [ogr.wkbPolygon, ogr.wkbLineString])

    def test_check_number_of_features(self):

        ds_points = ogr.Open(POINTS_PATH)
        ds_point = ogr.Open(POINT_PATH)

        self.assertIsNone(layer_checks.check_number_of_features(ds_point.GetLayer(), "point", number=1))

        with self.assertRaisesRegex(AttributeError, "must contain only"):
            layer_checks.check_number_of_features(ds_points.GetLayer(), "points", number=1)

    def test_check_is_projected(self):
        self.assertIsNone(layer_checks.check_is_projected(self.layer_loaded, "layer_loaded"))

        with self.assertRaisesRegex(ValueError, "layer does not have Spatial Reference specified"):
            layer_checks.check_is_projected(self.layer_point, "layer_points")

    def test_check_layers_sr_are_same(self):
        self.assertIsNone(layer_checks.check_layers_sr_are_same(self.layer_loaded, "test_srs_1",
                                                                self.layer_loaded, "test_srs_2"))

        with self.assertRaisesRegex(ValueError, "Spatial Reference of both variables"):
            layer_checks.check_layers_sr_are_same(self.layer_loaded_4326, "test_srs_4326",
                                                  self.layer_loaded, "test_srs_loaded")
