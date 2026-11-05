"""Paths and the canonical 2015 label list, shared by the fetchers."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DEFINITIONS = ROOT / "archive/2015-label-tool/definitions.json"
SHEET_CSV = ROOT / "archive/google-sheet/Github-Plone-Organisation-Labels-2026-11-05.csv"
SINCE = "2025-01-01"
BOT_LABELS = {"dependencies", "github_actions", "javascript", "python", "docker", "npm", "pip",
              "pre-commit.ci autofix", "github-actions", "submodules"}


def canonical_labels() -> list[str]:
    """The 27 labels of the 2015 scheme, in the tool's normalized spelling."""
    return list(json.load(DEFINITIONS.open())["LABELS"].keys())


def normalize(name: str) -> str:
    """'51: target: patch' -> '51 target: patch', lower-cased, single spaces."""
    return re.sub(r"\s+", " ", re.sub(r"^(\d\d):", r"\1", name.strip().lower()))


def load_repos(active_only: bool = False) -> list[dict]:
    repos = json.load((DATA / "plone_labels.json").open())
    return [r for r in repos if not (active_only and r["archived"])]


def gh_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')
