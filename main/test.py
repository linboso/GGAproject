import json

with open("./SignalMap.json") as f:
    data = json.load(f)

dlist = []
for i in data.values():
    for st in i:
        dlist.append(st)
print(dlist)