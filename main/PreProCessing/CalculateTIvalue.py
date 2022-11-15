
import pandas as pd
import talib
from talib import abstract



class TIValue():
    def __init__(self, Setting) -> None:
        setting = Setting
        
        self.stock_id = setting['StockID']
        self.start = setting['TrainingPeriod']['StartDate']
        self.end = setting['TrainingPeriod']['EndDate']
        # self.TI_List = setting['TechnicalIndicator'] # 自選
        self.TI_List = ['WMA5', 'WMA10', 'WMA20', 'WMA60', 'TRIMA5', 'TRIMA10', 'TRIMA20', 'TRIMA60', 
                        'TEMA5', 'TEMA10', 'TEMA20', 'TEMA60', 'SMA5', 'SMA10', 'SMA20', 'SMA60', 
                        'MAMA', 'MA5', 'MA10', 'MA20', 'MA60', 'KAMA5', 'KAMA10', 'KAMA20', 
                        'KAMA60', 'EMA5', 'EMA10', 'EMA20', 'EMA60', 'DEMA5', 'DEMA10', 'DEMA20', 'DEMA60', 'TRIX', 
                        'PLUS_DI', 'PLUS_DM', 'RSI', 'WILLR', 'ULTOSC', 'MOM', 'BOP', 'APO', 'MFI', 'AROONOSC', 'CCI', 
                        'CMO', 'ROC', 'PPO', 'MACD', 'STOCH', 'ADX', 'ADXR']
        

        if __name__ == "__main__":
            self.path = f"../{setting['Path']}/{setting['StockID']}/TrainingData"
        else:
            self.path = f"{setting['Path']}/{setting['StockID']}/TrainingData"

    def CalculateTIValue(self):
        df = pd.DataFrame()

        try:
            with open(f"{self.path}/StockData.json") as f:
                df = pd.read_json(f)

        except:
            print(f"缺失 {self.stock_id} 的 StockData.json 的資料")
        
        TIValueTable = pd.DataFrame()
        # ALL_TI_List = talib.get_functions()
        
        ColName = []
        for TI in self.TI_List:
            try:
                if TI[-2:].isdigit():                               #如果 最後兩位 是數字
                    TIValue:pd.DataFrame = eval(f'abstract.{TI[:-2]}(df, timeperiod={TI[-2:]})')
                    ColName.append(TI)
                    
                elif not TI[-2].isdigit() and TI[-1].isdigit():     #如果 最後一位 是數字
                    TIValue:pd.DataFrame = eval(f'abstract.{TI[:-1]}(df, timeperiod={TI[-1]})')
                    ColName.append(TI)

                else:
                    TIValue:pd.DataFrame = eval(f'abstract.{TI}(df)') 
                    if type(TIValue) == pd.DataFrame:
                        [ColName.append(Name.upper()) for Name in list(TIValue.columns)]
                    else:
                        ColName.append(f"{TI}")
            except:

                print(f"沒有此 {TI} 技術指標\r\n")
                continue

            TIValueTable = pd.concat([TIValueTable, TIValue], axis=1)
            #把算出來的Value 合併到 Table 中
        # print(ColName)
        # print(TIValueTable)
        TIValueTable.columns = ColName
        # Rename 行

        print(f"計算出來的 指標數值有: {list(TIValueTable.columns)}")
        # print(TIValueTable.head(5))
        
        TIValueTable.to_json(f"{self.path}/TIvalue.json" ,orient='records')
        print(f"儲存 TIvalue.json 在 {self.path}\r\n")
        



    def getTIValue(self):
        table = pd.DataFrame()
        with open(f"{self.path}/TIvalue.json", 'r') as f:
            table = pd.read_json(f)

        return table




if __name__ == "__main__":
    # 獨立執行 測試用
    import json
    import cProfile

    with open('../setting.json') as f:
        TIv = TIValue(json.load(f))

    TIv.CalculateTIValue()

    # print(talib.get_functions())
    # cProfile.run("TIv.CalculateTIValue()")

