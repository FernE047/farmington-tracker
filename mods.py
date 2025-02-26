import json
import utils

with open("vdatabase.json", "r", encoding="UTF-8") as f:
    database_list = json.load(f)
mods = set()
database = {}
for mod in database_list:
    mod["game_amount"] = 0
    mods.add(mod["id"])
    database[mod["id"]] = mod
database_list = None
step = 100
offset = 0
while True:
    try:
        print(step)
        if step == 0:
            print(f"jumped offset {offset}")
            offset += 1
            step = 100
        games = utils.doARequest(
            f"games?offset={offset}&max={step}&embed=moderators", mute_exceptions=True
        )
        games = games.get("data", [])
        for game in games:
            game_id = game.get("id", "")
            json.dump(game, open(f"outputs/games/{game_id}.json", "w"))
            for mod in game.get("moderators", {}).get("data", []):
                modID = mod.get("id", "")
                if not modID:
                    continue
                if modID in mods:
                    database[modID]["game_amount"] += 1
                    continue
                mods.add(modID)
                json.dump(mod, open(f"outputs/mods/{modID}.json", "w"))
                if mod["location"] is None:
                    flag = ":united_nations:"
                else:
                    flag = f":flag_{mod['location']['country']['code'][:2]}:"
                name = mod["names"]["international"]
                print(f"{modID} : {name}, {flag}, 1", offset)
                database[modID] = {
                    "id": modID,
                    "name": name,
                    "flag": flag,
                    "game_amount": 1,
                }
            utils.time_estimation(offset, 40000, step)
        offset += step
        if len(games) < step:
            break
    except Exception:
        step = step // 2
        continue

database_list = list(database.values())

with open("vdatabase.json", "w", encoding="UTF-8") as vd:
    vd.truncate(0)
    vd.writelines(json.dumps(database_list))
