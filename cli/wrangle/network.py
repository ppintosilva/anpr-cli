import click

@click.command()
def network():
    """
    Obtain the road network graph for a set of ANPR cameras from OpenStreetMap.
    """
    pass

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
