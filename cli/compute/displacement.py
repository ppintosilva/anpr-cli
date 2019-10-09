import click

from anprx.compute import all_ods_displacement

import os
import numpy     as np
import pandas    as pd
import geopandas as gpd


@click.argument(
    'input-pkl',
    type=str
)
@click.option(
    '--buffer-size',
    default = 100,
    type = int,
    show_default = True,
    required = False,
    help = "Trip identification threshold."
)
@click.option(
    '--output',
    default = None,
    type = str,
    show_default = True,
    required = False,
    help = ("Output filename. "
            "By default appends displacement column to input dataframe.")
)
@click.option(
    '--parallel/--not-parallel',
    is_flag = True,
    default = True,
    show_default = True,
    help = "Parallelise calculation."
)
@click.command()
def displacement(
    input_pkl,
    buffer_size,
    parallel,
    output
):
    """
    Calculate vehicle displacements.
    """

    click.echo(("Reading input pkl file of size {:,.2f} MB.")\
            .format(os.stat(input_pkl).st_size/1e6))


    df = pd.read_pickle(input_pkl)

    df = all_ods_displacement(df, buffer_size, parallel)

    if output:
        df.to_pickle(output)
    else:
        # write to same input to save space
        df.to_pickle(input_pkl)

    return 0
