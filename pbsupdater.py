import requests, json, time
src = "https://www.speedrun.com/api/v1/"
with open("database.json", "r") as f:
    fjson = json.loads(f.readlines()[0])
no, no2 = 0, 0

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

no2 = 0
t = time.time()
skip = True
for id in fjson:
    if skip:
        if id == "x3557mqj":
            skip = False
        else:
            print(id)
            continue
    alllevels, allcategories, allgames, allgameswithwrs, gamesmostwrs  = [], [], [], [], []
    allpodiums, allwrs, allILwrs, allFGwrs= 0, 0, 0, 0
    deleted = False
    if (no % 50 == 0 and no != 0) and time.time() - t < 40:
        time.sleep(40 - (time.time() - t))
        t = time.time()
    no2 += 1
    while True:
        try:
            pbs = requests.get(src + f"users/{id}/personal-bests").json()
        except Exception:
            continue
        no += 1
        if "status" in list(pbs.keys()):
            if pbs["status"] == 404:
                deleted = True
                break
            else:
                print("We're getting rate limited!")
                time.sleep(10)
                continue
        pbs = pbs["data"]
        for run in pbs:
            if run["run"]["level"] != None and not (run["run"]["level"] in alllevels):
                alllevels.append(run["run"]["level"])
            if run["run"]["category"] != None and not (run["run"]["category"] in allcategories):
                allcategories.append(run["run"]["category"])
            if not (run["run"]["game"] in allgames):
                allgames.append(run["run"]["game"])
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
        break
    print(fjson[id][0], len(list(fjson.keys()))-no2, len(pbs), len(alllevels), len(allcategories), len(allgames), allwrs, allFGwrs, allILwrs, allpodiums, len(pbs), len(allgameswithwrs))
    with open("outputs/pbsoutput.txt", "a") as p:
        if deleted:
            continue
        else:
            p.writelines(f"{id}, {len(alllevels)}, {len(allcategories)}, {len(allgames)}, {allwrs}, {allFGwrs}, {allILwrs}, {allpodiums}, {len(pbs)}, {len(allgameswithwrs)}, {gamesmostwrs.count(most_frequent(gamesmostwrs))}\n")