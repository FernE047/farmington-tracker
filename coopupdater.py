import requests
from core.request_handler import request_handler
import utils
import csv
import time
from collections import defaultdict

platforms = {item["id"]: item["name"] for item in utils.updateAllPlatforms()}
# print(platforms)
with open("coop_categories.csv", "w", newline="", encoding="UTF-8") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter="\t")
    csvwriter.writerow(["game_id", "category_id"])
    offset = 0
    max_limit = 200
    request_count = 0
    start_time = time.time()
    total_games = 40000
    while True:
        games = request_handler.request(
            f"games?offset={offset}&max=200&embed=levels,categories"
        )
        if not games:
            continue
        games_data = games["data"]
        for game in games_data:
            game_id = game["id"]
            game_name = game.get("names", {"international": ""}).get("international")
            game_platforms = ";".join(
                [platforms[plat] for plat in game.get("platforms", [])]
            )
            if "categories" in game:
                for category in game["categories"]["data"]:
                    player_value = category["players"]["value"]
                    if player_value > 1:
                        category_id = category["id"]
                        category_type = category["type"]
                        category_name = category["name"]
                        category_url = category["weblink"]
                        player_type = category["players"]["type"]
                        csvwriter.writerow(
                            [
                                game_id,
                                category_id,
                                game_name,
                                game_platforms,
                                category_url,
                                category_type,
                                player_type,
                                player_value,
                            ]
                        )
        utils.time_estimation(offset, total_games)
        if len(games_data) < max_limit:
            print("Reached the last page. Breaking the loop.")
            break
        offset += max_limit
print("CSV file has been generated!")
game_and_category_ids = []
with open("coop_categories.csv", mode="r", encoding="UTF-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter="\t")
    next(csv_reader, None)
    for row in csv_reader:
        game_and_category_ids.append({"game_id": row[0], "category_id": row[1]})
with open("multiplayer_runs.csv", mode="w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Run_ID", "Runner_IDs"])
with open("multiplayer_runs.csv", mode="a", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    for n, pair in enumerate(game_and_category_ids):
        print(n, pair)
        game_id = pair["game_id"]
        category_id = pair["category_id"]
        offset = 0
        runs = utils.get_runs(
            lambda x: x, game=game_id, category=category_id, status="verified"
        )
        if runs is None:
            print("Error retrieving runs. Retrying...")
            time.sleep(5)
            continue
        for run in runs:
            players = run["players"]
            if len(players) > 1:
                line = [run["id"]]
                runner_ids = []
                for player in players:
                    name = player.get("id", "")
                    if not name:
                        name = player.get("name", "UNKNOWN_NAME")
                    line.append(name)
                csv_writer.writerow(line)
        utils.time_estimation(n, len(game_and_category_ids))
print("Done!")
value_count = defaultdict(int)
n = 0
with open("multiplayer_runs.csv", "r", encoding="UTF-8") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    for row in csvreader:
        n += 1
        for value in row[1:]:
            value_count[value] += 1
sorted_value_count = {
    k: v for k, v in sorted(value_count.items(), key=lambda item: item[1], reverse=True)
}
with open("value_count_output.csv", "w", newline="", encoding="UTF-8") as outfile:
    csvwriter = csv.writer(outfile, delimiter=";")
    csvwriter.writerow(["Value", "Frequency"])
    for value, count in sorted_value_count.items():
        csvwriter.writerow([value, count])


def get_user_details(user_id):
    src = "https://www.speedrun.com/api/v1/"
    response = requests.get(src + f"users/{user_id}").json()
    try:
        data = response["data"]
        username = data["names"]["international"]
        flag = (
            f":flag_{data['location']['country']['code'][:2]}:"
            if data["location"]
            else ":united_nations:"
        )
        return {"username": username, "flag": flag}
    except KeyError:
        return None


leaderboard = {}
with open("value_count_output.csv", "r", encoding="UTF-8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=";")
    next(csvreader)
    for row in csvreader:
        user_id, score = row
        leaderboard[user_id] = leaderboard.get(user_id, 0) + int(score)
n = 0
final_leaderboard = {}
for user_id, score in sorted(leaderboard.items(), key=lambda x: x[1], reverse=True):
    n += 1
    print(n)
    if n > 300:
        break
    if len(user_id) == 8:
        user_details = get_user_details(user_id)
        if user_details:
            flag = user_details["flag"]
            username = user_details["username"]
        else:
            flag = "(guest)"
            username = user_id.strip()
    else:
        flag = "(guest)"
        username = user_id.strip()

    final_leaderboard[user_id] = [username, flag, score]
rank = 1
last_one = 0
for n, (user_id, details) in enumerate(final_leaderboard.items(), 1):
    username, flag, score = details
    if score != last_one:
        rank = n
    print(f"`{rank}.{score}`{flag}`{username}`")
    last_one = score


def get_user_details(user_id, known_users):
    if user_id in known_users:
        return known_users[user_id]
    response = request_handler.request(f"users/{user_id}")
    try:
        data = response["data"]
        username = data["names"]["international"]
        flag = (
            f":flag_{data['location']['country']['code'][:2]}:"
            if data["location"]
            else ":united_nations:"
        )
        known_users[user_id] = {"username": username, "flag": flag}
        return known_users[user_id]
    except Exception as _:
        return {"username": user_id, "flag": "(quest)"}


team_leaderboard = {}
with open("multiplayer_runs.csv", "r", encoding="UTF-8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    next(csvreader)
    for row in csvreader:
        run_id, *team_members = row
        team_id = ",".join(sorted(team_members))
        team_leaderboard[team_id] = team_leaderboard.get(team_id, 0) + 1
unique_users = set()
with open("teams_rank.csv", "w", newline="", encoding="UTF-8") as file:
    csvwriter = csv.writer(file, delimiter=";")
    for team_id, runs in sorted(
        team_leaderboard.items(), key=lambda x: x[1], reverse=True
    ):
        csvwriter.writerow([runs, *team_id.split(",")])
for team_id, _ in sorted(team_leaderboard.items(), key=lambda x: x[1], reverse=True)[
    :110
]:
    for user_id in team_id.split(","):
        unique_users.add(user_id)
known_users = {}
# for user_id in unique_users:
#    get_user_details(user_id, known_users)
rank = 1
last_one = 0
for n, (team_id, runs) in enumerate(
    sorted(team_leaderboard.items(), key=lambda x: x[1], reverse=True)[:150], 1
):
    team_members = team_id.split(",")
    if runs != last_one:
        rank = n
    team_display = []
    for user_id in team_members:
        if len(user_id) == 8:
            details = get_user_details(user_id, known_users)
            team_display.append(f"{details['flag']}`{details['username']}")
        else:
            team_display.append(f"(guest)`{user_id}")
    team_str = ",`".join(team_display)
    print(f"`{rank}.{runs}`{team_str}`")
    last_one = runs
