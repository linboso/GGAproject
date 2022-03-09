import numpy as np
import pandas as pd
import talib
# 

c = np.random.randn(100)

k, d = talib.STOCHRSI(c)

rsi = talib.RSI(c)
k, d = talib.STOCHF(rsi, rsi, rsi)

rsi = talib.RSI(c)
k, d = talib.STOCH(rsi, rsi, rsi)


print(k, d)