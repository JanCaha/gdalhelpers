from osgeo import ogr
from typing import List
import math
import os
import warnings
import numpy as np
import numbers.Number
from gdalhelpers.checks import values_checks, datasource_checks, layer_checks
from gdalhelpers.helpers import layer_helpers, datasource_helpers, geometry_helpers


def create_points_at_angles_distance_in_direction(start_points: ogr.DataSource,
                                                  main_direction_point: ogr.DataSource,
                                                  distance: numbers.Number,
                                                  output_points_ds: ogr.DataSource,
                                                  angle_offset: numbers.Number = ((2*math.pi)/360)*10,
                                                  angle_density: numbers.Number = (2*math.pi)/360,
                                                  input_points_id_field: str = None) -> str:

    output_points_ds = datasource_helpers.create_temp_gpkg_datasource()

    datasource_checks.check_is_ogr_datasource(start_points, "start_points")
    datasource_checks.check_is_ogr_datasource(main_direction_point, "main_direction_point")

    values_checks.check_value_is_zero_or_positive(distance, "distance")

    input_points_layer = start_points.GetLayer()
    layer_checks.check_is_layer_geometry_type(input_points_layer, "input_points_layer", [ogr.wkbPoint, ogr.wkbPoint25D,
                                                                                         ogr.wkbPointM, ogr.wkbPointZM])

    input_points_srs = input_points_layer.GetSpatialRef()

    main_point_layer = main_direction_point.GetLayer()
    layer_checks.check_is_layer_geometry_type(main_point_layer, "main_point_layer", [ogr.wkbPoint, ogr.wkbPoint25D,
                                                                                     ogr.wkbPointM, ogr.wkbPointZM])
    layer_checks.check_number_of_features(main_point_layer, "main_point_layer", 1)

    if input_points_id_field is not None:
        if not layer_checks.does_field_exist(input_points_layer, input_points_id_field):
            input_points_id_field = None
            warnings.warn(
                "Field {0} does not exist in {1}. Defaulting to FID.".format(input_points_id_field,
                                                                             os.path.basename(start_points))
            )
        else:
            if not layer_checks.is_field_of_type(input_points_layer, input_points_id_field, "Integer"):
                input_points_id_field = None
                warnings.warn(
                    "Field {0} in {1} is not `Integer`. Defaulting to FID.".format(input_points_id_field,
                                                                                   os.path.basename(start_points))
                )

    if input_points_id_field is None:
        field_name_id = "input_point_FID"
    else:
        field_name_id = "input_point_ID"

    field_name_angle = "angle"

    output_points_layer = layer_checks.create_layer_points(output_points_ds, input_points_srs, "points")

    fields = {field_name_id: ogr.OFTInteger,
              field_name_angle: ogr.OFTReal}

    layer_checks.add_fields_from_dict(output_points_layer, fields)

    output_points_def = output_points_layer.GetLayerDefn()

    for main_feature in main_point_layer:

        main_geom = main_feature.GetGeometryRef()

        for feature in input_points_layer:
            geom = feature.GetGeometryRef()

            if input_points_id_field is None:
                f_id = feature.GetFID()
            else:
                f_id = feature.GetField(input_points_id_field)

            main_angle = geometry_helpers.angle_points(geom, main_geom)

            angles = np.arange(main_angle - angle_offset,
                               np.nextafter(main_angle + angle_offset, np.Inf),
                               step=angle_density)

            for angle in angles:
                p = geometry_helpers.point_at_angle_distance(geom, distance, angle)

                output_point_feature = ogr.Feature(output_points_def)
                output_point_feature.SetGeometry(p)

                values = {field_name_id: f_id,
                          field_name_angle: angle}

                layer_helpers.add_values_from_dict(output_point_feature, values)

                output_points_layer.CreateFeature(output_point_feature)

        return output_points_layer
