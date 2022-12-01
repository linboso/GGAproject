import dask
import pandas as pd
import numpy as np

from dask.distributed import Client, LocalCluster

# cluster = LocalCluster(n_workers=16, threads_per_worker=1)  
# cluster = LocalCluster(processes=True)
# client = await Client(cluster, asynchronous=True)


def Signal2LargeTable(Signal, Buy, n, m):
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


def Ranking(BuyDay, SellDay, ClosePrice) -> list:
    b, s= 0, 0
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
            # 這是 returnRate
            Flag = False

        if BuyDay[b] > SellDay[s]:
            s += 1
        else:
            b += 1
    return  returnRate

def Collects(n, Table, ClosePrice) -> np.array:
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

def RankingSort(Collect, ColName, SelectRange, HowMuch):
    #           [ARR, MDD, TF] 
    # SelectRange  1   2   3     最多就是 3
    # SelectRange = 3, HowMuch = 5  ==> Top555
    # SelectRange = 1, HowMuch = 15  ==> Top15 (前 15個 ARR)
    
    Select = []
    for i in range(SelectRange):
        count = 0
        for Top in np.argsort(-Collect[:, i]):
            if count == HowMuch:
                break
            if Top not in Select:
                Select.append(Top)
                count += 1
                
    return Collect[Select], ColName[Select]
    # ColName = ColName[Select]
    # Top555 = Collect[Select]

def Top555(Table, n, ClosePrice, ColName):
    Collect = Collects(n, Table, ClosePrice)
    return RankingSort(Collect, ColName, 3, 5) 

import time
# 如果想分析 用jupyterlab 比較快理解
if __name__ == "__main__":
    s = time.time()
    cluster = LocalCluster(n_workers=16, threads_per_worker=1)  
    client = Client(cluster, asynchronous=True)
    
    NorSignal = pd.read_json("Signal.json")
    ClosePrice_ = pd.read_json("StockData.json")['close'].to_numpy()
    SignalName = NorSignal.columns[1:]
    Date = NorSignal['Date']
    NorSignal = NorSignal.drop(['Date'], axis=1)

    m = len(NorSignal)  # 天數
    n = len(SignalName) # 種類

    NorSignal = NorSignal.to_numpy()
    
    Signal = client.scatter(NorSignal, broadcast=True)
    Close = client.scatter(ClosePrice_, broadcast=True)
    # Dask 的前置處裡 比較大的 Data 要這樣處理
    print(f"================================================= process 1 =================================================")
    delayObject = [dask.delayed(Signal2LargeTable)(Signal, buy, n, m) for buy in range(n)]
    delayObject = dask.compute(*delayObject)
    Tables, ColName = zip(*delayObject)

    Tables = client.scatter(Tables, broadcast=True)
    ColName = client.scatter(ColName, broadcast=True)
    
    print(f"================================================= process 2 =================================================")
    delayObject = [dask.delayed(Top555)(table, n, Close, colname) for table, colname in zip(Tables, ColName)]
    delayObject = dask.compute(*delayObject)

    Ranking, ColName = zip(*delayObject)

    del delayObject
    print(f"================================================= process 3 =================================================")
    CombineTop = np.concatenate(Ranking)
    ColName = np.concatenate(ColName)
    # print(np.shape(CombineTop))
    
    # CombineTop = CombineTop[np.argsort(CombineTop[:,1])]
    CombineTop = CombineTop[np.argsort(CombineTop[:,1])]

    Select = []
    for i in range(3):
        count = 0 

        for Top5 in np.argsort( -CombineTop[:, i]):
            if count == 5:
                break
            if Top5 not in Select:
                Select.append(Top5)
                count += 1
                
    ColName = ColName[Select]
    Top555 = CombineTop[Select]
    Top555[:, 1] = (Top555[:, 1] - np.min(Top555[:, 1])) / (np.max(Top555[:, 1]) - np.min(Top555[:, 1]))

    Top555 = np.concatenate((ColName[:,np.newaxis], Top555), axis=1)
    Top555 = pd.DataFrame(Top555, columns=["Trading Strategy","ARR", "MDD", "TF"])

    Top555.to_json("tmp/newTop555.json", orient="columns")
    e = time.time()
    
    print(f"Time: {e-s}")