from importlib.resources import Package
import numpy as np
import pandas as pd
import talib
from pardata_package import _Function as _pk

#
# 股票代號 = ticker symbol
# Date, open, high, low , close, volumn
# ma5 > ma20 
# ma5 < ma20 
# rsi > 30 
# wms%r < 80
# MOM > 0
# PSY > 25
# CCI > -100
# DIF > MACD(DEM) 
# BIAS > -4.5% Talib沒有
# +DI > -DI  => PLUS_DI & MINUS_DI 
#  
_stock_id = "0050.TW"
_start = "2008-06-01"
_end = "2015-06-01"
_ti_list = ["RSI", "CCI", "MA","CMO","ADX", "RF"]

savepath = f"stock/{_stock_id}/{_start}~{_end}"
readpath = f"stock/{_stock_id}/{_start}~{_end}"

_pk.StockDataDownload(_stock_id, _start, _end, savepath)
_pk.getCalculateTIValue(_start, _end, _ti_list, readpath, savepath)