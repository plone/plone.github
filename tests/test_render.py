import pytest

from scripts.render import assemble, render


def test_render_substitutes():
    assert render("{{a}} repos", {"a": 3}) == "3 repos"


def test_render_joins_lists():
    assert render("dead: {{d}}", {"d": ["x", "y"]}) == "dead: x, y"


def test_render_unknown_placeholder_fails():
    with pytest.raises(KeyError):
        render("{{nope}}", {})


def test_assemble_sorted(tmp_path):
    (tmp_path / "02-b.md").write_text("B")
    (tmp_path / "01-a.md").write_text("A")
    assert assemble(tmp_path) == "A\n\nB\n"


def test_appendix_b_lists_dead_and_redundant():
    from pathlib import Path
    from scripts.render import appendix_b
    md = appendix_b(Path(__file__).resolve().parents[1] / "data")
    assert "35 needs: rebase" in md and "dead" in md and "24 status: ready" in md


def test_appendix_c_lists_the_2015_scheme():
    from pathlib import Path
    from scripts.render import appendix_c
    root = Path(__file__).resolve().parents[1]
    md = appendix_c(root / "archive/google-sheet/Github-Plone-Organisation-Labels-2026-11-05.csv",
                    root / "archive/2015-label-tool/definitions.json")
    assert "01 type: bug" in md and "fa0000" in md and "something does not work" in md


def test_appendix_b_board_table_shows_sample_size_and_right_path():
    from pathlib import Path
    from scripts.render import appendix_b
    md = appendix_b(Path(__file__).resolve().parents[1] / "data")
    assert "Sampled" in md
    assert "data/scripts" not in md and "`scripts/`" in md


def test_render_rejects_leftover_braces():
    with pytest.raises(ValueError):
        render("{{ key }} stays", {"key": 1})
