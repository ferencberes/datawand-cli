import os, argparse
from .utils import *
from .repository_utils import *
from .pipeline_utils import *
from .experiment_utils import *

def cli_parser():
    welcome_txt = "Welcome to datawand CLI. Happy coding! :)"
    parser = argparse.ArgumentParser(description=welcome_txt)
    subparsers = parser.add_subparsers(dest="command")
    _ = subparsers.add_parser("status", help="Get information about your current folder")
    _ = subparsers.add_parser("list", help="List available datawand repositories")
    init = subparsers.add_parser("init", help="Initialize new repository in your current folder")
    init.add_argument("--name", help=REPO_NAME_MSG)
    drop = subparsers.add_parser("drop", help="Disable repository by providing its name")
    drop.add_argument("name", help=REPO_NAME_MSG)
    create = subparsers.add_parser("create", help="Create a new pipeline")
    create.add_argument("name", help="Provide pipeline name")
    add = subparsers.add_parser("add", help="Add new component to pipeline")
    add.add_argument("pipeline_path", help="Provide pipeline config path")
    add.add_argument("object_path", help="Provide relative path to the new object in the repository")
    add.add_argument("--name", help="Provide name for the new component")
    add.add_argument("--type", help="Provide component type", choices=['pyscript', 'notebook', 'module'])
    remove = subparsers.add_parser("remove", help="Remove component from pipeline")
    remove.add_argument("pipeline_path", help="Provide pipeline config path")
    remove.add_argument("object_name", help="Provide name for the component to be deleted")
    remove.add_argument("--source", action="store_true", help="Delete the related source file as well")
    dependency = subparsers.add_parser("dependency", help="Add new dependency relation")
    dependency.add_argument("action", help="Choose dependency action", choices=['add', 'remove'])
    dependency.add_argument("pipeline_path", help="Provide pipeline config path")
    dependency.add_argument("dependant_name", help="Provide dependant object name")
    dependency.add_argument("dependency_name", help="Provide depdendency object name")
    view = subparsers.add_parser("view", help="View pipeline (items)")
    view.add_argument("path", help=PATH_MSG)
    view.add_argument("--name", help="Select an object name from the pipeline")
    copy = subparsers.add_parser("copy", help="Copy pipeline")
    copy.add_argument("path", help=PATH_MSG + " to be copied")
    copy.add_argument("name", help="Provide name for the new pipeline")
    delete = subparsers.add_parser("delete", help="Remove pipeline")
    delete.add_argument("path", help=PATH_MSG)
    run = subparsers.add_parser("run", help="Run experiment")
    run.add_argument("path", help=EXP_PATH)
    run.add_argument("--workers", type=int, default=1, help="Number luigi workers to enable parallel execution (default: 1)")
    log = subparsers.add_parser("log", help="View experiment logs")
    log.add_argument("path", help=EXP_PATH)
    log.add_argument("--name", help="Select an object name from the pipeline")
    log.add_argument("--tail", type=int, default=20, help="Show the last few lines (default: 20)")
    log.add_argument("--all", action="store_true", help="Show every row (default: last 20 rows are shown)")
    clear = subparsers.add_parser("clear", help="Clear experiment")
    clear.add_argument("path", help=EXP_PATH)
    kill = subparsers.add_parser("kill", help="Kill  experiment processes")
    kill.add_argument("path", help=EXP_PATH)
    scheduler = subparsers.add_parser("scheduler", help="Interact with luigi scheduler")
    scheduler.add_argument("action", choices=['start', 'status', 'stop'], help="Choose scheduler action")
    scheduler.add_argument("--port", type=int, default=8082, help="Select the port for luigi central scheduler (default: 8082).")
    scheduler.add_argument("--keep", type=int, default=3600, help="Number of seconds until task history is cleared (default: 60 minutes).")
    scheduler.add_argument("--retry", type=int, default=1800, help="Number of seconds until failed tasks are re-executed (default: 30 minutes). Failed tasks are only re-tried if this value is smaller than the --keep argument.")
    return parser
    
def execute():
    # init environment
    repos_table = "repositories"
    conn, c, config_dir = prepare_environment(repos_table)
    
    # parse arguments
    parser = cli_parser()
    args = parser.parse_args()
    if args.command == "init":
        success = create_repo(conn, c, repos_table, args.name)
        if success:
            print("A new repository was added.")
    elif args.command == "list":
        show_repo_table(list_repos(c, repos_table))
    elif args.command == "status":
        status_repo(c, repos_table)
    elif args.command == "drop":
        success = remove_repo(conn, c, repos_table, args.name)
        if success:
            print("A repository was deleted.")
    elif args.command == "create":
        create_pipeline(c, repos_table, args.name)
    elif args.command == "add":
        success = add_component(args.pipeline_path, args.object_path, args.name, args.type)
    elif args.command == "remove":
        success = remove_component(args.pipeline_path, args.object_name, args.source)
    elif args.command == "dependency":
        success = update_dependencies(args.action, args.pipeline_path, args.dependant_name, args.dependency_name)
    elif args.command == "copy":
        success = copy_pipeline(args.path, args.name)
        if success:
            print("The pipeline was copied")
    elif args.command == "view":
        success = view_pipeline(args.path, args.name)
    elif args.command == "delete":
        success = remove_pipeline(args.path)
        if success:
            print("The pipeline was deleted")
    elif args.command == "run":
        success = run_experiment(c, repos_table, args.path, args.workers)
        if success:
            print("Experiment script was started")
    elif args.command == "clear":
        success = clear_experiment(c, repos_table, args.path)
        if success:
            print("Experiment was cleared")
    elif args.command == "kill":
        success = kill_experiment(c, repos_table, args.path)
    elif args.command == "log":
        success = log_experiment(c, repos_table, args.path, args.name, args.tail, args.all)
    elif args.command == "scheduler":
        if args.action == "start":
            start_luigi(args.port, args.keep, args.retry)
        elif args.action == "status":
            find_luigi(False)
        elif args.action == "stop":
            find_luigi(True)
        else:
            raise ValueError("Invalid option")
    else:
        parser.print_help()
    # close database connection
    conn.close()