from argparse import ArgumentTypeError


import pytest
from pathlib import Path

from nutstools.main import check_if_valid_nuts_level
from nutstools.main import main

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


def test_main_one_postalcode(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(
        [
            "--nuts_file_name",
            "pc2020_NL_NUTS-2021_v2.0_selection.csv",
            "--postal_code",
            "8277AM",
        ]
    )
    captured = capsys.readouterr()
    assert "NL211" in captured.out


def test_main_input_file(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    examples_directory = Path("examples")
    postal_codes = examples_directory / Path("postal_codes.txt")
    postal_codes_expected = Path("postal_codes_expected.txt")

    if not examples_directory.exists():
        # if we run from the tests directory, move one directory up for the examples data
        postal_codes = Path("..") / postal_codes
    else:
        # if we run from the root directory, move into tests to get the expected data
        postal_codes_expected = Path("tests") / postal_codes_expected

    main(
        [
            "--nuts_file_name",
            "pc2020_NL_NUTS-2021_v2.0_selection.csv",
            "--input_file",
            postal_codes.as_posix(),
            "--output_file_name",
            "-",
        ]
    )
    captured = capsys.readouterr()
    with open(postal_codes_expected.as_posix(), "r") as fp:
        for line in captured.out.splitlines():
            expected_line = fp.readline().strip()
            assert line == expected_line
