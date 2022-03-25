
import pandas as pd
import json
from talib import abstract 
import talib






if __name__ ==  '__main__':
    import matplotlib.pyplot as plt
    # case 1: ti vs ti
    # case 2: ti vs constant
    # case 3: others....
    #
    #
    def case1_signal(ti_a, ti_b):
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

    # def case2_signal(ti, c):
    #     signal_long

    def MA_signal(MA_l, MA_b):
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
        # print(MA_signal)
        return MA_signal


    with open('../stock/0050.TW/2009-08-30~2010-12-30/techical_indicator.json') as f:
        data = pd.DataFrame(json.load(f))

    import time

    start = time.time()
    r = case1_signal(data['MA5'], data['MA20'])
    end = time.time()
    print(end-start)

    # r.plot(color='green' ,linewidth = 5.0)

    start = time.time()
    c = MA_signal(data['MA5'], data['MA20'])
    end =  time.time()

    print(end - start)

    # cc = []
    # for i in c:
    #     if i == 0:
    #         cc.append(-1)
    #     elif i == 1:
    #         cc.append(1)
    #     else:
    #         cc.append(0)

    # plt.plot(cc, color='red', linewidth = 1.0)
    # plt.show()

