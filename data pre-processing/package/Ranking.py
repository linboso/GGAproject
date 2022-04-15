import pandas as pd
import numpy as np
import json
import sys

from SettingFile import SettingFile

class Ranking():
    def __init__(self) -> None:
        setting = SettingFile().Read()
        self.stock_id = setting['StockID']
        self.start = setting['StartDate']
        self.end = setting['EndDate']

        self.savepath = f"stock/{self.stock_id}/{self.start}~{self.end}"
        self.readpath = f"stock/{self.stock_id}/{self.start}~{self.end}"
        
        with open(f'../{self.readpath}/Table.json') as f:
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
                    # print(f"{TS} : ({ClosePrice[i]} - {BuyPrice}) / BuyPrice ==> {retunrRate} => MDD:{MDD}")
                    ARR += retunrRate
                    TF += 1
                    Flag = False

            if TF != 0:
                ARR = ARR / TF
            else:
                MDD = 0
            Top555.append([ARR, MDD, TF])
            
        # print(Top555)
        Top555 = pd.DataFrame(Top555, columns=["ARR", "MDD", "TF"])
        Top555.set_index(TS_list[2:], inplace=True)
        Top555['MDD'] = self.__minmax_norm(Top555['MDD']) #執行 normalize

        Keep = []
        for i in Top555.columns:
            count = 0
            for top5 in Top555[i].sort_values(ascending=False).index:
                # 先由大->小排 再取 index
                if count == 5:
                    break

                if top5 not in Keep:
                    Keep.append(top5)
                    count += 1

        for i in Top555.index:
            #全部有策略 拿出來確認
            if i not in Keep:
                # 不在Keep裡面就 Drop
                Top555.drop(i)
        
        # print(Top555)

        Top555.to_json(f"../{self.savepath}/Top555.json", orient = 'index')
    
    def __minmax_norm(self, df:pd.DataFrame): # Min-Max normalize 標準化的一種 把數字 mapping 到 0 ~ 1
        return (df - df.min()) / (df.max() - df.min())

            
            



if __name__ == "__main__":
    ranking = Ranking()
    ranking.Top555()



