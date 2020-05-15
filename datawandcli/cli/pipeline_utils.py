import os, json
from .utils import *
from .repository_utils import get_repo, NO_DW_MSG
from datawandcli.components.objects import Pipeline

def create_pipeline(cursor, repo_table, name, description=""):
    success = False
    cwd = os.getcwd()
    repo_name, repo_path = get_repo(cursor, cwd, repo_table)
    if repo_name != None:
        file_path = "%s/%s.json" % (repo_path, name)
        pipe_obj = Pipeline(name, description) 
        if os.path.exists(file_path):
            print("A Pipeline with the same name already exists!")
        else:
            pipe_obj.save(repo_path)
            print("A new pipeline was created")
            print("Configuration file at: %s" % file_path)
            success = True
    else:
        print(NO_DW_MSG)
    return success

def remove_pipeline(cursor, repo_table, file_path):
    success = False
    if ".json" in file_path:
        os.remove(file_path)
        success = True
        print("The pipeline was deleted")
    else:
        print("You must provide a JSON file!")
    return success

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