import os
from cli.utils import *
from cli.session_utils import *

home_dir = expanduser("~")
config_dir = "%s/.datawandlite" % home_dir
db_path = "%s/dwlite_test.db" % config_dir
kv_path = "%s/kvstore_test.db" % config_dir
if os.path.exists(db_path):
    os.remove(db_path)
if os.path.exists(kv_path):
    os.remove(kv_path)

class TestSession:
    def test_single_create(self):
        sess_table = "sessions"
        sess_name = "trial"
        conn, c, kvstore = prepare_environment(sess_table, postfix="_test")
        assert create_session(conn, c, sess_table, sess_name)
        
    def test_list(self):
        sess_table = "sessions"
        conn, c, kvstore = prepare_environment(sess_table, postfix="_test")
        assert len(list_sessions(c, sess_table)) == 1
        
    def test_single_remove(self):
        sess_table = "sessions"
        sess_name = "trial"
        conn, c, kvstore = prepare_environment(sess_table, postfix="_test")
        success = remove_session(conn, c, sess_table, sess_name)
        size = len(list_sessions(c, sess_table))
        print(success, size)
        assert success and (size == 0)
