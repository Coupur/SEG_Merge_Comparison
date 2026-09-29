"""Tests pin the metrics to numbers printed in the proposal and in Schesch et al."""
import pytest

from mergedrift.metrics import (breakeven_k, cost_units, effort_reduction, kendall_tau,
                                rank_tools, bootstrap_ci, er_from_outcomes)
from mergedrift.models import Outcome, outcome_from_schesch


# Proposal section 3 worked example: (unhandled, incorrect) per 100 merges.
SPORK = (35, 11)
ORT = (51, 3)


@pytest.mark.parametrize("k,spork,ort", [(1, 46, 54), (2, 57, 57), (4, 79, 63), (6, 101, 69), (8, 123, 75)])
def test_worked_example_table(k, spork, ort):
    assert cost_units(*SPORK, k) == spork
    assert cost_units(*ORT, k) == ort


def test_er_endpoints():
    assert effort_reduction(0, 0, 100, 4) == 1.0        # only correct merges
    assert effort_reduction(100, 0, 100, 4) == 0.0      # only unhandled = by hand
    assert effort_reduction(0, 100, 100, 4) < 0         # worse than no tool


def test_schesch_fig8_spork_breakeven_about_six():
    # Paper Fig. 8: Spork 3260 correct / 2080 unhandled / 643 incorrect (N=5983); paper says ~6.
    assert breakeven_k(2080, 643, 5983) == pytest.approx(6.07, abs=0.01)


def test_schesch_fig8_spork_best_at_k1_worse_than_ort_by_k2_or_so():
    n = 5983
    spork = lambda k: effort_reduction(2080, 643, n, k)
    ort = lambda k: effort_reduction(3078, 157, n, k)
    assert spork(1) > ort(1)
    assert spork(3) < ort(3)


def test_kendall_tau():
    a = {"x": 3, "y": 2, "z": 1}
    assert kendall_tau(a, a) == 1.0
    assert kendall_tau(a, {"x": 1, "y": 2, "z": 3}) == -1.0
    assert kendall_tau(a, {"x": 3, "y": 1, "z": 2}) == pytest.approx(1 / 3)


def test_rank_ties_share_rank():
    assert rank_tools({"a": 0.5, "b": 0.5, "c": 0.1}) == {"a": 1, "b": 1, "c": 3}


def test_outcome_mapping_and_loud_failure():
    assert outcome_from_schesch("Merge_timedout") is Outcome.UNHANDLED
    assert outcome_from_schesch("Tests_passed") is Outcome.CORRECT
    with pytest.raises(ValueError):
        outcome_from_schesch("Something_new")


def test_bootstrap_ci_brackets_point_estimate():
    outs = [Outcome.CORRECT] * 60 + [Outcome.UNHANDLED] * 35 + [Outcome.INCORRECT] * 5
    lo, hi = bootstrap_ci(outs, k=2)
    assert lo < er_from_outcomes(outs, 2) < hi
