import os, sys
sys.path.insert(0,"../")
from .utils import *
from components.objects import Pipeline


def create_pipeline(kvstore, cursor, sess_table, pipeline_name):
    success = False
    current_sess = kvstore.get("session", None)
    if current_sess != None:
        sess_dir = get_session_dir(cursor, current_sess, sess_table)
        pipe_dir = "%s/datawand/pipelines/" % sess_dir
        pipe_obj = Pipeline(pipeline_name, pipe_dir, "") 
        if not os.path.exists(pipe_obj.path):
            pipe_obj.save()
            success = True
        else:
            print("Pipeline already exists!")
    else:
        print("No active session was found. First, you must activate a session!")
    return success
      
def remove_pipeline(kvstore, cursor, sess_table, pipeline_name):
    success = False
    current_sess = kvstore.get("session", None)
    if current_sess != None:
        sess_dir = get_session_dir(cursor, current_sess, sess_table)
        pipeline_wout_extension = pipeline_name.replace(".json","")
        f_name = "%s/datawand/pipelines/%s.json" % (sess_dir, pipeline_wout_extension)
        if os.path.exists(f_name):
            os.remove(f_name)
            success = True
        else:
            print("Pipeline does not exists!")
    else:
        print("No active session was found. First, you must activate a session!")
    return success

def list_pipeline(kvstore, cursor, sess_table):
    cnt = 0
    current_sess = kvstore.get("session", None)
    if current_sess != None:
        sess_dir = get_session_dir(cursor, current_sess, sess_table)
        pipe_dir = sess_dir+"/datawand/pipelines"
        print(pipe_dir)
        pipes = os.listdir(pipe_dir)
        print(pipes)
        cnt = len(pipes)
    else:
        print("No active session was found. First, you must activate a session!")
    return cnt