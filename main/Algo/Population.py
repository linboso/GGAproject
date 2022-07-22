import copy
from tkinter.tix import Select
import pandas as pd
import numpy as np

if __name__ == "__main__":
    from Chromosome import Chromosome
else:
    from .Chromosome import Chromosome


class Population():
    def __init__(self, Setting) -> None:
        self.Setting = Setting
        self.pSize:int = Setting['pSize']
        self.Size:int = Setting['pSize']
        self.Chrom:list[Chromosome] = []
        self.CrossoverRate:float = Setting['CrossoverRate']
        self.MutationRate:float = Setting['MutationRate']
        self.InversionRate:float = Setting['InversionRate']
        self.Generation:int = Setting['Generation']

        self.mTS:int = Setting['mTS']
        self.kGroup:int = Setting['kGroup']
        self.WeightPart:int = Setting['WeightPart']
        self.Capital:float = Setting['Capital']

        self.GroupingPart_len:int = Setting['mTS'] + Setting['kGroup'] 
        self.WeightPart_len:int = Setting['WeightPart'] + Setting['kGroup'] + 1

        if __name__ == "__main__":
            with open(f"../../data/stock/0050.TW/TraningData/Top555.json") as f:
                StrategyData = pd.read_json(f)
        else:
            with open(f"{Setting['Path']}/{Setting['StockID']}/TraningData/{Setting['Strategy']}.json") as f:
                StrategyData = pd.read_json(f)

        self.Chrom:list[Chromosome] = [Chromosome(kGroup=self.kGroup, WeightPart=self.WeightPart, mTS=self.mTS, Capital=self.Capital, StrategyData=StrategyData) for _ in range(self.pSize)]
        

    def Genealogy(self):
        for i in range(self.Size):
            print(f"{i+1:3d}-th | Fitness Value: {self.Chrom[i].fitness:10.4f} >> Gene: {self.Chrom[i].gene}")

    # print all Chromosome

    def GenerateOffspring_With_logFile(self):
        import time
        import os

        if not os.path.exists(f'{self.Setting["Path"]}/{self.Setting["StockID"]}/History/'):
            os.makedirs(f'{self.Setting["Path"]}/{self.Setting["StockID"]}/History')

        STime = time.time()
        for i in range(self.Generation):
            print(f"{i+1:3d}-th Generation")
            s = time.time()
            self.Selection()
            self.Crossover()
            self.Mutation()
            self.Inversion()
            e = time.time()
            print(f"Time: {e-s}\r\n")
            # gc.collect()
            with open(f'{self.Setting["Path"]}/{self.Setting["StockID"]}/History/{i+1}-th.txt', 'w') as f:
                f.writelines(f"Fitness: {chrom.fitness:10f} \t{list(chrom.gene)}\n" for chrom in self.Chrom)
                f.write(f"Time: {e-s:3.5f}")
            

        ETime = time.time()
        print(f"Total Time: {ETime - STime}")

        # Next Step Process Final GTSP
        # and Vail thw GTSP


    def GenerateOffspring(self):
        import time
        s = time.time()
        for _ in range(self.Generation):

            self.Selection()
            self.Crossover()
            self.Mutation()
            self.Inversion()

        e = time.time()
        # gc.collect()
        print(f"Total Time: {e-s}")
        print(f"Finish Iterate\r\n")
    
        #Do BackTesting
            
        
    # END of Selection

    def Selection(self):
        FitList = sorted([(chrom.Fitness(), chrom) for chrom in self.Chrom], reverse=True, key=lambda x:x[0])[:self.pSize]
    
        self.Size = self.pSize
        self.Chrom = [Chrom[1] for Chrom in FitList]
        del FitList


    def Mutation(self):
        # 隨機選 2 群 A, B  從 A 中 隨機抽一個 TS 移到 B
        # 隨機選 1 個 1 & 1 個 0 交換
        numbers:int = round(self.pSize * self.MutationRate)
        Variants:list[Chromosome] = copy.deepcopy(np.random.choice(self.Chrom, numbers, replace=False)) 
        # DEEPCOPY 很重要代表 "完整" 複製一份 

        for VarChrom in Variants:
            selected_group = np.random.choice(self.kGroup, 2, replace=False)        
            #選出 2 個 group   第一個: 是從該group 選出一個 TS, 第二個: insert 該 group

            GTSP = VarChrom.getGTSP()
            pickTS = np.random.choice(GTSP[selected_group[0]])  #選出 1個 TS  **

            GTSP[selected_group[1]].append(pickTS)
            # #插入 被選到的組裡

            if len(GTSP[selected_group[0]]) == 1:
                lenList = [len(TSP) for TSP in GTSP]
                selected_group[1] = np.argmax(lenList)   #選出有最多元素的子集
                GTSP[selected_group[0]] = GTSP[selected_group[1]][: lenList[selected_group[1]]//2]  #把 最多元素的子集 拆分成 2 組
                GTSP[selected_group[1]] = GTSP[selected_group[1]][lenList[selected_group[1]]//2:].copy()

                
            else:
                GTSP[selected_group[0]] = np.delete(GTSP[selected_group[0]], np.where(GTSP[selected_group[0]] == pickTS))
    
            # print(f"GTSP[selected_group[1]]: >> {GTSP[selected_group[1]]}")
            # print(f"GTSP[selected_group[0]]: >> {GTSP[selected_group[0]]}\r\n")
            VarChrom.gene[:self.GroupingPart_len] = np.concatenate([(list(TSP) + [0]) for TSP in GTSP])
            selected_group = np.random.choice(self.kGroup, 2, replace=False)        

            #============== 處理 Weigth Part ==============
            geneTmp = VarChrom.gene[self.GroupingPart_len:-1]
            Pick0 = np.random.choice(np.where(geneTmp == 0)[0])
            Pick1 = np.random.choice(np.where(geneTmp == 1)[0])

            geneTmp[Pick1], geneTmp[Pick0] = geneTmp[Pick0], geneTmp[Pick1]
            VarChrom.gene[self.GroupingPart_len:-1] = geneTmp

            self.Size += 1
            self.Chrom.append(VarChrom)
            ## print(f"===================================== \t\n")
    # END of Mutation


    def Inversion(self):
        numbers:int = round(self.pSize * self.InversionRate)
        Variants:list[Chromosome] = copy.deepcopy(np.random.choice(self.Chrom, numbers, replace=False))

        for VarChrom in Variants:
            invertgroup = np.random.choice(self.kGroup, 2, replace=False)
            GTSP = VarChrom.getGTSP()
            GTSP[invertgroup[0]] , GTSP[invertgroup[1]] = GTSP[invertgroup[1]] , GTSP[invertgroup[0]].copy()

            VarChrom.gene[:self.GroupingPart_len] = np.concatenate([(NewGroup + [0]) for NewGroup in GTSP])
            self.Size += 1

            self.Chrom.append(VarChrom)

        del Variants
        
    # END of Inversion
            
    def Crossover(self):
        numbers:int = int(x-1) if (x:=self.pSize * self.CrossoverRate) % 2 else int(x) 
        #一定要整數

        Parents:list[Chromosome] = copy.deepcopy(np.random.choice(self.Chrom, numbers, replace=False))
        Offsprings:list[Chromosome] = copy.deepcopy(Parents[:numbers//2])

        IndexList = [x for x in range(self.kGroup)]
        round = 0
        for Father, Mother in zip(Parents[:numbers//2], Parents[numbers//2:]):

            #======================================= Weight part =========================================
            CutOffPoint = np.random.choice([x for x in range(self.WeightPart_len)], 2, replace = False)
            if(CutOffPoint[1] < CutOffPoint[0]):
                CutOffPoint[0], CutOffPoint[1] = CutOffPoint[1], CutOffPoint[0]
         
            while CutOffPoint[0] != CutOffPoint[1]:
                Count_Father, Count_Mother = 0, 0 #gene 區間1的總數
                
                for k in range(CutOffPoint[0], CutOffPoint[1]): #count 區間內 1 的總數 如果值是 0 本就不妨礙 sum
                    Count_Father += Father.gene[-self.WeightPart_len:][k]
                    Count_Mother += Mother.gene[-self.WeightPart_len:][k]

                if Count_Father == Count_Mother: # 總數相等 => 進行交換

                    Father.gene[-self.WeightPart_len:][CutOffPoint[0]:CutOffPoint[1]], Mother.gene[-self.WeightPart_len:][CutOffPoint[0]:CutOffPoint[1]] = Mother.gene[-self.WeightPart_len:][CutOffPoint[0]:CutOffPoint[1]], Father.gene[-self.WeightPart_len:][CutOffPoint[0]:CutOffPoint[1]]

                    self.Chrom.append(Father)
                    self.Chrom.append(Mother)
                    self.Size += 2
                    break
                
                CutOffPoint[1] -= 1
            #======================================= Grouping part =========================================
            SelectedGroups = np.random.choice(IndexList, 2, replace = False) #選出 2組 插入
            InsertPoint:int = np.random.choice(IndexList[:self.kGroup-1])    #從第 x-th group 插入
            
            tmp = Father.getGTSP()
            ParentsGroups:list = [tmp[x] for x in SelectedGroups] 
            OffspringGroups:list = Mother.getGTSP()

            tmpSet1:set = set(TS for GTS in ParentsGroups for TS in GTS)
            tmpSet2:set = set(TS for GTS in OffspringGroups[InsertPoint:InsertPoint+2] for TS in GTS)
            ## print(f" ori :{OffspringGroups}")
   

            MissingTS:list = list(tmpSet2 - tmpSet1) # 缺少的 TS 需補上 
            RepeatTS:list = list(tmpSet1 - tmpSet2) # 重複的 TS 需移除

            OffspringGroups[InsertPoint] = ParentsGroups[0] 
            OffspringGroups[InsertPoint + 1] = ParentsGroups[1]
            
            MissCount:int = 0 #計算 有幾個 MissTS 以補回
            # print(f" pr0 :{OffspringGroups} \t Insert")
            # print(f"MissingTS >> {MissingTS}")
            # print(f"RepeatTS  >> {RepeatTS}")

            for i in range(self.kGroup):
                if i == InsertPoint or i == InsertPoint + 1:
                    continue 
                # 如果 i == 插入 & i+1 的位置 則跳過
                
                NewGroup:list = OffspringGroups[i].copy() 

                for j in range(len(OffspringGroups[i])):
                    if OffspringGroups[i][j] in RepeatTS:
                        if MissCount != len(MissingTS):
                            RepeatTS.remove(OffspringGroups[i][j])
                            NewGroup[j] = MissingTS[MissCount]
                            MissCount += 1
                        else: # RepeatTS 用完
                            NewGroup.remove(OffspringGroups[i][j])
              
                OffspringGroups[i] = NewGroup
                #用NewGroup 取代
            ## print(f" pr1 :{OffspringGroups} \t SWAP(MissingTS, RepeatTS)")

            [OffspringGroups[self.kGroup-1].append(TS) for TS in MissingTS[MissCount:]]

            # 如果 MissingTS 裡面還有東西 則 通通直接 append 到最後一組 裡面
            ## print(f" pr2 :{OffspringGroups} \t appned all MissingTS to least Group")


            while (lenList := sorted(zip([len(GTS) for GTS in OffspringGroups], IndexList)))[0][0] == 0:
                OffspringGroups[lenList[0][1]] = OffspringGroups[lenList[self.kGroup -1][1]][lenList[self.kGroup -1][0]//2:]
                OffspringGroups[lenList[self.kGroup -1][1]] = OffspringGroups[lenList[self.kGroup -1][1]][:lenList[self.kGroup -1][0]//2]

            # while (lenList := sorted(zip([len(GTS) for GTS in OffspringGroups], IndexList)))[0][0] == 0:
            #     OffspringGroups[lenList[0][1]] = OffspringGroups[lenList[self.kGroup -1][1]][lenList[self.kGroup -1][0]//2:]
            #     OffspringGroups[lenList[self.kGroup -1][1]] = OffspringGroups[lenList[self.kGroup -1][1]][:lenList[self.kGroup -1][0]//2]

                ## print(f" pr3 {OffspringGroups}")
            ## print(f" end :{OffspringGroups}\r\n")

            # 小 --> 大 排序
            # (Group's Len,  Group's Index)  ==> (長度, index)
            # 如果有 空群 => 找出 有最多TS 的群/2 move to 空群 
            # 有很低的機率 空群 > 1 所以 要用 while
            # 最多做 k //2 次

            Offsprings[round].gene[:self.GroupingPart_len] = np.concatenate([(GTS + [0]) for GTS in OffspringGroups])
            self.Chrom.append(Offsprings[round])
            round += 1
            
        self.Size += round
        del Parents
        del Offsprings
    # END of Crossover




            

            


if __name__ == "__main__":
    import cProfile
    import json
    import time
    # from .Chromosome import Chromosome

    with open(f"../setting.json") as f2:
        Settg = json.load(f2)

    p = Population(Setting=Settg)


    # p.Mutation()
    # p.Inversion()
    # cProfile.run('p.Mutation()')
    # cProfile.run('p.Selection()')
    # cProfile.run('p.Inversion()')
    # cProfile.run('p.Crossover()')

    cProfile.run('p.GenerateOffspring_With_logFile()')


    for c in range(len(p.Chrom)):
        print(f"{c}: {p.Chrom[c].gene.tolist()}")

    print('--------------------=-==-=-=-=-=-=-=-=-====')

    




