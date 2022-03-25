import pandas as pd
import json
from talib import abstract 
import talib


def MA_signal(MA_l,MA_b):
    MA_l = MA_l.values
    MA_b = MA_b.values
    MA_signal = []
    for day in range(0,len(MA_l)):
        if MA_l[day] > MA_b[day] and MA_l[day-1] < MA_b[day-1]:
            MA_signal.append(1)
        elif MA_l[day] < MA_b[day] and MA_l[day-1] > MA_b[day-1]:
            MA_signal.append(0)
        else:
            MA_signal.append(None)
    MA_signal= pd.Series(MA_signal)
    MA_signal = MA_signal.rename('MA_signal')
    #print(MA_signal)
    return MA_signal







