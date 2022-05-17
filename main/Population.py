
import copy

import numpy as np
import pandas as pd 

from Chromosome import Chromosome





class Population():
    def __init__(self, pSize=10, CrossoverRate=0.80, MutationRate=0.3, InversionRate=0.60, Generation=10, kGroup=5, mTS=15, WeightPart=10, Capital=100000) -> None:
        self.pSize:int = pSize
        self.Size:int = pSize
        self.Chrom:list[Chromosome] = []
        self.CrossoverRate:float = CrossoverRate
        self.MutationRate:float = MutationRate
        self.InversionRate:float = InversionRate
        self.Generation:int = Generation

        self.mTS:int = mTS
        self.kGroup:int = kGroup
        self.WeightPart:int = WeightPart
        self.Capital:float = Capital

        self.GroupingPart_len:int = mTS + kGroup 
        self.WeightPart_len:int = WeightPart + kGroup + 1


        self.Initiate()
        
    def Initiate(self) -> list:
 
        self.Chrom = [Chromosome(kGroup=self.kGroup, WeightPart=self.WeightPart, mTS=self.mTS, Capital=self.Capital) for _ in range(self.pSize)]
        return self.Chrom

    def Selection(self):
        FitList = np.sort([chrom.fitness for chrom in self.Chrom])
        print(FitList)
        
        for chrom in self.Chrom:
            if chrom.fitness in FitList[self.pSize:]: # 只保留 前 self.pSize 個 染色體
                del chrom 
        
        return self.Chrom

   

    def mutation(self):
        # 隨機選 2 群 A, B  從 A 中 隨機抽一個 TS 移到 B
        # 隨機選 1 個 1 & 1 個 0 交換
        numbers:int = int(self.pSize * self.MutationRate)
        if numbers < 1:
            return

        Variants:list[Chromosome] = copy.deepcopy(np.random.choice(self.Chrom, numbers, replace=False)) 
        # DEEPCOPY 很重要代表 "完整" 複製一份 

        for VarChrom in Variants:
            #============== 處理 Grouping Part ==============
            # print(f"Origin Chromosome: {VarChrom.gene} >> {VarChrom.fitness}")
            selected_group = np.random.choice([x for x in range(self.kGroup)], 2, replace=False)        
            #選出 2 個 group   第一個: 是從該group 選出一個 TS, 第二個: insert 該 group

            GTSP = VarChrom.getGTSP()
            pickTS = np.random.choice(GTSP[selected_group[0]])
            #選出 1個 TS

            # print(f"Origin Gruop: {VarChrom.gene[:self.GroupingPart_len]}")
            GTSP[selected_group[1]] = np.insert(GTSP[selected_group[1]], 0, pickTS)
            #Insert into selected Group
            # print(f"Inserted GTSP: {GTSP} > Pick TS: {pickTS}") 

            if len(GTSP[selected_group[0]]) == 1:
                # print(" ====== Happend =====")
                lenList = [len(x) for x in GTSP]
                selected_group[1] = np.argmax(lenList)
                #choice max_len group which means them have most number of elements  
                # print(f">>> Group len :{lenList}, \tMax Len Index:{selected_group[1]} ==> Selected Group: {GTSP[selected_group[1]]}")
                GTSP[selected_group[0]] = GTSP[selected_group[1]][: lenList[selected_group[1]]//2]
                #and divide group by 2
                GTSP[selected_group[1]] = np.delete(GTSP[selected_group[1]], [x for x in range(lenList[selected_group[1]]//2)])
                # print(f">>> new GTSP: {GTSP}")
                # print(f" ====================")
            else:
                GTSP[selected_group[0]] = np.delete(GTSP[selected_group[0]], np.where(GTSP[selected_group[0]] == pickTS))
                # print(f"Deleted  GTSP: {GTSP}")   

            VarChrom.gene[:self.GroupingPart_len] = np.concatenate([(list(TSP) + [0]) for TSP in GTSP])
            # print(f"  New  Gruop: {VarChrom.gene[:self.GroupingPart_len]}")
 
            #============== 處理 Weigth Part ==============
            # print(f"Origin Weigth >> {VarChrom.gene[-self.WeightPart_len:]}")
            Ones_index = []
            Zores_index = []
            for i in range(len(VarChrom.gene[-self.WeightPart_len:-1])):
                if VarChrom.gene[-self.WeightPart_len:][i] == 0:
                    Zores_index.append(i)
                else:
                    Ones_index.append(i)

            Pick0 = np.random.choice(Zores_index, 1)
            Pick1 = np.random.choice(Ones_index, 1)

            VarChrom.gene[-self.WeightPart_len:-1][Pick1], VarChrom.gene[-self.WeightPart_len:-1][Pick0] = VarChrom.gene[-self.WeightPart_len:-1][Pick0], VarChrom.gene[-self.WeightPart_len:-1][Pick1].copy()
            # print(f"  New  Weigth >> {VarChrom.gene[-self.WeightPart_len:]}")

            self.Size += 1
            VarChrom.Fitness() # 不急 ?
            # print(f"  New   Chromosome: {VarChrom.gene} >> {VarChrom.fitness}")

            self.Chrom.append(VarChrom)
            # print(f"===================================== \t\n")




if __name__ == "__main__":
    np.set_printoptions(linewidth=200)

    p = Population(pSize=10)

    # for c in p.chrom:
    #     print(f"{c.gene} >> {c.fitness}")

    # p.Crossover()    
    p.mutation()