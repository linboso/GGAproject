from ast import Load
from datetime import date
from tkinter.filedialog import LoadFileDialog

import pandas as pd
import numpy as ny
import json
import yfinance as yf
import talib
from talib import abstract

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
# BIAS > -4.5%
# +DI > -DI
#  

#data = yf.Ticker("0050.TW")
#data = data.history(period='max')
#print(data)
#with open(location, "w") as f:
    #f.write(data.to_json(orient = 'records'))
location = "./0050_tw.json"
data = pd.DataFrame()
with open(location) as f:
    data = pd.DataFrame(json.load(f))

print(data)






