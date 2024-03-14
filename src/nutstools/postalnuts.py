# Class definition for NutsTools. Can be used in your own Python code to retrieve the nuts data from the EU-website
# and convert postal codes in NUTS codes

import logging
from pathlib import Path
from typing import Union

import appdirs
import pandas as pd
import requests

try:
    from requests_kerberos_proxy.util import get_session
except ImportError:
    requests_kerberos_proxy = None

import yaml

from .nutsdata import (
    COUNTRY_CODES,
    DEFAULT_YEAR,
    DEFAULT_COUNTRY,
    NUTS_YEARS,
    NUTS_DATA,
    NUTS_CODE_DEFAULT_DIRECTORY,
    NUTS_CODE_DEFAULT_SETTINGS_FILE_NAME,
)

from ._typings import SeriesLike, PathLike

_logger = logging.getLogger(__name__)


class NutsPostalCode:
    """
    Class to hold the postal nuts code

    Args:
        file_name (PathLike): The nuts input file holding all the nuts codes. Can be either a pathlib Path or a string.

    Attributes:
        file_name (Path): Path of the file contains the nuts code downloaded from the Eurostat website
        nuts_data (DataFrame): All the nuts data loaded from the file
        nuts_key (str): Name of column containing the NUTS codes. Equal to the first column of the input data file
        postal_codes_key (str): Name of the column containing the postal codes. Equal to the second column of the input
            data file
    """

    def __init__(self, file_name: PathLike):
        """
        The constructor to initialize the object
        """
        self.file_name = Path(file_name)

        _logger.info(f"Reading data {file_name}")
        if self.file_name.suffix == ".zip":
            compression = "zip"
        else:
            compression = None
        self.nuts_data = pd.read_csv(
            self.file_name.as_posix(), sep=";", compression=compression
        )
        self.nuts_key = self.nuts_data.columns[0]
        self.postal_codes_key = self.nuts_data.columns[1]
        for column_name in self.nuts_data.columns:
            self.nuts_data[column_name] = (
                self.nuts_data[column_name]
                .str.replace("'", "")
                .replace("\s", "", regex=True)
            )
        self.nuts_data = self.nuts_data.set_index(self.postal_codes_key, drop=True)[
            self.nuts_key
        ]
        _logger.debug(f"Done")

    def postal2nuts(self, postal_codes: SeriesLike, level: int = 3):
        """
        Convert the series or list of postal codes to a series of nuts code at level

        Args:
            postal_codes: DataFrame or Series
            level: int
                Level of the nuts codes. Either, 0, 1, 2 or 3. Default is 3

        Returns:
            Series with the converted NUTS codes
        """

        if isinstance(postal_codes, list):
            # turn list into Series
            postal_codes = pd.Series(postal_codes)

        postal_codes = postal_codes.str.replace("\s", "", regex=True)

        nuts_codes = self.nuts_data.reindex(postal_codes)

        # in case a nuts level lower than 3 is given, remove the last digits
        if level == 2:
            nuts_codes = nuts_codes.str.replace(".$", "", regex=True)
            nuts_codes = nuts_codes.rename("NUTS2")
        elif level == 1:
            nuts_codes = nuts_codes.str.replace("..$", "", regex=True)
            nuts_codes = nuts_codes.rename("NUTS1")
        elif level == 0:
            nuts_codes = nuts_codes.str.replace("...$", "", regex=True)
            nuts_codes = nuts_codes.rename("NUTS0")

        return nuts_codes

    def one_postal2nuts(self, postal_code: str, level: int = 3):
        """
        Return the NUTS code for a single postal code

        Args:
            postal_code: str
                The postal code to retrieve the data for
            level: int
                The nuts level

        Returns:
            str:
                The nuts code belonging to the postal code
        """

        try:
            postal_code = postal_code.replace(" ", "")
        except AttributeError:
            raise AttributeError(
                f"Postal code {postal_code} is not a string. Please check your input"
            )
        else:
            postal_code = postal_code.upper()

        try:
            nuts_code = self.nuts_data.loc[postal_code]
        except KeyError:
            raise KeyError(f"Could not find NUTS code for postal code {postal_code}")

        # in case a nuts level lower than 3 is given, remove the last digits
        if level == 2:
            nuts_code = nuts_code.replace(".$", "", regex=True)
        elif level == 1:
            nuts_code = nuts_code.replace("..$", "", regex=True)
        elif level == 0:
            nuts_code = nuts_code.replace("...$", "", regex=True)

        return nuts_code


