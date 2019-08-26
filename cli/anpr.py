"""anpr-cli: A CLI for pre-processing and analysing batches of ANPR data."""

import click
import anprx

from .wrangle import cameras as cameras
from .wrangle import network as network
from .wrangle import data    as data
from .compute import flows   as flows
from .compute import trips   as trips


# Custom class so that we can change the order of subcommands as diplayed
# in the help
class PipelineCLI(click.Group):
    def list_commands(self, ctx):
        """A CLI for wrangling and analysing batches of ANPR data."""
        # original value --> return sorted(self.commands)
        return ['wrangle', 'compute', 'explore']


class WranglePipeline(click.Group):
    def list_commands(self, ctx):
        """A CLI for wrangling and analysing batches of ANPR data."""
        # original value --> return sorted(self.commands)
        return ['cameras', 'network', 'merge', 'camera-pairs', 'nodes',
                'expert-pairs', 'raw-anpr']

class ComputePipeline(click.Group):
    def list_commands(self, ctx):
        """A CLI for transforming and aggregating wrangled ANPR data."""
        # original value --> return sorted(self.commands)
        return ['trips', 'flows']

# Main group - entry point
@click.option("--quiet", "-q",
                is_flag = True,
                default = False              ,
                help = "Suppress printing log messages to console."
)
@click.option("--app_folder", "-p",
              default = ".temp",
              type = str,
              show_default = True,
              help = "Path to work directory (logs, images, files)"
)
@click.group(cls=PipelineCLI)
def cli(quiet, app_folder):
    anprx.utils.config(
        app_folder = app_folder,
        log_to_console = not quiet,
        cache_http = True
    )

# Data wrangling operations
@cli.group(cls=WranglePipeline)
def wrangle():
    """Pre-process and wrangle raw data."""
    pass

# Summarise operations, e.g.: compute flows
@cli.group(cls=ComputePipeline)
def compute():
    """Identify trips in wrangled data and summarise it into traffic flows."""
    pass


wrangle.add_command(cameras.cameras)
wrangle.add_command(cameras.nodes)
wrangle.add_command(cameras.expert_pairs)
wrangle.add_command(network.network)
wrangle.add_command(network.merge)
wrangle.add_command(network.camera_pairs)
wrangle.add_command(data.raw_anpr)
compute.add_command(trips.trips)
compute.add_command(flows.flows)
