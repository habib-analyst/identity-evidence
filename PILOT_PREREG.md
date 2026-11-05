# PILOT_PREREG.md — project #120 "identity-evidence"

Written BEFORE any pilot number is generated. Pilot seed: 120001.
Pilot purpose: verify the build is not vacuous and the harness runs end to end.
Pilot numbers NEVER set headline bars by themselves and NEVER gate the headline
except through the pass/fail gates below; headline bars are locked separately
in PREREG.md before the headline run.

## Design under test (same as headline design, smaller n)
- Scripted deterministic agents only. Zero LLM calls. CPU only. $0.
- Families:
  - WEAK: name + candidate list (k=10), no decisive evidence. Entities are
    KNOWN: a recall table maps 80% of weak entities to their answer
    (RECALL_COVERAGE=0.80); the rest are unmapped. Named agent uses the
    recall table; blinded agent sees an opaque token (not in the table) and
    guesses deterministically (seeded hash pick over candidates).
  - STRONG: decisive sequence motif determines the answer. Entities are
    NOVEL (not in the recall table). Both named and blinded agents parse the
    motif; 8% of items carry an ambiguous motif shared by 2 candidates, on
    which the agent picks the first match (expected ~50% on those).
  - PASSAGE-GRADIENT: known entities with a passage containing a decisive
    keyword. Redaction removes passage words at 0/33/66/100%. The agent uses
    the passage if the decisive keyword survives, else falls back to recall
    (named) or seeded guess (blinded, k=4).
  - POSITIVE CONTROL: a decisive line states an answer; the line is correct
    on 95% of items (seeded); the agent always follows the line.
  - RECALL PROBE: name only, no evidence, "unknown" allowed. For known
    entities the probe answers from the recall table; for novel entities it
    answers "unknown" (counted as not-correct for accuracy, and reported
    separately). Telemetry logs every decision's source
    (recall / evidence / line / guess) and every recall-table lookup attempt
    and hit.
- Pilot n: WEAK 60, STRONG 60, PASSAGE 40 per redaction level, POSITIVE 60,
  RECALL PROBE on the WEAK + STRONG items (name-only).

## Pilot gates (ALL must pass, else redesign before PREREG lock)
- P1 (runs): the pilot completes without error and every condition yields a
  finite accuracy in [0, 1].
- P2 (non-vacuity, directional only): WEAK named-minus-blinded gap > 0.20
  AND STRONG |named-minus-blinded| gap < 0.20 AND POSITIVE-CONTROL accuracy
  > 0.80. (Headline bars are stricter and locked separately; pilot gates
  only check the effect is in the expected direction and the instrument works.)
- P3 (determinism): re-running the pilot with the same seed produces a
  byte-identical results JSON (SHA-256 match).
- P4 (telemetry integrity): every decision has a telemetry row; blinded
  recall-hit count is recorded (expected 0 hits, attempts > 0); recall-probe
  rows exist for both known and novel entities.
- P5 (tests): the pytest suite passes at pilot time (harness, blinding,
  telemetry/probe, benign cohort).

If any pilot gate fails: STOP, diagnose, fix the harness/design, and re-run
the pilot under this same preregistration. Do NOT proceed to PREREG lock on a
failed pilot, and do NOT carry pilot numbers into headline bars as fitted values
— headline bars are set from the design's theoretical expectations with margin,
not from pilot point estimates.
