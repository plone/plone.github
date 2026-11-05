from pathlib import Path

import pytest

from scripts.conformance import canon_from_sheet

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def canon27():
    c = canon_from_sheet(ROOT / "archive/google-sheet/Github-Plone-Organisation-Labels-2026-11-05.csv")
    assert len(c) == 27
    return set(c)
