
import pandas as pd
import json




class Ranking():
    def __init__(self, Setting) -> None:
        setting = Setting
        self.stock_id = setting['StockID']
        self.start = setting['TrainingPeriod']['StartDate']
        self.end = setting['TrainingPeriod']['EndDate']
        self.path = f"{setting['Path']}/{setting['StockID']}"
        
        if __name__ == "__main__":
            with open(f'../../data/stock/{self.stock_id}/TraningData/Table.json') as f:
                self.table = pd.DataFrame(json.load(f))
        else:
            with open(f'{self.path}/TraningData/Table.json') as f:
                self.table = pd.DataFrame(json.load(f))
        


    def Top15(self):
        Table:pd.DataFrame = self.table
        TS_list = Table.columns
        ClosePrice= Table['close'].to_list()
        Top15 = []

        for TS in TS_list[2:]:
            Signal:list = Table[TS].to_list()
            BuyPrice:int = 0
            Flag:bool = False
            
            Temp:list = []
            for i in range(len(Signal)):
                if Signal[i] == 0:
                    continue
                if Signal[i] == 1 and not Flag:
                    BuyPrice = ClosePrice[i]
                    Flag = True
                elif Signal[i] == -1 and Flag:
                    retunrRate = (ClosePrice[i] - BuyPrice) / BuyPrice
                    Temp.append(retunrRate)
                    Flag = False

            ARR:float = 0      #Average Return Rate
            if (TF:=len(Temp)) != 0:
                ARR = sum(Temp) / TF

            Top15.append([TS, ARR])
        
        Top15 = pd.DataFrame(Top15, columns=["Trading Strategy","ARR"])

        DontKeep = Top15['ARR'].sort_values(ascending=False).index[15:]
        #捨棄後 85 個
        Top15 = Top15.drop(DontKeep).sort_values(by=["ARR"], ascending =False).reset_index(drop=True)
        #保留 ARR最高的 前 15 個

        if __name__ == "__main__":
            Top15.T.to_json(f"../../data/stock/{self.stock_id}/TraningData/Top15.json", orient = 'index')
        else:
            Top15.T.to_json(f"{self.path}/TraningData/Top15.json", orient = 'index')

        # 先 轉置 在輸出 json 
        print("已完成 TOP15 的篩選")

    def Top21(self):
        Table:pd.DataFrame = self.table
        TS_list = Table.columns
        ClosePrice= Table['close'].to_list()
        Top15 = []

        for TS in TS_list[2:]:
            Signal:list = Table[TS].to_list()
            BuyPrice:int = 0
            Flag:bool = False
            
            Temp:list = []
            for i in range(len(Signal)):
                if Signal[i] == 0:
                    continue
                if Signal[i] == 1 and not Flag:
                    BuyPrice = ClosePrice[i]
                    Flag = True
                elif Signal[i] == -1 and Flag:
                    retunrRate = (ClosePrice[i] - BuyPrice) / BuyPrice
                    Temp.append(retunrRate)
                    Flag = False

            ARR:float = 0      #Average Return Rate
            if (TF:=len(Temp)) != 0:
                ARR = sum(Temp) / TF

            Top15.append([TS, ARR])
        
        Top15 = pd.DataFrame(Top15, columns=["Trading Strategy","ARR"])

        DontKeep = Top15['ARR'].sort_values(ascending=False).index[21:]
        #捨棄後 85 個
        Top15 = Top15.drop(DontKeep).sort_values(by=["ARR"], ascending =False).reset_index(drop=True)
        #保留 ARR最高的 前 21 個

        if __name__ == "__main__":
            Top15.T.to_json(f"../../data/stock/{self.stock_id}/TraningData/Top21.json", orient = 'index')
        else:
            Top15.T.to_json(f"{self.path}/TraningData/Top21.json", orient = 'index')

        # 先 轉置 在輸出 json 
        print("已完成 TOP21 的篩選")
    #==================================== Top15 ===========================================

    def Top555(self):
        Table:pd.DataFrame = self.table
        TS_list = Table.columns
        ClosePrice= Table['close'].to_list()
        Top555 = []

        tmp = []
        for TS in TS_list[2:]:
            Signal:list = Table[TS].to_list()
            BuyPrice:int = 0
            Flag:bool = False
            
            Temp = []
            for i in range(len(Signal)):
                if Signal[i] == 0:
                    continue
                if Signal[i] == 1 and not Flag:
                    BuyPrice = ClosePrice[i]
                    Flag = True
                elif Signal[i] == -1 and Flag:
                    retunrRate = (ClosePrice[i] - BuyPrice) / BuyPrice
                    Temp.append(retunrRate)
                    # MDD = min(MDD, retunrRate)
                    # ARR += retunrRate
                    # TF += 1
                    Flag = False

            TF:int = 0  #交易次數
            ARR:float = 0     #Average Return Rate
            MDD:float = 0     #最大回落
            if (TF := len(Temp)) != 0:
                MDD = min(Temp)
                ARR = sum(Temp) / TF
                # ARR = ARR / TF
            else:
                MDD = 0
            Top555.append([TS, ARR, MDD, TF])
        
        Top555 = pd.DataFrame(Top555, columns=["Trading Strategy","ARR", "MDD", "TF"])
        Top555['MDD'] = self.__minmax_norm(Top555['MDD']) #執行 normalize

        Keep = []
        for i in Top555.columns[1:]:
            count = 0
            for top5 in Top555[i].sort_values(ascending=False).index:
                # 先由大->小排 再取 index
                if count == 5:
                    break

                if top5 not in Keep:
                    Keep.append(top5)
                    count += 1

        # print(F">> {Keep}")
        DontKeep = [dontkeep for dontkeep in Top555.index if dontkeep not in Keep]
        #沒有要保留的
        
        Top555 = Top555.drop(DontKeep).reset_index(drop=True)
        # 一次 drop 所有不要的部位
        
        if __name__ == "__main__":
            Top555.T.to_json(f"../../data/stock/{self.stock_id}/TraningData/Top555.json", orient = 'index')
        else:
            Top555.T.to_json(f"{self.path}/TraningData/Top555.json", orient = 'index')

        # 先 轉置 在輸出 json 
        print("已完成 TOP555 的篩選")

    #==================================== Top555 ===========================================
    
    def Top777(self):
        Table:pd.DataFrame = self.table
        TS_list = Table.columns
        ClosePrice= Table['close'].to_list()
        Top777 = []

        for TS in TS_list[2:]:
            Signal:list = Table[TS].to_list()
            BuyPrice:int = 0
            Flag:bool = False
            

            Temp = []
            for i in range(len(Signal)):
                if Signal[i] == 0:
                    continue
                if Signal[i] == 1 and not Flag:
                    BuyPrice = ClosePrice[i]
                    Flag = True
                elif Signal[i] == -1 and Flag:
                    retunrRate = (ClosePrice[i] - BuyPrice) / BuyPrice
                    Temp.append(retunrRate)
                    # MDD = min(MDD, retunrRate)
                    # ARR += retunrRate
                    # TF += 1
                    Flag = False

            TF:int = 0  #交易次數
            ARR:float = 0     #Average Return Rate
            MDD:float = 0     #最大回落
            if (TF := len(Temp)) != 0:
                MDD = min(Temp)
                ARR = sum(Temp) / TF
                # ARR = ARR / TF
            else:
                MDD = 0
            Top777.append([TS, ARR, MDD, TF])
        

        Top777 = pd.DataFrame(Top777, columns=["Trading Strategy","ARR", "MDD", "TF"])
        Top777['MDD'] = self.__minmax_norm(Top777['MDD']) #執行 normalize

        Keep = []
        for i in Top777.columns[1:]:
            count = 0
            for top5 in Top777[i].sort_values(ascending=False).index:
                if count == 7:
                    break
                if top5 not in Keep:
                    Keep.append(top5)
                    count += 1

        Keep = [dontkeep for dontkeep in Top777.index if dontkeep not in Keep]
        
        Top777 = Top777.drop(Keep).reset_index(drop=True)
        Top777.T.to_json(f"{self.path}/TraningData/Top777.json", orient = 'index')
        print("已完成 Top777 的篩選")
    #==================================== Top777 ===========================================


    def __minmax_norm(self, df:pd.DataFrame): # Min-Max normalize 標準化的一種 把數字 mapping 到 0 ~ 1
        return (df - df.min()) / (df.max() - df.min())

            
            



if __name__ == "__main__":
    with open('../setting.json') as f:
        ranking = Ranking(json.load(f))

    # ranking.Top555()
    ranking.Top21()
    # ranking.Top15()



