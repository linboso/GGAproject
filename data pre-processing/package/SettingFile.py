import json
import os

class SettingFile():
    def __init__(self) -> None:
        pass

    def Set(self, **value):
        try:
            setting = self.ReadSetting()
            for i in value:
                setting[str(i)] = str(value[i])
        except:
            print("File not exist")
        try:
            self.__SavingFile(setting)
            print("Set successfuly")
        except:
            print("Saving setting failed")

    def Read(self, show:bool = False):
        try:
            with open("./Setting.json") as f:
                data = json.load(f)
            if show:
                print("============= Setting Data =============")
                print("Stock ID: ", data["StockID"])
                print("Start Date: ", data["StartDate"])
                print("End Date: ", data["EndDate"])
                print("Technical Indicator: ", data["TechnicalIndicator"])
                print("========================================")
                # print(data)
            return data
        except:
            init_setting = {
                "StockID":"0050.TW",
                "StartDate":"2009-08-30",
                "EndDate":"2010-12-30",
                "TechnicalIndicator":["MA5", "MA20", "RSI", "MACD", "STOCH"] } 
            #init setting format
            self.__SavingFile(init_setting)

            print("...Creating Setting.json")
            print("Reloading...")
            return self.Read() #Reload data

    def CheckPath(savepath):
        if not os.path.exists(savepath):
            try:
                #print(savepath)
                os.makedirs(savepath)
                print("Create folder successfully")
                return True
            except:
                print("Failed to create folder")
                return False
        else:
            return True

    def __SavingFile(self, data:dict, path:str="./setting.json"):
        try:
            with open(path, "w") as f:
                json.dump(data, f) # save as .json file
        except:
            print("Failed to saving file")


if __name__ == '__main__':
# test function
    baseEnv = SettingFile()
    # baseEnv.ReadSetting()
    baseEnv.Set(StockID = "0050.TW")
    baseEnv.Read(show=True)
    # os.remove('./setting.json')# delete