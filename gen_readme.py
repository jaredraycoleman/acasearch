from acasearch import get_parser
from acasearch.authors import get_parser as get_authors_parser
from acasearch.conferences import get_parser as get_conferences_parser
import pathlib

thisdir = pathlib.Path(__file__).parent.resolve()

def main():
    parser = get_parser()

    main_help = parser.format_help()
    authors_help = get_authors_parser().format_help()
    conferences_help = get_conferences_parser().format_help()

    help_str = "\n".join(
        [
            "# acasearch", main_help, 
            "## acasearch authors", authors_help, 
            "## acasearch conferences", conferences_help
        ]
    )

    thisdir.joinpath("README.md").write_text(help_str)


if __name__ == "__main__":
    main()