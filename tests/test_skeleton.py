import pytest

from NutsTools.main import postal_code2nuts, main

__author__ = "EVLT"
__copyright__ = "EVLT"
__license__ = "MIT"


def test_fib():
    """API Tests"""
    assert postal_code2nuts(1) == 1
    assert postal_code2nuts(2) == 1
    assert postal_code2nuts(7) == 13
    with pytest.raises(AssertionError):
        postal_code2nuts(-10)


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["7"])
    captured = capsys.readouterr()
    assert "The 7-th Fibonacci number is 13" in captured.out
