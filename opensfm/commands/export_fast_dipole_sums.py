from opensfm.actions import export_fast_dipole_sums

from . import command
import argparse
from opensfm.dataset import DataSet


class Command(command.CommandBase):
    name = "export_fast_dipole_sums"
    help = "Export dense reconstruction to fast dipole sums format"

    def run_impl(self, dataset: DataSet, args: argparse.Namespace) -> None:
        export_fast_dipole_sums.run_dataset(dataset)

    def add_arguments_impl(self, parser: argparse.ArgumentParser) -> None:
        pass
