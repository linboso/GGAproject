import numpy as np
import pandas as pd
import talib
import package._Function as _pf

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


Stock_Id = "0050.TW"

savepath = f"./stock/{Stock_Id}"
readpath = f"./stock/{Stock_Id}"

start = "2008-06-01" #-1
end = "2010-06-01"  #+1

_pf.StockDataDownload(Stock_Id,start,end)
_pf.getCalculateTIValue()