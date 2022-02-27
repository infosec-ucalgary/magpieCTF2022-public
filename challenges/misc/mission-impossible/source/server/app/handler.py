import time
import sqlite3
import os

DB_PATH = "database.db"

# How long to wait after reseting laser status to default.
RESET_TIME = 1

# How long to hold laser status after processing request.
SLEEP_TIME = 5

# How long to wait before retrying sqlite initialization.
ERROR_TIME = 10

def init():
    while not os.path.exists(DB_PATH):
        log("Waiting for database file to exist.")
        time.sleep(ERROR_TIME)
    
    log("Database file found.")

def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return (connection, connection.cursor())

def reset(conn, cur):

    cur.execute("UPDATE Lasers SET State=1 WHERE Name='Laser0';")
    cur.execute("UPDATE Lasers SET State=1 WHERE Name='Laser1';")
    cur.execute("UPDATE Lasers SET State=1 WHERE Name='Laser2';")
    cur.execute("UPDATE Lasers SET State=1 WHERE Name='Laser3';")
    
    conn.commit()

def update_lasers(data, conn, cur):
    cur.execute("UPDATE Lasers SET State=? WHERE Name='Laser0';", (data["Laser0"], ))
    cur.execute("UPDATE Lasers SET State=? WHERE Name='Laser1';", (data["Laser1"], ))
    cur.execute("UPDATE Lasers SET State=? WHERE Name='Laser2';", (data["Laser2"], ))
    cur.execute("UPDATE Lasers SET State=? WHERE Name='Laser3';", (data["Laser3"], ))
    
    cur.execute("DELETE FROM Requests;")
    
    conn.commit()

    log("Lasers updated with request.")

def main():
    log("Starting laser handler.")

    while True:
        init()
        
        while True:
            try:
                conn, cur = connect_db()
                reset(conn, cur)
                time.sleep(RESET_TIME)
                conn.close()

                conn, cur = connect_db()
                cur.execute("SELECT * FROM Requests ORDER BY Timestamp ASC LIMIT 1;")
                data = cur.fetchone()
                if data:
                    update_lasers(data, conn, cur)

                else:
                    reset(conn, cur)

                conn.close()

                time.sleep(SLEEP_TIME)
            except sqlite3.Error as e:
                log(f"Database connection error: {e}")
                time.sleep(ERROR_TIME)
                break

def log(data):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {data}")

if __name__ == "__main__":
    main()
