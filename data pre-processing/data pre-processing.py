
import numpy as np
import pandas as pd
import talib

from package.getStockData import DownloadStockData
from package.CalculateTIvalue import TIValue


TIv = TIValue()
stockvalue = DownloadStockData().StockDataDownload()
TIv.CalculateTIValue()






