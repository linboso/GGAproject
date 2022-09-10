from ast import Return
from sqlite3 import Date
from ssl import SSLWantReadError
from numpy import array
import pandas as pd
import json

from sqlalchemy import false
from Algo.Chromosome import Chromosome


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
    
    def ProduceTable(self):
        
        with open(f"{self.Path}/{self.StockID}/ValidationData/Signal.json") as f1, open(f"{self.Path}/{self.StockID}/ValidationData/StockData.json") as f2:
            Signal = pd.read_json(f1)
            Data = pd.read_json(f2)
            
        with open(f'{self.Path}/{self.StockID}/TraningData/{self.Strategy}.json') as s:
            chosenTS = pd.read_json(s) 
                        
        Signal_list = Signal.columns
        
        
        #Without_SLTP
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
        
        Table.to_json(f"{self.Path}/{self.StockID}/ValidationData/Table_withoutSLTP.json", orient='records')
        #Table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/Table_withoutSLTP.csv")
        print("Finished Producing Table_withoutSLTP\r\n")  
    

        #With_SLTP
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
        
        Table.to_json(f"{self.Path}/{self.StockID}/ValidationData/Table_withSLTP.json", orient='records')
        #Table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/Table_withSLTP.csv")
        print("Finished Producing Table_withSLTP\r\n")
         
    def Run(self):   
        with open(f'{self.Path}/{self.StockID}/ValidationData/Table_withoutSLTP.json') as f1, open(f'{self.Path}/{self.StockID}/ValidationData/Table_withSLTP.json') as f2:
            withoutSLTP = pd.read_json(f1)
            withSLTP = pd.read_json(f2)
        with open(f'{self.Path}/{self.StockID}/TraningData/{self.Strategy}.json') as s:
            chosenTS = pd.read_json(s) 
        
        price = withoutSLTP["close"].values    
        date  = withoutSLTP["Date"].values       
        
        
        #define map_group
        map_group1 = dict(chosenTS["Trading Strategy"])# {'2': MACD^STOCH}
        map_group2 = {value:key for key,value in map_group1.items()}#key value change {'MACD^STOCH': 2}
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
        #print(map_group2)
 
        
        #Buy and Hold strategy
        bh_return_rate = (price[-1] - price[0])/price[0]
        bh_return_money = bh_return_rate * self.Capital
        buy_and_hold = {
          "Date": f"{date[0]} ~ {date[-1]}",
          "return_rate": bh_return_rate,
          "return_money": bh_return_money,
        }
        with open(f'{self.Path}/{self.StockID}/ValidationData/buy_and_hold.json', "w") as outfile:
            json.dump(buy_and_hold, outfile)
        

        #withoutSLTP
        withoutSLTP_list = withoutSLTP.columns               
        detail_table = pd.DataFrame()
        
        for signal in withoutSLTP_list[3:]:
            now_Signal = withoutSLTP[signal].values                 
            buy_price = 0 
            weight = self.Chrom.getWeight()

            for i in range(len(now_Signal)):
                record = []
                Transaction_amount = self.Capital * weight[map_group2[signal]]
                if now_Signal[i] == 1:
                    buy_price = price[i] 
                    record = [date[i], signal, now_Signal[i], price[i], Transaction_amount, None, None]            
                elif now_Signal[i] == -1:
                    Return_money = int((price[i] - buy_price) / buy_price * Transaction_amount)
                    record = [date[i], signal, now_Signal[i], price[i], Transaction_amount, Return_money, (Return_money/Transaction_amount)]
                record = pd.DataFrame(record)
                detail_table = pd.concat([detail_table , record.T], axis=0)
                
        detail_table.columns = ["Date", "Trading_Strategy", "Transaction_Type", "Stock_price", "Transaction_amount", "Return_money", "Rate_of_Return"]
        detail_table.reset_index(drop=True, inplace=True)
        detail_table.to_json(f"{self.Path}/{self.StockID}/ValidationData/withoutSLTP_detail.json", orient='records')
        #detail_table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/withoutSLTP_detail.csv")
        print("Finished withoutSLTP_table\r\n")
        
        
        #withSLTP
        withSLTP_list = withSLTP.columns               
        detail_table2 = pd.DataFrame()
        
        for signal in withSLTP_list[3:]:
            now_Signal = withSLTP[signal].values                 
            buy_price = 0 
            weight = self.Chrom.getWeight()

            for i in range(len(now_Signal)):
                record = []
                Transaction_amount = self.Capital * weight[map_group2[signal]]
                if now_Signal[i] == 1:
                    buy_price = price[i] 
                    record = [date[i], signal, now_Signal[i], price[i], Transaction_amount, None, None]                     
                elif now_Signal[i] == -1:
                    Return_money = int((price[i] - buy_price) / buy_price * Transaction_amount)
                    record = [date[i], signal, now_Signal[i], price[i], Transaction_amount, Return_money, (Return_money/Transaction_amount)]
                record = pd.DataFrame(record)
                detail_table2 = pd.concat([detail_table2 , record.T], axis=0)
                
        detail_table2.columns = ["Date", "Trading_Strategy", "Transaction_Type", "Stock_price", "Transaction_amount", "Return_money", "Rate_of_Return"]
        detail_table2.reset_index(drop=True, inplace=True)
        detail_table2.to_json(f"{self.Path}/{self.StockID}/ValidationData/withSLTP_detail.json", orient='records')
        #detail_table2.to_csv(f"{self.Path}/{self.StockID}/ValidationData/withSLTP_detail.csv")
        print("Finished withSLTP_table\r\n")

    
    def Query(self):
        with open(f'{self.Path}/{self.StockID}/ValidationData/withoutSLTP_detail.json') as f1,open(f'{self.Path}/{self.StockID}/ValidationData/withSLTP_detail.json') as f2:
            withoutSLTP_table = pd.read_json(f1)
            withSLTP_table = pd.read_json(f2)
        with open(f'{self.Path}/{self.StockID}/TraningData/{self.Strategy}.json') as s:
            chosenTS = pd.read_json(s) 
        map_group1 = dict(chosenTS["Trading Strategy"])#{'2': MACD^STOCH}
        Alltsp:list = self.Chrom.ADVcombine()
            
        #withoutSLTP    
        for tsp in Alltsp:
            table = pd.DataFrame()
            for i in tsp:
                temp = withoutSLTP_table[withoutSLTP_table["Trading_Strategy"] == map_group1[i-1]]
                table = pd.concat([table,temp],axis = 0)
            table = table.sort_values("Date")

            table.reset_index(drop=True, inplace=True)
            table.to_json(f"{self.Path}/{self.StockID}/ValidationData/withoutSLTP_folder/{tsp}.json", orient='records')
            #table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/withoutSLTP_folder/{tsp}.csv",index = False)

        #withSLTP    
        for tsp in Alltsp:
            table = pd.DataFrame()
            for i in tsp:
                temp = withSLTP_table[withSLTP_table["Trading_Strategy"] == map_group1[i-1]]
                table = pd.concat([table,temp],axis = 0)
            table = table.sort_values("Date")

            table.reset_index(drop=True, inplace=True)
            table.to_json(f"{self.Path}/{self.StockID}/ValidationData/withSLTP_folder/{tsp}.json", orient='records')
            #table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/withSLTP_folder/{tsp}.csv",index = False)
            
            
        print("Finished all backtesting works")


if __name__ == '__main__':
    #import os

    #print(f"{os.path}")

    #with open(f'../../data/stock/0050.TW/ValidationData/StockData.json') as f:
        #VaildationData = pd.read_json(f)
    
    #print(VaildationData)

    #a = pd.DataFrame(json.load(f))
    print()