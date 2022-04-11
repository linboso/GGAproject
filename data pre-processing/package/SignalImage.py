

import matplotlib.pylab as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

import os
import time
import json
import pandas as pd


from SettingFile import SettingFile



class Simage():
    def __init__(self) -> None:
        # self.data = pd.DataFrame()
        setting = SettingFile().Read()
        self.stock_id = setting['StockID']
        self.start = setting['StartDate']
        self.end = setting['EndDate']
        self.savepath = f"stock/{self.stock_id}/{self.start}~{self.end}"
        self.readpath = f"stock/{self.stock_id}/{self.start}~{self.end}"

    def __readSingal(self):
        with open(f"../{self.readpath}/Signal.json") as f:
            data = pd.DataFrame(json.load(f))
        return data

    def SingleImage(self):
        data = self.__readSingal()

        if not os.path.exists(f'../{self.readpath}/Singal2Image'):
            os.mkdir(f'../{self.readpath}/Singal2Image/')

        for i in range(len(data['Date'])):
            time_local = time.localtime(data['Date'][i]/1000)
            data['Date'][i] =  time.strftime("%Y-%m-%d", time_local)

        # print(data['Date'])

        for i in data.columns[1:]:
            plt.figure(figsize = (20, 10))
            plt.plot(data['Date'], data[i], label=i)
            plt.xticks(rotation = 45)
            
            ax = plt.gca()
            ax.xaxis.set_major_locator(mticker.MultipleLocator(15)) 

            plt.title(i)
            plt.legend()
            plt.savefig(f'../{self.readpath}/Singal2Image/{i}.png', dpi = 300)
            plt.clf()






if __name__ == "__main__":
    si = Simage()
    si.SingleImage()