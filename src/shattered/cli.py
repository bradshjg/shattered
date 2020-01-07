import argparse
import os
import sys

from .shattered import Shattered


def load_app(args):
    sys.path.insert(0, os.getcwd())
    module_file = args.app or os.getenv("SHATTERED_APP", "app.py")
    module_name = os.path.splitext(module_file)[0]
    __import__(module_name)
    module = sys.modules[module_name]
    matches = [v for v in module.__dict__.values() if isinstance(v, Shattered)]
    if len(matches) == 1:
        return matches[0]
    else:
        raise EnvironmentError("Detected multiple Shattered applications.")


def run_app(args):
    app = load_app(args)
    app.run()


def print_config(args):
    app = load_app(args)
    for k, v in app.config.items():
        print(f"{k}: {v}")


def parse_arguments():
    parser = argparse.ArgumentParser(prog="shattered")
    parser.add_argument("-a", "--app", help="shattered app")
    subparsers = parser.add_subparsers(
        title="subcommands", description="valid subcommands", help="additional help"
    )
    parser_run = subparsers.add_parser("run", help="run shattered app")
    parser_run.set_defaults(func=run_app)
    parser_config = subparsers.add_parser("config", help="show shattered app config")
    parser_config.set_defaults(func=print_config)
    return parser.parse_args()


def main():
    args = parse_arguments()
    args.func(args)
