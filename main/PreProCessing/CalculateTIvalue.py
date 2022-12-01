import pandas as pd
import numpy as np
import talib
from talib import abstract
import json



class TIValue():
    def __init__(self, Setting, TI_List) -> None:     
        self.StockID = Setting['StockID']
        # self.TI_List = setting['TechnicalIndicator'] # 自選
        self.NON_MA_TYEP_List = TI_List['NON_MA_TYPE']
        self.MA_TYEP_List = TI_List['MA_TYPE']
        

        if __name__ == "__main__":
            self.Path = f"../{Setting['Path']}/{Setting['StockID']}/TrainingData"
        else:
            self.Path = f"{Setting['Path']}/{Setting['StockID']}/TrainingData"

    def CalculateTIValue(self):
        df = pd.DataFrame()

        try:
            with open(f"{self.Path}/StockData.json") as f:
                df = pd.read_json(f)
        except:
            print(f"缺少 {self.StockID} 的 StockData.json 的資料")
            return
        
        TIValueTable = pd.DataFrame()

        ColName = []
        
        for TI in self.NON_MA_TYEP_List:
            TIValue = eval(f'abstract.{TI}(df)')
            if type(TIValue) == pd.DataFrame:
                [ColName.append(Name.upper()) for Name in list(TIValue.columns)]
            else:
                ColName.append(TI)
                
            TIValueTable = pd.concat([TIValueTable, TIValue], axis=1)
             #把算出來的Value 合併到 Table 中
            
        for TI in self.MA_TYEP_List:
            TIValue = eval(f'abstract.{TI[0]}(df, timeperiod={TI[1]})')
            ColName.append(f"{TI[0]}{TI[1]}")

            TIValueTable = pd.concat([TIValueTable, TIValue], axis=1)
           

        TIValueTable.columns = ColName
        # Rename 行


        
        TIValueTable.to_json(f"{self.Path}/TIvalue.json", orient='columns')
        
        # print(f"計算出來的 指標數值有: {list(TIValueTable.columns)}")
        # print(f"儲存 TIvalue.json 在 {self.Path}\r\n")
        



    def getTIValue(self):
        table = pd.DataFrame()
        with open(f"{self.Path}/TIvalue.json", 'r') as f:
            table = pd.read_json(f)

        return table




if __name__ == "__main__":
    # 獨立執行 測試用
    import cProfile

    with open('../setting.json') as f1, open('../TI_List.json') as f2:
        TIv = TIValue(json.load(f1), json.load(f2))

    TIv.CalculateTIValue()

    # print(talib.get_functions())
    # cProfile.run("TIv.CalculateTIValue()")

