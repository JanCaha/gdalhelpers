from osgeo import ogr
import unittest
from gdalhelpers.helpers import datasource_helpers


class DatasourceHelpersTests(unittest.TestCase):

    def test_create_temp_gpkg_datasource(self):

        datasource = datasource_helpers.create_temp_gpkg_datasource()

        self.assertIsInstance(datasource, ogr.DataSource)
        self.assertIn("gpkg", datasource.GetDescription())
        self.assertIn("/vsimem/", datasource.GetDescription())
