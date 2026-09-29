"""Metrics from proposal sections 3 and 5. Pure functions, no I/O.

Cost(T)  = (U + k*I) * c_U          ER_k(T) = 1 - (U + k*I) / N
tau      = (P_agree - P_flip) / (n(n-1)/2)
"""
from __future__ import annotations

from itertools import combinations
from typing import Iterable, Mapping, Sequence

import numpy as np

from .models import Outcome

KS = (1, 2, 4, 8)


def split(outcomes: Iterable[Outcome]) -> tuple[int, int, int]:
    """Return (unhandled, correct, incorrect) counts."""
    u = c = i = 0
    for o in outcomes:
        if o == Outcome.UNHANDLED:
            u += 1
        elif o == Outcome.CORRECT:
            c += 1
        elif o == Outcome.INCORRECT:
            i += 1
        else:
            raise ValueError(o)
    return u, c, i


def cost_units(u: int, i: int, k: float) -> float:
    """Developer cost in units of one unhandled merge (c_U = 1)."""
    return u + k * i


def effort_reduction(u: int, i: int, n: int, k: float) -> float:
    if n <= 0:
        raise ValueError("n must be positive")
    return 1.0 - (u + k * i) / n


def breakeven_k(u: int, i: int, n: int) -> float:
    """k at which ER_k = 0, i.e. the tool is no better than resolving everything by hand."""
    return float("inf") if i == 0 else (n - u) / i


def er_from_outcomes(outcomes: Sequence[Outcome], k: float) -> float:
    u, _, i = split(outcomes)
    return effort_reduction(u, i, len(outcomes), k)


def bootstrap_ci(outcomes: Sequence[Outcome], k: float, n_boot: int = 2000,
                 alpha: float = 0.05, seed: int = 0) -> tuple[float, float]:
    """Percentile bootstrap CI for ER_k. Report this: per-cell samples are small."""
    rng = np.random.default_rng(seed)
    # per-merge cost contribution: unhandled=1, incorrect=k, correct=0
    cost = np.array([1.0 if o == Outcome.UNHANDLED else (k if o == Outcome.INCORRECT else 0.0)
                     for o in outcomes])
    n = len(cost)
    idx = rng.integers(0, n, size=(n_boot, n))
    ers = 1.0 - cost[idx].mean(axis=1)
    return float(np.quantile(ers, alpha / 2)), float(np.quantile(ers, 1 - alpha / 2))


def rank_tools(scores: Mapping[str, float]) -> dict[str, int]:
    """Rank 1 = highest ER. Ties share the better rank."""
    ordered = sorted(scores.items(), key=lambda kv: -kv[1])
    ranks: dict[str, int] = {}
    prev, prev_rank = None, 0
    for pos, (tool, s) in enumerate(ordered, start=1):
        rank = prev_rank if prev is not None and s == prev else pos
        ranks[tool], prev, prev_rank = rank, s, rank
    return ranks


def kendall_tau(scores_a: Mapping[str, float], scores_b: Mapping[str, float]) -> float:
    """Proposal formula. Pairs tied in either ranking count as neither agree nor flip."""
    tools = sorted(set(scores_a) & set(scores_b))
    n = len(tools)
    if n < 2:
        raise ValueError("need at least two common tools")
    agree = flip = 0
    for x, y in combinations(tools, 2):
        da, db = scores_a[x] - scores_a[y], scores_b[x] - scores_b[y]
        if da == 0 or db == 0:
            continue
        if (da > 0) == (db > 0):
            agree += 1
        else:
            flip += 1
    return (agree - flip) / (n * (n - 1) / 2)


def environment_delta(er_modern: float, er_published: float) -> float:
    """Delta_{T,k}(t) in the proposal."""
    return er_modern - er_published


def idea_gain(er_ported: float, er_plain_llm: float) -> float:
    """G_k(t) in the proposal: ported idea vs plain modern LLM."""
    return er_ported - er_plain_llm
