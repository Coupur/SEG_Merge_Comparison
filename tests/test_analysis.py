import pandas as pd

from mergedrift.analysis import er_table


def test_er_table_groups_by_tool_and_era():
    long = pd.DataFrame({
        "tool": ["a"] * 4 + ["b"] * 4,
        "era": ["E1", "E1", "E2", "E2"] * 2,
        "outcome": ["correct", "unhandled", "correct", "incorrect",
                    "unhandled", "unhandled", "correct", "correct"],
    })
    t = er_table(long, by=["tool", "era"], ks=[1, 2]).set_index(["tool", "era"])
    assert t.loc[("a", "E1"), "ER_k1"] == 0.5
    assert t.loc[("a", "E2"), "ER_k2"] == 0.0     # 1 - (0 + 2*1)/2 = 0? -> 1-1 = 0
    assert t.loc[("b", "E1"), "ER_k1"] == 0.0
    assert t.loc[("b", "E2"), "ER_k1"] == 1.0
