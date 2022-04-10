

def combine(caselist:list):
    n = len(caselist)
    res = []

    def backtrack(tmp:list, start:int):
        
        if len(tmp) == 2:
            res.append(tmp[:])
            return

        for i in range(start, n):
            tmp.append(caselist[i])
            backtrack(tmp,  i + 1)
            tmp.pop()
    
    backtrack([], 0)
    return res

r = ["MA5", "MA15", "MA30","MAMA5", "MAMA10"]


dic = {}
for i in r:
    for k in range(len(i)):
        if i[k].isdigit() == True:
            break
    
    if i[:k] not in dic:
        dic[i[:k]] = []

    dic[i[:k]].append(i)
   
print(dic)
for i in dic:
    r = combine(dic[i])
    print(f"===== {r}")
    for k in r:
        print(f"{k} => {k[0]} <> { k[1]}")

