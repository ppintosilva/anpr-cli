import click

from anprx       import preprocessing
from anprx.utils import log

import numpy     as np
import pandas    as pd
import geopandas as gpd
import logging   as lg

@click.argument(
    'output-geojson',
    type = str,
)
@click.argument(
    'input-csv',
    type=click.File('rb')
)
@click.option(
    '--names',
    type = str,
    default = None,
    required = False,
    help = "Names of columns in the input csv file"
)
@click.option(
    '--distance',
    type = float,
    default = 100.0,
    required = False,
    help = ("Merge cameras within distance meters, that have the "
            "same address and direction")
)
@click.option(
    '--skip-lines',
    default = 0,
    show_default = True,
    type = int,
    required = False,
    help = "Number of lines to skip at the start of the file."
)
@click.option(
    '--merge-cameras',
    default = True,
    show_default = True,
    type = bool,
    required = False,
    help ="Whether to merge nearby cameras with the same address and direction."
)
@click.command()
def cameras(input_csv, output_geojson,
            names, skip_lines,
            distance, merge_cameras):
    """
    Wrangle a raw dataset of ANPR cameras.

    A raw cameras dataset contains essential information about a set of ANPR
    cameras: their ids and coordinates. In addition, it usually contains other
    important information about the location and orientation of the cameras,
    but that is available in unstructured format. This command retrieves this
    information from text-based descriptions of the cameras, and assigns it to
    new columns. Furthermore, cameras that may not be relevant are filtered
    out: decomissioned cameras, test cameras and cameras located in car parks.

    By default, column names are retrieved from the first line of the file.
    The following column names are mandatory: 'id', 'lat' and 'lon'. Either
    edit the column names directly in the input csv file or specify these as a
    comma separated string of values via the --names option. Additional
    recognised column names are: 'name', 'description' and 'is_commissioned'.
    Any additional columns will be ignored but kept on the resulting dataframe.
    The 'description' column is used to infer the following attributes:
    direction, is_carpark, address, road_category. The 'name' column is used to
    infer whether the camera is a test camera or not. Car park cameras and
    decommissioned cameras are removed.

    Example usage:

    \b
        (1) - Using header from file:

    \b
        anpr wrangle cameras raw_cameras.csv wrangled_cameras.geojson

    \b
        (2) - Specyfing column names via the --names option:

    \b
        anpr wrangle cameras \\
            --names "id,name,lat,lon,description,is_commissioned,other_col" \\
            --skip-lines 1 \\
            raw_cameras.csv \\
            wrangled_cameras.geojson

    The cameras coordinates are projected into UTM coordinates.
    Working with UTM coordinates is useful to merge cameras onto the
    road network (see command wrangle merge-cameras).

    This script uses anprx to wrangle the cameras dataset. For more
    fine-grained control over the behavior of this function please consider
    using the python library: https://github.com/ppintosilva/anprx
    """

    cameras = pd.read_csv(
        filepath_or_buffer = input_csv,
        sep    = ',',
        names  = names.split(',') if names else None,
        header = None if names else 0,
        skiprows = skip_lines,
        dtype  = {
            "id": object,
            "name": object,
            "lat": np.float64,
            "lon": np.float64,
            "is_commissioned" : bool,
            "description" : object
        }
    )

    col_names = names.split(',') if names else cameras.columns.values

    has_name             = ('name' in col_names)
    has_description      = ('description' in col_names)
    has_is_commissioned  = ('is_commissioned' in col_names)

    wcameras = preprocessing.wrangle_cameras(
        cameras               = cameras,
        is_test_col           = "name" if has_name else False,
        is_commissioned_col   = "is_commissioned" if has_is_commissioned else False,
        road_attr_col         = "description" if has_description else False,
        drop_car_park         = True,
        drop_na_direction     = True,
        distance_threshold    = distance,
        sort_by               = 'id',
        merge_cameras         = merge_cameras
    )

    wcameras.to_file(output_geojson, driver='GeoJSON')

    return 0

###

