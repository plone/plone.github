"""Thin wrapper around ``gh api graphql`` with retries, plus the visibility filter."""
import json
import subprocess
import time


def gql(query: str, **variables) -> dict:
    """Run a GraphQL query through the gh CLI and return its ``data`` object.

    String variables are passed with ``-f``, integers with ``-F``. Retries five
    times with backoff; raises RuntimeError when all attempts fail.
    """
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if value is None:
            continue
        flag = "-F" if isinstance(value, int) and not isinstance(value, bool) else "-f"
        args += [flag, f"{key}={value}"]
    last = ""
    for attempt in range(5):
        proc = subprocess.run(args, capture_output=True, text=True)
        if proc.returncode == 0:
            try:
                payload = json.loads(proc.stdout)
            except ValueError:
                payload = {}
            if "data" in payload and payload["data"]:
                return payload["data"]
        last = (proc.stderr or proc.stdout or "")[:300]
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"GraphQL query failed after 5 attempts: {last}")


def rest(path: str, *extra: str) -> object:
    """Run ``gh api <path>`` and return the parsed JSON."""
    proc = subprocess.run(["gh", "api", path, *extra], capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


def is_public(repo: dict) -> bool:
    """True only for repositories GitHub reports as not private."""
    return repo.get("isPrivate") is False
