"""identity-evidence: synthetic analog of arXiv 2610.36510's identity-vs-evidence audit.

Deterministic scripted agents only. Zero LLM calls. CPU only. $0.
Standard library only.

Design (see PILOT_PREREG.md / PREREG.md):
- WEAK: name + candidate list (k=10), no decisive evidence. Entities are KNOWN:
  a recall table maps exactly RECALL_COVERAGE of them to their answer.
  Named agent consults recall; blinded agent sees an opaque salted token that
  is not in the table and guesses by a seeded hash.
- STRONG: decisive sequence motif determines the answer. Entities are NOVEL
  (not in the recall table). Both agents parse the motif. A fixed 8% of items
  carry an ambiguous motif shared by two candidates.
- PASSAGE-GRADIENT: KNOWN entities with a passage holding a decisive keyword.
  Redaction removes words at 0/33/66/100%. Agent uses the passage if the
  decisive keyword survives, else falls back to recall (named) or guess (blinded).
  A fixed 3% of items have a corrupted decisive keyword.
- POSITIVE CONTROL: a decisive line states an answer; correct on exactly 95%
  of items; the agent always follows the line.
- RECALL PROBE: name only, no evidence. Known entities answer from recall;
  novel entities answer "unknown" (counted not-correct; n_answered reported).

Blinding guarantee: the blinded prompt is the named prompt with ONLY the
entity-name field replaced by an opaque token (sha256 salted, truncated);
the evidence block is byte-identical. render_prompt() enforces this and the
test suite checks it.
"""

import hashlib
import json
import random

RECALL_COVERAGE = 0.80
STRONG_AMBIGUOUS_FRAC = 0.08
PASSAGE_CORRUPT_FRAC = 0.03
POSITIVE_LINE_CORRECT_FRAC = 0.95
WEAK_K = 10
STRONG_K = 4
PASSAGE_K = 4
REDACTION_LEVELS = (0.0, 0.33, 0.66, 1.0)


def opaque_token(entity: str, salt: str = "identity-evidence-v1") -> str:
    """Opaque per-entity token. Not reversible to the name by table lookup."""
    return "TOK-" + hashlib.sha256(f"{salt}:{entity}".encode()).hexdigest()[:12]


def seeded_guess(item_id: str, seed: int, k: int, key: str) -> int:
    """Deterministic uniform pick over k candidates (hash, not hash())."""
    h = hashlib.sha256(f"{seed}:{key}:{item_id}".encode()).hexdigest()
    return int(h, 16) % k


def render_prompt(entity_display: str, evidence: str, candidates) -> str:
    """Prompt rendering. Named and blinded differ ONLY in entity_display."""
    cand = "\n".join(f"{i}. {c}" for i, c in enumerate(candidates))
    return f"Entity: {entity_display}\nEvidence:\n{evidence}\nCandidates:\n{cand}\nAnswer with a candidate index."


def _exact_fraction_flags(rng: random.Random, n: int, frac: float) -> list:
    """Boolean flags with exactly round(n*frac) True, positions shuffled."""
    k = int(round(n * frac))
    flags = [True] * k + [False] * (n - k)
    rng.shuffle(flags)
    return flags


