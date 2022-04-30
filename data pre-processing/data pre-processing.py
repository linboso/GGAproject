
from package.DownloadData import DownloadStockData
from package.CalculateTIvalue import TIValue
from package.TI2Signal import TI2Signal
from package.SettingFile import SettingFile
from package.Cov2Image import Simage
from package.Ranking import Ranking



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


Ranking().Top555() 
# 執行 ranking 策略為 Top555 




