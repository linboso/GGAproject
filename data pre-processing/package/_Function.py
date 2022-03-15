from cgi import print_arguments
from email.errors import CharsetError
from importlib.resources import path
from tabnanny import check
from turtle import onkey

import os
import pandas as pd
import json
import yfinance as yf
import talib
from talib import abstract


# ["SMA","RSI","MACD","CCI","MACDEXT","PLUS_DI ", "MINUS_DI"]


Stock_Id = "0"

savepath = os.getcwd() + f"\\stock\\{Stock_Id}"
readpath = os.getcwd() + f"\\stock\\{Stock_Id}"

start = "2008-06-01" #-1
end = "2010-06-01"  #+1
_ti_list = ["CCI","RSI"]

try:
    with open("../setting.json") as f:
        setting = json.load(f)
        Stock_Id = setting.StockID
except:
    print("Missing setting.json")


class _Fuction:
    def __init__(self) -> None:
        print("import successed")




def CheckPath():
    if not os.path.exists(savepath):
        try:
            print(savepath)
            os.makedirs(savepath)
            print("Create folder successfully")
            return True
        except:
            print("Failed to create folder")
            return False
    else:
        return True
        

def StockDataDownload(Stock_Id, start, end):
    if CheckPath():
        data = yf.download(Stock_Id, start=start, end=end)
        data.drop(['Adj Close'], axis=1, inplace=True)
        data.columns = ["open","high","low","close","volume"]
        # download Stock-data from yahoo
        # and drop 1 column, "Adj Close" which are no needs to use 
        print(f"Saving file at {savepath}")
        data.to_json(f"{savepath}/{start}+{end}.json", orient='records')
        print(f"Done")
        # Save the data as .json Type
        # data name save as {Stock_Id}+{Star_day}+{End_day}.json
    else:
        print("No folder to storge data")



def getCalculateTIValue(readpath=readpath, _ti_list=_ti_list):
    
    df = pd.DataFrame()
    try:
        if CheckPath():
            with open(f"{readpath}/{start}+{end}.json") as f:
                df = pd.DataFrame(json.load(f))
            #read stock.json file and convent to DataFrame Type
    except:
        print(f"No file name \" {savepath}/{start}+{end}.json\"")

    _df_with_ti = df
    _Techical_Indicators_list = _ti_list #select n techical indicator

    for _ti in _Techical_Indicators_list:
        try:
            output = eval(f'abstract.{_ti}(df)') #Great Function!
            #print(f" =========={_ti}========== ")
            #print(output)
            output = pd.DataFrame(output)
            output.columns = [_ti.lower()] #name it
            _df_with_ti = pd.concat([_df_with_ti, output], axis=1)
            #merge Techical indicator value into main.json file
        except:
            print(f"{_ti} error")

    #print(_df_with_ti)
    _df_with_ti.to_json(f"{savepath}/TI_{start}+{end}.json" ,orient='records') #save file 
    print("done")

