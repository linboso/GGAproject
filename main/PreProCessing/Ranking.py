import pandas as pd
import numpy as np
import json
import sys



class Ranking():
    def __init__(self, Setting) -> None:
        setting = Setting
        self.stock_id = setting['StockID']
        self.start = setting['TrainingPeriod']['StartDate']
        self.end = setting['TrainingPeriod']['EndDate']
        self.path = setting['Path']
        
        with open(f'{self.path}/TraningData/Table.json') as f:
            self.table = pd.DataFrame(json.load(f))

        

    def Top555(self):
        Table:pd.DataFrame = self.table
        TS_list = Table.columns
        ClosePrice= Table['close'].values
        Top555 = []

        for TS in TS_list[2:]:
            Signal = Table[TS]
            BuyPrice = 0
            Flag:bool = False
            
            TF:int = 0
            ARR:float = 0
            MDD:float = sys.maxsize #設定為 系統上線最大值
            for i in range(len(Signal)):
                if Signal[i] == 0:
                    continue
                if Signal[i] == 1 and not Flag:
                    BuyPrice = ClosePrice[i]
                    Flag = True
                elif Signal[i] == -1 and Flag:
                    retunrRate = (ClosePrice[i] - BuyPrice) / BuyPrice
                    MDD = min(MDD, retunrRate)
                    ARR += retunrRate
                    TF += 1
                    Flag = False

            if TF != 0:
                ARR = ARR / TF
            else:
                MDD = 0
            Top555.append([TS, ARR, MDD, TF])
        
            
        # print(Top555)
        Top555 = pd.DataFrame(Top555, columns=["Trading Strategy","ARR", "MDD", "TF"])
        # Top555.set_index(TS_list[2:], inplace=True)
        Top555['MDD'] = self.__minmax_norm(Top555['MDD']) #執行 normalize

        Keep = []
        for i in Top555.columns[1:]:
            # print(Top555[i].sort_values(ascending=False))
            count = 0
            for top5 in Top555[i].sort_values(ascending=False).index:
                # 先由大->小排 再取 index
                if count == 5:
                    break

                if top5 not in Keep:
                    Keep.append(top5)
                    count += 1

        # print(Keep)
        Keep = [dontkeep for dontkeep in Top555.index if dontkeep not in Keep]
        # 原本 Keep 裡面是 要保留的 現在變成 沒有要保留的
        
        Top555 = Top555.drop(Keep).reset_index(drop=True)
        # 一次 drop 所有不要的部位
        
        Top555.T.to_json(f"{self.path}/TraningData/Top555.json", orient = 'index')
        # 先 轉置
        print("Finished TOP555 Ranking")
    
    def Top777(self):
        Table:pd.DataFrame = self.table
        TS_list = Table.columns
        ClosePrice= Table['close'].values
        Top777 = []

        for TS in TS_list[2:]:
            Signal = Table[TS]
            BuyPrice = 0
            Flag:bool = False
            
            TF:int = 0
            ARR:float = 0
            MDD:float = sys.maxsize #設定為 系統上線最大值
            for i in range(len(Signal)):
                if Signal[i] == 0:
                    continue
                if Signal[i] == 1 and not Flag:
                    BuyPrice = ClosePrice[i]
                    Flag = True
                elif Signal[i] == -1 and Flag:
                    retunrRate = (ClosePrice[i] - BuyPrice) / BuyPrice
                    MDD = min(MDD, retunrRate)
                    ARR += retunrRate
                    TF += 1
                    Flag = False

            if TF != 0:
                ARR = ARR / TF
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
        print("Finished Top777 Ranking")


    def __minmax_norm(self, df:pd.DataFrame): # Min-Max normalize 標準化的一種 把數字 mapping 到 0 ~ 1
        return (df - df.min()) / (df.max() - df.min())

            
            



if __name__ == "__main__":
    ranking = Ranking()
    ranking.Top555()



