import pandas as pd
import json

#Subroutine建立表

def create_TI_signal_table(TI_value):
    with open(f"./stock/0050.TW/2009-08-30~2010-12-30/origin_stockdata.json", 'r') as f:
            TI_signal = pd.DataFrame(json.load(f))
    
    try:
        TI_signal = pd.concat([TI_signal,MA_signal(TI_value["MA5"],TI_value["MA20"])],axis=1)
    except:
        print("Don't have MA5&MA20 this time")

    try:
        TI_signal = pd.concat([TI_signal,RSI_signal(TI_value["RSI"])],axis=1)
    except:
        print("Don't have RSI this time")
    
    try:
        TI_signal = pd.concat([TI_signal,WMS_R_signal(TI_value["WMS%R"])],axis=1)
    except:
        print("Don't have WMS%R this time")          
    
    try:
        TI_signal = pd.concat([TI_signal,MOM_signal(TI_value["MOM"])],axis=1)
    except:
        print("Don't have MOM this time")
    
    try:
        TI_signal = pd.concat([TI_signal,PSY_signal(TI_value["PSY"])],axis=1)
    except:
        print("Don't have PSY this time")
    
    try:
        TI_signal = pd.concat([TI_signal,CCI_signal(TI_value["CCI"])],axis=1)
    except:
        print("Don't have CCI this time")
    
    try:
        TI_signal = pd.concat([TI_signal,KD_signal(TI_value["K"],TI_value["D"])],axis=1)
    except:
        print("Don't have KD this time")
    
    try:
        TI_signal = pd.concat([TI_signal,MACD_signal(TI_value["DIF"],TI_value["MACD_DEM"])],axis=1)
    except:
        print("Don't have MACD this time")
    
    try:
        TI_signal = pd.concat([TI_signal,BIAS_signal(TI_value["BIAS"])],axis=1)
    except:
        print("Don't have BIAS this time")

    try:
        TI_signal = pd.concat([TI_signal,DI_signal(TI_value["DI_positive"],TI_value["DI_negative"])],axis=1)
    except:
        print("Don't have DI this time")

    TI_signal.to_csv(f"./stock/0050.TW/2009-08-30~2010-12-30/TI_signal.csv") #save file 
    # save the TI_signal file
    return TI_signal
#save TI_signal and return the result

def create_TS_signal_table(TI_signal):
    with open(f"./stock/0050.TW/2009-08-30~2010-12-30/origin_stockdata.json", 'r') as f:
            TS_signal = pd.DataFrame(json.load(f))
    print(TS_signal)
    TI_columns = TI_signal.columns #get TI_signal table name
    n = 0
    for buy in TI_columns[6:]:
        for sell in TI_columns[6:]:
            n+=1
            print("TS"+ str(n) + "(buy:"+ buy +" | " + "sell:"+ sell+")")
            TI_buy = TI_signal[buy].values
            TI_sell = TI_signal[sell].values
            each_TS_signal = []
            for day in range(0,len(TI_buy)):
                combine_signal = None
                if TI_buy[day] == 1 and TI_sell[day] == 0:
                    combine_signal = 10
                elif TI_buy[day] == 1:
                    combine_signal = 1
                elif TI_sell[day] == 0:
                    combine_signal = 0
                else:
                    combine_signal = None
                each_TS_signal.append(combine_signal)
            each_TS_signal= pd.Series(each_TS_signal)
            each_TS_signal = each_TS_signal.rename("TS"+ str(n) + "(buy:"+ buy +" | " + "sell:"+ sell+")")   
            TS_signal = pd.concat([TS_signal,each_TS_signal],axis=1)
    TS_signal.to_csv(f"./stock/0050.TW/2009-08-30~2010-12-30/TS_signal.csv") #save file 
    # save the TI_signal file
    return TS_signal
#save TS_signal and return the result


#-----below TI_value convert TI_signal list-----
# 1.MA_l & MA_b 
# 2.RSI 
# 3.WMS%R 
# 4.MOM
# 5.PSY
# 6.CCI
# 7.KD
# 8.DIF & MACD(DEM)
# 9.BIAS
# 10.+DI & -DI

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

def RSI_signal(RSI):
    RSI = RSI.values
    RSI_signal = []
    for day in range(0,len(RSI)):
        if RSI[day] > 30 and RSI[day-1] < 30:
            RSI_signal.append(1)
        elif RSI[day] < 70 and RSI[day-1] > 70:
            RSI_signal.append(0)
        else:
            RSI_signal.append(None)
    RSI_signal= pd.Series(RSI_signal)
    RSI_signal = RSI_signal.rename('RSI_signal')
    #print(RSI_signal)
    return RSI_signal

