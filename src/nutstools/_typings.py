# -*- coding: utf-8 -*-
"""
Some typing definitions used in the NutsTools package
"""
from typing import Union
from pandas import Series, DataFrame
from pathlib import Path

SerieType = Union[Series, None]
DataFrameType = Union[DataFrame, None]
SeriesLike = Union[Series, list]
PathLike = Union[Path, str]
