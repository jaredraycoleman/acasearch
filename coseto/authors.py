import argparse
import logging
import pathlib
import time
from copy import deepcopy
from functools import lru_cache
from typing import Any, Dict, Optional, Set

import numpy as np
import requests
import yaml

from coseto.conferences import load_data

logging.getLogger().setLevel(logging.INFO)

thisdir = pathlib.Path(__file__).parent.resolve()

URLS = {
    "author": "https://dblp.org/search/author/api",
    "venue": "https://dblp.org/search/venue/api",
    "pub": "https://dblp.org/search/publ/api",
}

conference_aliases = {
    "WDAG": "DISC",
    "IEEE ICBC": "ICBC",
    "SPDP": "IPDPS",
}


def get_matching_venue(venue_abbr: str, all_venues: Set[str]) -> Optional[str]:
    """Returns first matching venue

    First checks exact match, then capitalization, then keeping only alpha characters

    Args:
        venue_abbr (str): Abbreviation of venue
        all_venues (Set[str]): All venues

    Returns:
        Optional[str]: Matching venue
    """
    for venue in all_venues:
        if venue == venue_abbr or venue.lower().split("/")[0] == venue_abbr.lower():
            return venue
    for venue_alias in conference_aliases:
        if venue_abbr == venue_alias:
            return conference_aliases[venue_alias]

    venue_abbr = venue_abbr.lower()
    for venue in all_venues:
        if venue.lower() == venue_abbr:
            return venue
        elif venue.lower().split("/")[0] == venue_abbr:
            return venue
    for venue in conference_aliases:
        if venue_abbr == venue.lower():
            return conference_aliases[venue]
        elif venue_abbr == venue.lower().split("/")[0]:
            return conference_aliases[venue]

    venue_abbr = "".join([c for c in venue_abbr if c.isalpha()])
    for venue in all_venues:
        if "".join([c for c in venue.lower() if c.isalpha()]) == venue_abbr:
            return venue
        elif "".join([c for c in venue.lower().split("/")[0] if c.isalpha()]) == venue_abbr:
            return venue
    for venue in conference_aliases:
        if "".join([c for c in venue.lower() if c.isalpha()]) == venue_abbr:
            return conference_aliases[venue]
        elif "".join([c for c in venue.lower().split("/")[0] if c.isalpha()]) == venue_abbr:
            return conference_aliases[venue]

    return None


@lru_cache(maxsize=1000)
def get_info(venue_abbr: str) -> Dict[str, Any]:
    df = load_data()
    all_venues = df["conference"].unique()
    venue = get_matching_venue(venue_abbr, all_venues)
    if venue is None:
        raise ValueError(f"Could not find venue {venue_abbr}")

    df = df.drop(columns=["topics", "last_deadline"])
    df = df.astype(object).where((df.notna() & df.notnull()), None)

    info = df[df["conference"] == venue].iloc[0].to_dict()
    del info["conference"]
    return info


points = {
    "A*": 4.0,
    "A": 4.0,
    "B": 3.0,
    "C": 2.0,
    "A1": 4.0,
    "A2": 4.0,
    "B1": 3.5,
    "B2": 3.0,
    "B3": 2.5,
    "B4": 2.0,
    "B5": 1.5,
}


def get_parser(
    parser: Optional[argparse.ArgumentParser] = None,
) -> argparse.ArgumentParser:
    if parser is None:
        parser = argparse.ArgumentParser()
    parser.add_argument("authors_file")
    parser.add_argument("-o", "--output", default="authors.yaml")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    parser.set_defaults(func=authors_command)
    return parser


def authors_command(args: argparse.Namespace):
    logging.getLogger().setLevel(args.log_level)
    infile = pathlib.Path(args.authors_file).resolve(strict=True)
    outfile = pathlib.Path(args.output).resolve()

    authors = yaml.load(infile.read_text(encoding="utf-8"), Loader=yaml.SafeLoader)
    authors = [author if isinstance(author, dict) else {"name": author} for author in authors]
    author_venues = {}
    author_venues = {author["name"]: author for author in author_venues}
    missing_venues = {}
    for author in authors:
        # Get author publications
        name_query = author["name"].replace(" ", "_").strip()
        logging.info(f"Getting venues for {name_query}")

        # try request 3 times before giving up
        while True:
            try:
                res = requests.get(
                    "https://dblp.org/search/publ/api",
                    params={
                        "q": f"author:{name_query}:type:Conference_and_Workshop_Papers:",
                        "h": 500,
                        "c": 500,
                        "p": "2",
                        "compl": "venue",
                        "format": "json",
                    },
                )
                print(res.url)
                # print(res.request.url)
                if res.status_code == 200:
                    logging.info(f"Got venues for {name_query}")
                    break
                else:
                    logging.error(
                        f"Got status code {res.status_code} for {name_query}. Trying again in 5 seconds"
                    )
                    time.sleep(5)
            except:
                logging.error(f"Request failed, trying again after 5 seconds")
                time.sleep(5)

        if res.status_code != 200:
            logging.warning(f"Error getting author {author['name']}")
            logging.warning(f"Status code: {res.status_code}")
            # logging.warning(f"Response: {res.text}")
            continue
        res_json = res.json()
        if "c" not in res_json["result"]["completions"]:
            logging.warning(f"Could not find venues for {author['name']}")
            continue
        venues = res_json["result"]["completions"]["c"]
        if isinstance(venues, dict):
            venues = [venues]

        venue_counts = {}
        for venue in venues:
            name = venue["text"].lstrip(":facet:venue:")
            venue_counts[name] = int(venue["@sc"])

        venue_gpa_points = 0
        venue_gpa_total = 0
        venues = {}
        for venue, count in sorted(venue_counts.items(), key=lambda x: x[1], reverse=True):
            try:
                info = get_info(venue)
                venues[venue] = info
                info["count"] = count
            except ValueError:
                venues[venue] = {"count": count}
                missing_venues[venue] = missing_venues.get(venue, 0) + count
                continue

            rank_points = [
                points[info[rank]]
                for rank in ["core_rank", "era_rank", "qualis_rank"]
                if points.get(info[rank]) is not None
            ]
            if rank_points:
                venue_gpa_points += np.mean(rank_points) * count
                venue_gpa_total += count

        venue_gpa = (
            None if venue_gpa_total == 0 else float(round(venue_gpa_points / venue_gpa_total, 2))
        )
        author["venue_gpa"] = venue_gpa
        author["venues"] = deepcopy(venues)

    outfile.write_text(
        yaml.safe_dump(authors, sort_keys=False, indent=2, allow_unicode=True),
        encoding="utf-8",
    )

    if missing_venues:
        logging.info("Missing venues (Top 20):")
        for venue, count in sorted(missing_venues.items(), key=lambda x: x[1], reverse=True)[:20]:
            logging.info(f"\t{venue}: {count}")


def main():
    parser = get_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
