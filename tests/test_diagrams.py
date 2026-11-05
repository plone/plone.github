import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_diagrams_render(tmp_path):
    for name in ("triage-flow", "then-now"):
        out = tmp_path / f"{name}.pdf"
        subprocess.run(["dot", "-Tpdf", "-o", out, ROOT / f"proposal/diagrams/{name}.dot"], check=True)
        assert out.read_bytes()[:4] == b"%PDF"


def test_triage_flow_is_legible_at_text_width(tmp_path):
    out = tmp_path / "t.pdf"
    subprocess.run(["dot", "-Tpdf", "-o", out, ROOT / "proposal/diagrams/triage-flow.dot"], check=True)
    info = subprocess.run(["pdfinfo", out], capture_output=True, text=True).stdout
    width = float(next(l for l in info.splitlines() if l.startswith("Page size")).split()[2])
    assert width <= 680, width  # 453 pt text width / 680 keeps 11 pt labels above 7 pt
