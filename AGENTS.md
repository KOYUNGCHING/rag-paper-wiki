# RAG Paper Wiki agent contract

## Mission

Build a Karpathy-style LLM Wiki about Retrieval-Augmented Generation (RAG),
grounded in five research papers, then use only verified Wiki knowledge to make
a Traditional Chinese teaching presentation for computer-science students who
already understand basic LLM concepts but have not learned RAG.

The repository itself does not call an LLM API. A coding agent performs semantic
work by following this file; small Python programs perform deterministic checks.

## Non-negotiable workflow

1. Work on one paper at a time.
2. Before ingesting a paper, create a reading proposal in `proposals/`.
3. The proposal must explain the research problem, planned Introduction and
   Results coverage, teaching value, and likely interpretation risks.
4. Stop and obtain the user's approval. Only the user can authorize the
   `proposed -> approved` transition.
5. After approval, create the structured paper note and update related concept
   pages.
6. Validate evidence before marking the paper `verified`.
7. Report the milestone, checks, and changed files. Provide Git commands, but do
   not run `git commit` or `git push`.

The ingest lifecycle is:

`not_started -> proposed -> approved -> ingested -> verified`

Never skip a state. Content from a paper that is not `verified` must not be used
in the teaching presentation.

## Fixed core sources

The five core sources are:

- Dense Passage Retrieval (DPR)
- Retrieval-Augmented Generation (RAG)
- Fusion-in-Decoder (FiD)
- Self-RAG
- RAGChecker

Formal papers are the primary evidence. Official documentation may clarify
implementation terminology but does not count toward the required five sources.
Avoid general articles unless their use is exceptional and clearly labelled.

Original PDFs belong in `raw/pdfs/`, which is ignored by Git. Do not copy entire
papers into the repository. Record reproducible source URLs, versions, download
dates, and SHA-256 values in `raw/manifest.yaml`.

## Paper-note order

Each paper note must help a reader understand outcomes before implementation
details. Use this order:

1. Bibliographic information and one-sentence summary
2. Introduction and research motivation
3. Research gap
4. Contributions
5. Main results
6. Method
7. Experiments, datasets, metrics, and baselines
8. Ablations, when present
9. Limitations
10. Related Wiki concepts
11. Source evidence

## Evidence and claims

- General claims require a paper ID, section, and PDF page.
- Numerical claims additionally require a Table or Figure locator and the
  relevant row/column or comparison target.
- An author's interpretation must be labelled as an author claim, not a proven
  fact.
- Cross-paper conclusions must be labelled `wiki_synthesis`.
- Unresolved items must be labelled `needs_verification` and cannot flow into
  slides.
- Every slide must list the Wiki pages it uses. Slide numbers must remain
  traceable through Wiki evidence to the original paper.
- Do not invent page numbers, table numbers, experimental values, findings, or
  failure records.

## Wiki rules

`wiki/papers/` contains structured notes for individual papers.
`wiki/concepts/` contains cumulative explanations synthesized across papers.
`wiki/comparisons/` contains explicit cross-paper comparisons.

The Wiki is more than five summaries: concepts must be linked, terminology must
be consistent, and differences between papers must be explicit. Use Traditional
Chinese prose, retain English technical terms on first use, and keep filenames
and schema fields in English.

## Presentation rules

The presentation title is **RAG 是什麼？讓 LLM 先查資料再回答**.

- Target 12–14 slides and 10–12 minutes.
- Teach the overall RAG concept; Self-RAG is an advanced development near the end.
- Include one complete interactive RAG example, one retrieval-failure example,
  expandable sources, and three quiz questions.
- Use native HTML, CSS, and JavaScript under `docs/` for GitHub Pages.
- Support keyboard, buttons, touch, responsive layouts, and
  `prefers-reduced-motion`.
- Core reading must remain available when JavaScript is disabled.
- Use an academic-note visual style: light paper-like surface, dark blue text,
  and teal accents.
- Draw original HTML/CSS/SVG diagrams. Do not copy paper figures. Redrawn result
  charts must identify the source paper and table.

## Validation and logs

Agents handle semantic reading, synthesis, teaching structure, and revision.
Python handles deterministic validation such as:

- manifest and schema completeness
- legal state transitions
- Markdown links
- citation IDs and evidence fields
- unverified claims
- slide-to-Wiki mappings

Every meaningful run belongs in `logs/runs/` and records inputs, checks before
the fix, findings, actions, checks after the fix, files changed, and final status.
Preserve genuine failures. After all five ingests, write the reflection from the
recorded findings rather than deciding the answer in advance. If no real failure
occurs, use an explicitly labelled test fixture; never present it as a real run.

## Git boundaries

- The user owns commits, pushes, GitHub Pages settings, and publication.
- Do not run `git commit`, `git push`, rewrite history, or publish Pages.
- Finish one reviewable milestone at a time.
- At handoff, summarize the result, checks, changed files, and exact suggested
  `git status`, `git diff`, `git add`, `git commit`, and `git push` commands.
- Never commit PDFs, API keys, tokens, credentials, or personal secrets.

## Definition of done

The work is complete only when all five papers are verified; paper notes and
cross-paper concepts are linked; no slide uses unverified evidence; deterministic
validators pass; the 12–14 slide experience works on desktop and mobile; the
workflow graph matches actual operations; real run evidence and reflection are
present; and the README links the Wiki, graph, logs, slides, and deployment.

