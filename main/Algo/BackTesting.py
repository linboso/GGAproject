from ast import Return
from sqlite3 import Date
from ssl import SSLWantReadError
from numpy import array
import pandas as pd
import json

# from .Chromosome import Chromosome


class BackTesting():
    def __init__(self, StopLess:float, TakeProfit:float, GTSP:array, Setting) -> None:
        self.SL = StopLess
        self.TP = TakeProfit
        self.GTSP = GTSP
        
        self.StockID = Setting['StockID']
        self.Path = Setting['Path']
        self.Strategy = Setting['Strategy']
        self.Capital = Setting['Capital']
        self.Strategy = Setting['Strategy']
    
    def ProduceTable(self):
        #Without_SLSP
        with open(f"{self.Path}/{self.StockID}/ValidationData/Signal.json") as f1, open(f"{self.Path}/{self.StockID}/ValidationData/StockData.json") as f2:
            Signal = pd.read_json(f1)
            Data = pd.read_json(f2)

        Signal_list = Signal.columns
        Table = pd.concat([Signal['Date'], Data['close']], axis=1)
        

        for buy in Signal_list[1:]:
            for sell in Signal_list[1:]: 
                Buy_Signal = Signal[buy].values   
                Sell_Signal = Signal[sell].values 
                
                New_Signal = []
                Flag:bool = False
                for i in range(len(Buy_Signal)):
                    if Buy_Signal[i] == 1 and Sell_Signal[i] == -1:
                        if Flag:
                            New_Signal.append(-1)
                            Flag = False
                        else:
                            New_Signal.append(1)
                            Flag = True
                    elif Buy_Signal[i] == 1 and not Flag:
                        New_Signal.append(1)
                        Flag = True
                    elif Sell_Signal[i] == -1 and Flag:
                        New_Signal.append(-1)
                        Flag = False
                    else:
                        New_Signal.append(0)

                New_Signal = pd.DataFrame(New_Signal)
                New_Signal.columns = [f"{buy}^{sell}"]
                Table = pd.concat([Table, New_Signal], axis=1)
                

                #By training data choosing TS
        with open(f'{self.Path}/{self.StockID}/TraningData/{self.Strategy}.json') as s:
            chosenTS = pd.read_json(s) 
        Keep = chosenTS["Trading Strategy"].values
        Keep = [dontkeep for dontkeep in Table.columns if dontkeep not in Keep]
        del Keep[0:2]  #保留'Date', 'close'
        Table = Table.drop(Keep,axis = 1).reset_index(drop=True)#delete not chosen TS
        #Table.to_json(f"{self.Path}/{self.StockID}/ValidationData/Table_withoutSLSP.json", orient='records')
        Table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/Table_withoutSLSP.csv")

        print("Finished Producing Table_withoutSLSP\r\n")  
        #With_SLSP    
           
    def Run(self):   
        with open(f'{self.Path}/{self.StockID}/ValidationData/Table_withoutSLSP.csv') as f:
            withoutSLSP = pd.read_csv(f)
        with open(f'{self.Path}/{self.StockID}/TraningData/{self.Strategy}.json') as s:
            chosenTS = pd.read_json(s) 
        map_group = dict(chosenTS["Trading Strategy"])
        map_group = {value:key for key,value in map_group.items()}#key value change
        #print(map_group)


        #table setting
        withoutSLSP_list = withoutSLSP.columns               
        detail_table = pd.DataFrame()
        date = withoutSLSP["Date"].values
        price = withoutSLSP["close"].values
        
        for signal in withoutSLSP_list[2:]:
                now_Signal = withoutSLSP[signal].values                 
                buy_price = 0 
                weight = [0.25, 0.25, 0.25, 0.25] #到時候用chromosome.getWeight()

                for i in range(len(now_Signal)):
                    record = []
                    if now_Signal[i] == 1:
                        buy_price = price[i]
                        record.extend([date[i], signal, now_Signal[i], price[i], self.Capital, None, None])
                    elif now_Signal[i] == -1:
                        Return_money = (price[i] - buy_price) / buy_price * self.Capital
                        record.extend([date[i], signal, now_Signal[i], price[i], self.Capital, Return_money, Return_money/10000])
                    record = pd.DataFrame(record)
                    detail_table = pd.concat([detail_table , record.T], axis=0)
                
        detail_table.columns = ["Date", "Trading_strategy", "Type", "Stock_price", "Money", "Return_money", "Rate_of_Return"]
        #detail_table = detail_table.sort_values(["Date"],ascending = True)
        #detail_table.to_json(f"{self.Path}/{self.StockID}/ValidationData/detail_table.json", orient='records')
        detail_table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/detail_table.csv")
        print("Finished detail_Table\r\n")
        #print(self.Capital)
        #print(self.GTSP)
        #to do-list:
        #query this table by what u want
     


if __name__ == '__main__':
    #import os

    #print(f"{os.path}")

    #with open(f'../../data/stock/0050.TW/ValidationData/StockData.json') as f:
        #VaildationData = pd.read_json(f)
    
    #print(VaildationData)

    #a = pd.DataFrame(json.load(f))
    print()