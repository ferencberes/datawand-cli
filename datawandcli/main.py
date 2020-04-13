import os
from cli.utils import *
from cli.session_utils import *
from cli.pipeline_utils import *
from cli.parser_utils import *


if __name__ == "__main__":
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