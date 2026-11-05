# identity-evidence — staged payload (project #120)

Kill-gate-first open reimplementation (synthetic analog) of arXiv 2610.36510.
G1 verdict: PASS (see G1_STATUS.md). Headline verdict: PASS (see KILLGATE.md).
No push, no repo creation, no repo request from this builder.

## Run
- Pilot: `python3 audit.py --seed 120001 --n-weak 60 --n-strong 60 --n-passage 40 --n-positive 60 --resamples 500 --out results/pilot.json`
- Headline: `python3 audit.py --seed 120002 --n-weak 240 --n-strong 240 --n-passage 160 --n-positive 200 --resamples 2000 --out results/headline.json`
- Tests: `python3 -m pytest tests/ -q` (10 tests)
- Determinism: rerun headline to `results/headline_rerun.json` and `cmp` — byte-identical. SHA-256 of headline.json: 27176248d5bc33cb1f4c705f300679ede2948855d81bf82d5e223b3c34ada4b3.

## Contents
- `audit.py` — deterministic scripted agents, generation, telemetry, bootstrap (stdlib only; zero LLM calls; $0; CPU only).
- `tests/test_audit.py` — harness, blinding, telemetry/probe, benign cohort.
- `G1_STATUS.md` — G1 adjudication history (append-only).
- `PILOT_PREREG.md`, `PILOT_RESULT.md` — pilot preregistration and outcome.
- `PREREG.md` — LOCKED headline bars (do not edit after the headline run).
- `KILLGATE.md` — PASS verdict with the full bar table and lock order by mtime.
- `results/` — pilot.json, headline.json, headline_rerun.json, determinism.txt.
- `arxiv_html.html`, `arxiv_abs.html`, `arxiv_api.xml`, `arxiv_fulltext.txt` — G1 evidence files (paper text/listings only; NO author supplementary package was downloaded).
- Companion outputs (goal hidden_files): `papers/identity-evidence/PAPER.md`, `linkedin_drafts/identity-evidence.md` (DRAFT ONLY).
- Standing trigger: if an author package for arXiv:2610.36510 is located later, the G1 verdict must be re-examined before any repo request.
