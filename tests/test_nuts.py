from argparse import ArgumentTypeError


import pytest
from pathlib import Path

from nutstools.main import check_if_valid_nuts_level
from nutstools.postalnuts import NutsPostalCode, NutsData
from .test_nuts_command_line_tool import get_root_directory

__author__ = "EVLT"
__copyright__ = "EVLT"
__license__ = "MIT"


def test_check_if_valid_nuts_level_one():
    assert check_if_valid_nuts_level(1)


def test_check_if_valid_nuts_level_two():
    assert check_if_valid_nuts_level(2)


def test_check_if_valid_nuts_level_three():
    assert check_if_valid_nuts_level(3)


def test_check_if_valid_nuts_level_string():
    with pytest.raises(ArgumentTypeError, match=".*"):
        check_if_valid_nuts_level("four")


def test_check_if_valid_nuts_level_four():
    with pytest.raises(ArgumentTypeError, match=".*"):
        check_if_valid_nuts_level(4)


def test_nuts_data():
    """ NutsData is used to store the default file location """
    root = get_root_directory()
    nuts_file_name = root / Path("tests/pc2020_NL_NUTS-2021_v2.0_selection.csv")

    nuts_dl = NutsData(
        nuts_code_directory=".",
        nuts_file_name=nuts_file_name,
    )
    assert nuts_dl.nuts_codes_file == Path(nuts_file_name)
    assert nuts_dl.year == '2021'
    assert nuts_dl.url == "https://gisco-services.ec.europa.eu/tercet/NUTS-2021//pc2020_NL_NUTS-2021_v2.0.zip"


def test_nuts_postcode():
    """ NutsData is used to store the default file location """
    root = get_root_directory()
    nuts_file_name = root / Path("tests/pc2020_NL_NUTS-2021_v2.0_selection.csv")

    nuts = NutsPostalCode(file_name=nuts_file_name)

    post_codes = ["2675BP", "5704 HG", "3344  em"]
    nuts_codes = ["NL333", "NL414", "NL33A"]

    for postal_code, expected_code in zip(post_codes, nuts_codes):
        nuts_code = nuts.one_postal2nuts(postal_code=postal_code)
        assert nuts_code == expected_code

    with pytest.raises(KeyError):
        nuts.one_postal2nuts(postal_code="9999ZZ")

    with pytest.raises(AttributeError):
        nuts.one_postal2nuts(postal_code=6)


