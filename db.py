import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    print("<DB> Creating connection with db")
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except Error as e:
        print(e)

def create_temp_table(connection):
    if connection is not None:
        try:
            query = """
                CREATE TABLE IF NOT EXISTS temp (
                    id INTEGER PRIMARY KEY,
                    device VARCHAR NOT NULL DEFAULT '',
                    value FLOAT NOT NULL DEFAULT 0,
                    time INTEGER NOT NULL DEFAULT 0
                );
            """
            cursor = connection.cursor()
            cursor.execute(query)
        except Error as e:
            print(e)
    else:
        print("Invalid connection")
        exit()

def add_temp(connection, device, temp, time):
    if connection is not None:
        try:
            query = """
                INSERT INTO temp(device, value, time)
                VALUES(?, ?, ?);
            """
            cursor = connection.cursor()
            cursor.execute(query, (device, temp))
            connection.commit()
        except Error as e:
            print(e)
    else:
        print("Invalid connection")
        exit()

def get_all_temp(connection):
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM temp;")
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)
    else:
        print("Invalid connection")
        exit()

def get_device_temp(connection, device):
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user WHERE device = ?;", (device, ))
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)
    else:
        print("Invalid connection")
        exit()