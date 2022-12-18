
from PreProCessing.DownloadData import DownloadStockData
from PreProCessing.CalculateTIvalue import TIValue
from PreProCessing.TI2Signal import TI2Signal
from PreProCessing.TI2Ranking import TI2Ranking
from RFiles import RFiles

from Algo.Population import Population

import time
import pandas as pd

# 多核版本

if __name__ == "__main__": 
    SIGNALMAPOFFSET = 20

    Files = RFiles(SIGNALMAPOFFSET)
    Files.PrintALL()
    Setting = Files.Setting
    SignalMap = Files.SignalMap
    TI_List = Files.TI_List

    SLTP = Setting['SLTP']
    StockID = Setting['StockID']
    TrainingPeriod = Setting['TrainingPeriod']
    ValidationPeriod = Setting['ValidationPeriod']
    Path = Setting['Path'] + "/" + StockID
    Strategy = Setting['Strategy']

    Dls = DownloadStockData()                                                                                   # 下載股票資料
    Dls.Download(StockID, f"{Path}/TrainingData", TrainingPeriod['StartDate'], TrainingPeriod['EndDate'])       #TrainingData
    Dls.Download(StockID, f"{Path}/ValidationData", ValidationPeriod['StartDate'], ValidationPeriod['EndDate']) #ValidationData

    # TIv = TIValue(StockID, TI_List, Path)
    # TIv.CalculateTIValue()
    # 計算所有 指標的 Values

    # TI2Signal(SIGNALMAPOFFSET, Path).ProduceSignal()
    # 把value 轉換成 Signal 

    with open(f"{Path}/TrainingData/Signal.json") as f1, open(f"{Path}/TrainingData/StockData.json") as f2:
        Signal = pd.read_json(f1).to_numpy()
        ClosePrice = pd.read_json(f2)['close'].to_numpy()
        
    # time.sleep(1)

    # 這是用來 確保 Parent and Child 的區別
    s = time.time()
    
    t2r = TI2Ranking()
    t2r.Run(Signal, ClosePrice, ThreadNumbers=16)
    ResultStrategy = eval(f"t2r.{Strategy}('{Path}/TrainingData')")
    # 執行不同的策略為
    
    e = time.time()
    print(f"Finish time: {e-s}")
    
    ResultStrategy = pd.DataFrame(ResultStrategy)
    print(ResultStrategy)
    
    # population = Population(Setting, ResultStrategy)
    # population.GenerateOffspring_With_logFile()
    # cProfile.run('population.GenerateOffspring_With_logFile()')
    # population.GenerateOffspring()
    # population.Genealogy()
