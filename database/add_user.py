from database import Database_Manager


db = Database_Manager()
user = {"id": "user123", "name": "Abraham Lincoln", "flag": ":gb:"}
db.add_user(user)

# TODO, turn this into a function, input the user_id and get information using the api and then add in the database
