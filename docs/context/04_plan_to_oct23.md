# 04 — Plan to the deadline (2026-10-23)

Today is 2026-09-29. 24 days. Status legend: [ ] todo · [~] in progress · [x] done.

## Phase 0 — before the Oct 2 meeting with Alex
- [x] Repo skeleton, metrics with tests, E0 reproduces Schesch (done in the scaffold)
- [ ] `git init`, push, run `pip install -e ".[dev]" && pytest`, `./scripts/setup_external.sh`, E0
- [ ] `scripts/build_scenarios.py` and `enrich_dates.py --limit 5`, then full date run (about 1–2 h with a token) → **Fig S1: how many merges per year?**
- [ ] `tools/registry.csv`: fill every TO VERIFY (year, artifact link, availability)
- [ ] Claim tables for 3–4 papers (Schesch drafted; add Spork, GMerge, LastMerge or MergeBERT)
- [ ] One resurrection attempt with a log (suggest JDime — cheapest way to learn what "does not run" looks like)
- [ ] Bring D1–D3, D5 to Alex

## Phase 1 — data and first result (Oct 3–9)
- [ ] E1 attrition + era histogram → decide D4
- [ ] E2/E3 first decay table from Schesch's outcomes (needs no tool runs)
- [ ] `make small-test` in the harness, in Docker or Linux with JDK 8/11/17

## Phase 2 — new arms (Oct 10–16)
- [ ] Wrapper + resurrection for JDime; decide the model-bound arm (D6, D11)
- [ ] Re-run of one tool in a second environment on a small slice; check the cache warning first (architecture §5)

## Phase 3 — analysis and writing (Oct 17–23)
- [ ] Freeze runs Oct 19; figures Fig 1–4, Table 1–3
- [ ] Draft the 4 pages from Oct 14 in parallel — do not wait for Phase 2
- [ ] Submit Oct 23

## Fallback (the honest minimum pilot)
If Phase 2 slips: RQ1 decay and RQ3 rank stability on tools whose outcomes already exist (Git ort, Spork, IntelliMerge, Mergiraf, others), plus resurrection/porting logs for JDime and one LLM idea. Per proposal §9, "does not run" and time-to-port are themselves results.
