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
    df = pd.read_csv(thisdir.joinpath("data.csv"))
    df.loc[:, "Last Deadline"] = df["Last Deadline"].apply(date_parse)
    return df

def query_data(df: pd.DataFrame, query: List[List[str]]) -> pd.DataFrame:
    df.loc[:, "Query Score"] = df["Topics"].apply(partial(score, query))
    df = df.sort_values(
        by=["Query Score", "ERA Rank", "Qualis Rank"], 
        ascending=[False, True, True]
    )
    return df

def to_report(df: pd.DataFrame) -> str:
    columns = ["Conference", "ERA Rank", "Qualis Rank", "Last Deadline", "Name", "Query Score"]
    columns = [col for col in df.columns if col in columns]
    df.loc[:, "Last Deadline"] = df["Last Deadline"].dt.strftime("%b %d")
    return df[columns].to_string(index=None)

def main():
    query = [
        ["mobile"],
        ["agent", "robot"]
    ]
    df = query_data(load_data(), query)
    print(to_report(df))

if __name__ == "__main__":
    main()
