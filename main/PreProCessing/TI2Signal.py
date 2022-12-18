import pandas as pd
import numpy as np
import json

if __name__ == "__main__":
    from Case import Case
else:
    from .Case import Case
    

class TI2Signal():
    def __init__(self, SIGNALMAPOFFSET):
        self.SIGNALMAPOFFSET = SIGNALMAPOFFSET
        pass


    # Signal 單純判斷 buy and sell 的 時間點
    # Table 是有時間順序性質的 ==> Buy 的時間點 必 早於 Sell
    def ProduceSignal(self, Path):
        TI_Format, TIvale = pd.DataFrame(), pd.DataFrame()
        SignalMap, Date = pd.DataFrame(), pd.DataFrame()
        
        if __name__ == "__main__":
            with open(f'./Case/TIformat.json', encoding="utf-8") as f1, open(f'../SignalMap.json', encoding="utf-8") as f2:
                TI_Format = json.load(f1)
                SignalMap = json.load(f2)
        else:
            try:
                with open('./PreProCessing/Case/TIformat.json', encoding="utf-8") as f1, open('./SignalMap.json', encoding="utf-8") as f2:
                    TI_Format = json.load(f1)
                    SignalMap = json.load(f2)
            except:
                print("缺少 TIformat.json or SignalMap.json")
                return 
            
        try:
            with open(f"{Path}/TIvalue.json") as f1, open(f"{Path}/Date.json") as f2:
                TIvale = pd.read_json(f1)
                Date = pd.read_json(f2)

        except:
            print(f"缺少 TIvalue.json or Date.json")
            return 

   
        #確認所有 必要的資料 是否都在

        if __name__ == "__main__":
            ColName = []                # 存 ColName

        Signal, SignalTable = np.empty(len(Date)), np.empty((len(Date), 1)) # 強制要 2D dim

        for TS in SignalMap[:self.SIGNALMAPOFFSET]:                            
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

            SignalTable = np.concatenate((SignalTable, Signal[:, np.newaxis]), axis=1)
   

        for Combination in SignalMap[self.SIGNALMAPOFFSET:]:

            Signal = Case.case1(
                TIvale[Combination[0]], TIvale[Combination[1]]
            ) 
            if __name__ == "__main__":
                ColName.append(f"{Combination[0]}&{Combination[1]}")
                
            SignalTable = np.concatenate((SignalTable, Signal[:, np.newaxis]), axis=1)

        SignalTable = np.delete(SignalTable, 0, 1)        # Del first colunm
        
        if __name__ == "__main__":
            tmp = pd.concat([Date, pd.DataFrame(SignalTable, columns=ColName)], axis=1)
            tmp.to_csv(f"{Path}/SignalforDebug.csv")
            print("已完成交易信號的產生")   

        SignalTable = pd.DataFrame(SignalTable)
        SignalTable.to_json(f"{Path}/Signal.json", orient='columns')

    

    #======================================
    # 這邊用不到
    '''
    def SignleProcessor_ProduceTable(self):
        with open(f"{self.Path}/Signal.json") as f1, open(f"{self.Path}/StockData.json") as f2:
            Signal:pd.DataFrame = pd.read_json(f1)
            Data:pd.DataFrame = pd.read_json(f2)

        Signal_list = Signal.columns
        #把 Signal 的 name 轉成 list

        n = len(Signal)
        TSlen = len(Signal_list)
        Signal = Signal.to_numpy()      # pd.Series to np.array

        Table = np.concatenate(
                    [Data['close'].to_numpy().reshape(n, 1), 
                    np.zeros((n, (TSlen - 1)*(TSlen - 1)), dtype=np.int0) ], 
                        axis=1)

        # Table中 第1行是 Close 收盤價
        # 接下來合併 n * (TSlen-1)^2 大小的 0 矩陣
        #Martix Size = n * [(TSlen-1)^2 + 2]

        ColName:list = ["close"]

        Col = 1
        for buy in range(1, TSlen):
            Buy_Signal:np.array = Signal[:, buy]

            for sell in range(1, TSlen):
                Sell_Signal:np.array = Signal[:, sell]                

                Flag:bool = False                     # True == 有買了
                for i in range(n):
                    if Buy_Signal[i] == 1 and Sell_Signal[i] == -1:
                        # 當同時有 Buy & Sell 的信號時
                        # 要先確認 Flag
                        if Flag:
                            Table[:, Col][i] = -1
                            Flag = False
                            #Flag 狀態改為 尚未買
                        else:
                            Table[:, Col][i] = 1
                            Flag = True
                            #Flag 狀態改為 有買了

                    elif (not Flag) and Buy_Signal[i] == 1:
                        Table[:, Col][i] = 1
                        Flag = True
                        #還沒買 後 完改 True
                    elif Flag and Sell_Signal[i] == -1:
                        Table[:, Col][i] = -1
                        Flag = False

                Col += 1
                ColName.append(f"{Signal_list[buy]}^{Signal_list[sell]}")

        Output = pd.DataFrame(Table, columns=ColName)
        ColName = [] # clean

        Output.to_json(f"{self.Path}/Table.json", orient='columns')

        # if __name__ == "__main__":
        #     Output.to_csv(f"{self.path}/Table.csv")
        # Output.to_json(f"{self.path}/Table.json", orient='columns')
        print("Finished Producing TradingRule Table\r\n")
'''
      
if __name__ == "__main__":
    # 獨立執行 測試用
    import cProfile
    with open('../setting.json') as f:
        ti2s = TI2Signal(json.load(f))
    
    
    ti2s.ProduceSignal()
    # ti2s.ProduceTable() ## Dask
    # cProfile.run("ti2s.ProduceSignal()")
    # cProfile.run("ti2s.ProduceTable()")



