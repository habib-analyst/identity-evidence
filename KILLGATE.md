# KILLGATE.md — project #120 "identity-evidence" — VERDICT: PASS

Kill-gate-first build. G1 (see G1_STATUS.md) PASSED before any design or code:
the paper's §2 "supplementary" sentence names no retrievable artifact, no
ancillary file is attached to arXiv:2610.36510v1 (abs page: no ancillary
section; API record: only abs + PDF links; HEAD on /anc/2610.36510v1 → 404),
the full-text sweep is clean, and no author repo/package was found.
#100 re-examination trigger stands: if an author package is located later,
the G1 verdict must be re-examined before any repo request.

## Headline run
Seed 120002 (fresh; pilot seed 120001 not reused). n: WEAK 240, STRONG 240,
PASSAGE 160 per redaction level, POSITIVE CONTROL 200. Paired bootstrap,
2000 resamples, 95% CIs on every bar. Determinism digest (SHA-256 of
results/headline.json): 27176248d5bc33cb1f4c705f300679ede2948855d81bf82d5e223b3c34ada4b3.
Same-seed rerun results/headline_rerun.json is byte-identical (cmp PASS).
Tests: pytest 10 passed.

## Lock order (filesystem mtime, UTC as recorded by stat; PKT = UTC + 5h)
- G1_STATUS.md: epoch 1793554448 (2026-11-01 17:34:08 UTC)
- PILOT_PREREG.md: epoch 1793554462 (2026-11-01 17:34:22 UTC)
- PREREG.md: epoch 1793554619 (2026-11-01 17:36:59 UTC)
- results/headline.json: epoch 1793554638 (2026-11-01 17:37:18 UTC)
Order is correct: G1 → pilot prereg → prereg lock → headline. PREREG.md was
not edited after the headline run.

## Locked-bar adjudication (ALL PASS — no bar moved, no re-seed, no re-tune)
| bar | locked threshold | measured (95% CI) | verdict |
|---|---|---|---|
| D1 WEAK gap | CI lower ≥ 0.40 | 0.7333 [0.6750, 0.7917], n=240 | PASS |
| D2 STRONG gap | point ≤ 0.10 and CI upper ≤ 0.10 | 0.0000 [0.0000, 0.0000], n=240 | PASS |
| D3 passage gradient | gap100−gap0 ≥ 0.20 and gap100 CI lower ≥ 0.20 | 0.5562−0.0125 = 0.5437; gap100 CI [0.4625, 0.6438] | PASS |
| M1 positive control | CI lower ≥ 0.90 | 0.9500 [0.9200, 0.9750], n=200 | PASS |
| M2 recall-probe contrast | point ≥ 0.40 | 0.8000 − 0.0000 = 0.8000 | PASS |
| M3 telemetry | blinded hit rate ≤ 0.05 and named ≥ 0.70 | blinded 0/240 = 0.0000; named 192/240 = 0.8000 | PASS |
| B1 benign bound | STRONG blinded CI lower ≥ 0.85 | 0.9708 [0.9458, 0.9917], n=240 | PASS |

Supporting headline numbers: WEAK named 0.8167 [0.7667, 0.8625], blinded
0.0833 [0.0500, 0.1167] (chance 0.10, k=10). STRONG named 0.9708 [0.9500,
0.9917], blinded 0.9708 [0.9458, 0.9917]. PASSAGE named/blinded/gap by
level — 0%: 0.9938/0.9812/0.0125; 33%: 0.9625/0.7750/0.1875; 66%:
0.8938/0.4875/0.4063; 100%: 0.8500/0.2938/0.5562. RECALL PROBE: WEAK
0.8000 (192/240 answered), STRONG 0.0000 (0/240 answered).

## Verdict
PASS. Payload staged in ~/workspace/build/identity-evidence/ (code, this
file, PREREG.md, results/). PAPER.md written to the goal hidden_files
papers directory; LinkedIn draft written and marked DRAFT ONLY. No push, no
repo creation, no repo request from this builder — repo request (if any) is
for the orchestrator to verify first, subject to the #100 re-examination
trigger above.
