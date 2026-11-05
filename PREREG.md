# PREREG.md — project #120 "identity-evidence" — LOCKED

LOCKED BEFORE the headline run. Zero amendments after locking; no re-seed,
re-tune, re-split, or bar-weakening after a failure. Decision rule: ANY locked
bar fails → KILL (KILLED.md + negative PAPER.md, no LinkedIn draft, no repo
request). Lock timestamps are filesystem mtimes (recorded in KILLGATE.md /
the final report after the headline run), never wall-clock estimates.
This file must NOT be edited after the headline run.

## Headline run (fixed)
- Seed: 120002 (fresh; pilot used 120001 and pilot items are NOT reused).
- n: WEAK 240, STRONG 240, PASSAGE 160 per redaction level (0/33/66/100%),
  POSITIVE CONTROL 200.
- Inference: paired bootstrap, 2000 resamples, 95% CIs on every bar.
  Bootstrap RNGs are deterministically seeded from the headline seed
  (see audit.py). No timestamps are written into results JSON, so a
  same-seed rerun must be byte-identical (headline_rerun.json).
- Agents: deterministic scripted agents only (audit.py). Zero LLM calls.
  CPU only. $0. No author data, prompts, responses, or scripts used anywhere.

## Detailed protocol (synthetic analog of arXiv 2610.36510)
The paper audits whether a benchmark score depends on entity identity or on
supplied evidence, by varying identity and evidence independently. Our analog
reproduces the DESIGN (paired named/blinded contrasts, evidence gradient,
recall probe, positive control, telemetry), not the paper's data or models:
- WEAK (name + candidate list, k=10, no decisive evidence): entities are
  KNOWN — a recall table maps exactly 80% to their answer. Named agent
  consults recall (miss → seeded guess); blinded agent sees an opaque salted
  token (SHA-256, truncated; not in the table) and guesses by seeded hash.
  Expected named ≈ 0.82, blinded ≈ 0.10 (chance).
- STRONG (decisive sequence motif, k=4): entities are NOVEL (not in the
  recall table). Both agents parse the motif from the sequence; blinding
  cannot change the parse because the evidence block is byte-identical and
  the motif is carried by the sequence, not the name. Exactly 8% of items
  carry an ambiguous motif shared by two candidates (agent picks first
  match; correct-first in a seeded half). Expected ≈ 0.96 in both conditions.
- PASSAGE-GRADIENT (known entities, k=4, passage with a decisive keyword):
  words are redacted at 0/33/66/100%. The agent uses the passage iff the
  clean decisive keyword survives; else it falls back to recall (named) or
  seeded guess (blinded). Exactly 3% of passages carry a typo'd keyword
  (parse miss → fallback). Expected gaps grow with redaction: ~0.00 → ~0.19
  → ~0.38 → ~0.57.
- POSITIVE CONTROL: a decisive line states an answer, correct on exactly
  95% of items; the agent always follows the line. Expected 0.95.
- RECALL PROBE (name only, no evidence, "unknown" allowed): known entities
  answer from recall (accuracy = coverage = 0.80); novel entities answer
  "unknown" (accuracy 0.00). Telemetry logs every decision's source and
  every recall-table lookup attempt/hit.

## Differentiation vs project #111 (blindfold)
#111 tests CERTIFICATE VALIDITY UNDER LEAKAGE: whether a certificate/claim
remains valid when leaked information is present. #120 tests EVIDENCE
DEPENDENCE: whether a score survives when identity is removed but evidence
is held byte-identical, and whether blinded scoring + retrieval telemetry +
positive controls expose evidence-independent answering. Different estimand,
different intervention, different fix. #120 makes no claim about certificate
validity, and #111 makes no claim about identity-blinded scoring.

## Locked bars (D = disease, M = mechanism, B1 = benign bound)
- D1 (large gap where evidence is absent): WEAK named−blinded gap, 95% paired
  bootstrap CI lower bound ≥ 0.40.
- D2 (small gap where evidence is decisive): STRONG |named−blinded| gap
  point ≤ 0.10 AND its 95% CI upper bound ≤ 0.10.
- D3 (gap grows as evidence is removed): PASSAGE gap(100%) − gap(0%)
  ≥ 0.20 on point estimates, AND PASSAGE gap(100%) 95% CI lower bound ≥ 0.20.
- M1 (instrument sensitivity — positive control): POSITIVE-CONTROL accuracy
  95% bootstrap CI lower bound ≥ 0.90.
- M2 (probe flags recall-driven, not evidence-driven, items): RECALL-PROBE
  contrast (WEAK accuracy − STRONG accuracy) point ≥ 0.40.
- M3 (telemetry exposes the mechanism): blinded WEAK recall-hit rate
  ≤ 0.05 AND named WEAK recall-hit rate ≥ 0.70.
- B1 (benign bound — audit must not destroy genuinely evidence-driven
  performance): STRONG blinded accuracy 95% bootstrap CI lower bound ≥ 0.85.

## Scope honesty (carried into PAPER.md)
Scripted analog only. The paper's figures (0.742 named vs 0.082 blinded on
gwas_causal_gene; LitQA2 slope +0.147, p=0.004; clinical 0.783 vs 0.531) are
context only and are NEVER claimed as reproduced. Our numbers describe our
synthetic system, not the paper's models, benchmarks, or data.
