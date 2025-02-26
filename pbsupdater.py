import json
import utils
import runsupdater

with open("database.json", "r", encoding="UTF-8") as f:
    user_datas = json.load(f)


def most_frequent(List):
    try:
        counter = 0
        num = List[0]
        for i in List:
            curr_frequency = List.count(i)
            if curr_frequency > counter:
                counter = curr_frequency
                num = i
        return num
    except Exception:
        return 0


def getDataV1(user):
    alllevels = set()
    allcategories = set()
    allgames = set()
    allgameswithwrs = set()
    gamesmostwrs = []
    allpodiums, allwrs, allILwrs, allFGwrs = 0, 0, 0, 0
    pbs_data = utils.doARequest(f"users/{user['id']}/personal-bests")
    if not pbs_data:
        return
    pbs = pbs_data["data"]
    for run in pbs:
        if run["run"]["level"] is not None:
            alllevels.add(run["run"]["level"])
        if run["run"]["category"] is not None:
            allcategories.add(run["run"]["category"])
        allgames.add(run["run"]["game"])
        if run["place"] == 1:
            allwrs += 1
            if run["run"]["level"] is None:
                allFGwrs += 1
            else:
                allILwrs += 1
            gamesmostwrs.append(run["run"]["game"])
            if run["run"]["game"] not in allgameswithwrs:
                allgameswithwrs.add(run["run"]["game"])
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
    user["obsoletes"] = user["runs"] - len(pbs)
    user["allGamesWithWrs"] = len(allgameswithwrs)
    user["mostFrequentGame"] = most_frequent(gamesmostwrs)


def getDataV2(user):
    allgameswithwrs = set()
    gamesmostwrs = []
    allpodiums, allwrs, allILwrs, allFGwrs, allObsoletes = 0, 0, 0, 0, 0
    pbs_data = utils.doARequest(f"GetUserLeaderboard?userId={user['id']}", v=2)
    if not pbs_data:
        return
    if "error" in pbs_data:
        return
    for run in pbs_data.get("runs", []):
        if "place" in run:
            if run["place"] == 1:
                allwrs += 1
                if "levelId" in run:
                    allILwrs += 1
                else:
                    allFGwrs += 1
                gamesmostwrs.append(run["gameId"])
                if run["gameId"] not in allgameswithwrs:
                    allgameswithwrs.add(run["gameId"])
            if run["place"] <= 3:
                allpodiums += 1
        if "obsolete" in run:
            if run["obsolete"]:
                allObsoletes += 1
    user["levels"] = len(pbs_data["levels"])
    user["categories"] = len(pbs_data["categories"])
    user["games"] = len(pbs_data["games"])
    user["wrs"] = allwrs
    user["FGwrs"] = allFGwrs
    user["ILwrs"] = allILwrs
    user["podiums"] = allpodiums
    user["obsoletes"] = allObsoletes
    user["pbs"] = len(pbs_data["runs"]) - allObsoletes
    user["allGamesWithWrs"] = len(allgameswithwrs)
    user["mostFrequentGame"] = most_frequent(gamesmostwrs)


for n, user in enumerate(user_datas):
    user["flag"] = user["flag"].replace(":", "")
    getDataV2(user)
    print(user["name"])
    utils.time_estimation(n, len(user_datas))
with open("database.json", "w", encoding="UTF-8") as f:
    json.dump(user_datas, f, indent=4)
for cat in [
    "levels",
    "categories",
    "games",
    "wrs",
    "FGwrs",
    "ILwrs",
    "podiums",
    "pbs",
    "allGamesWithWrs",
    "obsoletes",
]:
    print(cat)
    utils.make_lb("database.json", cat)

runsupdater.main()
