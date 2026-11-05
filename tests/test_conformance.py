from scripts.conformance import canon_from_sheet, classify, normalize


def test_full_set_is_A(canon27):
    assert classify(sorted(canon27), canon27)["cls"] == "A full"


def test_deferred_drift(canon27):
    labels = [l for l in canon27 if l != "25 status: deferred"] + ["24 status: deferred"]
    r = classify(labels, canon27)
    assert r["score"] == 27
    assert r["drift"] == {"24 status: deferred": "25 status: deferred"}
    assert r["cls"] == "A full"


def test_github_defaults_are_F(canon27):
    r = classify(["bug", "enhancement", "question", "wontfix"], canon27)
    assert r["cls"] == "F none"
    assert r["extras"] == ["bug", "enhancement", "question", "wontfix"]


def test_extras_exclude_99_and_bot_labels(canon27):
    r = classify(sorted(canon27) + ["99 tag: sprint", "dependencies", "skip changelog"], canon27)
    assert r["cls"] == "B full+extras"
    assert r["extras"] == ["skip changelog"]
    assert r["tag99"] == ["99 tag: sprint"]


def test_colon_variant_counts():
    assert normalize("51: target: patch") == "51 target: patch"
    assert normalize("  01 Type:  Bug ") == "01 type: bug"


def test_canon_from_sheet_excludes_06_and_99(tmp_path):
    p = tmp_path / "sheet.csv"
    p.write_text("Color,Label,Description,,Color,Label,Description\n"
                 ",01 type: bug,something does not work,,,21 status: confirmed,issue was read\n"
                 ",06 type: accessibility,proposed! ,,,,\n"
                 ",,,,,99 tag: {others},free form labels\n"
                 ",43 lvl: complex,for wizards,,,51: target: patch,release target is a patch\n")
    c = canon_from_sheet(p)
    assert set(c) == {"01 type: bug", "21 status: confirmed", "43 lvl: complex", "51 target: patch"}
    assert c["01 type: bug"] == "something does not work"
