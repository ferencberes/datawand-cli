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
    init.add_argument("name", help=REPO_NAME_MSG)
    drop = subparsers.add_parser("drop", help="Disable repository by providing its name")
    drop.add_argument("name", help=REPO_NAME_MSG)
    create = subparsers.add_parser("create", help="Create a new pipeline")
    create.add_argument("name", help="Provide pipeline name")
    copy = subparsers.add_parser("copy", help="Copy pipeline")
    copy.add_argument("path", help=PATH_MSG + " to be copied")
    copy.add_argument("name", help="Provide name for the new pipeline")
    view = subparsers.add_parser("view", help="View pipeline (items)")
    view.add_argument("path", help=PATH_MSG)
    view.add_argument("--name", help="Select an object name from the pipeline")
    delete = subparsers.add_parser("delete", help="Remove pipeline")
    delete.add_argument("path", help=PATH_MSG)
    run = subparsers.add_parser("run", help="Run experiment")
    run.add_argument("path", help=EXP_PATH)
    run.add_argument("--workers", help="Set the number luigi workers to enable parallel execution")
    log = subparsers.add_parser("log", help="View experiment logs")
    log.add_argument("path", help=EXP_PATH)
    log.add_argument("--name", help="Select an object name from the pipeline")
    clear = subparsers.add_parser("clear", help="Clear experiment")
    clear.add_argument("path", help=EXP_PATH)
    kill = subparsers.add_parser("kill", help="Kill  experiment processes")
    kill.add_argument("path", help=EXP_PATH)
    scheduler = subparsers.add_parser("scheduler", help="Interact with luigi scheduler")
    scheduler.add_argument("action", choices=['start', 'status', 'stop'])
    scheduler.add_argument("--port", help="Select the port for luigi central scheduler")
    scheduler.add_argument("--remove", help="Number of seconds after which task history is cleared")
    scheduler.add_argument("--retry", help="Number of seconds after which failed tasks are re-executed again")
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
        success = log_experiment(c, repos_table, args.path, args.name)
    elif args.command == "scheduler":
        if args.action == "start":
            start_luigi(args.port, args.remove, args.retry)
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