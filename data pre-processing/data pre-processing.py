import numpy as np
import pandas as pd
import talib
from pardata_package import _Function as _pk
from pardata_package import convert_signal

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
_end = "2010-06-01"
_ti_list = ["MACD","ADX", "CCI", "MA5","MA20","RSI"]
# _ti_list = talib.get_functions()


savepath = f"stock/{_stock_id}/{_start}~{_end}"
readpath = f"stock/{_stock_id}/{_start}~{_end}"

k = _pk.ReadSetting()
print(">>> " , k)
#_pk.StockDataDownload(_stock_id, _start, _end, savepath)
_pk.getCalculateTIValue(_start, _end, _ti_list, readpath, savepath)


#TI_signal table
TI_signal = _pk.getCalculateTIValue(_start, _end, _ti_list, readpath, savepath)
print(TI_signal)
TI_signal = pd.concat([TI_signal,convert_signal.RSI_signal(TI_signal["RSI"])],axis=1)
print(TI_signal)#after add RSI_signal
TI_signal = pd.concat([TI_signal,convert_signal.MA_signal(TI_signal["MA5"],TI_signal["MA20"])],axis=1)
print(TI_signal)#after add MA5&MA20 signal
TI_signal = pd.concat([TI_signal,convert_signal.combine_signal(TI_signal["RSI_signal"],TI_signal["MA_signal"])],axis=1)
print(TI_signal)#after add combine_signal

TI_signal.to_json(f"{savepath}/test.json" ,orient='records') #save file 
# save the test file
