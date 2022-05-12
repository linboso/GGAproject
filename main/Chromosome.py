
from email.headerregistry import Group
from secrets import choice
import time 
import sys
import numpy as np
import pandas as pd 
import json 
import math

# dask? for future

class Population():
    def __init__(self, pSize=10, CrossoverRate=0.80, MutationRate=0.3, InversionRate=0.60, Generation=10, kGroup=5, mTS=15, WeightPart=100, Capital=100000) -> None:
        self.pSize:int = pSize
        self.chrom:list[Chromosome] = []
        self.CrossoverRate:float = CrossoverRate
        self.MutationRate:float = MutationRate
        self.InversionRate:float = InversionRate
        self.Generation:int = Generation

        self.mTS = mTS
        self.kGroup = kGroup
        self.WeightPart = WeightPart
        self.Capital = Capital

        self.GroupingPart_len = mTS + kGroup 
        self.WeightPart_len = WeightPart + kGroup + 1


        self.Initiate()
        
    def Initiate(self) -> list:
 
        self.chrom = [Chromosome(kGroup=self.kGroup, WeightPart=self.WeightPart, mTS=self.mTS, Capital=self.Capital) for _ in range(self.pSize)]
        return self.chrom

    def Selection(self):
        FitList = np.sort([chrom.fitness for chrom in self.chrom])
        print(FitList)
        
        for chrom in self.chrom:
            if chrom.fitness in FitList[self.pSize:]: # 只保留 前 self.pSize 個 染色體
                del chrom 
        
        return self.chrom

    def Crossover(self):
        numbers:int = int(self.pSize * self.CrossoverRate)
        parents:list[Chromosome] = np.random.choice(self.chrom, numbers, replace=False)
        #選出 父母   父母數量為 Psize * Crossover Rate
        # g = [x for x in range(self.pSize)]
        area = np.random.choice([x + self.chrom[0].kGroup + self.chrom[0].mTS - 1 for x in range(self.chrom[0].kGroup + self.chrom[0].WeightPart)], 2, replace=False)
        if area[0] > area[1]:
            area[0], area[1] = area[1], area[0] 
        # 位置 不重複取 x + Bais 直接避開 前面 TS 部分
        # 數字小 放前面
        print(f"============== {area} ===============")

        def Vaild(geneA, geneB):
            unique, count = np.unique(geneA, return_counts= True)
            A = dict(zip(unique, count))
            unique, count = np.unique(geneB, return_counts= True)
            B = dict(zip(unique, count))
            print(f"{A}, {B}")


        for i in range(0, numbers, 2):
            Vaild(parents[i].gene[area[0]:area[1]].copy(), parents[i+1].gene[area[0]:area[1]].copy())
            # parents[i].gene[area[0] : area[1]], parents[i+1].gene[area[0] : area[1]] = parents[i+1].gene[area[0] : area[1]], parents[i].gene[area[0] : area[1]].copy()
            # 由於 python 特性 傳value 跟 傳address 是由compiler 決定
            # 在此需要用 copy() 先複製一份

            print('======================================\r\n')

            #驗證 組合規則 是否合法..........

    def mutation(self):
        # 隨機選 2 群 A, B  從 A 中 隨機抽一個 TS 移到 B
        # 隨機選 1 個 1 & 1 個 0 交換
        numbers:int = int(self.pSize * self.MutationRate)
        variants:list[Chromosome] = np.random.choice(self.chrom, numbers, replace=False)

        Groups = [x for x in range(self.kGroup)]
        print(Groups)
        for chrom in variants:
            selection = np.random.choice(Groups, 2, replace=False)          # OK
            pickedTS = np.random.choice(chrom.getGTSP()[selection[0]])      # OK
            
            # print(f"{chrom.getGTSP()} >>> {selection} >> {chrom.getGTSP()[selection[0]]}, {pickedTS}")


        
        





