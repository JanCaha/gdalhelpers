from osgeo import ogr
import os
import numpy as np
from gdalhelpers.functions import create_points_at_angles_distance

PATH_DATA = os.path.join(os.path.dirname(__file__), "..", "tests", "test_data")
PATH_DATA_RESULTS = os.path.join(PATH_DATA, "results")

points = ogr.Open(os.path.join(PATH_DATA, "points.gpkg"))

angles = np.arange(0, 360, step=10).tolist()

new_points = create_points_at_angles_distance(points, angles=angles, distance=25)

ds_points_around = ogr.GetDriverByName("GPKG").CreateDataSource(os.path.join(PATH_DATA_RESULTS, "points_around.gpkg"))
ds_points_around.CopyLayer(new_points.GetLayer(), "points_around", ["OVERWRITE=YES"])

ds_points_around = None