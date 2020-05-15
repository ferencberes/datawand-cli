import sqlite3, os
import pandas as pd
from os.path import expanduser
from sqlitedict import SqliteDict

def prepare_environment(repo_table, postfix=""):
    home_dir = expanduser("~")
    config_dir = "%s/.datawandcli" % home_dir
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    db_path = "%s/repositories%s.db" % (config_dir, postfix)
    kv_path = "%s/kvstore%s.db" % (config_dir, postfix)
    conn = sqlite3.connect(db_path)
    kvstore = SqliteDict(kv_path, autocommit=True)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS %s (name text NOT NULL UNIQUE, path text NOT NULL UNIQUE, created_at timestamp)" % repo_table)
    return conn, c, kvstore

def fetch_table(cursor, table_name):
    cursor.execute("SELECT * FROM %s" % table_name)
    rows = cursor.fetchall()
    return rows

def show_repo_table(rows):
    if len(rows) > 0:
        df = pd.DataFrame(rows, columns=["name","path","created_at"])
        df = df.sort_values("created_at", ascending=False).reset_index(drop=True)
        print(df)
    else:
        print("No instances were found")