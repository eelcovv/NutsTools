"""
A tool to convert postal codes to NUTS-values based on the NUTS files distributed by Eurostat
"""

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from nutstools import __version__
from nutstools import postalnuts
from nutstools.nutsdata import COUNTRY_CODES, DEFAULT_YEAR, NUTS_YEARS, DEFAULT_COUNTRY

__author__ = "EVLT"
__copyright__ = "EVLT"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def check_if_valid_nuts_level(value):
    """check if the argument is a valid nuts level. Must be between 0 and 3"""
    try:
        value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Nuts level should be an integer between the range 0 - 3. Now given level {value}"
        )
    try:
        assert 0 <= value <= 3
    except AssertionError:
        raise argparse.ArgumentTypeError(
            f"Nuts level should be in the range 0 - 3. Now given level {value}"
        )
    return value


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Converts a postal code to its NUTS code")
    parser.add_argument(
        "--version",
        action="version",
        version="NutsTools {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-p",
        "--postal_code",
        help="Postcode",
        type=str,
        metavar="POSTALCODE",
        action="append",
    )
    parser.add_argument(
        "-i",
        "--input_file_name",
        help="Input file with Postal codes",
        type=str,
        metavar="INPUT_FILE_NAME",
    )
    parser.add_argument(
        "--nuts_file_name",
        help="Overrule input filename with the NUTS translation data",
        type=str,
        metavar="NUTS_INPUT_FILE_NAME",
    )
    parser.add_argument(
        "-o",
        "--output_file_name",
        help="Output file with Postal codes and NUTS",
        type=str,
        metavar="OUTPUT_FILE_NAME",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--debug",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "-l",
        "--level",
        dest="level",
        type=check_if_valid_nuts_level,
        help="The level at we want to get the NUTS-code",
        default=3,
    )
    parser.add_argument(
        "--year",
        help="The year of the NUTS files",
        choices=NUTS_YEARS,
    )
    parser.add_argument(
        "--country",
        help="The country code for the NUTS file ",
        choices=COUNTRY_CODES,
    )
    parser.add_argument(
        "--update_settings",
        help="Update the settings file with the new values",
        action="store_true",
    )
    parser.add_argument(
        "--directory",
        help="The location of the  the NUTS files. If not given, the default directory will be picked ",
    )

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`postal_code2nuts` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`postal_code2nuts`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    if args.postal_code is None and args.input_file_name is None:
        raise argparse.ArgumentError(
            argument=args.postal_code,
            message="Either --postal_code or --input_file_name option must be given",
        )
    elif args.postal_code is not None and args.input_file_name is not None:
        raise argparse.ArgumentError(
            argument=args.postal_code,
            message="Only one of the options --postal_code or --input_file_name option can "
            "be given",
        )

    nuts_dl = postalnuts.NutsData(
        year=args.year,
        country=args.country,
        nuts_file_name=args.nuts_file_name,
        nuts_code_directory=args.directory,
        update_settings=args.update_settings,
    )

    if args.input_file_name is not None:
        input_file_name = Path(args.input_file_name)
        postal_codes = pd.read_csv(input_file_name)
        output_file_name = "_".join(
            [input_file_name.with_suffix("").as_posix(), f"nuts{args.level}.csv"]
        )
    else:
        postal_codes = pd.DataFrame(data=args.postal_code, columns=["CODES"])
        output_file_name = None

    if args.output_file_name is not None:
        if args.output_file_name == "-":
            output_file_name = None
        else:
            output_file_name = Path(args.output_file_name)

    first_column_name = postal_codes.columns[0]

    postal_codes = (
        postal_codes[first_column_name]
        .str.replace("'", "")
        .replace("\s", "", regex=True)
    )

    nuts = postalnuts.NutsPostalCode(file_name=nuts_dl.nuts_codes_file)
    nuts_codes = nuts.postal2nuts(postal_codes=postal_codes, level=args.level)

    if output_file_name is not None:
        _logger.info(f"Writing nuts codes to {output_file_name}")
        nuts_codes.to_csv(output_file_name)
    else:
        print(nuts_codes.to_string(header=False))

    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m nutstools.skeleton 42
    #
    run()
