#!/usr/bin/env python3
"""Validate evidence records, Wiki citations, links, and verified paper pages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
EVIDENCE = WIKI / "evidence"

CITATION_RE = re.compile(r"\[([A-Z][A-Z0-9-]*):([a-z0-9-]+)\]")
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_evidence(errors: list[str]) -> tuple[dict[str, dict], dict[str, str]]:
    claims: dict[str, dict] = {}
    labels: dict[str, str] = {}

    for path in sorted(EVIDENCE.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(errors, f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue

        paper_id = record.get("paper_id")
        paper_label = record.get("paper_label")
        if not paper_id or not paper_label:
            fail(errors, f"{path.relative_to(ROOT)}: missing paper_id or paper_label")
            continue
        if record.get("status") != "verified":
            fail(errors, f"{path.relative_to(ROOT)}: evidence record is not verified")

        labels[paper_label] = paper_id
        for claim in record.get("claims", []):
            claim_id = claim.get("id")
            required = ("id", "summary", "section", "pdf_page", "evidence_type", "status")
            missing = [field for field in required if claim.get(field) in (None, "")]
            if missing:
                fail(errors, f"{path.relative_to(ROOT)}: claim {claim_id!r} missing {missing}")
                continue
            if claim_id in claims:
                fail(errors, f"duplicate evidence ID: {claim_id}")
            if claim.get("status") != "verified":
                fail(errors, f"{claim_id}: claim is not verified")
            if not isinstance(claim.get("pdf_page"), int) or claim["pdf_page"] < 1:
                fail(errors, f"{claim_id}: pdf_page must be a positive integer")

            if claim.get("evidence_type") == "result":
                locator = claim.get("locator")
                if not isinstance(locator, dict):
                    fail(errors, f"{claim_id}: result is missing a Table/Figure locator")
                else:
                    for field in ("kind", "label", "selection", "comparison_target"):
                        if not locator.get(field):
                            fail(errors, f"{claim_id}: locator missing {field}")
                    if locator.get("kind") not in {"table", "figure"}:
                        fail(errors, f"{claim_id}: locator kind must be table or figure")
            claims[claim_id] = claim

    return claims, labels


def check_markdown(
    errors: list[str], claims: dict[str, dict], labels: dict[str, str]
) -> set[str]:
    cited: set[str] = set()

    for path in sorted(WIKI.rglob("*.md")):
        text = path.read_text(encoding="utf-8")

        if path.name != "README.md" and "needs_verification" in text:
            fail(errors, f"{path.relative_to(ROOT)}: contains needs_verification")

        for label, claim_id in CITATION_RE.findall(text):
            if label not in labels:
                fail(errors, f"{path.relative_to(ROOT)}: unknown paper label {label}")
            elif claim_id not in claims:
                fail(errors, f"{path.relative_to(ROOT)}: unknown evidence ID {claim_id}")
            else:
                cited.add(claim_id)

        for raw_target in LINK_RE.findall(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                fail(errors, f"{path.relative_to(ROOT)}: broken link {raw_target}")

    return cited


def check_paper_pages(errors: list[str]) -> None:
    for path in sorted((WIKI / "papers").glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            fail(errors, f"{path.relative_to(ROOT)}: missing front matter")
            continue
        front_matter = text.split("---\n", 2)[1]
        if not re.search(r"^status:\s*verified\s*$", front_matter, re.MULTILINE):
            fail(errors, f"{path.relative_to(ROOT)}: paper page is not verified")


def main() -> int:
    errors: list[str] = []
    claims, labels = load_evidence(errors)
    cited = check_markdown(errors, claims, labels)
    check_paper_pages(errors)

    uncited = sorted(set(claims) - cited)
    if uncited:
        fail(errors, f"uncited evidence IDs: {', '.join(uncited)}")

    if errors:
        print("Wiki validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Wiki validation passed: {len(claims)} verified claims, "
        f"{len(cited)} cited claims, {len(labels)} paper."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

