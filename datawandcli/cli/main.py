import os, argparse
from .utils import *
from .session_utils import *
from .pipeline_utils import *

def cli_parser():
    welcome_txt = "Welcome to datawand CLI. Happy coding! :)"
    parser = argparse.ArgumentParser(description=welcome_txt)
    subparsers = parser.add_subparsers(dest="command")
    activate_parser = subparsers.add_parser("activate")
    activate_parser.add_argument("name", help="provide session name")
    _ = subparsers.add_parser("deactivate")
    _ = subparsers.add_parser("status")
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
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument(
        "object",
        choices=["session","pipeline"],
        help='Choose from the available object options')
    return parser

def execute():
    # init environment
    sess_table = "sessions"
    conn, c, kvstore = prepare_environment(sess_table)
    
    # parse arguments
    parser = cli_parser()
    args = parser.parse_args()
    if args.command == "activate":
        sess_name = args.name
        activate_session(kvstore, sess_name)
    elif args.command == "deactivate":
        deactivate_session(kvstore)
    elif args.command == "status":
        current_sess, num_pipes, num_exps = status_session(kvstore, c, sess_table)
    elif args.command == "list":
        if args.object == "session":
            print(list_sessions(c, sess_table))
        else:
            cnt = list_pipeline(kvstore, c, sess_table)
    elif args.command == "create":
        obj_name = args.name
        if args.object == "session":
            success = create_session(conn, c, sess_table, obj_name)
            if success:
                print("Sessions:")
                print(list_sessions(c, sess_table))
        else:
            success = create_pipeline(kvstore, c, sess_table, obj_name)
            if success:
                print("Pipelines:")
                list_pipeline(kvstore, c, sess_table)
    elif args.command == "remove":
        obj_name = args.name
        if args.object == "session":
            success = remove_session(kvstore, conn, c, sess_table, obj_name)
            if success:
                print("Sessions:")
                print(list_sessions(c, sess_table))
        else:
            success = remove_pipeline(kvstore, c, sess_table, obj_name)
            if success:
                print("Pipelines:")
                list_pipeline(kvstore, c, sess_table)
    else:
        parser.print_help()
    
    # close database connection
    conn.close()