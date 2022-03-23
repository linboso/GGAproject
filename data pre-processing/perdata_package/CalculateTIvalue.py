import os
import json
import pandas as pd
import talib
from talib import abstract

from .BasicFunction import CheckPath, ReadSetting


class TIValue():
    def __init__(self) -> None:
        setting = ReadSetting()
        self.stock_id = setting['StockID']
        self.start = setting['StartDate']
        self.end = setting['EndDate']
        self.ti_list = setting['TechicalIndicator']
        self.savepath = f"stock/{self.stock_id}/{self.start}~{self.end}"
        self.readpath = f"stock/{self.stock_id}/{self.start}~{self.end}"

    def CalculateTIValue(self):
        _df_with_ti = df = pd.DataFrame()
        try:
            if CheckPath(self.readpath):
                with open(f"{self.readpath}/stockdata.json") as f:
                    df = pd.DataFrame(json.load(f))
                with open(f"{self.readpath}/origin_stockdata.json") as f:
                    _df_with_ti = pd.DataFrame(json.load(f))
                #read stock.json file and convent to DataFrame Type
        except:
            print(f"At {os.getcwd() + self.savepath} no file name \" {self.start}~{self.end}/stockdata.json\"\r\n")

        _Techical_Indicators_list = self.ti_list #selected n techical indicator
        _ALL_TI_LIST = talib.get_functions()
 
        for _ti in _Techical_Indicators_list:
            try:
                if not _ti in _ALL_TI_LIST:
                    output = eval(f'abstract.{_ti[:2]}(df, timeperiod = {_ti[2:]})')
                    #Talib not suport MA5, MA10, MAxx so need to use 'timeperiod' attr
                else:
                    output = eval(f'abstract.{_ti}(df)') #Great Function!
                output = pd.DataFrame(output) #turn "output" into DataFrame type
                output.columns = [_ti] if list(output.columns)[0]==0 else [str(i).upper() for i in list(output.columns)] #name it
                _df_with_ti = pd.concat([_df_with_ti, output], axis=1)
                #merge Techical indicator value into main.json file
            except:
                print(f"--> No such techical Inidicator like \"{_ti}\"\r\n")
        #print(_df_with_ti)
        _df_with_ti.to_json(f"{self.savepath}/techical_indicator.json" ,orient='records') #save file 
        print(f"Saving techical_indicator.json file at {self.savepath}\r\n")


    def getTIValue(self):
        table = pd.DataFrame()
        with open(f"{self.savepath}/techical_indicator.json", 'r') as f:
            table = pd.DataFrame(json.load(f))
        return table

