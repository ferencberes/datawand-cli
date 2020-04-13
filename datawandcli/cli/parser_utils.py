import argparse

welcome_txt = "Welcome to datawand-lite CLI. Happy coding! :)"

def cli_parser():
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