import json
import os


def ReadSetting():
    try:
        with open("../setting.json") as f:
            setting = json.load(f)
            print("============= Setting Data =============")
            print("Stock ID: ", setting["StockID"])
            print("Start Date: ", setting["StartDate"])
            print("End Date: ", setting["EndDate"])
            print("Techical Indicator: ", setting["TechicalIndicator"])
            print("========================================")
        return setting
    except:
        init_setting = {
            "StockID":"0050.TW",
            "StartDate":"2009-08-30",
            "EndDate":"2010-12-30",
            "TechicalIndicator":["MA5", "MA20", "RSI", "MACD"] } #init setting format
        with open("../setting.json", "w") as f:
            json.dump(init_setting, f) # save as .json file
        print("...Create setting.json at \"../setting.json\"")
        print("Reloading...")
        return ReadSetting() #Reload data


def CheckPath(savepath):
    if not os.path.exists(savepath):
        try:
            #print(savepath)
            os.makedirs(savepath)
            print("Create folder successfully")
            return True
        except:
            print("Failed to create folder")
            return False
    else:
        return True





# def getCalculateTIValue(_start, _end, _ti_list, readpath, savepath):
#     _df_with_ti = df = pd.DataFrame()
#     try:
#         if CheckPath(readpath):
#             with open(f"{readpath}/stockdata.json") as f:
#                 df = pd.DataFrame(json.load(f))
#             with open(f"{readpath}/origin_stockdata.json") as f:
#                 _df_with_ti = pd.DataFrame(json.load(f))
#             #read stock.json file and convent to DataFrame Type
#     except:
#         print(f"At {os.getcwd() + savepath} no file name \" {_start}~{_end}/stockdata.json\"\r\n")

#     _Techical_Indicators_list = _ti_list #select n techical indicator
#     _ALL_TI_LIST = talib.get_functions()
#     for _ti in _Techical_Indicators_list:
#         try:
#             if not _ti in _ALL_TI_LIST:
#                 output = eval(f'abstract.{_ti[:2]}(df, timeperiod = {_ti[2:]})')
#                 #Talib not suport MA5, MA10, MAxx so need to use 'timeperiod' attr
#             else:
#                 output = eval(f'abstract.{_ti}(df)') #Great Function!
#             output = pd.DataFrame(output) #turn "output" into DataFrame type
#             output.columns = [_ti] if list(output.columns)[0]==0 else [str(i).upper() for i in list(output.columns)] #name it
#             _df_with_ti = pd.concat([_df_with_ti, output], axis=1)
#             #merge Techical indicator value into main.json file
#         except:
#             print(f"--> No such techical Inidicator like \"{_ti}\"\r\n")
#     #print(_df_with_ti)
#     _df_with_ti.to_json(f"{savepath}/techical_indicator.json" ,orient='records') #save file 
#     print(f"Saving techical_indicator.json file at {savepath}\r\n")
    
#     # return _df_with_ti #return new table

