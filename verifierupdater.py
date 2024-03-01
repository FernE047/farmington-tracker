import requests, json, time

def rateLimit():
    global t, delay
    now = time.time()
    duration = now - t
    if duration < delay:
        time.sleep(delay - duration)
    t = now

def doARequest(requestText):
    while True:
        rateLimit()
        try:
            runs = requests.get(requestText,timeout=60).json()
            if "status" in runs:
                if runs["status"] == 404:
                    return False
                else:
                    print(f"sleep 10 secs : {runs}")
                    time.sleep(10)
                    continue
            return runs
        except Exception as e:
            print(f"Error: {e}. Retrying after 10 seconds...")
            time.sleep(10)

def processRuns(runs,allruns,lastrun):
    for run in runs:
        players = run.get("players",[])
        if not players:
            continue
        player = players[0]
        if player["rel"] == "guest" and player["name"].lower() == "n/a":
            continue
        if run["id"] == lastrun:
            return True
        allruns.append(run)
    return False
    
def getRuns(userid):
    allruns = []
    lastrun = "whadohdwao///"
    for direction in ["asc", "desc"]:
        offset = 0
        while offset < 10000:
            runs = doARequest(f"{src}runs?examiner={userid}&direction={direction}&max=200&offset={offset}&orderby=date")
            if not runs:
                return False
            runs = runs.get("data",[])
            isABreak = processRuns(runs,allruns,lastrun)
            if len(runs) < 200 or isABreak:
                return allruns
            offset += 200
        lastrun = allruns[-1]["id"]
        if offset != 10000:
            return allruns
    return allruns

src = "https://www.speedrun.com/api/v1/"
with open("vdatabase.json", "r") as f:
    fjson = json.loads(f.readlines()[0])
delay = 0.6
no = 0
usersid = ""
t = time.time()
fjsonk = list(fjson.keys())
total = len(fjsonk)
begin = time.time()
result = {}
for n,userid in enumerate(fjsonk):
    missing = total - n
    if fjson[userid][0] in ["dha", "1", "Reni", "jensj56"]:
        continue
    runs = getRuns(userid)
    if runs is False:
        print(f"deleted : {fjson[userid][0]}")
        continue
    result[userid] = len(runs)
    end = time.time()
    duration = end - begin
    single = duration / (n+1)
    remaining = (missing - 1) * single
    print(f"{fjson[userid][0]} : {missing} : {len(runs)}")
    print(f"{duration} : {single} : {remaining}")
with open("outputs/verifieroutput.txt", "a") as f:
    for i,j in result.items():
        f.writelines(f"{i}, {j}\n")