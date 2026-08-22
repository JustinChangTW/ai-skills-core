---
name: textbook-figure-remap
description: >
  Extract individual figures from PDF textbooks on demand with deterministic
  matching and built-in quality checks. Use when writing or supplementing a
  note that needs an embedded anatomy, classification, algorithm, or imaging
  figure; when the user asks to extract a figure; or when a note's TODO or REF
  points to a figure not yet embedded.
---

# Figure Remap

Resolve `SKILL_ROOT` to the absolute directory containing this `SKILL.md`.
The extraction pipeline is bundled in `$SKILL_ROOT/scripts/project`.

Treat source PDFs as read-only. Write only to the output path chosen by the
user. Read `references/figure-remap-reference.md` when implementation details,
backend behavior, failure schemas, or legacy batch operations are needed.

## Setup

Before first use, verify that the core packages in
`references/requirements.txt` are available. Optional local-vision checks use
Ollama at `T2N_OLLAMA_HOST`; do not require Ollama for strict deterministic
extraction.

## Standard workflow

1. Find the requested figure ID, caption, PDF path, and 1-indexed page number.
2. Read the real caption before extraction; do not infer a figure's meaning
   from its ID alone.
3. Run the public `figure_remap.py extract` entrypoint. Never call
   `figure_qc_gate.py` directly.
4. Parse the returned JSON contract and branch on `status` and
   `match_quality`.
5. Embed the output only when `status` is `pass`.

```bash
python "$SKILL_ROOT/scripts/project/figures/figure_remap.py" extract \
  --book "BookID" \
  --fig-id "5-1" \
  --caption "Caption text from the textbook" \
  --out "path/to/attachments/Fig_5-1_Book.png" \
  --pdf "path/to/source.pdf" \
  --page 42
```

The command returns only this stable contract:

```json
{
  "status": "pass|fail|escalate",
  "match_quality": "exact|uncertain|failed",
  "hard_fail": true,
  "file": "path or null",
  "fig_id": "normalized id",
  "reason": "explanation"
}
```

## Decision rules

- `status: pass`, `match_quality: exact`: use the returned file after checking
  its caption and visual content.
- `status: fail`: treat it as a correct refusal. Recheck the page and figure
  ID; otherwise leave a TODO or ask before escalating.
- `status: escalate`: inspect the page render and retry only with explicit
  visual guidance.
- Keep strict mode as the default. Do not add `--no-strict` unless the user
  accepts a plausible-but-wrong crop risk.
- The strict entrypoint automatically checks neighboring pages when the stated
  page misses.
- Multi-panel captions may route to relaxed handling because one-caption to
  one-raster matching does not apply.

## Source modes

- `--source auto` (default): check a conventional existing crop, then fall
  back to strict PDF extraction.
- `--source pdf`: ignore existing crops and re-extract from the PDF.
- `--source existing`: validate an existing crop only; do not fall back.

## Multiple figures on one scanned page

Use the cache-aware wrapper when several requested figures share a page:

```bash
python "$SKILL_ROOT/scripts/project/figures/figure_remap.py" extract-page \
  --book "BookID" \
  --pdf "path/to/source.pdf" \
  --page 42 \
  --out-dir "path/to/attachments" \
  --fig-ids "4-1A,4-1B,4-1C" \
  --name-template "Fig_{fig_id}_Book.png"
```

This wrapper still emits one full contract per figure. Do not treat it as a
whole-book batch extraction command.

## Note embed

After a verified pass, use the note tool's native image syntax. For Obsidian:

```markdown
![[Fig_5-1_Book.png|400]]
*Fig. 5.1 — verified caption (Author, year, p. 42)*
```

Never claim that a successful crop proves the user's interpretation of the
figure. A pass verifies figure identity and crop quality, not semantic intent.
