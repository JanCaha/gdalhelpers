from osgeo import ogr
from typing import Union, List


# https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html
# TODO fix using names to codes
def check_variable_geometry(geometry: ogr.Geometry,
                            variable_name: str,
                            expected_geometry_type: Union[int, List[int]]) -> None:
    """
    Checks if `geometry` (`ogr.Geometry`) is of expected type or types, raises `TypeError` if not.

    :param geometry: ogr.Geometry.
    :param variable_name: string. Variable name for error message.
    :param expected_geometry_type: either int or list of ints. Only values provided by ogr.wkbPoint etc. makes sense.
    Can be constructed as `expected_geometry_type=ogr.wkbPoint` or
    `[expected_geometry_type=ogr.wkbPoint, ogr.wkbPoint25D, ogr.wkbPointZM ]`.
    :return: nothing
    """

    if not isinstance(geometry, ogr.Geometry):
        raise TypeError("`{0}` must be of class `ogr.Geometry`. `{0}` is of type `{1}`.".
                        format(variable_name, type(geometry).__name__))

    geometry_name = ogr.GeometryTypeToName(geometry.GetGeometryType())

    check: bool = False
    expected_geometry_name: str

    if isinstance(expected_geometry_type, list):

        for egt in expected_geometry_type:
            if ogr.GeometryTypeToName(geometry.GetGeometryType()) == ogr.GeometryTypeToName(egt):
                check = True

        expected_geometry_name = [ogr.GeometryTypeToName(x) for x in expected_geometry_type]
        expected_geometry_name = ", ".join(expected_geometry_name)
    else:
        expected_geometry_name = ogr.GeometryTypeToName(expected_geometry_type)
        check = (ogr.GeometryTypeToName(geometry.GetGeometryType()) in ogr.GeometryTypeToName(expected_geometry_type))

    if not check:
        raise TypeError("`{0}` must be of geometry type/types `{1}`, but it is `{2}`.".
                        format(variable_name, expected_geometry_name, geometry_name))


def check_is_wkt_geometry(string: str, variable_name: str) -> None:
    """
    Checks if the provided `string` is a valid WKT. Raises `TypeError` otherwise.

    :param string: string. To check if it is WKT.
    :param variable_name: string. Variable name for error message.
    :return:
    """
    if ogr.CreateGeometryFromWkt(string) is None:
        raise TypeError("`{0}` is not a valid WKT. `{1}` cannot be loaded as geometry.".format(variable_name, string))
