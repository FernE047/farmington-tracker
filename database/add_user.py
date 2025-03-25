from .update_users import get_user_info
from . import Database_Manager


def main() -> None:
    db = Database_Manager()
    user_id = "INSERT ID HERE"
    try:
        user_update = get_user_info(user_id)
        db.update_user(user_update)
    except ResourceWarning as _:
        print(f"{user_id} does not exist")


if __name__ == "__main__":
    main()
