
import numpy as np
import pandas as pd
import talib


from package.DownloadData import DownloadStockData
from package.CalculateTIvalue import TIValue
from package.TI2Signal import TI2Signal
from package.SettingFile import SettingFile



Setting = SettingFile()
Setting.Read(show = True)



TIv = TIValue()
DownloadStockData().StockDataDownload()

TIv.CalculateTIValue()

TI2Signal().ProduceSignal()






