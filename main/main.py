
from PreProCessing.DownloadData import DownloadStockData
from PreProCessing.CalculateTIvalue import TIValue
from PreProCessing.TI2Signal import TI2Signal
from PreProCessing.SettingFile import SettingFile
from PreProCessing.Cov2Image import Simage
from PreProCessing.Ranking import Ranking


from Algo.Population import Population
from Algo.Chromosome import Chromosome


Setting = SettingFile()
Setting.print()



# DownloadStockData().StockDataDownload()
# 下載 股票資料

# TIv = TIValue()
# TIv.CalculateTIValue()
# 計算各種 我們指定的 指標的 value
# 都在 setting.json 檔案裡

# TI2Signal().ProduceSignal()
# TI2Signal().ProduceTable()
# # 把value 轉換成 signal 

# Simage().StockImage()
# Simage().SignalImage()


# Ranking().Top555() 
# 執行 ranking 策略為 Top555 


population = Population(pSize=50, WeightPart=100, CrossoverRate=0.8, MutationRate=0.03, InversionRate=0.6, Generation=10)
population.GenerateGeneration_With_logFile()


