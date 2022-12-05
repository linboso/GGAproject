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
            self.Path = f"../data/stock/{self.StockID}/ValidationData"
            self.privateMapping = {}
        except:
            print("讀取 BackTestingBlock.json 失敗")
            print("請確認該檔案是否存在")
        print()
        try:
        #init the object
            self.PreBackTesting()
            self.Run()
            self.Query()
        except:
            print("BackTesting物件初始化失敗")
            print("請確認該程序是否有誤")
    
    def reWeight(self):
        try:
            with open("./BackTestingBlock.json") as f:
                data = json.load(f)
                #print(data)
            self.Weight = data['Weight']
            self.PreBackTesting()
            self.Run()
            self.Query()
        except:
            print("在reWight時 讀取 BackTestingBlock.json 失敗")
            print("請確認該檔案是否存在")  

    def PreBackTesting(self):
        #DownloadData
        self.__CalculateTIvalue()
        self.__TI2signal()
        self.__ProduceTable()
        print("Finished all PreBackTestingWorks\r\n")

    def __CalculateTIvalue(self):
        #====================CalculateTIvalue====================
        TI_List = set()
        TIpair = []
        for i in self.TradingStrategy.values():

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
        #print('TIpair:',self.TIpair)
        #print('TI_List:',TI_List)
        df = pd.DataFrame()

        try:
            #print(f"{self.Path}/StockData.json")
            with open(f"{self.Path}/StockData.json") as f:
                df = pd.read_json(f)
        except:
            print(f"缺失 {self.StockID} 的 StockData.json 的資料")
        

        TIValueTable = pd.DataFrame()
        ALL_TI = ['WMA5', 'WMA10', 'WMA20', 'WMA60', 'TRIMA5', 'TRIMA10', 'TRIMA20', 'TRIMA60', 
                        'TEMA5', 'TEMA10', 'TEMA20', 'TEMA60', 'SMA5', 'SMA10', 'SMA20', 'SMA60', 
                        'MAMA', 'MA5', 'MA10', 'MA20', 'MA60', 'KAMA5', 'KAMA10', 'KAMA20', 
                        'KAMA60', 'EMA5', 'EMA10', 'EMA20', 'EMA60', 'DEMA5', 'DEMA10', 'DEMA20', 'DEMA60', 'TRIX', 
                        'PLUS_DI', 'PLUS_DM', 'RSI', 'WILLR', 'ULTOSC', 'MOM', 'BOP', 'APO', 'MFI', 'AROONOSC', 'CCI', 
                        'CMO', 'ROC', 'PPO', 'MACD', 'STOCH', 'ADX', 'ADXR']

        ColName = []
        for TI in ALL_TI:
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

        #print(f"計算出來的 指標數值有: {list(TIValueTable.columns)}")
        # print(TIValueTable.head(5))
        
        #print(f"儲存 TIvalue.json 在 {self.Path}\r\n")
        TIValueTable.to_json(f"{self.Path}/TIvalue.json" ,orient='columns')
         
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
            with open(f'./SignalMap.json', 'r', encoding="utf-8") as f:
                SignalMap = json.load(f)
        else:
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
        


        for TS in SignalMap["NON_MA_TYPE"]:                            
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
        
          
        Date = pd.concat([Date, pd.DataFrame(Data, columns=ColName)], axis=1)
        #根據training出結果保留交易策略
        chosenTS = []
        for i in self.TIpair:
            if isinstance(i, str):chosenTS.append(i)
            else:chosenTS.append(f'{i[0]}&{i[1]}') 
        chosenTS = [dontchosenTS for dontchosenTS in Date.columns if dontchosenTS not in chosenTS]
        Date = Date.drop(chosenTS,axis = 1).reset_index(drop=True)#delete not chosen TS  
        Date.to_json(f"{self.Path}/Signal.json", orient='columns')

        if __name__ == "__main__":
            Date.to_csv(f"{self.Path}/SignalforDebug.csv")
                #print("已產生SignalforDebug供確認") 

    def __ProduceTable(self):
        #此function為將買賣signal合併為交易信號，最終結果分為兩個files:
        #1.Table_GTSP.json:為該GTSP的最終交易訊號
        #2.Table_SLTP.josn:為該GTSP的最終交易訊號且具有停損停利之功能

        keep = []
        for i in range(0,len(self.TIpair),2):
            tmp = []
            if isinstance(self.TIpair[i], str):
                tmp.append(self.TIpair[i])
            else:
                tmp.append(f'{self.TIpair[i][0]}&{self.TIpair[i][1]}')
            if isinstance(self.TIpair[i+1], str):
                tmp.append(self.TIpair[i+1])
            else:
                tmp.append(f'{self.TIpair[i+1][0]}&{self.TIpair[i+1][1]}')
            keep.append(f'{tmp[0]}^{tmp[1]}')
        #print(keep)
        privateMapping = {}
        for i in range(len(keep)):
            privateMapping[i] = keep[i]
        self.privateMapping = privateMapping
        #print('privateMapping:',privateMapping)
            

        
        with open(f"{self.Path}/Signal.json") as f1, open(f"{self.Path}/StockData.json") as f2, open(f"{self.Path}/Date.json") as f3:
            Signal = pd.read_json(f1)
            Data = pd.read_json(f2)#停損停利用
            Date = pd.read_json(f3)

        Signal_list = Signal.columns

        #===================================================Table_GTSP===================================================
        Table = pd.concat([Date, Data['close']], axis=1) #create a new table
        for buy in Signal_list[0:]:
            for sell in Signal_list[0:]: 
                Buy_Signal = Signal[buy].values   
                Sell_Signal = Signal[sell].values 
                
                New_Signal = []
                Flag:bool = False
                last_buy:int = 0
                for i in range(len(Buy_Signal)):
                    if Buy_Signal[i] == 1 and Sell_Signal[i] == -1:
                        if Flag:
                            New_Signal.append(-1)
                            Flag = False
                        else:
                            New_Signal.append(1)
                            Flag = True
                            last_buy = i
                    elif Buy_Signal[i] == 1 and not Flag:
                        New_Signal.append(1)
                        Flag = True
                        last_buy = i
                    elif Sell_Signal[i] == -1 and Flag:
                        New_Signal.append(-1)
                        Flag = False
                    else:
                        New_Signal.append(0)
                if Flag:
                    New_Signal[last_buy] = 0 #remove the last buy cuz it won't be selled 
                New_Signal = pd.DataFrame(New_Signal)
                New_Signal.columns = [f"{buy}^{sell}"]
                Table = pd.concat([Table, New_Signal], axis=1)
        
        #By training data choosing TS
        dropIt = [dontkeep for dontkeep in Table.columns if dontkeep not in keep]
        del dropIt[0:2]  #保留'Date', 'close'
        Table = Table.drop(dropIt,axis = 1).reset_index(drop=True)#delete not chosen TS

        
        Table.to_json(f"{self.Path}/Table_GTSP.json", orient='records')
        Table.to_csv(f"{self.Path}/Table_GTSP.csv")
        print("Finished Table_GTSP\r\n")  
    

        #===================================================Table_SLTP===================================================
        Table = pd.concat([Date, Data['close']], axis=1) #create a new table
        close = Data["close"].values
        
        for buy in Signal_list[0:]:
            for sell in Signal_list[0:]: 
                Buy_Signal = Signal[buy].values   
                Sell_Signal = Signal[sell].values 
                stop_loss_price:float = None
                take_profit_price:float = None

                New_Signal = []
                Flag:bool = False
                last_buy:int = 0
                for i in range(len(Buy_Signal)):
                    #先判斷SLTP,有買過就會紀錄SLTP之price
                    if Flag:
                        if(stop_loss_price > close[i]) or (close[i] > take_profit_price):
                            New_Signal.append(-1)
                            Flag = False
                            stop_loss_price = None
                            take_profit_price = None
                            continue

                    if Buy_Signal[i] == 1 and Sell_Signal[i] == -1:
                        if Flag:
                            New_Signal.append(-1)
                            Flag = False
                            stop_loss_price = None
                            take_profit_price = None
                        else:
                            New_Signal.append(1)
                            Flag = True
                            last_buy = i
                            stop_loss_price = (1-self.SL)*close[i]
                            take_profit_price = (1+self.TP)*close[i]
                    elif Buy_Signal[i] == 1 and not Flag:
                        New_Signal.append(1)
                        Flag = True
                        last_buy = i
                        stop_loss_price = (1-self.SL)*close[i]
                        take_profit_price = (1+self.TP)*close[i]
                    elif (Sell_Signal[i] == -1 and Flag) :
                        New_Signal.append(-1)
                        Flag = False
                        stop_loss_price = None
                        take_profit_price = None
                    else:
                        New_Signal.append(0)
                if Flag:
                    New_Signal[last_buy] = 0 #remove the last buy cuz it won't be selled 
                New_Signal = pd.DataFrame(New_Signal)
                New_Signal.columns = [f"{buy}^{sell}"]
                Table = pd.concat([Table, New_Signal], axis=1)

        #By training data choosing TS
        dropIt = [dontkeep for dontkeep in Table.columns if dontkeep not in keep]
        del dropIt[0:2]  #保留'Date', 'close'
        Table = Table.drop(dropIt,axis = 1).reset_index(drop=True)#delete not chosen TS
                
        
        Table.to_json(f"{self.Path}/Table_SLTP.json", orient='records')
        Table.to_csv(f"{self.Path}/Table_SLTP.csv")
        print("Finished Table_SLTP\r\n")

    def Run(self): 
        #約花14秒
        #此function為將買賣signal合併為交易信號，最終結果分為三個files:
        #1.Buy&Hold.json:為該區間使用B&H的效果(目的是為了比對GTSP系統是否有效果)
        #2.Detail_GTSP.json:為該GTSP的最終交易訊號
        #3.Detail_SLTP.josn:為該GTSP的最終交易訊號且具有停損停利之功能
        
        with open(f'{self.Path}/Table_GTSP.json') as f1, open(f'{self.Path}/Table_SLTP.json') as f2:
            withoutSLTP = pd.read_json(f1)
            withSLTP = pd.read_json(f2)
        #with open(f'{self.Path}/{self.StockID}/TraningData/{self.Strategy}.json') as s:
            #chosenTS = pd.read_json(s) 
        
        price = withoutSLTP["close"].values    
        date  = withoutSLTP["Date"].values       
        
        #===================================================Buy&Hold===================================================
        bh_return_rate = (price[-1] - price[0])/price[0]
        bh_return_money = bh_return_rate * self.Capital
        buy_and_hold = {
          "Date": f"{date[0]} ~ {date[-1]}",
          "return_rate": bh_return_rate,
          "return_money": bh_return_money,
        }
        with open(f'{self.Path}/Buy&Hold.json', "w") as outfile:
            json.dump(buy_and_hold, outfile)
        
                
        #define map_group:用來mapping data
        map_group1 = self.privateMapping
        # {'2': MACD^STOCH}:指標2 is MACD^STOCH
        map_group2 = {value:key for key,value in map_group1.items()}
        
        
        #map_group2 to 資金比例
        map = {}
        num = 0
        for i in self.GTSP:
            if i == 0:
                num += 1
            else:
                map[f"{i-1}"] = num
        for i in map_group2:
            index = map_group2[f"{i}"]
            map_group2[f"{i}"] = map[f"{index}"]
        # {'MACD^STOCH': 3}:MACD^STOCH is 是第三組(資金權重)
        
        
        #===================================================Detail_GTSP===================================================
        withoutSLTP_list = withoutSLTP.columns               
        
        #record用column方式並起來
        recordDate, Trading_Strategy, recordTransaction_Type, recordStock_price, recordTransaction_amount, recordReturn_money, recordRate_of_Return = [[] for x in range(7)]

        for signal in withoutSLTP_list[3:]:
            now_Signal = withoutSLTP[signal].values                 
            buy_price = 0 

            for i in range(len(now_Signal)):
                record = []
                Transaction_amount = self.Capital * self.Weight[map_group2[signal]]
                if now_Signal[i] == 1:
                    buy_price = price[i] 
                    recordDate.append(date[i])
                    Trading_Strategy.append(signal)
                    recordTransaction_Type.append(now_Signal[i])
                    recordStock_price.append(price[i])
                    recordTransaction_amount.append(Transaction_amount)
                    recordReturn_money.append(None)
                    recordRate_of_Return.append(None)          
                elif now_Signal[i] == -1:
                    Return_money = int((price[i] - buy_price) / buy_price * Transaction_amount)
                    recordDate.append(date[i])
                    Trading_Strategy.append(signal)
                    recordTransaction_Type.append(now_Signal[i])
                    recordStock_price.append(price[i])
                    recordTransaction_amount.append(Transaction_amount)
                    recordReturn_money.append(Return_money)
                    recordRate_of_Return.append((Return_money/Transaction_amount))      
        
        detail_table = pd.DataFrame({
            "Date" :recordDate,
            "Trading_Strategy":Trading_Strategy, 
            "Transaction_Type":recordTransaction_Type, 
            "Stock_price":recordStock_price, 
            "Transaction_amount":recordTransaction_amount, 
            "Return_money":recordReturn_money, 
            "Rate_of_Return":recordRate_of_Return
        })

        #detail_table.columns = ["Date", "Trading_Strategy", "Transaction_Type", "Stock_price", "Transaction_amount", "Return_money", "Rate_of_Return"]
        detail_table.reset_index(drop=True, inplace=True)
        detail_table.to_json(f"{self.Path}/Detail_GTSP.json", orient='records')
        detail_table.to_csv(f"{self.Path}/Detail_GTSP.csv")
        print("Finished Detail_GTSP\r\n")
        
        
        #===================================================Detail_SLTP===================================================
        withSLTP_list = withSLTP.columns

        #record用column方式並起來
        recordDate, Trading_Strategy, recordTransaction_Type, recordStock_price, recordTransaction_amount, recordReturn_money, recordRate_of_Return = [[] for x in range(7)]             
        
        for signal in withSLTP_list[3:]:
            now_Signal = withSLTP[signal].values                 
            buy_price = 0 

            for i in range(len(now_Signal)):
                record = []
                Transaction_amount = self.Capital * self.Weight[map_group2[signal]]
                if now_Signal[i] == 1:
                    buy_price = price[i] 
                    recordDate.append(date[i])
                    Trading_Strategy.append(signal)
                    recordTransaction_Type.append(now_Signal[i])
                    recordStock_price.append(price[i])
                    recordTransaction_amount.append(Transaction_amount)
                    recordReturn_money.append(None)
                    recordRate_of_Return.append(None)                      
                elif now_Signal[i] == -1:
                    Return_money = int((price[i] - buy_price) / buy_price * Transaction_amount)
                    recordDate.append(date[i])
                    Trading_Strategy.append(signal)
                    recordTransaction_Type.append(now_Signal[i])
                    recordStock_price.append(price[i])
                    recordTransaction_amount.append(Transaction_amount)
                    recordReturn_money.append(Return_money)
                    recordRate_of_Return.append((Return_money/Transaction_amount))  

        
        detail_table2 = pd.DataFrame({
            "Date" :recordDate,
            "Trading_Strategy":Trading_Strategy, 
            "Transaction_Type":recordTransaction_Type, 
            "Stock_price":recordStock_price, 
            "Transaction_amount":recordTransaction_amount, 
            "Return_money":recordReturn_money, 
            "Rate_of_Return":recordRate_of_Return
        }) 

        
        detail_table2.reset_index(drop=True, inplace=True)
        detail_table2.to_json(f"{self.Path}/Detail_SLTP.json", orient='records')
        detail_table2.to_csv(f"{self.Path}/Detail_SLTP.csv")
        print("Finished Detail_SLTP\r\n")

    def Query(self):
        #將所有可能組合出來放入Folder:
        #1.Folder_GTSP:存放該GTSP交易明細所有組合之資料夾
        #2.Folder_SLTP:存放該GTSP且具有SLTP功能之交易明細所有組合之資料夾
        with open(f'{self.Path}/Detail_GTSP.json') as f1,open(f'{self.Path}/Detail_SLTP.json') as f2:
            withoutSLTP_table = pd.read_json(f1)
            withSLTP_table = pd.read_json(f2)

        map_group1 = self.privateMapping# {'2': MACD^STOCH}:指標2 is MACD^STOCH
        Alltsp:list = self.ADVcombine()
            
        #===================================================Folder_GTSP=================================================== 
        for tsp in Alltsp:
            table = pd.DataFrame()
            
            for i in tsp:
                temp = withoutSLTP_table[withoutSLTP_table["Trading_Strategy"] == map_group1[i-1]]
                table = pd.concat([table,temp],axis = 0)
            table = table.sort_values("Date")
            total_return_money = table['Return_money'].sum()

            table.reset_index(drop=True, inplace=True)
            table.to_json(f"{self.Path}/Folder_GTSP/{tsp}_{total_return_money}.json", orient='records')
            #table.to_csv(f"{self.Path}/Folder_GTSP/{tsp}.csv",index = False)
        print("Finished Folder_GTSP\r\n")
        #===================================================Folder_SLTP===================================================    
        for tsp in Alltsp:
            table = pd.DataFrame()
            for i in tsp:
                temp = withSLTP_table[withSLTP_table["Trading_Strategy"] == map_group1[i-1]]
                table = pd.concat([table,temp],axis = 0)
            table = table.sort_values("Date")
            total_return_money = table['Return_money'].sum()

            table.reset_index(drop=True, inplace=True)
            table.to_json(f"{self.Path}/Folder_SLTP/{tsp}_{total_return_money}.json", orient='records')
            #table.to_csv(f"{self.Path}/Folder_SLTP/{tsp}.csv",index = False)

        print("Finished Folder_SLTP\r\n")

    def ADVcombine(self) -> list:
        GTSP = []
        tem = []
        n = 0
        for i in self.GTSP:
            if i == 0:
                GTSP.append(tem)
                tem = []
                n+=1
                continue
            tem.append(i)

        res = []#restore result
        #TSP 為 每一個不同的 TSG 中 各取一個 TS 組合成的 
        def backtrack(TSP, start):
            if len(TSP) == n:
                return res.append(TSP[:])

            for Kth_Group in range(start, n):
                for TS in range(len(GTSP[Kth_Group])):
                    # 每一個 TSG 的 長度都不一樣
                    TSP.append(GTSP[Kth_Group][TS])
                    backtrack(TSP,  Kth_Group + 1)
                    TSP.pop()
        
        backtrack([], 0)
        return res

    # def mapTest(self):
    #     TI_List = set()
    #     for i in self.TradingStrategy.values():
    #         if isinstance(self.SignalMap[i[0]], str):
    #             TI_List.add(self.SignalMap[i[0]])
    #         else:
    #             for j in self.SignalMap[i[0]]:
    #                 TI_List.add(j) 
    #         if isinstance(self.SignalMap[i[1]], str):
    #             TI_List.add(self.SignalMap[i[1]])
    #         else:
    #             for j in self.SignalMap[i[1]]:
    #                 TI_List.add(j) 
    #     print(TI_List)
    #     #TI.List = self.SignalMap[self.TradingStrategy]


if __name__ == '__main__':
    obj = BackTesting()
    #obj.mapTest()
    #obj.PreBackTesting()
    #obj.Run()
    #obj.Query()
    #print(obj)