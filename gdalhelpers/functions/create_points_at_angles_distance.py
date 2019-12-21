from osgeo import ogr
from typing import List
import os
import warnings
from gdalhelpers.checks import geometry_checks, layer_checks, datasource_checks
from gdalhelpers.helpers import layer_helpers, datasource_helpers, geometry_helpers


def create_points_at_angles_distance(input_points_ds: ogr.DataSource,
                                     angles: List[float],
                                     distance: float,
                                     input_points_id_field: str = None) -> ogr.Layer:

    output_points_ds = datasource_helpers.create_temp_gpkg_datasource()

    datasource_checks.check_is_ogr_datasource(input_points_ds, "input_points_ds")

    input_points_layer = input_points_ds.GetLayer()

    layer_checks.check_is_layer_geometry_type(input_points_layer, "input_points_layer", [ogr.wkbPoint,
                                                                                         ogr.wkbPoint25D,
                                                                                         ogr.wkbLineStringM,
                                                                                         ogr.wkbPointZM])

    input_points_srs = input_points_layer.GetSpatialRef()

    if not layer_checks.does_field_exist(input_points_layer, input_points_id_field):
        input_points_id_field = None
        warnings.warn(
            "Field `{0}` does not exist in `{1}`. Defaulting to FID."
                .format(input_points_id_field,
                        os.path.basename(input_points_ds))
        )
    else:
        if not layer_checks.is_field_of_type(input_points_layer, input_points_id_field, ogr.OFTInteger):
            input_points_id_field = None
            warnings.warn(
                "Field `{0}` in `{1}` is not `Integer`. Defaulting to FID."
                    .format(input_points_id_field,
                            os.path.basename(input_points_ds))
            )

    if input_points_id_field is None:
        field_name_id = "input_point_FID"
    else:
        field_name_id = "input_point_ID"

    field_name_angle = "angle"

    output_points_layer = layer_helpers.create_layer_points(output_points_ds, input_points_srs, "points")

    fields = {field_name_id: ogr.OFTInteger,
              field_name_angle: ogr.OFTReal}

    layer_helpers.add_fields_from_dict(output_points_layer, fields)

    output_points_def = output_points_layer.GetLayerDefn()

    for feature in input_points_layer:
        geom = feature.GetGeometryRef()

        if input_points_id_field is None:
            f_id = feature.GetFID()
        else:
            f_id = feature.GetField(input_points_id_field)

        for angle in angles:
            p = geometry_helpers.point_at_angle_distance(geom, distance, angle)

            output_point_feature = ogr.Feature(output_points_def)
            output_point_feature.SetGeometry(p)

            values = {field_name_id: f_id,
                      field_name_angle: angle}

            layer_helpers.add_values_from_dict(output_point_feature, values)

            output_points_layer.CreateFeature(output_point_feature)

    return output_points_layer