def WMS_R_signal(WMS_R):
    WMS_R = WMS_R.values
    WMS_R_signal = []
    for day in range(0,len(WMS_R)):
        if WMS_R[day] < 80 and WMS_R[day-1] > 80:
            WMS_R_signal.append(1)
        elif WMS_R[day] > 20 and WMS_R[day-1] < 20:
            WMS_R_signal.append(0)
        else:
            WMS_R_signal.append(None)
    WMS_R_signal= pd.Series(WMS_R_signal)
    WMS_R_signal = WMS_R_signal.rename('WMS%R_signal')
    #print(WMS_R_signal)
    return WMS_R_signal    

def MOM_signal(MOM):
    MOM = MOM.values
    MOM_signal = []
    for day in range(0,len(MOM)):
        if MOM[day] > 0 and MOM[day-1] < 0:
            MOM_signal.append(1)
        elif MOM[day] < 0 and MOM[day-1] > 0:
            MOM_signal.append(0)
        else:
            MOM_signal.append(None)
    MOM_signal= pd.Series(MOM_signal)
    MOM_signal = MOM_signal.rename('MOM_signal')
    #print(MOM_signal)
    return MOM_signal    

def PSY_signal(PSY):
    PSY = PSY.values
    PSY_signal = []
    for day in range(0,len(PSY)):
        if PSY[day] > 0.25 and PSY[day-1] < 0.25:
            PSY_signal.append(1)
        elif PSY[day] < 0.75 and PSY[day-1] > 0.75:
            PSY_signal.append(0)
        else:
            PSY_signal.append(None)
    PSY_signal= pd.Series(PSY_signal)
    PSY_signal = PSY_signal.rename('PSY_signal')
    #print(PSY_signal)
    return PSY_signal

def CCI_signal(CCI):
    CCI = CCI.values
    CCI_signal = []
    for day in range(0,len(CCI)):
        if CCI[day] > -100 and CCI[day-1] < -100:
            CCI_signal.append(1)
        elif CCI[day] < 100 and CCI[day-1] > 100:
            CCI_signal.append(0)
        else:
            CCI_signal.append(None)
    CCI_signal= pd.Series(CCI_signal)
    CCI_signal = CCI_signal.rename('CCI_signal')
    #print(CCI_signal)
    return CCI_signal    

def KD_signal(K,D):
    K = K.values
    D = D.values
    KD_signal = []
    for day in range(0,len(K)):
        if D[day] < 20 and K[day] > D[day] and K[day-1] < D[day-1]:
            KD_signal.append(1)
        elif D[day] > 80 and K[day] < D[day] and K[day-1] > D[day-1]:
            KD_signal.append(0)
        else:
            KD_signal.append(None)
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
            MACD_signal.append(0)
        else:
            MACD_signal.append(None)
    MACD_signal= pd.Series(MACD_signal)
    MACD_signal = MACD_signal.rename('MACD_signal')
    #print(MACD_signal)
    return MACD_signal    

def BIAS_signal(BIAS):
    BIAS = BIAS.values
    BIAS_signal = []
    for day in range(0,len(BIAS)):
        if BIAS[day] > -0.045 and BIAS[day-1] < -0.045:
            BIAS_signal.append(1)
        elif BIAS[day] < 0.05 and BIAS[day-1] > 0.05:
            BIAS_signal.append(0)
        else:
            BIAS_signal.append(None)
    BIAS_signal= pd.Series(BIAS_signal)
    BIAS_signal = BIAS_signal.rename('BIAS_signal')
    #print(BIAS_singal)
    return BIAS_signal    

def DI_signal(DI_positive,DI_negative):
    DI_positive = DI_positive.values
    DI_negative = DI_negative.values
    DI_signal = []
    for day in range(0,len(DI_positive)):
        if DI_positive[day] > DI_negative[day] and DI_positive[day-1] < DI_negative[day-1]:
            DI_signal.append(1)
        elif DI_positive[day] < DI_negative[day] and DI_positive[day-1] > DI_negative[day-1]:
            DI_signal.append(0)
        else:
            DI_signal.append(None)
    DI_signal= pd.Series(DI_signal)
    DI_signal = DI_signal.rename('DI_signal')
    #print(DI_signal)
    return DI_signal


