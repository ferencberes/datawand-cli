import os
from .utils import *
from .repository_utils import get_repo, NO_DW_MSG
from datawandcli.components.objects import *

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
            deps = pipe_obj.dependencies.get(object_name, [])
            if len(deps) > 0:
                print("Dependencies:", deps)
            else:
                print("No dependencies were set.")
            cfg = pipe_obj.default_config.copy()
            cfg.update(pipe_obj.parts[object_name].config)
            if len(cfg) > 0:
                print("Parameters:")
                print(cfg)
            else:
                print("No parameters were set.")
            
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

def infer_type(path):
    ext = path.split(".")[-1]
    if "ipynb" == ext:
        return "notebook"
    elif "py" == ext:
        return "pyscript"
    else:
        return "module"

# TODO: possible problem with object path handling
def add_component(pipeline_path, object_path, object_name=None, object_type=None):
    success = False
    is_valid, _ = validate_config_json(pipeline_path)
    if object_type == None:
        object_type = infer_type(object_path)
        print("Infered object type is: %s" % object_type)
    if is_valid:
        pipe_obj = Pipeline()
        pipe_obj.load(pipeline_path)
        if object_type == "notebook":
            new_obj = Notebook(object_path, object_name)
        elif object_type == "pyscript":
            new_obj = PyScript(object_path, object_name)
        else:
            new_obj = Module(object_path, object_name)
        if not new_obj.name in pipe_obj.parts and not os.path.exists(object_path):
            create_object(object_path, pipe_obj.name, object_type)
        pipe_obj.add(new_obj)
        pipe_obj.save()
        success = True
    return success

def remove_component(pipeline_path, object_name, with_source=False):
    success = False
    is_valid, _ = validate_config_json(pipeline_path)
    if is_valid:
        pipe_obj = Pipeline()
        pipe_obj.load(pipeline_path)
        if object_name in pipe_obj.parts:
            pipe_obj.remove(object_name, with_source)
            pipe_obj.save()
        success = True
    return success

def update_dependencies(action, pipeline_path, dependant_name, dependency_name):
    success = False
    is_valid, _ = validate_config_json(pipeline_path)
    if is_valid:
        pipe_obj = Pipeline()
        pipe_obj.load(pipeline_path)
        if action == "add":
            pipe_obj.add_dependencies(dependant_name, [dependency_name])
        else:
            pipe_obj.remove_dependencies(dependant_name, [dependency_name])
        pipe_obj.save()
        success = True
    return success