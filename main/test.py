import json
import os

class BackTesting():
    def __init__(self) -> None:
        try:
            with open("./record.json") as f:
                data = json.load(f)
                #print(data)
            self.StockID = data['StockID']  
            self.TrainingPeriod = data['TrainingPeriod']
            self.ValidationPeriod = data['ValidationPeriod']
            self.SL = data['SLTP'][0]
            self.TP = data['SLTP'][1]
            self.Capital = data['Capital']
            self.GTSP = data['GTSP']
            self.Weight = data['Weight']
            self.TradingStrategy = data['TradingStrategy']
            self.SignalMap = data['SignalMap']
        except:
            print("讀取 record.json 失敗")
            print("請確認該檔案是否存在")
        print()


if __name__ == '__main__':
    obj = BackTesting()
    print(obj)