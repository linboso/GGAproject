
import copy

import numpy as np

from Chromosome import Chromosome




class Population():
    def __init__(self, pSize=10, CrossoverRate=0.80, MutationRate=0.3, InversionRate=0.30, Generation=10, kGroup=5, mTS=15, WeightPart=10, Capital=100000) -> None:
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

    def Genealogy(self):
        for i in range(self.Size):
            print(f"{i+1:3d}-th: {self.Chrom[i].fitness:10.4f} >> {self.Chrom[i].gene}")

    def Initiate(self) -> list:
 
        self.Chrom = [Chromosome(kGroup=self.kGroup, WeightPart=self.WeightPart, mTS=self.mTS, Capital=self.Capital) for _ in range(self.pSize)]
        return self.Chrom

    def Selection(self): ## need fix
        FitList = np.sort([chrom.fitness for chrom in self.Chrom])
        
        for chrom in self.Chrom:
            if chrom.fitness in FitList[self.pSize:]: # 只保留 前 self.pSize 個 染色體
                del chrom 

        self.Size = self.pSize
  


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
            print(f"Origin Chromosome: {VarChrom.gene} >> {VarChrom.fitness}")
            selected_group = np.random.choice([x for x in range(self.kGroup)], 2, replace=False)        
            #選出 2 個 group   第一個: 是從該group 選出一個 TS, 第二個: insert 該 group

            GTSP = VarChrom.getGTSP()
            pickTS = np.random.choice(GTSP[selected_group[0]])
            #選出 1個 TS

            print(f"Origin Gruop: {VarChrom.gene[:self.GroupingPart_len]}")
            GTSP[selected_group[1]] = np.insert(GTSP[selected_group[1]], 0, pickTS)
            #Insert into selected Group
            print(f"Inserted GTSP: {GTSP} > Pick TS: {pickTS}") 

            if len(GTSP[selected_group[0]]) == 1:
                print(" ====== Happend =====")
                lenList = [len(x) for x in GTSP]
                selected_group[1] = np.argmax(lenList)
                #choice max_len group which means them have most number of elements  
                print(f">>> Group len :{lenList}, \tMax Len Index:{selected_group[1]} ==> Selected Group: {GTSP[selected_group[1]]}")
                GTSP[selected_group[0]] = GTSP[selected_group[1]][: lenList[selected_group[1]]//2]
                #and divide group by 2
                GTSP[selected_group[1]] = np.delete(GTSP[selected_group[1]], [x for x in range(lenList[selected_group[1]]//2)])
                print(f">>> new GTSP: {GTSP}")
                print(f" ====================")
            else:
                GTSP[selected_group[0]] = np.delete(GTSP[selected_group[0]], np.where(GTSP[selected_group[0]] == pickTS))
                print(f"Deleted  GTSP: {GTSP}")   

            VarChrom.gene[:self.GroupingPart_len] = np.concatenate([(list(TSP) + [0]) for TSP in GTSP])
            print(f"  New  Gruop: {VarChrom.gene[:self.GroupingPart_len]}")
 
            #============== 處理 Weigth Part ==============
            # print(f"Origin Weigth >> {VarChrom.gene[-self.WeightPart_len:]}")
            Ones_index = []
            Zeros_index = []
            for i in range(len(VarChrom.gene[-self.WeightPart_len:-1])):
                if VarChrom.gene[-self.WeightPart_len:][i] == 0:
                    Zeros_index.append(i)
                else:
                    Ones_index.append(i)

            Pick0 = np.random.choice(Zeros_index, 1)
            Pick1 = np.random.choice(Ones_index, 1)

            VarChrom.gene[-self.WeightPart_len:-1][Pick1], VarChrom.gene[-self.WeightPart_len:-1][Pick0] = VarChrom.gene[-self.WeightPart_len:-1][Pick0], VarChrom.gene[-self.WeightPart_len:-1][Pick1].copy()
            # print(f"  New  Weigth >> {VarChrom.gene[-self.WeightPart_len:]}")

            self.Size += 1

            # print(f"  New   Chromosome: {VarChrom.gene} >> {VarChrom.fitness}")
            VarChrom.Fitness()
            self.Chrom.append(VarChrom)
            print(f"===================================== \t\n")


    def inversion(self):
        numbers:int = int(self.pSize*self.InversionRate)
        Variants:list[Chromosome] = copy.deepcopy(np.random.choice(self.Chrom, numbers, replace=False))

        for VarChrom in Variants:
            invertgroup = np.random.choice([x for x in range(self.kGroup)], 2, replace=False)
            GTSP = VarChrom.getGTSP()
            GTSP[invertgroup[0]] , GTSP[invertgroup[1]] = GTSP[invertgroup[1]] , GTSP[invertgroup[0]]
            VarChrom.gene[:self.GroupingPart_len] = np.concatenate([(list(NewGroup) + [0]) for NewGroup in GTSP])

            self.Size += 1
            VarChrom.Fitness()
            self.Chrom.append(VarChrom)

            
    def Crossover(self):
        numbers:int = int(self.pSize * self.CrossoverRate)

        # tmp = list(np.random.choice([x for x in range(self.pSize)], numbers, replace= False))
        Parents:list[Chromosome] = copy.deepcopy(np.random.choice(self.Chrom, numbers, replace=False))
        Offsprings:list[Chromosome] = copy.deepcopy(Parents[:numbers//2])

        IndexList = [x for x in range(self.kGroup)]

        #=======================================weight part=========================================
        round = 0
        for Father, Mother in zip(Parents[:numbers//2], Parents[numbers//2:]):
            # print(f"======================{round}-th=========================")
    
            CutOffPoint = np.random.choice([x for x in range(self.WeightPart_len)], 2, replace = False)
            if(CutOffPoint[1] < CutOffPoint[0]):
                CutOffPoint[0], CutOffPoint[1] = CutOffPoint[1], CutOffPoint[0]
         
            while CutOffPoint[0] != CutOffPoint[1]:
                Count_Father = 0 #gene 區間1的總數
                Count_Mother = 0
                for k in range(CutOffPoint[0], CutOffPoint[1]): #count 區間內 1 的總數 如果值是 0 本就不妨礙 sum
                    Count_Father += Father.gene[-self.WeightPart_len:][k]
                    Count_Mother += Mother.gene[-self.WeightPart_len:][k]

                if Count_Father == Count_Mother: # 總數相等 => 進行交換
                    tmp =  Father.gene[-self.WeightPart_len:][CutOffPoint[0]:CutOffPoint[1]].copy()
                    Father.gene[-self.WeightPart_len:][CutOffPoint[0]:CutOffPoint[1]] = Mother.gene[-self.WeightPart_len:][CutOffPoint[0]:CutOffPoint[1]]
                    Mother.gene[-self.WeightPart_len:][CutOffPoint[0]:CutOffPoint[1]] = tmp
               
                    self.Chrom.append(Father)
                    self.Chrom.append(Mother)
                    self.Size += 2
                    break
                
                CutOffPoint[1] -= 1

            SelectedGroups = np.random.choice(IndexList, 2, replace = False) #選出 2組 插入
            InsertPoint:int = np.random.choice(IndexList[:self.kGroup-1])                  #從第 x-th group 插入
            
            ParentsGroups = [Father.getGTSP()[x] for x in SelectedGroups]
            # ParentsGroups = np.random.choice(Father.getGTSP(), 2, replace= False)
            OffspringGroups = Mother.getGTSP()
            # print(f"InsertPoint: {InsertPoint}")
            # print(f"Parents   Groups: {ParentsGroups}")
            # print(f"offspring Groups: {OffspringGroups[InsertPoint:InsertPoint+2]}")

            tmpSet1 = set(TS for GTS in ParentsGroups for TS in GTS)
            tmpSet2 = set(TS for GTS in OffspringGroups[InsertPoint:InsertPoint+2] for TS in GTS)
            MissingTS= list(tmpSet2 - tmpSet1) # 缺少的 TS 需補上 
            RepeatTS = list(tmpSet1 - tmpSet2) # 重複的 TS 需移除

            # print(f"MissingTS >> {MissingTS}")
            # print(f"RepeatTS >> {RepeatTS}\r\n")
            # print(f"          OffspringGroups: {OffspringGroups}")

            OffspringGroups[InsertPoint] = ParentsGroups[0] 
            OffspringGroups[InsertPoint + 1] = ParentsGroups[1]

            # print(f"nuprocess OffspringGroups: {OffspringGroups}")
            
            
            MissCount = 0
            for i in range(self.kGroup):
                if i == InsertPoint or i == InsertPoint + 1:
                    continue 
                # 如果 i == 插入&+1 的位置 則跳過
              
                NewGroup = OffspringGroups[i].copy()

                for j in range(len(OffspringGroups[i])):
                    if OffspringGroups[i][j] in RepeatTS:
                        if MissCount != len(MissingTS):
                            RepeatTS.remove(OffspringGroups[i][j])
                            NewGroup[j] = MissingTS[MissCount]
                            MissCount += 1
                        else: # RepeatTS 用完
                            NewGroup.remove(OffspringGroups[i][j])
              
                OffspringGroups[i] = NewGroup
            # print(f" process1 OffspringGroups: {OffspringGroups}")

         
            # print(f"MissingTS >> {MissingTS} >> {MissCount}")
            # print(f"RepeatTS  >> {RepeatTS}\r\n")


            for TS in MissingTS[MissCount:]:
                OffspringGroups[self.kGroup-1].append(TS)
            # 如果 MissingTS 裡面還有東西 則 通通直接 append 到最後一組 裡面
            # print(f" process2 OffspringGroups: {OffspringGroups}")


            lenList = sorted(zip([len(GTS) for GTS in OffspringGroups], IndexList)) 
            # 小 --> 大 排序
            # (Group's Len, Group's Index)
            if lenList[0][0] == 0: 
                OffspringGroups[lenList[0][1]] = OffspringGroups[lenList[self.kGroup -1 ][1]][lenList[self.kGroup -1 ][1]//2:]
                OffspringGroups[lenList[self.kGroup -1 ][1]] = OffspringGroups[lenList[self.kGroup -1 ][1]][:lenList[self.kGroup -1 ][1]//2]

            # print(f" process3 OffspringGroups: {OffspringGroups}")

            Offsprings[round].gene[:self.GroupingPart_len] = np.concatenate([(GTS + [0]) for GTS in OffspringGroups])
            self.Chrom.append(Offsprings[round])
            self.Size += 1
            round += 1





            

            





if __name__ == "__main__":
    import time
    np.set_printoptions(linewidth=200)


    p = Population(pSize=10, InversionRate=1)

    p.Crossover()

    for i in range(p.Size):
        print(f"{i} >> {p.Chrom[i].gene}")

    # p.mutation()



