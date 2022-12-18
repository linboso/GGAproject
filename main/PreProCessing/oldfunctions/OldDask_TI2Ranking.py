import dask
import pandas as pd
import numpy as np

from dask.distributed import Client, LocalCluster

# cluster = LocalCluster(n_workers=16, threads_per_worker=1)  
# cluster = LocalCluster(processes=True)
# client = await Client(cluster, asynchronous=True)


def CalculateTable(Signal, n, m):
    delayObject = [dask.delayed(Signal2LargeTable)(Signal, buy, n, m) for buy in range(n)]
    delayObject = dask.compute(*delayObject)
    Tables, ColName = zip(*delayObject)
    
    del delayObject
    return Tables, ColName

def CalculateRanking(RankingType, n, Tables, ColName, ClosePrice):
    delayObject = [dask.delayed(RankingType)(Table, n, ClosePrice, Cname) for Table, Cname in zip(Tables, ColName)]
    delayObject = dask.compute(*delayObject)

    MultiTable, ColName = zip(*delayObject)
    
    del delayObject
    return MultiTable, ColName



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


def RankingSort(Collect:np.array , ColName:list, HowMuch:int):
    #   Collect  =  [ARR, MDD, TF] 
    Select = []
    for Col in range(np.shape(Collect)[1]):
        count = 0
        for Top in np.argsort(-Collect[:, Col]): #Sorting descending
            if count == HowMuch:
                break
            if Top not in Select:
                Select.append(Top)
                count += 1
                
    return Collect[Select], ColName[Select]


def MaxMinNormal(array:np.array) -> np.array:
    __min = np.min(array)
    return (array - __min) / (np.max(array) - __min)


def Top555(Table, n, ClosePrice, ColName):
    Collect = Collects(n, Table, ClosePrice)
    return RankingSort(Collect, ColName, 5)
 
def Top15(Table, n, ClosePrice, ColName):
    Collect = Collects(n, Table, ClosePrice)['ARR'] 
    # 只保留 ARR
    return RankingSort(Collect, ColName, 15) 


import time
import json
# 如果想分析 用jupyterlab 比較快理解


if __name__ == "__main__":
    s = time.time()
    cluster = LocalCluster(n_workers=16, threads_per_worker=1)  
    client = Client(cluster, asynchronous=True)

    
    SignalSource = pd.read_json("Signal.json").to_numpy()
    ClosePrice_ = pd.read_json("StockData.json")['close'].to_numpy()

    m, n = np.shape(SignalSource)[0], np.shape(SignalSource)[1]
    # row, col
    
    Signal = client.scatter(SignalSource, broadcast=True)
    Close = client.scatter(ClosePrice_, broadcast=True)
    # Dask 的前置處裡 比較大的 Data 要這樣處理
    
    print(f"================================================= process 1 =================================================")

    Tables, ColName = CalculateTable(Signal, m, n)
    
    Tables = client.scatter(Tables, broadcast=True)
    ColName = client.scatter(ColName, broadcast=True)
    
    print(f"================================================= process 2 =================================================")
    MultiTable, ColName = CalculateRanking(Top555, n, Tables, ColName, Close)
    
    print(f"================================================= process 3 =================================================")
    CombineTop = np.concatenate(MultiTable)
    ColName = np.concatenate(ColName)

    CombineTop, ColName = RankingSort(CombineTop, ColName, 5)
    CombineTop[:, 1] = MaxMinNormal(CombineTop[:, 1]) 

    CombineTop = np.concatenate((ColName[:,np.newaxis], CombineTop), axis=1)
    CombineTop = pd.DataFrame(CombineTop, columns=["Trading Strategy","ARR", "MDD", "TF"])

    CombineTop.to_json("tmp/newTop555.json", orient="columns")
    
    

    e = time.time()
    
    print(f"Time: {e-s}")