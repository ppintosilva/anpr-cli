import  click
import  geopandas           as gpd
import  networkx            as nx

from    anprx.preprocessing import network_from_cameras
from    anprx.preprocessing import merge_cameras_network
from    anprx.preprocessing import camera_pairs_from_graph

@click.argument(
    'output',
    type = str,
)
@click.argument(
    'input',
    type=click.File('rb')
)
@click.option(
    '--input-format',
    type=click.Choice(['geojson', 'csv']),
    default = 'geojson',
    show_default = True,
    required = False,
    help = "Format of the input file with the wrangled cameras dataset"
)
@click.option(
    '--output-format',
    type=click.Choice(['pkl', 'graphml', 'shapefile']),
    default = 'pkl',
    show_default = True,
    required = False,
    help = "Format of the output file with the (unmerged) network graph"
)
@click.option(
    '--residential',
    is_flag = True,
    show_default = True,
    help = "Retrieve residential and service roads from OpenStreetMap"
)
@click.option(
    '--clean',
    is_flag = True,
    show_default = True,
    help = "Clean intersections in the road graph"
)
@click.option(
    '--clean-tolerance',
    default = 30,
    show_default = True,
    required = False,
    help = "Tolerance parameter when --clean flag is activated."
)
@click.option(
    '--figures/--no-figures',
    default = True,
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
@click.command()
def network(
    input, output,
    input_format, output_format,
    residential,
    clean, clean_tolerance,
    figures, figure_format
):
    """
    Obtain the road network graph from OpenStreetMap.

    Obtain the road network graph for a set of ANPR cameras from OpenStreetMap.
    """

    if input_format == "geojson":
        cameras = gpd.GeoDataFrame.from_file(input)
    elif input_format == "csv":
        cameras = pd.read_csv(
            filepath_or_buffer = input,
            sep    = ',',
            header = 0,
            dtype  = {
                "id": object,
                "name": object,
                "lat": np.float64,
                "lon": np.float64,
                "is_commissioned" : bool,
                "description" : object
            }
        )

    G = network_from_cameras(
        cameras,
        filter_residential = not residential,
        clean_intersections = clean,
        tolerance = clean_tolerance,
        plot = figures,
        file_format = figure_format,
        fig_height = 14
    )

    if output_format == "pkl":
        nx.write_gpickle(G, output)
    elif output_format == "graphml":
        nx.write_graphml(G, output)
    elif output_format == "shapefile":
        nx.write_shp(G, output)

    return 0

#-------------------------------------------------------------------------------
@click.argument(
    'output',
    type = str,
)
@click.argument(
    'input_network',
    type=click.File('rb')
)
@click.argument(
    'input_cameras',
    type=click.File('rb')
)
@click.option(
    '--cameras-format',
    type=click.Choice(['geojson', 'csv']),
    default = 'geojson',
    show_default = True,
    required = False,
    help = "Format of the input file with the wrangled cameras dataset"
)
@click.option(
    '--network-format',
    type=click.Choice(['pkl', 'graphml', 'shapefile']),
    default = 'pkl',
    show_default = True,
    required = False,
    help = "Format of the input file with the (unmerged) network graph"
)
@click.option(
    '--output-format',
    type=click.Choice(['pkl', 'graphml', 'shapefile']),
    default = 'pkl',
    show_default = True,
    required = False,
    help = "Format of the output file with the (unmerged) network graph"
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
    default = True,
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
@click.command()
def merge(
    input_cameras,
    input_network,
    output,
    cameras_format,
    network_format,
    output_format,
    passes,
    figures,
    figure_format
):
    """
    Merge a set of cameras with a road network graph.
    """

    if cameras_format == "geojson":
        cameras = gpd.GeoDataFrame.from_file(input_cameras)
    elif cameras_format == "csv":
        cameras = pd.read_csv(
            filepath_or_buffer = input_cameras,
            sep    = ',',
            header = 0,
            dtype  = {
                "id": object,
                "name": object,
                "lat": np.float64,
                "lon": np.float64,
                "is_commissioned" : bool,
                "description" : object
            }
        )

    if network_format == "pkl":
        G = nx.read_gpickle(input_network)
    elif network_format == "graphml":
        G = nx.read_graphml(input_network)
    elif network_format == "shapefile":
        G = nx.read_shp(input_network)

    G = merge_cameras_network(
        G,
        cameras,
        passes = passes,
        plot = figures,
        figure_format = figure_format,
        fig_height = 14
    )

    if output_format == "pkl":
        nx.write_gpickle(G, output)
    elif output_format == "graphml":
        nx.write_graphml(G, output)
    elif output_format == "shapefile":
        nx.write_shp(G, output)

    return 0


@click.argument(
    'output',
    type = str,
)
@click.argument(
    'input_network',
    type=click.File('rb')
)
@click.option(
    '--network-format',
    type=click.Choice(['pkl', 'graphml', 'shapefile']),
    default = 'pkl',
    show_default = True,
    required = False,
    help = "Format of the input file with merged network graph"
)
@click.command()
def camera_pairs(input_network, output, network_format):
    """
    Compute valid camera pairs and their distance.

    Compute the shortest route and the total driving distance for all valid
    combinations of cameras pairs : (origin, destination).
    """

    if network_format == "pkl":
        G = nx.read_gpickle(input_network)
    elif network_format == "graphml":
        G = nx.read_graphml(input_network)
    elif network_format == "shapefile":
        G = nx.read_shp(input_network)

    pairs = camera_pairs_from_graph(G)

    pairs.to_csv(output, index = False)

    return 0
