from scripts.numbers import REDUNDANT, dead_labels, is_dead


def test_dead_rule():
    assert is_dead(6, 19, "23 status: testing")
    assert not is_dead(45, 9, "24 status: ready")      # still used in 2025
    assert not is_dead(1, 2, "11 prio: blocker")       # rare by nature, exempt
    assert not is_dead(9, 42, "02 type: regression")   # 42 open > 20


def test_dead_labels_from_rows():
    rows = [{"label": "35 needs: rebase", "open_issues": "0", "open_prs": "3", "created_since_2025_any_state": "0"},
            {"label": "01 type: bug", "open_issues": "599", "open_prs": "18", "created_since_2025_any_state": "596"}]
    assert dead_labels(rows) == ["35 needs: rebase"]


def test_redundant_set_is_fixed():
    assert len(REDUNDANT) == 7
    assert "24 status: ready" in REDUNDANT
