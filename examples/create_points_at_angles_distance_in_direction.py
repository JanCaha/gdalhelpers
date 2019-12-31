from osgeo import ogr
import os
from gdalhelpers.functions import create_points_at_angles_distance_in_direction

PATH_DATA = os.path.join(os.path.dirname(__file__), "..", "tests", "test_data")
PATH_DATA_RESULTS = os.path.join(PATH_DATA, "results")

points = ogr.Open(os.path.join(PATH_DATA, "points.gpkg"))
direction_point = ogr.Open(os.path.join(PATH_DATA, "single_point.gpkg"))

direction_points = create_points_at_angles_distance_in_direction(points, direction_point,
                                                                 distance=25,
                                                                 angle_offset=20, angle_density=5)

ds_direction_points = ogr.GetDriverByName("GPKG").CreateDataSource(os.path.join(PATH_DATA_RESULTS,
                                                                                "points_direction.gpkg"))

ds_direction_points.CopyLayer(direction_points.GetLayer(), "points_around", ["OVERWRITE=YES"])

ds_points_around = None