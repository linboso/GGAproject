import json
import os

class SettingFile():
    def __init__(self) -> None:
        try:
            with open("./Setting.json") as f:
                    data = json.load(f)
            self.data = data
        except:
            init_setting = {
                "StockID":"0050.TW",
                "StartDate":"2009-08-30",
                "EndDate":"2010-12-30",
                "TechnicalIndicator":["MA5", "MA20", "RSI", "MACD", "STOCH"] } 
            #init setting format
            self.__SavingFile(init_setting)
            self.data = init_setting
            print("...Creating Setting.json")
        
    

    def Set(self, **value):
        try:
            setting = self.data
            for i in value:
                setting[str(i)] = str(value[i])
        except:
            print("File not exist")
        try:
            self.__SavingFile(setting)
            print("Change setting  successfully")
        except:
            print("Change setting failed")

    def Read(self):
        return self.data
        

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

    def print(self):
        data = self.data
        print("============= Setting Data =============")
        print("Stock ID: ", data["StockID"])
        print("Start Date: ", data["StartDate"])
        print("End Date: ", data["EndDate"])
        print("Technical Indicator: ", data["TechnicalIndicator"])
        print("========================================")


    # __ 是 prvate 的用法 無法從外部使用
    def __SavingFile(self, data:dict, path:str="./setting.json"): 
        try:
            with open(path, "w") as f:
                json.dump(data, f) # save as .json file
        except:
            print("Failed to saving file")


if __name__ == '__main__':
# test function
    baseEnv = SettingFile().Read()
    # baseEnv.ReadSetting()
    # baseEnv.Set(StockID = "0050.TW")
    print(baseEnv)
