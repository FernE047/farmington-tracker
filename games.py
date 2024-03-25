import requests, json, time

#NEEDS TO BE REWRITTEN

src = "https://www.speedrun.com/api/v1/"

t = time.time()
data = {"longlevel": {}, "longcat": {}, "longabrv": {}, "longgame": {}, "mostlvls": {}, "mostmods": {}, "mostplat": {}}
for offset in range(100000000000):
    while True:
        try:
            games = requests.get(src + f"games?offset={offset*200}&max=200&embed=levels,categories").json()
            try:
                games = games["data"]
                break
            except Exception:
                print(f"we throttle at offset : {offset}, error : {games['status'], games['message']}")
                time.sleep(10)
        except Exception:
            for i in range(2):
                games = requests.get(src + f"games?offset={offset*200}&max=100&embed=levels,categories").json()["data"]
                games.append(requests.get(src + f"games?offset={offset*200+100}&max=100&embed=levels,categories").json()["data"])
    if time.time() - t < 0.7:
        try:
            time.sleep(0.7 - (time.time() - t))
            t = time.time()
        except Exception:
            t = time.time()
    for game in games:
        longlevel = ""
        for lvl in game["levels"]["data"]:
            if len(longlevel) < len(lvl["name"]):
                longlevel = lvl["name"]
        longcat = ""
        for cat in game["categories"]["data"]:
            if len(longcat) < len(cat["name"]):
                longcat = cat["name"]
        data["longlevel"].update({f'{game["names"]["international"]}[{longlevel}]': len(longlevel)})
        data["longcat"].update({f'{game["names"]["international"]}[{longcat}]': len(longcat)})
        data["longabrv"].update({game["abbreviation"]: len(game["abbreviation"])})
        data["longgame"].update({game["names"]["international"]: len(game["names"]["international"])})
        data["mostlvls"].update({game["names"]["international"]: len(game["levels"]["data"])})
        data["mostmods"].update({game["names"]["international"]: len(game["moderators"])})
        data["mostplat"].update({game["names"]["international"]: len(game["platforms"])})
        print(game["names"]["international"], len(longlevel), len(longcat), len(game["abbreviation"]), len(game["names"]["international"]), len(game["levels"]["data"]), len(game["moderators"]), len(game["platforms"]))
    if len(games) < 100:
        break
with open("outputs/gamesoutput.json", "a") as g:
    g.truncate(0)
    g.writelines(json.dumps(data))