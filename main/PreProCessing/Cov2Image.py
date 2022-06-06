
import matplotlib.pylab as plt
import matplotlib.ticker as mticker

import os
import time
import json
import pandas as pd


class Simage():
    def __init__(self, Setting) -> None:
        # self.data = pd.DataFrame()
        setting = Setting
        self.stock_id = setting['StockID']
        self.start = setting['StartDate']
        self.end = setting['EndDate']
        self.path = setting['Path']


    def __readSingal(self):
        with open(f"{self.path}/Signal.json") as f:
            data = pd.DataFrame(json.load(f))
        return data

    def __Time(self):
        with open(f"{self.path}/Date.json") as f:
            data = pd.DataFrame(json.load(f))
        data = self.__CovTime(data['Date'])
        return data

    def __readStock(self):
        with open(f"{self.path}/StockData.json") as f:
            data = pd.DataFrame(json.load(f))
        return data
        
    def __readTIValue(self):
        with open(f"{self.path}/TIvalue.json") as f:
            data = pd.DataFrame(json.load(f))
        return data


    def __CovTime(self, t:pd.Series):
        for i in range(len(t)):
            time_local = time.localtime(t[i]/1000)
            t[i] =  time.strftime("%Y-%m-%d", time_local)

        return t

        

    def TIValueImage(self):
        data = self.__readTIValue()

        if not os.path.exists(f'{self.path}/Image'):
            os.mkdir(f'{self.path}/Image/')

        date = self.__Time()
        for i in data.columns:
            plt.figure(figsize = (12, 8)) # unit  is inch?
            plt.plot(date, data[i], label=i)
            plt.xticks(rotation = 45)
            plt.grid(axis='y',linestyle=':', color='k')

            ax = plt.gca()
            ax.xaxis.set_major_locator(mticker.MultipleLocator(15)) 

            plt.title(i)
            plt.legend()
            plt.savefig(f'{self.readpath}/Image/{i}_TI.png', dpi = 180)
            plt.clf()


    def SignalImage(self):
        data = self.__readSingal()

        if not os.path.exists(f'{self.path}/Image'):
            os.mkdir(f'{self.path}/Image/')

        data['Date'] = self.__CovTime(data['Date'])
        # print(data['Date'])

        for i in data.columns[1:]:
            plt.figure(figsize = (12, 8)) # unit  is inch?
            plt.plot(data['Date'], data[i], label=i)
            plt.xticks(rotation = 45)
            
            ax = plt.gca()
            ax.xaxis.set_major_locator(mticker.MultipleLocator(15)) 

            plt.title(i)
            plt.legend()
            plt.savefig(f'{self.path}/Image/{i}.png', dpi = 180)
            plt.clf()


    def StockImage(self):
        data = self.__readStock()

        if not os.path.exists(f'{self.path}/Image'):
            os.mkdir(f'{self.path}/Image/')
        
        date = self.__Time()
        
        plt.figure(figsize=(12, 8)) 
        plt.plot(date, data["close"], color='RED', label='Close price')
        plt.plot(date, data['open'], color='GREEN', label='Open price')

        plt.grid(axis='y',linestyle='-.', color='k')
        plt.xticks(rotation = 45)

        ax = plt.gca()
        ax.xaxis.set_major_locator(mticker.MultipleLocator(15))

        plt.title('Stock History')
        plt.legend()
        plt.savefig(f'{self.path}/Image/Stock History.png', dpi = 180)
        plt.clf()







if __name__ == "__main__":
    
    from SettingFile import SettingFile

    si = Simage()
    # si.TIValueImage()
    # si.SignalImage()
    # si.StockImage()
