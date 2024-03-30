import json
from utils import *

def extract_length(data, cat):
    value = data.get(cat,"")
    if not value: value = ""
    return len(value)

def process_data(game):
    game.pop("links")
    levels = game.pop("levels")["data"]
    categories = game.pop("categories")["data"]
    variables = game.pop("variables")["data"]
    process_game(game, levels, categories, variables)
    process_categories(game,categories)
    process_levels(game,levels)
    values = process_variables(game,variables)
    return {"game": game, "levels": levels, "categories": categories, "variables": variables, "values": values}

def process_game(game, levels, categories, variables):
    for data in [("levels",levels),("categories",categories),("variables",variables)]:
        game[data[0]] = [item["id"] for item in data[1]]
    game["name"] = game["names"]["international"]
    dump_info(game, "games")
    for cat in ["levels","categories","variables","platforms","gametypes","regions","genres","engines","developers","publishers","moderators"]:
        game[cat] = extract_length(game, cat)
    for cat in ["name","abbreviation","weblink","discord"]:
        game[f"{cat}_length"] = extract_length(game, cat)

def process_levels(game,levels):
    for level in levels:
        level.pop("links")
        level["game_id"] = game["id"]
        level["game"] = game["name"]
        dump_info(level, "levels")
        for cat in ["name","rules","weblink"]:
            level[f"{cat}_length"] = extract_length(level, cat)

def process_categories(game,categories):
    for category in categories:
        category.pop("links")
        category["game_id"] = game["id"]
        category["game"] = game["name"]
        dump_info(category, "categories")
        for cat in ["name","rules","weblink"]:
            category[f"{cat}_length"] = extract_length(category, cat)

def process_variables(game,variables):
    all_values = []
    for variable in variables:
        variable.pop("links")
        variable["game_id"] = game["id"]
        variable["game"] = game["name"]
        dump_info(variable, "variables")
        values = variable.get("values",{}).get("values",[])
        variable["values_length"] = len(values)
        variable["name_length"] = extract_length(variable, "name")
        all_values.extend(process_values(game,variable,values))
    return all_values

def process_values(game,variable,values):
    all_values = []
    for value_id in values:
        value = values[value_id]
        value["id"] = value_id
        value["game_id"] = game["id"]
        value["variable_id"] = variable["id"]
        value["game"] = game["name"]
        value["variable"] = variable["name"]
        dump_info(value, "values")
        for cat in ["label","rules"]:
            value[f"{cat}_length"] = extract_length(value, cat)
        all_values.append(value)
    return all_values

updateAllPlatforms()
offset = 0
data_total = {
    "games": [],
    "levels": [],
    "categories": [],
    "variables": [],
    "values": []
}
while True:
    games = doARequest(f"games?offset={offset}&max=200&embed=levels,categories,variables")
    if not games: continue
    games = games["data"]
    for game in games:
        data = process_data(game)
        data_total["games"].append(data["game"])
        data_total["levels"].extend(data["levels"])
        data_total["categories"].extend(data["categories"])
        data_total["variables"].extend(data["variables"])
        data_total["values"].extend(data["values"])
    print(len(data_total["games"]))
    if len(games) < 100:
        break
    offset += 200
    time_estimation(offset, 40000)
for cat in data_total:
    with open(f"outputs/{cat}_output.json", "w") as g:
        json.dump(data_total[cat], g, indent=4)

#game
database_name = "outputs/games_output.json"
subtitle = "game"
for cat in ["levels","categories","variables","platforms","gametypes","regions","genres","engines","developers","publishers","moderators"]:
    make_lb(database_name, f"{cat}", limit = 100, subtitle=subtitle, flag = False)
for cat in ["name","abbreviation","weblink","discord"]:
    func_name = lambda x: f"{x["name"]}" + (f" : {x[cat]}" if cat != "name" else "")
    make_lb(database_name, f"{cat}_length", limit = 100, subtitle=subtitle, flag = False, func_name=func_name)
#for cat in ["release-date","created"]:
#    func_name = lambda x: f"{x["name"]} : {x[cat]}"
#    make_lb(database_name, f"{cat}", limit = 100, subtitle=subtitle, reverse = False, flag = False, func_name=func_name)


#levels
database_name = "outputs/levels_output.json"
subtitle = "level"
for cat in ["name","rules","weblink"]:
    func_name = lambda x: f"{x["game"]} : {x[cat]}"
    make_lb(database_name, f"{cat}_length", limit = 100, subtitle=subtitle, flag = False, func_name=func_name)

#categories
database_name = "outputs/categories_output.json"
subtitle = "category"
for cat in ["name","rules","weblink"]:
    func_name = lambda x: f"{x["game"]} : {x[cat]}"
    make_lb(database_name, f"{cat}_length", limit = 100, subtitle=subtitle, flag = False, func_name=func_name)

#variables
database_name = "outputs/variables_output.json"
subtitle = "variable"
cat = "name"
func_name = lambda x: f"{x["game"]} : {x[cat]}"
make_lb(database_name, f"{cat}_length", limit = 100, subtitle=subtitle, flag = False, func_name=func_name)
subtitle = "variable"
cat = "values"
func_name = lambda x: f"{x["game"]}"
make_lb(database_name, f"{cat}_length", limit = 100, subtitle=subtitle, flag = False, func_name=func_name)

#values
database_name = "outputs/values_output.json"
subtitle = "value"
for cat in ["label","rules"]:
    func_name = lambda x: f"{x["game"]} : {x["variable"]} : {x["label"]}"
    make_lb(database_name, f"{cat}_length", limit = 100, subtitle=subtitle, flag = False, func_name=func_name)