# merge-drift

Pilot study: how do merge-tool results change with data era and environment?
Start with `CLAUDE.md` (LLM entry point) and `docs/context/00_proposal.md` (the study).

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]" && pytest
./scripts/setup_external.sh
python scripts/reproduce_schesch_table.py
python scripts/build_scenarios.py
```
Java 8/11/17, Maven 3.9, conda, `gh`, `jq` are only needed once you re-run tools (see `environments/README.md`).
