"""anpr-cli: A CLI for pre-processing and analysing batches of ANPR data."""

import click

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
@click.group(cls=PipelineCLI)
def cli():
    pass

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