@click.argument(
    'output-nodes-geojson',
    type = str,
)
@click.argument(
    'input-cameras-geojson',
    type=click.File('rb')
)
@click.argument(
    'input-nodes-csv',
    type=click.File('rb')
)
@click.option(
    '--names',
    type = str,
    default = None,
    required = False,
    help = "Names of columns in the input csv file"
)
@click.option(
    '--distance',
    type = float,
    default = 100.0,
    required = False,
    help = ("Map nodes to cameras within distance meters, that have the "
            "same address and direction")
)
@click.option(
    '--skip-lines',
    default = 0,
    show_default = True,
    type = int,
    required = False,
    help = "Number of lines to skip at the start of the file."
)
@click.command()
def nodes(input_nodes_csv,
          input_cameras_geojson,
          output_nodes_geojson,
          names,
          skip_lines,
          distance
):
    """
    Wrangle a raw dataset of Nodes.
    """

    raw_nodes = pd.read_csv(
        filepath_or_buffer = input_nodes_csv,
        sep    = ',',
        names  = names.split(',') if names else None,
        header = None if names else 0,
        skiprows = skip_lines,
        dtype  = {
            "id": object,
            "name": object,
            "lat": np.float64,
            "lon": np.float64,
            "is_commissioned" : bool,
            "description" : object
        }
    )

    col_names = names.split(',') if names else raw_nodes.columns.values

    has_name             = ('name' in col_names)
    has_description      = ('description' in col_names)
    has_is_commissioned  = ('is_commissioned' in col_names)

    cameras = gpd.GeoDataFrame.from_file(input_cameras_geojson)

    wnodes = preprocessing.map_nodes_cameras(
        nodes                 = raw_nodes,
        cameras               = cameras,
        is_test_col           = "name" if has_name else False,
        is_commissioned_col   = "is_commissioned" if has_is_commissioned else False,
        road_attr_col         = "description" if has_description else False,
        drop_car_park         = True,
        drop_na_direction     = True,
        distance_threshold    = distance,
        sort_by               = 'id'
    )

    wnodes.to_file(output_nodes_geojson, driver='GeoJSON')

    return 0

@click.argument(
    'output-pairs-csv',
    type = str,
)
@click.argument(
    'input-nodes-geojson',
    type=click.File('rb')
)
@click.argument(
    'input-links-csv',
    type=click.File('rb')
)
@click.option(
    '--names',
    type = str,
    default = None,
    required = False,
    help = "Names of columns in the input csv file"
)
@click.option(
    '--skip-lines',
    default = 0,
    show_default = True,
    type = int,
    required = False,
    help = "Number of lines to skip at the start of the file."
)
@click.command()
def expert_pairs(
    input_links_csv,
    input_nodes_geojson,
    output_pairs_csv,
    names,
    skip_lines
):
    """
    Merge a file with

    Wrangle a csv file containing information about the pairs of cameras used by
    traffic operators, and other experts, to reason about the flow of traffic.
    """

    nodes = gpd.GeoDataFrame.from_file(input_nodes_geojson)
    nodes = nodes[['id', 'camera']]

    links = pd.read_csv(
        filepath_or_buffer = input_links_csv,
        sep    = ',',
        names  = names.split(',') if names else None,
        header = None if names else 0,
        skiprows = skip_lines,
        dtype  = {
            "id": object,
            "description" : object,
            "start_node": object,
            "end_node": object
        }
    )

    links_start = pd.merge(
        links[['id', 'description', 'start_node']],
        nodes,
        how = 'left',
        left_on = 'start_node',
        right_on = 'id',
        suffixes = ('_link', '_node'))

    links_end = pd.merge(
        links[['id', 'end_node']],
        nodes,
        how = 'left',
        left_on = 'end_node',
        right_on = 'id',
        suffixes = ('_link', '_node'))

    pairs = pd.merge(
        links_start, links_end, 'inner',
        on = 'id_link',
        suffixes = ('_start', '_end'))

    if len(pairs) != len(links):
        log(("Length of resulting expert camera pairs (n = {}) "
             "is different than input links file (n = {})")\
                .format(len(pairs), len(links)),
            level = lg.WARNING)

    pairs = pairs[['id_link', 'description',
                   'camera_start', 'camera_end']]
    pairs = pairs.rename(columns = {
        'id_link' : 'id',
        'camera_start'   : 'start_camera',
        'camera_end'     : 'end_camera'
    })

    log(("Determined expert camera pairs from wrangled nodes and links "
         "input files and saved output to {}")\
            .format(output_pairs_csv),
        level = lg.INFO)

    pairs[['id', 'start_camera', 'end_camera', 'description']]\
        .to_csv(output_pairs_csv, index = False)
