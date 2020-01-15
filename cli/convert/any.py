import os
import click
import pandas         as pd

@click.argument(
    'input-pkl',
    type = str
)
@click.option(
    '--to',
    type=click.Choice(['csv']),
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
def pkl(
    input_pkl,
    to,
    out_name
):
    """
    Convert trip pickle files to other formats.
    """

    # Read networkx graph as pkl
    df = pd.read_pickle(input_pkl)

    # Write output
    if out_name is None:
        out_name = os.path.splitext(input_pkl)[0]

    output = '{}.{}'.format(out_name, to)

    df.to_csv(output, index = False)

    return 0
