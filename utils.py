import os
import time
import json
from core.request_handler import request_handler


def dump_info(data, folder):
    if not os.path.exists(f"outputs/{folder}"):
        os.makedirs(f"outputs/{folder}")
    with open(f"outputs/{folder}/{data['id']}.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def updateAllPlatforms():
    all_platforms = []
    offset = 0
    while True:
        platforms = request_handler.request(f"platforms?offset={offset}&max=100")
        if not platforms:
            return all_platforms
        for platform in platforms["data"]:
            dump_info(platform, "platforms")
            all_platforms.append(platform)
        print(len(platforms["data"]))
        if len(platforms["data"]) < 100:
            return all_platforms
        offset += 100


def separateNewRuns(runs, lastrun_id):
    if lastrun_id not in [run["id"] for run in runs]:
        return runs
    runs_return = []
    for run in runs:
        if run["id"] == lastrun_id:
            return runs_return
        runs_return.append(run)


def get_runs(func, **kwargs):
    params = ""
    if kwargs:
        params += "&"
    params += "&".join([f"{key}={value}" for key, value in kwargs.items()])
    allruns = []
    lastrun_id = ""
    for direction in ["asc", "desc"]:
        offset = 0
        while offset < 10000:
            runs = request_handler.request(
                f"runs?direction={direction}&max=200&offset={offset}&orderby=date{params}"
            )
            if not runs:
                return False  # deleted user while fetching
            runs = runs.get("data", [])
            if direction == "desc":
                runs = separateNewRuns(runs, lastrun_id)
            allruns.extend(func(runs))
            if len(runs) < 200:
                return allruns
            offset += 200
        lastrun_id = allruns[-1]["id"]
        if offset != 10000:
            return allruns
    return allruns


def make_lb(
    database,
    category,
    limit=200,
    space_amount=28,
    func_value=lambda x: x,
    reverse=True,
    subtitle="",
    flag=True,
    func_flag="",
    func_name="",
):
    if flag:
        if not func_flag:

            def func_flag(x):
                return f"`:{data['flag']}:`"
    else:

        def func_flag(x):
            return ""

    if not func_name:

        def func_name(x):
            return x["name"]

    with open(database, "r", encoding="UTF-8") as f:
        data = json.load(f)
    filtered_data = [x for x in data if x.get(category) is not None]
    sorted_data = sorted(filtered_data, key=lambda x: x[category], reverse=reverse)
    untied_position, position, last_value = 1, 1, []
    if not subtitle:
        name_file = f"outputs/{'_'.join([category, 'lb.txt'])}"
    else:
        name_file = f"outputs/{'_'.join([subtitle, category, 'lb.txt'])}"
    with open(name_file, "w", encoding="UTF-8") as f:
        for data in sorted_data:
            value = func_value(data[category])
            if value != last_value:
                position = untied_position
            if position > limit:
                break
            name = func_name(data)
            flag = func_flag(data)
            main_message = f"{position}{value}{name}"
            pretty_spaces = " " * (space_amount - len(main_message))
            f.writelines(f"`{position}.{flag}{name}{pretty_spaces} {value}`\n")
            untied_position += 1
            last_value = value


def is_user_deleted(**kwargs):
    params = "=".join(list(kwargs.items())[0])
    runs = request_handler.request(f"runs?{params}&max=1")
    return not runs


def time_estimation(n, total, step=1):
    global BEGIN, TIME_DATA
    end = time.time()
    elapsed_time = (end - BEGIN) / step
    TIME_DATA.append(elapsed_time)
    if len(TIME_DATA) > 10:
        TIME_DATA.pop(0)
    average = sum(TIME_DATA) / len(TIME_DATA)
    to_process = total - n
    remaining = (to_process - 1) * average
    print(" : ".join([format_time(elapsed_time), str(average), format_time(remaining)]))
    BEGIN = end
