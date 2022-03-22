
from asyncore import read
import os
from re import T
import pandas as pd
import json
from talib import abstract 

_stock_id = "0050.TW"
_start = "2008-06-01"
_end = "2010-06-01"

savepath = f"\\stock\\{_stock_id}"
readpath = f"/stock/{_stock_id}/{_start}~{_end}"


print("Greeeeeeeeeeeee")
with open(f"../{readpath}/stockdata.json") as f:
    data = pd.DataFrame(json.load(f))



_df_with_ti = pd.DataFrame()
for _ti in ["MACD", "CCI", "RSI"]:
    try:
        output = eval(f'abstract.{_ti}(data)') #Great Function!
        # output = abstract.MACD(data)
        # output = pd.DataFrame(output)

        # output.columns = [_ti] #name it
        output = pd.DataFrame(output)
        # print(output)
        # print(list(output.columns))
        output.columns = [_ti] if list(output.columns)[0]==0 else [str(i).upper() for i in list(output.columns)]
        _df_with_ti = pd.concat([_df_with_ti, output], axis=1)
        print("----------------------------")
    except:
        print(f"--> No such techical Inidicator like \"{_ti}\"\r\n")

print(_df_with_ti)
