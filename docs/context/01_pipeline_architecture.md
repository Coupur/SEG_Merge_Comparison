# 01 — Pipeline architecture: from theory to execution

## 1. Dataflow
```
Schesch results CSV (5,971 merges x 16 tools, committed in their repo)
        │  scripts/build_scenarios.py
        ▼
data/interim/scenarios.csv  ── scripts/enrich_dates.py (GitHub API: merge-commit dates) ──►  + merge_date, era
        │
        ├──► [FREE PATH]  join with Schesch outcomes ──► scripts/decay_from_schesch.py ──► ER_k per (tool, era)
        │
        └──► [BENCH PATH] scenarios × tool arms × environments
                 │  tools/<slug>/wrapper.sh   (contract in §2)
                 │  environments/<env_id>     (JDK, Git, model)
                 ▼
            data/results/runs.jsonl (RunRecord per merge)  ──► metrics.py ──► tables + figures (02_experiments_and_figures.md)
```

## 2. The three interfaces (this is the whole "bridge")
**(a) Scenario record** — `mergedrift.models.Scenario`. Minimal: repo, merge commit, parent1, parent2, branch, date, era.
**(b) Tool wrapper contract** — copied from Schesch's harness so tools plug into it unchanged:
```
tools/<slug>/wrapper.sh [--verbose] <clone_dir> <branch-1> <branch-2>
  merges branch-2 into branch-1 inside <clone_dir>
  exit 0 = clean merge · 1 = conflict (print "Conflict") · 2 = script failure
```
[verified: external/AST-Merging-Evaluation/src/scripts/merge_tools/*.sh, e.g. spork.sh, mergiraf.sh]. Tools that are git merge drivers are configured via `.gitattributes`.
LLM arms (proposed extension): the wrapper runs `git merge`; if it conflicts it calls the model per conflict, writes the resolution, exits 0. It also writes `run_meta.json` (model, version, settings, prompt hash, tokens, cost) next to the clone so cost lands in `RunRecord`.
**(c) Run record** — `mergedrift.models.RunRecord`; fields = proposal §9 "Run" log. Outcome comes from (exit code, build+test of merged tree, parents pass).

Outcome mapping [verified against Schesch Fig. 8 on 2026-09-29]: `Merge_failed`/`Merge_timedout` → unhandled · `Tests_passed` → correct · `Tests_failed` → incorrect.

## 3. Two environment axes (design decision — not in the proposal text)
The proposal's E mixes two things that must be recorded separately:
- **tool_env**: what the *tool* runs on — JDK, dependencies, Git version, or model + settings + price. Varied by resurrection/porting.
- **project_env**: what the *merged project* is built and tested with (JDK 8/11/17 chosen per project in Schesch's harness). Held fixed per project so the oracle does not move.
Some "environment effects" are really data effects: JDime's Java-8 syntax gap is about the language level of the *code being merged*, which correlates with era. Log both fields so the two can be separated later.

## 4. What is free and what costs work
| Cell | Status |
|---|---|
| Git ort, Spork, IntelliMerge, Mergiraf, Hires-Merge, Imports/IVn ... × all 5,971 merges × Schesch's 2024 harness environment | **Already computed** in their committed results. Needs only dates → era. |
| Same tools × other environments (published/older, newer) | Needs runs (build, test, 5×). Expensive: parent test timeout 30 min, merged 45 min. |
| JDime, GMerge, MergeGen, plain LLM | Not in Schesch's harness. Needs wrapper + resurrection/porting logs. |
Whether Schesch's environment counts as the "modern" cell or just "one cell" is open decision D5.

## 5. Harness strategy
Recommended (D10, proposed): **do not merge everything into one monolith.** Keep Schesch's harness as a pinned external checkout (later: your fork), add new tools as wrapper scripts following §2, and keep everything study-specific (dates, eras, environments, logs, analysis) in this repo. Reason: the proposal requires results labeled *published* vs *patched*; a monolith blurs which code changed.
Cache warning [unverified — read `src/python/cache_utils.py` first]: the harness caches test/merge results per commit or merge. Re-running a tool under a second environment may silently return cached results. Use a separate cache directory (harness supports `cache-small/` style dirs) or environment-suffixed tool names.

## 6. Harness facts to respect [verified: variables.py, README]
Merge timeout 15 min · parent test timeout 30 min · merged test timeout 45 min · `N_TESTS = 5` (test counted as passing if any run passes) · needs JDK 8, 11, 17 (`JAVA8_HOME` etc.), Maven 3.9.*, conda env `AST`, `gh`, `jq`, git-lfs; GraalVM 21+ by default for timing. Full 84 GB uncompressed cache only needed to *re-run*; results CSV is in git (18 MB).
