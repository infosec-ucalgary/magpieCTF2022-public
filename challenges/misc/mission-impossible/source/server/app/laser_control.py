import sqlite3
import uuid
import time
from os import path
from flask import jsonify, Blueprint

DB_PATH = "database.db"
SCHEMA_FILE = "schema.sql"
FLAG = "magpie{ju5t_w0rm_4r0und_th3_la53r5}"

ALLOWED_ATTEMPTS = 5
ATTEMPT_PERIOD = 3600 # s.

# These IPs are not subject to the cooldown.
ALLOWED_IPS = [
    "127.0.0.1",
    "172.17.0.1",       # Alpine bridge
    "184.64.207.141",   # Jeremy
    "68.146.23.104",    # Alex
    "104.205.180.44"    # James
]

def init():
    create_db()

def create_db():
    full_path = path.dirname(path.abspath(__file__)) + "/" + SCHEMA_FILE
    con, cursor = connect_db()

    with open(full_path, "r") as fp:
        cursor.executescript(fp.read())
    
    con.commit()
    con.close()

def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return (connection, connection.cursor())

def clean_data(list_of_lasers):
    var0 = not "laser0" in list_of_lasers
    var1 = not "laser1" in list_of_lasers
    var2 = not "laser2" in list_of_lasers
    var3 = not "laser3" in list_of_lasers

    return (var0, var1, var2, var3)

def shutdown_lasers(list_of_lasers, request):
    remote_addr = request.remote_addr

    # Check if being sent by solve script.
    ignore_lasers = 'Ignore-Lasers' in request.headers and request.headers['Ignore-Lasers'] == "true"

    clean = clean_data(list_of_lasers)

    if not 0 in clean:
        return "You didn't shut down any of the lasers.\n"

    request_allowed, time_remaining, attempts_remaining = (True, -1, 999)
    if not remote_addr in ALLOWED_IPS and not ignore_lasers:
        request_allowed, time_remaining, attempts_remaining = check_request(remote_addr)

    if request_allowed and not ignore_lasers:
        insert_request(clean)

    ret_value = "You shut down " + str((not clean[0]) + (not clean[1]) + (not clean[2]) + (not clean[3])) + " of 4 lasers!\n"

    if not True in (clean[0], clean[1], clean[2], clean[3]):
        ret_value += "\n" + FLAG + "\n"

    if ignore_lasers:
        return ret_value

    if request_allowed:
        if attempts_remaining != 0:
            ret_value += f"\nYour IP can only shut off the laser video stream {attempts_remaining} more time(s) this hour.\n"
        else:
            ret_value += f"\nYou've shut off the video laser stream {ALLOWED_ATTEMPTS} times this hour.\n"
            ret_value += f"Cooldown remaining: {time.strftime('%H:%M:%S', time.gmtime(ATTEMPT_PERIOD - time_remaining))}\n"

    else:
        ret_value += f"\nSorry, your IP can only shut off the laser video stream {ALLOWED_ATTEMPTS} times per hour.\n"
        ret_value += f"Cooldown remaining: {time.strftime('%H:%M:%S', time.gmtime(ATTEMPT_PERIOD - time_remaining))}\n"

    return ret_value

def check_request(remote_addr):
    conn, cur = connect_db()
    cur.execute("SELECT First_time, Attempts FROM Connections WHERE IP=?;", (remote_addr,))
    data = cur.fetchone()

    # First time connecting.
    if not data:
        cur.execute("INSERT INTO Connections VALUES (?, ?, ?);", (remote_addr, int(time.time()), 1))
        conn.commit()
        conn.close()
        return (True, None, ALLOWED_ATTEMPTS - 1)

    # Less than an hour has elapsed.
    delta_t = int(time.time()) - data["First_time"]
    if delta_t < ATTEMPT_PERIOD:
        # Increment attempts by one.
        if data["Attempts"] < ALLOWED_ATTEMPTS:
            cur.execute("UPDATE Connections SET Attempts = Attempts + 1 WHERE IP=?;", (remote_addr,))
            conn.commit()
            conn.close()
            return (True, delta_t, ALLOWED_ATTEMPTS - data["Attempts"] - 1)

        # Too many attempts.
        else:
            conn.close()
            return (False, delta_t, None)

    # An hour has elapsed, reset the state.
    else:
        cur.execute("UPDATE Connections SET First_time = ?, Attempts = 1 WHERE IP=?;", (int(time.time()), remote_addr))
        conn.commit()
        conn.close()
        return (True, delta_t, ALLOWED_ATTEMPTS - 1)

def insert_request(clean):
    conn, cur = connect_db()
    cur.execute("INSERT INTO Requests VALUES (?,?,?,?,?,?);",
        (
            str(uuid.uuid1()), 
            time.time(), 
            clean[0], 
            clean[1], 
            clean[2], 
            clean[3]
        )
    )
    conn.commit()
    conn.close()

laser_bp = Blueprint("laser_bp", __name__)
@laser_bp.route('/7ETfKgw4NYND9JMStKNVuSpjLDCB6y/laser-state', methods=['GET'])
def pi_get():
    conn, cur = connect_db()
    cur.execute("SELECT * FROM Lasers;")
    data = cur.fetchall()
    conn.close()
    return jsonify([dict(e) for e in data])
