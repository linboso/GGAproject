import pandas as pd
import yfinance as yf
from .BasicFunction import CheckPath, ReadSetting


class DownloadStockData():
    def __init__(self) -> None:
        setting = ReadSetting()
        self.stock_id = setting['StockID']
        self.start = setting['StartDate']
        self.end = setting['EndDate']
        self.savepath = f"stock/{self.stock_id}/{self.start}~{self.end}"


    def StockDataDownload(self):
        if CheckPath(self.savepath):        
            data = yf.download(self.stock_id, start = self.start, end = self.end)
            print(f"Finish downloaded")
            data.drop(['Adj Close'], axis=1, inplace=True)
            data.columns = ["open","high","low","close","volume"]
            # download Stock-data from yahoo
            # and drop 1 column, "Adj Close" which are no needs to use 
            data.to_json(f"{self.savepath}/stockdata.json", orient='records')
            print(f"Saving {self.stock_id} stock data file at {self.savepath} \r\n")
            # Save the data as .json Type
            # data name save as {Stock_Id}+{Star_day}+{End_day}.json
            data = pd.concat([pd.DataFrame(data.index).reset_index(drop=True), data.reset_index(drop=True)], axis=1)
            data.to_json(f"{self.savepath}/origin_stockdata.json", orient='records')
            # Save another data but with "Date"
        else:
            print("No folder to storge data\r\n")