class NutsData:
    """
    Class to hold all the references to NUTS data

    Args:
        year (str): Year of the NUTS data
        country (str): Two-letter code of the country to use for the NUTS data
        nuts_file_name (PathLike): Name of the file of the downloaded nuts data
        nuts_code_directory (PathLike): Name of the directory where the NUTS data is stored
        update_settings (bool): If true, the settings file is updated.

    Attributes:
        directory (Path): Location of the configuration settings file. Defaults to
            C:\\\\Users\\\\username\\\\AppData\\\\Local\\\\nutstools (Windows) or /home/username/.local/share (linux)
        cache_directory (Path): directory where downloaded data is stored for reuse. Defaults to 'Cache' relative
            'directory'.
        settings_file_name (Path): Name of the settings file to store the default settings. Defaults to
            'nutstools_settings.yml' located in 'directory'.
            This file is created the first run and read every next run. Altering the values in this file  alters the
            default behaviour. The default behaviour can also be overwritten by using the update_settings command line
            argument
        url (str): The URL to the NUTS data at the EU website. Is stored in the settings file and can be altered there.
        year (str): The year for which the NUTS data is retrieved. Defaults to '2021' (current latest version), but
            can be altered in the settings file.
        country (str): Two-letter code to set the country for which we want to download the NUTS data. Defaults to
            'NL'. Can be altered using the *country* command line option combined with *update_settings* in order
            to force to rewrite the settings file
        nuts_codes_file (PathLike): The filename to the NUTS data downloaded from the EU website
        nuts_data (DataFrame): The Dataframe where the NUTS data is stored after reading the *nuts_codes_file*
    """

    def __init__(
        self,
        year: str = None,
        country: str = None,
        nuts_file_name: Union[Path, str] = None,
        nuts_code_directory: str = None,
        update_settings: bool = False,
        force_download: bool = False,
    ):
        if nuts_code_directory is None:
            self.directory = Path(
                appdirs.user_config_dir(NUTS_CODE_DEFAULT_DIRECTORY)
            ).parent
        else:
            self.directory = Path(nuts_code_directory)

        self.cache_directory = self.directory / Path("Cache")

        self.directory.mkdir(exist_ok=True, parents=True)
        self.cache_directory.mkdir(exist_ok=True, parents=True)

        self.settings_file_name = self.directory / Path(
            NUTS_CODE_DEFAULT_SETTINGS_FILE_NAME
        )
        self.url = None

        if year is not None:
            self.year = year
        else:
            self.year = DEFAULT_YEAR

        if country is not None:
            self.country = country
        else:
            self.country = DEFAULT_COUNTRY

        self.nuts_codes_file: Path = Path(".")

        default_settings = dict(
            DEFAULT_YEAR=self.year,
            DEFAULT_COUNTRY=self.country,
            NUTS_CODE_DEFAULT_DIRECTORY=self.directory.as_posix(),
            COUNTRY_CODES=COUNTRY_CODES,
            NUTS_YEARS=NUTS_YEARS,
            NUTS_DATA=NUTS_DATA,
        )

        if not self.settings_file_name.exists() or update_settings:
            _logger.info(f"Writing default settings to {self.settings_file_name}")
            with open(self.settings_file_name, "w") as stream:
                yaml.dump(default_settings, stream, default_flow_style=False)

        _logger.info(f"Reading settings from {self.settings_file_name}")
        with open(self.settings_file_name, "r") as stream:
            self.settings = yaml.safe_load(stream)

        self.get_nuts_settings()

        if nuts_file_name is not None:
            nuts_file_name = Path(nuts_file_name)
            if nuts_file_name.exists():
                self.nuts_codes_file = nuts_file_name

        if not self.nuts_codes_file.exists() or force_download:
            self.download_nuts_codes()
        else:
            _logger.info(f"File {self.nuts_codes_file} already downloaded!")

        if self.nuts_codes_file.suffix == ".zip":
            self.nuts_data = pd.read_csv(
                self.nuts_codes_file, sep=";", compression="zip"
            )
        else:
            self.nuts_data = pd.read_csv(self.nuts_codes_file, sep=";")

    def get_nuts_settings(self):
        """
        Read the settings of the tool from the stored settings file
        """

        self.year = self.settings["DEFAULT_YEAR"]
        self.country = self.settings["DEFAULT_COUNTRY"]

        try:
            nuts_year_prop = NUTS_DATA[self.year]
        except KeyError as err:
            _logger.warning(err)
            raise KeyError(f"Year {self.year} not available. Please pick another one")

        self.url = nuts_year_prop["url"]
        nuts_files = nuts_year_prop["files"]

        try:
            remote_file_name = nuts_files[self.country]
        except KeyError as err:
            _logger.warning(err)
            raise KeyError(
                f"Country {self.country} not available. Please pick another one"
            )
        else:
            self.url = "/".join([self.url, remote_file_name])

        self.nuts_codes_file = self.cache_directory / Path(remote_file_name)

    def download_nuts_codes(self):
        """
        Download the NUTS data from the EU website

        Notes
        -----
        * Open a session, either via kerberos and a proxy or via a normal request session

        Returns:
            bool: True for success, False for failed download.
        """
        if requests_kerberos_proxy is not None:
            session = get_session()
        else:
            _logger.debug("Trying to connection using plain requests")
            session = requests.Session()

        _logger.debug(f"Requesting {self.url}")
        request = session.get(self.url)

        success = False

        if request.ok:
            _logger.debug(f"Url exists : {self.url}.")
            _logger.info(f"Downloading data from : {self.url}.")
            with open(self.nuts_codes_file, "wb") as stream:
                stream.write(request.content)
            _logger.info(f"Success!")
            success = True
        else:
            _logger.warning(f"Cannot fine data set: {self.url}")

        return success
