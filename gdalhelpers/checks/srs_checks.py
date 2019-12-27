from osgeo import osr


def check_srs_projected(srs: osr.SpatialReference, srs_name: str):
    if srs.IsProjected() != 1:
        raise ValueError("`{0}` Spatial Reference needs to be projected. "
                         "The definition of current SRS is not projected: \n `{1}`"
                         .format(srs_name, srs.ExportToProj4()))


def check_srs_are_same(srs1: osr.SpatialReference, srs2: osr.SpatialReference):
    if srs1.IsSame(srs2) != 1:
        raise ValueError("Spatial Reference of both layers `{0}`, `{1}` needs to be equal.")