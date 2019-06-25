"""anpr-cli: A CLI for pre-processing and analysing batches of ANPR data."""

import anprx
import click

# Main group
@click.group()
def cli():
    """A CLI for wrangling and analysing batches of ANPR data."""
    pass

@cli.group(chain = True)
def wrangle():
    """Pre-process and wrangle raw data."""
    pass

@cli.group()
def compute():
    """Aggregate wrangled data by field and compute ."""
    pass

@wrangle.command()
def cameras():
    """
    Wrangle a csv file containing the location, identifiers and other
    raw information about ANPR cameras.
    """
    pass

@wrangle.command()
def expert_camera_pairs():
    """
    Wrangle a csv file containing information about the pairs of cameras used by
    traffic operators, and other experts, to reason about the flow of traffic.
    """
    pass

@wrangle.command()
def network():
    """
    Obtain the road network graph for a set of ANPR cameras from OpenStreetMap.
    """
    pass

@wrangle.command()
def merge_cameras_network():
    """
    Merge a graph of the road network with the location of the cameras such that
    each camera is mapped onto one edge of the graph.
    """
    pass

@wrangle.command()
def all_camera_pairs():
    """
    Compute the k-shortest routes and the total driving distance for all valid
    combinations of cameras pairs : (origin, destination).
    """
    pass

@wrangle.command()
def raw_anpr():
    """
    Wrangle a csv file containing raw ANPR data:
        - Filter bad number plates
        - Remove all sightings with confidence < THRESHOLD
        - Sort by Timestamp
        - Anonymise (if necessary)
        - Identify trips
        - Outlier detection: duplicates, vehicles travelling too fast
    """
    pass


@compute.command()
def flows():
    """Compute flows between camera pairs from wrangled data."""
    pass


@compute.command()
def trip_history():
    """Compute trip history features for each vehicle."""
    pass
