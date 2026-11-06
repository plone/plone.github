import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "proposal/src"
BANNED = ["shrink", "clog", "noise", "inbox", "backlog size", "minutes, not hours", "efficien"]


def _files():
    files = sorted(SRC.glob("*.md"))
    post = ROOT / "proposal/forum-post.md"
    return files + ([post] if post.exists() else [])


def test_language_rules():
    for f in _files():
        low = f.read_text().lower()
        for w in BANNED:
            assert w not in low, f"{w!r} in {f.name}"


def test_no_hardcoded_counts():
    pat = re.compile(r"\b\d{2,4} (repos|repositories|labels|issues|boards|pull requests)\b", re.I)
    for f in SRC.glob("*.md"):
        m = pat.search(f.read_text())
        assert not m, f"{f.name}: {m.group(0)!r}"


def test_no_ai_focus():
    for f in _files():
        text = f.read_text().strip()
        if f.name == "forum-post.md":
            text = "\n".join(text.splitlines()[:-1])  # the owner's transparency line may name AI
        assert not re.search(r"\bLLM\b|\bAI\b|Copilot", text), f.name


def test_forum_post_length_and_trailer():
    text = (ROOT / "proposal/forum-post.md").read_text().strip()
    lines = text.splitlines()
    assert re.search(r"(?i)assisted-by:? Claude Fable 5\.1", lines[-1]), lines[-1]
    body = "\n".join(lines[:-1])
    assert len(body.split()) <= 350, len(body.split())
    assert "https://github.com/plone/plone.github/releases/download/proposal-v" in body
