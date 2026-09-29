#!/usr/bin/env python
"""First decay table: ER_k per (tool, era) using Schesch's existing outcomes + our dates.

Needs data/interim/scenarios.csv with merge_date/era filled (scripts/enrich_dates.py).
CAVEAT: Schesch's runs used one 2024-era harness environment for every tool, so this is ONE
environment cell, not the 'published' environment (see docs/context/01_pipeline_architecture.md).
"""
from pathlib import Path

import pandas as pd

from mergedrift.analysis import er_table, load_schesch_long

root = Path("external/AST-Merging-Evaluation")
long = load_schesch_long(root / "results/combined/result_adjusted.csv", root / "input_data/repos_combined.csv")
scen = pd.read_csv("data/interim/scenarios.csv", dtype=str, keep_default_na=False)[["scenario_id", "era", "merge_date"]]
long = long.merge(scen, on="scenario_id", how="left")
print("scenarios per era:\n", long.drop_duplicates("scenario_id")["era"].replace("", "none").value_counts().to_string(), "\n")
long = long[long["era"] != ""]
tab = er_table(long, by=["tool", "era"])
pd.set_option("display.width", 220)
print(tab.sort_values(["tool", "era"]).to_string(index=False))
Path("data/results").mkdir(parents=True, exist_ok=True)
tab.to_csv("data/results/e3_decay_schesch_env.csv", index=False)
