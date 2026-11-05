# PILOT_RESULT.md — project #120 "identity-evidence"

Pilot seed 120001 (n: WEAK 60, STRONG 60, PASSAGE 40/level, POSITIVE 60;
bootstrap 500 for pilot only). All pilot gates PASS:

- P1 (runs): completed, all accuracies finite. YES.
- P2 (non-vacuity): WEAK gap 0.783 > 0.20; STRONG |gap| 0.000 < 0.20;
  POSITIVE-CONTROL accuracy 0.950 > 0.80. YES.
- P3 (determinism): same-seed rerun byte-identical (SHA-256 match). YES.
- P4 (telemetry): every decision logged; blinded recall hits 0/60 attempts;
  recall probe answered 48/60 known vs 0/60 novel. YES.
- P5 (tests): pytest 10 passed. YES.

Pilot numbers (directional only; NOT headline bars):
- WEAK named 0.817, blinded 0.033, gap 0.783.
- STRONG named 0.950, blinded 0.950, gap 0.000.
- PASSAGE gaps: 0% → 0.000; 33% → 0.150; 66% → 0.275; 100% → 0.525.
- POSITIVE CONTROL 0.950. RECALL PROBE weak 0.800 vs strong 0.000 (contrast 0.800).

Pre-lock fix (made BEFORE PREREG.md was written, so no locked bar is affected):
the first pilot version's passage-corruption flag was a no-op — the agent
checked for the item's own (already-typo'd) keyword, so a "corrupted" passage
still parsed. Fixed so the stored keyword is the CLEAN token the agent looks
for while the passage carries the typo'd token; verified at item level
(P0023: named falls back to recall, blinded to guess, on the corrupted item).
The pilot gap at 0% redaction stayed 0.000 only because that single corrupt
item's seeded blinded guess happened to land on the correct candidate — a
1-item coincidence at n=40, not a mechanism failure. Headline n=160/level
gives 5 corrupt items, so the 0% gap is expected near ~0.02, far below the
D3 margin.
