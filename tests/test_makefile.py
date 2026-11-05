import subprocess


def test_make_targets_declared():
    out = subprocess.run(["make", "-pn"], capture_output=True, text=True).stdout
    for t in ("test", "data", "numbers", "diagrams", "md", "pdf", "clean"):
        assert f"\n{t}:" in out, t
