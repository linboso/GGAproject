
import sys
import numpy as np
import pandas as pd 
import math



class Chromosome():
    def __init__(self, kGroup, WeightPart, mTS, Capital, StrategyData) -> None:
        self.kGroup:int = kGroup                                                    #分幾群
        self.WeightPart:int = WeightPart                                            #要幾個 1
        self.mTS:int = mTS                                                          #有幾個 TS (根據Ranking策略)

        self.Data:pd.DataFrame = StrategyData

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
        GTSP, tmp = [], []
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

        for i in self.gene[self.mTS + self.kGroup:]:
            if i == 0:
                Weight.append(count/self.WeightPart)
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
        ALLtsp = self.__ADVcombine()
        TSPlen = len(ALLtsp)
    
        def PR() -> float:    
            Allweight = self.getWeight()
            ReturnTSP = []

            for TSP in ALLtsp:
                [ReturnTSP.append(self.Data['ARR'][TSP[TS]-1] * Allweight[TS+1]) for TS in range(self.kGroup)]
            
                # for TS in range(self.kGroup):
                #     ReturnTSP.append(self.Data['ARR'][TSP[TS]-1] * Allweight[TS+1])
         
            return sum(ReturnTSP)*self.Capital/TSPlen

        # # ======================= PR =======================

        def RISK() -> float:
            RiskTSP = []

            for TSP in ALLtsp:
                # minRiskTsp = sys.maxsize
                # for TS in TSP:
                #     minRiskTsp = min(minRiskTsp, self.Data['MDD'][TS-1])
                # RiskTSP.append(minRiskTsp)
                RiskTSP.append(min([self.Data['MDD'][TS-1] for TS in TSP]))
           
            return sum(RiskTSP)/TSPlen
        
        # ====================== RISK =======================

        def GB() -> float:
            S = []
            for TSG in self.getGTSP():
                tmp = len(TSG)/self.mTS
                S.append(-tmp*math.log(tmp, 10))
            return sum(S)

        # ======================= GB =======================

        def WB() -> float:
            S = 0
            for C in self.getWeight():
                if C == 0:
                    continue
                S += -C*math.log(C, 10)
                # 此 C = |ci| / T 
                # getWeight() 都算好了
            return S

        self.fitness = PR()*RISK()*GB()*WB()
        # del ALLtsp
        



if __name__ == "__main__":
    import cProfile
    #it__(self, kGroup, WeightPart, mTS, Capital, StrategyData) 
    with open(f"../../data/stock/0050.TW/TraningData/Top555.json") as f:
            StrategyData = pd.read_json(f)

    c = Chromosome(3, 100, 15, 100000, StrategyData)
    cProfile.run('c.Fitness()')
    # a = 0.042735868 * 0.36
    # print(a)
    # b = 0.0548327287 * 0.17
    # print(b)
    # c = 0.0757129283 * 0.37
    # print(c)
    # print()
    # print(a+b+c)
    # print(np.average([0, 0.042735868, 0.0548327287, 0.0757129283], weights=[0.1 ,0.36, 0.17,0.37]))






