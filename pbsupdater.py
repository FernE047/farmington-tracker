import json
from utils import *

with open("database.json", "r", encoding="UTF-8") as f:
    user_datas = json.load(f)

def most_frequent(List):
    try:
        counter = 0
        num = List[0]
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num = i
        return num
    except Exception:
        return 0

skip = True
for n,user in enumerate(user_datas):
    alllevels = set()
    allcategories = set()
    allgames = set()
    allgameswithwrs = set()
    gamesmostwrs  = []
    allpodiums, allwrs, allILwrs, allFGwrs= 0, 0, 0, 0
    pbs_data = doARequest(f"users/{user['id']}/personal-bests")
    if not pbs_data: continue
    pbs = pbs["data"]
    for run in pbs:
        if run["run"]["level"] != None: alllevels.add(run["run"]["level"])
        if run["run"]["category"] != None: allcategories.add(run["run"]["category"])
        allgames.add(run["run"]["game"])
        if run["place"] == 1:
            allwrs += 1
            if run["run"]["level"] == None:
                allFGwrs += 1
            else:
                allILwrs += 1
            gamesmostwrs.append(run["run"]["game"])
            if not run["run"]["game"] in allgameswithwrs:
                allgameswithwrs.append(run["run"]["game"])
        if run["place"] <= 3:
            allpodiums += 1
    user["levels"] = len(alllevels)
    user["categories"] = len(allcategories)
    user["games"] = len(allgames)
    user["wrs"] = allwrs
    user["FGwrs"] = allFGwrs
    user["ILwrs"] = allILwrs
    user["podiums"] = allpodiums
    user["pbs"] = len(pbs)
    user["allGamesWithWrs"] = len(allgameswithwrs)
    user["mostFrequentGame"] = most_frequent(gamesmostwrs)
    print(user["name"])
    time_estimation(n, len(user_datas))
with open("database.json", "w", encoding="UTF-8") as f:
    json.dump(user_datas, f, indent=4)
for cat in ["levels", "categories", "games", "wrs", "FGwrs", "ILwrs", "podiums", "pbs", "allGamesWithWrs", "mostFrequentGame"]:
    make_lb("database.json", cat)