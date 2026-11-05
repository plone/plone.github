from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "proposal/src"


def _all_text():
    return "\n".join(p.read_text() for p in sorted(SRC.glob("*.md")))


def test_required_sentences_present():
    text = _all_text()
    for s in ["This is an invitation, not a rule.",
              "an issue has a definition of done",
              "`needs: triage`", "`needs: info`", "`help wanted`", "`good first issue`",
              "`blocker`", "`accessibility`", "`i18n`", "`documentation`",
              "blank_issues_enabled: false", "\\tableofcontents"]:
        assert s in text, s


def test_no_bot_as_label_automation():
    assert "roboto" not in _all_text().lower()
