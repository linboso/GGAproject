from asyncore import read
import pandas as pd
import json
import yfinance as yf
import talib
from talib import abstract
import os

def ReadSetting():
    try:
        with open("../setting.json") as f:
            setting = json.load(f)
            print("============= Setting Data =============")
            print("Stock ID: ", setting["StockID"])
            print("Start Date: ", setting["StartDate"])
            print("End Date: ", setting["EndDate"])
            print("Techical Indicator: ", setting["TechicalIndicator"])
            print("========================================")
        return setting
    except:
        init_setting = {
            "StockID":"0050.TW",
            "StartDate":"2008-06-01",
            "EndDate":"2009-06-01",
            "TechicalIndicator":["MA", "RSI"] } #init setting format
        with open("../setting.json", "w") as f:
            json.dump(init_setting, f) # save as .json file
        print("...Create setting.json at \"../setting.json\"")
        
        print("Reloading...")
        return ReadSetting() #Reload data


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
        print(f"Finish downloaded")
        data.drop(['Adj Close'], axis=1, inplace=True)
        data.columns = ["open","high","low","close","volume"]
        # download Stock-data from yahoo
        # and drop 1 column, "Adj Close" which are no needs to use 
        data.to_json(f"{savepath}/stockdata.json", orient='records')
        print(f"Saving {_stock_id} stock data file at {savepath} \r\n")
        # Save the data as .json Type
        # data name save as {Stock_Id}+{Star_day}+{End_day}.json
        data = pd.concat([pd.DataFrame(data.index).reset_index(drop=True), data.reset_index(drop=True)], axis=1)
        data.to_json(f"{savepath}/origin_stockdata.json", orient='records')
        # Save another data but with "Date"
    else:
        print("No folder to storge data\r\n")


def getCalculateTIValue(_start, _end, _ti_list, readpath, savepath):
    _df_with_ti = df = pd.DataFrame()
    try:
        if CheckPath(readpath):
            with open(f"{readpath}/stockdata.json") as f:
                df = pd.DataFrame(json.load(f))
            with open(f"{readpath}/origin_stockdata.json") as f:
                _df_with_ti = pd.DataFrame(json.load(f))
            #read stock.json file and convent to DataFrame Type
    except:
        print(f"At {os.getcwd() + savepath} no file name \" {_start}~{_end}/stockdata.json\"\r\n")

    _Techical_Indicators_list = _ti_list #select n techical indicator

    for _ti in _Techical_Indicators_list:
        try:
            output = eval(f'abstract.{_ti}(df)') #Great Function!
            #print(f" =========={_ti}========== ")
            #print(output)
            output = pd.DataFrame(output)
            output.columns = [_ti] if list(output.columns)[0]==0 else [str(i).upper() for i in list(output.columns)] #name it
            _df_with_ti = pd.concat([_df_with_ti, output], axis=1)
            #print(_df_with_ti)
            #merge Techical indicator value into main.json file
        except:
            print(f"--> No such techical Inidicator like \"{_ti}\"\r\n")

    #print(_df_with_ti)
    _df_with_ti.to_json(f"{savepath}/techical_indicator.json" ,orient='records') #save file 
    print(f"Saving techical_indicator.json file at {savepath}\r\n")

