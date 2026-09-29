# 03 — Decisions

Status: OPEN / PROPOSED (my suggestion, not yet agreed) / DECIDED. Move rows to the bottom once DECIDED and add the date and who agreed.

| ID | Decision | Status | Proposed default and why | Needed by |
|---|---|---|---|---|
| D1 | Outcome taxonomy: unhandled/correct/incorrect vs better/comparable/unresolved/worse | OPEN | Keep Schesch's three (ER_k needs them; the four-way one needs human resolutions). Ask Alex whether the previous study's taxonomy is also wanted as secondary. | Oct 2 |
| D2 | Tool shortlist incl. the resource-bound slot | OPEN | Control: Git ort. Version-bound: Spork + JDime. Scope-limited: IntelliMerge. Model-bound: GMerge or MergeGen + plain LLM. Resource-bound: TBD (ask Alex). Add Mergiraf as a free extra arm — its outcomes already exist in Schesch's results. | Oct 2 |
| D3 | Reuse the previous study's harness vs Schesch's infrastructure | OPEN | Schesch's is public, has wrappers, cache and CI (`make small-test`). Ask Alex what "previous study's harness" is and whether it is better. | Oct 2 |
| D4 | Era boundaries and sample size per cell | OPEN | Blocked on E1 (date histogram). Placeholders 2015–16 / 2019–20 / 2023–24 are in `eras.py`. | after E1 |
| D5 | Does Schesch's 2024 harness run count as the "modern environment" cell, or as a third cell? | OPEN | Treat as its own cell `harness_2024` until agreed; do not relabel. | Oct 2 |
| D6 | GMerge base model (GPT-3 vs GPT-J) and how non-public tools are handled | OPEN | Read GMerge §method for the model; resolve in its claim table. | Oct 9 |
| D7 | Flaky-test aggregation over 5 runs | PROPOSED | "Any run passes" as in Schesch [verified: variables.py N_TESTS=5; paper §5.2] for comparability; report flake rate per era. The proposal says five runs but not the rule. | Oct 9 |
| D8 | Canonical N | PROPOSED | Analyze the committed results (5,971 merges, 1,116 repos) and say so; mention 6,045 as collected. See paper note for the 6,045 / 5,983 / 5,971 discrepancy. | now |
| D9 | Source of merge dates | PROPOSED | GitHub REST by SHA (works for deleted-branch merges; about 6k calls, needs a token). Local clones only as fallback. | now |
| D10 | Harness strategy | PROPOSED | Pinned external checkout, later a fork for patches; study code stays in this repo. See architecture §5. | now |
| D11 | Plain-LLM arm: model, prompt, budget | OPEN | Pin model name + version + date + settings; estimate cost per 100 merges before choosing. | Oct 9 |
| D12 | Tools that are not public (AutoMerge, DeepMerge, MergeBERT, GMerge) | OPEN | Reported numbers only, drawn in a separate style, never mixed with re-run numbers. | Oct 9 |

## DECIDED
Here are my decitions on these topics

