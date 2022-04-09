import pandas as pd
import os
import yfinance as yf
from .SettingFile import SettingFile


class DownloadStockData():
    def __init__(self) -> None:
        setting = SettingFile()
        setting = setting.Read(show=True)

        self.stock_id = setting['StockID']
        self.start = setting['StartDate']
        self.end = setting['EndDate']
        self.savepath = f"stock/{self.stock_id}/{self.start}~{self.end}"
        print(self.savepath)


    def StockDataDownload(self):
        try:       
            data = yf.download(self.stock_id, start = self.start, end = self.end)
            data.drop(['Adj Close'], axis=1, inplace=True)
            data.columns = ["open","high","low","close","volume"]
            # download Stock-data from yahoo
            # and drop 1 column, "Adj Close" which are no needs to use 
        except:
            print("yfinance error")
        try:
            if not os.path.exists(self.savepath):
                os.makedirs(self.savepath)
                print("Create folder path")

            data.to_json(f"{self.savepath}/StockData.json", orient='records')
            # data = pd.concat([pd.DataFrame(data.index).reset_index(drop=True), data.reset_index(drop=True)], axis=1)
            data = pd.DataFrame(data.index)
            data.to_json(f"{self.savepath}/History.json", orient='records')
            # Save another data but with "Date"

            # Save the data as .json Type
            # data name save as {Stock_Id}+{Star_day}+{End_day}.json
            print(f"Saving {self.stock_id} stock data file at {self.savepath} \r\n")
        except:
            print("Dowload Stock Data Failed \r\n")
        


if __name__ == "__main__":
    ds = DownloadStockData()
    ds.StockDataDownload()
    print(ds)