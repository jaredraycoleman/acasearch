import argparse
import pathlib
import sys
from datetime import datetime
from functools import lru_cache, partial
from io import StringIO
from typing import List, Optional

import pandas as pd
from dateutil.parser import parse as date_parse
from thefuzz import fuzz

thisdir = pathlib.Path(__file__).resolve().parent

def score(clauses: List[List[str]], topics: str) -> float:
    return min( # max match across clauses - ALL clauses should match
        max( # max across topics and queries - any query can match any topic
            fuzz.partial_ratio(
                query.strip().lower(), 
                topic.strip().lower()
            )
            for topic in topics.split(" // ")
            for query in clause
        )
        for clause in clauses
    )

@lru_cache(maxsize=None)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(
        StringIO(
            ''.join([
                i if ord(i) < 128 else ' ' 
                for i in thisdir.joinpath("data.csv").read_text()
            ])
        )
    )
    df["last_deadline"] = pd.to_datetime(df["last_deadline"].apply(date_parse))
    df["core_rank"] = pd.Categorical(df["core_rank"], ["A*", "A", "B", "C"])
    return df

def query_data(df: pd.DataFrame, query: List[List[str]]) -> pd.DataFrame:
    df.loc[:, "query_score"] = df["topics"].apply(partial(score, query))
    return df

SORT_COLS = ["core_rank", "era_rank", "qualis_rank", "h5_index"]
DESCENDING_COLS = {"query_score"}
def sort_data(df: pd.DataFrame, 
              cols: List[str] = SORT_COLS) -> pd.DataFrame:
    return df.sort_values(
        by=cols,
        ascending=[col not in DESCENDING_COLS for col in cols]
    )

def to_report(df: pd.DataFrame) -> str:
    columns = ["conference", "h5_index", "core_rank", "era_rank", "qualis_rank", "last_deadline", "name", "query_score"]
    columns = [col for col in df.columns if col in columns]
    print(df['last_deadline'])
    df.loc[:, "last_deadline"] = df["last_deadline"].dt.strftime("%b %d")
    return df[columns].to_string(index=None)


# API
def remaining_days(deadline: datetime) -> int:
    return (deadline - datetime.today()).days % 365

def do_query(query: List[List[str]], sort_upcoming: bool = False, rank_threshold: str = "N/A", query_threshold: int = 0) -> None:
    df = load_data()

    sort_cols = [*SORT_COLS]
    if sort_upcoming:
        df["remaining_days"] = df["last_deadline"].apply(remaining_days)
        sort_cols = ["remaining_days", *sort_cols]

    # df = df[df["last_deadline"] - datetime.today()]
    if query:
        df = query_data(df, query)
        sort_cols = ["query_score", *sort_cols]
        
    sortorder = ["A*", "A", "B", "C", "N/A"]
    df["core_rank"] = pd.Categorical(df["core_rank"], categories=sortorder, ordered=True)
    df["core_rank"] = df["core_rank"].fillna("N/A")
    df["core_rank"] = df["core_rank"].apply(lambda rank: rank if rank in sortorder else "N/A")
    if rank_threshold != "N/A":
        threshold_int = sortorder.index(rank_threshold)
        df = df[df["core_rank"].apply(lambda rank: sortorder.index(rank) <= threshold_int)]

        
    if query_threshold > 0:
        # remove CFPs with score below threshold
        df = df[df["query_score"] >= query_threshold]

    df = sort_data(df, sort_cols)
    print(to_report(df))

def search_command(args: argparse.Namespace) -> None:
    query = [[keyword for keyword in clause.split(",")] for clause in (args.query or " ").split(";")]
    do_query(query, sort_upcoming=args.upcoming, rank_threshold=args.rank_threshold, query_threshold=args.query_threshold)

def get_command(args: argparse.Namespace) -> None:
    df = load_data()
    if args.column is None:
        data = df[df["conference"] == args.conference].T
        topics = "\t" + "\n\t".join(data.loc["topics"].values[0].split(" // "))
        columns = ["conference", "name", "core_rank", "era_rank", "qualis_rank", "h5_index", "last_deadline"]
        data.loc['last_deadline'] = pd.to_datetime(data.loc['last_deadline']).dt.strftime("%B %d")
        data = data.loc[columns]
        print(data.to_string(header=False))
        print(f"topics {topics}")
    else:
        data = df.set_index("conference").loc[args.conference,args.column]
        if args.column == "topics":
            data = "\n".join(data.split(" // "))
        elif args.column == "last_deadline":
            data = data.strftime("%B %d")
        print(data)


def get_parser(parser: Optional[argparse.ArgumentParser] = None) -> argparse.ArgumentParser:
    df = load_data()

    if parser is None:
        parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    query_parser = subparsers.add_parser("search")
    query_parser.add_argument("query", help="Semi-colon seperated AND clauses of comma-seperated OR keywords", nargs="?")
    query_parser.add_argument("--upcoming", action="store_true", help="If set, sort by upcoming deadline before ranking")
    query_parser.set_defaults(func=search_command)
    query_parser.add_argument("--query-threshold", help="Threshold for fuzzy matching", default=0.0, type=float)
    query_parser.add_argument(
        "--rank-threshold", help="Threshold for CORE rank", default="N/A", 
        choices=["A*", "A", "B", "C", "N/A"]
    )

    get_parser = subparsers.add_parser("get")
    get_parser.add_argument(
        "conference", 
        choices=df["conference"].unique(), 
        metavar='CONFERENCE ABBREVIATION', 
        help="Conference to get data for - one of: [" + ', '.join(df['conference'].unique()) + "]"
    )
    attr_choices = [*df.columns, None]
    get_parser.add_argument(
        "column", 
        choices=attr_choices, 
        metavar='ATTRIBUTE',
        help="Conference attribute to get - one of: [" + ', '.join(map(str, attr_choices)) + "]",
        default=None,
        nargs="?"
    )
    get_parser.set_defaults(func=get_command)
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        sys.argv.append("--help")
        parser.parse_args()
    else:
        args.func(args)
        
if __name__ == "__main__":
    main()
