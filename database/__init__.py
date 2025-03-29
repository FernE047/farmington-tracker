import sqlite3
from typing import Any, Iterator, Optional, Self

from common.type_def import UserDatabaseData


class Database_Manager:
    def __init__(self) -> None:
        self.private = Database("private")
        self.public = Database("public")

    def add_user(self, user: UserDatabaseData) -> None:
        self.private.execute_commit(
            """
            INSERT INTO users (id, name, flag, Large_20k) 
            VALUES (?, ?, ?, ?)
        """,
            [user["id"], user["name"], user["flag"], False],
        )
        self.public.execute_commit(
            """
            INSERT INTO users (id, name, flag) 
            VALUES (?, ?, ?)
        """,
            [user["id"], user["name"], user["flag"]],
        )

    def update_user(self, user: UserDatabaseData) -> None:
        for db in (self.private, self.public):
            db.execute_commit(
                """
                UPDATE users 
                SET name = ?, flag = ?
                WHERE id = ?
            """,
                [user["name"], user["flag"], user["id"]],
            )
        print(f"User {user['id']} updated in both databases.")

    def new_column(self, column_name: str, default_value: Any) -> None:
        for db in (self.private, self.public):
            db.execute_commit(
                """
                ALTER TABLE users
                ADD COLUMN ? TEXT DEFAULT ?;
            """,
                [column_name, default_value],
            )
        print(f"Column {column_name} added in both databases.")

    def update_values(self, user: dict[str, str | int]) -> None:
        db = self.private
        values: list[str | int] = []
        keys: list[str] = []
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
            values,
        )

    def close(self):
        self.private.close()
        self.public.close()


class Database:
    def __init__(self, name: str) -> None:
        self.name = name
        self.connection = sqlite3.connect(f"./database/{name}.db")
        self.cursor = self.connection.cursor()
        self._filters: dict[str, Any] = {}
        self._data_iter: Optional[Iterator[dict[str, Any]]] = None

    def filter_by(self, **kwargs: Any) -> None:
        self._filters = kwargs
        self._data_iter = None

    def execute_commit(self, query: str, values: list[Any]) -> None:
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"{values} already exists in {self.name}.db.")

    def fetch_all(self) -> None:
        query = "SELECT * FROM users"
        params: list[Any] = []

        if self._filters:
            where_clauses: list[str] = []
            for column, value in self._filters.items():
                where_clauses.append(f"{column} = ?")
                params.append(value)
            query += " WHERE " + " AND ".join(where_clauses)

        self.cursor.execute(query, params)
        column_names = [desc[0] for desc in self.cursor.description]
        rows = self.cursor.fetchall()
        self._data_iter = iter([dict(zip(column_names, row)) for row in rows])

    def __iter__(self) -> Self:
        if self._data_iter is None:
            self.fetch_all()
        return self

    def __next__(self) -> dict[str, Any]:
        if self._data_iter is None:
            raise StopIteration
        return next(self._data_iter)

    def close(self) -> None:
        self.connection.close()
