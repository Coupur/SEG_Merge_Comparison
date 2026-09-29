#!/usr/bin/env python
"""Fill merge_date (committer date of the merge commit) via the GitHub REST API. Resumable.

UNTESTED against the live API (author's sandbox was rate-limited). Run on ~5 rows first:
    GITHUB_TOKEN=... python scripts/enrich_dates.py --limit 5

Why the API and not local clones: some merges come from deleted branches, so their commits may be
missing from a normal clone; GitHub still serves commits by SHA. Authenticated limit is 5000 req/h,
so ~6k merges takes a little over an hour. 404/422 are recorded as 'missing' and reported.
"""
import argparse
import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests

from mergedrift.eras import assign_era

SCEN = Path("data/interim/scenarios.csv")
CACHE = Path("data/interim/merge_dates.csv")


def fetch(session, repo, sha):
    r = session.get(f"https://api.github.com/repos/{repo}/commits/{sha}", timeout=30)
    if r.status_code == 403 and r.headers.get("x-ratelimit-remaining") == "0":
        wait = max(int(r.headers.get("x-ratelimit-reset", "0")) - int(time.time()), 0) + 5
        print(f"rate limited; sleeping {wait}s", file=sys.stderr)
        time.sleep(wait)
        return fetch(session, repo, sha)
    if r.status_code in (404, 422):
        return "missing"
    r.raise_for_status()
    return r.json()["commit"]["committer"]["date"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("Set GITHUB_TOKEN (unauthenticated limit is 60 requests/hour).")
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})

    scen = pd.read_csv(SCEN, dtype=str, keep_default_na=False)
    done = pd.read_csv(CACHE, dtype=str, keep_default_na=False) if CACHE.exists() else pd.DataFrame(columns=["scenario_id", "merge_date"])
    have = dict(zip(done["scenario_id"], done["merge_date"]))
    todo = scen[~scen["scenario_id"].isin(have)]
    if args.limit:
        todo = todo.head(args.limit)
    for n, row in enumerate(todo.itertuples(), 1):
        have[row.scenario_id] = fetch(s, row.repo, row.merge_commit)
        if n % 100 == 0:
            pd.DataFrame(have.items(), columns=["scenario_id", "merge_date"]).to_csv(CACHE, index=False)
            print(f"{n}/{len(todo)}")
    pd.DataFrame(have.items(), columns=["scenario_id", "merge_date"]).to_csv(CACHE, index=False)

    scen["merge_date"] = scen["scenario_id"].map(have).fillna("")
    scen["era"] = [assign_era(d) or "" if d not in ("", "missing") else "" for d in scen["merge_date"]]
    scen.to_csv(SCEN, index=False)
    ok = (~scen["merge_date"].isin(["", "missing"])).sum()
    print(f"dated {ok}/{len(scen)}; missing {(scen['merge_date']=='missing').sum()}")
    print(scen["era"].replace("", "outside/none").value_counts().to_string())


if __name__ == "__main__":
    main()
