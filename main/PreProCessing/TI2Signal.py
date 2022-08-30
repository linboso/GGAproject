import pandas as pd
import numpy as np

if __name__ == "__main__":
    from Case import Case
else:
    from .Case import Case
    


class TI2Signal():
    def __init__(self, Setting) -> None:
        self.stock_id = Setting['StockID']
        self.start = Setting['TrainingPeriod']['StartDate']
        self.end = Setting['TrainingPeriod']['EndDate']
        self.ti_list = Setting['TechnicalIndicator']

        if __name__ == "__main__":
            self.path = f"../{Setting['Path']}/{Setting['StockID']}/TrainingData"
        else:
            self.path = f"{Setting['Path']}/{Setting['StockID']}/TrainingData"



    def ProduceSignal(self):
        ti_format, TIvale ,data = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        if __name__ == "__main__":
            with open(f'./Case/TIformat1.json', 'r', encoding="utf-8") as f:
                ti_format = pd.read_json(f)
        else:
            try:
                with open('./PreProCessing/Case/TIformat.json', 'r', encoding="utf-8") as f:
                    ti_format = pd.read_json(f)
            except:
                print("缺失 TIformat.json \t位置: ./PreProCessing/Case/TIformat.json")
                return 

        try:
            with open(f"{self.path}/TIvalue.json") as f:
                TIvale = pd.read_json(f)
        except:
            print(f"缺失 TIvalue.json 檔 \t位置: {self.path}/TIvalue.json")
            return 

        try:
            with open(f"{self.path}/Date.json") as f:
                data = pd.read_json(f)
        except:
            print(f"缺失 Date.json 檔 \t位置: {self.path}/Date.json")
            return 

        
        #確認所有 必要的資料 是否都在
        signal, MovingAvg = [], []

        for TS in self.ti_list: # 有被選擇的 TI list 
            
            # --- Moving Average Tpye 的指標 要另外處理 ---
            if TS[-2:].isdigit():                               #如果 最後兩位 是數字
                MovingAvg.append((int(TS[-2:]), TS))
            elif not TS[-2].isdigit() and TS[-1].isdigit():     #如果 最後一位 是數字
                MovingAvg.append((int(TS[-1:]), TS))

            else:
                case = ti_format[TS]['Case']
                # print(f"TI: {TS:5} \t 屬於第 {case} Case")
                if case == "1":
                    signal = Case.case1(
                        TIvale[ti_format[TS]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[TS]["InputArray"]['ti2']],    # Get ti 2 Value
                    )

                elif case == "2":
                    signal = Case.case2(
                        TIvale[ti_format[TS]["InputArray"]['ti1']],    # Get ti 1 Value
                        ti_format[TS]["InputArray"]['C1'],           # C1
                        ti_format[TS]["InputArray"]['C2']            # C2
                    )
                elif case == "3":
                    signal = Case.case3(
                        TIvale[ti_format[TS]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[TS]["InputArray"]['ti2']],    # Get ti 2 Value
                        ti_format[TS]["InputArray"]['C1'],           # C1
                        ti_format[TS]["InputArray"]['C2']            # C2
                    )
                elif case == "4":
                    signal = Case.case4(
                        TIvale[ti_format[TS]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[TS]["InputArray"]['ti2']],    # Get ti 2 Value
                        ti_format[TS]["InputArray"]['C1'],           # C1
                        ti_format[TS]["InputArray"]['C2']            # C2
                    )
                elif case == "5":
                    signal = Case.case5(
                        TIvale[ti_format[TS]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[TS]["InputArray"]['ti2']],    # Get ti 2 Value
                        TIvale[ti_format[TS]["InputArray"]['ti3']],    # Get ti 3 Value
                        ti_format[TS]["InputArray"]['C1']            # C1
                    )
                elif case == "6":
                    signal = Case.case6(
                        TIvale[ti_format[TS]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[TS]["InputArray"]['ti2']],    # Get ti 2 Value
                        TIvale[ti_format[TS]["InputArray"]['ti3']],    # Get ti 3 Value
                        TIvale[ti_format[TS]["InputArray"]['ti4']]     # Get ti 4 Value
                    )
                elif case == "AROON": # Special
                    signal = Case.caseAROON(
                        TIvale[ti_format[TS]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[TS]["InputArray"]['ti2']],    # Get ti 2 Value
                        TIvale[ti_format[TS]["InputArray"]['ti3']],    # Get ti 3 Value
                        ti_format[TS]["InputArray"]['C1'],           # C1
                        ti_format[TS]["InputArray"]['C2'],           # C2
                        ti_format[TS]["InputArray"]['C3']            # C3
                    )

                signal = pd.DataFrame(signal)
                signal.columns = [TS]       # 命名 Column
                data = pd.concat([data, signal], axis=1)
        
        MovingAvg = [TS[1] for TS in sorted(MovingAvg)]

        Combinaion = self.__Combine(MovingAvg)
        for c in Combinaion:

            signal = Case.case1(
                TIvale[c[0]],
                TIvale[c[1]]
            ) 

            signal = pd.DataFrame(signal)
            signal.columns = [f"{c[0]}&{c[1]}"]
            data = pd.concat([data, signal], axis=1)

        if __name__ == "__main__":
            data.to_csv(f"{self.path}/Signal.csv")
    
        data.to_json(f"{self.path}/Signal.json", orient='columns')
        # data.to_json(f"{self.path}/Signal.json", orient='records')
        print(f"已完成交易信號的產生")   
    ##


    def __Combine(self, MovingList:list) -> list: 
        # 利用 backtracking 做組合 
        # 但要 先確保 list 裡面的指標 要是 由小 --> 大 的排列方式
        n = len(MovingList)
        res = []
        def backtrack(tmp, start):
            
            if len(tmp) == 2:
                res.append(tmp.copy())
                return

            for i in range(start, n):
                tmp.append(MovingList[i])
                backtrack(tmp,  i + 1)
                tmp.pop()
        
        backtrack([], 0)
        return res

    #======================================

    def ProduceTable(self):
        with open(f"{self.path}/Signal.json") as f1, open(f"{self.path}/StockData.json") as f2:
            Signal:pd.DataFrame = pd.read_json(f1)
            Data:pd.DataFrame = pd.read_json(f2)

        Signal_list = Signal.columns
        #把 Signal 的 name 轉成 list

        n = len(Signal)
        TSlen = len(Signal_list)

        Signal = Signal.to_numpy()

        Table = np.concatenate([Data['close'].to_numpy().reshape(n, 1), np.zeros((n, (TSlen - 1)*(TSlen - 1)), dtype=np.int0) ], axis=1)

        # Table中 第1行是 Close 收盤價
        # 接下來合併 n * (TSlen-1)^2 大小的 0 矩陣
        #Martix Size = n * [(TSlen-1)^2 + 2]

        ColName:list = ["close"]


        # print(Table)
        Col = 1
        for buy in range(1, TSlen):
            Buy_Signal:np.array = Signal[:, buy]   # pd.Series to np.array

            for sell in range(1, TSlen): 
                Sell_Signal:np.array = Signal[:, sell] #                

                # print(f"{buy} : {sell} ==> {Col}")
                Flag:bool = False # True == 有買了
                for i in range(n):
                    if Buy_Signal[i] == 1 and Sell_Signal[i] == -1:
                        #當 同時有 Buy & Sell 的信號時
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

        if __name__ == "__main__":
            Output.to_csv(f"{self.path}/Table.csv")
        Output.to_json(f"{self.path}/Table.json", orient='columns')
        # Output.to_json(f"{self.path}/Table_test.json", orient='records')


        print("Finished Producing TradingRule Table\r\n")
            
  
      
if __name__ == "__main__":
    # 獨立執行 測試用
    import json
    import cProfile
    with open('../setting.json') as f:
        ti2s = TI2Signal(json.load(f))
    
    # ti2s.ProduceSignal()
    ti2s.ProduceTable()
    # cProfile.run("ti2s.ProduceTable()")



'''
		"WMA",
		"TRIMA",
		"SMA",
		"MAMA",
		"KAMA",
		"EMA",
		"DEMA",
		"TRIX",
		"PLUS_DM",
		"PLUS_DI",
		"MINUS_DM",
		"MINUS_DI",
		"PSY",
		"WMS%R",
		"ULTOSC",
		"MOM",
		"BOP",
		"APO",
		"MFI",
		"CMO",
		"ADX",
		"ROC",
		"PPO",
		"ADXR",
		"AROON"
'''