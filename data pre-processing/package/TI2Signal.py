
import pandas as pd
import json
import os

from .SettingFile import SettingFile
from .case_package import Case


class TI2Signal():
    def __init__(self) -> None:
        setting = SettingFile().Read()
        self.stock_id = setting['StockID']
        self.start = setting['StartDate']
        self.end = setting['EndDate']
        self.ti_list = setting['TechnicalIndicator']
        self.savepath = f"stock/{self.stock_id}/{self.start}~{self.end}"
        self.readpath = f"stock/{self.stock_id}/{self.start}~{self.end}"

    def ProduceSignal(self):
        ti_format = TIvale = data = pd.DataFrame()
        try:
            with open('./package/case_package/TIformat.json', 'r', encoding="utf-8") as f:
                ti_format = pd.DataFrame(json.load(f))
        except:
            print("Missing TIformat.json \tlocation: ./package/case_package/TIformat.json")

        try:
            with open(f"{self.readpath}/TIvalue.json") as f:
                TIvale = pd.DataFrame(json.load(f))
        except:
            print(f"Missing TIvalue.json \tlocation: {self.readpath}/TIvalue.json")

        try:
            with open(f"{self.readpath}/Date.json") as f:
                data = pd.DataFrame(json.load(f))
        except:
            print(f"Missing Date.json \tlocation: {self.readpath}/Date.json")
        
        # above all are just make sure to get Essential Data Value
        signal = []
        tmp = {}
        for i in self.ti_list: # 有被選擇的 TI list 
            #e.g  假設 i = MA5 
            # i[:2] == MA 確實 in ti format 裡面
            # 但像是 MACD 的 [:2] 也是 MA 
            # 所以 必須加上 i=MA5 not in ti format 裡面  

            if i not in ti_format:
                for k in range(len(i)):
                    if i[k].isdigit() == True:
                        break
                if i[:k] not in tmp:
                    tmp[i[:k]] = []
                tmp[i[:k]].append(i)
                # print(tmp)

            else:
                case = ti_format[i]['Case']
                print(f"TI: {i} is belong to \t Case : {case}")
                if case == "1":
                    signal = Case.case1(
                        TIvale[ti_format[i]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[i]["InputArray"]['ti2']],    # Get ti 2 Value
                    )

                elif case == "2":
                    signal = Case.case2(
                        TIvale[ti_format[i]["InputArray"]['ti1']],    # Get ti 1 Value
                        ti_format[i]["InputArray"]['C1'],           # C1
                        ti_format[i]["InputArray"]['C2']            # C2
                    )
                elif case == "3":
                    signal = Case.case3(
                        TIvale[ti_format[i]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[i]["InputArray"]['ti2']],    # Get ti 2 Value
                        ti_format[i]["InputArray"]['C1'],           # C1
                        ti_format[i]["InputArray"]['C2']            # C2
                    )
                elif case == "4":
                    signal = Case.case4(
                        TIvale[ti_format[i]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[i]["InputArray"]['ti2']],    # Get ti 2 Value
                        ti_format[i]["InputArray"]['C1'],           # C1
                        ti_format[i]["InputArray"]['C2']            # C2
                    )
                elif case == "5":
                    signal = Case.case5(
                        TIvale[ti_format[i]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[i]["InputArray"]['ti2']],    # Get ti 2 Value
                        TIvale[ti_format[i]["InputArray"]['ti3']],    # Get ti 3 Value
                        ti_format[i]["InputArray"]['C1']            # C1
                    )
                elif case == "6":
                    signal = Case.case6(
                        TIvale[ti_format[i]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[i]["InputArray"]['ti2']],    # Get ti 2 Value
                        TIvale[ti_format[i]["InputArray"]['ti3']],    # Get ti 3 Value
                        TIvale[ti_format[i]["InputArray"]['ti4']]     # Get ti 4 Value
                    )
                elif case == "AROON": # Special
                    signal = Case.caseAROON(
                        TIvale[ti_format[i]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[i]["InputArray"]['ti2']],    # Get ti 2 Value
                        TIvale[ti_format[i]["InputArray"]['ti3']],    # Get ti 3 Value
                        ti_format[i]["InputArray"]['C1'],           # C1
                        ti_format[i]["InputArray"]['C2'],           # C2
                        ti_format[i]["InputArray"]['C3']            # C3
                    )

                signal = pd.DataFrame(signal)
                signal.columns = [i] # name col
                data = pd.concat([data, signal], axis=1)
                data.to_json(f"{self.savepath}/Signal.json", orient='records')

       # 等全部的 ma, sma... 之類的指標都 一次append 到 tmp 裡面後再處理
        for i in tmp:
            combinaion = self.__combine(tmp[i])
            print(f"{tmp[i]} >> before combination >> {combinaion}")
            for c in combinaion:
                try:
                    signal = Case.case1(
                        TIvale[c[0]],
                        TIvale[c[1]]
                    ) 
                    signal = pd.DataFrame(signal)
                    signal.columns = [f"{c[0]}&{c[1]}"]
                    data = pd.concat([data, signal], axis=1)
                    data.to_json(f"{self.savepath}/Signal.json", orient='records')
                except:
                    print(f"TIValue has no {c[0]} or {c[1]} value")
            print(f"Finished all producing signal")   
    ##


    def __combine(self, ti_list:list) -> list: 
        # 利用 backtracking 做組合 
        # 但是 要先確保 list 裡面的指標 要是 由小 --> 大 的排列方式
        n = len(ti_list)
        res = []

        def backtrack(tmp, start):
            
            if len(tmp) == 2:
                res.append(tmp[:])
                return

            for i in range(start, n):
                tmp.append(ti_list[i])
                backtrack(tmp,  i + 1)
                tmp.pop()
        
        backtrack([], 0)
        return res
        

    def ProduceTalbe(self):
        with open(f"{self.readpath}/Signal.json") as f:
            Signal = pd.DataFrame(json.load(f))

        Signal_list = Signal.columns
        Table = Signal["Date"]

        for buy in Signal_list[1:]:
            for sell in Signal_list[1:]: 
                Buy_Signal = Signal[buy].values   # pd.Series to list
                Sell_Signal = Signal[sell].values # List 計算上 速度比較快
                
                New_Signal = []
                Flag:bool = False
                for i in range(len(Buy_Signal)):
                    if Buy_Signal[i] == 1 and Sell_Signal[i] == -1:
                        if not Flag:
                            New_Signal.append(-1)
                            Flag = True
                        else:
                            New_Signal.append(1)
                    elif Buy_Signal[i] == 1 and not Flag:
                        New_Signal.append(1)
                        Flag = True
                    elif Sell_Signal[i] == -1 and Flag:
                        New_Signal.append(-1)
                        Flag = True
                    else:
                        New_Signal.append(0)

                New_Signal = pd.DataFrame(New_Signal)
                New_Signal.columns = [f"{buy}^{sell}"]
                Table = pd.concat([Table, New_Signal], axis=1)
                Table.to_json(f"{self.readpath}/Table.json", orient='records')
            
      






