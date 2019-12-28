from osgeo import ogr
import numpy as np
import math
from typing import List
import gdalhelpers.checks.geometry_checks as geometry_checks
import gdalhelpers.checks.values_checks as values_checks
import gdalhelpers.helpers.math_helpers as math_helpers
from gdalhelpers.classes.DEM import DEM


def line_segmentize(line: ogr.Geometry,
                    segment_length: float = None,
                    allowed_input_types: List[int] = None) -> ogr.Geometry:

    if allowed_input_types is None:
        allowed_input_types = [ogr.wkbLineString, ogr.wkbLineString25D, ogr.wkbLineStringM, ogr.wkbLineStringZM]

    geometry_checks.check_variable_expected_geometry(line, "line", allowed_input_types)

    if segment_length is not None:
        values_checks.check_value_is_zero_or_positive(segment_length, "segment_length")
        # offset distance by the smallest possible value change towards higher value,
        # otherwise Segmetize tries to use smaller value and not the actual distance as limit
        segment_length = np.nextafter(float(segment_length), np.Inf)

        line.Segmentize(segment_length)

    return line


def line_create_3_points(p1: ogr.Geometry,
                         p2: ogr.Geometry,
                         p3: ogr.Geometry,
                         segment_length: float = None,
                         allowed_input_types: List[int] = None) -> ogr.Geometry:

    if allowed_input_types is None:
        allowed_input_types = [ogr.wkbPoint, ogr.wkbPoint25D, ogr.wkbPointM, ogr.wkbPointZM]

    geometry_checks.check_variable_expected_geometry(p1, "p1", allowed_input_types)
    geometry_checks.check_variable_expected_geometry(p2, "p2", allowed_input_types)
    geometry_checks.check_variable_expected_geometry(p3, "p3", allowed_input_types)

    line = ogr.Geometry(ogr.wkbLineString)

    line.SetPoint(0, p1.GetX(), p1.GetY())
    line.SetPoint(1, p2.GetX(), p2.GetY())
    line.SetPoint(2, p3.GetX(), p3.GetY())

    line = line_segmentize(line, segment_length)

    return line


def line_create_2_points(p1: ogr.Geometry,
                         p2: ogr.Geometry,
                         segment_length: float = None,
                         allowed_input_types: List[int] = None) -> ogr.Geometry:

    if allowed_input_types is None:
        allowed_input_types = [ogr.wkbPoint, ogr.wkbPoint25D, ogr.wkbPointM, ogr.wkbPointZM]

    geometry_checks.check_variable_expected_geometry(p1, "p1", allowed_input_types)
    geometry_checks.check_variable_expected_geometry(p2, "p2", allowed_input_types)

    line = ogr.Geometry(ogr.wkbLineString)

    line.SetPoint(0, p1.GetX(), p1.GetY())
    line.SetPoint(1, p2.GetX(), p2.GetY())

    line = line_segmentize(line, segment_length)

    return line


def line_assign_z_to_vertexes(line_2d: ogr.Geometry,
                              dem: DEM,
                              allowed_input_types: List[int] = None) -> ogr.Geometry:

    if allowed_input_types is None:
        allowed_input_types = [ogr.wkbLineString, ogr.wkbLineString25D, ogr.wkbLineStringM, ogr.wkbLineStringZM]

    geometry_checks.check_variable_expected_geometry(line_2d, "line_2d", allowed_input_types)

    line_3d = ogr.Geometry(ogr.wkbLineStringZM)

    for i in range(0, line_2d.GetPointCount()):
        pt = line_2d.GetPoint(i)
        z_value = dem.get_value_bilinear(pt[0], pt[1])

        if z_value != dem.get_nodata_value():
            line_3d.AddPoint(pt[0], pt[1], z_value)

    return line_3d


def angle_points(p1: ogr.Geometry,
                 p2: ogr.Geometry,
                 allowed_input_types: List[int] = None) -> float:

    if allowed_input_types is None:
        allowed_input_types = [ogr.wkbPoint, ogr.wkbPoint25D, ogr.wkbPointM, ogr.wkbPointZM]

    geometry_checks.check_variable_expected_geometry(p1, "p1", allowed_input_types)
    geometry_checks.check_variable_expected_geometry(p2, "p2", allowed_input_types)

    return math_helpers.horizontal_angle(p1.GetX(), p1.GetY(), p2.GetX(), p2.GetY())


def point_at_angle_distance(p: ogr.Geometry,
                            distance: float,
                            theta: float,
                            allowed_input_types: List[int] = None) -> ogr.Geometry:

    if allowed_input_types is None:
        allowed_input_types = [ogr.wkbPoint, ogr.wkbPoint25D, ogr.wkbPointM, ogr.wkbPointZM]

    geometry_checks.check_variable_expected_geometry(p, "p", allowed_input_types)
    values_checks.check_value_is_zero_or_positive(distance, "distance")
    values_checks.check_return_value_is_angle(theta, "theta")

    p_res = ogr.Geometry(ogr.wkbPoint)

    p_res.AddPoint_2D(p.GetX() - distance * math.cos(theta),
                      p.GetY() - distance * math.sin(theta))

    return p_res
