import click

from anprx.flows import get_flows
from anprx.flows import get_periods
from anprx.flows import expand_flows
from anprx.utils import log

import os
import numpy     as np
import pandas    as pd
import geopandas as gpd
import logging   as lg

@click.argument(
    'output',
    type=str
)
@click.argument(
    'input-trips-pkl',
    type=str
)
@click.option(
    '--output-format',
    type=click.Choice(['csv','pkl']),
    default = 'pkl',
    show_default = True,
    required = False,
    help = ("Format of output file.")
)
@click.option(
    '--freq',
    type = str,
    default = "5T",
    required = False,
    show_default = True,
    help = ("Frequency string determining the length of each time period. "
            "Refer to pandas' timeseries user guide for valid strings.")
)
@click.option(
    '--drop-na',
    is_flag = True,
    default = False,
    show_default = True,
    help = ("Ignore od pairs, whose origin or destination is missing "
            "(first and last steps of each trip)")
)
@click.option(
    '--skip-explicit',
    is_flag = True,
    default = False,
    show_default = True,
    help = "Skip filling in missing spatio-temporal combinations: (od, period)"
)
@click.command()
def flows(
    input_trips_pkl,
    output,
    output_format,
    freq,
    drop_na,
    skip_explicit):
    """Compute flows between camera pairs from wrangled data."""

    log(("Reading input pkl file with wrangled trip data of size {:,.2f} MB.")\
            .format(os.stat(input_trips_pkl).st_size/1e6),
        level = lg.INFO)

    trips = pd.read_pickle(input_trips_pkl)

    flows = get_flows(trips, freq,
                      remove_na = drop_na)

    if not skip_explicit:
        periods = get_periods(trips, freq)[:-1]

        flows = expand_flows(
            flows.set_index(['origin','destination','period']),
            periods
        )

    if output_format == "csv":
        flows.to_csv(output, index = False)
    elif output_format == "pkl":
        flows.to_pickle(output)

    return 0
