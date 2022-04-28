import numpy as np
# dask? for future

class Population():
    def __init__(self, pSize=50 , CrossoverRate=0.03, MutationRate=0.03, InversionRate=0.05) -> None:
        self.pSize = pSize
        self.population = []
        self.CrossoverRate = CrossoverRate
        self.MutationRate = MutationRate
        self.InversionRate = InversionRate
        
    def initiate(self):

        for i in range(self.pSize):
            self.population.append(Chromosome())
            self.population[i].initiate()
            print(self.population[i].getChrom())
            print(f"{self.population[i].getTS()} < == > {self.population[i].getWeight()}")
            print()



class Chromosome():
    def __init__(self, kGroup=3, WeightPart=15, mTS = 9) -> None:
        self.kGroup = kGroup
        self.WeightPart = WeightPart
        self.mTS = mTS

        # self.GroupingLength = kGroup * 2
        # self.WeightLength = WeightPart + kGroup
        self.length = self.mTS + self.kGroup * 2 + self.WeightPart - 1
        # self.chromosomes:np.array = np.ones(weightPart, dtype=int)


    def initiate(self):

        self.chromosome:np.array = np.concatenate([np.arange(1, self.mTS+1, dtype=int), 
                                                    np.zeros(self.kGroup*2 -1, dtype=int), 
                                                    np.ones(self.WeightPart, dtype=int) ]) 

        # print(self.chromosome)

        Groupinglen = self.mTS + self.kGroup -1

        for i in range(len(self.chromosome[:Groupinglen])):
            if self.chromosome[0] == 0 or self.chromosome[Groupinglen-1] or self.chromosome[i] == self.chromosome[i+1]:
                i -= 1
                np.random.shuffle(self.chromosome[:Groupinglen])
            # shuffle 前半

        np.random.shuffle(self.chromosome[Groupinglen:])
        # shuffle 後半
        

        # 前半部為 mTS個 策略用 1 ~ mTS 表示 一樣用 0 區隔  後面產生 TotalLength 個 0       
        # 因為有 k group 所以需要 k 個 0 做區分 前面&後面 共 2k 個零
    
    def getChrom(self):
        return self.chromosome

    def getTS(self):
        return self.chromosome[:self.mTS + self.kGroup-1]

    def getWeight(self):
        return self.chromosome[self.mTS + self.kGroup-1:]






    




if __name__ == "__main__":
    
    p = Population().initiate()






