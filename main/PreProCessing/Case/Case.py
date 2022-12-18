import pandas as pd
import json
import numpy as np


# Ti Value 是 Json 匯入的 所以要用 pd
def case1(ti1: pd.Series, ti2: pd.Series) -> np.array:
    ti1:np.array = ti1.to_numpy()
    ti2:np.array = ti2.to_numpy()

    r:np.array = np.zeros(len(ti1))
    for i in range(len(ti1)):
        if ti1[i] > ti2[i] and ti1[i-1] < ti2[i-1]:
            r[i] = 1
        elif ti1[i] < ti2[i] and ti1[i-1] > ti2[i-1]:
            r[i] = -1 

    return r


def case2(ti: pd.Series, c1: float, c2: float) -> np.array:
    ti:np.array = ti.to_numpy()
    r:np.array = np.zeros(len(ti))
    for i in range(len(ti)):
        if ti[i] > c1 and ti[i-1] < c1:
            r[i] = 1
        elif ti[i] < c2 and ti[i-1] > c2:
            r[i] = -1
 
    return r



def case3(ti1: pd.Series, ti2: pd.Series, c1: float, c2: float) -> np.array: #eg. k/d
    pre_signal:np.array = case1(ti1, ti2)
    ti2:np.array = ti2.to_numpy()

    r:np.array = np.zeros(len(ti1))

    for i in range(len(ti1)):
        if ti2[i] < c1 and pre_signal[i] == 1:
            r[i] = 1
        elif ti2[i] > c2 and pre_signal[i] == -1:
            r[i] = -1
    return r        


def case4(ti1:pd.Series, ti2:pd.Series, c1:float, c2:float) -> np.array: # eg. macd
    pre_signal1:np.array = case1(ti1, ti2)
    pre_signal2:np.array = case2(ti1, c1, c2)

    r:np.array = np.zeros(len(ti1))

    for i in range(len(ti1)):
        if pre_signal1[i] == 1 or pre_signal2[i] == 1:
            r[i] = 1
        elif pre_signal1[i] == -1 or pre_signal2[i] == -1:
            r[i] = -1

    return r  



def case5(ti1:pd.Series, ti2:pd.Series, ti3:pd.Series, c1:float) -> np.array: # eg. adx
    pre_signal1:np.array = case1(ti1, c1, c1)
    pre_signal2:np.array = case2(ti2, ti3)
    
    r:np.array = np.zeros(len(ti1))

    for i in range(len(ti1)):
        if pre_signal1[i] > c1:
            if pre_signal2[i] == 1:
                r[i] = 1
            elif pre_signal2[i] == -1:
                r[i] = -1
        
    return r

def case6(ti1:pd.Series, ti2:pd.Series, ti3:pd.Series, ti4:pd.Series) -> np.array: # eg. adxr    
    pre_signal1:np.array = case2(ti1, ti2)
    pre_signal2:np.array = case2(ti3, ti4)
    
    r:np.array = np.zeros(len(ti1))
    
    for i in range(len(ti1)):
        if pre_signal1[i] == 1:
            if pre_signal2[i] == 1:
                r[i] = 1
            elif pre_signal2[i] == -1:
                r[i] = -1

    return r


#Old version 偏慢

# def case2(ti: pd.Series, c1: float, c2: float):
#     ti = ti.values
#     r = []
#     for i in range(len(ti)):
#         if ti[i] > c1 and ti[i-1] < c1:
#             r.append(1)
#         elif ti[i] < c2 and ti[i-1] > c2:
#             r.append(-1)
#         else:
#             r.append(0)
#     return r

# def case3(ti1: pd.Series, ti2: pd.Series, c1: float, c2: float): #eg. k/d
#     pre_signal:np.ndarray = case1(ti1, ti2)
#     ti2 = ti2.to_numpy()
#     r = []
#     for i in range(len(ti1)):
#         if ti2[i] < c1 and pre_signal[i] == 1:
#             r.append(1)
#         elif ti2[i] > c2 and pre_signal[i] == -1:
#             r.append(-1)
#         else:
#             r.append(0)
#     return r        


if __name__ ==  '__main__':
    import sys, os
    import cProfile
    with open("../../Setting.json") as f:
        Setting = json.load(f)

    with open(f"../../{Setting['Path']}/{Setting['StockID']}/TrainingData/TIvalue.json") as f:
        data = pd.DataFrame(json.load(f))
        
    re = case1(data['MA5'], data['MA20'])

    re = pd.DataFrame(re)
    re.to_csv("Signal_Debug.csv")

    # cProfile.run("case1(data['MA5'], data['MA15'])")

    

    

