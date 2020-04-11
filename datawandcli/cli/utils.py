import sqlite3, os

def init_tables(config_dir, instances_table):
    db_path = "%s/dwlite.db" % config_dir
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS %s (name text NOT NULL UNIQUE, path text NOT NULL UNIQUE)" % instances_table)
    return conn, c, db_path

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

def get_instance_dir(cursor, instance_name, table_name):
    dir_map = dict(fetch_table(cursor, table_name))
    return dir_map.get(instance_name, None)
        
def handle_instance_request(args, connection, cursor, table_name):
    if args.action in ["create","remove"]:
        inst_name = args.name
        if inst_name == None:
            print("Provide an instance name!")
        else:
            if args.action == "create":
                cwd = os.getcwd()
                cursor.execute('INSERT INTO %s VALUES (?,?)' % table_name, (inst_name, cwd))
            else:
                cursor.execute('DELETE FROM %s WHERE name=?' % table_name, (inst_name,))
            connection.commit()
    show_table(cursor, table_name)