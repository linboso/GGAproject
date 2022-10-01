
import numpy as np
import pandas as pd 
# import sys



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

        TempGene = np.concatenate([np.arange(1, self.mTS+1, dtype=int), 
                                    np.zeros(self.kGroup*2 +1, dtype=int),     
                                    np.ones(self.WeightPart, dtype=int) ]) 
        #GroupingPart&WeightPart 的最尾端都要補 0 方便後續計算

        # 前半部為 mTS個 策略用 1 ~ mTS 表示 mTS個數, 區隔 k 群需要 k-1 個 0,尾補一個 0 => mTS + k -1 + 1 = mTS + k
        # 後半部為 C(0) + C(1) ~ C(k) 共分成 1 + k 個C  需要 1+k-1 個 0  尾補一個 0    => WeightPart + k + 1
        TempGene[-1], TempGene[-self.WeightPart-1] = TempGene[-self.WeightPart-1], TempGene[-1] 
        #把其中一個 0 換到 最最後面
         
        Groupinglen = self.mTS + self.kGroup -1 # 不包含最後一個 0

        Flag = True
        while Flag:
            np.random.shuffle(TempGene[:Groupinglen])
            if TempGene[0] == 0 or TempGene[Groupinglen-1] == 0:
                continue
            #如果GroupingPart 的頭||尾是 0 直接重來
        
            for i in range(1, Groupinglen - 2): # 去 Head & tail
                if TempGene[i] == TempGene[i+1]:
                    Flag = True
                    break
                else:
                    Flag = False
        # shuffle GroupingPart

        np.random.shuffle(TempGene[Groupinglen+1:-1])
        # shuffle WeigthPart

        self.gene = TempGene


    def getGTSP(self):
        GTSP = []
        gene = self.gene[:self.mTS + self.kGroup]
        r = 0
        for s in np.where(gene == 0)[0]:
            GTSP.append(gene[r:s].tolist())
            r = s + 1
        return GTSP

        
    def getWeight(self):
        return (np.diff(np.where(self.gene[self.mTS + self.kGroup -1:] == 0)[0]) - 1) / self.WeightPart

    # def getWeight(self): #比較沒效率
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
        GTSP:list = self.getGTSP()

        Arr = self.Data['ARR'].to_numpy()
        Mdd = self.Data['MDD'].to_numpy()
        GTSP = [[(Arr[i-1], Mdd[i-1]) for i in TSG] for TSG in GTSP]

        res:list[tuple] = []
        n:int = self.kGroup

        #TSP 為 每一個不同的 TSG 中 各取一個 TS 組合成的 
        def backtrack(TSP, start):
            if len(TSP) == n:
                return res.append(TSP.copy())

            for Kth_Group in range(start, n):
                for TS in GTSP[Kth_Group]:
                    TSP.append(TS)
                    backtrack(TSP,  Kth_Group + 1)
                    TSP.pop()
        
        backtrack([], 0)
        return res

    def Fitness(self) -> float:
        import math
        ALLtsp = self.__ADVcombine()
        TSPlen:int = len(ALLtsp)

        def PR() -> float:    
            Weight:list = self.getWeight()
            # ARR = self.Data['ARR'] # 使用區域變數 可加速 python 速度
            ReturnTSP:list = []

            # [[ReturnTSP.append(ARR[TSP[TS]-1] * Weight[TS+1]) for TS in range(self.kGroup)] for TSP in ALLtsp]
            # 版本 2 

            [[ReturnTSP.append(TSP[i][0] * Weight[i+1]) for i in range(self.kGroup)] for TSP in ALLtsp]

            
            # 版本 1 很慢
            # for TSP in ALLtsp:  
                # for TS in range(self.kGroup):
                #     ReturnTSP.append(self.Data['ARR'][TSP[TS]-1] * Allweight[TS+1])


         
            return sum(ReturnTSP)*self.Capital/TSPlen

        # # ======================= PR =======================

        def RISK() -> float:
            RiskTSP:list = []
            # MDD = self.Data['MDD']
            # [[RiskTSP.append(min([MDD[TS-1] for TS in TSP]))] for TSP in ALLtsp]

            [[RiskTSP.append(min([TS[1]for TS in TSP]))] for TSP in ALLtsp]
            
            # print(f"RiskTSP: {RiskTSP}")
            # for TSP in ALLtsp:
            #     minRiskTsp = sys.maxsize
            #     for TS in TSP:
            #         minRiskTsp = min(minRiskTsp, self.Data['MDD'][TS-1])
            #     RiskTSP.append(minRiskTsp)
            # 功能一樣 但是這樣寫慢很多很多

            #     RiskTSP.append(min([self.Data['MDD'][TS-1] for TS in TSP]))
            # 功能一樣 但是這樣寫還是偏慢
           
            return sum(RiskTSP)/TSPlen
        
        # ====================== RISK =======================

        def GB() -> float:
            # S:float = 0
            # for TSG in self.getGTSP():
            #     tmp = len(TSG)/self.mTS
            #     S += -tmp*math.log(tmp, 10)
            # return S
            return -sum([(tmp := len(TSG)/self.mTS) * math.log10(tmp) for TSG in self.getGTSP() ])

        # ======================= GB =======================

        def WB() -> float:
            # S:float = 0
            # for C in self.getWeight():
            #     if C == 0:
            #         continue
            #     S += -C*math.log10(C)
            #     # 此 C = |ci| / T 
            #     # getWeight() 都算好了
            # return S

            return -sum([C*math.log10(C) for C in self.getWeight() if C != 0])
            

        self.fitness = PR()*RISK()*GB()*WB()

        return self.fitness

        



if __name__ == "__main__":
    import cProfile

    with open(f"../../data/stock/2603.TW/TraningData/Top555.json") as f:
        StrategyData = pd.read_json(f)

    c = Chromosome(4, 100, 15, 100000, StrategyData)

    # cProfile.run('c.Fitness()')
    c.Fitness()
    # print(f"Fitness Value: {c.fitness}")




