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


    with open('../stock/0050.TW/2009-08-30~2010-12-30/techical_indicator.json') as f:
        data = pd.DataFrame(json.load(f))

    r = case4_signal(data['MACD'], data['MACDSIGNAL'], 0 ,0)
    r = pd.DataFrame(r)
    r.plot( color='green' ,linewidth = 3.0)

    plt.show()

