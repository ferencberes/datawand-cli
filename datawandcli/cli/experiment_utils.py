from datawandcli.components.objects import Pipeline
from datawandcli.components.luigi import SUCCESS_MSG, FAILURE_MSG
from .utils import *
import subprocess, shutil, psutil, time

def get_paths(json_path, repo_path):
    pipe_obj = Pipeline()
    pipe_obj.load(json_path)
    executable_folder = "%s/%s" % (repo_path, pipe_obj.base_dir)
    executable_name = "%s.sh" % pipe_obj.experiment_name
    master_log= "%s/%s.log" % (executable_folder, pipe_obj.experiment_name)
    status_files, log_files = [], []
    for item in pipe_obj.notebooks+pipe_obj.pyscripts:
        if item.is_clone:
            tmp_path = item.path
            ext = tmp_path.split(".")[-1]
            status_path = os.path.join(repo_path, pipe_obj.base_dir, tmp_path.replace(ext,"info"))
            log_path = os.path.join(repo_path, pipe_obj.base_dir, tmp_path.replace(ext,"log"))
            status_files.append(status_path)
            log_files.append(log_path)
    return executable_folder, executable_name, master_log, status_files, log_files

def experiment_status(cursor, repo_table, file_path):
    status, success_rate = "N/A", "N/A"
    cwd = os.getcwd()
    repo_name, repo_path = get_repo(cursor, cwd, repo_table)
    if repo_name != None:
        is_valid, is_experiment = validate_config_json(file_path)
        if is_experiment:
            _, _, master_log, status_files, _ = get_paths(file_path, repo_path)
            if os.path.exists(master_log):
                with open(master_log) as f:
                    content = f.read()
                if SUCCESS_MSG in content:
                    status = "SUCCESS"
                elif FAILURE_MSG in content:
                    status = "FAILED"
            finished = 0
            for fp in status_files:
                if os.path.exists(fp):
                    finished += 1
            success_rate = "%i" % (100 * finished / len(status_files)) + "%"
        else:
            print(EXP_PATH)
    else:
        print(NO_DW_MSG)
    return status, success_rate

def run_experiment(cursor, repo_table, file_path, workers, delim="/"):
    success = False
    if workers == None:
        workers = 1
    cwd = os.getcwd()
    repo_name, repo_path = get_repo(cursor, cwd, repo_table)
    if repo_name != None:
        is_valid, is_experiment = validate_config_json(file_path)
        if is_experiment:
            executable_folder, executable_name, master_log, _, _ = get_paths(file_path, repo_path)
            fp = open(master_log, 'w')
            process = subprocess.Popen(["bash",  executable_name, str(workers)], cwd=executable_folder, stdout=fp, stderr=fp)
            success = True
        else:
            print(EXP_PATH)
    else:
        print(NO_DW_MSG)
    return success

def clear_experiment(cursor, repo_table, file_path):
    success = False
    cwd = os.getcwd()
    repo_name, repo_path = get_repo(cursor, cwd, repo_table)
    if repo_name != None:
        is_valid, is_experiment = validate_config_json(file_path)
        if is_experiment:
            pipe_obj = Pipeline()
            pipe_obj.load(file_path)
            experiment_dir = pipe_obj.base_dir
            if experiment_dir != "":
                shutil.rmtree(experiment_dir)
            else:
                _, _, master_log, status_files, log_files = get_paths(file_path, repo_path)
                os.remove(master_log)
                for fp in status_files+log_files:
                    if os.path.exists(fp):
                        os.remove(fp)
                pipe_obj.clear()
            success = True
        else:
            print(EXP_PATH)
    else:
        print(NO_DW_MSG)
    return success

def log_experiment(cursor, repo_table, file_path, name, delim="/"):
    success = False
    cwd = os.getcwd()
    repo_name, repo_path = get_repo(cursor, cwd, repo_table)
    if repo_name != None:
        is_valid, is_experiment = validate_config_json(file_path)
        if is_experiment:
            _, _, master_log, _, log_files = get_paths(file_path, repo_path)
            if name == None:
                log_file = master_log
            else:
                log_file = None
                for fp in log_files:
                    fname = fp.split(delim)[-1]
                    ext = fp.split(".")[-1]
                    fname = fname.replace("."+ext,"")
                    if name == fname:
                        log_file = fp
                        break
            if log_file != None:
                with open(log_file) as f:
                    print(f.read())
                success = True
            else:
                print("Log file was not found!")
        else:
            print(EXP_PATH)
    else:
        print(NO_DW_MSG)
    return success

def kill_experiment(cursor, repo_table, file_path):
    success = False
    cwd = os.getcwd()
    repo_name, repo_path = get_repo(cursor, cwd, repo_table)
    if repo_name != None:
        is_valid, is_experiment = validate_config_json(file_path)
        if is_experiment:
            pipe_obj = Pipeline()
            pipe_obj.load(file_path)
            experiment_name = pipe_obj.experiment_name
            still_found = True
            num_proc = 0
            while still_found:
                still_found = False
                for p in psutil.process_iter():
                    command = ' '.join(p.cmdline())
                    #if not "datawand" in command and not "luigi" in command and experiment_name in command:
                    if experiment_name in command and "CLONE" in command:
                        print(command)
                        p.terminate()
                        p.wait()
                        num_proc += 1
                        still_found = True
                if still_found:
                    print("...")
                    time.sleep(5)
            success = True
        else:
            print(EXP_PATH)
    else:
        print(NO_DW_MSG)
    if success:
        print("%i processes were killed" % num_proc)
    return success