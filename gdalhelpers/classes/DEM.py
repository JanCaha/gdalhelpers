import gdal
from gdal import osr, ogr
from typing import List
from numpy import floor, array
import os
import math
import numbers
import warnings
import gdalhelpers.helpers.math_helpers as math_helpers
from gdalhelpers.checks import geometry_checks


class DEM:

    __band_number = 1
    __gdal_nodata_default = -3.4028e+38

    def __init__(self, path: str, epsg: int = None):

        if not os.path.isfile(path):
            raise IOError("File at specified path `{0}` does not exist.".format(path))

        self.path = path
        self.ds = gdal.Open(self.path)

        if self.ds.RasterCount > 1:
            raise ValueError("DEM is only allowed to have one band. The raster has `{}` bands."
                             .format(self.ds.RasterCount))

        projection = self.ds.GetProjection()
        projection = osr.SpatialReference(wkt=projection)

        if projection.ExportToWkt() == "" and epsg is None:
            raise ValueError("Cannot obtain projection from raster `{0}` and epsg argument is not set."
                             .format(path))

        if projection != "" and epsg is not None:
            epsg = None
            warnings.warn(
                "Raster has specified projection and epsg is set. Using projection from raster!",
                SyntaxWarning)

        if epsg is None:

            if projection.IsProjected() != 1:
                raise ValueError("DEM has to be projected, the given projection is not projected: \n `{0}`."
                                 .format(projection.ExportToWkt()))
        else:

            projection = osr.SpatialReference()
            projection.ImportFromEPSG(epsg)

            if projection.IsProjected() != 1:
                raise ValueError("DEM has to be projected, the definition of provided EPSG is not projected: \n `{0}`.".
                                 format(projection.ExportToProj4()))
            else:
                self.ds.SetProjection(projection.ExportToWkt())

        self.gt = self.ds.GetGeoTransform()
        self.nx = self.ds.RasterXSize
        self.ny = self.ds.RasterYSize
        self.no_data = self.ds.GetRasterBand(self.__band_number).GetNoDataValue()
        self.np_array = None

    @classmethod
    def from_gdal_raster(cls, gdal_raster: gdal.Dataset):

        if not isinstance(gdal_raster, gdal.Dataset):
            raise TypeError("`gdal_raster` has to be of type `gdal.Dataset`. "
                            "But it is type `{0}`".format(type(gdal_raster).__name__))

        return cls(path=gdal_raster.GetDescription())

    def __str__(self):
        return "Raster from `{0}` with sizes(`{1}`, `{2}`) using projection `{3}`.".format(self.path,
                                                                                           self.nx,
                                                                                           self.ny,
                                                                                           self.ds.GetProjection())

    def __del__(self):
        self.ds = None
        self.destroy_array()

    def get_min_pixel_size(self) -> float:
        return abs(min(self.gt[1], self.gt[5]))

    def __check_value_is_nodata(self, value: numbers.Number) -> bool:
        return (value < self.__gdal_nodata_default) or math_helpers.is_almost_equal(value, self.no_data)

    def load_array(self) -> None:
        self.np_array = self.ds.GetRasterBand(self.__band_number).ReadAsArray()

    def destroy_array(self) -> None:
        self.np_array = None

    def get_nodata_value(self) -> float:
        return self.no_data

    def get_max_size(self) -> float:
        return max(self.gt[1] * self.nx, self.gt[5] * self.ny)

    def get_diagonal_size(self) -> float:
        size = math.sqrt(math.pow(self.gt[1] * self.nx, 2) + math.pow(self.gt[5] * self.ny, 2))
        return size

    def get_bounding_box(self) -> ogr.Geometry:
        x1 = self.gt[0]
        x2 = self.gt[0] + self.nx * self.gt[1]
        y1 = self.gt[3]
        y2 = self.gt[3] + self.ny * self.gt[5]

        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(min(x1, x2), min(y1, y2))
        ring.AddPoint(max(x1, x2), min(y1, y2))
        ring.AddPoint(max(x1, x2), max(y1, y2))
        ring.AddPoint(min(x1, x2), max(y1, y2))
        ring.AddPoint(min(x1, x2), min(y1, y2))

        bbox = ogr.Geometry(ogr.wkbPolygon)
        bbox.AddGeometry(ring)

        return bbox

    # code from http://gis.stackexchange.com/questions/7611/bilinear-interpolation-of-point-data-on-a-raster-in-python
    def get_value_bilinear(self, px: float, py: float) -> float:
        """Bilinear interpolated point at (px, py) on raster"""

        if not isinstance(px, numbers.Number):
            raise TypeError("px must be number. The variable is of `{}`.".format(type(px)))

        if not isinstance(py, numbers.Number):
            raise TypeError("py must be number. The variable is of `{}`.".format(type(py)))

        if self.np_array is None:
            self.load_array()

        ny, nx = self.np_array.shape
        # Half raster cell widths
        hx = self.gt[1] / 2.0
        hy = self.gt[5] / 2.0
        # Calculate raster lower bound indices from point
        fx = (px - (self.gt[0] + hx)) / self.gt[1]
        fy = (py - (self.gt[3] + hy)) / self.gt[5]

        ix1 = int(floor(fx))
        iy1 = int(floor(fy))
        # Special case where point is on upper bounds
        if fx == float(nx - 1):
            ix1 -= 1
        if fy == float(ny - 1):
            iy1 -= 1
        # Upper bound indices on raster
        ix2 = ix1 + 1
        iy2 = iy1 + 1
        # Test array bounds to ensure point is within raster midpoints
        if (ix1 < 0) or (iy1 < 0) or (ix2 > nx - 1) or (iy2 > ny - 1):
            return self.no_data
        # Calculate differences from point to bounding raster midpoints
        dx1 = px - (self.gt[0] + ix1 * self.gt[1] + hx)
        dy1 = py - (self.gt[3] + iy1 * self.gt[5] + hy)

        dx2 = (self.gt[0] + ix2 * self.gt[1] + hx) - px
        dy2 = (self.gt[3] + iy2 * self.gt[5] + hy) - py
        # Use the differences to weigh the four raster values
        div = self.gt[1] * self.gt[5]

        # if any value is nodata then everything is nodata
        if (self.__check_value_is_nodata(self.np_array[iy1, ix1]) or
                self.__check_value_is_nodata(self.np_array[iy1, ix2]) or
                self.__check_value_is_nodata(self.np_array[iy2, ix1]) or
                self.__check_value_is_nodata(self.np_array[iy2, ix2])):

            return self.no_data

        return ((self.np_array[iy1, ix1] * dx2 * dy2) / div +
                (self.np_array[iy1, ix2] * dx1 * dy2) / div +
                (self.np_array[iy2, ix1] * dx2 * dy1) / div +
                (self.np_array[iy2, ix2] * dx1 * dy1) / div)

    def get_values_bilinear(self, positions: List[List[float]]):

        values: list = [None] * len(positions)
        i: int = 0

        for position in positions:

            if len(position) != 2:
                pos_str = [str(x) for x in position]
                raise ValueError("Every element of list of positions must be of length `2`. "
                                 "Element `{0}`, has `{1}` elements (values: `{2}`)".format(i,
                                                                                            len(position),
                                                                                            ", ".join(pos_str)))
            values[i] = self.get_value_bilinear(position[0], position[1])
            i += 1

        return values

    def get_values_points_bilinear(self, points: List[ogr.Geometry]):

        values: list = [None] * len(points)
        i: int = 0

        for p in points:
            geometry_checks.check_variable_geometry(p, "point[{}]".format(i), [ogr.wkbPoint, ogr.wkbPoint25D,
                                                                               ogr.wkbPointM, ogr.wkbPointZM])

            values[i] = self.get_value_bilinear(p.GetX(), p.GetY())
            i += 1

        return values
