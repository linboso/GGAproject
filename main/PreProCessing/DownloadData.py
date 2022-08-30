import pandas as pd
import os
import yfinance as yf


class DownloadStockData():
    def __init__(self, Setting) -> None:
        setting = Setting

        self.stock_id = setting['StockID']
        self.Tstart = setting['TrainingPeriod']['StartDate']
        self.Tend = setting['TrainingPeriod']['EndDate']
        
        self.Vstart = setting['ValidationPeriod']['StartDate']
        self.Vend = setting['ValidationPeriod']['EndDate']
        
        self.path = f"{setting['Path']}/{setting['StockID']}"
        print(f"Store at {self.path}")


    def DownloadStockData(self):
        try:       
            data:pd.DataFrame = yf.download(self.stock_id, start = self.Tstart, end = self.Tend)
            data.drop(['Adj Close'], axis=1, inplace=True)
            data.columns = ["open","high","low","close","volume"]
            # download Stock-data from yahoo
            # and drop 1 column, "Adj Close" which is not need to be used
        except:
            print("Fail to download Traning Data ")

        try:
            if not os.path.exists(f"{self.path}/TrainingData/"):
                os.makedirs(f"{self.path}/TrainingData/")
                print("Create TrainingData folder")
            
            # data.to_json(f"{self.path}/TrainingData/StockData.json", orient='columns')
            data.to_json(f"{self.path}/TrainingData/StockData.json", orient='records')

            data = pd.DataFrame(data.index)

            # data.to_json(f"{self.path}/TrainingData/Date.json", orient='columns')
            data.to_json(f"{self.path}/TrainingData/Date.json", orient='records')

            print(f"Saving TrainingData data at {self.path} \r\n")
        except:
            print("Fail to saving file \r\n")
        #
        # ValidationData
        #
        try:       
            data:pd.DataFrame = yf.download(self.stock_id, start = self.Vstart, end = self.Vend)
            data.drop(['Adj Close'], axis=1, inplace=True)
            data.columns = ["open","high","low","close","volume"]
        except:
            print("Fail to download Traning Data ")

        try:
            if not os.path.exists(f"{self.path}/ValidationData/"):
                os.makedirs(f"{self.path}/ValidationData/")
                print("Create ValidationData folder")
            
            # data.to_json(f"{self.path}/ValidationData/StockData.json", orient='columns')
            data.to_json(f"{self.path}/ValidationData/StockData.json", orient='records')

            data = pd.DataFrame(data.index)
            # data.to_json(f"{self.path}/ValidationData/Date.json", orient='columns')
            data.to_json(f"{self.path}/ValidationData/Date.json", orient='records')


            print(f"Saving ValidationData data at {self.path}/ValidationData \r\n")
        except:
            print("Fail to saving file \r\n")
        


