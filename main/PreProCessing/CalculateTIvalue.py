import pandas as pd
import numpy as np
import talib
from talib import abstract
import json



class TIValue():
    def __init__(self, StockID, TI_List, Path) -> None:     
        self.StockID = StockID
        
        self.NON_MA_TYEP_List = TI_List['NON_MA_TYPE']
        self.MA_TYEP_List = TI_List['MA_TYPE']
        
        if __name__ == "__main__":
            self.Path = f"../{Path}/TrainingData"
        else:
            self.Path = f"{Path}/TrainingData"


    def CalculateTIValue(self):
        StockData, TIValueTable = pd.DataFrame(), pd.DataFrame()

        with open(f"{self.Path}/StockData.json") as f:
            StockData = pd.read_json(f)
        

        ColName = []
        
        for TI in self.NON_MA_TYEP_List:
            TIValue = eval(f'abstract.{TI}(StockData)')
            if type(TIValue) == pd.DataFrame:
                [ColName.append(Name.upper()) for Name in list(TIValue.columns)]
            else:
                ColName.append(TI)
                
            TIValueTable = pd.concat([TIValueTable, TIValue], axis=1, ignore_index=True)
             #把算出來的Value 合併到 Table 中
        
        for TI in self.MA_TYEP_List:
            TIValue = eval(f'abstract.{TI[0]}(StockData, timeperiod={TI[1]})')
            ColName.append(f"{TI[0]}{TI[1]}")

            TIValueTable = pd.concat([TIValueTable, TIValue], axis=1)
        TIValueTable.columns = ColName  # Rename 行

        TIValueTable = TIValueTable.reset_index(drop=True)
        TIValueTable.to_json(f"{self.Path}/TIvalue.json", orient='columns')
        




if __name__ == "__main__":
    import cProfile

    with open('../Setting.json') as f1, open('../TI_List.json') as f2:
        Setting = json.load(f1)
        Path = Setting['Path'] + "/" + Setting['StockID']
        TIv = TIValue(Setting['StockID'], json.load(f2), Path)

    TIv.CalculateTIValue()

    # cProfile.run("TIv.CalculateTIValue()")

