from typing import Any, Optional
from common.type_def import UserDatabaseData
from database import Database_Manager
from common.speedrun_types import RunResponse, UserData, UserResponse
from core.request_handler import request_handler


def is_user_deleted(params: dict[str, Any]):
    params_list = ["max=1"]
    for param in params.items():
        params_list.append(f"{param[0]}={param[1]}")
    params_str = "&".join(params_list)
    runs = request_handler.request(f"runs?{params_str}", 1, response_type=RunResponse)
    return not runs


def extract_flag(user_update: UserData) -> str:
    location = user_update.get("location")
    if location is None:
        return "united_nations"
    country_code = location.get("country", {}).get("code", "")
    if not country_code:
        return "united_nations"
    return f"flag_{country_code[:2]}"


def get_user_info(user_id: str) -> UserDatabaseData:
    response: Optional[UserResponse] = request_handler.request(
        f"users/{user_id}", response_type=UserResponse
    )
    if not response:
        raise ResourceWarning(f"{user_id} was deleted")
    user_update: UserData = response["data"]
    user: UserDatabaseData = {
        "id": user_id,
        "flag": extract_flag(user_update),
        "name": user_update.get("names", {}).get("international", "no_name"),
    }
    return user


def update_all_users() -> None:
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
    update_all_users()
