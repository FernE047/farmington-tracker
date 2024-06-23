import json
import os
from utils import *

def processRun(run):
    players = run.get("players",[])
    if not players: return
    player = players[0]
    if player["rel"] == "guest" and player["name"].lower() == "n/a": return
    return run

def processRuns(runs):
    allruns = []
    for run in runs:
        run = processRun(run)
        if run: allruns.append(run)
    return allruns

def process20kRuns(runs,fetched_runs):
    allruns = []
    for run in runs:
        if run["id"] in [fetched_run["id"] for fetched_run in fetched_runs]: continue
        run = processRun(run)
        if run: allruns.append(run)
    return allruns
    
def getRuns(user_id):
    allruns = get_runs(processRuns,examiner=user_id)
    return allruns

def getRuns20k(moderator):
    allruns = []
    for platform_filename in os.listdir("outputs/platforms/"):
        for emu in ["1", "0"]:
            for status in ["verified", "rejected"]:
                with open(f"outputs/platforms/{platform_filename}", "r", encoding="UTF-8") as f:
                    platform = json.load(f)
                print(emu, platform["name"], status, moderator["name"], len(allruns))
                allruns.extend(get_runs(lambda x:process20kRuns(x,allruns), examiner=moderator["id"], emulated=emu, platform=platform["id"], status=status))
    return allruns

with open("vdatabase.json", "r", encoding="UTF-8") as f:
    moderators_data = json.load(f)
updateAllPlatforms()
total = len(moderators_data)
for n,moderator in enumerate(moderators_data):
    print(n,moderator)
    if is_user_deleted(examiner = moderator["id"]):
        print(f"deleted : {moderator['name']}")
        continue
    if "20k_club" not in moderator:
        moderator["20k_club"] = False
    if moderator["20k_club"]:
        runs = getRuns20k(moderator)
        moderator["20k_club"] = len(runs) >= 20000
    else:
        runs = getRuns(moderator["id"])
        moderator["20k_club"] = len(runs) >= 20000
        if moderator["20k_club"]:
            runs = getRuns20k(moderator)
    moderator["runs_amount"] = len(runs)
    print(f"{moderator['name']} : {total - n - 1} : {len(runs)}")
    time_estimation(n, total)
with open("vdatabase.json", "w", encoding="UTF-8") as f:
    json.dump(moderators_data, f, indent=4, ensure_ascii=False)
make_lb("vdatabase.json", "runs_amount")
make_lb("vdatabase.json", "game_amount")