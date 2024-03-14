# -*- coding: utf-8 -*-
"""
Some typing definitions used in the NutsTools package
"""
from typing import Union, TypeAlias
from pandas import Series, DataFrame
from pathlib import Path

SerieType: TypeAlias = Union[Series, None]
DataFrameType: TypeAlias = Union[DataFrame, None]
SeriesLike: TypeAlias = Union[Series, list]
PathLike: TypeAlias = Union[Path, str]
