import json
import os


def ReadSetting():
    try:
        with open("./setting.json") as f:
            setting = json.load(f)
            print("============= Setting Data =============")
            print("Stock ID: ", setting["StockID"])
            print("Start Date: ", setting["StartDate"])
            print("End Date: ", setting["EndDate"])
            print("Techical Indicator: ", setting["TechicalIndicator"])
            print("========================================")
        return setting
    except:
        init_setting = {
            "StockID":"0050.TW",
            "StartDate":"2009-08-30",
            "EndDate":"2010-12-30",
            "TechicalIndicator":["MA5", "MA20", "RSI", "MACD", "STOCH"] } #init setting format
        with open("./setting.json", "w") as f:
            json.dump(init_setting, f) # save as .json file
        print("...Creating setting.json")
        print("Reloading...")
        return ReadSetting() #Reload data


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





