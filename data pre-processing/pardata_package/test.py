import pandas as pd
import json
from talib import abstract 
import talib

_stock_id = "0050.TW"
_start = "2008-06-01"
_end = "2010-06-01"

savepath = f"\\stock\\{_stock_id}"
readpath = f"/stock/{_stock_id}/{_start}~{_end}"


print("Greeeeeeeeeeeee")
with open(f"../{readpath}/stockdata.json") as f:
    data = pd.DataFrame(json.load(f))

_df_with_ti = pd.DataFrame()
_ALL_TI_LIST = talib.get_functions()
for _ti in ["MA5","MA20","MACD","RSI"]:
    try:
        if(not _ti in _ALL_TI_LIST):
            print(_ti[2:])
            output = eval(f'abstract.{_ti[:2]}(data, timeperiod = {_ti[2:]})')
        else:
            output = eval(f'abstract.{_ti}(data)') #Great Function!
        output = pd.DataFrame(output)
        output.columns = [_ti] if list(output.columns)[0]==0 else [str(i).upper() for i in list(output.columns)]
        _df_with_ti = pd.concat([_df_with_ti, output], axis=1)
        print("----------------------------")
    except:
        print(f"--> No such techical Inidicator like \"{_ti}\"\r\n")

print(_df_with_ti)
