import json
import utils
import os


def process20kRuns(runs, fetched_runs):
    allruns = []
    for run in runs:
        if run["id"] in [fetched_run["id"] for fetched_run in fetched_runs]:
            continue
        if run:
            allruns.append(run)
    return allruns


def getRuns(user_id):
    allruns = utils.get_runs(lambda x: x, user=user_id, status="verified")
    return allruns


def getRuns20k(user):
    allruns = []
    for platform_filename in os.listdir("outputs/platforms/"):
        for emu in ["1", "0"]:
            with open(
                f"outputs/platforms/{platform_filename}", "r", encoding="UTF-8"
            ) as f:
                platform = json.load(f)
            print(user["name"], platform["name"], emu, len(allruns))
            allruns.extend(
                utils.get_runs(
                    lambda x: process20kRuns(x, allruns),
                    user=user["id"],
                    emulated=emu,
                    platform=platform["id"],
                    status="verified",
                )
            )
    return allruns


def main():
    with open("database.json", "r", encoding="UTF-8") as f:
        user_data = json.load(f)
    # updateAllPlatforms()
    total = len(user_data)
    for n, user in enumerate(user_data):
        if utils.is_user_deleted(user=user["id"]):
            print(f"deleted : {user['name']}")
            continue
        runs = []
        if user["20k_club"]:
            runs = getRuns20k(user)
            user["20k_club"] = len(runs) >= 20000
        else:
            runs = getRuns(user["id"])
            user["20k_club"] = len(runs) >= 20000
            if user["20k_club"]:
                runs = getRuns20k(user)
        user["totaltime"] = 0
        user["runsIL"] = 0
        user["runsFG"] = 0
        for run in runs:
            user["totaltime"] += run["times"]["primary_t"]
            if run["level"] is None:
                user["runsFG"] += 1
            else:
                user["runsIL"] += 1
        user["runs"] = len(runs)
        print(f"{n} : {user}")
        utils.time_estimation(n, total)
    with open("database.json", "w", encoding="UTF-8") as f:
        json.dump(user_data, f, indent=4)
    utils.make_lb(
        "database.json", "totaltime", 200, 40, lambda x: utils.format_time(int(x))
    )
    utils.make_lb("database.json", "runs")
    utils.make_lb("database.json", "runsIL")
    utils.make_lb("database.json", "runsFG")
