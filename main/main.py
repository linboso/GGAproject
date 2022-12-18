
#from PreProCessing.DownloadData import DownloadStockData
from PreProCessing.CalculateTIvalue import TIValue
from PreProCessing.TI2Signal import TI2Signal
from PreProCessing.Ranking import Ranking

# from PreProCessing.Cov2Image import Simage

from RFiles import RFiles

from Algo.Population import Population
from Algo.BackTesting import BackTesting

import cProfile

Files = RFiles()
Setting = Files.Setting
SignalMap = Files.SignalMap
TI_List = Files.TI_List
Files.print()

# # DownloadStockData(Setting=Setting).DownloadStockData()
# # 下載 股票資料

# # TIv = TIValue(Setting = Setting, TI_List = TI_List)
# # TIv.CalculateTIValue()
# # 計算各種 我們指定的 指標的 value
# # 都在 setting.json 檔案裡

# # TI2Signal(Setting = Setting).ProduceSignal()
# # TI2Signal(Setting = Setting).ProduceTable()
# # 把value 轉換成 signal 

# # Ranking(Setting = Setting).Top555() 
# # 執行 ranking 策略為 Top555 / Top777


# population = Population(Setting=Setting)
# population.GenerateOffspring_With_logFile()
# # # cProfile.run('population.GenerateOffspring_With_logFile()')
# population.GenerateOffspring()
# population.Genealogy()
# #iterate

obj = BackTesting()
obj.PreBackTesting()
obj.Run()
obj.Query()


#chromosome 用 array 算 fintness?