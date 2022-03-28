
from tracemalloc import start
from turtle import right
import pandas as pd
import json
import numpy as np
from talib import abstract 
import talib






if __name__ ==  '__main__':
    import matplotlib.pyplot as plt
    # case 1: ti vs ti
    # case 2: ti vs constant
    # case 3: others....
    #
    #
    def case1_signal(ti_a: pd.Series(), ti_b: pd.Series()):
        ti_a = ti_a.values
        ti_b = ti_b.values
        r = []
        for i in range(len(ti_a)):
            if ti_a[i] > ti_b[i] and ti_a[i-1] < ti_b[i-1]:
                r.append(1)
            elif ti_a[i] < ti_b[i] and ti_a[i-1] > ti_b[i-1]:
                r.append(-1)
            else:
                r.append(0)
        # signal_long = (ti_a > ti_b) & (ti_a.shift(1) < ti_b.shift(1))
        # signal_short = (ti_a < ti_b) & (ti_a.shift(1) > ti_b.shift(1))
        # r = signal_long.combine(signal_short, (lambda x1, x2: -x2.astype(int) if ( x2 != 0) else x1.astype(int)))
        return r

    def case2_signal(ti: pd.Series(), c1: float, c2: float):
        ti = ti.values
        r = []
        for i in range(len(ti)):
            if ti[i] > c1 and ti[i-1] < c1:
                r.append(1)
            elif ti[i] < c2 and ti[i-1] > c2:
                r.append(-1)
            else:
                r.append(0)
        return r

    def case3_signal(ti1: pd.Series(), ti2: pd.Series(), c1: float, c2: float): #eg. k/d
        pre_signal:list = case1_signal(ti1, ti2)
        ti2 = ti2.values
        r = []
        for i in range(len(ti1)):
            if ti2[i] < c1 and pre_signal[i] == 1:
                r.append(1)
            elif ti2[i] > c2 and pre_signal[i] == -1:
                r.append(-1)
            else:
                r.append(0)
        return r        


    def case4_signal(ti1:pd.Series(), ti2:pd.Series(), c1:float, c2:float): # eg. macd
        pre_signal1:list = case1_signal(ti1, ti2)
        pre_signal2:list = case2_signal(ti1, c1, c2)
        r = []
        for i in range(len(ti1)):
            if pre_signal1[i] == 1 or pre_signal2[i] == 1:
                r.append(1)
            elif pre_signal1[i] == -1 or pre_signal2[i] == -1:
                r.append(-1)
            else:
                r.append(0)
        return r  


    def KD_signal(K,D):
        K = K.values
        D = D.values
        KD_signal = []
        for day in range(0,len(K)):
            if D[day] < 20 and K[day] > D[day] and K[day-1] < D[day-1]:
                KD_signal.append(1)
            elif D[day] > 80 and K[day] < D[day] and K[day-1] > D[day-1]:
                KD_signal.append(-1)
            else:
                KD_signal.append(0)
        KD_signal= pd.Series(KD_signal)
        KD_signal = KD_signal.rename('KD_signal')
        #print(KD_signal)
        return KD_signal

    def MACD_signal(DIF,MACD_DEM):
        DIF = DIF.values
        MACD_DEM = MACD_DEM.values
        MACD_signal = []
        for day in range(0,len(DIF)):
            if (DIF[day] > 0 and DIF[day-1] < 0 ) or (DIF[day] > MACD_DEM[day] and DIF[day-1] < MACD_DEM[day-1]):
                MACD_signal.append(1)
            elif (DIF[day] < 0 and DIF[day-1] > 0 ) or (DIF[day] < MACD_DEM[day] and DIF[day-1] > MACD_DEM[day-1]):
                MACD_signal.append(-1)
            else:
                MACD_signal.append(0)
        MACD_signal= pd.Series(MACD_signal)
        MACD_signal = MACD_signal.rename('MACD_signal')
        #print(MACD_signal)
        return MACD_signal    





    with open('../stock/0050.TW/2009-08-30~2010-12-30/techical_indicator.json') as f:
        data = pd.DataFrame(json.load(f))

    import time
    # r = case3_signal(data['SLOWK'], data['SLOWD'], 20, 80) work
    start = time.time()

    r = case4_signal(data['MACD'], data['MACDSIGNAL'], 0 ,0)
    r = pd.DataFrame(r)

    end = time.time()
    print(end - start)

    r.plot( color='green' ,linewidth = 5.0)

    start = time.time()
    # c = KD_signal(data['SLOWK'], data['SLOWD'])
    c = MACD_signal(data['MACD'], data['MACDSIGNAL'])

    end = time.time()
    print(end - start)
    plt.plot(c.index, c.values, color='red', linewidth = 1.0)
    plt.show()

