from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / "archive/google-sheet/Github-Plone-Organisation-Labels-2026-11-05"


def test_sheet_csv_has_06_row():
    csv = (SHEET.with_suffix(".csv")).read_text()
    assert "06 type: accessibility" in csv
    assert "51: target: patch" in csv  # the sheet as it is, typo included


def test_sheet_pdf_present():
    assert SHEET.with_suffix(".pdf").read_bytes()[:4] == b"%PDF"


def test_old_tool_archived():
    assert (ROOT / "archive/2015-label-tool/definitions.json").exists()
    assert not (ROOT / "definitions.json").exists()
