"""Assemble proposal/src/*.md, fill {{placeholders}} from data/numbers.json,
write build/proposal.md."""
import json
import re
from pathlib import Path

from scripts.common import DATA, ROOT

SRC = ROOT / "proposal/src"
BUILD = ROOT / "build"
PLACEHOLDER = re.compile(r"\{\{(\w+)\}\}")


def render(text: str, values: dict) -> str:
    def sub(m):
        key = m.group(1)
        if key not in values:
            raise KeyError(key)
        v = values[key]
        return ", ".join(map(str, v)) if isinstance(v, list) else str(v)
    return PLACEHOLDER.sub(sub, text)


def assemble(src_dir: Path) -> str:
    parts = [p.read_text(encoding="utf-8").strip("\n") for p in sorted(src_dir.glob("*.md"))]
    return "\n\n".join(parts) + "\n"


def main() -> None:
    numbers = json.load((DATA / "numbers.json").open())
    BUILD.mkdir(exist_ok=True)
    (BUILD / "proposal.md").write_text(render(assemble(SRC), numbers), encoding="utf-8")
    print(f"build/proposal.md written from {len(list(SRC.glob('*.md')))} source files")


if __name__ == "__main__":
    main()
