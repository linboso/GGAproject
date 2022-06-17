import pandas as pd
import json

# from .Chromosome import Chromosome


class BackTesting():
    def __init__(self, StopLess:float, TakeProfit:float, GTSP, Setting) -> None:
        self.SL = StopLess
        self.TP = TakeProfit
        self.GTSP = GTSP
        
        self.StockID = Setting['StockID']
        self.Path = Setting['Path']
        self.Strategy = Setting['Strategy']
        self.Capital = Setting['Capital']

    def Run(self):
        with open(f'{self.Path}/{self.StockID}/ValidationData/StockData.json') as f:
            VaildationData = pd.read_json(f)
            a = pd.DataFrame(json.load(f))
            
        print(VaildationData)
        print(a)




if __name__ == '__main__':
    import os

    print(f"{os.path}")

    with open(f'../../data/stock/0050.TW/ValidationData/StockData.json') as f:
            VaildationData = pd.read_json(f)
            print(VaildationData)

            # a = pd.DataFrame(json.load(f))
            # print(a)
