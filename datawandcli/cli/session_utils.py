import os
from shutil import rmtree
from .utils import *

def create_session(connection, cursor, table_name, sess_name):
    cwd = os.getcwd()
    cursor.execute('INSERT INTO %s VALUES (?,?)' % table_name, (sess_name, cwd))
    connection.commit()
    return get_session_dir(cursor, sess_name, table_name) != None

def remove_session(connection, cursor, table_name, sess_name):
    sess_dir = get_session_dir(cursor, sess_name, table_name)
    cursor.execute('DELETE FROM %s WHERE name=?' % table_name, (sess_name,))
    connection.commit()
    rmtree(sess_dir+"/datawand")
    return get_session_dir(cursor, sess_name, table_name) == None
    
def list_sessions(cursor, table_name):
    return fetch_table(cursor, table_name)

def get_session_dir(cursor, sess_name, table_name):
    dir_map = dict(fetch_table(cursor, table_name))
    sess_dir = dir_map.get(sess_name, None)
    if sess_dir != None and not "datawand" in os.listdir(sess_dir):
        os.makedirs(sess_dir + "/datawand/pipelines")
        os.makedirs(sess_dir + "/datawand/experiments")
    return sess_dir