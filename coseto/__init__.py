import argparse
import sys

from .authors import get_parser as get_authors_parser
from .conferences import get_parser as get_conferences_parser


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()
    conferences_parser = subparsers.add_parser("conferences")
    get_conferences_parser(conferences_parser)

    authors_parser = subparsers.add_parser("authors")
    get_authors_parser(authors_parser)

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        sys.argv.append("--help")
        parser.parse_args()
    else:
        args.func(args)
