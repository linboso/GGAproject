
from cProfile import label
import matplotlib.pyplot as plt
import pandas as pd
import talib
import json
from SettingFile import SettingFile

def case1_signal(ti1: pd.Series, ti2: pd.Series):
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

def case2_signal(ti: pd.Series, c1: float, c2: float):
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

def case3_signal(ti1: pd.Series, ti2: pd.Series, c1: float, c2: float): #eg. k/d
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



def case4_signal(ti1:pd.Series, ti2:pd.Series, c1:float, c2:float): # eg. macd
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



st = SettingFile().Read()


path  = './jsonformatter.json'
with open(path, 'r', encoding="utf-8") as f:
    data = json.load(f)

new_data = pd.DataFrame(data)
# print(new_data)


with open('../stock/0050.TW/2009-08-30~2010-12-30/technical_indicator.json') as f:
    data = pd.DataFrame(json.load(f))


# tmp = []
x = data.index
# for i in st['TechnicalIndicator']:
#     if i[:2] in new_data and i not in new_data:

#         tmp.append(i)
#         if len(tmp) == 2:
#             print(tmp)

#     elif i in new_data:
#         c = new_data[i]['Case']
#         r = []
#         if c == "2":
#             r = case2_signal(data[i], new_data[i]["InputArray"]['C1'], new_data[i]["InputArray"]['C2'])
#         elif c == "3":
#             r = case3_signal(data[new_data[i]["InputArray"]['ti1']], data[new_data[i]["InputArray"]['ti2']], new_data[i]["InputArray"]['C1'], new_data[i]["InputArray"]['C2'])
#         elif c == "4":
#              r = case4_signal(data[new_data[i]["InputArray"]['ti1']], data[new_data[i]["InputArray"]['ti2']], new_data[i]["InputArray"]['C1'], new_data[i]["InputArray"]['C2'])

#         plt.plot(x, r, label=f'Case{new_data[i]["Case"]}{i}')


r = case3_signal(data['SLOWK'], data['SLOWD'], 20, 80)
plt.plot(x, r, label = "case3 sss")








plt.legend()
plt.show()




