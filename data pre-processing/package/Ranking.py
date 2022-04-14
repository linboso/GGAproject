import pandas as pd
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

        pass

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
            MDD:float = sys.maxsize
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
            Top555.append([ARR, MDD, TF])
            
        # print(Top555)
        Top555 = pd.DataFrame(Top555, columns=["ARR", "MDD", "TF"])
        Top555.set_index(TS_list[2:], inplace=True)
        Top555.to_json(f"../{self.savepath}/Top555.json", orient = 'index')
            
            



if __name__ == "__main__":
    ranking = Ranking()
    ranking.Top555()



