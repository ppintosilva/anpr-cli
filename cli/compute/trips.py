import click

from anprx.trips import transform_anpr
from anprx.trips import calculate_avspeed
from anprx.trips import trip_identification
from anprx.utils import log

import os
import numpy     as np
import pandas    as pd
import geopandas as gpd
import logging   as lg


@click.argument(
    'output-pkl',
    type=str
)
@click.argument(
    'input-pairs-geojson',
    type=str
)
@click.argument(
    'input-anpr-pkl',
    type=str
)
@click.option(
    '--speed-threshold',
    default = 3.0,
    type = float,
    show_default = True,
    required = False,
    help = "Trip identification threshold."
)
@click.option(
    '--duplicate-threshold',
    default = 300.0,
    type = float,
    show_default = True,
    required = False,
    help = ("Two vehicle observations at the same camera under this threshold "
            "are considered duplicates.")
)
@click.option(
    '--max-speed',
    default = 120.0,
    type = float,
    show_default = True,
    required = False,
    help = ("Observations that register a speed over this value are labelled "
            "as 'unfeasible' and removed.")
)
@click.command()
def trips(
    output_pkl,
    input_pairs_geojson,
    input_anpr_pkl,
    speed_threshold,
    duplicate_threshold,
    max_speed
):
    """
    Identify trips for a batch of wrangled anpr data.
    """
    log(("Reading input pkl file with wrangled anpr data of size {:,.2f} MB.")\
            .format(os.stat(input_anpr_pkl).st_size/1e6),
        level = lg.INFO)

    anpr = pd.read_pickle(input_anpr_pkl)

    camera_pairs = gpd.GeoDataFrame.from_file(input_pairs_geojson)

    click.echo("Running trip identification. This may take a while...")

    trips = trip_identification(
        anpr, camera_pairs,
        speed_threshold = speed_threshold,
        duplicate_threshold = duplicate_threshold,
        maximum_av_speed = max_speed
    )

    trips.to_pickle(output_pkl)

    return 0


@click.argument(
    'output-pkl',
    type=str
)
@click.argument(
    'input-pairs-geojson',
    type=str
)
@click.argument(
    'input-anpr-pkl',
    type=str
)
@click.command()
def avspeed(
    output_pkl,
    input_pairs_geojson,
    input_anpr_pkl
):
    """
    Transform wrangled anpr data and compute vehicle
    avspeed using shortest path distance.
    """
    log(("Reading input pkl file with wrangled anpr data of size {:,.2f} MB.")\
            .format(os.stat(input_anpr_pkl).st_size/1e6),
        level = lg.INFO)

    anpr = pd.read_pickle(input_anpr_pkl)

    camera_pairs = gpd.GeoDataFrame.from_file(input_pairs_geojson)

    t_anpr = transform_anpr(anpr)

    t_anpr = calculate_avspeed(t_anpr, camera_pairs)

    t_anpr.to_pickle(output_pkl)

    return 0
