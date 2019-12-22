from osgeo import ogr
from typing import Union, List


def check_is_layer(variable, variable_name: str) -> None:
    if not isinstance(variable, ogr.Layer):
        raise TypeError("`{0}` must be of class `ogr.Layer`. `{0}` is of type `{1}`."
                        .format(variable_name, type(variable).__name__))


# https://gis.stackexchange.com/questions/239289/gdal-ogr-python-getgeomtype-method-returns-integer-what-is-the-matching-geo
def check_is_layer_geometry_type(variable: ogr.Layer,
                                 variable_name: str,
                                 expected_geom_type: Union[int, List[int]]) -> None:

    geometry_name = ogr.GeometryTypeToName(variable.GetGeomType())

    check: bool = False
    expected_geometry_name: str

    if isinstance(expected_geom_type, list):

        for egt in expected_geom_type:
            if variable.GetGeomType() == egt:
                check = True

        expected_geometry_name = [ogr.GeometryTypeToName(x) for x in expected_geom_type]
        expected_geometry_name = ", ".join(expected_geometry_name)
    else:
        expected_geometry_name = ogr.GeometryTypeToName(expected_geom_type)
        check = (variable.GetGeomType() == expected_geom_type)

    if not check:
        raise TypeError("`{0}` must be of geometry type/types `{1}`, but it is `{2}`.".
                        format(variable_name, expected_geometry_name, geometry_name))


def does_field_exist(layer: ogr.Layer, field_name: Union[str, None]) -> bool:

    if field_name is None:
        return False

    field_index = layer.GetLayerDefn().GetFieldIndex(field_name)

    if field_index < 0:
        return False
    else:
        return True


def is_field_of_type(layer: ogr.Layer, field_name: str, field_type: int) -> bool:

    if field_type == get_field_type(layer, field_name):
        return True
    else:
        return False


def get_field_type(layer: ogr.Layer, field_name: str) -> str:

    field_index = layer.GetLayerDefn().GetFieldIndex(field_name)

    return layer.GetLayerDefn().GetFieldDefn(field_index).GetType()


def check_number_of_features(layer: ogr.Layer,
                             variable_name: str,
                             number: int):

    if not layer.GetFeatureCount() == 1:
        raise AttributeError("Layer `{0}` must contain only `{1}` feature/s. Currently there are `{2}` features.".
                             format(variable_name, number, layer.GetFeatureCount()))
