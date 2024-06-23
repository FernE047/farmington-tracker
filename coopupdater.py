from utils import *
import csv
import time

platforms = {item["id"]:item["name"] for item in updateAllPlatforms()}
#print(platforms)

# Initialize CSV file
with open('coop_categories.csv', 'w', newline='', encoding="UTF-8") as csvfile:
    csvwriter = csv.writer(csvfile,delimiter = "\t")
    csvwriter.writerow(['game_id', 'category_id'])

    offset = 0
    max_limit = 200
    request_count = 0
    start_time = time.time()

    total_games = 40000  # Total number of games as per your information

    while True:
        games = doARequest(f"games?offset={offset}&max=200&embed=levels,categories")
        if not games: continue
        games_data = games["data"]

        for game in games_data:
            game_id = game['id']
            game_name = game.get("names",{"international":""}).get("international")
            game_platforms = ";".join([platforms[plat] for plat in game.get("platforms",[])])

            if 'categories' in game:
                for category in game['categories']['data']:
                    player_value = category['players']['value']
                    if player_value > 1:
                        category_id = category['id']
                        category_type = category["type"]
                        category_name = category["name"]
                        category_url = category["weblink"]
                        player_type = category['players']['type']
                        csvwriter.writerow([game_id, category_id,
                           game_name,game_platforms,category_url,
                           category_type,player_type,player_value])

        # Time prediction
        time_estimation(offset, total_games)

        # Check if we've reached the last page
        if len(games_data) < max_limit:
            print("Reached the last page. Breaking the loop.")
            break

        # Update offset to fetch the next set of games
        offset += max_limit

print("CSV file has been generated!")

# Read game and category IDs from a CSV file
game_and_category_ids = []
with open('coop_categories.csv', mode='r', encoding = "UTF-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    next(csv_reader, None)  # Skip header
    for row in csv_reader:
        game_and_category_ids.append({'game_id': row[0], 'category_id': row[1]})

# Initialize CSV file and write header
with open('multiplayer_runs.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Run_ID', 'Runner_IDs'])

                
# Write to CSV
with open('multiplayer_runs.csv', mode='a', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    for n,pair in enumerate(game_and_category_ids):
        print(n,pair)
        game_id = pair['game_id']
        category_id = pair['category_id']

        offset = 0  # Initialize offset
        runs = get_runs(lambda x:x, game=game_id, category=category_id, status="verified")
        if runs is None:
            print("Error retrieving runs. Retrying...")
            time.sleep(5)
            continue
        for run in runs:
            players = run['players']
            
            # Check if multiplayer
            if len(players) > 1:
                line = [run['id']]
                runner_ids = []
                for player in players:
                    name = player.get("id","")
                    if not name:
                        name = player.get("name","UNKNOWN_NAME")
                    line.append(name)
                csv_writer.writerow(line)
        time_estimation(n, len(game_and_category_ids))

print("Done!")

from collections import defaultdict

# Initialize an empty dictionary to store the frequency of each value
value_count = defaultdict(int)

# Open the CSV file for reading
n = 0
with open('multiplayer_runs.csv', 'r',encoding="UTF-8") as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Skip the header row
    next(csvreader)
    
    # Loop through each row in the CSV file
    for row in csvreader:
        n+=1
        # Only consider values after the second column
        for value in row[1:]:
            value_count[value] += 1
# Sort the dictionary items by frequency in descending order
sorted_value_count = {k: v for k, v in sorted(value_count.items(), key=lambda item: item[1], reverse=True)}

# Open the output CSV file for writing
with open('value_count_output.csv', 'w', newline='',encoding="UTF-8") as outfile:
    csvwriter = csv.writer(outfile, delimiter = ";")
    
    # Write the header row
    csvwriter.writerow(['Value', 'Frequency'])
    
    # Write the frequency of each value
    for value, count in sorted_value_count.items():
        csvwriter.writerow([value, count])


# Function for API call to get user details
def get_user_details(user_id):
    src = "https://www.speedrun.com/api/v1/"
    response = requests.get(src + f"users/{user_id}").json()
    try:
        data = response["data"]
        username = data["names"]["international"]
        flag = f':flag_{data["location"]["country"]["code"][:2]}:' if data["location"] else ":united_nations:"
        return {"username": username, "flag": flag}
    except KeyError:
        return None

# Read CSV and populate initial leaderboard
leaderboard = {}
with open('value_count_output.csv', 'r', encoding="UTF-8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter = ";")
    next(csvreader)  # Skip the header
    
    for row in csvreader:
        user_id, score = row
        leaderboard[user_id] = leaderboard.get(user_id, 0) + int(score)

# Update leaderboard with user details from API
n = 0
final_leaderboard = {}
for user_id, score in sorted(leaderboard.items(), key=lambda x: x[1], reverse=True):
    n+=1
    print(n)
    if n>300:
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
# Print the leaderboard
for n, (user_id, details) in enumerate(final_leaderboard.items(), 1):
    username, flag, score = details
    if score != last_one:
        rank = n
    print(f"`{rank}.{score}`{flag}`{username}`")
    last_one = score

# Function to get user details
def get_user_details(user_id, known_users):
    if user_id in known_users:
        return known_users[user_id]

    response = doARequest(f"users/{user_id}")
    
    try:
        data = response["data"]
        username = data["names"]["international"]
        flag = f':flag_{data["location"]["country"]["code"][:2]}:' if data["location"] else ":united_nations:"
        known_users[user_id] = {"username": username, "flag": flag}
        return known_users[user_id]
    except:
        return {"username": user_id, "flag": "(quest)"}

# Read CSV and populate initial team leaderboard
team_leaderboard = {}
with open('multiplayer_runs.csv', 'r', encoding="UTF-8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter = ",")  # Assuming the delimiter is ","
    next(csvreader)  # Skip the header
    
    for row in csvreader:
        run_id, *team_members = row  # first item is run_id, rest are team members
        # Create a unique identifier for the team by sorting and joining team member IDs
        team_id = ",".join(sorted(team_members))
        team_leaderboard[team_id] = team_leaderboard.get(team_id, 0) + 1


# Find unique users in the top 110 teams
unique_users = set()
with open("teams_rank.csv","w", newline='',encoding = "UTF-8") as file:
    csvwriter = csv.writer(file, delimiter = ";")
    for team_id, runs in sorted(team_leaderboard.items(), key=lambda x: x[1], reverse=True):
        csvwriter.writerow([runs,*team_id.split(",")])

for team_id, _ in sorted(team_leaderboard.items(), key=lambda x: x[1], reverse=True)[:110]:
    for user_id in team_id.split(","):
        unique_users.add(user_id)

# Fetch user details for unique users
known_users = {}
#for user_id in unique_users:
#    get_user_details(user_id, known_users)

rank = 1
last_one = 0
# Print the leaderboard
for n, (team_id, runs) in enumerate(sorted(team_leaderboard.items(), key=lambda x: x[1], reverse=True)[:150], 1):
    team_members = team_id.split(",")
    if runs != last_one:
        rank = n
    team_display = []
    for user_id in team_members:
        if len(user_id) == 8:
            details = get_user_details(user_id, known_users)
            team_display.append(f'{details["flag"]}`{details["username"]}')
        else:
            team_display.append(f"(guest)`{user_id}")
    
    # Join the inline displays together
    team_str = ',`'.join(team_display)
    print(f"`{rank}.{runs}`{team_str}`")
    last_one = runs

