
import os
import pandas as pd
import json

_stock_id = ""

savepath = os.getcwd() + f"\\stock\\{_stock_id}"
readpath = os.getcwd() + f"\\stock\\{_stock_id}"

_start = "2008-06-01" #-1
_end = "2010-06-01"  #+1
_ti_list = ["CCI","RSI"]


try:
    with open("../setting.json") as f:
        setting = pd.DataFrame(json.load(f))
        _stock_id = setting["StockID"].values[0]
        _start = setting["StartDate"].values[0]
        _end = setting["EndDate"].values[0]
        _ti_list = setting["TechicalIndicator"].values[0]

except:
    init_setting = {
        "StockID":["0050.TW"],
        "StartDate":["2008-06-01"],
        "EndDate":["2009-06-01"],
        "TechicalIndicator":[["MA", "RSI"]]
    }
    df = pd.DataFrame(init_setting)
    df.to_json("../setting.json")
    print("...Created setting.json")


