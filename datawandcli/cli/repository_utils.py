import os
from shutil import rmtree
from .utils import *

def validate(cursor, repo_name, repo_path, repo_table):
    rows = fetch_table(cursor, repo_table)
    for name, path, _ in rows:
        if name == repo_name:
            raise RuntimeError("Provide a unique repository name!")
        if repo_path in path or path in repo_path:
            raise RuntimeError("Repository paths cannot contain each other!")

def create_repo(connection, cursor, repo_table, repo_name=None):
    cwd = os.getcwd()
    if repo_name == None:
        repo_name = cwd.split("/")[-1]
    validate(cursor, repo_name, cwd, repo_table)
    cursor.execute('INSERT INTO %s VALUES (?,?,CURRENT_TIMESTAMP)' % repo_table, (repo_name, cwd))
    connection.commit()
    return get_repo(cursor, cwd, repo_table)[0] != None

def list_repos(cursor, repo_table):
    return fetch_table(cursor, repo_table)

def remove_repo(connection, cursor, repo_table, repo_name=None):
    old_length = len(fetch_table(cursor, repo_table))
    if repo_name != None:
        cursor.execute('DELETE FROM %s WHERE name=?' % repo_table, (repo_name,))
        connection.commit()
    else:
        raise RuntimeError("The name of the repository must be provided!")
    return old_length-1 == len(fetch_table(cursor, repo_table))

def status_repo(cursor, repo_table):
    success = False
    cwd = os.getcwd()
    repo_name, repo_path = get_repo(cursor, cwd, repo_table)
    if repo_name == None:
        print(NO_DW_MSG)
    else:
        pipelines, experiments = collect_config_files(repo_path)
        print("### General information ###")
        print("Name: %s" % repo_name)
        print("Base folder: %s" % repo_path)
        print("Number of pipelines: %i" % len(pipelines))
        print("Number of experiments: %i" % len(experiments))
        print("### Pipelines ###")
        success = list_pipelines(cursor, repo_table)
        print("### Experiments with status ###")
        success = list_experiments(cursor, repo_table)
    return success