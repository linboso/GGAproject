import dask
import pandas as pd
import numpy as np

from dask.distributed import Client, LocalCluster

# cluster = LocalCluster(n_workers=16, threads_per_worker=1)  
# cluster = LocalCluster(processes=True)

# client = await Client(cluster, asynchronous=True)



# class DaskTI2Signal():
def Signal2Table(Signal, Buy, n, m):
    Table = np.zeros((m, n), dtype=np.int0)
    
    BuySignal = Signal[:, Buy]
    # ColName = []
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
        # ColName.append((Buy, Sell)) # 換成數字
        
    return Table, ColName


def Top555(Table, n, ClosePrice, ColName):
    Collect = np.empty((n, 3))
    for Col in range(n):
        BuyDay:np.array = np.where(Table[:, Col] == 1)[0]
        SellDay:np.array = np.where(Table[:, Col] == -1)[0]
        blen = len(BuyDay)
        slen = len(SellDay)

        b, s = 0, 0
        Flag:bool = False
        buyPrice:int = 0
        returnRate = []

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

        TF:int = len(returnRate)    #交易次數
        ARR:float = 0               #Average Return Rate
        MDD:float = 0               #最大回落
        if TF != 0:
            MDD = min(returnRate)
            ARR = sum(returnRate) / TF
            # ARR = ARR / TFTop555
        else:
            MDD = 0
        Collect[Col] = [ARR, MDD, TF]

    Select = []
    for i in range(3):
        count = 0
        for Top5 in Collect[:, i].argsort():
            if count == 5:
                break
            if Top5 not in Select:
                Select.append(Top5)
                count += 1
    ColName = ColName[Select]
    Top555 = Collect[Select]
    
    del Select
    del Collect
    return Top555, ColName

import time
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


    delayObject = [dask.delayed(Signal2Table)(Signal, buy, n, m) for buy in range(n)]
    delayObject = dask.compute(*delayObject)
    Tables, ColName = zip(*delayObject)

    delayObject = [dask.delayed(Top555)(table, n, Close, colname) for table, colname in zip(Tables, ColName)]
    delayObject = dask.compute(*delayObject)

    Ranking, ColName = zip(*delayObject)
    del delayObject

    CombineTop = np.concatenate(Ranking)
    ColName = np.concatenate(ColName)

    CombineTop = CombineTop[CombineTop[:,1].argsort()]

    Select = []
    for i in range(3):
        count = 0 
        for Top5 in CombineTop[:, i].argsort()[-5:]:
            if count == 5:
                break
            if Top5 not in Select:
                Select.append(Top5)
                
    ColName = ColName[Select]
    Top555 = CombineTop[Select]
    Top555[:, 1] = (Top555[:, 1] - np.min(Top555[:, 1])) / (np.max(Top555[:, 1]) - np.min(Top555[:, 1]))


    Top555 = np.concatenate((ColName[:,np.newaxis], Top555), axis=1)
    Top555 = pd.DataFrame(Top555, columns=["Trading Strategy","ARR", "MDD", "TF"])

    Top555.to_json("tmp/newTop555.json", orient="columns")
    e = time.time()
    
    print(f"Time: {e-s}")