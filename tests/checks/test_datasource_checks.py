from osgeo import ogr
import unittest
import tempfile
import gdalhelpers.checks.datasource_checks as datasource_checks


class DataSourceChecksTests(unittest.TestCase):

    def setUp(self):
        # point layer
        tf = tempfile.NamedTemporaryFile(suffix=".gpkg")
        file_name = tf.name
        tf.close()
        self.ds_points = ogr.GetDriverByName("GPKG").CreateDataSource(file_name)
        self.layer_point = self.ds_points.CreateLayer("test", geom_type=ogr.wkbPoint)

        tf = tempfile.NamedTemporaryFile(suffix=".shp")
        file_name = tf.name
        tf.close()
        self.ds_shp = ogr.GetDriverByName("ESRI Shapefile").CreateDataSource(file_name)
        self.layer_shp = self.ds_shp.CreateLayer("test", geom_type=ogr.wkbPoint)

    def tearDown(self):
        self.ds_points = None
        self.ds_shp = None

    def test_check_is_ogr_datasource(self):
        with self.assertRaisesRegex(TypeError, "must be of class `ogr.DataSource`"):
            datasource_checks.check_is_ogr_datasource(5, "val")

        self.assertIsInstance(datasource_checks.check_is_ogr_datasource(self.ds_points, "ds"),
                              type(None))

    def test_warn_shapefile_output(self):
        with self.assertWarnsRegex(UserWarning, "not recommended to use `ESRI Shapefile`"):
            datasource_checks.warn_shapefile_output(self.ds_shp, "ds_shp")

        self.assertIsNone(datasource_checks.warn_shapefile_output(self.ds_points, "ds_points"))
