
import sys
import numpy as np
import pandas as pd 
import json 
import math



class Chromosome():
    def __init__(self, kGroup=6, WeightPart=21, mTS = 21, Capital = 10000) -> None:
        self.kGroup:int = kGroup                                            #分幾群
        self.WeightPart:int = WeightPart                                    #要幾個 1
        self.mTS:int = mTS                                                  #有幾個 TS (根據Ranking策略)

        self.Capital:float = Capital
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

    def Fitness(self) -> float:
        with open(f"../data pre-processing/stock/0050.TW/2012-08-30~2013-12-30/Top777.json") as f:
            data = pd.DataFrame(json.load(f))


        ALLtsp = self.__ADVcombine()
        TSPlen = len(ALLtsp)
    
        def PR() -> float:
            ReturnTSP = []
            def returnTSP():
                Allwight = self.getWeight()
                for TSP in ALLtsp:
                    for TS in range(len(TSP)):
                        ReturnTSP.append(data['ARR'][TSP[TS]-1] * Allwight[TS+1] * self.Capital)
            returnTSP()
            return sum(ReturnTSP)/TSPlen

        # ======================= PR =======================

        def RISK() -> float:
            RiskTSP = []
            def riskTSP():
                for TSP in ALLtsp:
                    minRiskTsp = sys.maxsize
                    for TS in range(len(TSP)):
                        minRiskTsp = min(minRiskTsp, data['MDD'][TSP[TS]-1])
                    RiskTSP.append(minRiskTsp)
            riskTSP()
            return sum(RiskTSP)/TSPlen

        # ====================== RISK =======================

        def GB() -> float:
            sum = 0
            for TSG in self.getGTSP():
                tmp = len(TSG)/self.mTS
                sum += -tmp*math.log(tmp, 10)
            return sum

        # ======================= GB =======================

        def WB() -> float:
            sum = 0
            for C in self.getWeight():
                if C == 0:
                    continue
                sum += -C*math.log(C, 10)
            return sum

        self.fitness = PR()*RISK()*GB()*WB()









