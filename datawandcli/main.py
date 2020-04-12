import os
from cli.utils import *
from cli.session_utils import *

sess_table = "sessions"
sess_name = "trial"
conn, c, kvstore = prepare_environment(sess_table, postfix="_test")
print(create_session(conn, c, sess_table, sess_name))
print(remove_session(conn, c, sess_table, sess_name))

"""
if __name__ == "__main__":
    # init environment
    home_dir = expanduser("~")
    config_dir = "%s/.datawandlite" % home_dir
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    # init database
    instances_table="instances"
    conn, c, kvstore = init_tables(config_dir, instances_table)
    current_instance = kvstore.get("instance",None)
    
    # parse arguments
    if current_instance == None:
        parser = instance_parser()
        args = parser.parse_args()
        if args.action in ["create", "list","remove"]:
            handle_instance_request(args, conn, c, instances_table)
        elif args.action == "activate":
            if args.name != None:
                inst_name = args.name
                kvstore["instance"] = inst_name
                kvstore.commit()
                print("Instance '%s' was activated." % inst_name)
            else:
                print("Provide an instance name!")
        else:
            parser.print_help()
    else:
        parser = pipeline_parser()
        args = parser.parse_args()
        if args.subcommand == "deactivate":
            del kvstore["instance"]
            print("Instance '%s' was deactivated." % current_instance)
            kvstore.commit()
        elif args.subcommand == "status":
            base_dir, num_pipelines, num_experiments = extract_base_dir(c, current_instance, instances_table)
            print("Instance '%s' is currently active." % current_instance)
            print("Instance folder: %s" % base_dir)
            print("Number of pipelines: %i" % num_pipelines)
            print("Number of experiments: %i" % num_experiments)
        elif args.subcommand == "pipeline":
            handle_pipeline_request(args, c, current_instance, instances_table)
        elif args.subcommand == "experiment":
            pass
        else:
            parser.print_help()
    
    # close database connection
    conn.close()
"""