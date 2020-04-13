import os
from shutil import rmtree
from .utils import *

def get_session_dir(cursor, sess_name, table_name):
    dir_map = dict(fetch_table(cursor, table_name))
    sess_dir = dir_map.get(sess_name, None)
    if sess_dir != None and not "datawand" in os.listdir(sess_dir):
        os.makedirs(sess_dir + "/datawand/pipelines")
        os.makedirs(sess_dir + "/datawand/experiments")
    return sess_dir

def create_session(connection, cursor, table_name, sess_name):
    cwd = os.getcwd()
    cursor.execute('INSERT INTO %s VALUES (?,?)' % table_name, (sess_name, cwd))
    connection.commit()
    return get_session_dir(cursor, sess_name, table_name) != None

def remove_session(kvstore, connection, cursor, table_name, sess_name):
    current_sess = kvstore.get("session", None)
    if current_sess == sess_name:
        deactivate_session(kvstore)
    sess_dir = get_session_dir(cursor, sess_name, table_name)
    cursor.execute('DELETE FROM %s WHERE name=?' % table_name, (sess_name,))
    connection.commit()
    rmtree(sess_dir+"/datawand")
    return get_session_dir(cursor, sess_name, table_name) == None
    
def list_sessions(cursor, table_name):
    return fetch_table(cursor, table_name)

def activate_session(kvstore, sess_name):
    kvstore["session"] = sess_name
    kvstore.commit()
    print("Session '%s' was activated." % sess_name)

def deactivate_session(kvstore):
    current_sess = kvstore.get("session", None)
    if current_sess != None:
        del kvstore["session"]
        kvstore.commit()
        print("Session '%s' was deactivated." % current_sess)
    else:
        print("No active session was found.")
        
def status_session(kvstore, cursor, table_name):
    current_sess = kvstore.get("session", None)
    num_pipes, num_exps = 0, 0
    if current_sess != None:
        print("Session '%s' is currently active." % current_sess)
        sess_dir = get_session_dir(cursor, current_sess, table_name)
        num_pipes = len(os.listdir(sess_dir+"/datawand/pipelines"))
        num_exps = len(os.listdir(sess_dir+"/datawand/experiments"))
        print("Number of pipelines in this session: %i" % num_pipes)
        print("Number of pipelines in this session: %i" % num_exps)
    else:
        print("No active session was found.")
    return current_sess, num_pipes, num_exps
    