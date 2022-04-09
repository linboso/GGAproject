from turtle import delay
import pandas as pd
import json
import os

from .SettingFile import SettingFile
from .case_package import Case


class TI2Signal():
    def __init__(self) -> None:
        setting = SettingFile().Read()
        self.stock_id = setting['StockID']
        self.start = setting['StartDate']
        self.end = setting['EndDate']
        self.ti_list = setting['TechnicalIndicator']
        self.savepath = f"stock/{self.stock_id}/{self.start}~{self.end}"
        self.readpath = f"stock/{self.stock_id}/{self.start}~{self.end}"

    def ProduceSignal(self):
        with open('./package/case_package/TIformat.json', 'r', encoding="utf-8") as f:
            ti_format = pd.DataFrame(json.load(f))

        with open(f"{self.readpath}/TIvalue.json") as f:
            TIvale = pd.DataFrame(json.load(f))

        with open(f"{self.readpath}/History.json") as f:
            data = pd.DataFrame(json.load(f))

        signal = tmp = []
        
        for i in self.ti_list:
            if i[:2] in ti_format and i not in ti_format:
                tmp.append(i)
            elif i in ti_format:
                case = ti_format[i]['Case']
                if case == "2":
                    signal = Case.case2(
                        TIvale[ti_format[i]["InputArray"]['ti1']],    # Get ti 1 Value
                        ti_format[i]["InputArray"]['C1'],           # C1
                        ti_format[i]["InputArray"]['C2']            # C2
                    )
                elif case == "3":
                    signal = Case.case3(
                        TIvale[ti_format[i]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[i]["InputArray"]['ti2']],    # Get ti 2 Value
                        ti_format[i]["InputArray"]['C1'],           # C1
                        ti_format[i]["InputArray"]['C2']            # C2
                    )
                elif case == "4":
                    signal = Case.case4(
                        TIvale[ti_format[i]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[i]["InputArray"]['ti2']],    # Get ti 2 Value
                        ti_format[i]["InputArray"]['C1'],           # C1
                        ti_format[i]["InputArray"]['C2']            # C2
                    )
                elif case == "5":
                    signal = Case.case5(
                        TIvale[ti_format[i]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[i]["InputArray"]['ti2']],    # Get ti 2 Value
                        TIvale[ti_format[i]["InputArray"]['ti3']],    # Get ti 3 Value
                        ti_format[i]["InputArray"]['C1']            # C1
                    )
                elif case == "6":
                    signal = Case.case6(
                        TIvale[ti_format[i]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[i]["InputArray"]['ti2']],    # Get ti 2 Value
                        TIvale[ti_format[i]["InputArray"]['ti3']],    # Get ti 3 Value
                        TIvale[ti_format[i]["InputArray"]['ti4']]     # Get ti 4 Value
                    )
                elif case == "AROON":
                    signal = Case.caseAROON(
                        TIvale[ti_format[i]["InputArray"]['ti1']],    # Get ti 1 Value
                        TIvale[ti_format[i]["InputArray"]['ti2']],    # Get ti 2 Value
                        TIvale[ti_format[i]["InputArray"]['ti3']],    # Get ti 3 Value
                        ti_format[i]["InputArray"]['C1'],           # C1
                        ti_format[i]["InputArray"]['C2'],           # C2
                        ti_format[i]["InputArray"]['C3']            # C3
                    )
            signal = pd.DataFrame(signal)
            signal.columns = [i] # name col
            data = pd.concat([data, signal], axis=1)
            data.to_json(f"{self.savepath}/Signal.json", orient='records')
        os.remove(f"{self.savepath}/History.json")





