import json
with open("outputs/pbsoutput.txt", "r") as o:
    output = "".join(o.readlines())
    # alllevels, allcats, allgames, allwrs, wrsFG, wrsIL, podiums, pbs, gameswithwrs, obsoletes, ratiodata
    lbs = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    for i in output.split("\n"):
        if i == "":
            continue
        for it in range(len(lbs)):
            lbs[it].update({i.split(", ")[0]: int(i.split(", ")[it+1])})
    ratio = {}
    with open("database.json", "r") as datab:
        database = json.loads(datab.readlines()[0])
    for i in output.split("\n"):
        if i == "":
            continue
        userid = i.split(", ")[0]
        if lbs[3][userid] == 0:
            continue
        ratio.update({userid: (lbs[3][userid]/lbs[7][userid])*100})
    lbs.append(ratio)
    with open("outputs/runsoutput.txt", "r") as r:
        runso = r.readlines()
        obsoletes = {}
        for stat in range(len("".join(runso).split("\n"))):
            if "".join(runso).split("\n")[stat] == "":
                continue
            st = "".join(runso).split("\n")[stat].split(", ")
            if len(st) < 2:
                print(f"Error: {st} does not have at least 2 values.")
                continue

            output_lines = output.split("\n")
            if stat >= len(output_lines):
                print(f"Error: output doesn't have line {stat}.")
                continue

            output_values = output_lines[stat].split(", ")
            if len(output_values) < 9:
                print(f"Error: output line {stat} does not have at least 9 values.")
                continue

            obsoletes.update({st[0]: int(st[1])-int(output.split("\n")[stat].split(", ")[8])})
    lbs.append(obsoletes)

allcats = ["levels", "category", "games", "wrs", "wrsFG", "wrsIL", "podiums", "pbs", "gameswithwrs", "gameswithmostwrs", "ratiodata",  "obsoletes"]
for cat in allcats:
    with open(f"outputs/{cat}finallb.txt", "a") as flb:
        flb.truncate(0)
        nr, no, ibefore = 1, 1, 1
        for i in list(dict(sorted(lbs[allcats.index(cat)].items(), key=lambda item: item[1], reverse=True)).keys()):
            if not ibefore == 1:
                if not lbs[allcats.index(cat)][ibefore] == lbs[allcats.index(cat)][i]:
                    no = nr
            if cat != "ratiodata":
                flb.writelines(f'`{no}.`{database[i][1]}`{database[i][0]}' + " "*(26-(len(str(lbs[allcats.index(cat)][i]))+len(database[i][0])+len(str(no)))) + f'{lbs[allcats.index(cat)][i]}`\n')
            else:
                ratiod = f'{round(lbs[allcats.index(cat)][i], 2)}%`'
                flb.writelines(f'{database[i][1]}`{database[i][0]}' + " "*(32-(len(ratiod)+1+len(database[i][0])+len(str(no)))) + ratiod + '\n')
            nr+=1
            ibefore = i
