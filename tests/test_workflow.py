from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_workflow_shape():
    wf = yaml.safe_load((ROOT / ".github/workflows/pdf.yml").read_text())
    on = wf.get(True, wf.get("on"))
    assert "push" in on and "pull_request" in on
    assert on["push"]["tags"] == ["proposal-v*"]
    steps = " ".join(s.get("run", "") + " " + s.get("uses", "") for s in wf["jobs"]["pdf"]["steps"])
    for needle in ("fonts-lato", "make test", "make pdf", "upload-artifact", "gh release create"):
        assert needle in steps, needle
    assert wf["permissions"]["contents"] == "write"
