import os
import json
import pandas as pd
import talib
from talib import abstract

from .SettingFile import SettingFile





class TIValue():
    def __init__(self) -> None:
        setting = SettingFile()
        setting = setting.Read()
        self.stock_id = setting['StockID']
        self.start = setting['StartDate']
        self.end = setting['EndDate']
        self.ti_list = setting['TechnicalIndicator']
        self.savepath = f"stock/{self.stock_id}/{self.start}~{self.end}"
        self.readpath = f"stock/{self.stock_id}/{self.start}~{self.end}"

    def CalculateTIValue(self):
        _df_with_ti = df = pd.DataFrame()
        try:
            if not os.path.exists(self.readpath):
                print(f"No such {self.stock_id} info & data")
                print("要先下載資料再作運算")
            else:
                with open(f"{self.readpath}/StockData.json") as f:
                    df = pd.DataFrame(json.load(f))
                # with open(f"{self.readpath}/origin_stockdata.json") as f:
                #     _df_with_ti = pd.DataFrame(json.load(f))

            #read stock.json file and convent to DataFrame Type
        except:
            print(f"At {os.getcwd() + self.savepath} no file name \" {self.start}~{self.end}/StockData.json\"\r\n")

        
        _ALL_TI_LIST = talib.get_functions()
 
        for _ti in self.ti_list: #selected n techical indicator
            try:
                if not _ti in _ALL_TI_LIST:
                    output = eval(f'abstract.{_ti[:2]}(df, timeperiod = {_ti[2:]})')
                    #Talib not suport MA5, MA10, MAxx so need to use 'timeperiod' attr
                else:
                    output = eval(f'abstract.{_ti}(df)') #eval is great Function!
                output = pd.DataFrame(output) #turn "output" into DataFrame type
                output.columns = [_ti] if list(output.columns)[0]==0 else [str(i).upper() for i in list(output.columns)] #name it
                _df_with_ti = pd.concat([_df_with_ti, output], axis=1)
                #merge Techical indicator value into main.json file
            except:
                print(f"--> No such technical Inidicator like \"{_ti}\"\r\n")
        #print(_df_with_ti)
        _df_with_ti.to_json(f"{self.savepath}/TIvalue.json" ,orient='records') #save file 
        print(f"Saving TIvalue.json file at {self.savepath}\r\n")


    def getTIValue(self):
        table = pd.DataFrame()
        with open(f"{self.savepath}/TIvalue.json", 'r') as f:
            table = pd.DataFrame(json.load(f))
        return table

