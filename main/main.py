
from PreProCessing.DownloadData import DownloadStockData
from PreProCessing.CalculateTIvalue import TIValue
from PreProCessing.TI2Signal import TI2Signal
from PreProCessing.Ranking import Ranking

# from PreProCessing.Cov2Image import Simage

from SettingFile import SettingFile

from Algo.Population import Population

import cProfile

import Algo.BackTesting

Setting = SettingFile()
Setting.print() 
Setting = Setting.Read()

# DownloadStockData(Setting=Setting).DownloadStockData()
# 下載 股票資料

#TIv = TIValue(Setting = Setting)
#TIv.CalculateTIValue()
# 計算各種 我們指定的 指標的 value
# 都在 setting.json 檔案裡

#TI2Signal(Setting = Setting).ProduceSignal()
#TI2Signal(Setting = Setting).ProduceTable()
# # # 把value 轉換成 signal 

#Ranking(Setting = Setting).Top555() 
# 執行 ranking 策略為 Top555 / Top777



#population = Population(Setting=Setting)
# cProfile.run('population.GenerateOffspring_With_logFile()')
#population.GenerateOffspring_With_logFile()
# population.GenerateOffspring()
# population.Genealogy()
#iterate



ini  = Algo.BackTesting.BackTesting(0.25,0.15,Setting = Setting)
#之後補GTSP
ini.ProduceTable_withoutSLSP()
ini.Run()

#chromosome 用 array 算 fintness?