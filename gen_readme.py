import argparse
import pathlib
from typing import Dict, List

from coseto import get_parser

thisdir = pathlib.Path(__file__).parent.resolve()

def get_subparsers(parser: argparse.ArgumentParser) -> Dict[str, argparse.ArgumentParser]:
    try:
        return parser._subparsers._group_actions[0].choices
    except:
        return {}

def format_help(name: str, parser: argparse.ArgumentParser, depth: int = 1) -> List[str]:
    header_str = "#"*depth + " " + name
    help_str = parser.format_help().replace(pathlib.Path(__file__).name, 'coseto')
    subparsers = get_subparsers(parser)
    return [
        header_str, help_str, 
        *(line for n, p in subparsers.items() for line in format_help(f"{name} {n}", p, depth + 1) if line)
    ]


def main():
    parser = get_parser()

    readme_lines = [
        "# CoSeTo",
        "Conference Search Tool (CoSeTo) is a command-line tool for searching academic venues and authors",
        
        "",

        "## Installation",
        "```bash",
        "pip install -e ./coseto # -e flag is optional - it installs the package in editable mode",
        "```",

        "",

        "## Usage",
        "```bash",
        "coseto --help",
        "```",

        "## Examples",
        "```bash",
        "# search for conferences which have either blockchain or distributed ledger and either iot or internet of things in their call-for-papers",
        "coseto conferences search --upcoming \"blockchain,distributed ledger;iot\" > report.txt",
        "",
        "# get information on a specific conference",
        "coseto conferences get ISAAC",
        "",
        "# get author publication venues",
        "coseto authors ./examples/authors_input.yml -o ./examples/authors_output.yml",
        "```",

        "## CLI Documentation",
        *format_help("coseto", parser, depth=3)
    ]

    print(readme_lines)

    thisdir.joinpath("README.md").write_text("\n".join(readme_lines))


if __name__ == "__main__":
    main()
