import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="Welcome to datawand-lite CLI. Happy coding! :)")
    subparsers = parser.add_subparsers(dest="subcommand")
    # subparser for instances
    parser_init = subparsers.add_parser("instance")
    parser_init.add_argument(
        "action",
        choices=["create", "list","remove"],
        help="Provide instance action")
    parser_init.add_argument("--name", "-n", help="provide instance name")
    # subparser for pipelines
    parser_pipeline = subparsers.add_parser("pipeline")
    parser_pipeline.add_argument(
        "action",
        choices=["create","remove","list","show"],
        help='Provide pipeline action')
    parser_pipeline.add_argument("--instance", "-i", help="provide instance name")
    parser_pipeline.add_argument("--name", "-n", help="provide pipeline name")
    # subparser for experiments
    parser_exp = subparsers.add_parser("experiment")
    parser_exp.add_argument(
        "action",
        choices=["status", "list","create","remove","run","stop"],
        help="Provide experiment action")
    return parser