import sqlite3, os
import pandas as pd
from os.path import expanduser
from datawandcli.components.objects import Pipeline

### messages ###

NO_DW_MSG = "Datawand was not enabled for your current folder!"
PATH_MSG = "Provide path for pipeline json file"
REPO_NAME_MSG = "Provide repository name"

### database ###

def prepare_environment(repo_table, postfix=""):
    home_dir = expanduser("~")
    config_dir = "%s/.datawandcli" % home_dir
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    db_path = "%s/repositories%s.db" % (config_dir, postfix)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS %s (name text NOT NULL UNIQUE, path text NOT NULL UNIQUE, created_at timestamp)" % repo_table)
    return conn, c

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