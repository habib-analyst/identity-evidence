"""Tests for identity-evidence: harness, blinding, telemetry/probe, benign cohort."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from audit import (generate_items, opaque_token, render_prompt, run_agent_weak,
                   run_agent_strong, run_agent_passage, run_agent_positive,
                   run_recall_probe, run_all, seeded_guess)


def test_blinding_changes_only_entity_field_and_evidence_byte_identical():
    items = generate_items(7, 10, 10, 10, 10)
    for it in items["weak"]:
        named = run_agent_weak(it, False, 7)
        blind = run_agent_weak(it, True, 7)
        # Entity line differs; every other line identical.
        n_lines = named["prompt"].split("\n")
        b_lines = blind["prompt"].split("\n")
        assert len(n_lines) == len(b_lines)
        assert n_lines[0] != b_lines[0]
        assert n_lines[1:] == b_lines[1:]
        # Blinded display carries no part of the entity name.
        assert it["entity"] not in blind["prompt"]
        assert blind["prompt"].split("\n")[0].startswith("Entity: TOK-")


def test_blinding_token_is_opaque_and_stable():
    assert opaque_token("ENT-W-0001") == opaque_token("ENT-W-0001")
    assert opaque_token("ENT-W-0001") != opaque_token("ENT-W-0002")
    assert "ENT-W-0001" not in opaque_token("ENT-W-0001")


def test_strong_evidence_parse_is_identity_invariant():
    items = generate_items(7, 5, 40, 5, 5)
    for it in items["strong"]:
        assert run_agent_strong(it, False, 7)["pick"] == \
            run_agent_strong(it, True, 7)["pick"]


def test_telemetry_rows_complete_and_blinded_recall_never_hits():
    items = generate_items(7, 50, 10, 10, 10)
    rows = [run_agent_weak(it, True, 7) for it in items["weak"]]
    assert all("source" in r and "recall_attempt" in r and "recall_hit" in r
               for r in rows)
    assert sum(r["recall_attempt"] for r in rows) == len(rows)
    assert sum(r["recall_hit"] for r in rows) == 0


def test_recall_probe_flags_known_not_novel():
    items = generate_items(7, 50, 50, 5, 5)
    pw = [run_recall_probe(it, True) for it in items["weak"]]
    ps = [run_recall_probe(it, False) for it in items["strong"]]
    # Known: answered exactly for mapped items; novel: never answered.
    assert sum(r["answered"] for r in pw) == sum(it["mapped"] for it in items["weak"])
    assert sum(r["answered"] for r in ps) == 0
    assert sum(r["correct"] for r in pw) > sum(r["correct"] for r in ps)


def test_positive_control_follows_line():
    items = generate_items(7, 5, 5, 5, 40)
    for it in items["positive"]:
        assert run_agent_positive(it)["pick"] == it["line_answer"]


def test_seeded_guess_deterministic_and_in_range():
    for k in (4, 10):
        assert seeded_guess("W0001", 120002, k, "x") == \
            seeded_guess("W0001", 120002, k, "x")
        assert 0 <= seeded_guess("W0001", 120002, k, "x") < k


def test_benign_cohort_blinded_strong_accuracy_preserved():
    # Benign cohort = genuinely evidence-driven (STRONG) items: blinding must
    # not destroy accuracy. Deterministic small run; bar mirrors PREREG B1.
    res = run_all(120001, 20, 60, 20, 20, 200)
    assert res["strong"]["blinded"]["point"] >= 0.85
    assert abs(res["strong"]["gap"]["point"]) <= 0.10


def test_run_all_deterministic_same_seed():
    a = run_all(120001, 20, 20, 20, 20, 200)
    b = run_all(120001, 20, 20, 20, 20, 200)
    assert a == b


def test_passage_redaction_monotone_gap_direction():
    # Gap at full redaction must exceed gap at zero redaction (directional).
    res = run_all(120001, 20, 20, 40, 20, 200)
    assert res["passage"]["1.0"]["gap"]["point"] > \
        res["passage"]["0.0"]["gap"]["point"]
