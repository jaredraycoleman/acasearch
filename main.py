from functools import partial
from typing import List, Tuple
import pandas as pd 
import pathlib 
from thefuzz import fuzz
from dateutil.parser import parse as date_parse

thisdir = pathlib.Path(__file__).resolve().parent

def score(queries: List[Tuple[str, str]], topics: str) -> float:
    return sum(
        min(
            sum(
                fuzz.ratio(query.strip().lower(), topic.strip().lower()) 
                for query in clause
            )
            for clause in queries
        )
        for topic in topics.split(" // ")
    )

def load_data() -> pd.DataFrame:
    df = pd.read_csv(thisdir.joinpath("data.csv"))
    df.loc[:, "Last Deadline"] = df["Last Deadline"].apply(date_parse)
    return df

def query(df: pd.DataFrame, queries: List[Tuple[str, str]]) -> pd.DataFrame:
    df.loc[:, "Query Score"] = df["Topics"].apply(partial(score, queries))
    df = df.sort_values(
        by=["Query Score", "ERA Rank", "Qualis Rank"], 
        ascending=[False, True, True]
    )
    return df

def to_report(df: pd.DataFrame) -> str:
    columns = ["Conference", "ERA Rank", "Qualis Rank", "Last Deadline", "Name", "Query Score"]
    df.loc[:, "Last Deadline"] = df["Last Deadline"].dt.strftime("%b %d")
    return df[columns].to_string(index=None)

def main():
    df = load_data()
    df = query(df, [
        ("mobile", "agents"),
        ("algorithms")
    ])
    print(to_report(df))

if __name__ == "__main__":
    main()