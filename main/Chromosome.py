import numpy as np
import json 
import pandas as pd 
# dask? for future

class Population():
    def __init__(self, pSize=3, CrossoverRate=0.03, MutationRate=0.03, InversionRate=0.05) -> None:
        self.pSize = pSize
        self.population = []
        self.CrossoverRate = CrossoverRate
        self.MutationRate = MutationRate
        self.InversionRate = InversionRate
        
    def Initiate(self):

        for i in range(self.pSize):
            self.population.append(Chromosome())

            chrom = self.population[i].getChrom()
            print(chrom)
            print(f"GTSP   > {chrom[:12]} \t {self.population[i].getGTSP()}")
            print(f"Weight > {chrom[12:]} \t {self.population[i].getWeight()}")
            
            print()

        # self.Fitness()

        return self.population

    def Fitness(self):
        with open(f"../data pre-processing/stock/0050.TW/2012-08-30~2013-12-30/Top555.json") as f:
            data = pd.DataFrame(json.load(f))

        print(data)

        




class Chromosome():
    def __init__(self, kGroup=3, WeightPart=10, mTS = 9) -> None:
        self.kGroup = kGroup                                            #分幾群
        self.WeightPart = WeightPart                                    #要幾個 1
        self.mTS = mTS                                                  #有幾個 TS (根據Ranking策略)
        self.length = self.mTS + self.kGroup * 2 + self.WeightPart + 1  #全長是多少
        self.chromosome:np.array
        self.Initiate()

    def Initiate(self):

        self.chromosome = np.concatenate([np.arange(1, self.mTS+1, dtype=int), 
                                            np.zeros(self.kGroup*2, dtype=int),     #grouping 尾端補 0 
                                            np.ones(self.WeightPart, dtype=int),
                                            [0]                                     #Weight最尾端 補 0 方便後續計算 
                                        ]) 

        Groupinglen = self.mTS + self.kGroup -1 #不包含最後一個 0

        Flag = True
        while Flag:
            np.random.shuffle(self.chromosome[:Groupinglen])
            if self.chromosome[0] == 0 or self.chromosome[Groupinglen-1] == 0:
                continue
        
            for i in range(1, Groupinglen - 2): # 去 Head & tail
                if self.chromosome[i] == self.chromosome[i+1]:
                    Flag = True
                    break
                else:
                    Flag = False

        # shuffle 前半
            # print(self.chromosome[:Groupinglen])

        np.random.shuffle(self.chromosome[Groupinglen+1:-1])
        # shuffle 後半
        # Grouping part 有一個 尾0 所以要算回來 +1   Weight part 最後一個 0 不要動 所以扣掉 -1

        # 前半部為 mTS個 策略用 1 ~ mTS 表示 一樣用 0 區隔  k 群 需要 k-1 個 0     尾 0 + 1 => mTS + k -1 + 1 = mTS + k
        # 後半部為 C(0) + C(1) ~ C(k) 共 1 + k 個 C  需要 1+k-1 個 0             尾 0 + 1 => WeightPart + k + 1
        return self.chromosome

    def getChrom(self):
        return self.chromosome

    def getGTSP(self):
        GTSP = []
        tmp = []
        for i in self.chromosome[:self.mTS + self.kGroup]:
            if i == 0:
                GTSP.append(tmp)
                tmp = []
            else:
                tmp.append(i)

        return GTSP

    def getWeight(self):
        Weight = []
        count = 0
        total_ones = self.WeightPart
        # print(f"{self.chromosome[self.mTS + self.kGroup:]}")
        for i in self.chromosome[self.mTS + self.kGroup:]:
            if i == 0:
                # print(f"--> {count}")
                Weight.append(count/total_ones)
                count = 0
            else:
                count += 1

        return Weight

    





    




if __name__ == "__main__":
    
    p = Population().Initiate()
    






