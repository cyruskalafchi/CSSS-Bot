import sqlite3

CREATE_USERPOINTS = "CREATE TABLE IF NOT EXISTS userpoints (id INTEGER PRIMARY KEY, user INTEGER, points INTEGER);"
INSERT_USERPOINTS = "INSERT INTO userpoints (user, points) VALUES (?, ?);"
GET_ALL_USERPOINTS = "SELECT * FROM userpoints;"
GET_USERPOINTS_BY_USER = "SELECT * FROM userpoints WHERE user = ?;"
GET_TOP_USERS = """
SELECT * FROM userpoints
ORDER BY points DESC
LIMIT 5;
"""
UPDATE_USERPOINTS = "UPDATE userpoints SET points = ? WHERE user = ?"

def connect():
    return sqlite3.connect("data.db")

def create_tables(connection):
    with connection:
        connection.execute(CREATE_USERPOINTS)

def add_userpoints(connection, user, points):
    with connection:
        connection.execute(INSERT_USERPOINTS, (user, points))

def get_all_userpoints(connection):
    with connection:
        return connection.execute(GET_ALL_USERPOINTS).fetchall()

def get_userpoints_by_user(connection, user):
    with connection:
        return connection.execute(GET_USERPOINTS_BY_USER, (user,)).fetchone()

def get_top_users(connection):
    with connection:
        return connection.execute(GET_TOP_USERS).fetchall()

def update_userpoints(connection, points, user):
    with connection:
        connection.execute(UPDATE_USERPOINTS, (points, user))

