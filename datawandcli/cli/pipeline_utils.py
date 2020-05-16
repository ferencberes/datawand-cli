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

def copy_pipeline(file_path, new_name, delim="/"):
    success = False
    if file_path == None:
        print("Provide path for the config file to be copied")
    elif new_name == None:
        print("Provide name for the new pipeline")
    else:
        is_valid, _ = validate_config_json(file_path)
        if is_valid:
            pipe_obj = Pipeline()
            pipe_obj.load(file_path, experiment_name=new_name)
            pipe_obj.name = new_name
            pipe_folder = delim.join(file_path.split(delim)[:-1])
            pipe_obj.save(pipe_folder)
            success = True
    return success

def view_pipeline(file_path, object_name):
    success = False
    is_valid, _ = validate_config_json(file_path)
    if is_valid:
        pipe_obj = Pipeline()
        pipe_obj.load(file_path)
        if object_name == None:
            print("Name:", pipe_obj.name)
            print("Namespace:", pipe_obj.experiment_name)
            bd = pipe_obj.base_dir
            if len(bd) > 0:
                print("Base directory:", bd)
            desc = pipe_obj.description
            if len(desc) > 0:
                print("Description:", desc)
            cfg = pipe_obj.default_config
            if len(cfg) > 0:
                print("Parameters:")
                print(cfg)
            mod_names = [item.name for item in pipe_obj.modules]
            if len(mod_names) > 0:
                print("Modules:", mod_names)
            nb_names = [item.name for item in pipe_obj.notebooks]
            if len(nb_names) > 0:
                print("Notebooks:", nb_names)
            ps_names = [item.name for item in pipe_obj.pyscripts]
            if len(ps_names) > 0:
                print("Python scripts:", ps_names)
        else:
            print("Name:", pipe_obj.parts[object_name].name)
            obj_type = pipe_obj.parts[object_name].type
            if len(obj_type) > 0:
                print("Type:", obj_type)
            print("Path:", pipe_obj.parts[object_name].path)
            cfg = pipe_obj.default_config.copy()
            cfg.update(pipe_obj.parts[object_name].config)
            if len(cfg) > 0:
                print("Parameters:")
                print(cfg)
        success = True
    return success

def remove_pipeline(file_path):
    success = False
    if ".json" in file_path:
        os.remove(file_path)
        success = True
    else:
        print("You must provide a JSON file!")
    return success

