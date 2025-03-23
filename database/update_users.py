import json
import utils
from core.request_handler import request_handler


def extract_flag(user_update):
    flag = user_update.get("location", {})
    if not flag:
        return "united_nations"
    flag = flag.get("country", {}).get("code", "")
    if not flag:
        return "united_nations"
    return f"flag_{flag[:2]}"


def main():
    with open("database.json", "r", encoding="UTF-8") as f:
        users_data = json.load(f)
    for n, user in enumerate(users_data):
        user_update = request_handler.request(f"users/{user['id']}")
        if not user_update:
            user["deleted"] = True
            continue
        user_update = user_update.get("data", {})
        user["flag"] = extract_flag(user_update)
        user["name"] = user_update.get("names", {}).get("international", user["name"])
        utils.time_estimation(n, len(users_data))
    with open("database.json", "w", encoding="UTF-8") as f:
        json.dump(users_data, f, indent=4)


if __name__ == "__main__":
    main()
