from typing import Any
from ..common.type_def import UserDatabaseData
from . import Database_Manager
from ..common.speedrun_types import UserData
from core.request_handler import request_handler


def extract_flag(user_update: UserData) -> str:
    location = user_update.get("location")
    if location is None:
        return "united_nations"
    country_code = location.get("country", {}).get("code", "")
    if not country_code:
        return "united_nations"
    return f"flag_{country_code[:2]}"


def get_user_info(user_id: str) -> UserDatabaseData:
    user_update: UserData = request_handler.request(
        f"users/{user_id}", response_type=UserData
    )
    if not user_update:
        raise ResourceWarning(f"{user_id} was deleted")
    user: dict[str, Any] = {}
    user = user_update.get("data", {})
    user["flag"] = extract_flag(user_update)
    user["name"] = user_update.get("names", {}).get("international", user["name"])
    return UserDatabaseData(**user)


def main() -> None:
    db = Database_Manager()
    for user in db.public:
        user_id = user.get("id")
        if user_id is None:
            continue
        try:
            user_update = get_user_info(user_id)
            db.update_user(user_update)
        except ResourceWarning as _:
            print(f"{user['name']} was deleted")


if __name__ == "__main__":
    main()
