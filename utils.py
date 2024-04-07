import requests, time, json

SRC_URL = "https://www.speedrun.com/api/v"
DELAY = 0.7 # delay to not exceed rate limit
RATE_LIMIT = time.time()
BEGIN = time.time()

def format_time(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    days_str = str(days)
    hours_str = str(hours).zfill(2)
    minutes_str = str(minutes).zfill(2)
    seconds_str = str(seconds).zfill(2)
    time_str = ""
    if days > 0:
        time_str += f"{days_str}D {hours_str}h {minutes_str}m {seconds_str}s"
    elif hours > 0:
        time_str += f"{hours_str}h {minutes_str}m {seconds_str}s"
    elif minutes > 0:
        time_str += f"{minutes_str}m {seconds_str}s"
    else:
        time_str += f"{seconds_str}s"
    return time_str

def time_estimation(n, total):
    global BEGIN
    end = time.time()
    to_process = total - n
    elapsed_time = end - BEGIN
    single = elapsed_time / (n+1)
    remaining = (to_process - 1) * single
    print(" : ".join([format_time(elapsed_time), str(single), format_time(remaining)]))

def rateLimit():
    global RATE_LIMIT, DELAY
    now = time.time()
    duration = now - RATE_LIMIT
    if duration < DELAY:
        time.sleep(DELAY - duration)
    RATE_LIMIT = now

def doARequest(requestText, v=1):
    global SRC_URL
    src_url = f"{SRC_URL}{v}/"
    while True:
        rateLimit()
        try:
            data = requests.get(f"{src_url}{requestText}", timeout=60)
            data = data.json()
            if "status" in data:
                if data["status"] == 404:
                    return False
                else:
                    print(f"sleep 10 secs : {data}")
                    time.sleep(10)
                    continue
            return data
        except TimeoutError:
            print("TimeoutError. Retrying after 10 seconds...")
            time.sleep(10)
        except Exception as e:
            print(f"Error: {e}. Retrying after 10 seconds...")
            time.sleep(10)

def dump_info(data, folder):
    with open(f"outputs/{folder}/{data['id']}.json", "w",encoding="UTF-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def updateAllPlatforms():
    all_platforms = []
    offset = 0
    while True:
        platforms = doARequest(f"platforms?offset={offset}&max=100")
        if not platforms:
            return all_platforms
        for platform in platforms['data']:
            dump_info(platform,"platforms")
            all_platforms.append(platform)
        print(len(platforms['data']))
        if len(platforms['data']) < 100:
            return all_platforms
        offset += 100

def separateNewRuns(runs,lastrun_id):
    if lastrun_id not in [run["id"] for run in runs]: return runs
    runs_return = []
    for run in runs:
        if run["id"] == lastrun_id: return runs_return
        runs_return.append(run)

def get_runs(func,**kwargs):
    params = ""
    if kwargs:
        params += "&"
    params += "&".join([f"{key}={value}" for key, value in kwargs.items()])
    allruns = []
    lastrun_id = ""
    for direction in ["asc", "desc"]:
        offset = 0
        while offset < 10000:
            runs = doARequest(f"runs?direction={direction}&max=200&offset={offset}&orderby=date{params}")
            if not runs: return False #deleted user while fetching
            runs = runs.get("data",[])
            if direction == "desc": runs = separateNewRuns(runs,lastrun_id)
            allruns.extend(func(runs))
            if len(runs) < 200: return allruns
            offset += 200
        lastrun_id = allruns[-1]["id"]
        if offset != 10000: return allruns
    return allruns

def make_lb(database, category, limit=200, space_amount=28,
            func_value=lambda x: x, reverse=True, subtitle="",
            flag = True, func_flag="", func_name=""):
    if flag:
        if not func_flag:
            func_flag = lambda x: f"`:{data['flag']}:`"
    else:
        func_flag = lambda x: ""
    if not func_name:
        func_name = lambda x: x["name"]
    with open(database, "r", encoding="UTF-8") as f:
        data = json.load(f)
    lb = {}
    filtered_data = [x for x in data if x.get(category) != None]
    sorted_data = sorted(filtered_data, key=lambda x: x[category], reverse=reverse)
    untied_position, position, last_value = 1, 1, []
    with open(f"outputs/{subtitle}_{category}_lb.txt", "w", encoding="UTF-8") as f:
        for data in sorted_data:
            value = func_value(data[category])
            if value != last_value:
                position = untied_position
            if position > limit: break
            name = func_name(data)
            flag = func_flag(data)
            main_message = f"{position}{value}{name}"
            pretty_spaces = " "*(space_amount-len(main_message))
            f.writelines(f"`{position}.{flag}{name}{pretty_spaces} {value}`\n")
            untied_position+=1
            last_value = value

def is_user_deleted(**kwargs):
    params = "=".join(list(kwargs.items())[0])
    runs = doARequest(f"runs?{params}&max=1")
    return not runs

def webScrape(user_id): 
    # This function is not used in the code, use by your own risk.
    # it's against the SRC ToS to scrape their website.
    url = f"https://www.speedrun.com/users/{user_id}"
    while True:
        try:
            response = requests.get(url)
            html = response.text

            # Find the div with class "hidden"
            start_index = html.find('<div class="hidden">')
            end_index = html.find('</div>', start_index)
            hidden_div = html[start_index:end_index]

            # Find the JSON inside the script tag
            start_index = hidden_div.find('type="application/json">')
            end_index = hidden_div.find('</script>', start_index)
            script_content = hidden_div[start_index:end_index]

            # Extract the JSON data
            start_index = script_content.find('{')
            end_index = script_content.rfind('}') + 1
            json_data = script_content[start_index:end_index]

            # This Json will have all data used on the user runs, categories, variables, everything
            # but you have to make a second request to get the user's Ils runs
            # https://www.speedrun.com/users/{user_id}?view=levels

            return json.loads(json_data)
        except TimeoutError:
            print("TimeoutError. Retrying after 10 seconds...")
            time.sleep(10)
        except Exception as e:
            print(f"Error: {e}. Retrying after 10 seconds...")
            time.sleep(10)