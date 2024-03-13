from pathlib import Path

from nutstools.main import main

__author__ = "EVLT"
__copyright__ = "EVLT"
__license__ = "MIT"


def get_root_directory():
    """small utility to get the root directory from which pytests is launched"""
    current_directory = Path(".").cwd().name
    if current_directory == "tests":
        # we are inside the tests-directory. Move one up
        root_directory = Path("..")
    else:
        # we are in the root directory
        root_directory = Path(".")
    return root_directory


def test_main_one_postalcode(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html

    root = get_root_directory()
    nuts_file = root / Path("tests/pc2020_NL_NUTS-2021_v2.0_selection.csv")

    main(
        [
            "--nuts_file_name",
            nuts_file.as_posix(),
            "--postal_code",
            "8277AM",
        ]
    )
    captured = capsys.readouterr()
    assert captured.out == "8277AM    NL211\n"


def test_main_input_file(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    root = get_root_directory()

    postal_codes = root / Path("examples/postal_codes.txt")
    postal_codes_expected = root / Path("tests/postal_codes_expected.txt")

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
