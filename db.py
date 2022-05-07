import sqlite3
from sqlite3 import Error

DBPATH = "./database/database.db"

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

def create_vent_table(connection):
    if connection is not None:
        try:
            query = """
                CREATE TABLE IF NOT EXISTS vent (
                    id INTEGER PRIMARY KEY,
                    device VARCHAR NOT NULL DEFAULT '',
                    value FLOAT NOT NULL DEFAULT 0
                );
            """
            cursor = connection.cursor()
            cursor.execute(query)
        except Error as e:
            print(e)
    else:
        print("Invalid connection")
        exit()

def add_vent(connection, device, value):
    if connection is not None:
        try:
            query = """
                INSERT INTO vent(device, value)
                VALUES(?, ?);
            """
            cursor = connection.cursor()
            cursor.execute(query, (device, value))
            connection.commit()
        except Error as e:
            print(e)
    else:
        print("Invalid connection")
        exit()  

def get_device_vent(connection, device):
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT value FROM vent WHERE device = ? ORDER BY id DESC LIMIT 1;", (device, ))
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)
    else:
        print("Invalid connection")
        exit()    

def add_temp(connection, device, temp, detection_time):
    if connection is not None:
        try:
            query = """
                INSERT INTO temp(device, value, time)
                VALUES(?, ?, ?);
            """
            cursor = connection.cursor()
            cursor.execute(query, (device, temp, detection_time))
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
            cursor.execute("SELECT * FROM temp WHERE device = ?;", (device, ))
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)
    else:
        print("Invalid connection")
        exit()

def get_device_temp_ord(connection, device, limit=-1):
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT value, time from temp WHERE device = ? ORDER BY time DESC LIMIT ?", (device, limit))
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)
    else:
        print("Invalid connection")
        exit()

def get_last_temp(connection):
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT device, value, MAX(time) FROM temp GROUP BY device;")
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)
    else:
        print("Invalid connection")
        exit()

def remove_vent(connection):
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM vent;")
            connection.commit()
        except Error as e:
            print(e)
    else:
        print("Invalid connection")
        exit()