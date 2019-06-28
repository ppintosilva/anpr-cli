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

# Main group - entry point
@click.option("--verbose", "-v", count = True, show_default = True)
@click.option("--app_folder", "-p", default = ".temp",
              type = str, show_default = True)
@click.group(cls=PipelineCLI)
def cli(verbose, app_folder):
    anprx.utils.config(
        app_folder = app_folder,
        log_to_console = verbose,
        cache = True
    )

# Data wrangling operations
@cli.group(chain = True)
def wrangle():
    """Pre-process and wrangle raw data."""
    pass

# Summarise operations, e.g.: compute flows
@cli.group()
def compute():
    """Summarise wrangled data into traffic flows."""
    pass


wrangle.add_command(cameras.cameras)
wrangle.add_command(network.network)
compute.add_command(flows.flows)