def generate_items(seed: int, n_weak: int, n_strong: int, n_passage: int,
                   n_positive: int) -> dict:
    """Generate all synthetic items. Fully determined by `seed`."""
    rng = random.Random(seed)
    pool = [f"CAND-{i:04d}" for i in range(4000)]
    items = {"weak": [], "strong": [], "passage": [], "positive": []}

    # WEAK: known entities, recall coverage exact.
    mapped = _exact_fraction_flags(rng, n_weak, RECALL_COVERAGE)
    for i in range(n_weak):
        entity = f"ENT-W-{i:04d}"
        correct = rng.choice(pool)
        distractors = rng.sample([c for c in pool if c != correct], WEAK_K - 1)
        candidates = distractors + [correct]
        rng.shuffle(candidates)
        ans = candidates.index(correct)
        items["weak"].append({
            "id": f"W{i:04d}", "entity": entity, "candidates": candidates,
            "answer": ans, "mapped": mapped[i],
            "evidence": "(no decisive evidence; name and candidate list only)",
        })

    # STRONG: novel entities, decisive motif, 8% ambiguous.
    ambiguous = _exact_fraction_flags(rng, n_strong, STRONG_AMBIGUOUS_FRAC)
    for i in range(n_strong):
        entity = f"ENT-S-{i:04d}"
        correct = rng.choice(pool)
        distractors = rng.sample([c for c in pool if c != correct], STRONG_K - 1)
        candidates = distractors + [correct]
        rng.shuffle(candidates)
        ans = candidates.index(correct)
        motif = f"MOTIF-{i:04d}"
        if ambiguous[i]:
            # A second candidate shares the motif; agent picks first match.
            # Seeded coin: correct candidate first in half the ambiguous cases.
            sharer_first = rng.random() < 0.5
            if sharer_first:
                order = [ans] + [j for j in range(STRONG_K) if j != ans][:1]
            else:
                order = [j for j in range(STRONG_K) if j != ans][:1] + [ans]
            motif_holders = order
        else:
            motif_holders = [ans]
        seq = "ACGT" * 10 + motif + "TGCA" * 10
        items["strong"].append({
            "id": f"S{i:04d}", "entity": entity, "candidates": candidates,
            "answer": ans, "motif": motif, "motif_holders": motif_holders,
            "sequence": seq,
            "evidence": f"Sequence: {seq}",
        })

    # PASSAGE: known entities, 80% recall-mapped, 3% corrupted keyword.
    mapped_p = _exact_fraction_flags(rng, n_passage, RECALL_COVERAGE)
    corrupt = _exact_fraction_flags(rng, n_passage, PASSAGE_CORRUPT_FRAC)
    for i in range(n_passage):
        entity = f"ENT-P-{i:04d}"
        correct = rng.choice(pool)
        distractors = rng.sample([c for c in pool if c != correct], PASSAGE_K - 1)
        candidates = distractors + [correct]
        rng.shuffle(candidates)
        ans = candidates.index(correct)
        keyword = f"DECISIVE-{i:04d}"
        # Corruption garbles the passage token so the agent's exact-match
        # parse for the CLEAN keyword misses it (fallback path). The stored
        # "keyword" is the clean token the agent looks for; the passage word
        # is the typo'd token on corrupt items.
        display_keyword = keyword + "-TYPO" if corrupt[i] else keyword
        filler = [f"word-{j}" for j in range(20)]
        passage_words = filler[:10] + [display_keyword] + filler[10:]
        items["passage"].append({
            "id": f"P{i:04d}", "entity": entity, "candidates": candidates,
            "answer": ans, "mapped": mapped_p[i], "keyword": keyword,
            "passage_words": passage_words,
        })

    # POSITIVE CONTROL: line correct on exactly 95%.
    line_ok = _exact_fraction_flags(rng, n_positive, POSITIVE_LINE_CORRECT_FRAC)
    for i in range(n_positive):
        correct = rng.choice(pool)
        distractors = rng.sample([c for c in pool if c != correct], 3)
        candidates = distractors + [correct]
        rng.shuffle(candidates)
        ans = candidates.index(correct)
        stated = ans if line_ok[i] else (ans + 1) % 4
        items["positive"].append({
            "id": f"C{i:04d}", "candidates": candidates, "answer": ans,
            "line_answer": stated,
            "evidence": f"Decisive line: the answer is candidate {stated}.",
        })
    return items


def redact_words(words: list, level: float, item_id: str, seed: int) -> list:
    """Word-level redaction; each word kept with prob 1-level (seeded)."""
    rng = random.Random(f"{seed}:redact:{item_id}:{level}")
    return [w for w in words if rng.random() >= level]


def run_agent_weak(item: dict, blinded: bool, seed: int) -> dict:
    display = opaque_token(item["entity"]) if blinded else item["entity"]
    prompt = render_prompt(display, item["evidence"], item["candidates"])
    if blinded:
        pick = seeded_guess(item["id"], seed, WEAK_K, "blinded-weak")
        return {"pick": pick, "correct": pick == item["answer"],
                "source": "guess", "recall_attempt": True, "recall_hit": False,
                "prompt": prompt}
    if item["mapped"]:
        return {"pick": item["answer"], "correct": True,
                "source": "recall", "recall_attempt": True, "recall_hit": True,
                "prompt": prompt}
    pick = seeded_guess(item["id"], seed, WEAK_K, "named-weak-fallback")
    return {"pick": pick, "correct": pick == item["answer"],
            "source": "guess", "recall_attempt": True, "recall_hit": False,
            "prompt": prompt}