class Chromosome():
    def __init__(self, kGroup=6, WeightPart=21, mTS = 21, Capital = 10000) -> None:
        self.kGroup = kGroup                                            #分幾群
        self.WeightPart = WeightPart                                    #要幾個 1
        self.mTS = mTS                                                  #有幾個 TS (根據Ranking策略)
        # self.length = self.mTS + self.kGroup * 2 + self.WeightPart + 1  #全長是多少
        self.Capital = Capital
        self.gene:np.array
        self.fitness:float = 0
        self.Initiate()
        self.Fitness()

    def Initiate(self):

        self.gene = np.concatenate([np.arange(1, self.mTS+1, dtype=int), 
                                    np.zeros(self.kGroup*2, dtype=int),     #grouping 尾端補 0 
                                    np.ones(self.WeightPart, dtype=int),
                                    [0]                                     #Weight最尾端 補 0 方便後續計算 
                                ]) 

        Groupinglen = self.mTS + self.kGroup -1 #不包含最後一個 0

        Flag = True
        while Flag:
            np.random.shuffle(self.gene[:Groupinglen])
            if self.gene[0] == 0 or self.gene[Groupinglen-1] == 0:
                continue
        
            for i in range(1, Groupinglen - 2): # 去 Head & tail
                if self.gene[i] == self.gene[i+1]:
                    Flag = True
                    break
                else:
                    Flag = False

        # shuffle 前半

        np.random.shuffle(self.gene[Groupinglen+1:-1])
        # shuffle 後半
        # Grouping part 有一個 尾0 所以要算回來 +1   Weight part 最後一個 0 不要動 所以扣掉 -1

        # 前半部為 mTS個 策略用 1 ~ mTS 表示 一樣用 0 區隔  k 群 需要 k-1 個 0     尾 0 + 1 => mTS + k -1 + 1 = mTS + k
        # 後半部為 C(0) + C(1) ~ C(k) 共 1 + k 個 C  需要 1+k-1 個 0             尾 0 + 1 => WeightPart + k + 1
        return self.gene


    def getGTSP(self):
        GTSP = []
        tmp = []
        for i in self.gene[:self.mTS + self.kGroup]:
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
        for i in self.gene[self.mTS + self.kGroup:]:
            if i == 0:
                # print(f"--> {count}")
                Weight.append(count/total_ones)
                count = 0
            else:
                count += 1

        return Weight

    def __ADVcombine(self) -> list:
        GTSP = self.getGTSP()
        n = len(GTSP)
        res = []
        #TSP 為 每一個不同的 TSG 中 各取一個 TS 組合成的 
        def backtrack(TSP, start):
            if len(TSP) == self.kGroup:
                return res.append(TSP[:])

            for Kth_Group in range(start, n):
                for TS in range(len(GTSP[Kth_Group])):
                    # 每一個 TSG 的 長度都不一樣
                    TSP.append(GTSP[Kth_Group][TS])
                    backtrack(TSP,  Kth_Group + 1)
                    TSP.pop()
        
        backtrack([], 0)
        return res

    def Fitness(self):
        with open(f"../data pre-processing/stock/0050.TW/2012-08-30~2013-12-30/Top777.json") as f:
            data = pd.DataFrame(json.load(f))


        ALLtsp = self.__ADVcombine()
        TSPlen = len(ALLtsp)
    
        def PR() -> float:
            ReturnTSP = []
            def returnTSP():
                Allwight = self.getWeight()
                for TSP in ALLtsp:
                    # print(f" === {TSP} === ")
                    for TS in range(len(TSP)):
                        # print(f"{data['ARR'][TSP[TS]-1]} <> {Allwight[TS+1]} <> {self.Capital}")
                        ReturnTSP.append(data['ARR'][TSP[TS]-1] * Allwight[TS+1] * self.Capital)
                    # print()
            returnTSP()
            return sum(ReturnTSP)/TSPlen

        # ======================= PR =======================

        def RISK() -> float:
            RiskTSP = []
            def riskTSP():
                for TSP in ALLtsp:
                    minRiskTsp = sys.maxsize
                    for TS in range(len(TSP)):
                        # print(f"{data['ARR'][TSP[TS]-1]} <> {Allwight[TS+1]} <> {self.Capital}")
                        minRiskTsp = min(minRiskTsp, data['MDD'][TSP[TS]-1])
                    RiskTSP.append(minRiskTsp)
            riskTSP()
            return sum(RiskTSP)/TSPlen

        # ====================== RISK =======================

        def GB():
            sum = 0
            for TSG in self.getGTSP():
                tmp = len(TSG)/self.mTS
                sum += -tmp*math.log(tmp, 10)
            return sum

        # ======================= GB =======================

        def WB():
            sum = 0
            for C in self.getWeight():
                if C == 0:
                    continue
                sum += -C*math.log(C, 10)
            return sum
            
        # print(f"{PR()} <> {RISK()} <> {GB()} <> {WB()}")
        self.fitness = PR()*RISK()*GB()*WB()




if __name__ == "__main__":
    np.set_printoptions(linewidth=200)

    p = Population(pSize=10)

    # for c in p.chrom:
    #     print(f"{c.gene} >> {c.fitness}")

    # p.Crossover()    
    p.mutation()
    





