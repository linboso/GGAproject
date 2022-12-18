import pandas as pd
import numpy as np
import json



class Ranking():
    def __init__(self, Setting) -> None:
        setting = Setting
        self.stock_id = setting['StockID']
        self.start = setting['TrainingPeriod']['StartDate']
        self.end = setting['TrainingPeriod']['EndDate']
        
        if __name__ == "__main__":
            self.path = f"../{setting['Path']}/{setting['StockID']}/TrainingData"
        else:
            self.path = f"{setting['Path']}/{setting['StockID']}/TrainingData"

        with open(f'{self.path}/Table.json') as f:
            self.table = pd.DataFrame(json.load(f))
        


    def Top15(self):
        TSList = self.table.columns
        Table:np.array = self.table.to_numpy()
        ClosePrice:np.array = Table[:, 0] #Close Price 

        Top15 = []
        n = Table.shape[1]
        for Col in range(2, n):
            BuyDay:np.array = np.where(Table[:, Col] == 1)[0]
            SellDay:np.array = np.where(Table[:, Col] == -1)[0]

            blen = len(BuyDay)  # 2者長度不一定相同
            slen = len(SellDay)

            b, s = 0, 0
            Flag:bool = False # Flag == True => 有買了
            buyPrice:int = 0 
            returnRate = []
            # 上4列 為前置作業
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
            # 這邊跟 TI2Signal 的策略不一樣
            # 故寫法會不一樣 原本的寫法在最下面

            ARR:float = 0      #Average Return Rate

            if (TF:=len(returnRate)) != 0:
                ARR = sum(returnRate) / TF
            Top15.append([TSList[Col], ARR])
        
        Top15 = pd.DataFrame(Top15, columns=["Trading Strategy","ARR"])

        DontKeep = Top15['ARR'].sort_values(ascending=False).index[15:]

        #捨棄後 85 個
        Top15 = Top15.drop(DontKeep).sort_values(by=["ARR"], ascending =False).reset_index(drop=True)
        #保留 ARR最高的 前 15 個
        Top15.T.to_json(f"{self.path}/Top15.json", orient = 'index')

        # 先 轉置 在輸出 json 
        print("完成 TOP15 的篩選")

    #==================================== Top15 ===========================================

    def Top21(self):
        TSList = self.table.columns
        Table:np.array = self.table.to_numpy()
        ClosePrice:np.array = Table[:, 0] #Close Price 

        Top21 = []
        n = Table.shape[1]
        for Col in range(2, n):
            
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

            ARR:float = 0      #Average Return Rate

            if (TF:=len(returnRate)) != 0:
                ARR = sum(returnRate) / TF

            Top21.append([TSList[Col], ARR])
        
        Top21 = pd.DataFrame(Top21, columns=["Trading Strategy","ARR"])

        DontKeep = Top21['ARR'].sort_values(ascending=False).index[21:]
        #捨棄後 85 個
        Top21 = Top21.drop(DontKeep).sort_values(by=["ARR"], ascending =False).reset_index(drop=True)
        #保留 ARR最高的 前 15 個

        Top21.T.to_json(f"{self.path}/Top21.json", orient = 'index')

        # 先 轉置 在輸出 json 
        print("完成 TOP21 的篩選")
    #==================================== Top21 ===========================================

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

    #==================================== Top555 ===========================================
    
    def Top777(self):
        TSList = self.table.columns
        Table:np.array = self.table.to_numpy()
        ClosePrice:np.array = Table[:, 0] #Close Price 

        Top777 = []
        n = Table.shape[1]
        for Col in range(2, n):
            
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
                # ARR = ARR / TF
            else:
                MDD = 0
            Top777.append([TSList[Col], ARR, MDD, TF])
        
        Top777 = pd.DataFrame(Top777, columns=["Trading Strategy","ARR", "MDD", "TF"])
        Top777['MDD'] = self.__minmax_norm(Top777['MDD']) #執行 normalize

        Keep = []
        for i in Top777.columns[1:]:
            count = 0
            for top7 in Top777[i].sort_values(ascending=False).index:
                if count == 7:
                    break
                if top7 not in Keep:
                    Keep.append(top7)
                    count += 1

        Keep = [dontkeep for dontkeep in Top777.index if dontkeep not in Keep]
        
        Top777 = Top777.drop(Keep).reset_index(drop=True)
        Top777.T.to_json(f"{self.path}/Top777.json", orient = 'index')
        print("完成 Top777 的篩選")
    #==================================== Top777 ===========================================

    #原版 比較慢  大約慢 現有版本的 2 倍
    #但是可以用來Check
    def Top21_for_debug(self):
        TSList = self.table.columns
        Table:np.array = self.table.to_numpy()
        ClosePrice= Table[:, 0]
        Top15 = []
        n = Table.shape[1]

        for Col in range(2, n):
            Signal:np.array = Table[:, Col]
            BuyPrice:int = 0
            Flag:bool = False
            
            Temp:list = []
            for i in range(len(Signal)):
                if Signal[i] == 0:
                    continue
                if Signal[i] == 1 and not Flag:
                    BuyPrice = ClosePrice[i]
                    # print(f"T->I: {i} {BuyPrice}")
                    Flag = True
                elif Signal[i] == -1 and Flag:
                    retunrRate = (ClosePrice[i] - BuyPrice) / BuyPrice
                    # print(f"F->I: {i} {ClosePrice[i]}")
                    Temp.append(retunrRate)
                    Flag = False

            ARR:float = 0      #Average Return Rate
            if (TF:=len(Temp)) != 0:
                ARR = sum(Temp) / TF

            Top15.append([TSList[Col], ARR])
        
        Top15 = pd.DataFrame(Top15, columns=["Trading Strategy","ARR"])

        DontKeep = Top15['ARR'].sort_values(ascending=False).index[21:]
        #捨棄後 85 個
        Top15 = Top15.drop(DontKeep).sort_values(by=["ARR"], ascending =False).reset_index(drop=True)
        #保留 ARR最高的 前 21 個

        Top15.T.to_json(f"{self.path}/Top21_Debug.json", orient = 'index')

        # 先 轉置 在輸出 json 
        print("完成 TOP21 for Debug 的篩選")


    def __minmax_norm(self, df:pd.DataFrame): # Min-Max normalize 標準化的一種 把數字 mapping 到 0 ~ 1
        return (df - df.min()) / (df.max() - df.min())

            
            



if __name__ == "__main__":
    import cProfile
    # 獨立執行 測試用
    # with open('../setting.json') as f:
    #     ranking = Ranking(json.load(f))
    
    # ranking.Top777()
    # ranking.Top555()
    # ranking.Top21() 
    # ranking.Top21_for_debug()
    # ranking.Top15() 
    # cProfile.run("ranking.Top555()")
    # cProfile.run("ranking.Top21()")
    # cProfile.run("ranking.Top15()")



