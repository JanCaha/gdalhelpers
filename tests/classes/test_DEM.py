import unittest
import tempfile
import numpy
import os
from osgeo import gdal, ogr
from gdalhelpers.classes.DEM import DEM
from gdalhelpers.helpers import layer_helpers

RASTER_PATH = os.path.join(os.path.dirname(__file__), "..", "test_data", "dsm.tif")
POINTS_PATH = os.path.join(os.path.dirname(__file__), "..", "test_data", "points.gpkg")


class DEMClassTests(unittest.TestCase):

    def setUp(self):
        self.path_to_raster = RASTER_PATH

        tf = tempfile.NamedTemporaryFile(suffix=".tif")
        self.gdal_temp_file = tf.name
        tf.close()

        self.dsm = DEM(self.path_to_raster)

    def tearDown(self):
        pass

    def test_init(self):
        self.assertIsInstance(DEM(self.path_to_raster), DEM)

        with self.assertRaisesRegex(IOError, "File at specified path"):
            DEM("wrong/path/")

    def test_from_gdal_raster(self):
        gdal_dataset = gdal.Open(self.path_to_raster)
        self.assertIsInstance(DEM.from_gdal_raster(gdal_dataset), DEM)

        with self.assertRaisesRegex(TypeError, "`gdal_raster` has to be of type `gdal.Dataset`"):
            DEM.from_gdal_raster("string")

    def test_init_wrong_parameters(self):

        gdal.Warp(self.gdal_temp_file, self.path_to_raster, dstSRS='EPSG:4326')

        with self.assertRaisesRegex(ValueError, "DEM has to be projected"):
            DEM(self.gdal_temp_file)

    def test_warnings_parameters(self):
        with self.assertWarnsRegex(SyntaxWarning, "Raster has specified projection and epsg is set"):
            DEM(self.path_to_raster, epsg=4326)

    def test_array(self):

        self.dsm.load_array()

        self.assertIsInstance(self.dsm.np_array, numpy.ndarray)

        self.dsm.destroy_array()

        self.assertIsNone(self.dsm.np_array)

    def test_get_min_pixel_size(self):
        self.assertIsInstance(self.dsm.get_min_pixel_size(), float)
        self.assertEqual(self.dsm.get_min_pixel_size(), 1)

    def test_get_nodata_value(self):
        self.assertIsInstance(self.dsm.get_nodata_value(), float)
        self.assertAlmostEqual(self.dsm.get_nodata_value(), -3.4028230607370965e+38, places=6)

    def test_get_max_size(self):
        self.assertIsInstance(self.dsm.get_max_size(), float)
        self.assertAlmostEqual(self.dsm.get_max_size(), 223, places=6)

    def test_get_diagonal_size(self):
        self.assertIsInstance(self.dsm.get_diagonal_size(), float)
        self.assertAlmostEqual(self.dsm.get_diagonal_size(), 283.467811, places=6)

    def test_get_bounding_box(self):
        self.assertIsInstance(self.dsm.get_bounding_box(), ogr.Geometry)

    def test_get_value_bilinear(self):
        self.assertAlmostEqual(self.dsm.get_value_bilinear(-336470.645, -1189050.119),
                               1010.77162,
                               places=2)

        self.assertAlmostEqual(self.dsm.get_value_bilinear(-336323.14, -1189196.80),
                               self.dsm.get_nodata_value(),
                               places=6)

        with self.assertRaisesRegex(TypeError, "px must be number"):
            self.dsm.get_value_bilinear("aa", -1189050.119)

        with self.assertRaisesRegex(TypeError, "py must be number"):
            self.dsm.get_value_bilinear(-336470.645, "aa")


    def test_get_values_bilinear(self):
        positions = [[-336470.645, -1189050.119],
                     [-336405.645, -1189162.119],
                     [-336323.14, -1189196.80]]

        values = self.dsm.get_values_bilinear(positions)

        self.assertAlmostEqual(values[0], 1010.7709809776737, places=6)
        self.assertAlmostEqual(values[1], 1016.941226865536, places=6)
        self.assertAlmostEqual(values[2], self.dsm.get_nodata_value(), places=6)

        with self.assertRaisesRegex(ValueError, "Every element of list of positions must be of length `2`"):
            positions = [[-336470.645, -1189050.119],
                         [-336405.645, -1189162.119, 3],
                         [-336323.14, -1189196.80]]

            values = self.dsm.get_values_bilinear(positions)

    def test_get_values_points_bilinear(self):
        ds = ogr.Open(POINTS_PATH)
        layer = ds.GetLayer()
        geom_list = layer_helpers.get_geometry_list(layer)
        values = self.dsm.get_values_points_bilinear(geom_list)
        self.assertListEqual(values, [1006.5723289546559, 999.4730636420012,
                                      988.1533017418318, 994.1223613936003,
                                      1002.6480790314989])

    def test_print(self):
        self.assertIsInstance(self.dsm.__str__(), str)