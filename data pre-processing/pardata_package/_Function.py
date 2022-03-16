import pandas as pd
import json
import yfinance as yf
import talib
from talib import abstract
import os

def CheckPath(savepath):
    if not os.path.exists(savepath):
        try:
            #print(savepath)
            os.makedirs(savepath)
            print("Create folder successfully")
            return True
        except:
            print("Failed to create folder")
            return False
    else:
        return True


def StockDataDownload(_stock_id, _start, _end, savepath):
    if CheckPath(savepath):        
        data = yf.download(_stock_id, start = _start, end = _end)
        data.drop(['Adj Close'], axis=1, inplace=True)
        data.columns = ["open","high","low","close","volume"]
        # download Stock-data from yahoo
        # and drop 1 column, "Adj Close" which are no needs to use 
        
        data.to_json(f"{savepath}/stockdata.json", orient='records')
        print(f"Saving {_stock_id} stock data file at {savepath}")
        print(f"Finish downloaded")
        # Save the data as .json Type
        # data name save as {Stock_Id}+{Star_day}+{End_day}.json
    else:
        print("No folder to storge data")




def getCalculateTIValue(_start, _end, _ti_list, readpath, savepath):
    df = pd.DataFrame()
    try:
        if CheckPath(readpath):
            with open(f"{readpath}/stockdata.json") as f:
                df = pd.DataFrame(json.load(f))
            #read stock.json file and convent to DataFrame Type
    except:
        print(f"At {os.getcwd() + savepath} no file name \" {_start}~{_end}/stockdata.json\"")

    _df_with_ti = df
    _Techical_Indicators_list = _ti_list #select n techical indicator

    for _ti in _Techical_Indicators_list:
        try:
            output = eval(f'abstract.{_ti}(df)') #Great Function!
            #print(f" =========={_ti}========== ")
            #print(output)
            output = pd.DataFrame(output)
            output.columns = [_ti] #name it
            _df_with_ti = pd.concat([_df_with_ti, output], axis=1)
            #merge Techical indicator value into main.json file
        except:
            print(f"No techical Inidicator such like \"{_ti}\"")

    #print(_df_with_ti)
    _df_with_ti.to_json(f"{savepath}/techical_indicator.json" ,orient='records') #save file 
    print(f"Saving techical_indicator.json file at {savepath}")

