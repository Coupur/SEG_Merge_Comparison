"""Shared record types. These mirror docs/context/01_pipeline_architecture.md.

Keep this file small: it is the contract between data, tools, bench, and analysis.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional


class Outcome(str, Enum):
    """Proposal section 3 taxonomy (Schesch et al.). One taxonomy for every tool."""

    UNHANDLED = "unhandled"  # tool reported conflicts (or timed out merging)
    CORRECT = "correct"      # no conflicts; builds and passes tests
    INCORRECT = "incorrect"  # no conflicts; fails build or tests


# Strings found in Schesch's results/combined/result_adjusted.csv (verified 2026-09-29).
# Merge_timedout counts as UNHANDLED: reproduces paper Fig. 8 for IntelliMerge
# (1238 Merge_failed + 344 Merge_timedout = 1582 unhandled).
SCHESCH_STATE_TO_OUTCOME = {
    "Merge_failed": Outcome.UNHANDLED,
    "Merge_timedout": Outcome.UNHANDLED,
    "Tests_passed": Outcome.CORRECT,
    "Tests_failed": Outcome.INCORRECT,
}


def outcome_from_schesch(state: str) -> Outcome:
    try:
        return SCHESCH_STATE_TO_OUTCOME[state]
    except KeyError as e:  # fail loudly: an unmapped state must be a conscious decision
        raise ValueError(f"Unmapped Schesch state {state!r}; decide and add it to models.py") from e


@dataclass
class Scenario:
    """One merge scenario. scenario_id = '<repo-idx>-<merge-idx>' as in Schesch's data."""

    scenario_id: str
    repo: str                      # 'owner/name'
    merge_commit: str
    parent1: str                   # Schesch 'left'
    parent2: str                   # Schesch 'right'
    branch_name: str               # raw, e.g. refs/heads/master
    source: Optional[str] = None   # 'main' | 'other' -- rule still TO DECIDE (see 03_decisions.md)
    merge_date: Optional[str] = None   # committer date of merge commit, ISO 8601
    era: Optional[str] = None
    data_origin: str = "schesch2024"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RunRecord:
    """One tool run on one scenario. Fields follow proposal section 9 ('Run' log).

    Two environment axes are recorded separately on purpose (see architecture doc):
      tool_env_id    -- what the TOOL runs on (JDK, deps, model+settings)
      project_env_id -- what the merged PROJECT is built/tested with
    """

    run_id: str
    scenario_id: str
    tool: str
    tool_commit: str
    tool_env_id: str
    project_env_id: str
    outcome: Outcome
    runtime_s: Optional[float] = None
    cost_usd: Optional[float] = None       # LLM arms
    tokens_in: Optional[int] = None
    tokens_out: Optional[int] = None
    test_runs: int = 5
    test_aggregation: str = "any_pass"     # Schesch rule; see 03_decisions.md D7
    label: str = "published"               # 'published' | 'patched'
    git_version: Optional[str] = None
    os: Optional[str] = None
    hardware: Optional[str] = None
    notes: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["outcome"] = self.outcome.value
        return d
