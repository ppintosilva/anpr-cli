import click
from anprx import preprocessing

import numpy  as np
import pandas as pd

@click.argument(
    'output',
    type=click.File('wb')
)
@click.argument(
    'input',
    type=click.File('rb')
)
@click.option(
    '--output-format',
    type=click.Choice(['geojson', 'csv']),
    default = 'geojson',
    required = False
)
@click.option(
    '--names', '-h',
    type = str,
    default = 'id,lat,lon,name,description,is_commissioned,type',
    required = False,
)
@click.option(
    '--header/--no-header',
    default = True,
    required = False,
)
# @click.option(
#     '--infer-direction',
#     type = str,
#     default = 'description',
#     required = False,
# )
@click.command()
def cameras(input, output, output_format, names, header):
    """
    Wrangle a csv file containing the location, identifiers and other
    raw information about ANPR cameras.
    """
    cameras = pd.read_csv(
        filepath_or_buffer = input,
        sep = ',',
        names = names.split(','),
        header = 1 if header else None,
        dtype = {
            "id": object,
            "name": object,
            "lat": np.float64,
            "lon": np.float64,
            "is_commissioned" : bool,
            "type": object,
            "description" : object
        }
    )

    proj_coords = (output_format == "geojson")

    wcameras = preprocessing.wrangle_cameras(
        cameras = cameras
        # infer_direction_col = infer_direction
    )
    if proj_coords:
        wcameras.to_file(output, driver='GeoJSON')
    elif output_format == "csv":
        wcameras.to_csv(output, index = False)

    return 0

# @wrangle.command()
# def expert_camera_pairs():
#     """
#     Wrangle a csv file containing information about the pairs of cameras used by
#     traffic operators, and other experts, to reason about the flow of traffic.
#     """
#     pass
