
import json
import os

class SettingFile():
    def __init__(self) -> None:
        try:
            with open("./Setting.json") as f:
                    data = json.load(f)
            self.data = data

            if not os.path.exists(data['Path']):
                os.makedirs(data['path'])
        except:
            init_setting = {
                "StockID":"0050.TW",
                "TrainingPeriod": {
                        "StartDate":"2009-08-30",
                        "EndDate":"2010-12-30"
                    },
                "ValidationPeriod": {
                        "StartDate":"2010-08-30",
                        "EndDate":"2012-12-30"
                    },
                "Path":"../data/stock/0050.TW/",
                "TechnicalIndicator":["MA5", "MA20", "RSI", "MACD", "STOCH", "CCI"],
                "Strategy": "Top777",
                "pSize": 100,
                "CrossoverRate": 0.8,
                "MutationRate": 0.03,
                "InverstionRate": 0.3,
                "Generation": 10,
                "kroup": 5,
                "mTS": 21,
                "WeightPart":100,
                "Capital": 100000          
            }
            #init setting format
            self.__SavingFile(init_setting)
            self.data = init_setting
            print("...Creating Setting.json")
        
    

    def Set(self, **value):
 
        setting = self.data
        try:
            for i in value:
                setting[str(i)] = value[i]

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
        print(f"Stock ID: {data['StockID']}")
        print(f">   Traning  Period\tStratDate: {data['TrainingPeriod']['StartDate']} ~ {data['TrainingPeriod']['EndDate']}")
        print(f"> Validation Period\tStratDate: {data['ValidationPeriod']['StartDate']} ~ {data['ValidationPeriod']['EndDate']}")
        print(f"Path: {data['Path']}")
        print(f"Technical Indicator: {data['TechnicalIndicator']}")
        print(f"Strategy: {data['Strategy']}")
        print(f"CrossoverRate:  {data['CrossoverRate']}")
        print(f" MutationRate:  {data['MutationRate']}")
        print(f"InversionRate: {data['InversionRate']}")
        print(f"Generation: {data['Generation']}")
        print(f"kGroup: {data['kGroup']}")
        print(f"mTS: {data['mTS']}")
        print(f"WeightPart: {data['WeightPart']}")
        print(f"Capital: {data['Capital']}")
        print("========================================")


    # __ 是 prvate 的用法 無法從外部使用
    def __SavingFile(self, data:dict, path:str="./setting.json"): 
        try:
            with open(path, "w") as f:
                json.dump(data, f) # save as .json file
        except:
            print("Failed to saving file")


if __name__ == '__main__':
    baseEnv = SettingFile()
    print(baseEnv.data['TrainingPeriod'])
    baseEnv.print() 
    # baseEnv.Set(TechnicalIndicator = ['CCI'])

    # NewDate = {
    #         "StartDate":"2010-08-30",
    #         "EndDate":"2012-12-30"
    #     }

    # baseEnv.Set(ValidationPeriod = NewDate)
    # baseEnv.Set(TrainingPeriod = {
    #     "StartDate": "2009-10-01",
	# 	"EndDate": "2010-12-30"
    #     })

    #  Way to set new date / Values
   

