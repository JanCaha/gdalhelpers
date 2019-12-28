from osgeo import ogr
import warnings


def check_is_ogr_datasource(variable, variable_name: str) -> None:
    """
    Checks if variable is `ogr.DataSource` type, otherwise raises `TypeError`.

    :param variable: variable to check
    :param variable_name: string. Variable name for error message.
    :return: nothing
    """

    if not isinstance(variable, ogr.DataSource):
        raise TypeError("`{0}` must be of class `ogr.DataSource`. `{0}` is of type `{1}`."
                        .format(variable_name, type(variable).__name__))


def warn_shapefile_output(ds: ogr.DataSource, ds_name: str) -> None:
    """
    Prints `warning` if provided `ogr.DataSource` (`ds`) is `ESRI Shapefile`.

    :param ds: ogr.DataSource to check.
    :param ds_name: string. Variable name for error message.
    :return: nothing
    """

    if ds.GetDriver().GetDescription() == "ESRI Shapefile":
        warnings.warn(
            "It is not recommended to use `ESRI Shapefile` as output type (for variable `{0}`). "
            "Geopackage (GPKG) is the recomended file output.".format(ds_name),
            UserWarning
        )
