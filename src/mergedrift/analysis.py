"""Thin pandas layer: Schesch results -> long format -> ER_k tables."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from .metrics import KS, effort_reduction, breakeven_k
from .models import Outcome, outcome_from_schesch

# Base tool columns in result_adjusted.csv (the *_plus variants and *_fingerprint columns are skipped).
SCHESCH_TOOLS = [
    "gitmerge_ort", "gitmerge_ort_ignorespace", "gitmerge_recursive_histogram",
    "gitmerge_recursive_myers", "gitmerge_recursive_minimal", "gitmerge_recursive_patience",
    "gitmerge_resolve", "git_hires_merge", "spork", "mergiraf", "intellimerge",
    "adjacent", "imports", "version_numbers", "ivn", "ivn_ignorespace",
]


def load_schesch_long(results_csv: Path, repos_csv: Path, tools: Iterable[str] = SCHESCH_TOOLS) -> pd.DataFrame:
    """Return one row per (scenario, tool) with columns: scenario_id, repo, merge, tool, outcome."""
    df = pd.read_csv(results_csv, low_memory=False)
    repos = pd.read_csv(repos_csv).rename(columns={"idx": "repo-idx", "repository": "repo"})
    df = df.merge(repos, on="repo-idx", how="left")
    df["scenario_id"] = df["idx"]
    tools = [t for t in tools if t in df.columns]
    long = df.melt(id_vars=["scenario_id", "repo", "merge", "branch_name"], value_vars=tools,
                   var_name="tool", value_name="state")
    long["outcome"] = long["state"].map(lambda s: outcome_from_schesch(s).value)
    return long.drop(columns="state")


def er_table(long: pd.DataFrame, by: list[str], ks: Iterable[int] = KS) -> pd.DataFrame:
    """ER_k per group. `by` must include 'tool'; add 'era' etc. as needed."""
    rows = []
    for key, g in long.groupby(by):
        key = key if isinstance(key, tuple) else (key,)
        n = len(g)
        u = int((g["outcome"] == Outcome.UNHANDLED.value).sum())
        c = int((g["outcome"] == Outcome.CORRECT.value).sum())
        i = int((g["outcome"] == Outcome.INCORRECT.value).sum())
        row = dict(zip(by, key), n=n, unhandled=u, correct=c, incorrect=i,
                   breakeven_k=round(breakeven_k(u, i, n), 2))
        for k in ks:
            row[f"ER_k{k}"] = round(effort_reduction(u, i, n, k), 4)
        rows.append(row)
    return pd.DataFrame(rows)
