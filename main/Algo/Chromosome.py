
import numpy as np
import pandas as pd 




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


    # def getGTSP(self):
    #     tmp = np.array_split(self.gene[:self.mTS + self.kGroup -1], np.where(self.gene[:self.mTS + self.kGroup -1] == 0)[0])
    #     return [GTSP[1:] if GTSP[0] == 0 else GTSP[:] for GTSP in tmp]

    # def getGTSP(self):
    #     tmp = np.array_split(self.gene[:self.mTS + self.kGroup -1], np.where(self.gene[:self.mTS + self.kGroup -1] == 0)[0])
    #     return np.unique(tmp)

    def getGTSP(self):
        GTSP = []
        gene = self.gene[:self.mTS + self.kGroup]
        r = 0
        for s in np.where(gene == 0)[0]:
            GTSP.append(gene[r:s].tolist())
            r = s + 1
        return GTSP


    # def getGTSP(self):
    #     GTSP, tmp = [], []
    #     for i in self.gene[:self.mTS + self.kGroup]:
    #         if i == 0:
    #             GTSP.append(tmp)
    #             tmp = []
    #         else:
    #             tmp.append(i)

    #     return GTSP

        

    def getWeight(self):
        return (np.diff(np.where(self.gene[self.mTS + self.kGroup -1:] == 0)[0]) - 1) / self.WeightPart

    # def getWeight(self):
    #     Weight = []
    #     count = 0
        
    #     for i in self.gene[self.mTS + self.kGroup:]:
    #         if i == 0:
    #             Weight.append(count/self.WeightPart)
    #             count = 0 
    #         else:
    #             count += 1

    #     return Weight

    def __ADVcombine(self) -> list:
        GTSP = self.getGTSP()
        n = self.kGroup
      
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
        import math
        ALLtsp:list = self.__ADVcombine()
        TSPlen:int = len(ALLtsp)


        def PR() -> float:    
            Allweight:list = self.getWeight()
            ARR = self.Data['ARR'] # 使用區域變數 可加速 python 速度
            ReturnTSP = []
            [[ReturnTSP.append(ARR[TSP[TS]-1] * Allweight[TS+1]) for TS in range(self.kGroup)] for TSP in ALLtsp]

            # for TSP in ALLtsp:  
            #     [ReturnTSP.append(self.Data['ARR'][TSP[TS]-1] * Allweight[TS+1]) for TS in range(self.kGroup)]
                # for TS in range(self.kGroup):
                #     ReturnTSP.append(self.Data['ARR'][TSP[TS]-1] * Allweight[TS+1])
         
            return sum(ReturnTSP)*self.Capital/TSPlen

        # # ======================= PR =======================

        def RISK() -> float:
            RiskTSP = []
            MDD = self.Data['MDD']
            [[RiskTSP.append(min([MDD[TS-1] for TS in TSP]))] for TSP in ALLtsp]
            # for TSP in ALLtsp:
                # minRiskTsp = sys.maxsize
                # for TS in TSP:
                #     minRiskTsp = min(minRiskTsp, self.Data['MDD'][TS-1])
                # RiskTSP.append(minRiskTsp)
                # RiskTSP.append(min([self.Data['MDD'][TS-1] for TS in TSP]))
           
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

    c = Chromosome(4, 10, 15, 100000, StrategyData)
    
    print(c.getGTSP())

    # cProfile.run('c.Fitness()')


  





