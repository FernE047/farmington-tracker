import requests, json, time
from utils import *

#CODE NOT READY FOR PRODUCTION

with open("vdatabase.json", "r") as f:
    database = json.load(f)
mods = set()
step = 100
offset = 0
while True:
    try:
        print(step)
        if step == 0:
            print(f"jumped offset {offset}")
            offset += 1
            step = 100
        games = doARequest(f"games?offset={offset}&max={step}&embed=moderators")
        games = games.get("data",[])
        for game in games:
            game_id = game.get("id","")
            json.dump(game, open(f"outputs/games/{game_id}.json", "w"))
            for mod in game.get("moderators",{}).get("data",[]):
                modID = mod.get("id","")
                if not modID: continue
                if modID in mods:
                    database[modID][2] += 1
                    continue
                mods.add(modID)
                json.dump(mod, open(f"outputs/mods/{modID}.json", "w"))
                if mod["location"] == None:
                    flag = ":united_nations:"
                else:
                    flag = f':flag_{mod["location"]["country"]["code"][:2]}:'
                name = mod["names"]["international"]
                print(f'{modID} : {name}, {flag}, 1', offset)
                time_estimation(offset,40000)
                database[modID] = [name, flag, 1]
        offset += step
        if len(games) < step:
            break
    except Exception:
        step = step//2
        continue

with open("vdatabase.json", "a") as vd:
    vd.truncate(0)
    vd.writelines(json.dumps(database))