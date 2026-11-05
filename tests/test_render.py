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
