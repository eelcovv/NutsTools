import logging
import os
from pathlib import Path
from typing import Union

import appdirs
import pandas as pd
import requests

try:
    import requests_kerberos_proxy
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
)

_logger = logging.getLogger(__name__)


class NutsPostalCode:
    def __init__(self, file_name: Union[object, str]):
        """
        Parameters
        ----------
        file_name : object
            Filename of the nuts input file
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

    def postal2nuts(self, postal_codes: type(pd.Series), level=3):
        postal_codes = postal_codes.str.replace("\s", "", regex=True)

        nuts_codes = self.nuts_data.reindex(postal_codes)

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


class NutsData:
    def __init__(
        self,
        year: str = None,
        country: str = None,
        nuts_file_name: Union[Path, str] = None,
        nuts_code_directory: str = None,
        update_settings: bool = False,
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

        self.settings_file_name = self.directory / Path("nutstools_settings.yml")

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

        if not self.nuts_codes_file.exists():
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
        proxies = dict(
            http=os.environ.get("HTTP_PROXY"),
            https=os.environ.get("HTTPS_PROXY"),
        )

        if proxies and requests_kerberos_proxy is not None:
            _logger.debug("Trying to connection using Kerberos and potentially a proxy")
            session = requests_kerberos_proxy.util.get_session(proxies=proxies)
        else:
            _logger.debug("Trying to connection using plain requests")
            session = requests.Session()

        _logger.debug(f"Requesting {self.url}")
        request = session.get(self.url)

        if request.status_code == 200:
            _logger.debug(f"Url exists : {self.url}.")
            _logger.info(f"Downloading data from : {self.url}.")
            with open(self.nuts_codes_file, "wb") as stream:
                stream.write(request.content)
            _logger.info(f"Success!")
        else:
            _logger.warning(f"Cannot fine data set: {self.url}")
