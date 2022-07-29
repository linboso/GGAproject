import os

import pandas as pd
import talib
from talib import abstract



class TIValue():
    def __init__(self, Setting) -> None:
        setting = Setting
        
        self.stock_id = setting['StockID']
        self.Tstart = setting['TrainingPeriod']['StartDate']
        self.Tend = setting['TrainingPeriod']['EndDate']

        self.Vstart = setting['ValidationPeriod']['StartDate']
        self.Vend = setting['ValidationPeriod']['EndDate']
        
        self.ti_list = setting['TechnicalIndicator']
        self.path = f"{setting['Path']}/{setting['StockID']}"
        #self.path = f"{setting['Path']}/{setting['StockID']}/TraningData"



    def CalculateTIValue(self):
        df = pd.DataFrame()
        try:
            if not os.path.exists(self.path):
                print(f"No such {self.stock_id} info & data")
                print("要先下載資料再作運算")
            else:
                with open(f"{self.path}/TraningData/StockData.json") as f:
                    df = pd.read_json(f)
 

            #read stock.json file and convent to DataFrame Type
        except:
            print(f"At {os.getcwd() + self.path}/ValidationData no file name \" {self.path}/TraningData/StockData.json\"\r\n")

        _df_with_ti = pd.DataFrame()
        _ALL_TI_LIST = talib.get_functions()
 
        for _ti in self.ti_list: #selected n techical indicator
            try:
                # ========================= need improve
                if not _ti in _ALL_TI_LIST:
                    for k in range(len(_ti)):
                        if _ti[k].isdigit() == True: # 這邊需要改
                            break
                    output = eval(f'abstract.{_ti[:k]}(df, timeperiod = {_ti[k:]})')
                    #Talib not suport MA5, MA10, MAxx so need to use 'timeperiod' attr
                else:
                    output = eval(f'abstract.{_ti}(df)') #eval is great Function!
                output = pd.DataFrame(output) #turn "output" into DataFrame type
                output.columns = [_ti] if list(output.columns)[0]==0 else [str(i).upper() for i in list(output.columns)] #name it
                _df_with_ti = pd.concat([_df_with_ti, output], axis=1)
                #merge Techical indicator value into main.json file
            except:
                print(f"--> No such technical Inidicator like \"{_ti}\"\r\n")
        print(f"計算出來的 數值有: {list(_df_with_ti.columns)}")
        try:
            _df_with_ti.to_json(f"{self.path}/TraningData/TIvalue.json" ,orient='records') #save file 
            print(f"Saving TIvalue.json file at {self.path}/TraningData\r\n")
        except:
            print(f"Saving File Faild")


        #===================================================================================
        #ValidationData part
        try:
            if not os.path.exists(self.path):
                print(f"No such {self.stock_id} info & data")
                print("要先下載資料再作運算")
            else:
                with open(f"{self.path}/ValidationData/StockData.json") as f:
                    df = pd.read_json(f)
 

            #read stock.json file and convent to DataFrame Type
        except:
            print(f"At {os.getcwd() + self.path}/ValidationData no file name \" {self.path}/ValidationData/StockData.json\"\r\n")

        _df_with_ti = pd.DataFrame()
        _ALL_TI_LIST = talib.get_functions()
 
        for _ti in self.ti_list: #selected n techical indicator
            try:
                # ========================= need improve
                if not _ti in _ALL_TI_LIST:
                    for k in range(len(_ti)):
                        if _ti[k].isdigit() == True: # 這邊需要改
                            break
                    output = eval(f'abstract.{_ti[:k]}(df, timeperiod = {_ti[k:]})')
                    #Talib not suport MA5, MA10, MAxx so need to use 'timeperiod' attr
                else:
                    output = eval(f'abstract.{_ti}(df)') #eval is great Function!
                output = pd.DataFrame(output) #turn "output" into DataFrame type
                output.columns = [_ti] if list(output.columns)[0]==0 else [str(i).upper() for i in list(output.columns)] #name it
                _df_with_ti = pd.concat([_df_with_ti, output], axis=1)
                #merge Techical indicator value into main.json file
            except:
                print(f"--> No such technical Inidicator like \"{_ti}\"\r\n")
        print(f"計算出來的 數值有: {list(_df_with_ti.columns)}")
        try:
            _df_with_ti.to_json(f"{self.path}/ValidationData/TIvalue.json" ,orient='records') #save file 
            print(f"Saving TIvalue.json file at {self.path}/ValidationData\r\n")
        except:
            print(f"Saving File Faild")






    def getTIValue(self):
        table = pd.DataFrame()
        with open(f"{self.path}/TIvalue.json", 'r') as f:
            table = pd.read_json(f)
        return table

