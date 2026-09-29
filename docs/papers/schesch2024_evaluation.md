# Schesch et al. (2024), "Evaluation of Version Control Merge Tools" — ASE 2024

Anchor paper of the study. Read in full 2026-09-29 (arXiv v1, 2410.09934). Harness inspected at commit 9238a737 (2025-01-27).

## Links [verified: paper + harness README]
- Paper: https://arxiv.org/pdf/2410.09934 · DOI 10.1145/3691620.3695075
- Code: https://github.com/benedikt-schesch/AST-Merging-Evaluation
- Data (results cache): https://zenodo.org/records/13366866 (DOI 10.5281/zenodo.13366866; v3 seen, a newer version exists)
- New tools (Imports, IVn ...): https://github.com/plume-lib/merging
- Appendix: UW-CSE-24-09-01 (75 analyzed merges) — not yet read

## Claim table
| Claim | Metric | Dataset | Environment | Baselines | Artifact |
|---|---|---|---|---|---|
| Ranking depends on k: Spork best at k=1, worst except IntelliMerge by k≈2, worse than manual at k≈6 (§1, §6.2) | ER_k, tests as oracle | 5,983 merges in tables (6,045 collected), 1,120 Java repos | JDK 8/11/17 per project; i9-13900KF; tool versions TO VERIFY | All tools re-run by the authors via wrappers | Code + Zenodo, public |
| IntelliMerge rarely applicable; ~50% incorrect vs Git Merge 3% (Fig. 8) | outcome split | same | same | same | public |
| Imports (Git Merge + import re-merge) beats Spork and IntelliMerge; IVn best except k≈1 | ER_k | same | same | same | public |
| Non-main-branch merges are harder; relative ranking similar (Fig. 12, §6.3) | outcome split by source | 3,524 main / 2,459 other | same | same | public |
| ort ≈ recursive when both use Myers; ort-ignorespace beats ort for k<5 (§6.1) | ER_k | same | Git version TO VERIFY | 7 Git configs | public |

## Data facts [verified: paper Fig. 4, §5]
Repo sets: GitHub's Greatest Hits (published Nov 2020) and Reaper (Munaiah et al. 2017, from GHTorrent). Funnel: 42,092 Java repos → 4,072 (head passes tests, 294,714 merges) → 1,653 (java diff, 21,860 merges) → 1,120 repos / 6,045 merges (both parents pass). Imports involved in 93% of final merges. Test coverage on 100 random projects: mean 53% (JaCoCo). Non-main-branch merges of deleted branches were fetched from GitHub.
Because the repo lists date from 2017–2020, **coverage of the 2023–24 era may be thin** [inference — check with E1].

## Harness facts [verified: repo]
- Merge dates are **not** stored in their data (`merges/*.csv` columns: idx, branch_name, merge_commit, parent_1, parent_2, notes). We add them (`scripts/enrich_dates.py`).
- Outcome strings: Merge_failed, Merge_timedout, Tests_passed, Tests_failed. Timeouts: merge 15 min, parent tests 30 min, merged tests 45 min. `N_TESTS = 5`, success if any run passes.
- `result_adjusted.csv` (18 MB, 5,971 rows, 93 columns) differs from `result_raw.csv`; `_adjusted` reclassifies unhandled→incorrect when the IVn fix-up finishes the merge and tests fail (paper §4.1). Use adjusted unless stated.
- The harness now includes **Mergiraf**, which the paper does not evaluate ("the framework has been expanded", README).

## Numbers from the committed results (scripts/reproduce_schesch_table.py, N = 5,971)
| Tool | unhandled | correct | incorrect | ER_k1 | ER_k4 | ER_k8 | break-even k |
|---|---|---|---|---|---|---|---|
| mergiraf | 2180 | 3456 | 335 | 0.579 | 0.411 | 0.186 | 11.3 |
| spork | 2079 | 3250 | 642 | 0.544 | 0.222 | -0.208 | 6.06 |
| gitmerge_ort | 3074 | 2741 | 156 | 0.459 | 0.381 | 0.276 | 18.6 |
| intellimerge | 1582 | 1429 | 2960 | 0.239 | -1.248 | -3.231 | 1.48 |
Git ort, recursive-histogram, -myers, -minimal give identical counts, consistent with §6.1.1.

## Discrepancies to resolve before writing
1. **N**: 6,045 (README, paper Fig. 4) vs 5,983 (paper results tables) vs 5,971 (committed results). Cite the N you analyze (D8).
2. **Git ort default year**: paper §2.3.1 says ort became default in 2023; from memory Git 2.34 (Nov 2021) made it the default [unverified — check Git release notes]. The proposal §4 repeats the 2023 claim.
3. **Timeout wording**: paper §4.1 says timeouts are labeled incorrect, but Fig. 8 counts IntelliMerge's 344 merge timeouts as unhandled (1238 + 344 = 1582). We follow the table. Test timeouts are handled in `repo.py` (not analyzed yet).
4. The proposal's "Spork (Java 17, per Alex)" is not from this paper; keep it attributed to Alex until verified.

## Proposal claims checked against the paper
Verified: 54/35/11 and 46/51/3 splits; 93% imports; IntelliMerge ~50% incorrect vs 3%; >1 person-month on Spork; JDime lacks full Java 8 syntax; five test runs; non-main-branch merges harder.
