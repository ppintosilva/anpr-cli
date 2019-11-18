import os
import click
import fiona
import networkx             as nx
import geopandas            as gpd

from   anprx.preprocessing  import gdfs_from_network


supported_out_formats = \
    [k for k, v in fiona.supported_drivers.items() if 'w' in v]
"""
{'AeronavFAA': 'r',
 'ARCGEN': 'r',
 'BNA': 'raw',
 'DXF': 'raw',
 'CSV': 'raw',
 'OpenFileGDB': 'r',
 'ESRIJSON': 'r',
 'ESRI Shapefile': 'raw',
 'GeoJSON': 'rw',
 'GeoJSONSeq': 'rw',
 'GPKG': 'rw',
 'GML': 'raw',
 'GPX': 'raw',
 'GPSTrackMaker': 'raw',
 'Idrisi': 'r',
 'MapInfo File': 'raw',
 'DGN': 'raw',
 'S57': 'r',
 'SEGY': 'r',
 'SUA': 'r',
 'TopoJSON': 'r'}
"""

supported_out_format_extensions = \
    ['bna', 'dxf', 'csv', 'shp', 'geojson', 'geojsonseq',
     'gpkg', 'gml', 'gpx', 'gtm', 'mapinfo']

format_to_extension = dict(zip(supported_out_formats,
                               supported_out_format_extensions))

@click.argument(
    'input-pkl',
    type = click.File('rb')
)
@click.option(
    '--out-format',
    type=click.Choice(supported_out_formats),
    default = "ESRI Shapefile"
)
@click.option(
    '--out-stem',
    type=str,
    default = None
)

@click.command()
def network(
    input_pkl,
    out_format,
    out_stem
):
    """
    Obtain the road network graph from OpenStreetMap.
    """

    # Read networkx graph as pkl
    G = nx.read_gpickle(input_pkl)

    # Convert to geopandas
    nodes_gdf, edges_gdf = gdfs_from_network(G)

    # Write output
    if out_stem is None:
        out_stem = os.path.splitext(input_pkl)[0]

    extension = format_to_extension[out_format]

    nodes_gdf.to_file('{}_nodes.{}'.format(out_stem, extension),
                      driver = out_format)

    edges_gdf.to_file('{}_edges.{}'.format(out_stem, extension),
                      driver = out_format)

    return 0
