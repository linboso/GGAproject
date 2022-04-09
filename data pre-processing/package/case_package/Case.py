import pandas as pd
import json


def case1(ti1: pd.Series, ti2: pd.Series):
    ti1 = ti1.values
    ti2 = ti2.values
    r = []
    for i in range(len(ti1)):
        if ti1[i] > ti2[i] and ti1[i-1] < ti2[i-1]:
            r.append(1)
        elif ti1[i] < ti2[i] and ti1[i-1] > ti2[i-1]:
            r.append(-1)
        else:
            r.append(0)
    return r

def case2(ti: pd.Series, c1: float, c2: float):
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

def case3(ti1: pd.Series, ti2: pd.Series, c1: float, c2: float): #eg. k/d
    pre_signal:list = case1(ti1, ti2)
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

def case4(ti1:pd.Series, ti2:pd.Series, c1:float, c2:float): # eg. macd
    pre_signal1:list = case1(ti1, ti2)
    pre_signal2:list = case2(ti1, c1, c2)
    r = []
    for i in range(len(ti1)):
        if pre_signal1[i] == 1 or pre_signal2[i] == 1:
            r.append(1)
        elif pre_signal1[i] == -1 or pre_signal2[i] == -1:
            r.append(-1)
        else:
            r.append(0)
    return r  



def case5(ti1:pd.Series, ti2:pd.Series, ti3:pd.Series, c1:float): # eg. adx
    pre_signal1:list = case1(ti1, c1, c1)
    pre_signal2:list = case2(ti2, ti3)
    r = []
    for i in range(len(ti1)):
        if pre_signal1[i] > c1:
            if pre_signal2[i] == 1:
                r.append(1)
            elif pre_signal2[i] == -1:
                r.append(-1)
        else:
            r.append(0)
    return r


def case6(ti1:pd.Series, ti2:pd.Series, ti3:pd.Series, ti4:pd.Series): # eg. adxr    
    pre_signal1:list = case2(ti1, ti2)
    pre_signal2:list = case2(ti3, ti4)
    r = []
    for i in range(len(ti1)):
        if pre_signal1[i] == 1:
            if pre_signal2[i] == 1:
                r.append(1)
            elif pre_signal2[i] == -1:
                r.append(-1)
        else:
            r.append(0)
    return r


def caseAROON(ti1:pd.Series, ti2:pd.Series, ti3:pd.Series, c1:float, c2:float, c3:float): # eg. aroon
    pre_signal1:list = case2(ti1, c1, c1)
    pre_signal2:list = case2(ti2, c2, c3)
    pre_signal3:list = case2(ti3, c2, c3)

    r = []
    for i in range(len(ti1)):
        if pre_signal1[i] == 1 and (pre_signal2[i] == 1 or pre_signal3[i] == -1):
            r.append(1)
        elif pre_signal1[i] == -1 and (pre_signal2[i] == -1 or pre_signal3[i] == 1):
            r.append(-1)
        else:
            r.append(0)
    return r




if __name__ ==  '__main__':
    import matplotlib.pyplot as plt


    with open('../stock/0050.TW/2009-08-30~2010-12-30/technical_indicator.json') as f:
        data = pd.DataFrame(json.load(f))

    #  r = case4(data['MACD'], data['MACDSIGNAL'], 0 ,0)
    r = caseAROON(data['AROONOSC'], data['AROONUP'], data['AROONDOWN'], 0, 70, 50)
    plt.plot(data.index, r, color='black' ,linewidth = 5, label='signal 1')

    r = case2(data['AROONOSC'], 0, 0)
    plt.plot(data.index, r, linewidth = 1, label='osc')

    r = case2(data['AROONUP'], 70 , 50)
    plt.plot(data.index, r, linewidth = 1, label='up')
    
    r = case2(data['AROONDOWN'], 70 , 50)
    plt.plot(data.index, r, linewidth = 1, label='down')

    # plt.plot(data['AROONUP'], label="AROONUP")
    # plt.plot(data['AROONDOWN'], label='AROONDOWN')

    plt.legend()
    plt.show()

