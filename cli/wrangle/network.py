import  os
import  click
import  geopandas           as gpd
import  osmnx               as ox
import  networkx            as nx
import  pathlib

from    anprx.preprocessing import network_from_cameras
from    anprx.preprocessing import merge_cameras_network
from    anprx.preprocessing import camera_pairs_from_graph
from    anprx.preprocessing import gdfs_from_network
from    anprx.nominatim     import get_amenities

@click.argument(
    'output-pkl',
    type = str,
)
@click.argument(
    'input-geojson',
    type=click.File('rb')
)
@click.option(
    '--road-type',
    type=click.Choice(['all', 'primary', 'arterial'], case_sensitive=False),
    default = 'primary',
    show_default = True,
    help = "Retrieve all or a subset of all roads from OpenStreetMap"
)
@click.option(
    '--clean',
    is_flag = True,
    show_default = True,
    help = "Clean intersections in the road graph"
)
@click.option(
    '--clean-tolerance',
    default = 20,
    show_default = True,
    required = False,
    help = "Tolerance parameter when --clean flag is activated."
)
@click.option(
    '--figures/--no-figures',
    default = False,
    show_default = True,
    help = "Make graph plots and save them to app_folder"
)
@click.option(
    '--figure-format',
    default = 'png',
    show_default = True,
    required = False,
    help = "Format of output figures"
)
@click.option(
    '--dpi',
    default = 300,
    show_default = True,
    required = False,
    help = "Dpi of images"
)
@click.option(
    '--fig-height',
    default = 14,
    show_default = True,
    required = False,
    help = "Height of each figure (width is computed accordingly)"
)
@click.option(
    '--subdir',
    default = "cameras/unmerged",
    show_default = True,
    required = False,
    help = ("Where to save close-up camera figures within the working "
            "directory's image folder")
)
@click.command()
def network(
    input_geojson, output_pkl,
    road_type,
    clean, clean_tolerance,
    figures, figure_format,
    dpi, fig_height, subdir
):
    """
    Obtain the road network graph from OpenStreetMap.
    """

    cameras = gpd.GeoDataFrame.from_file(input_geojson)

    G = network_from_cameras(
        cameras,
        road_type = road_type,
        clean_intersections = clean,
        tolerance = clean_tolerance,
        plot = figures,
        file_format = figure_format,
        fig_height = fig_height,
        dpi = dpi,
        subdir = subdir
    )

    nx.write_gpickle(G, output_pkl)

    return 0

#-------------------------------------------------------------------------------
@click.argument(
    'output_pkl',
    type = str,
)
@click.argument(
    'input_network_pkl',
    type=click.File('rb')
)
@click.argument(
    'input_cameras_geojson',
    type=click.File('rb')
)
@click.option(
    '--passes',
    default = 3,
    show_default = True,
    required = False,
    help = "Number of passes."
)
@click.option(
    '--figures/--no-figures',
    default = False,
    show_default = True,
    help = "Make graph plots and save them to app_folder"
)
@click.option(
    '--figure-format',
    default = 'png',
    show_default = True,
    required = False,
    help = "Format of output figures"
)
@click.option(
    '--dpi',
    default = 300,
    show_default = True,
    required = False,
    help = "Dpi of images"
)
@click.option(
    '--camera-range',
    default = 50.0,
    show_default = True,
    required = False,
    help = "Camera range, in meters."
)
@click.option(
    '--fig-height',
    default = 14,
    show_default = True,
    required = False,
    help = "Height of each figure (width is computed accordingly)"
)
@click.option(
    '--subdir',
    default = "cameras/merged",
    show_default = True,
    required = False,
    help = ("Where to save close-up camera figures within the working "
            "directory's image folder")
)
@click.command()
def merge(
    input_cameras_geojson,
    input_network_pkl,
    output_pkl,
    passes, camera_range,
    figures, figure_format,
    dpi, fig_height, subdir
):
    """
    Merge a set of cameras with a road network graph.
    """

    cameras = gpd.GeoDataFrame.from_file(input_cameras_geojson)

    G = nx.read_gpickle(input_network_pkl)

    G = merge_cameras_network(
        G,
        cameras,
        passes = passes,
        camera_range = camera_range,
        plot = figures,
        figure_format = figure_format,
        fig_height = fig_height,
        dpi = dpi,
        subdir = subdir
    )

    nx.write_gpickle(G, output_pkl)

    return 0


@click.argument(
    'output-geojson',
    type = str,
)
@click.argument(
    'input-pkl',
    type=click.File('rb')
)
@click.command()
def camera_pairs(input_pkl, output_geojson):
    """
    Compute valid camera pairs and their distance.

    Compute the shortest route and the total driving distance for all valid
    combinations of cameras pairs : (origin, destination).
    """

    G = nx.read_gpickle(input_pkl)

    pairs = camera_pairs_from_graph(G)

    pairs.to_file(output_geojson, driver='GeoJSON')

    return 0


@click.argument(
    'output-geojson',
    type = str,
)
@click.argument(
    'input-geojson',
    type=click.File('rb')
)
@click.command()
def amenities(input_geojson, output_geojson):
    """
    Get amenities within a geographical polygon.
    """

    gdf = gpd.GeoDataFrame.from_file(input_geojson)

    amenities = get_amenities(gdf.iloc[0].geometry)

    amenities.to_file(output_geojson, driver='GeoJSON')

    return 0
