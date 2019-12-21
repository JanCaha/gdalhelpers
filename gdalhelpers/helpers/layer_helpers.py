from osgeo import ogr, osr
from typing import List


def create_layer_points(los_ds: ogr.DataSource, srs: osr.SpatialReference, layer_name: str):
    return los_ds.CreateLayer(layer_name, srs, ogr.wkbPoint, ['OVERWRITE=YES'])


def create_layer_points_25d(los_ds: ogr.DataSource, srs: osr.SpatialReference, layer_name: str):
    return los_ds.CreateLayer(layer_name, srs, ogr.wkbPoint25D, ['OVERWRITE=YES'])


def create_layer_lines_25d(los_ds: ogr.DataSource, srs: osr.SpatialReference, layer_name: str):
    return los_ds.CreateLayer(layer_name, srs, ogr.wkbLineString25D, ['OVERWRITE=YES'])


def add_fields_from_dict(layer: ogr.Layer, fields_types: dict):

    for field, types in fields_types.items():
        field_def = ogr.FieldDefn(field, types)
        layer.CreateField(field_def)


def add_values_from_dict(feature: ogr.Feature, fields_values: dict):

    for field, value in fields_values.items():
        feature.SetField(field, value)


def get_geometry_list(layer: ogr.Layer) -> List[str]:

    feature_list: list = [None] * layer.GetFeatureCount()
    i: int = 0

    for feature in layer:
        feature_list[i] = feature.GetGeometryRef().ExportToWkt()
        i += 1

    return feature_list
