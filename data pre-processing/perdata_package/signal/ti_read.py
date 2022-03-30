import json



def fun(**value):
    for i in value:
        print(f"{i} ==> {value[i]}")


path = "./jsonformatter.json"

with open(path, 'r', encoding="utf-8") as f:
    data = json.load(f)

new_data = {}
for i in data:
    print(f" ================= {i} ============== ")
    for j in data[i]:
        for k in j:
            print(f"{i} ==> {k} ==> {j[k]}")
            

