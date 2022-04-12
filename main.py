from datetime import datetime, timedelta
from io import StringIO
import pathlib
from functools import partial
from statistics import mean
from typing import List, Tuple

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

def load_data() -> pd.DataFrame:
    df = pd.read_csv(
        StringIO(
            ''.join([
                i if ord(i) < 128 else ' ' 
                for i in thisdir.joinpath("data.csv").read_text()
            ])
        )
    )
    df.loc[:, "Last Deadline"] = df["Last Deadline"].apply(date_parse)
    df["CORE Rank"] = pd.Categorical(df["CORE Rank"], ["A*", "A", "B", "C"])
    return df

def query_data(df: pd.DataFrame, query: List[List[str]]) -> pd.DataFrame:
    df.loc[:, "Query Score"] = df["Topics"].apply(partial(score, query))
    return df

SORT_COLS = ["CORE Rank", "ERA Rank", "Qualis Rank", "h5-index"]
DESCENDING_COLS = {"Query Score"}
def sort_data(df: pd.DataFrame, 
              cols: List[str] = SORT_COLS) -> pd.DataFrame:
    return df.sort_values(
        by=cols,
        ascending=[col not in DESCENDING_COLS for col in cols]
    )

def to_report(df: pd.DataFrame) -> str:
    columns = ["Conference", "h5-index", "CORE Rank", "ERA Rank", "Qualis Rank", "Last Deadline", "Name", "Query Score"]
    columns = [col for col in df.columns if col in columns]
    df.loc[:, "Last Deadline"] = df["Last Deadline"].dt.strftime("%b %d")
    return df[columns].to_string(index=None)


# API
def remaining_days(deadline: datetime) -> int:
    return (deadline - datetime.today()).days % 365

def do_query(query: List[List[str]], sort_upcoming: bool = False) -> None:
    df = load_data()

    sort_cols = [*SORT_COLS]
    if sort_upcoming:
        df["Remaining Days"] = df["Last Deadline"].apply(remaining_days)
        sort_cols = ["Remaining Days", *sort_cols]

    # df = df[df["Last Deadline"] - datetime.today()]
    if query:
        df = query_data(df, query)
        sort_cols = ["Query Score", *sort_cols]

    df = sort_data(df, sort_cols)
    print(to_report(df))

def main():
    query = [
        # ["mobile"],
        # ["agent", "robot", "online"],
        # ["distributed"].
        # ["competitive"],
        ["blockchain"],
        # ["system", "application"],
        ["iot"]
    ]

    do_query(query, sort_upcoming=False)

if __name__ == "__main__":
    main()
