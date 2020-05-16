import os, argparse
from .utils import *
from .repository_utils import *
from .pipeline_utils import *

def cli_parser():
    welcome_txt = "Welcome to datawand CLI. Happy coding! :)"
    parser = argparse.ArgumentParser(description=welcome_txt)
    subparsers = parser.add_subparsers(dest="command")
    _ = subparsers.add_parser("status", help="Get information about your current folder")
    _ = subparsers.add_parser("list", help="List available datawand repositories")
    init_parser = subparsers.add_parser("init", help="Initialize new repository in your current folder")
    init_parser.add_argument("name", help=REPO_NAME_MSG)
    drop_parser = subparsers.add_parser("drop", help="Disable  repository by providing its name")
    drop_parser.add_argument("name", help=REPO_NAME_MSG)
    create_pipe = subparsers.add_parser("create", help="Create a new pipeline")
    create_pipe.add_argument("name", help="Provide pipeline name")
    copy_pipe = subparsers.add_parser("copy", help="Copy pipeline")
    copy_pipe.add_argument("path", help=PATH_MSG + " to be copied")
    copy_pipe.add_argument("name", help="Provide name for the new pipeline")
    view_pipe = subparsers.add_parser("view", help="View pipeline (items)")
    view_pipe.add_argument("path", help=PATH_MSG)
    view_pipe.add_argument("--name", help="Select an object name from the pipeline")
    delete_pipe = subparsers.add_parser("delete", help="Remove pipeline")
    delete_pipe.add_argument("path", help=PATH_MSG)
    return parser

def execute():
    # init environment
    repos_table = "repositories"
    conn, c = prepare_environment(repos_table)
    
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
    else:
        parser.print_help()
    # close database connection
    conn.close()