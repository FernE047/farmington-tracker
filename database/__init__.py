import sqlite3


class Database_Manager:
    def __init__(self):
        self.private = Database("private")
        self.public = Database("public")

    def add_user(self, user):
        self.private.execute_commit(
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
        for db in (self.private, self.public):
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
        for db in (self.private, self.public):
            db.execute_commit(
                """
                ALTER TABLE users
                ADD COLUMN ? TEXT DEFAULT ?;
            """,
                (column_name, default_value),
            )
        print(f"Column {column_name} added in both databases.")

    def update_values(self, user: dict[str, str | int]):
        db = self.private
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
        self.private.close()
        self.public.close()


class Database:
    def __init__(self, name):
        self.name = name
        self.connection = sqlite3.connect(f"./database/{name}.db")
        self.cursor = self.connection.cursor()
        self._filters = {}
        self._data_iter = None

    def filter_by(self, **kwargs):
        # Save the filter parameters
        self._filters = kwargs
        self._data_iter = None  # Reset iterator

    def execute_commit(self, query, values):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"{values} already exists in {self.name}.db.")

    def fetch_all(self):
        query = "SELECT id, flag, name FROM users"
        params = []

        if self._filters:
            where_clauses = []
            for column, value in self._filters.items():
                where_clauses.append(f"{column} = ?")
                params.append(value)
            query += " WHERE " + " AND ".join(where_clauses)
        print()
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        self._data_iter = iter(
            [{"id": row[0], "flag": row[1], "name": row[2]} for row in rows]
        )

    def __iter__(self):
        if self._data_iter is None:
            self.fetch_all()
        return self

    def __next__(self):
        if self._data_iter is None:
            raise StopIteration
        return next(self._data_iter)

    def close(self):
        self.connection.close()


db = Database_Manager()
db.public.filter_by(flag="flag_br")
for a in db.public:
    print(a)
