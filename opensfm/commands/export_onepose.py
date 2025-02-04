from opensfm.actions import export_onepose

from argparse import ArgumentParser, Namespace
from .command import CommandBase
from opensfm.dataset import DataSet

class Command(CommandBase):
    name = "export_onepose"
    help = "Export reconstruction to OnePose format"

    def run_impl(self, dataset: DataSet, args: Namespace) -> None:
        export_onepose.run_dataset(dataset)

    def add_arguments_impl(self, parser: ArgumentParser) -> None:
        pass
