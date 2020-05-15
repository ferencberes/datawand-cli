import os
"""
from datawandcli.cli.utils import *
from datawandcli.cli.session_utils import *
from datawandcli.cli.pipeline_utils import *

home_dir = expanduser("~")
config_dir = "%s/.datawandlite" % home_dir
db_path = "%s/dwlite_test.db" % config_dir
kv_path = "%s/kvstore_test.db" % config_dir
if os.path.exists(db_path):
    os.remove(db_path)
if os.path.exists(kv_path):
    os.remove(kv_path)

def test_single_create():
    sess_table, sess_name = "sessions", "trial"
    conn, c, kvstore = prepare_environment(sess_table, postfix="_test")
    assert create_session(conn, c, sess_table, sess_name)

def test_list():
    sess_table = "sessions"
    conn, c, kvstore = prepare_environment(sess_table, postfix="_test")
    assert len(list_sessions(c, sess_table)) == 1

def test_activation():
    sess_table, sess_name = "sessions", "trial"
    conn, c, kvstore = prepare_environment(sess_table, postfix="_test")
    activate_session(kvstore, sess_name)
    current_sess, num_pipes, num_exps = status_session(kvstore, c, sess_table)
    assert (current_sess == sess_name) and (num_pipes == 0) and (num_exps == 0)
    
def test_create_pipeline():
    sess_table, pipe_name = "sessions", "pipe1"
    conn, c, kvstore = prepare_environment(sess_table, postfix="_test")
    assert create_pipeline(kvstore, c, sess_table, pipe_name)
    
#def test_list_pipeline():
#    sess_table = "sessions"
#    conn, c, kvstore = prepare_environment(sess_table, postfix="_test")
#    cnt = list_pipeline(kvstore, c, sess_table)
#    assert cnt == 1
    
def test_remove_pipeline():
    sess_table, pipe_name = "sessions", "pipe1"
    conn, c, kvstore = prepare_environment(sess_table, postfix="_test")
    success = remove_pipeline(kvstore, c, sess_table, pipe_name)
    cnt = list_pipeline(kvstore, c, sess_table)
    assert success and cnt == 0
    
def test_deactivation():
    sess_table = "sessions"
    conn, c, kvstore = prepare_environment(sess_table, postfix="_test")
    deactivate_session(kvstore)
    current_sess, _, _ = status_session(kvstore, c, sess_table)
    assert current_sess == None

def test_single_remove():
    sess_table, sess_name = "sessions", "trial"
    conn, c, kvstore = prepare_environment(sess_table, postfix="_test")
    success = remove_session(kvstore, conn, c, sess_table, sess_name)
    size = len(list_sessions(c, sess_table))
    print(success, size)
    assert success and (size == 0)
"""