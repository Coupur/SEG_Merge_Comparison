# CLAUDE.md — read this first

Project: **merge-drift** — a pilot study measuring how automated merge-tool results change with
*data era* and *environment*, instead of reporting one ranking from one snapshot.
Target: ICSE NIER short paper (4 pages), **due 2026-10-23**. Lead contact for the study: Alex (SEG lab, UniBE).
Owner: Sam.

## Source-of-truth order (when files disagree, higher wins)
1. `docs/context/03_decisions.md` — decisions already made
2. `docs/context/00_proposal.md` — the theory: RQs, formal framing, protocol, logging (frozen text; do not edit, supersede in 03)
3. `docs/context/01_pipeline_architecture.md` — how theory becomes code
4. `docs/context/02_experiments_and_figures.md` — experiments E0–E7 and the exact outputs wanted
5. `docs/papers/*.md` — per-paper notes and claim tables
6. Code in `src/mergedrift/` (tests in `tests/` pin the metrics to numbers printed in the papers)

## Repo map
| Path | What lives there |
|---|---|
| `docs/context/` | Everything an LLM needs to be productive. Numbered = read in order. |
| `docs/papers/` | One note per paper: claim table, dataset/env facts, discrepancies. |
| `tools/` | One folder per tool arm: `CARD.md`, pinned upstream ref, `patches/`, `wrapper.sh`. `registry.csv` = tool spreadsheet. |
| `data/` | `external/` (raw downloads), `interim/` (scenarios, dates), `eras/` (era datasets), `results/` (run outputs). Contents are gitignored; scripts regenerate them. |
| `logs/` | `resurrection/`, `porting/` = one markdown file per attempt (templates inside). `runs/` = machine logs. |
| `environments/` | Pinned environment definitions (JDK/Git/model) and the env-axis explanation. |
| `src/mergedrift/` | `models.py` (record types), `metrics.py` (ER_k, tau, bootstrap CI), `eras.py`, `analysis.py`. |
| `scripts/` | Numbered-by-purpose entry points; each has a docstring saying what it needs. |
| `external/` | Gitignored. Schesch et al.'s harness cloned at a pinned commit by `scripts/setup_external.sh`. |

## Rules for any LLM working here
1. **Provenance on every fact.** Write `[verified: <source>]` or `[unverified]`. Never invent a paper claim, number, URL, or artifact link; write `TO VERIFY` instead.
2. **The protocol is fixed; only era and environment vary.** One oracle (build + project tests, 5 runs), one taxonomy (unhandled/correct/incorrect), results always at k = 1, 2, 4, 8 — never a single ranking.
3. **No expected result.** Do not write text that presupposes decay, a rank flip, or that an idea survives.
4. **Never edit `external/` or vendored tool source.** Changes go in `tools/<slug>/patches/*.patch`, and any run using a patch is labeled `patched`, not `published`.
5. **Log effort the same day.** Every attempt to run or port a tool gets a `logs/resurrection/` or `logs/porting/` entry (hours, error, fix, patched?). Failing to run a tool is a result, not a failure to report.
6. **Report uncertainty.** ER_k per cell comes with a bootstrap CI (`metrics.bootstrap_ci`). Cells are small.
7. **Keep environments separate.** Record `tool_env_id` and `project_env_id` as different fields (see architecture doc §3).
8. **After changing metrics or the outcome mapping, run `pytest`.** Then re-run `scripts/reproduce_schesch_table.py` (E0) and confirm numbers still match Schesch et al. within the documented N difference.
9. **End every session** by appending to `docs/context/05_session_log.md` (what changed, what is next) and updating status in `docs/context/04_plan_to_oct23.md`.

## Vocabulary (details in the proposal §1–5)
- **Scenario** = one merge: base, parent 1 (`left`), parent 2 (`right`), developer resolution. **Era** = bin of merge-commit dates.
- **Unhandled** = tool reports conflict. **Correct** = clean + builds + tests pass. **Incorrect** = clean + fails build/tests.
- **k** = cost of an incorrect merge relative to an unhandled one. **ER_k** = 1 − (U + kI)/N.
- **Cell** = one (tool, environment, era) triple. **Arm** = one tool configuration in the study.
- **Resurrection** = getting a tool to run in its published environment. **Porting** = moving a tool or its idea to a modern environment.

## Commands
```
pip install -e ".[dev]" && pytest              # verify metrics
./scripts/setup_external.sh                    # clone Schesch harness at pinned commit
python scripts/reproduce_schesch_table.py      # E0
python scripts/build_scenarios.py              # data/interim/scenarios.csv
GITHUB_TOKEN=... python scripts/enrich_dates.py --limit 5   # then without --limit
python scripts/decay_from_schesch.py           # first decay table (needs dates)
```