def run_agent_strong(item: dict, blinded: bool, seed: int) -> dict:
    display = opaque_token(item["entity"]) if blinded else item["entity"]
    prompt = render_prompt(display, item["evidence"], item["candidates"])
    # Agent parses the motif from the sequence: first candidate whose motif
    # appears. Motif identity is carried by the sequence, not the name, so
    # blinding cannot change this parse.
    pick = item["motif_holders"][0]
    return {"pick": pick, "correct": pick == item["answer"],
            "source": "evidence", "recall_attempt": False, "recall_hit": False,
            "prompt": prompt}


def run_agent_passage(item: dict, blinded: bool, seed: int, level: float) -> dict:
    words = redact_words(item["passage_words"], level, item["id"], seed)
    evidence = "Passage: " + " ".join(words)
    display = opaque_token(item["entity"]) if blinded else item["entity"]
    prompt = render_prompt(display, evidence, item["candidates"])
    if item["keyword"] in words:
        return {"pick": item["answer"], "correct": True,
                "source": "evidence", "recall_attempt": False,
                "recall_hit": False, "prompt": prompt}
    if blinded:
        pick = seeded_guess(item["id"], seed, PASSAGE_K, "blinded-passage")
        return {"pick": pick, "correct": pick == item["answer"],
                "source": "guess", "recall_attempt": True, "recall_hit": False,
                "prompt": prompt}
    if item["mapped"]:
        return {"pick": item["answer"], "correct": True,
                "source": "recall", "recall_attempt": True, "recall_hit": True,
                "prompt": prompt}
    pick = seeded_guess(item["id"], seed, PASSAGE_K, "named-passage-fallback")
    return {"pick": pick, "correct": pick == item["answer"],
            "source": "guess", "recall_attempt": True, "recall_hit": False,
            "prompt": prompt}


def run_agent_positive(item: dict) -> dict:
    prompt = render_prompt("CONTROL", item["evidence"], item["candidates"])
    pick = item["line_answer"]  # agent always follows the decisive line
    return {"pick": pick, "correct": pick == item["answer"],
            "source": "line", "recall_attempt": False, "recall_hit": False,
            "prompt": prompt}


def run_recall_probe(item: dict, known: bool) -> dict:
    """Name only, no evidence. Known -> recall table; novel -> unknown."""
    if known and item.get("mapped"):
        return {"pick": item["answer"], "correct": True, "answered": True,
                "source": "recall", "recall_attempt": True, "recall_hit": True}
    return {"pick": None, "correct": False, "answered": False,
            "source": "unknown", "recall_attempt": True, "recall_hit": False}


def accuracy(results: list) -> float:
    return sum(1 for r in results if r["correct"]) / len(results) if results else 0.0


def paired_bootstrap_ci(named: list, blinded: list, n_resamples: int,
                        seed: int, alpha: float = 0.05) -> dict:
    """Paired bootstrap CI for (named acc - blinded acc). Deterministic."""
    n = len(named)
    assert n == len(blinded)
    rng = random.Random(seed)
    diffs = []
    for _ in range(n_resamples):
        idx = [rng.randrange(n) for _ in range(n)]
        diffs.append(sum(named[i] for i in idx) / n -
                     sum(blinded[i] for i in idx) / n)
    diffs.sort()
    lo = diffs[int((alpha / 2) * n_resamples)]
    hi = diffs[int((1 - alpha / 2) * n_resamples) - 1]
    point = sum(named) / n - sum(blinded) / n
    return {"point": point, "ci95": [lo, hi], "n": n,
            "resamples": n_resamples}


def bootstrap_ci(values: list, n_resamples: int, seed: int,
                 alpha: float = 0.05) -> dict:
    """Bootstrap CI for a single accuracy. Deterministic."""
    n = len(values)
    rng = random.Random(seed)
    stats = []
    for _ in range(n_resamples):
        idx = [rng.randrange(n) for _ in range(n)]
        stats.append(sum(values[i] for i in idx) / n)
    stats.sort()
    return {"point": sum(values) / n,
            "ci95": [stats[int((alpha / 2) * n_resamples)],
                     stats[int((1 - alpha / 2) * n_resamples) - 1]],
            "n": n, "resamples": n_resamples}


