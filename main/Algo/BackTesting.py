from numpy import array
import pandas as pd
import json

from Algo.Chromosome import Chromosome


#Manual:
#每次的backTesting調整參數（除了挑整weight可以從RUN跑）
#都要全部重跑拉
#Target:10秒內更新目標資料回傳

class BackTesting():
    def __init__(self, StopLess:float, TakeProfit:float, Chrom:Chromosome, Setting) -> None:
        self.SL = StopLess
        self.TP = TakeProfit
        self.Chrom = Chrom
        
        self.StockID = Setting['StockID']
        self.Path = Setting['Path']
        self.Strategy = Setting['Strategy']
        self.Capital = Setting['Capital']
        self.Strategy = Setting['Strategy']
    
    #def PreBackTesting():
        #DownloadData
        #CalculateTivalue
        #TI2signal
    
    def ProduceTable(self):
        #此function為將買賣signal合併為交易信號，最終結果分為兩個files:
        #1.Table_GTSP.json:為該GTSP的最終交易訊號
        #2.Table_SLTP.josn:為該GTSP的最終交易訊號且具有停損停利之功能
        
        with open(f"{self.Path}/{self.StockID}/ValidationData/Signal.json") as f1, open(f"{self.Path}/{self.StockID}/ValidationData/StockData.json") as f2:
            Signal = pd.read_json(f1)
            Data = pd.read_json(f2)
            
        with open(f'{self.Path}/{self.StockID}/TraningData/{self.Strategy}.json') as s:
            chosenTS = pd.read_json(s) 
          
        Signal_list = Signal.columns
        
        #===================================================Table_GTSP===================================================
        Table = pd.concat([Signal['Date'], Data['close']], axis=1) #create a new table
        for buy in Signal_list[1:]:
            for sell in Signal_list[1:]: 
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
        Keep = chosenTS["Trading Strategy"].values
        Keep = [dontkeep for dontkeep in Table.columns if dontkeep not in Keep]
        del Keep[0:2]  #保留'Date', 'close'
        Table = Table.drop(Keep,axis = 1).reset_index(drop=True)#delete not chosen TS
        
        Table.to_json(f"{self.Path}/{self.StockID}/ValidationData/Table_GTSP.json", orient='records')
        #Table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/Table_GTSP.csv")
        print("Finished Table_GTSP\r\n")  
    

        #===================================================Table_SLTP===================================================
        Table = pd.concat([Signal['Date'], Data['close']], axis=1) #create a new table
        close = Data["close"].values
        
        for buy in Signal_list[1:]:
            for sell in Signal_list[1:]: 
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
                

        Keep = chosenTS["Trading Strategy"].values
        Keep = [dontkeep for dontkeep in Table.columns if dontkeep not in Keep]
        del Keep[0:2]  #保留'Date', 'close'
        Table = Table.drop(Keep,axis = 1).reset_index(drop=True)#delete not chosen TS
        
        Table.to_json(f"{self.Path}/{self.StockID}/ValidationData/Table_SLTP.json", orient='records')
        #Table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/Table_SLTPP.csv")
        print("Finished Table_SLTP\r\n")
         
    def Run(self): 
        #約花34秒
        #此function為將買賣signal合併為交易信號，最終結果分為三個files:
        #1.Buy&Hold.json:為該區間使用B&H的效果(目的是為了比對GTSP系統是否有效果)
        #2.Detail_GTSP.json:為該GTSP的最終交易訊號
        #3.Detail_SLTP.josn:為該GTSP的最終交易訊號且具有停損停利之功能
        
        with open(f'{self.Path}/{self.StockID}/ValidationData/Table_GTSP.json') as f1, open(f'{self.Path}/{self.StockID}/ValidationData/Table_SLTP.json') as f2:
            withoutSLTP = pd.read_json(f1)
            withSLTP = pd.read_json(f2)
        with open(f'{self.Path}/{self.StockID}/TraningData/{self.Strategy}.json') as s:
            chosenTS = pd.read_json(s) 
        
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
        with open(f'{self.Path}/{self.StockID}/ValidationData/Buy&Hold.json', "w") as outfile:
            json.dump(buy_and_hold, outfile)
        
                
        #define map_group:用來mapping data
        map_group1 = dict(chosenTS["Trading Strategy"])
        # {'2': MACD^STOCH}:指標2 is MACD^STOCH
        map_group2 = {value:key for key,value in map_group1.items()}
        # {'MACD^STOCH': 2}:MACD^STOCH is 指標2
        
        map = {}
        num = 0
        for i in self.Chrom.gene[:self.Chrom.mTS + self.Chrom.kGroup]:
            if i == 0:
                num += 1
            else:
                map[f"{i-1}"] = num
        for i in map_group2:
            index = map_group2[f"{i}"]
            map_group2[f"{i}"] = map[f"{index}"]
        
        
        
        #===================================================Detail_GTSP===================================================
        withoutSLTP_list = withoutSLTP.columns               
        
        #record用column方式並起來
        recordDate, Trading_Strategy, recordTransaction_Type, recordStock_price, recordTransaction_amount, recordReturn_money, recordRate_of_Return = [[] for x in range(7)]

        for signal in withoutSLTP_list[3:]:
            now_Signal = withoutSLTP[signal].values                 
            buy_price = 0 
            weight = self.Chrom.getWeight()

            for i in range(len(now_Signal)):
                record = []
                Transaction_amount = self.Capital * weight[map_group2[signal]]
                if now_Signal[i] == 1:
                    buy_price = price[i] 
                    #record = [date[i], signal, now_Signal[i], price[i], Transaction_amount, None, None]
                    recordDate.append(date[i])
                    Trading_Strategy.append(signal)
                    recordTransaction_Type.append(now_Signal[i])
                    recordStock_price.append(price[i])
                    recordTransaction_amount.append(Transaction_amount)
                    recordReturn_money.append(None)
                    recordRate_of_Return.append(None)          
                elif now_Signal[i] == -1:
                    Return_money = int((price[i] - buy_price) / buy_price * Transaction_amount)
                    #record = [date[i], signal, now_Signal[i], price[i], Transaction_amount, Return_money, (Return_money/Transaction_amount)]
                    recordDate.append(date[i])
                    Trading_Strategy.append(signal)
                    recordTransaction_Type.append(now_Signal[i])
                    recordStock_price.append(price[i])
                    recordTransaction_amount.append(Transaction_amount)
                    recordReturn_money.append(Return_money)
                    recordRate_of_Return.append((Return_money/Transaction_amount))      
                #record = pd.DataFrame(record)
                #detail_table = pd.concat([detail_table , record.T], axis=0)
        
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
        detail_table.to_json(f"{self.Path}/{self.StockID}/ValidationData/Detail_GTSP.json", orient='records')
        #detail_table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/Detail_GTSP.csv")
        print("Finished Detail_GTSP\r\n")
        
        
        #===================================================Detail_SLTP===================================================
        withSLTP_list = withSLTP.columns

        #record用column方式並起來
        recordDate, Trading_Strategy, recordTransaction_Type, recordStock_price, recordTransaction_amount, recordReturn_money, recordRate_of_Return = [[] for x in range(7)]             
        
        for signal in withSLTP_list[3:]:
            now_Signal = withSLTP[signal].values                 
            buy_price = 0 
            weight = self.Chrom.getWeight()

            for i in range(len(now_Signal)):
                record = []
                Transaction_amount = self.Capital * weight[map_group2[signal]]
                if now_Signal[i] == 1:
                    buy_price = price[i] 
                    #record = [date[i], signal, now_Signal[i], price[i], Transaction_amount, None, None]
                    recordDate.append(date[i])
                    Trading_Strategy.append(signal)
                    recordTransaction_Type.append(now_Signal[i])
                    recordStock_price.append(price[i])
                    recordTransaction_amount.append(Transaction_amount)
                    recordReturn_money.append(None)
                    recordRate_of_Return.append(None)                      
                elif now_Signal[i] == -1:
                    Return_money = int((price[i] - buy_price) / buy_price * Transaction_amount)
                    #record = [date[i], signal, now_Signal[i], price[i], Transaction_amount, Return_money, (Return_money/Transaction_amount)]
                    recordDate.append(date[i])
                    Trading_Strategy.append(signal)
                    recordTransaction_Type.append(now_Signal[i])
                    recordStock_price.append(price[i])
                    recordTransaction_amount.append(Transaction_amount)
                    recordReturn_money.append(Return_money)
                    recordRate_of_Return.append((Return_money/Transaction_amount))  
                #record = pd.DataFrame(record)
                #detail_table2 = pd.concat([detail_table2 , record.T], axis=0)
        
        detail_table2 = pd.DataFrame({
            "Date" :recordDate,
            "Trading_Strategy":Trading_Strategy, 
            "Transaction_Type":recordTransaction_Type, 
            "Stock_price":recordStock_price, 
            "Transaction_amount":recordTransaction_amount, 
            "Return_money":recordReturn_money, 
            "Rate_of_Return":recordRate_of_Return
        }) 

        #detail_table2.columns = ["Date", "Trading_Strategy", "Transaction_Type", "Stock_price", "Transaction_amount", "Return_money", "Rate_of_Return"]
        detail_table2.reset_index(drop=True, inplace=True)
        detail_table2.to_json(f"{self.Path}/{self.StockID}/ValidationData/Detail_SLTP.json", orient='records')
        #detail_table2.to_csv(f"{self.Path}/{self.StockID}/ValidationData/Detail_SLTP.csv")
        print("Finished Detail_SLTP\r\n")
     
    def Query(self):
        #將所有可能組合出來放入Folder:
        #1.Folder_GTSP:存放該GTSP交易明細所有組合之資料夾
        #2.Folder_SLTP:存放該GTSP且具有SLTP功能之交易明細所有組合之資料夾
        with open(f'{self.Path}/{self.StockID}/ValidationData/Detail_GTSP.json') as f1,open(f'{self.Path}/{self.StockID}/ValidationData/Detail_SLTP.json') as f2:
            withoutSLTP_table = pd.read_json(f1)
            withSLTP_table = pd.read_json(f2)
        with open(f'{self.Path}/{self.StockID}/TraningData/{self.Strategy}.json') as s:
            chosenTS = pd.read_json(s) 
        map_group1 = dict(chosenTS["Trading Strategy"])#{'2': MACD^STOCH}
        Alltsp:list = self.Chrom.ADVcombine()
            
        #===================================================Folder_GTSP=================================================== 
        for tsp in Alltsp:
            table = pd.DataFrame()
            
            for i in tsp:
                temp = withoutSLTP_table[withoutSLTP_table["Trading_Strategy"] == map_group1[i-1]]
                table = pd.concat([table,temp],axis = 0)
            table = table.sort_values("Date")
            total_return_money = table['Return_money'].sum()

            table.reset_index(drop=True, inplace=True)
            table.to_json(f"{self.Path}/{self.StockID}/ValidationData/Folder_GTSP/{tsp}_{total_return_money}.json", orient='records')
            #table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/Folder_GTSP/{tsp}.csv",index = False)
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
            table.to_json(f"{self.Path}/{self.StockID}/ValidationData/Folder_SLTP/{tsp}_{total_return_money}.json", orient='records')
            #table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/Folder_SLTP/{tsp}.csv",index = False)
                        
        print("Finished Folder_SLTP\r\n")

if __name__ == "__main__":
    #獨立執行 測試用
    import cProfile
    #ini  = Algo.BackTesting.BackTesting(0.01,0.01,population.Chrom[0],Setting = Setting)
    #之後補GTSP
    #ini.ProduceTable()
    #ini.Run()
    #ini.Query()


    #a = pd.DataFrame(json.load(f))
    print()