import os, argparse
from .utils import *
from .repository_utils import *
from .pipeline_utils import *

def cli_parser():
    welcome_txt = "Welcome to datawand CLI. Happy coding! :)"
    parser = argparse.ArgumentParser(description=welcome_txt)
    subparsers = parser.add_subparsers(dest="command")
    _ = subparsers.add_parser("list", help="List available datawand repositories")
    _ = subparsers.add_parser("status", help="Get information about your current folder")
    init_parser = subparsers.add_parser("init", help="Enable datawand for your current folder")
    init_parser.add_argument("--name", help="provide repository name")
    delete_parser = subparsers.add_parser("delete", help="Disable  repository by providing its name or path")
    delete_parser.add_argument("--name", help="provide repository name")
    delete_parser.add_argument("--path", help="provide repository absolute path")
    """
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument(
        "object",
        choices=["session","pipeline"],
        help='Choose from the available object options')
    create_parser.add_argument("name", help="provide object name")
    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument(
        "object",
        choices=["session","pipeline"],
        help='Choose from the available object options')
    remove_parser.add_argument("name", help="provide object name")
    """
    return parser

def execute():
    # init environment
    repos_table = "repositories"
    conn, c, _ = prepare_environment(repos_table)
    
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
    elif args.command == "delete":
        success = remove_repo(conn, c, repos_table, args.name, args.path)
        if success:
            print("A repository was deleted.")
    else:
        parser.print_help()
    """
    elif args.command == "create":
        obj_name = args.name
        if args.object == "session":
            success = create_session(conn, c, repos_table, obj_name)
            if success:
                print("Sessions:")
                print(list_sessions(c, repos_table))
        else:
            success = create_pipeline(kvstore, c, repos_table, obj_name)
            if success:
                print("Pipelines:")
                list_pipeline(kvstore, c, repos_table)
    elif args.command == "remove":
        obj_name = args.name
        if args.object == "session":
            success = remove_session(kvstore, conn, c, repos_table, obj_name)
            if success:
                print("Sessions:")
                print(list_sessions(c, repos_table))
        else:
            success = remove_pipeline(kvstore, c, repos_table, obj_name)
            if success:
                print("Pipelines:")
                list_pipeline(kvstore, c, repos_table)
    """
    
    # close database connection
    conn.close()