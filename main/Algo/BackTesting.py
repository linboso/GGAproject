import json
import os
import pandas as pd
import numpy as np
#import talib
#from talib import abstract
#from ..PreProCessing.CalculateTIvalue import TIValue


class BackTesting():
    def __init__(self,StockID) -> None:
        print("Path at terminal when executing this file")
        print(os.getcwd() + "\n")
        print("This file path, relative to os.getcwd()")
        print(__file__ + "\n")
        
        try:
            if __name__ == "__main__":
                with open(f"../data/stock/{StockID}/block.json") as f:
                    data = json.load(f)
                    print("block:",data)
            else:
                with open(f"../data/stock/{StockID}/block.json") as f:
                    data = json.load(f)
                    print("block:",data)
            #loading data
            self.StockID = data['StockID']  
            self.TrainingPeriod = data['TrainingPeriod']
            self.ValidationPeriod = data['ValidationPeriod']
            #self.SL, self.TP = data['SLTP'][0], data['SLTP'][1]
            self.SL, self.TP = 0.03,0.1  #收集數據用 (寫死停損停利)
            self.Capital = data['Capital']
            self.GTSP = data['GTSP']
            self.Weight = data['Weight']
            self.TradingStrategy = {v : k for v,k in enumerate(data['TradingStrategy'])}
            #print(self.TradingStrategy)
        except:
            print("讀取 BackTestingBlock.json 失敗")
            print("請確認該檔案是否存在")
        finally:
            #private data
            self.TI_List = []
            self.TIpair = []
            self.Path = f"../data/stock/{self.StockID}/ValidationData"
            self.privateMapping = {}
        print()
        # try:
        # #init the object
        #     self.ProduceTable()
        #     self.Query()
        # except:
        #     print("BackTesting物件初始化失敗")
        #     print("請確認該程序是否有誤")
    
    def chosenSignal(self):
        #此function根據block裡training結果來保留選定的交易策略
        if __name__ == "__main__":
            with open(f"../data/stock/{self.StockID}/ValidationData/Signal.json") as f:
                Signal = pd.read_json(f)
        else:
            with open(f"../data/stock/{self.StockID}/ValidationData/Signal.json") as f:
                Signal= pd.read_json(f)

        chosenTS = set([i[0] for i in self.TradingStrategy.values()] + [i[1] for i in self.TradingStrategy.values()])
        chosenTS = [dontChosenTS for dontChosenTS in Signal.columns if dontChosenTS not in chosenTS]
        Signal = Signal.drop(chosenTS,axis = 1).reset_index(drop=True)#delete not chosen TS  
        Signal.to_json(f"{self.Path}/chosenSignal.json", orient='columns')     

    def ProduceTable(self):
        #此function為將買賣signal合併為交易信號，最終結果分為兩個files:
        #1.Table_GTSP.json:為該GTSP的最終交易訊號
        #2.Table_SLTP.josn:為該GTSP的最終交易訊號且具有停損停利之功能

        with open(f"{self.Path}/chosenSignal.json") as f1, open(f"{self.Path}/StockData.json") as f2, open(f"{self.Path}/Date.json") as f3:
            Signal = pd.read_json(f1)
            Data = pd.read_json(f2)#停損停利用
            Date = pd.read_json(f3)
        Data = Data.reset_index(drop=True)
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
        keep = []
        for i in self.TradingStrategy.values():
            keep.append(f"{i[0]}^{i[1]}")
        #print(keep)
        dropIt = [dontKeep for dontKeep in Table.columns if dontKeep not in keep]
        del dropIt[0:2]  #保留'Date', 'close'
        Table = Table.drop(dropIt,axis = 1).reset_index(drop=True)#delete not chosen TS

        Table = Table.sort_values(by=['Date'])

        #儲存前將columnName從index改為英文表示
        with open(f"./SignalMap.json") as SignalMap:
            SignalMap = pd.read_json(SignalMap).squeeze()
        SignalMap = SignalMap.to_list()
        columnsName = ['Date','close']
        for col in Table.columns[2:]:
            ts = col.split('^')
            ts1, ts2 ='',''
            if type(SignalMap[int(ts[0])]) == list: 
                ts1 = f'{SignalMap[int(ts[0])][0]}&{SignalMap[int(ts[0])][1]}'
            else:ts1 = f'{SignalMap[int(ts[0])]}'
            if type(SignalMap[int(ts[1])]) == list: 
                ts2 = f'{SignalMap[int(ts[1])][0]}&{SignalMap[int(ts[1])][1]}'
            else:ts2 = f'{SignalMap[int(ts[1])]}'
            columnsName.append(f'{ts1}^{ts2}')
        #順便存privateMapping供run使用======
        self.privateMapping = {v : k for v,k in enumerate(columnsName[2:])}
        with open(f'{self.Path}/TradingStrategy.json', "w") as outfile:
            json.dump(self.privateMapping, outfile)
        #=================================

        Table.columns = columnsName
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

        Table = Table.sort_values(by=['Date'])

        Table = Table.drop(dropIt,axis = 1).reset_index(drop=True)#delete not chosen TS
        Table.columns = columnsName#儲存前將columnName從index改為英文表示

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
        
        #===================================================Buy&Hold===================================================
        with open(f'{self.Path}/Date.json') as Date, open(f'{self.Path}/StockData.json') as StockData:
            Date = pd.read_json(Date)
            StockData = pd.read_json(StockData)
        close = StockData["close"]
        bh_return_rate = (close[-1] - close[0])/close[0]
        bh_return_money = int(bh_return_rate * self.Capital)
        buy_and_hold = {
          "Date": f"{self.ValidationPeriod}", "return_rate": f"{int(bh_return_rate*100)}%", "return_money": bh_return_money,
        }
        with open(f'{self.Path}/Buy&Hold.json', "w") as outfile:
            json.dump(buy_and_hold, outfile)
        
                
        #=====================================define map_group:用來mapping data=========================================
        map_group1 = self.privateMapping
        #print(map_group1)
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
        #print(map_group2)

        with open(f'{self.Path}/Table_GTSP.json') as f1, open(f'{self.Path}/Table_SLTP.json') as f2:
            withoutSLTP = pd.read_json(f1)
            withSLTP = pd.read_json(f2)

        date  = withoutSLTP["Date"].values
        price = withoutSLTP["close"].values    
        
        #===================================================Detail_GTSP===================================================
        withoutSLTP_list = withoutSLTP.columns               
        
        #record用column方式並起來
        recordDate, Trading_Strategy, recordTransaction_Type, recordStock_price, share ,recordTransaction_amount, recordReturn_money, recordRate_of_Return = [[] for x in range(8)]

        for signal in withoutSLTP_list[3:]:
            now_Signal = withoutSLTP[signal].values                 
            buy_price = 0 
            nowShare = 0

            for i in range(len(now_Signal)):
                
                Transaction_amount = self.Capital * self.Weight[map_group2[signal]]
                if now_Signal[i] == 1:
                    nowShare = int(Transaction_amount/price[i])
                    buy_price = price[i] 
                    recordDate.append(date[i])
                    Trading_Strategy.append(signal)
                    recordTransaction_Type.append(now_Signal[i])
                    recordStock_price.append(price[i])
                    share.append(nowShare)
                    recordTransaction_amount.append(int(nowShare*price[i]))
                    recordReturn_money.append(None)
                    recordRate_of_Return.append(None)          
                elif now_Signal[i] == -1:
                    try:
                        #Return_money = int((price[i] - buy_price) / buy_price * Transaction_amount)
                        Return_money = int(nowShare*price[i] - nowShare*buy_price)
                    except:
                        Return_money = 0 #本次運算小到無法表示數值
                    recordDate.append(date[i])
                    Trading_Strategy.append(signal)
                    recordTransaction_Type.append(now_Signal[i])
                    recordStock_price.append(price[i])
                    share.append(nowShare)
                    recordTransaction_amount.append(int(nowShare*price[i]))
                    recordReturn_money.append(Return_money)
                    recordRate_of_Return.append((Return_money/Transaction_amount))      
        
        detail_table = pd.DataFrame({
            "Date" :recordDate,
            "Trading_Strategy":Trading_Strategy, 
            "Transaction_Type":recordTransaction_Type, 
            "Stock_price":recordStock_price, 
            "Share":share,
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
        recordDate, Trading_Strategy, recordTransaction_Type, recordStock_price, share, recordTransaction_amount, recordReturn_money, recordRate_of_Return = [[] for x in range(8)]             
        
        for signal in withSLTP_list[3:]:
            now_Signal = withSLTP[signal].values                 
            buy_price = 0
            nowShare = 0 

            for i in range(len(now_Signal)):
                #record = []
                Transaction_amount = self.Capital * self.Weight[map_group2[signal]]
                if now_Signal[i] == 1:
                    nowShare = int(Transaction_amount/price[i])
                    buy_price = price[i] 
                    recordDate.append(date[i])
                    Trading_Strategy.append(signal)
                    recordTransaction_Type.append(now_Signal[i])
                    recordStock_price.append(price[i])
                    share.append(nowShare)
                    recordTransaction_amount.append(nowShare*price[i])
                    recordReturn_money.append(None)
                    recordRate_of_Return.append(None)                      
                elif now_Signal[i] == -1:
                    try:
                        #Return_money = int((price[i] - buy_price) / buy_price * Transaction_amount)
                        Return_money = int(nowShare*price[i] - nowShare*buy_price)
                    except:
                        Return_money = 0 #本次運算小到無法表示數值
                    recordDate.append(date[i])
                    Trading_Strategy.append(signal)
                    recordTransaction_Type.append(now_Signal[i])
                    recordStock_price.append(price[i])
                    share.append(nowShare)
                    recordTransaction_amount.append(nowShare*price[i])
                    recordReturn_money.append(Return_money)
                    recordRate_of_Return.append((Return_money/Transaction_amount))  

        
        detail_table2 = pd.DataFrame({
            "Date" :recordDate,
            "Trading_Strategy":Trading_Strategy, 
            "Transaction_Type":recordTransaction_Type, 
            "Stock_price":recordStock_price,
            "Share":share, 
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

        if not os.path.exists(f'{self.Path}/Folder_GTSP'):
            os.makedirs(f'{self.Path}/Folder_GTSP')
        if not os.path.exists(f'{self.Path}/Folder_SLTP'):
            os.makedirs(f'{self.Path}/Folder_SLTP')

        map_group1 = self.privateMapping# {'2': MACD^STOCH}:指標2 is MACD^STOCH
        Alltsp:list = self.ADVcombine()
            
        #===================================================Folder_GTSP=================================================== 
        log = {'below-15%':0,'-15%~-11%':0,'-10%~-6%':0,'-5%~-1%':0,
                '0%~5%':0,'6%~10%':0,'11%~15%':0,'MoreThan15%':0,'AvgReturnRate':0
        }
        numTS = 0 #群組交易策略總共數量
        for tsp in Alltsp:
            table = pd.DataFrame()
            
            for i in tsp:
                temp = withoutSLTP_table[withoutSLTP_table["Trading_Strategy"] == map_group1[i-1]]
                table = pd.concat([table,temp],axis = 0)
            table = table.sort_values("Date")
            total_return_money = table['Return_money'].sum()

            ratio = (total_return_money/self.Capital)*100
            if ratio < -15: log['below-15%']+=1
            elif -15 <= ratio < -11: log['-15%~-11%']+=1
            elif -10 <= ratio <  -6: log['-10%~-6%']+=1
            elif  -5 <= ratio <  -1: log['-5%~-1%']+=1
            elif   0 <= ratio <   5: log['0%~5%']+=1
            elif   6 <= ratio <  10: log['6%~10%']+=1
            elif  11 <= ratio <  15: log['11%~15%']+=1
            elif  ratio >  15: log['MoreThan15%']+=1
            numTS +=1
            log['AvgReturnRate'] += total_return_money


            table.reset_index(drop=True, inplace=True)
            table.to_json(f"{self.Path}/Folder_GTSP/{tsp}_{total_return_money}.json", orient='records')
            #table.to_csv(f"{self.Path}/Folder_GTSP/{tsp}.csv",index = False)
        
        log['AvgReturnRate'] = log['AvgReturnRate']/(numTS*self.Capital)
        with open(f"{self.Path}/Folder_GTSP/log.json", "w") as outfile:
            json.dump(log, outfile)
        print("Finished Folder_GTSP\r\n")
        #===================================================Folder_SLTP===================================================    
        log = {'below-15%':0,'-15%~-11%':0,'-10%~-6%':0,'-5%~-1%':0,
                '0%~5%':0,'6%~10%':0,'11%~15%':0,'MoreThan15%':0,'AvgReturnRate':0
        }
        numTS = 0
        for tsp in Alltsp:
            table = pd.DataFrame()
            for i in tsp:
                temp = withSLTP_table[withSLTP_table["Trading_Strategy"] == map_group1[i-1]]
                table = pd.concat([table,temp],axis = 0)
            table = table.sort_values("Date")
            total_return_money = table['Return_money'].sum()

            ratio = (total_return_money/self.Capital)*100
            if ratio < -15: log['below-15%']+=1
            elif -15 <= ratio < -11: log['-15%~-11%']+=1
            elif -10 <= ratio <  -6: log['-10%~-6%']+=1
            elif  -5 <= ratio <  -1: log['-5%~-1%']+=1
            elif   0 <= ratio <   5: log['0%~5%']+=1
            elif   6 <= ratio <  10: log['6%~10%']+=1
            elif  11 <= ratio <  15: log['11%~15%']+=1
            elif  ratio >  15: log['MoreThan15%']+=1
            numTS +=1
            log['AvgReturnRate'] += total_return_money


            table.reset_index(drop=True, inplace=True)
            table.to_json(f"{self.Path}/Folder_SLTP/{tsp}_{total_return_money}.json", orient='records')
            #table.to_csv(f"{self.Path}/Folder_SLTP/{tsp}.csv",index = False)
        
        log['AvgReturnRate'] = log['AvgReturnRate']/(numTS*self.Capital)
        with open(f"{self.Path}/Folder_SLTP/log.json", "w") as outfile:
            json.dump(log, outfile)
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

if __name__ == '__main__':
    obj = BackTesting("2413.TW")
    obj.chosenSignal()
    obj.ProduceTable()
    #obj.Run()
    #obj.Query()
    #print(obj)