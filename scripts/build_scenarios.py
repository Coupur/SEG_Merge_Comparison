#!/usr/bin/env python
"""Build data/interim/scenarios.csv (one row per merge scenario) from Schesch's results.

Dates are NOT in Schesch's data; run scripts/enrich_dates.py next.
"""
import sys
from pathlib import Path

import pandas as pd

root = Path("external/AST-Merging-Evaluation")
results = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "results/combined/result_adjusted.csv"
repos = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "input_data/repos_combined.csv"

df = pd.read_csv(results, low_memory=False)
r = pd.read_csv(repos).rename(columns={"idx": "repo-idx", "repository": "repo"})
df = df.merge(r, on="repo-idx", how="left")
out = pd.DataFrame({
    "scenario_id": df["idx"], "repo": df["repo"], "merge_commit": df["merge"],
    "parent1": df["left"], "parent2": df["right"], "branch_name": df["branch_name"],
    "source": "", "merge_date": "", "era": "", "data_origin": "schesch2024",
})
dest = Path("data/interim/scenarios.csv")
dest.parent.mkdir(parents=True, exist_ok=True)
out.to_csv(dest, index=False)
print(f"wrote {dest}: {len(out)} scenarios, {out['repo'].nunique()} repos, missing repo names: {out['repo'].isna().sum()}")
