import argparse

welcome_txt = "Welcome to datawand-lite CLI. Happy coding! :)"

def instance_parser():
    parser = argparse.ArgumentParser(description=welcome_txt)
    parser.add_argument(
        "action",
        choices=["create", "list","remove","activate"],
        help="Provide instance action")
    parser.add_argument("--name", "-n", help="provide instance name")
    return parser

def pipeline_parser():
    parser = argparse.ArgumentParser(description=welcome_txt)
    subparsers = parser.add_subparsers(dest="subcommand")
    # subparser for pipelines
    parser_pipeline = subparsers.add_parser("pipeline")
    parser_pipeline.add_argument(
        "action",
        choices=["create","remove","list","show"],
        help='Provide pipeline action')
    parser_pipeline.add_argument("--name", "-n", help="provide pipeline name")
    # subparser for experiments
    parser_exp = subparsers.add_parser("experiment")
    parser_exp.add_argument(
        "action",
        choices=["status", "list","create","remove","run","stop"],
        help="Provide experiment action")
    # other options
    _ = subparsers.add_parser("deactivate")
    _ = subparsers.add_parser("status")
    return parser