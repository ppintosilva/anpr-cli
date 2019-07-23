"""anpr-cli: A CLI for pre-processing and analysing batches of ANPR data."""

import click
import anprx

from .wrangle import cameras as cameras
from .wrangle import network as network
from .compute import flows as flows


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
                'expert-pairs']

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
@cli.group()
def compute():
    """Summarise wrangled data into traffic flows."""
    pass


wrangle.add_command(cameras.cameras)
wrangle.add_command(cameras.nodes)
wrangle.add_command(cameras.expert_pairs)
wrangle.add_command(network.network)
wrangle.add_command(network.merge)
wrangle.add_command(network.camera_pairs)
compute.add_command(flows.flows)
