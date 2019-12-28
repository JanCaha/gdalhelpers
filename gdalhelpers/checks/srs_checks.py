from osgeo import osr
from typing import Any


def check_srs(srs: Any, srs_name: str):
    """
    Checks if `srs` is `osr.SpatialReference`, raises `ValueError` otherwise.

    :param srs: Any. Value to check.
    :param srs_name: string. Variable name for error message.
    :return: nothing
    """
    if not isinstance(srs, osr.SpatialReference):
        raise ValueError("`{0}` is not of type `osr.SpatialReference`. It is: `{1}`."
                         .format(srs_name, type(srs).__name__))


def check_srs_projected(srs: osr.SpatialReference, srs_name: str):
    """
    Checks if `srs` (`osr.SpatialReference`) is projected, raises `ValueError` otherwise.

    :param srs: osr.SpatialReference to check.
    :param srs_name: string. Variable name for error message.
    :return: nothing
    """

    check_srs(srs, srs_name)

    if srs.IsProjected() != 1:
        raise ValueError("`{0}` Spatial Reference needs to be projected. "
                         "The definition of current SRS is not projected: \n `{1}`"
                         .format(srs_name, srs.ExportToProj4()))


def check_srs_are_same(srs1: osr.SpatialReference, srs1_name: str,
                       srs2: osr.SpatialReference, srs2_name: str):
    """
    Checks if two provided `osr.SpatialReference` are the same.

    :param srs1: osr.SpatialReference
    :param srs1_name: string. Variable name for error message.
    :param srs2: osr.SpatialReference
    :param srs2_name: string. Variable name for error message.
    :return: nothing
    """

    check_srs(srs1, srs1_name)
    check_srs(srs2, srs2_name)

    if srs1.IsSame(srs2) != 1:
        raise ValueError("Spatial Reference of both layers `{0}`, `{1}` needs to be equal.")