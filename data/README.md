# data/

Everything except this README and `.gitkeep` files is gitignored and regenerable.

| Folder | Content | Produced by |
|---|---|---|
| `external/` | Raw downloads (e.g. Zenodo cache) | manual, see `scripts/setup_external.sh` |
| `interim/` | `scenarios.csv` (one row per merge), `merge_dates.csv` (API cache) | `build_scenarios.py`, `enrich_dates.py` |
| `eras/` | One CSV per era, sampled per cell | TODO after decision D4 |
| `results/` | `e0_*.csv`, `e3_*.csv`, `runs.jsonl` | scripts + bench |

`scenarios.csv` columns: scenario_id, repo, merge_commit, parent1, parent2, branch_name, source, merge_date, era, data_origin. `scenario_id` = `<repo-idx>-<merge-idx>` from Schesch's data. `source` (main vs other branch) is empty until its derivation rule is decided.
