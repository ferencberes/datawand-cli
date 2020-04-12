import sqlite3, os
from os.path import expanduser
from sqlitedict import SqliteDict

def prepare_environment(session_table, postfix=""):
    home_dir = expanduser("~")
    config_dir = "%s/.datawandlite" % home_dir
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    db_path = "%s/dwlite%s.db" % (config_dir, postfix)
    kv_path = "%s/kvstore%s.db" % (config_dir, postfix)
    conn = sqlite3.connect(db_path)
    kvstore = SqliteDict(kv_path, autocommit=True)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS %s (name text NOT NULL UNIQUE, path text NOT NULL UNIQUE)" %session_table)
    return conn, c, kvstore

def fetch_table(cursor, table_name):
    cursor.execute("SELECT * FROM %s" % table_name)
    rows = cursor.fetchall()
    return rows

def show_table(cursor, table_name):
    rows = fetch_table(cursor, table_name)
    if len(rows) > 0:
        for row in rows:
            print(row)
    else:
        print("No instances were found")

def get_session_dir(cursor, sess_name, table_name):
    dir_map = dict(fetch_table(cursor, table_name))
    return dir_map.get(sess_name, None)