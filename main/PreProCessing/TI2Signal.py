import pandas as pd

if __name__ == "__main__":
    from Case import Case
else:
    from .Case import Case
    


class TI2Signal():
    def __init__(self, Setting) -> None:
        setting = Setting
        self.stock_id = setting['StockID']
        self.start = setting['TrainingPeriod']['StartDate']
        self.end = setting['TrainingPeriod']['EndDate']
        self.ti_list = setting['TechnicalIndicator']
        if __name__ == "__main__":
            self.path = f"../{setting['Path']}/{setting['StockID']}/TrainingData"
        else:
            self.path = f"{setting['Path']}/{setting['StockID']}/TrainingData"

    def ProduceSignal(self):
        ti_format, TIvale ,data = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        if __name__ == "__main__":
   
            with open(f'./Case/TIformat.json', 'r', encoding="utf-8") as f:
                ti_format = pd.read_json(f)

        # =========================================================== 
        else:
            try:
                with open('./PreProCessing/Case/TIformat.json', 'r', encoding="utf-8") as f:
                    ti_format = pd.read_json(f)
            except:
                print("缺失 TIformat.json \t位置: ./PreProCessing/Case/TIformat.json")

        try:
            with open(f"{self.path}/TIvalue.json") as f:
                TIvale = pd.read_json(f)
        except:
            print(f"缺失 TIvalue.json 檔 \t位置: {self.path}/TIvalue.json")

        try:
            with open(f"{self.path}/Date.json") as f:
                data = pd.read_json(f)
        except:
            print(f"缺失 Date.json 檔 \t位置: {self.path}/Date.json")


        
        #確認所有 必要的資料 是否都在
        signal = []
        tmp = {}
        for TS in self.ti_list: # 有被選擇的 TI list 
            if TS not in ti_format:
                for k in range(len(TS)):
                    if TS[k].isdigit() == True:
                        break
                print(f" >>> {TS[:k]}  <>  {TS} \t{tmp}")
                if TS[:k] not in tmp:
                    tmp[TS[:k]] = []
                tmp[TS[:k]].append(TS)
            # 假設 TS == MA5 
            # TS[:2] == MA 確實 in TS-format 裡面
            # 但像是 MACD 的 [:2] 也是 MA 
            # 所以 必須加上 (TS == MA5) not in TI-format 裡面  
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

                if __name__ == "__main__":
                    data.to_csv(f"{self.path}/Signal.csv")

                data.to_json(f"{self.path}/Signal.json", orient='records')
        # End For
        
       # 把 ma, sma... 之類的指標都 append 到 tmp 裡面後再一次處理
        for i in tmp:
            Combinaion = self.__combine(tmp[i])
            # print(f"{tmp[i]} Do Combination  \r\n{Combinaion}")
            for c in Combinaion:
                try:
                    signal = Case.case1(
                        TIvale[c[0]],
                        TIvale[c[1]]
                    ) 

                    signal = pd.DataFrame(signal)
                    signal.columns = [f"{c[0]}&{c[1]}"]
                    data = pd.concat([data, signal], axis=1)

                    # print(f"TIValue 沒有 {TIvale[c[0]]} 或 {TIvale[c[1]]} 的值")
                    # print(f"TIValue 沒有 {c[0]} 或 {c[1]} 的值")
                except:
                    print(f"TIValue 沒有 {c[0]} 或 {c[1]} 的值")

            if __name__ == "__main__":
                data.to_csv(f"{self.path}/Signal.csv")
      
            data.to_json(f"{self.path}/Signal.json", orient='records')

            print(f"已完成交易信號的產生")   
    ##


    def __combine(self, ti_list:list) -> list: 
        # 利用 backtracking 做組合 
        # 但要 先確保 list 裡面的指標 要是 由小 --> 大 的排列方式
        n = len(ti_list)
        res = []
        def backtrack(tmp, start):
            
            if len(tmp) == 2:
                res.append(tmp.copy())
                return

            for i in range(start, n):
                tmp.append(ti_list[i])
                backtrack(tmp,  i + 1)
                tmp.pop()
        
        backtrack([], 0)
        return res
        

    def ProduceTable(self):
        with open(f"{self.path}/Signal.json") as f1, open(f"{self.path}/StockData.json") as f2:
            Signal = pd.read_json(f1)
            Data = pd.read_json(f2)


        Signal_list = Signal.columns
        Table = pd.concat([Signal['Date'], Data['close']], axis=1)
        

        for buy in Signal_list[1:]:
            print(f"========= {buy} =========")
            for sell in Signal_list[1:]: 
                Buy_Signal = Signal[buy].to_numpy()   # pd.Series to np.array
                Sell_Signal = Signal[sell].to_numpy() #
                
                New_Signal:list = []
                Flag:bool = False # True == 有買了
                for i in range(len(Buy_Signal)):
                    if Buy_Signal[i] == 1 and Sell_Signal[i] == -1:
                        if Flag:
                            New_Signal.append(-1)
                        else:
                            New_Signal.append(1)
                            Flag = False
                    # 如果同時有 buy & sell 的信號 
                    # 則依 Flag 狀態 決定

                    elif Buy_Signal[i] == 1 and not Flag:
                        New_Signal.append(1)
                        Flag = True
                    # 若 有 buy Signal 且 Flag == False 
                    # 則可以買入
                    elif Sell_Signal[i] == -1 and Flag:
                        New_Signal.append(-1)
                        Flag = False
                    # 若 有 sell Signal 且 Flag == True 
                    # 則可以賣出  賣完後 Flag 改 False
                    else:
                        New_Signal.append(0)
                    # 沒有 Buy or Sell signal

                New_Signal = pd.DataFrame(New_Signal)
                New_Signal.columns = [f"{buy}^{sell}"]
                Table = pd.concat([Table, New_Signal], axis=1)
                if __name__ == "__main__":
                    Table.to_csv(f"{self.path}/Table.csv")

                Table.to_json(f"{self.path}/Table.json", orient='records')
                
                print(f"==> {sell}")
            print()

        print("Finished Producing TradingRule Table\r\n")
            
      
if __name__ == "__main__":
    # 獨立執行 測試用
    import json
    with open('../setting.json') as f:
        ti2s = TI2Signal(json.load(f))
    
    ti2s.ProduceSignal()
    ti2s.ProduceTable()



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