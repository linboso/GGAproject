
import json
import os

class RFiles():
    def __init__(self, SIGNALMAPOFFSET):
        try:
            with open("./Setting.json") as f1, open("./TI_List.json") as f2, open("./SignalMap.json") as f3:
                Setting = json.load(f1)
                TI_List = json.load(f2)
                SignalMap = json.load(f3)
                    
            self.Setting = Setting
            self.TI_List = TI_List
            self.SignalMap = SignalMap
            self.SIGNALMAPOFFSET = SIGNALMAPOFFSET
            
            if not os.path.exists(Setting['Path']):
                os.makedirs(Setting['path'])
        except:
            init_Setting = {
                "StockID":"0050.TW",
                "TrainingPeriod": {
                        "StartDate":"2009-08-30",
                        "EndDate":"2010-12-30"
                    },
                "ValidationPeriod": {
                        "StartDate":"2010-08-30",
                        "EndDate":"2012-12-30"
                    },
                "Path":"../data/stock/",
                # "TechnicalIndicator":["MA5", "MA20", "RSI", "MACD", "STOCH", "CCI", "MAMA"],
                "Strategy": "Top555",
                "SLTP": [10, 10],
                "pSize": 100,
                "CrossoverRate": 0.8,
                "MutationRate": 0.03,
                "InversionRate": 0.3,
                "Generation": 30,
                "kGroup": 5,
                "mTS": 15,
                "WeightPart":100,
                "Capital": 100000          
            }
            #init setting format
            
            self.__SavingFile(init_Setting)
            self.Setting_File = init_Setting
            print("...Creating Setting.json")
        
    

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

    def PrintALL(self):
        data = self.Setting
        print("======================================== Setting Content ========================================")
        print(f"\tStock ID: {data['StockID']}")
        print(f"\t>   Traning  Period\tStratDate: {data['TrainingPeriod']['StartDate']} ~ {data['TrainingPeriod']['EndDate']}")
        print(f"\t> Validation Period\tStratDate: {data['ValidationPeriod']['StartDate']} ~ {data['ValidationPeriod']['EndDate']}")
        print(f"\tPath: {data['Path']}")
        # print(f"Technical Indicator: {data['TechnicalIndicator']}")
        print(f"\tStrategy: {data['Strategy']}")
        print(f"\tSLTP: {data['SLTP']}")
        print(f"\tCrossoverRate: {data['CrossoverRate']}")
        print(f"\tMutationRate: {data['MutationRate']}")
        print(f"\tInversionRate: {data['InversionRate']}")
        print(f"\tGeneration: {data['Generation']}")
        print(f"\tkGroup: {data['kGroup']}")
        print(f"\tmTS: {data['mTS']}")
        print(f"\tWeightPart: {data['WeightPart']}")
        print(f"\tCapital: {data['Capital']}")
        print("\r\n========================================     TI_List     ========================================")
        data = self.TI_List
        print(f"---------------  Total Non-MA-Tpye TI Numbers: {len(data['NON_MA_TYPE'])}  ---------------")
        print(f"{data['NON_MA_TYPE']}\r\n")
        print(f"---------------  Total MA-Tpye TI Numbers: {len(data['MA_TYPE'])}  ---------------")
        print(f"{data['MA_TYPE']}")
        print("========================================    SignalMap    ========================================")
        data = self.SignalMap
        print(f"\tNON_MA_TYPE Numbers: {len(data[:self.SIGNALMAPOFFSET])}")
        print(f"\tMA_TYPE Numbers {len(data[self.SIGNALMAPOFFSET:])}")
        print("=================================================================================================")

    def __SavingFile(self, data:dict): 
        try:
            with open("./Setting.json", "w") as f:
                json.dump(data, f) # save as .json file
        except:
            print("Failed to saving file")



if __name__ == '__main__':
    baseEnv = RFiles()
    print(baseEnv.SignalMap)
    
