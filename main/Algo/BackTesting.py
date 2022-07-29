from ssl import SSLWantReadError
import pandas as pd
import json

# from .Chromosome import Chromosome


class BackTesting():
    def __init__(self, StopLess:float, TakeProfit:float, Setting) -> None:
        self.SL = StopLess
        self.TP = TakeProfit
        #self.GTSP = GTSP
        
        self.StockID = Setting['StockID']
        self.Path = Setting['Path']
        self.Strategy = Setting['Strategy']
        self.Capital = Setting['Capital']
        self.Strategy = Setting['Strategy']
    
    def ProduceTable_withoutSLSP(self):
        with open(f"{self.Path}/{self.StockID}/ValidationData/Signal.json") as f1, open(f"{self.Path}/{self.StockID}/ValidationData/StockData.json") as f2:
            Signal = pd.read_json(f1)
            Data = pd.read_json(f2)

        Signal_list = Signal.columns
        Table = pd.concat([Signal['Date'], Data['close']], axis=1)
        

        for buy in Signal_list[1:]:
            #print(f"========= {buy} =========")
            for sell in Signal_list[1:]: 
                Buy_Signal = Signal[buy].values   # pd.Series to list
                Sell_Signal = Signal[sell].values # 在小資料的情況下 List 的計算速度比 numpy.array 快
                
                New_Signal = []
                Flag:bool = False
                for i in range(len(Buy_Signal)):
                    if Buy_Signal[i] == 1 and Sell_Signal[i] == -1:
                        if Flag:
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
                #Table.to_json(f"{self.Path}/{self.StockID}/ValidationData/Table_withoutSLSP.json", orient='records')
                Table.to_csv(f"{self.Path}/{self.StockID}/ValidationData/Table_withoutSLSP.csv")
                #print(f"==> {sell}")
            #print()

        print("Finished Producing Table_withoutSLSP\r\n")        

    #def ProduceTable_withSLSP(self):

    def Run(self):
        with open(f'{self.Path}/{self.StockID}/TraningData/{self.Strategy}.json') as s:
            chosenTS = pd.read_json(s)        

        with open(f'{self.Path}/{self.StockID}/ValidationData/Table_withoutSLSP.csv') as f:
            withoutSLSP = pd.read_csv(f)    

        Keep = chosenTS["Trading Strategy"].values
        Keep = [dontkeep for dontkeep in withoutSLSP.columns if dontkeep not in Keep]
        del Keep[1:3]  #保留'Date', 'close'
        print(withoutSLSP.columns)
        print(Keep)
        withoutSLSP = withoutSLSP.drop(Keep,axis = 1).reset_index(drop=True)#delete not chosen TS
        print(withoutSLSP.columns)
        withoutSLSP.to_csv(f"{self.Path}/{self.StockID}/ValidationData/Table_withoutSLSP.csv")
        
        #to do-list:
        #read by 1 or -1 to create new table called transaction details
        #then sorted by date
        #query this table by what u want
    


if __name__ == '__main__':
    #import os

    #print(f"{os.path}")

    #with open(f'../../data/stock/0050.TW/ValidationData/StockData.json') as f:
        #VaildationData = pd.read_json(f)
    
    #print(VaildationData)

    #a = pd.DataFrame(json.load(f))
    print()