from jinja2 import Template
from .utils import *
import os

nb_str = """
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Load parameters"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "import sys\n",
    "from datawand.parametrization import ParamHelper"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "ph = ParamHelper('{{ rel_path }}', '{{ pipeline_name }}', sys.argv)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:py3]",
   "language": "python",
   "name": "conda-env-py3-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
"""

def create_pipeline(kvstore, cursor, sess_table, pipeline_name):
    success = False
    current_sess = kvstore.get("session", None)
    if current_sess != None:
        sess_dir = get_session_dir(cursor, current_sess, sess_table)
        template = Template(nb_str)
        rendered = template.render(rel_path="./", pipeline_name=pipeline_name)
        f_name = "%s/datawand/pipelines/%s.ipynb" % (sess_dir, pipeline_name)
        if not os.path.exists(f_name):
            with open(f_name, 'w') as f:
                f.write(rendered)
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
        pipeline_wout_extension = pipeline_name.replace(".ipynb","")
        f_name = "%s/datawand/pipelines/%s.ipynb" % (sess_dir, pipeline_wout_extension)
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