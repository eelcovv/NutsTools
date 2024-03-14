# -*- coding: utf-8 -*-
"""
A tool to convert postal codes to NUTS-values based on the NUTS files distributed by Eurostat.

Usage:
------

**Examples**:

Convert a postal code to NUTS:

.. code-block:: text

    > postalcode2nuts.exe --postal_code 2612AB

Output of this command is:

.. code-block:: text

    2612AB    NL333

Convert the file *postal_codes.txt* with postal codes to NUTS:

.. code-block:: text

    >> postalcode2nuts.exe --input_file_name postal_codes.txt --output_file_name -

gives  the following output:

.. code-block:: text

    8277AM    NL211
    2871KA    NL33B
    9408BJ    NL131
    3076KA    NL33C
    3068LM    NL33C
    7543GV    NL213

In case the *--output_file_name* argument is not given, the codes are written to file with the same name
as the input file with a suffix nuts3 (default), where 3 stands for the level of the NUTS output.
The level can be altered using the *--level*  option.

**Help**:

.. code-block:: text

    PS>postalcode2nuts.exe --help

    usage: postalcode2nuts [-h] [--version] [-p POSTALCODE] [-i INPUT_FILE_NAME]
                           [--nuts_file_name NUTS_INPUT_FILE_NAME] [-o OUTPUT_FILE_NAME] [-v] [-vv] [-l LEVEL]
                           [--year {2021}]
                           [--country {PT,DK,SE,PL,TR,MK,NO,SI,LV,ES,CH,NL,SK,CZ,LI,EL,HR,IS,LT,UK,IT,FI,HU,CY,EE,RS,IE,
                           RO,LU,BE,DE,FR,AT,BG}]
                           [--update_settings] [--force_download] [--directory DIRECTORY]

    Converts a postal code to its NUTS code

    options:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -p POSTALCODE, --postal_code POSTALCODE
                            Postcode
      -i INPUT_FILE_NAME, --input_file_name INPUT_FILE_NAME
                            Input file with Postal codes
      --nuts_file_name NUTS_INPUT_FILE_NAME
                            Overrule input filename with the NUTS translation data
      -o OUTPUT_FILE_NAME, --output_file_name OUTPUT_FILE_NAME
                            Output file with Postal codes and NUTS
      -v, --verbose         set loglevel to INFO
      -vv, --debug          set loglevel to DEBUG
      -l LEVEL, --level LEVEL
                            The level at we want to get the NUTS-code
      --year {2021}         The year of the NUTS files
      --country {PT,DK,SE,PL,TR,MK,NO,SI,LV,ES,CH,NL,SK,CZ,LI,EL,HR,IS,LT,UK,IT,FI,HU,CY,EE,RS,IE,RO,LU,BE,DE,FR,AT,BG}
                            The country code for the NUTS file
      --update_settings     Update the settings file with the new values
      --force_download      Forces to download the datafile again, even if it already exists
      --directory DIRECTORY
                        The location of the the NUTS files. If not given, the default directory will be picked
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
    parser = argparse.ArgumentParser(
        description="Converts a postal code to its NUTS code"
    )
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
        "--force_download",
        help="Forces to download the datafile again, even if it already exists",
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
        force_download=args.force_download,
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
