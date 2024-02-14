from argparse import ArgumentTypeError


import pytest

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
    main(
        [
            "--nuts_file_name",
            "pc2020_NL_NUTS-2021_v2.0_selection.csv",
            "--input_file",
            "../examples/postal_codes.txt",
            "--output_file_name",
            "-",
        ]
    )
    captured = capsys.readouterr()
    with open("postal_codes_expected.txt", "r") as fp:
        for line in captured.out.splitlines():
            expected_line = fp.readline().strip()
            assert line == expected_line
