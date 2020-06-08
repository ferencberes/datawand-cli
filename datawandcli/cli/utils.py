import sqlite3, os, time, subprocess, psutil
import pandas as pd
from os.path import expanduser
from datawandcli.components.objects import Pipeline

def get_config_dir():
    home_dir = expanduser("~")
    config_dir = "%s/.datawandcli" % home_dir
    return config_dir

### messages ###

NO_DW_MSG = "Datawand was not enabled for your current folder!"
PATH_MSG = "Provide path for pipeline json file"
REPO_NAME_MSG = "Provide repository name"
EXP_PATH = "Provide path for experiment json file"

### luigi ###

def get_luigi_dir():
    config_dir = get_config_dir()
    return os.path.join(config_dir,"luigi")

def get_luigi_conf():
    return os.path.join(get_luigi_dir(), "luigi.cfg")

def create_luigi_cfg(luigi_dir, luigi_port, remove_sec, retry_sec):
    luigi_conf = get_luigi_conf()
    with open(luigi_conf, 'w') as f:
        f.write("""[core]
default-scheduler-port=%i

[scheduler]
remove-delay=%i
retry-delay=%i
""" % (luigi_port, remove_sec, retry_sec))
    return luigi_conf

def start_luigi(luigi_port=8082, remove_sec=3600, retry_sec=1800):
    luigi_dir = get_luigi_dir()
    if not os.path.exists(luigi_dir):
        os.makedirs(luigi_dir)
    log_dir = os.path.join(luigi_dir, "log")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    pid_file = os.path.join(log_dir,"luigi.pid")
    state_file = os.path.join(log_dir,"luigi-state.pickle")
    luigi_conf = create_luigi_cfg(luigi_dir, luigi_port, remove_sec, retry_sec)
    luigi_command = "export LUIGI_CONFIG_PATH=%s ; luigid --port=%i --pidfile %s --logdir %s --state-path %s" % (luigi_conf, luigi_port,  pid_file, log_dir, state_file)
    luigi_process = subprocess.Popen(luigi_command, shell=True, executable='/bin/bash')
    time.sleep(1)
    
def find_luigi(kill):
    success = False
    luigi_dir = get_luigi_dir()
    for p in psutil.process_iter():
        command = ' '.join(p.cmdline())
        if luigi_dir in command:
            print(command)
            if kill:
                p.terminate()
                p.wait()
            success = True
    if success:
        if kill:
            print("Scheduler was terminated")
    else:
        print("Scheduler was not found!")

### database ###

def prepare_environment(repo_table, postfix=""):
    config_dir = get_config_dir()
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    db_path = "%s/repositories%s.db" % (config_dir, postfix)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS %s (name text NOT NULL UNIQUE, path text NOT NULL UNIQUE, created_at timestamp)" % repo_table)
    return conn, c, config_dir

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
        
### files ###
        
def list_of_json_in_subfolders(root_dir):
    all_files = list()
    for (dirpath, dirnames, filenames) in os.walk(root_dir):
        all_files += [os.path.join(dirpath, file) for file in filenames if (".json" in file and "checkpoint." not in file)]
    return all_files

def validate_config_json(json_path):
    valid_json = False
    has_clones = False
    if not os.path.exists(json_path):
        raise FileNotFoundError(json_path)
    try:
        pipe = Pipeline()
        pipe.load(json_path)
        valid_json = True
        for obj in pipe.notebooks+pipe.pyscripts:
            if obj.is_clone:
                has_clones = True
                break
    finally:
        return valid_json, has_clones
    
def collect_config_files(repo_path):
    pipes, experiments = [], []
    json_files = list_of_json_in_subfolders(repo_path)
    for file in json_files:
        is_valid, has_clones = validate_config_json(file)
        if is_valid and not has_clones:
            pipes.append(file)
        if is_valid and has_clones:
            experiments.append(file)
    return pipes, experiments

### repositories ###

def get_repo_path(cursor, name, repo_table):
    path = None
    rows = fetch_table(cursor, repo_table)
    for repo_name, repo_path, _ in rows:
        if repo_name == name:
            path = repo_path
            break
    return path

def get_repo(cursor, path, repo_table):
    name = None
    rows = fetch_table(cursor, repo_table)
    for repo_name, repo_path, _ in rows:
        if repo_path in path:
            name = repo_name
            break
    return name, None if name == None else repo_path

### pipelines ###

def list_pipelines(cursor, repo_table):
    success = False
    cwd = os.getcwd()
    repo_name, repo_path = get_repo(cursor, cwd, repo_table)
    if repo_name != None:
        pipelines = collect_config_files(repo_path)[0]
        if len(pipelines) > 0:
            for config_path in pipelines:
                print(config_path)
        else:
            print("No pipeline was found!")
        success = True
    else:
        print(NO_DW_MSG)
    return success

### experiments ###

from datawandcli.cli.experiment_utils import experiment_status

def list_experiments(cursor, repo_table):
    success = False
    cwd = os.getcwd()
    repo_name, repo_path = get_repo(cursor, cwd, repo_table)
    if repo_name != None:
        experiments = collect_config_files(repo_path)[1]
        if len(experiments) > 0:
            for config_path in experiments:
                status, success_rate = experiment_status(cursor, repo_table, config_path)
                print("%s %s %s" % (config_path, status, success_rate))
        else:
            print("No experiment was found!")
        success = True
    else:
        print(NO_DW_MSG)
    return success