import os
from shutil import rmtree
from .utils import *

def get_repo_name(cursor, path, table_name):
    name = None
    rows = fetch_table(cursor, table_name)
    for repo_name, repo_path, _ in rows:
        if repo_path in path:
            name = repo_name
            break
    return name

def get_repo_path(cursor, name, table_name):
    path = None
    rows = fetch_table(cursor, table_name)
    for repo_name, repo_path, _ in rows:
        if repo_name == name:
            path = repo_path
            break
    return path

def validate(cursor, repo_name, repo_path, table_name):
    rows = fetch_table(cursor, table_name)
    for name, path, _ in rows:
        if name == repo_name:
            raise RuntimeError("Provide a unique repository name!")
        if repo_path in path or path in repo_path:
            raise RuntimeError("Repository paths cannot contain each other!")

def create_repo(connection, cursor, table_name, repo_name=None):
    cwd = os.getcwd()
    if repo_name == None:
        repo_name = cwd.split("/")[-1]
    validate(cursor, repo_name, cwd, table_name)
    cursor.execute('INSERT INTO %s VALUES (?,?,CURRENT_TIMESTAMP)' % table_name, (repo_name, cwd))
    connection.commit()
    return get_repo_name(cursor, cwd, table_name) != None

def list_repos(cursor, table_name):
    return fetch_table(cursor, table_name)

def remove_repo(connection, cursor, table_name, repo_name=None, repo_path=None):
    old_length = len(fetch_table(cursor, table_name))
    if repo_name != None:
        cursor.execute('DELETE FROM %s WHERE name=?' % table_name, (repo_name,))
        connection.commit()
    elif repo_path != None:
        if "/" == repo_path[-1]:
            repo_path = repo_path[:-1]
        cursor.execute('DELETE FROM %s WHERE path=?' % table_name, (repo_path,))
        connection.commit()
    else:
        raise RuntimeError("The name or the absolute path of the repository must be provided!")
    return old_length-1 == len(fetch_table(cursor, table_name))

def status_repo(cursor, table_name):
    cwd = os.getcwd()
    repo_name = get_repo_name(cursor, cwd, table_name)
    if repo_name == None:
        print("Datawand was not enabled for your current folder!")
    else:
        repo_path = get_repo_path(cursor, repo_name, table_name)
        num_json = 0
        for file in os.listdir(repo_path):
            if ".json" in file:
                num_json += 1
        print("### Datawand repository information ###")
        print("Name: %s" % repo_name)
        print("Base folder: %s" % repo_path)
        print("Number of pipelines: %i" % num_json)
    return repo_name, num_json