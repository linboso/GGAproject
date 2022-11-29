import json
import os
import pandas as pd
import numpy as np
import talib
from talib import abstract


if __name__ == "__main__":
    from Case import Case
else:
    from .Case import Case

class BackTesting():
    def __init__(self) -> None:
        try:
            with open("./BackTestingBlock.json") as f:
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
            self.TI_List = []
            self.TIpair = []
            self.SignalMap = data['SignalMap']
            self.Path = f"../data/stock/0050.TW/ValidationData"
        except:
            print("讀取 record.json 失敗")
            print("請確認該檔案是否存在")
        print()
    
    def mapTest(self):
        TI_List = set()
        for i in self.TradingStrategy.values():
            if isinstance(self.SignalMap[i[0]], str):
                TI_List.add(self.SignalMap[i[0]])
            else:
                for j in self.SignalMap[i[0]]:
                    TI_List.add(j) 
            if isinstance(self.SignalMap[i[1]], str):
                TI_List.add(self.SignalMap[i[1]])
            else:
                for j in self.SignalMap[i[1]]:
                    TI_List.add(j) 
        print(TI_List)
        #TI.List = self.SignalMap[self.TradingStrategy]

    def PreBackTesting(self):
        #DownloadData
        self.__CalculateTIvalue()
        #self.__TI2signal()
    def __CalculateTIvalue(self):
        #====================CalculateTIvalue====================
        TI_List = set()
        TIpair = []
        for i in self.TradingStrategy.values():
            #必須分為"NON_MA_TYPE" or "MA_TYPE"

            TIpair.append(self.SignalMap[i[0]])
            TIpair.append(self.SignalMap[i[1]])
            if isinstance(self.SignalMap[i[0]], str):
                TI_List.add(self.SignalMap[i[0]])
            else:
                for j in self.SignalMap[i[0]]:
                    TI_List.add(j) 
            if isinstance(self.SignalMap[i[1]], str):
                TI_List.add(self.SignalMap[i[1]])
            else:
                for j in self.SignalMap[i[1]]:
                    TI_List.add(j) 
        self.TIpair = TIpair
        self.TI_List = list(TI_List)
        df = pd.DataFrame()

        try:
            print(f"{self.Path}/StockData.json")
            with open(f"{self.Path}/StockData.json") as f:
                df = pd.read_json(f)
        except:
            print(f"缺失 {self.StockID} 的 StockData.json 的資料")
        

        TIValueTable = pd.DataFrame()
        
        ColName = []
        for TI in TI_List:
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

    def __TI2signal(self):
        
        TI_Format, TIvale = pd.DataFrame(), pd.DataFrame()
        SignalMap, Date = pd.DataFrame(), pd.DataFrame()

        if __name__ == "__main__":
            with open(f'./PreProCessing/Case/TIformat.json', 'r', encoding="utf-8") as f:
                TI_Format = pd.read_json(f)
        else:
            try:
                with open('./PreProCessing/Case/TIformat.json', 'r', encoding="utf-8") as f:
                    TI_Format = pd.read_json(f)
            except:
                print("缺失 TIformat.json \t位置: ./PreProCessing/Case/TIformat.json")
                return 

        # ================================================================================
        if __name__ == "__main__":
            print("內部")
            with open(f'./SignalMap.json', 'r', encoding="utf-8") as f:
                SignalMap = json.load(f)
        else:
            print("外部")
            try:
                with open('./SignalMap.json', 'r', encoding="utf-8") as f:        
                    SignalMap = pd.read_json(f)
            except:
                print("缺失 SignalMap.json")
                return 
        
        # ================================================================================
        try:
            with open(f"{self.Path}/TIvalue.json") as f:
                TIvale = pd.read_json(f)

        except:
            print(f"缺失 TIvalue.json 檔 \t位置: {self.Path}/TIvalue.json")
            return 

        try:
            with open(f"{self.Path}/Date.json") as f:
                Date = pd.read_json(f)
        except:
            print(f"缺失 Date.json 檔 \t位置: {self.Path}/Date.json")
            return 

        # return
   
        #確認所有 必要的資料 是否都在

        if __name__ == "__main__":
            ColName = []                # 存 ColName

        Signal, Data = np.empty(len(Date)), np.empty((len(Date), 1)) # 強制要 2D dim

        for TS in self.TIpair:                            
            case = TI_Format[TS]['Case']
            Iuput = TI_Format[TS]["InputArray"]
            if case == "1":
                Signal = Case.case1(
                    TIvale[Iuput['ti1']],    # Get ti 1 Value
                    TIvale[Iuput['ti2']]     # Get ti 2 Value
                )

            elif case == "2":
                Signal = Case.case2(
                    TIvale[Iuput['ti1']],    # Get ti 1 Value
                    Iuput['C1'],             # C1
                    Iuput['C2']              # C2
                )

            elif case == "3":
                Signal = Case.case3(
                    TIvale[Iuput['ti1']],    # Get ti 1 Value
                    TIvale[Iuput['ti2']],    # Get ti 2 Value
                    Iuput['C1'],             # C1
                    Iuput['C2']              # C2
                )

            elif case == "4":
                Signal = Case.case4(
                    TIvale[Iuput['ti1']],    # Get ti 1 Value
                    TIvale[Iuput['ti2']],    # Get ti 2 Value
                    Iuput['C1'],             # C1
                    Iuput['C2']              # C2
                )

            elif case == "5":
                Signal = Case.case5(
                    TIvale[Iuput['ti1']],    # Get ti 1 Value
                    TIvale[Iuput['ti2']],    # Get ti 2 Value
                    TIvale[Iuput['ti3']],    # Get ti 3 Value
                    Iuput['C1']              # C1
                )

            elif case == "6":
                Signal = Case.case6(
                    TIvale[Iuput['ti1']],    # Get ti 1 Value
                    TIvale[Iuput['ti2']],    # Get ti 2 Value
                    TIvale[Iuput['ti3']],    # Get ti 3 Value
                    TIvale[Iuput['ti4']]     # Get ti 4 Value
                )
            
            if __name__ == "__main__":
                ColName.append(TS)               

            Data = np.concatenate((Data, Signal[:, np.newaxis]), axis=1)
    

        for Combination in SignalMap["MA_TYPE"]:

            Signal = Case.case1(
                TIvale[Combination[0]],
                TIvale[Combination[1]]
            ) 
            if __name__ == "__main__":
                ColName.append(f"{Combination[0]}&{Combination[1]}")
            Data = np.concatenate((Data, Signal[:, np.newaxis]), axis=1)

        Data = np.delete(Data, 0, 1)        # Del 多餘的 first colunm
        
        if __name__ == "__main__":
            tmp = pd.concat([Date, pd.DataFrame(Data, columns=ColName)], axis=1)
            tmp.to_csv(f"{self.Path}/SignalforDebug.csv")
            print("已完成交易信號的產生")   
    
        Date = pd.concat([Date, pd.DataFrame(Data)], axis=1)
        Date.to_json(f"{self.Path}/Signal.json", orient='columns')



if __name__ == '__main__':
    obj = BackTesting()
    #obj.mapTest()
    obj.PreBackTesting()
    #print(obj)