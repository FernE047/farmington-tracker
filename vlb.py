import json
with open("outputs/verifieroutput.txt", "r") as o:
    output = "".join(o.readlines())
    lb = {}
    for i in output.split("\n"):
        if not i:
            break
        lb.update({i.split(", ")[0]: int(i.split(", ")[1])})
with open("outputs/verifierfinallb.txt", "a") as flb:
    flb.truncate(0)
    nr, no, ibefore = 1, 1, []
    print(list(dict(sorted(lb.items(), key=lambda item: item[1], reverse=True)).keys()))
    for i in list(dict(sorted(lb.items(), key=lambda item: item[1], reverse=True)).keys()):
        with open("vdatabase.json", "r") as datab:
            if lb[i] != ibefore:
                no = nr
            database = json.loads(datab.readlines()[0])
            flb.writelines(f'`{no}.`{database[i][1]}`{database[i][0]}' + " "*(27-(len(f"{no}"))-(len(str(lb[i]))+len(database[i][0]))) + f'{lb[i]}`\n')
            nr+=1
            ibefore = lb[i]
