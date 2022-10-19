import argparse
from typing import Dict
from acasearch import get_parser
import pathlib

thisdir = pathlib.Path(__file__).parent.resolve()

def get_subparsers(parser: argparse.ArgumentParser) -> Dict[str, argparse.ArgumentParser]:
    try:
        return parser._subparsers._group_actions[0].choices
    except:
        return {}

def format_help(name: str, parser: argparse.ArgumentParser, depth: int = 1) -> str:
    header_str = "#"*depth + " " + name
    help_str = parser.format_help()
    subparsers = get_subparsers(parser)
    return "\n".join([
        header_str, help_str, 
        *(format_help(f"{name} {n}", p, depth + 1) for n, p in subparsers.items())
    ])


def main():
    parser = get_parser()
    help_str = format_help("acasearch", parser)

    thisdir.joinpath("README.md").write_text(help_str)


if __name__ == "__main__":
    main()