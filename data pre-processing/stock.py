

from importlib.resources import path
from turtle import onkey
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
# BIAS > -4.5% Talib沒有
# +DI > -DI  => PLUS_DI & MINUS_DI 
#  

savepath = "."
Stock_Id = "0050.TW"
start = "2008-06-01" #-1
end = "2008-12-02"  #+1

'''

data = yf.download(Stock_Id, start=start, end=end)
data.drop(['Adj Close'], axis=1, inplace=True)
data.columns = ["open","high","low","close","volume"]
# download Stock-data from yahoo
# and drop 1 column, "Adj Close" which are no needs to use 

data.to_json(f"{savepath}/{Stock_Id}+{start}+{end}.json", orient='records')

# Save the data as .json Type
# data name save as {Stock_Id}+{Star_day}+{End_day}.json
'''



df = pd.DataFrame()
with open(f"{savepath}/{Stock_Id}+{start}+{end}.json") as f:
    df = pd.DataFrame(json.load(f))
#read stock.json file and convent to DataFrame Type


_df_with_ti = df
#_Techical_Indicators = ["SMA","RSI","MACD","CCI","MACDEXT","PLUS_DI ", "MINUS_DI"]
_Techical_Indicators = ["CCI","RSI"]


for _ti in _Techical_Indicators:
    try:
        output = eval(f'abstract.{_ti}(df)')
        #print(f" =========={_ti}========== ")
        output = pd.DataFrame(output)
        output.columns = [_ti.lower()]
        print(output)
        _df_with_ti = pd.concat([_df_with_ti, output])
        
    except:
        print(f"{_ti} error")

print(df)
print(_df_with_ti)
_df_with_ti.to_json(f"{savepath}/TI_{Stock_Id}+{start}+{end}.json" ,orient='records')




print("done")

