import argparse
import pathlib

import pandas as pd
import yaml


def get_parser():
    parser = argparse.ArgumentParser(description="Top venues")
    parser.add_argument("author_venues_file", type=pathlib.Path)
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()

    author_venues = yaml.safe_load(args.author_venues_file.read_text())

    top_venues_dfs = []
    for author in author_venues:
        df = pd.DataFrame.from_dict(author['venues'], orient='index')
        top_venues = df[df["count"] >= 10]
        if len(top_venues) < 5:
            top_venues = df.nlargest(5, "count")

        top_venues["author"] = author["name"]
        top_venues.index.name = 'venue'
        top_venues = top_venues.reset_index().set_index(['author', 'venue'])

        top_venues_dfs.append(top_venues)

    top_venues_df = pd.concat(top_venues_dfs)
    print(top_venues_df.to_string())
    print()

    top_venues_df.to_clipboard(excel=True)

if __name__ == "__main__":
    main()