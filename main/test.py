import json
import os
import pandas as pd
import talib
from talib import abstract

class BackTesting():
    def __init__(self) -> None:
        try:
            with open("./record.json") as f:
                data = json.load(f)
                #print(data)
            self.StockID = data['StockID']  
            self.TrainingPeriod = data['TrainingPeriod']
            self.ValidationPeriod = data['ValidationPeriod']
            self.SL = data['SLTP'][0]
            self.TP = data['SLTP'][1]
            self.Capital = data['Capital']
            self.GTSP = data['GTSP']
            self.Weight = data['Weight']
            self.TradingStrategy = data['TradingStrategy']
            self.SignalMap = data['SignalMap']
            self.Path = f"../data/stock/0050.TW/ValidationData/.json"
        except:
            print("讀取 record.json 失敗")
            print("請確認該檔案是否存在")
        print()
    
    def mapTest(self):
        TIset = set({})
        for i in self.TradingStrategy.values():
            print(self.SignalMap[i[0]])
            print(self.SignalMap[i[1]])
            #TIset.add(j for j in self.SignalMap[i[0]])  
            #TIset.add(j for j in self.SignalMap[i[1]])  
        print(TIset)
        #TI.List = self.SignalMap[self.TradingStrategy]

    def PreBackTesting(self):
        #DownloadData
        print('okay')
        #====================CalculateTIvalue====================
        df = pd.DataFrame()

        try:
            print(f"{self.Path}/StockData.json")
            with open(f"{self.Path}/StockData.json") as f:
                df = pd.read_json(f)
        except:
            print(f"缺失 {self.StockID} 的 StockData.json 的資料")
        

        TIValueTable = pd.DataFrame()
        
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
        
        TIValueTable.to_json(f"{self.Path}/TIvalue.json" ,orient='columns')
        print(f"儲存 TIvalue.json 在 {self.Path}\r\n")
    #TI2signal

if __name__ == '__main__':
    obj = BackTesting()
    obj.mapTest()
    #obj.PreBackTesting()
    #print(obj)