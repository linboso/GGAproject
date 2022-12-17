
from PreProCessing.DownloadData import DownloadStockData
from PreProCessing.CalculateTIvalue import TIValue
from PreProCessing.TI2Signal import TI2Signal
from PreProCessing.TI2Ranking import TI2Ranking
from RFiles import RFiles

from Algo.Population import Population


import pandas as pd

SIGNALMAPOFFSET = 20

Files = RFiles(SIGNALMAPOFFSET)
Setting = Files.Setting
SignalMap = Files.SignalMap
TI_List = Files.TI_List


StockID = Setting['StockID']
TrainingPeriod = Setting['TrainingPeriod']
ValidationPeriod = Setting['ValidationPeriod']
Path = Setting['Path'] + "/" + StockID
Strategy = Setting['Strategy']

# Dls = DownloadStockData()                                                                                   # 下載股票資料
# Dls.Download(StockID, f"{Path}/TrainingData", TrainingPeriod['StartDate'], TrainingPeriod['EndDate'])       #TrainingData
# Dls.Download(StockID, f"{Path}/ValidationData", ValidationPeriod['StartDate'], ValidationPeriod['EndDate']) #ValidationData



# TIv = TIValue(StockID, TI_List, Path)
# TIv.CalculateTIValue()
# 計算所有 指標的 Values


# TI2Signal(Setting, SIGNALMAPOFFSET, Path).ProduceSignal()
# 把value 轉換成 Signal 

## ==============================================
with open(f"{Path}/TrainingData/Signal.json") as f1, open(f"{Path}/TrainingData/StockData.json") as f2:
    Signal = pd.read_json(f1).to_numpy()
    ClosePrice = pd.read_json(f2)['close'].to_numpy()
    

import time 
# 多核版本
ResultStrategy = None
if __name__ == "__main__": 
    # 這是用來 確保 Parent and Child 的區別
    s = time.time()
    
    t2r = TI2Ranking()
    t2r.Run(Signal, ClosePrice)
    ResultStrategy = eval(f"t2r.{Strategy}('{Path}/TrainingData')")
    
    e = time.time()
    print(f"Finish time: {e-s}")
    
# 執行不同的策略為
## ==============================================

# while ResultStrategy == None:
#     pass

# ResultStrategy = pd.DataFrame(ResultStrategy)
# print(ResultStrategy)
# population = Population(Setting, ResultStrategy)
# population.GenerateOffspring_With_logFile()

# cProfile.run('population.GenerateOffspring_With_logFile()')
# population.GenerateOffspring()
# population.Genealogy()
#iterate


#chromosome 用 array 算 fintness?