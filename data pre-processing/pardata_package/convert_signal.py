import pandas as pd

def combine_signal(TI_Buy_series,TI_sell_series):
    TS_signal = []
    for i in TI_Buy_series.size:
        TIbuy = TI_Buy_series[i]
        TIsell = TI_sell_series[i]
        judge_signal = None
        if TIbuy ==1 & TIsell ==0:
            judge_signal = 10
        elif TIbuy == 1:
            judge_signal = 1
        elif TIsell == 0:
            judge_signal = 0
        else:
            judge_signal = None
        TS_signal.append(judge_signal)
    return TS_signal
#input two series ,then gerenrating TS_signal      
       
def ma(MA_l,MA_b,MA_l_yesterday,MA_b_yesterday):
    if MA_l_yesterday < MA_b_yesterday & MA_l > MA_b:
        return 1
    if MA_l_yesterday > MA_b_yesterday & MA_l < MA_b:
        return 0
    return -1

def RSI_signal(rsi):
    rsi = rsi.values
    RSI_singal = []
    for day in range(0,len(rsi)):
        if rsi[day] > 30 and rsi[day-1] < 30:
            RSI_singal.append(1)
        elif rsi[day] < 70 and rsi[day-1] > 70:
            RSI_singal.append(0)
        else:
            RSI_singal.append(None)
    RSI= pd.Series(RSI_singal)
    RSI = RSI.rename('RSI_signal')
    print(RSI)
    return RSI



