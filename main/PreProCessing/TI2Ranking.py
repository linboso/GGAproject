import dask
import pandas as pd
import numpy as np

from dask.distributed import Client, LocalCluster

class TI2Ranking():
    def __init__(self):
        pass

    def RankingSort(self, Collect:np.array, ColName:list, HowMuch:int):
    #   Collect  =  [ARR, MDD, TF] 
        Select = []
        for Col in range(3):
            count = 0
            for Top in np.argsort(-Collect[:, Col]): # descending order
                if count == HowMuch:
                    break
                if Top not in Select:
                    Select.append(Top)
                    count += 1
                    
        return Collect[Select], ColName[Select]
    
    def Run(self, Signal, ClosePrice, ThreadNumbers):
        
        m, n = np.shape(Signal)[0], np.shape(Signal)[1] 
        # row, col
        cluster = LocalCluster(n_workers=ThreadNumbers, threads_per_worker=1)  
        # client = Client(cluster, asynchronous=True)
        client = Client(cluster, asynchronous=False)
        # 建立 Workers 
        
        Signal = client.scatter(Signal, broadcast=True)
        Tables, ColName = self.CalculateTable(Signal, m, n)
        
        Tables = client.scatter(Tables, broadcast=True)
        ColName = client.scatter(ColName, broadcast=True)
        ClosePrice = client.scatter(ClosePrice, broadcast=True)
        
        CombineRankTable, ColName = self.CalculateRanking(n, Tables, ColName, ClosePrice)
        
        self.Table = CombineRankTable
        self.ColName = ColName

    def CalculateTable(self, Signal, m, n):    
        def Signal2LargeTable(Signal, Buy, m, n):
            
            Table = np.zeros((m, n), dtype=np.int0)
            BuySignal = Signal[:, Buy]
            ColName = np.empty(n ,dtype=object)
            
            for Sell in range(n):
                SellSignal = Signal[:, Sell]
                Flag:bool = False
                for i in range(m):
                    if BuySignal[i] == 1 and SellSignal[i] == 1:
                        if Flag:
                            Table[i][Sell] = -1
                            Flag = False
                        else:
                            Table[i][Sell] = 1
                            Flag = True
                    elif (not Flag) and BuySignal[i] == 1:
                        Table[i][Sell] = 1
                        Flag = True
                    elif Flag and SellSignal[i] == -1:
                        Table[i][Sell] = -1
                        Flag = False
                ColName[Sell] = (Buy, Sell)

            return Table, ColName
    
        delayObject = [dask.delayed(Signal2LargeTable)(Signal, buy, m, n) for buy in range(n)]

        delayObject = dask.compute(*delayObject)
        Tables, ColName = zip(*delayObject)
        
        del delayObject
        return Tables, ColName

    def CalculateRanking(self, n, Tables, ColNames, ClosePrice):
        def Ranking(BuyDay:np.array, SellDay:np.array, ClosePrice:np.array) -> list:
            b, s = 0, 0
            blen = len(BuyDay)
            slen = len(SellDay)
            returnRate = []
            Flag = False
            # buyPrice = 0
            while b < blen and s < slen:
                if not Flag and BuyDay[b] < SellDay[s]:
                    buyPrice = ClosePrice[BuyDay[b]]
                    Flag = True
                if Flag:
                    returnRate.append((ClosePrice[SellDay[s]] - buyPrice) / buyPrice)
                    Flag = False
                if BuyDay[b] > SellDay[s]:
                    s += 1
                else:
                    b += 1
                    
            return  returnRate
        
        def Collects(n:int, Table:np.array, ClosePrice:np.array) -> np.array:
            Collect = np.empty((n, 3))
            
            for Col in range(n):
                BuyDay:np.array = np.where(Table[:, Col] == 1)[0]
                SellDay:np.array = np.where(Table[:, Col] == -1)[0]

                returnRate = Ranking(BuyDay, SellDay, ClosePrice)

                TF:int = len(returnRate)    #交易次數
                ARR:float = 0               #Average Return Rate
                MDD:float = 0               #最大回落
                if TF != 0:
                    MDD = min(returnRate)
                    ARR = sum(returnRate) / TF
                else:
                    MDD = 0
                Collect[Col] = [ARR, MDD, TF]
            
            return Collect

        def Topxxx(Table, n, ClosePrice, ColName):
            Collect = Collects(n, Table, ClosePrice)
            return self.RankingSort(Collect, ColName, 21)
        # 不在這邊做分類
        
        delayObject = [dask.delayed(Topxxx)(Table, n, ClosePrice, Cname) for Table, Cname in zip(Tables, ColNames)]
        delayObject = dask.compute(*delayObject)
        
        
        MultiRankTable, ColName = zip(*delayObject)
        del delayObject
        
        CombineRankTable = np.concatenate(MultiRankTable)
        ColName = np.concatenate(ColName)
        # 把所有 RankTable 合併

        return CombineRankTable, ColName
    
    def MaxMinNormal(self, array:np.array) -> np.array:
        __min = np.min(array)
        return (array - __min) / (np.max(array) - __min)

    def Top555(self, Path) -> np.array:
        CombineTop = self.Table
        ColName = self.ColName
        
        CombineTop, ColName = self.RankingSort(CombineTop, ColName, 5)
        CombineTop[:, 1] = self.MaxMinNormal(CombineTop[:, 1]) 

        CombineTop = np.concatenate((ColName[:,np.newaxis], CombineTop), axis=1)
        CombineTop = pd.DataFrame(CombineTop, columns=["Trading Strategy","ARR", "MDD", "TF"])
        CombineTop.to_json(f"{Path}/Top555.json", orient="columns")
        return CombineTop

    def Top15(self, Path) -> np.array:
        CombineTop = self.Table
        ColName = self.ColName
        
        CombineTop, ColName = self.RankingSort(CombineTop, ColName, 15)
        CombineTop = np.concatenate((ColName[:,np.newaxis], CombineTop), axis=1)
        
        CombineTop = CombineTop[:,:][:15]
        # 保留前 15 筆資料
        CombineTop = pd.DataFrame(CombineTop, columns=["Trading Strategy","ARR", "MDD", "TF"])
        CombineTop.to_json(f"{Path}/Top15.json", orient="columns")
        return CombineTop
        
    def Top777(self, Path) -> np.array:
        CombineTop = self.Table
        ColName = self.ColName
        
        CombineTop, ColName = self.RankingSort(CombineTop, ColName, 7)
        CombineTop[:, 1] = self.MaxMinNormal(CombineTop[:, 1]) 

        CombineTop = np.concatenate((ColName[:,np.newaxis], CombineTop), axis=1)
        CombineTop = pd.DataFrame(CombineTop, columns=["Trading Strategy","ARR", "MDD", "TF"])
        CombineTop.to_json(f"{Path}/Top777.json", orient="columns")
        return CombineTop
    
    def Top21(self, Path) -> np.array:
        CombineTop = self.Table
        ColName = self.ColName
        
        CombineTop, ColName = self.RankingSort(CombineTop, ColName, 21)
        CombineTop = np.concatenate((ColName[:,np.newaxis], CombineTop), axis=1)
        
        CombineTop = CombineTop[:,:][:21]

        CombineTop = pd.DataFrame(CombineTop, columns=["Trading Strategy","ARR", "MDD", "TF"])
        CombineTop.to_json(f"{Path}/Top21.json", orient="columns")
        return CombineTop

if __name__ == "__main__":
    import time
    
    s = time.time() 
    
    SignalSource = pd.read_json("Signal.json").to_numpy()
    ClosePrice = pd.read_json("StockData.json")['close'].to_numpy()
 
    rk = TI2Ranking()
    rk.Run(SignalSource, ClosePrice)
    rk.Top777("tmp/")
    
    
    e = time.time() 
    
    print(f"F time: {e-s}")
    
    
    