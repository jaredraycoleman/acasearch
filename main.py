import pathlib
from functools import partial
from statistics import mean
from string import ascii_lowercase
from typing import List, Tuple

import pandas as pd
from dateutil.parser import parse as date_parse
import re
import sympy
from thefuzz import fuzz
from sympy.logic.boolalg import to_cnf

thisdir = pathlib.Path(__file__).resolve().parent

def score(clauses: List[List[Tuple[bool, str]]], topics: str) -> float:
    return max( # max match across topics
        mean( # mean across clauses - ANY clause should match
            min( # min across expressions in clause - EVERY expression should match
                abs(
                    (100.0 if neg else 0) - 
                    fuzz.partial_ratio(
                        query.strip().lower(), 
                        topic.strip().lower()
                    )
                )
                for neg, query in clause
            )
            for clause in clauses
        )
        for topic in topics.split(" // ")
    )

def load_data() -> pd.DataFrame:
    df = pd.read_csv(thisdir.joinpath("data.csv"))
    df.loc[:, "Last Deadline"] = df["Last Deadline"].apply(date_parse)
    return df

def query(df: pd.DataFrame, query: str) -> pd.DataFrame:
    queries = parse_query(query=query)
    if queries:
        df.loc[:, "Query Score"] = df["Topics"].apply(partial(score, queries))
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

regex = re.compile(r"(?:(?<=[+&|])|(?<=^))(.+?)(?=(?:[+&|]|$))+")
def parse_query(query: str) -> List[List[Tuple[bool, str]]]:
    query = re.sub(r"\+", " | ", query).replace("!", "~")
    variables = {}
    for variable, match in zip(ascii_lowercase, regex.finditer(query)):
        variables[match.group(1).lower().strip()] = variable
    
    r_variables = {v: k for k, v in variables.items()}
    for expr_str, variable in variables.items():
        query = query.replace(expr_str, variable)

    clauses = []
    cnf = to_cnf(query, simplify=False)
    ands = cnf.args if not isinstance(cnf, sympy.core.symbol.Symbol) else [cnf]
    for clause_expr in ands:
        clause = []
        expressions = clause_expr.args if clause_expr.args else [clause_expr]
        isNot = clause_expr.is_Not # Should only be true if clause is singleton
        for expr in expressions:
            if expr.is_Not:
                isNot = True
            clause.append(
                (
                    isNot,
                    r_variables[str(expr).lstrip("~")]
                )
            )
        clauses.append(clause)
    return clauses

def main():
    df = load_data()
    df = query(df, "formal methods | transactional")
    print(to_report(df))

if __name__ == "__main__":
    main()
