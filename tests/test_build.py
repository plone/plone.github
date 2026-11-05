import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_make_pdf_builds_and_uses_lato():
    subprocess.run(["make", "pdf"], cwd=ROOT, check=True, capture_output=True)
    pdf = ROOT / "build/proposal.pdf"
    assert pdf.exists()
    fonts = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
    assert "Lato" in fonts
    text = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout
    assert "Management summary" in text
    first_page = subprocess.run(["pdftotext", "-f", "1", "-l", "1", pdf, "-"], capture_output=True, text=True).stdout
    assert "Version" in first_page and "github.com/plone/plone.github" in first_page
