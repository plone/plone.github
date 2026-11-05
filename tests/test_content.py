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


def test_wrong_claims_are_gone():
    text = _all_text()
    for s in ["half of it is unused",
              "Every repository created since late 2019",
              "keep working as filters after the rename",
              "Every one of them groups by its Status field",
              "everything outside the 2015 set, are never touched",
              "Of the organization's {{projects_total}} boards"]:
        assert s not in text, s
    assert "type:PLIP" in text and "type:Task" in text
    assert "Labels not listed in Appendix A are never touched" in text


def test_readme_layout_names_scripts_dir():
    readme = (SRC.parents[1] / "README.md").read_text()
    assert "data/scripts" not in readme and "scripts/" in readme and "tests/" in readme
