import pandas as pd
import os
import yfinance as yf


class DownloadStockData():
    def __init__(self) -> None:
        pass

    def Download(self, StID, Path, StartDate, EndDate):
  
        data:pd.DataFrame = yf.download(StID, StartDate, EndDate)           # 從 Yahoo 下載 Stock-data 
        data.drop(['Adj Close'], axis=1, inplace=True)                      # drop 掉 "Adj Close" 這一 col 用不到
        data.columns = ["open","high","low","close","volume"]               # 改小寫

        data.to_json(f"{Path}/StockData.json", orient='columns')

        data = pd.DataFrame(data.index)
        data.to_json(f"{Path}/Date.json", orient='columns')
        
        
    def CheckPath(self, Path):
        if not os.path.exists(Path):
            os.makedirs(Path)
            print("已建立資料夾")
            

