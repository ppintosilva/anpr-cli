import click
from anprx import preprocessing

import numpy  as np
import pandas as pd

@click.argument(
    'output',
    type = click.File('wb'),
)
@click.argument(
    'input-csv',
    type=click.File('rb')
)
@click.option(
    '--output-format',
    type=click.Choice(['geojson', 'csv']),
    default = 'geojson',
    required = False,
    help = "Format of the output file containing the wrangled cameras dataset"
)
@click.option(
    '--names',
    type = str,
    default = 'id,lat,lon,name,description,is_commissioned,type',
    required = False,
    help = "Role of each of the columns in the input csv file"
)
@click.option(
    '--header/--no-header',
    default = True,
    required = False,
    help = "Whether the first line of the csv file should be ignored or not."
)
@click.command()
def cameras(input_csv, output, output_format, names, header):
    """
    Wrangle a raw dataset of ANPR cameras.

    A raw cameras dataset contains essential information about a set of ANPR
    cameras: their ids and coordinates. In addition, it usually contains other
    important information about the location and orientation of the cameras,
    but that is available in unstructured format. This command retrieves this
    information from text-based descriptions of the cameras, and assigns it to
    new columns. Furthermore, cameras that may not be relevant are filtered
    out: decomissioned cameras, test cameras and cameras located in car parks.
    Use the --names option to specify the role of each column in the input csv
    file. Specify these a comma separated string of values. The following
    values are recognised: id,name,lat,lon,description,is_commissioned.
    Additional columns will be ignored but kept on the resulting dataframe.
    The description columns is used to infer the following attributes:
    direction, is_carpark, address, road_category. Name is used to infer
    whether the camera is a test camera or not. Car park cameras and
    decommissioned cameras are removed.

    Example usage:

    \b
    anpr wrangle cameras \\
        --names "id,name,lat,lon,description,is_commissioned,other_col" \\
        raw_cameras.csv \\
        wrangled_cameras.geojson

    Note that names specifies the new column names of the dataframe by role.
    Any pre-existing column names are ignored.

    If the output format is GeoJSON (default), the cameras coordinates are
    projected into UTM coordinates. Working with UTM coordinates is useful
    further down on the processing pipeline when cameras are mapped onto the
    road network (see command wrangle merge-cameras).
    """
    col_names = names.split(',')

    has_description = ('description' in col_names)

    infer_direction_col       = 'description' if has_description else False
    drop_car_park             = 'description' if has_description else False
    extract_address           = 'description' if has_description else False
    extract_road_category     = 'description' if has_description else False
    drop_is_test              = 'name' if ('name' in col_names) else False
    drop_is_not_commissioned  = ('is_commissioned' in col_names)

    click.echo(col_names)

    cameras = pd.read_csv(
        filepath_or_buffer = input_csv,
        sep    = ',',
        names  = col_names,
        header = 1 if header else None,
        dtype  = {
            "id": object,
            "name": object,
            "lat": np.float64,
            "lon": np.float64,
            "is_commissioned" : object,
            "description" : object
        }
    )
    click.echo(cameras.head())

    proj_coords = (output_format == "geojson")

    wcameras = preprocessing.wrangle_cameras(
        cameras                   = cameras,
        infer_direction_col       = infer_direction_col,
        drop_car_park             = drop_car_park,
        extract_address           = extract_address,
        extract_road_category     = extract_road_category,
        project_coords            = proj_coords,
        drop_is_test              = drop_is_test,
        drop_is_not_commissioned  = drop_is_not_commissioned
    )
    if proj_coords:
        wcameras.to_file(output, driver='GeoJSON')
    elif output_format == "csv":
        wcameras.to_csv(output, index = False)

    return 0

# @wrangle.command()
# def expert_camera_pairs():
#     """
#     Wrangle a csv file containing information about the pairs of cameras used by
#     traffic operators, and other experts, to reason about the flow of traffic.
#     """
#     pass
