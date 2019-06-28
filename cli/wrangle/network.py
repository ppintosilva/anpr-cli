import  click
import  geopandas           as gpd
import  networkx            as nx

from    anprx.preprocessing import network_from_cameras

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
    default = 'svg',
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
        make_plots = figures,
        file_format = figure_format
    )

    if output_format == "pkl":
        nx.write_gpickle(G, output)
    elif output_format == "graphml":
        nx.write_graphml(G, output)
    elif output_format == "shapefile":
        nx.write_shp(G, output)

# @click.command()
# def merge_cameras():
#     """
#     Merge a graph of the road network with the location of the cameras such that
#     each camera is mapped onto one edge of the graph.
#     """
#     pass

# @click.command()
# def all_camera_pairs():
#     """
#     Compute the k-shortest routes and the total driving distance for all valid
#     combinations of cameras pairs : (origin, destination).
#     """
#     pass
#
# @click.command()
# def raw_anpr():
#     """
#     Wrangle a csv file containing raw ANPR data:
#         - Filter bad number plates
#         - Remove all sightings with confidence < THRESHOLD
#         - Sort by Timestamp
#         - Anonymise (if necessary)
#         - Identify trips
#         - Outlier detection: duplicates, vehicles travelling too fast
#     """
#     pass
