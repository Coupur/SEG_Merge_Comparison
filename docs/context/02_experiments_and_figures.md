# 02 — Experiments and the outputs we want

Every figure/table below maps to a proposal §7 output. Status legend: TODO / READY (inputs exist) / DONE.

| ID | Question | Inputs | Procedure | Output | Status |
|---|---|---|---|---|---|
| E0 | Does our analysis stack reproduce Schesch et al.? | Schesch results CSV | `scripts/reproduce_schesch_table.py` | `data/results/e0_schesch_reproduction.csv` | READY (run OK 2026-09-29) |
| E1 | How many scenarios per era, and how many survive each filter? | `scenarios.csv` + dates | `enrich_dates.py`, then histogram by year; record attrition per filter | Fig S1 date histogram; **Table 1 attrition** | TODO — this gates D4 |
| E2 | Control: does difficulty change across eras? | Git ort outcomes × era | ER_k of Git ort per era | Fig 1 control line | TODO (needs E1) |
| E3 | RQ1 decay | tool outcomes × era, env fixed | `decay_from_schesch.py` first; new runs later | **Fig 1**: one line per tool, ER_k vs era, one panel per k ∈ {1,2,4,8}, publication dates marked, outcome split + run time alongside | TODO (needs E1) |
| E4 | RQ2 environment sensitivity | tool × era × {published, modern} | resurrection + porting, rerun | **Fig 2** per tool/era Δ (dumbbell); **Table 2** porting effort (hours, changed lines, blockers) | TODO |
| E5 | RQ2 idea survival | GMerge/MergeGen idea vs plain modern LLM | 3 arms per era: original, ported, plain LLM | **Fig 3** grouped bars, ER_k per arm per era | TODO |
| E6 | RQ3 rank stability | ER_k matrix (tool × era × k) | ranks + Kendall τ per pair of eras and per pair of k | **Fig 4** rank lines + τ heatmap | TODO |
| E7 | Logs as data | `logs/resurrection`, `logs/porting` | tabulate status, hours, breakage class | Table 3 (effort) | TODO |

## Standing conventions
- Every ER_k point carries a bootstrap 95% CI (`metrics.bootstrap_ci`). Hand estimate for N = 200 with an ort-like mix (46/51/3 %): about ±0.07 at k = 1 but about ±0.19 at k = 8 [hand-computed, verify with `bootstrap_ci`]. Rank claims at k = 8 in small cells are therefore weak. Tool-vs-tool differences use the same scenarios, so a paired bootstrap over scenarios is tighter (TODO: implement).
- Also report `breakeven_k` (k where ER = 0) per tool; it summarizes the k-sensitivity in one number (Spork ≈ 6.06 in Schesch's data).
- Show main-branch and non-main-branch merges separately when N allows (proposal §8, "merge source").
- Supplementary Schesch-style plot: ER vs continuous k per era (paper Fig. 9 style).
- Never plot published-number (copied) values on the same axes as re-run values without a distinct marker (non-public tools: D12).

## Figure→file naming
`analysis/figures/fig1_decay.pdf`, `fig2_env_sensitivity.pdf`, `fig3_idea_survival.pdf`, `fig4_rank_stability.pdf`, `figS1_date_histogram.pdf`; tables as CSV in `data/results/` and LaTeX in `analysis/tables/`.
