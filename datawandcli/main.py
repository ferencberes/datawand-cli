import os
from os.path import expanduser
from cli.utils import *
from cli.parser import *
from cli.pipeline import *

if __name__ == "__main__":
    # init environment
    home_dir = expanduser("~")
    config_dir = "%s/.datawandlite" % home_dir
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    # init database
    instances_table="instances"
    conn, c, db_path = init_tables(config_dir, instances_table)

    # parse arguments
    parser = create_parser()
    args = parser.parse_args()
    
    # execute command
    if args.subcommand == "instance":
        handle_instance_request(args, conn, c, instances_table)
    elif args.subcommand == "pipeline":
        handle_pipeline_request(args, c, instances_table)
    elif args.subcommand == "experiment":
        pass
    else:
        parser.print_help()
    
    # close database connection
    conn.close()