def run_all(seed: int, n_weak: int, n_strong: int, n_passage: int,
            n_positive: int, n_resamples: int) -> dict:
    """Full run. Returns a JSON-serialisable dict with NO timestamps
    (so a same-seed rerun is byte-identical)."""
    items = generate_items(seed, n_weak, n_strong, n_passage, n_positive)
    out = {"seed": seed, "n": {"weak": n_weak, "strong": n_strong,
                               "passage_per_level": n_passage,
                               "positive": n_positive},
           "bootstrap_resamples": n_resamples}

    w_named = [run_agent_weak(it, False, seed) for it in items["weak"]]
    w_blind = [run_agent_weak(it, True, seed) for it in items["weak"]]
    out["weak"] = {
        "named": bootstrap_ci([int(r["correct"]) for r in w_named],
                              n_resamples, seed + 11),
        "blinded": bootstrap_ci([int(r["correct"]) for r in w_blind],
                                n_resamples, seed + 12),
        "gap": paired_bootstrap_ci([int(r["correct"]) for r in w_named],
                                   [int(r["correct"]) for r in w_blind],
                                   n_resamples, seed + 13),
        "telemetry": {
            "named_recall_attempts": sum(r["recall_attempt"] for r in w_named),
            "named_recall_hits": sum(r["recall_hit"] for r in w_named),
            "blinded_recall_attempts": sum(r["recall_attempt"] for r in w_blind),
            "blinded_recall_hits": sum(r["recall_hit"] for r in w_blind)},
    }

    s_named = [run_agent_strong(it, False, seed) for it in items["strong"]]
    s_blind = [run_agent_strong(it, True, seed) for it in items["strong"]]
    out["strong"] = {
        "named": bootstrap_ci([int(r["correct"]) for r in s_named],
                              n_resamples, seed + 21),
        "blinded": bootstrap_ci([int(r["correct"]) for r in s_blind],
                                n_resamples, seed + 22),
        "gap": paired_bootstrap_ci([int(r["correct"]) for r in s_named],
                                   [int(r["correct"]) for r in s_blind],
                                   n_resamples, seed + 23),
    }

    out["passage"] = {}
    for level in REDACTION_LEVELS:
        p_named = [run_agent_passage(it, False, seed, level)
                   for it in items["passage"]]
        p_blind = [run_agent_passage(it, True, seed, level)
                   for it in items["passage"]]
        out["passage"][str(level)] = {
            "named": bootstrap_ci([int(r["correct"]) for r in p_named],
                                  n_resamples, seed + 31),
            "blinded": bootstrap_ci([int(r["correct"]) for r in p_blind],
                                    n_resamples, seed + 32),
            "gap": paired_bootstrap_ci([int(r["correct"]) for r in p_named],
                                       [int(r["correct"]) for r in p_blind],
                                       n_resamples, seed + 33),
        }

    pos = [run_agent_positive(it) for it in items["positive"]]
    out["positive_control"] = bootstrap_ci([int(r["correct"]) for r in pos],
                                           n_resamples, seed + 41)

    probe_w = [run_recall_probe(it, True) for it in items["weak"]]
    probe_s = [run_recall_probe(it, False) for it in items["strong"]]
    out["recall_probe"] = {
        "weak_accuracy": accuracy(probe_w),
        "weak_answered": sum(r["answered"] for r in probe_w),
        "weak_n": len(probe_w),
        "strong_accuracy": accuracy(probe_s),
        "strong_answered": sum(r["answered"] for r in probe_s),
        "strong_n": len(probe_s),
        "contrast": accuracy(probe_w) - accuracy(probe_s),
    }
    return out


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--n-weak", type=int, default=240)
    ap.add_argument("--n-strong", type=int, default=240)
    ap.add_argument("--n-passage", type=int, default=160)
    ap.add_argument("--n-positive", type=int, default=200)
    ap.add_argument("--resamples", type=int, default=2000)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    res = run_all(args.seed, args.n_weak, args.n_strong, args.n_passage,
                  args.n_positive, args.resamples)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, sort_keys=True)
        f.write("\n")
    return res


if __name__ == "__main__":
    main()
