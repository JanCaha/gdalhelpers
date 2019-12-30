from osgeo import ogr
import unittest
import tempfile
import gdalhelpers.checks.geometry_checks as geometry_checks


class GeometryChecksTests(unittest.TestCase):

    def setUp(self):
        # point
        self.point = ogr.Geometry(ogr.wkbPoint)
        self.point.AddPoint_2D(0, 0)

    def tearDown(self):
        self.ds_points = None

    def test_check_variable_geometry(self):

        with self.assertRaisesRegex(TypeError, "must be of class `ogr.Geometry`"):
            geometry_checks.check_variable_expected_geometry("test", "val", ogr.wkbPoint)

        with self.assertRaisesRegex(ValueError, "must be of geometry type/types"):
            geometry_checks.check_variable_expected_geometry(self.point, "val", ogr.wkbLineString)

        with self.assertRaisesRegexp(ValueError, "must be of geometry type/types"):
            geometry_checks.check_variable_expected_geometry(self.point, "val", [ogr.wkbPointM, ogr.wkbPointZM])

        self.assertIsNone(geometry_checks.check_variable_expected_geometry(self.point, "val", ogr.wkbPoint))
        self.assertIsNone(geometry_checks.check_variable_expected_geometry(self.point, "val",
                                                                           [ogr.wkbLineString, ogr.wkbPolygon, ogr.wkbPoint]))

    def test_check_is_wkt_geometery(self):
        self.assertIsNone(geometry_checks.check_is_wkt_geometry("POINT (1120351.5712494177 741921.4223245403)", "val"))

        with self.assertRaisesRegexp(ValueError, "is not a valid WKT"):
            geometry_checks.check_is_wkt_geometry("string, not WKT", "val")