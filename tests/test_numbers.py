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


def test_fetch_date_reads_record(tmp_path):
    import json
    from scripts.numbers import fetch_date
    (tmp_path / "fetched_at.json").write_text(json.dumps({"date": "2026-11-05"}))
    assert fetch_date(tmp_path) == "2026-11-05"


def test_date_is_independent_of_file_mtime(tmp_path):
    import os
    import shutil
    import time
    from pathlib import Path
    from scripts.numbers import compute
    data = Path(__file__).resolve().parents[1] / "data"
    for f in data.iterdir():
        if f.is_file():
            shutil.copy(f, tmp_path / f.name)
    future = time.time() + 400 * 86400
    os.utime(tmp_path / "plone_labels.json", (future, future))
    assert compute(tmp_path)["date"] == "2026-11-05"


def test_projects_counts_are_public_only():
    import json
    from pathlib import Path
    from scripts.numbers import compute
    data = Path(__file__).resolve().parents[1] / "data"
    boards = json.load((data / "projects.json").open())["boards"]
    n = compute(data)
    assert n["projects_total"] == len(boards)
    assert n["projects_open"] == sum(1 for b in boards if not b["closed"])
    assert "private_boards_omitted" not in json.load((data / "projects.json").open())
