import sqlite3


class Database_Manager:
    def __init__(self):
        self.runners = Database("runners")
        self.public = Database("public")

    def add_user(self, user):
        self.runners.execute_commit(
            """
            INSERT INTO users (id, name, flag, Large_20k) 
            VALUES (?, ?, ?, ?)
        """,
            (user["id"], user["name"], user["flag"], False),
        )
        self.public.execute_commit(
            """
            INSERT INTO users (id, name, flag) 
            VALUES (?, ?, ?)
        """,
            (user["id"], user["name"], user["flag"]),
        )

    def update_user(self, user):
        for db in (self.runners, self.public):
            db.execute_commit(
                """
                UPDATE users 
                SET name = ?, flag = ?
                WHERE id = ?
            """,
                (user["name"], user["flag"], user["id"]),
            )
        print(f"User {user['id']} updated in both databases.")

    def new_column(self, column_name, default_value):
        for db in (self.runners, self.public):
            db.execute_commit(
                """
                ALTER TABLE users
                ADD COLUMN ? TEXT DEFAULT ?;
            """,
                (column_name, default_value),
            )
        print(f"Column {column_name} added in both databases.")

    def update_values(self, user: dict[str, str | int]):
        db = self.runners
        values = []
        keys = []
        for key, value in user.items():
            if key in ("flag", "id", "name"):
                continue
            keys.append(f"{key} = ?")
            values.append(value)
        keys_str = ", ".join(keys)
        values.append(user["id"])
        db.execute_commit(
            f"""
                UPDATE users 
                SET {keys_str}
                WHERE id = ?
            """,
            tuple(values),
        )

    def close(self):
        self.runners.close()
        self.public.close()


class Database:
    def __init__(self, name):
        self.name = name
        self.connection = sqlite3.connect(f"./database/{name}.db")
        self.cursor = self.connection.cursor()

    def execute_commit(self, query, values):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"{values} already exists in {self.name}.db.")

    def close(self):
        self.connection.close()
