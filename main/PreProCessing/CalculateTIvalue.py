import pandas as pd
import talib
from talib import abstract



class TIValue():
    def __init__(self, Setting) -> None:
        setting = Setting
        
        self.stock_id = setting['StockID']
        self.start = setting['TrainingPeriod']['StartDate']
        self.end = setting['TrainingPeriod']['EndDate']
        self.ti_list = setting['TechnicalIndicator']

        if __name__ == "__main__":
            self.path = f"../{setting['Path']}/{setting['StockID']}/TrainingData"
        else:
            self.path = f"{setting['Path']}/{setting['StockID']}/TrainingData"

    def CalculateTIValue(self):
        df = pd.DataFrame()

        try:
            with open(f"{self.path}/StockData.json") as f:
                df = pd.read_json(f)

        except:
            print(f"缺失 {self.stock_id} 的 StockData.json 的資料")



        _df_with_ti = pd.DataFrame()
        _ALL_TI_LIST = talib.get_functions()
        # print(_ALL_TI_LIST)
 
        for _ti in self.ti_list: #selected n techical indicator
            try:
                # ========================= need improve
                if not _ti in _ALL_TI_LIST:
                    for k in range(len(_ti)):
                        if _ti[k].isdigit() == True: # 這邊需要改
                            break

                    output = eval(f'abstract.{_ti[:k]}(df, timeperiod = {_ti[k:]})')

                    #Talib not suport MA5, MA10, MAxx so need to use 'timeperiod' attr
                else:
                    output = eval(f'abstract.{_ti}(df)') #eval is great Function!


                output = pd.DataFrame(output) #turn "output" into DataFrame type
                output.columns = [_ti] if list(output.columns)[0]==0 else [str(i).upper() for i in list(output.columns)] #name it
                _df_with_ti = pd.concat([_df_with_ti, output], axis=1)
                #merge Techical indicator value into main.json file
            except:
                print(f"--> No such technical Inidicator like \"{_ti}\"\r\n")
                

        print(f"計算出來的 數值有: {list(_df_with_ti.columns)}")

        try:
            _df_with_ti.to_json(f"{self.path}/TIvalue.json" ,orient='records') #save file 
            print(f"Saving TIvalue.json file at {self.path}\r\n")
        except:
            print(f"Saving File Faild")



    def getTIValue(self):
        table = pd.DataFrame()
        with open(f"{self.path}/TIvalue.json", 'r') as f:
            table = pd.read_json(f)

        return table




if __name__ == "__main__":
    # 獨立執行 測試用
    import json

    with open('../setting.json') as f:
        TIv = TIValue(json.load(f))

    TIv.CalculateTIValue()

    

