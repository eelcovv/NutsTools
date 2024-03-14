from argparse import ArgumentTypeError

import pytest
from pathlib import Path

import pandas as pd

from nutstools.main import check_if_valid_nuts_level
from nutstools.postalnuts import NutsPostalCode, NutsData
from test_nuts_command_line_tool import get_root_directory

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
    """NutsData is used to store the default file location"""
    root = get_root_directory()
    nuts_file_name = root / Path("tests/pc2020_NL_NUTS-2021_v2.0_selection.csv")

    nuts_dl = NutsData(
        nuts_code_directory=".",
        nuts_file_name=nuts_file_name,
    )
    assert nuts_dl.nuts_codes_file == Path(nuts_file_name)
    assert nuts_dl.year == "2021"
    assert (
        nuts_dl.url
        == "https://gisco-services.ec.europa.eu/tercet/NUTS-2021//pc2020_NL_NUTS-2021_v2.0.zip"
    )


def test_one_postal2nuts():
    """NutsData is used to store the default file location"""
    root = get_root_directory()
    nuts_file_name = root / Path("tests/pc2020_NL_NUTS-2021_v2.0_selection.csv")

    nuts = NutsPostalCode(file_name=nuts_file_name)

    post_codes = ["2675BP", "5704 HG", "3344  em"]
    nuts_codes_level_3 = ["NL333", "NL414", "NL33A"]
    nuts_codes_level_2 = ["NL33", "NL41", "NL33"]
    nuts_codes_level_1 = ["NL3", "NL4", "NL3"]
    nuts_codes_level_0 = ["NL", "NL", "NL"]

    for postal_code, expected_code in zip(post_codes, nuts_codes_level_3):
        nuts_code = nuts.one_postal2nuts(postal_code=postal_code)
        assert nuts_code == expected_code

    for postal_code, expected_code in zip(post_codes, nuts_codes_level_2):
        nuts_code = nuts.one_postal2nuts(postal_code=postal_code, level=2)
        assert nuts_code == expected_code

    for postal_code, expected_code in zip(post_codes, nuts_codes_level_1):
        nuts_code = nuts.one_postal2nuts(postal_code=postal_code, level=1)
        assert nuts_code == expected_code

    for postal_code, expected_code in zip(post_codes, nuts_codes_level_0):
        nuts_code = nuts.one_postal2nuts(postal_code=postal_code, level=0)
        assert nuts_code == expected_code

    # postal code outside of domain gives None
    assert nuts.one_postal2nuts(postal_code="9999ZZ") is None

    # non-string postal code gives attribute error
    with pytest.raises(AttributeError):
        nuts.one_postal2nuts(postal_code=6)


def test_postal2nuts():
    """NutsData is used to store the default file location"""
    root = get_root_directory()
    nuts_file_name = root / Path("tests/pc2020_NL_NUTS-2021_v2.0_selection.csv")

    nuts = NutsPostalCode(file_name=nuts_file_name)

    postal_codes = ["2675BP", "5704 HG", "3344  em"]
    postal_codes_series = pd.Series(postal_codes)
    postal_codes_clean = ["2675BP", "5704HG", "3344EM"]
    nuts_codes_3 = ["NL333", "NL414", "NL33A"]
    nuts_codes_2 = ["NL33", "NL41", "NL33"]
    nuts_codes_1 = ["NL3", "NL4", "NL3"]
    nuts_codes_0 = ["NL", "NL", "NL"]

    nuts_codes_3 = pd.Series(nuts_codes_3, index=postal_codes_clean, name="NUTS3")
    nuts_codes_2 = pd.Series(nuts_codes_2, index=postal_codes_clean, name="NUTS2")
    nuts_codes_1 = pd.Series(nuts_codes_1, index=postal_codes_clean, name="NUTS1")
    nuts_codes_0 = pd.Series(nuts_codes_0, index=postal_codes_clean, name="NUTS0")

    nuts_codes = nuts.postal2nuts(postal_codes=postal_codes)
    pd.testing.assert_series_equal(nuts_codes_3, nuts_codes)

    nuts_codes = nuts.postal2nuts(postal_codes=postal_codes_series)
    pd.testing.assert_series_equal(nuts_codes_3, nuts_codes)

    nuts_codes = nuts.postal2nuts(postal_codes=postal_codes, level=2)
    pd.testing.assert_series_equal(nuts_codes_2, nuts_codes)

    nuts_codes = nuts.postal2nuts(postal_codes=postal_codes, level=1)
    pd.testing.assert_series_equal(nuts_codes_1, nuts_codes)

    nuts_codes = nuts.postal2nuts(postal_codes=postal_codes, level=0)
    pd.testing.assert_series_equal(nuts_codes_0, nuts_codes)

    # level must be in range 0 -- 3. Assertion error is raised otherwise
    with pytest.raises(ValueError):
        nuts_codes = nuts.postal2nuts(postal_codes=postal_codes, level=4)


def test_get_nuts_settings_nl():
    """test the retrieving of the default nuts settings"""
    root = get_root_directory()
    nuts_file_name = root / Path("tests/pc2020_NL_NUTS-2021_v2.0_selection.csv")

    nuts_dl = NutsData(
        nuts_code_directory=".",
        nuts_file_name=nuts_file_name,
        country="NL",
        update_settings=True,
    )
    nuts_dl.impose_nuts_settings()

    assert nuts_dl.country == "NL"
    assert nuts_dl.year == "2021"
    assert (
        nuts_dl.url
        == "https://gisco-services.ec.europa.eu/tercet/NUTS-2021//pc2020_NL_NUTS-2021_v2.0.zip"
    )
    assert "Cache/pc2020_NL_NUTS-2021_v2.0.zip" == nuts_dl.nuts_codes_file.as_posix()


def test_get_nuts_settings_be():
    """test the retrieving of the default nuts settings"""
    root = get_root_directory()
    nuts_file_name = root / Path("tests/pc2020_BE_NUTS-2021_v1.0_selection.csv")

    nuts_dl = NutsData(
        nuts_code_directory=".",
        nuts_file_name=nuts_file_name,
        country="BE",
        update_settings=True,
    )
    nuts_dl.impose_nuts_settings()

    assert nuts_dl.country == "BE"
    assert nuts_dl.year == "2021"
    assert (
        nuts_dl.url
        == "https://gisco-services.ec.europa.eu/tercet/NUTS-2021//pc2020_BE_NUTS-2021_v1.0.zip"
    )
    assert "Cache/pc2020_BE_NUTS-2021_v1.0.zip" == nuts_dl.nuts_codes_file.as_posix()
