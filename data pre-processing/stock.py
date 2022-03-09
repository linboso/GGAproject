from ast import Load
from tkinter.filedialog import LoadFileDialog
import pandas as pd
import numpy as ny
import json


#
# 股票代號 = ticker symbol
# Date, open, high, low , close, CCI, ~~signal

"""
class Stock:
    def __init__(self, _Date, _OpeningPrice, _HighPrice, _LowPrice, _ClosePrice, _CCI) -> None:
        self._Date = _Date  
        self._OpingPrice = _OpeningPrice
        self._HighPrice = _HighPrice
        self._LowPrice = _LowPrice
        self._ClosePrice = _ClosePrice
        self._CCI = _CCI
"""

loaction = "../Stock.json"
with open(loaction) as f:
    data = pd.DataFrame(json.load(f))
    print(data)
