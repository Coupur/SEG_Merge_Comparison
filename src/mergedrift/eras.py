"""Era binning. Boundaries are PLACEHOLDERS from proposal section 6 (open decision D4)."""
from __future__ import annotations

from typing import Optional

import pandas as pd

ERAS: dict[str, tuple[int, int]] = {
    "E1_2015_16": (2015, 2016),
    "E2_2019_20": (2019, 2020),
    "E3_2023_24": (2023, 2024),
}


def assign_era(date_iso: Optional[str], eras: dict[str, tuple[int, int]] = ERAS) -> Optional[str]:
    if not date_iso or pd.isna(date_iso):
        return None
    year = pd.Timestamp(date_iso).year
    for name, (lo, hi) in eras.items():
        if lo <= year <= hi:
            return name
    return None
