#!/usr/bin/env python3
"""test_fixture: deliberately broken copies of the repo, used only to prove the
validators catch each failure class. These are NOT real ingest failures.

Each case copies the repository (without raw/pdfs) into a temp dir, applies one
mutation, runs a validator, and expects a non-zero exit plus a message.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORE = shutil.ignore_patterns(".git", "pdfs", "tmp", "__pycache__")


def sub(path: str, old: str, new: str):
    def apply(root: Path) -> None:
        f = root / path
        text = f.read_text(encoding="utf-8")
        assert old in text, f"fixture setup: {old!r} not in {path}"
        f.write_text(text.replace(old, new, 1), encoding="utf-8")
    return apply


def write(path: str, content: str):
    def apply(root: Path) -> None:
        (root / path).write_text(content, encoding="utf-8")
    return apply


SLIDES_NO_MAP = "\n".join(
    f"## Slide {i}\n\n內容。[RAG 概念](../wiki/concepts/rag.md)\n" for i in range(1, 12)
) + "\n## Slide 12\n\n沒有任何 Wiki 來源的投影片。\n"

CASES = [
    ("unknown citation ID", "validate_wiki.py",
     sub("wiki/concepts/rag.md", "[RAG:rag-c03]", "[RAG:rag-c99]"), "unknown evidence ID"),
    ("result without locator", "validate_wiki.py",
     sub("wiki/evidence/fid.json", '"kind": "table"', '"kind": "paragraph"'), "locator kind"),
    ("unverified marker in Wiki", "validate_wiki.py",
     sub("wiki/concepts/chunk.md", "# ", "needs_verification\n\n# "), "needs_verification"),
    ("illegal lifecycle state", "validate_project.py",
     sub("raw/manifest.yaml", "ingest_status: verified", "ingest_status: done"), "illegal ingest_status"),
    ("verified without approval", "validate_project.py",
     sub("proposals/ragchecker.md", "approved_at: 2026-11-23", "approved_at: null"), "requires an approved proposal"),
    ("undeclared concept source", "validate_project.py",
     sub("wiki/concepts/rag.md", "  - self-rag\n", ""), "not listed in verified_sources"),
    ("slide without Wiki mapping", "validate_project.py",
     write("slides-src/outline.md", SLIDES_NO_MAP), "no Wiki source mapping"),
]


def main() -> int:
    failures = 0
    for name, script, mutate, expected in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, ignore=IGNORE)
            mutate(copy)
            result = subprocess.run(
                [sys.executable, str(copy / "scripts" / script)],
                capture_output=True, text=True,
            )
            ok = result.returncode != 0 and expected in result.stdout
            failures += not ok
            print(f"[{'PASS' if ok else 'FAIL'}] test_fixture: {name}")
            if not ok:
                print(result.stdout)
    print(f"{len(CASES) - failures}/{len(CASES)} fixture cases caught.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
