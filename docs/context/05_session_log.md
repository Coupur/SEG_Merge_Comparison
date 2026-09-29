# 05 — Session log (append only; newest last)

## 2026-09-29 — scaffold session
- Built repo skeleton and metrics; tests pin the proposal's worked example and Schesch Fig. 8 numbers (13 tests pass).
- Cloned Schesch harness (HEAD 9238a737, 2025-01-27); E0 reproduces the paper (Spork break-even k = 6.06).
- Found: merge dates are NOT in Schesch's data; committed results have 5,971 merges (paper: 6,045 collected, 5,983 in tables); Mergiraf is in the harness results though not in the paper.
- Untested: `enrich_dates.py` (GitHub API rate-limited from the sandbox).
- Next: Phase 0 in `04_plan_to_oct23.md`.
