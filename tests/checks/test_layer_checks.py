from osgeo import ogr
import unittest
import tempfile
import gdalhelpers.checks.layer_checks as layer_checks


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

    def tearDown(self):
        self.ds_points = None

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

        with self.assertRaisesRegex(TypeError, "must be of geometry type"):
            layer_checks.check_is_layer_geometry_type(self.layer_point, "layer", ogr.wkbPolygon)

        with self.assertRaisesRegex(TypeError, "must be of geometry type"):
            layer_checks.check_is_layer_geometry_type(self.layer_point, "layer", [ogr.wkbPolygon, ogr.wkbLineString])