import os
import click
import pandas         as pd

supported_out_formats = ['csv']

@click.argument(
    'input-pkl',
    type = str
)
@click.option(
    '--out-format',
    type=click.Choice(supported_out_formats),
    default = "csv"
)
@click.option(
    '--out-name',
    type=str,
    default = None,
    help = ("Set custom name for output file. "
            "Defaults to same as input file.")
)

@click.command()
def trips(
    input_pkl,
    out_format,
    out_name
):
    """
    Convert trip pickle files to other formats.
    """

    # Read networkx graph as pkl
    trips = pd.read_pickle(input_pkl)

    # Write output
    if out_name is None:
        out_name = os.path.splitext(input_pkl)[0]

    output = '{}.{}'.format(out_name, out_format)

    trips.to_csv(output, index = False)

    return 0
