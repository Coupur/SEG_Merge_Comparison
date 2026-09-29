#!/usr/bin/env python
"""E0: reproduce Schesch et al. outcome split + ER_k from their committed results.

Usage: python scripts/reproduce_schesch_table.py [results_csv] [repos_csv]
Sanity check for the whole analysis stack. Expect numbers close to (not identical to) paper Fig. 8:
the paper tables have N=5983; the committed results have N=5971 (see docs/papers/schesch2024_evaluation.md).
"""
import sys
from pathlib import Path

import pandas as pd

from mergedrift.analysis import er_table, load_schesch_long

root = Path("external/AST-Merging-Evaluation")
results = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "results/combined/result_adjusted.csv"
repos = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "input_data/repos_combined.csv"

long = load_schesch_long(results, repos)
tab = er_table(long, by=["tool"]).sort_values("ER_k1", ascending=False)
pd.set_option("display.width", 200)
print(f"scenarios: {long['scenario_id'].nunique()}   tools: {long['tool'].nunique()}\n")
print(tab.to_string(index=False))
out = Path("data/results/e0_schesch_reproduction.csv")
out.parent.mkdir(parents=True, exist_ok=True)
tab.to_csv(out, index=False)
print(f"\nwrote {out}")
