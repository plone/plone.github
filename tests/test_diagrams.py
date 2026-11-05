import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_diagrams_render(tmp_path):
    for name in ("triage-flow", "then-now"):
        out = tmp_path / f"{name}.pdf"
        subprocess.run(["dot", "-Tpdf", "-o", out, ROOT / f"proposal/diagrams/{name}.dot"], check=True)
        assert out.read_bytes()[:4] == b"%PDF"
