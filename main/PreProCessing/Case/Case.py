import pandas as pd
import json
import numpy as np

def case1(ti1: pd.Series, ti2: pd.Series):
    ti1 = ti1.to_numpy()
    ti2 = ti2.to_numpy()

    r = np.zeros(len(ti1))
    for i in range(len(ti1)):
        if ti1[i] > ti2[i] and ti1[i-1] < ti2[i-1]:
            r[i] = 1
        elif ti1[i] < ti2[i] and ti1[i-1] > ti2[i-1]:
            r[i] = -1 
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


if __name__ ==  '__main__':
    import sys, os
    with open("../../Setting.json") as f:
        Setting = json.load(f)

    with open(f"../../{Setting['Path']}/{Setting['StockID']}/TrainingData/Signal.json") as f:
        data = pd.DataFrame(json.load(f))
        
    print(data)

    ## Fix Case Problem 

    

