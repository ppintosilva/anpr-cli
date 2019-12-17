import click

from anprx.cameras  import wrangle_raw_anpr
from anprx.utils    import log

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
    'input-csv',
    type=str
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
@click.option(
    '--cameras-geojson',
    default = None,
    type = click.File('rb'),
    required = False,
    help = "Geojson file of wrangled camears."
)
@click.option(
    '--anonymise/--no-anonymise',
    default = True,
    show_default = True,
    help = "Anonymise vehicle license numbers"
)
@click.option(
    '--filter/--no-filter',
    default = True,
    show_default = True,
    help = "Filter low confidence observations"
)
@click.option(
    '--confidence-threshold',
    default = 0.70,
    type = float,
    show_default = True,
    required = False,
    help = "Filter every observation with confidence below this threshold."
)
@click.option(
    '--digest-size',
    default = 10,
    type = int,
    show_default = True,
    required = False,
    help = "Size of the resulting hash in bytes."
)
@click.option(
    '--digest-salt',
    default = None,
    type = str,
    show_default = True,
    required = False,
    help = ("Salt used in hashing plate numbers. "
            "Defaults to a randomly generated string.")
)
@click.option(
    '--date-format',
    default = '%Y-%m-%d %H:%M:%S.%f',
    type = str,
    show_default = True,
    required = False,
    help = "Timestamp datetime format."
)
@click.command()
def raw_anpr(
    input_csv,
    output_pkl,
    names,
    skip_lines,
    cameras_geojson,
    anonymise,
    filter,
    confidence_threshold,
    digest_size,
    digest_salt,
    date_format
):
    """
    Wrangle a csv file containing raw ANPR data.

    The following tasks are executed:
        - Filter badly formatted license plate numbers
        - Filter all observations with confidence less than given threshold
        - Sort by Timestamp
        - Anonymise
        - Correct camera ids, given a wrangled cameras dataframe
    """

    log(("Reading input csv file with raw anpr data of size {:,.2f} MB.")\
            .format(os.stat(input_csv).st_size/1e6),
        level = lg.INFO)

    raw_anpr = pd.read_csv(
        filepath_or_buffer = input_csv,
        sep    = ',',
        names  = names.split(',') if names else None,
        header = None if names else 0,
        skiprows = skip_lines,
        parse_dates = ['timestamp'],
        date_parser = lambda x: pd.datetime.strptime(x, date_format),
        dtype  = {
            "vehicle": object,
            "camera": object,
            "timestamp": object,
            "confidence": np.float64
        },
        # Ignore any na values, assume there isn't any
        # (potentially just badly formatted plate numbers)
        na_values = ""
    )

    log("OK", level = lg.INFO)

    cameras = None if cameras_geojson is None else \
              gpd.GeoDataFrame.from_file(cameras_geojson)

    wrangled_anpr = wrangle_raw_anpr(
        raw_anpr,
        cameras = cameras,
        filter_low_confidence = filter,
        confidence_threshold = confidence_threshold,
        anonymise = anonymise,
        digest_size = digest_size,
        digest_salt = digest_salt.encode() if digest_salt else os.urandom(10),
    )

    pd.to_pickle(wrangled_anpr, output_pkl)

    return 0
