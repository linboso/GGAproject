import json 


TIarray = ['MAMA', 'TRIX', 'PLUS_DI', 'PLUS_DM', 'RSI', 'WILLR', 'ULTOSC', 'MOM', 'BOP', 'APO', 'MFI', 'AROONOSC', 'CCI', 
            'CMO', 'ROC', 'PPO', 'MACD', 'STOCH', 'ADX', 'ADXR', 'WMA5', 'WMA10', 'WMA20', 'WMA60', 'TRIMA5', 'TRIMA10', 
            'TRIMA20', 'TRIMA60', 'TEMA5', 'TEMA10', 'TEMA20', 'TEMA60', 'SMA5', 'SMA10', 'SMA20', 'SMA60', 'MA5', 'MA10', 
            'MA20', 'MA60', 'KAMA5', 'KAMA10', 'KAMA20', 'KAMA60', 'EMA5', 'EMA10', 'EMA20', 'EMA60', 'DEMA5', 'DEMA10', 'DEMA20', 'DEMA60', ]


'''
如果有要新增任何新的指標 都只需要 append 到 TIarray 就好了
但是在正式跑 main 之前 要確認 
    1. 新的指標 是正確可以被執行的
    2. 有先執行此程式 完成輸出新的 SignalMap 

'''


def Combine(MovingList:list) -> list: 
    # 利用 backtracking 做組合 
    # 但要 先確保 list 裡面的指標 要是 由小 --> 大 的排列方式
    n = len(MovingList)
    res = []
    def backtrack(tmp, start):
        
        if len(tmp) == 2:
            res.append(tmp.copy())
            return

        for i in range(start, n):
            tmp.append(MovingList[i])
            backtrack(tmp,  i + 1)
            tmp.pop()
    
    backtrack([], 0)
    return res

# =========================================================================

MA_TYPE, NON_MA_TYPE = [], []
MA_TYPE_ARR = [] 

for TS in TIarray:                            
    if TS[-2:].isdigit():                               #如果 最後兩位 是數字
        MA_TYPE.append((int(TS[-2:]), TS))
        MA_TYPE_ARR.append([TS[:-2], int(TS[-2:])])

    elif not TS[-2].isdigit() and TS[-1].isdigit():     #如果 最後一位 是數字
        MA_TYPE.append((int(TS[-1:]), TS))
        MA_TYPE_ARR.append([TS[:-1], int(TS[-1:])])
    else:
        NON_MA_TYPE.append(TS)
        

# with open('../TI_List.json', 'w') as f:
#     inti_file = {
#         "NON_MA_TYPE": NON_MA_TYPE,
#         "MA_TYPE": MA_TYPE_ARR
#     }
#     json.dump(inti_file, f)


MA_TYPE = [TS[1] for TS in sorted(MA_TYPE)]         #天數小的放前面 # ma5 < ma10 <...< ma100
MA_TYPE = Combine(MA_TYPE)


with open('./SignalMap.json', 'w') as f:

    json.dump(NON_MA_TYPE + MA_TYPE, f)

