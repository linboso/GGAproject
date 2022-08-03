from ast import Return
from sqlite3 import Date
from ssl import SSLWantReadError
from numpy import array
import pandas as pd
import json
from Algo.Chromosome import Chromosome

# from .Chromosome import Chromosome


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
        map_group1 = dict(chosenTS["Trading Strategy"])
        map_group2 = {value:key for key,value in map_group1.items()}#key value change

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

        print(map_group2)


        #table setting
        withoutSLSP_list = withoutSLSP.columns               
        detail_table = pd.DataFrame()
        date = withoutSLSP["Date"].values
        price = withoutSLSP["close"].values
        
        for signal in withoutSLSP_list[3:]:
                now_Signal = withoutSLSP[signal].values                 
                buy_price = 0 
                weight = self.Chrom.getWeight() #到時候用chromosome.getWeight()

                for i in range(len(now_Signal)):
                    record = []
                    Transaction_amount = self.Capital * weight[map_group2[signal]]
                    if now_Signal[i] == 1:
                        buy_price = price[i]                      
                        record.extend([date[i], signal, now_Signal[i], price[i], Transaction_amount, None, None])
                    elif now_Signal[i] == -1:
                        Return_money = int((price[i] - buy_price) / buy_price * Transaction_amount)
                        record.extend([date[i], signal, now_Signal[i], price[i], Transaction_amount, Return_money, Return_money/Transaction_amount])
                    record = pd.DataFrame(record)
                    detail_table = pd.concat([detail_table , record.T], axis=0)
                
        detail_table.columns = ["Date", "Trading_strategy", "Transaction_Type", "Stock_price", "Transaction_amount", "Return_money", "Rate_of_Return"]
        #detail_table.to_json(f"{self.Path}/{self.StockID}/ValidationData/detail_table.json", orient='records')
        detail_table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/detail_table.csv")
        print("Finished detail_Table\r\n")
         
        #to do-list:
        #query this table by what u want
    
    def Query(self):
        with open(f'{self.Path}/{self.StockID}/ValidationData/detail_table.csv') as f:
            detail_table = pd.read_csv(f)
        """Alltsp:list = self.Chrom.__ADVcombine() #I dunno why I cannot compile this
        tsplen:int = len(Alltsp)
        for tsp in Alltsp:
            table = pd.DataFrame()
            for i in tsp:
                temp = detail_table[detail_table["Trading Strategy"] == f"{i}"]
                table = pd.concat([table,temp],axis = 0)
            table.sort_values("Date")
            table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/folder/{tsp}.csv")
        
        print("finished all backtesting works")"""


if __name__ == '__main__':
    #import os

    #print(f"{os.path}")

    #with open(f'../../data/stock/0050.TW/ValidationData/StockData.json') as f:
        #VaildationData = pd.read_json(f)
    
    #print(VaildationData)

    #a = pd.DataFrame(json.load(f))
    print()