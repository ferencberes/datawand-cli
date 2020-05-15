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
    delete_parser = subparsers.add_parser("drop", help="Disable  repository by providing its name or path")
    delete_parser.add_argument("--name", help="provide repository name")
    pipeline_parser = subparsers.add_parser("pipeline", help="Choose from ['create','drop','list'] subcommands!")
    pipe_subs = pipeline_parser.add_subparsers(dest="subcommand")
    _ = pipe_subs.add_parser("list", help="List pipelines")
    create_pipe = pipe_subs.add_parser("create", help="Create new pipeline")
    create_pipe.add_argument("--name", help="provide pipeline name")
    delete_pipe = pipe_subs.add_parser("drop", help="Remove pipeline")
    delete_pipe.add_argument("--path", help="provide pipeline json file path")
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
    elif args.command == "pipeline":
        if args.subcommand == "list":
            list_pipelines(c, repos_table)
        elif args.subcommand == "create":
            create_pipeline(c, repos_table, args.name)
        elif args.subcommand == "drop":
            remove_pipeline(c, repos_table, args.path)
        else:
            parser.print_help()
    else:
        parser.print_help()
    # close database connection
    conn.close()