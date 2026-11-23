#!/usr/bin/env python3
"""Project-level deterministic checks.

Checks manifest schema, legal lifecycle states, proposal/run-log consistency,
PDF hashes, concept-page source declarations, and slide-to-Wiki mappings.
No model API is used.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
STATES = ["not_started", "proposed", "approved", "ingested", "verified"]
MANIFEST_FIELDS = (
    "id", "short_name", "title", "arxiv_id", "landing_page", "pdf_url",
    "version", "local_pdf", "downloaded_at", "sha256", "ingest_status",
)
CITATION_RE = re.compile(r"\[([A-Z][A-Z0-9-]*):([a-z0-9-]+)\]")
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    return yaml.safe_load(text.split("---\n", 2)[1]) or {}


def load_labels() -> dict[str, str]:
    """Map paper_label -> paper_id from evidence JSON."""
    labels = {}
    for path in (ROOT / "wiki" / "evidence").glob("*.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        labels[record["paper_label"]] = record["paper_id"]
    return labels


def check_manifest(errors: list[str]) -> dict[str, dict]:
    manifest = yaml.safe_load((ROOT / "raw" / "manifest.yaml").read_text(encoding="utf-8"))
    papers = {}
    for entry in manifest.get("papers", []):
        pid = entry.get("id")
        for field in MANIFEST_FIELDS:
            if field not in entry:
                errors.append(f"manifest {pid}: missing field {field}")
        state = entry.get("ingest_status")
        if state not in STATES:
            errors.append(f"manifest {pid}: illegal ingest_status {state!r}")
            continue
        if STATES.index(state) >= STATES.index("proposed"):
            for field in ("version", "downloaded_at", "sha256"):
                if not entry.get(field):
                    errors.append(f"manifest {pid}: {state} paper needs {field}")
            if entry.get("version") and not str(entry.get("pdf_url", "")).endswith(str(entry["version"])):
                errors.append(f"manifest {pid}: pdf_url is not pinned to {entry['version']}")
            pdf = ROOT / str(entry.get("local_pdf"))
            if pdf.exists():
                digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
                if digest != entry.get("sha256"):
                    errors.append(f"manifest {pid}: local PDF hash mismatch")
            # Missing local PDFs are allowed: raw/pdfs/ is Git-ignored, so a fresh
            # clone cannot contain them.
        papers[pid] = entry
    if len(papers) != 5:
        errors.append(f"manifest: expected 5 core papers, found {len(papers)}")
    return papers


def check_lifecycle(errors: list[str], papers: dict[str, dict]) -> None:
    runs = []
    for path in sorted((ROOT / "logs" / "runs").glob("[0-9][0-9][0-9]-*.md")):
        fm = front_matter(path)
        if not fm:
            errors.append(f"{path.relative_to(ROOT)}: missing front matter")
            continue
        for field in ("run_id", "operation", "started_at", "status"):
            if field not in fm:
                errors.append(f"{path.relative_to(ROOT)}: missing {field}")
        prefix = path.name[:3]
        # Read run_id as raw text: YAML 1.1 parses "010" as octal 8.
        raw_id = re.search(r"^run_id:\s*(\S+)\s*$", path.read_text(encoding="utf-8"), re.MULTILINE)
        if not raw_id or raw_id.group(1).strip("'\"") != prefix:
            errors.append(f"{path.relative_to(ROOT)}: run_id does not match filename")
        runs.append((prefix, path, fm))

    ids = [int(p) for p, _, _ in runs]
    if ids != list(range(1, len(ids) + 1)):
        errors.append(f"logs/runs: run ids are not contiguous from 001: {ids}")

    for pid, entry in papers.items():
        state = entry["ingest_status"]
        proposal_path = ROOT / "proposals" / f"{pid}.md"
        paper_path = ROOT / "wiki" / "papers" / f"{pid}.md"
        evidence_path = ROOT / "wiki" / "evidence" / f"{pid}.json"
        rank = STATES.index(state)

        if rank >= STATES.index("proposed") and not proposal_path.exists():
            errors.append(f"{pid}: state {state} but proposal file is missing")
        if proposal_path.exists():
            pfm = front_matter(proposal_path)
            if pfm.get("source_sha256") != entry.get("sha256"):
                errors.append(f"{pid}: proposal source_sha256 differs from manifest")
            if rank >= STATES.index("approved"):
                if pfm.get("status") != "approved" or not pfm.get("approved_at"):
                    errors.append(f"{pid}: state {state} requires an approved proposal with approved_at")
            elif pfm.get("status") == "approved":
                errors.append(f"{pid}: proposal approved but manifest is still {state}")

        has_note = paper_path.exists() or evidence_path.exists()
        if has_note and rank < STATES.index("ingested"):
            errors.append(f"{pid}: Wiki note/evidence exists before ingest ({state})")
        if state == "verified" and not (paper_path.exists() and evidence_path.exists()):
            errors.append(f"{pid}: verified but paper note or evidence is missing")

        # Every verified paper needs a proposal run that precedes an ingest run.
        sources = [(p, fm) for p, _, fm in runs if fm.get("source") == pid]
        proposal_runs = [p for p, fm in sources if "proposal" in str(fm.get("operation"))]
        ingest_runs = [p for p, fm in sources if "ingest" in str(fm.get("operation"))]
        if rank >= STATES.index("proposed") and not proposal_runs:
            errors.append(f"{pid}: no proposal run log")
        if state == "verified":
            if not ingest_runs:
                errors.append(f"{pid}: verified without an ingest run log")
            elif proposal_runs and min(ingest_runs) < min(proposal_runs):
                errors.append(f"{pid}: ingest run precedes proposal run")


def check_concept_sources(errors: list[str], labels: dict[str, str]) -> None:
    """verified_sources in front matter must equal the papers actually cited."""
    for folder in ("concepts", "comparisons"):
        for path in sorted((ROOT / "wiki" / folder).glob("*.md")):
            if path.name == "README.md":
                continue
            fm = front_matter(path)
            rel = path.relative_to(ROOT)
            if fm.get("status") != "verified":
                errors.append(f"{rel}: status is not verified")
            declared = set(fm.get("verified_sources") or [])
            text = path.read_text(encoding="utf-8")
            cited = {labels[l] for l, _ in CITATION_RE.findall(text) if l in labels}
            if cited - declared:
                errors.append(f"{rel}: cites {sorted(cited - declared)} not listed in verified_sources")
            if declared - cited:
                errors.append(f"{rel}: verified_sources lists {sorted(declared - cited)} but never cites them")


def check_slide_mapping(errors: list[str], labels: dict[str, str]) -> int:
    """slides-src/outline.md: every '## Slide N' section must link verified Wiki pages."""
    outline = ROOT / "slides-src" / "outline.md"
    if not outline.exists():
        return 0
    text = outline.read_text(encoding="utf-8")
    sections = re.split(r"^## Slide (\d+)", text, flags=re.MULTILINE)[1:]
    numbers = []
    for num, body in zip(sections[0::2], sections[1::2]):
        numbers.append(int(num))
        wiki_links = [t for t in LINK_RE.findall(body) if "wiki/" in t]
        if not wiki_links:
            errors.append(f"slide {num}: no Wiki source mapping")
        for target in wiki_links:
            page = (outline.parent / target.split("#")[0]).resolve()
            if not page.exists():
                errors.append(f"slide {num}: broken Wiki link {target}")
            elif page.suffix == ".md" and front_matter(page).get("status") != "verified":
                errors.append(f"slide {num}: Wiki page {target} is not verified")
        for label, _ in CITATION_RE.findall(body):
            if label not in labels:
                errors.append(f"slide {num}: unknown paper label {label}")
    if numbers != list(range(1, len(numbers) + 1)):
        errors.append(f"slides: numbering is not contiguous: {numbers}")
    if not 12 <= len(numbers) <= 14:
        errors.append(f"slides: expected 12-14 slides, found {len(numbers)}")
    return len(numbers)


def main() -> int:
    errors: list[str] = []
    labels = load_labels()
    papers = check_manifest(errors)
    check_lifecycle(errors, papers)
    check_concept_sources(errors, labels)
    slides = check_slide_mapping(errors, labels)
    if errors:
        print("Project validation failed:")
        for e in errors:
            print(f"- {e}")
        return 1
    print(f"Project validation passed: {len(papers)} papers in manifest, "
          f"lifecycle consistent, {slides} mapped slides.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
