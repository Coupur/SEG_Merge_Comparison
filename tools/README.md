# tools/

One folder per tool arm. Contract for `wrapper.sh` is in `docs/context/01_pipeline_architecture.md` §2:
`wrapper.sh [--verbose] <clone_dir> <branch-1> <branch-2>` → exit 0 clean, 1 conflict, 2 script failure.

Folder layout (copy `_TEMPLATE/`):
```
tools/<slug>/
  CARD.md        status, paper, artifact, environment binding, resurrection/porting log links
  PIN            upstream URL + commit/tag/model version (one line each)
  patches/       *.patch applied to the pinned upstream; any run using one is labeled 'patched'
  wrapper.sh     conforms to the contract; for tools already in Schesch's harness, link to its script instead
```
Upstream source is cloned into `external/tools/<slug>/` (gitignored), never edited in place.
`registry.csv` is the tool spreadsheet from the proposal ("Before the meeting with Alex"): year, paradigm, environment binding, artifact link, availability, slot. Every `TO VERIFY` must be resolved from the paper or the repo, not from memory.
