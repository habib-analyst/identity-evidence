# G1_STATUS.md — project #120 "identity-evidence"

History file. APPEND only, never overwrite. Each entry is dated in PKT.

## 2026-11-01 ~22:35 PKT — G1 RECHECK: PASS (supplementary-material question resolved)

Paper: arXiv 2610.36510v1, "Identity or Evidence? Auditing Evidence Dependence in
Agentic Life-Science Benchmarks", Danai Brilli / Maria Georgila (Zo Labs),
submitted 27 Oct 2026, v1 only. Workshop paper (AgenticLS: Agentic AI for
Biological Discovery).

### The specific question
The paper was SHELVED (not ranked, not dead) because its full text §2 reportedly
states "Full prompts, raw responses, and scripts are supplementary." Under the
#100 lesson that reads as an author-release-package signal — but the
supplementary files were never downloaded or inspected, so the signal was
unresolved. This G1 resolves it WITHOUT downloading any author supplementary
package, dataset, or code (per task constraint).

### 1. Machine-readable full text — OBTAINED
- Source: https://arxiv.org/html/2610.36510v1 (arXiv HTML v1), fetched
  2026-11-01, HTTP 200, 120,403 bytes, saved locally as arxiv_html.html.
- Tag-stripped text saved as arxiv_fulltext.txt: 28,859 chars, 4,252 words.
- Full text read end-to-end via the HTML version (396 lines). Visual-only
  reading was NOT relied on for the verdict; the sweep below is machine-counted.
- The §2 sentence is confirmed verbatim in §2 ("Related work and protocol"):
  "Full prompts, raw responses, and scripts are supplementary."
  It names no repository, URL, DOI, identifier, licence, or access route.

### 2. Validated sweep of the extracted full text (case-insensitive, tag-stripped)
Counts are from the scripted count over arxiv_fulltext.txt (not hand counts):

| term | count | classification |
|---|---|---|
| github | 3 | ALL arXiv HTML chrome ("Report GitHub Issue" UI). Zero in the paper body. Raw-HTML hrefs containing github are only https://github.com/arXiv/html_feedback/issues and LaTeXML tool links (brucemiller/LaTeXML) — third-party tooling, not an author release. |
| zenodo | 0 | — |
| 4open | 0 | — |
| replication | 2 | Methods words only: "81 external-replication calls" (§3) and "not independent replication across model families" (§4.5). No replication package. |
| supplement | 1 | The single §2 sentence above. No location attached. |
| supplementary | 1 | Same single §2 sentence. |
| anonymous | 0 | — |
| "code is available" | 0 | — |
| "data is available" | 0 | — |
| "available at" | 1 | Methods phrase only: "evidence available at a scientific decision point" (§1). Not a release location. |
| "we release" | 0 | — |
| "will release" | 0 | — |
| "open source" | 0 | — |
| "upon request" | 0 | — |

No author code/data package, release location, or access statement exists
anywhere in the full text. The sweep is clean apart from the one unlocated
§2 sentence.

### 3. Is the supplementary material actually attached/retrievable? — NO
Checked from metadata/listings only; no package, source tarball, or dataset
was downloaded:
- arXiv abs page (https://arxiv.org/abs/2610.36510, fetched 2026-11-01):
  zero occurrences of "ancillar" and zero of "supplement"; NO "Ancillary
  files" section. Only "View PDF" / HTML / TeX Source access links. The
  abs-page "Code, Data and Media" block is arXiv's generic third-party
  toggles (alphaXiv, CatalyzeX, DagsHub, Hugging Face, etc.), not an author
  link — and its "code" hits are those toggle labels only.
- arXiv API record (https://export.arxiv.org/api/query?id_list=2610.36510,
  fetched 2026-11-01, updated 2026-10-27T02:16:05Z): exactly two links —
  alternate (abs page) and related (PDF). No ancillary link, no code/data link.
- Ancillary endpoint probe, headers only (no body downloaded):
  HEAD https://arxiv.org/anc/2610.36510v1 → 404 Not Found.
  The HTML source itself contains zero "/anc/" occurrences.
- (TeX Source exists as application/gzip per a headers-only HEAD on
  /src/2610.36510v1; that is the paper manuscript source, not a
  prompts/responses/scripts package, and it was NOT downloaded.)

Conclusion on the §2 sentence: "are supplementary" is a description of
intended status, not a retrievable attachment. Nothing in the submission
listing, API record, or abs page attaches "full prompts, raw responses, and
scripts" to arXiv:2610.36510v1, and the sentence gives no other route to them.

### 4. Web search for an author repository/package — NONE FOUND
- Search: "Identity or Evidence" + Brilli + Georgila + code repository →
  only the arXiv record; no repo, package, or author page for this paper.
- Search: Danai Brilli / Maria Georgila / Zo Labs + github → only an
  unrelated 2022 GSoC gist by Danai Brilli (DIY Robot) and an unrelated
  "ZoeLabs" Upwork agency. No paper repo.
- Search: 2610.36510 + supplementary/prompts/scripts → no author package;
  results are unrelated prompt-engineering pages.

### 5. G1 VERDICT: PASS
- Supplementary material is NOT actually attached/retrievable, AND the sweep
  is clean (one unlocated sentence, no release location), AND no author
  repo/package was found. Per the task's decision rule, this is a G1 PASS,
  not a KILL.
- Why the #100 signal does not constitute an obtainable package: the §2
  sentence asserts supplementary status without attaching the files to the
  arXiv submission, without naming any external host, and without any
  "available at / upon request / we release" statement. There is nothing
  retrievable to reimplement-from; the open reimplementation (synthetic
  analog, scripted agents, no author data) is therefore legitimate.
- Scope guard: this build uses NO author prompts, responses, scripts, or
  data. All traces are synthetic and generated by our own scripted agents.
  The paper's figures (e.g. 0.742 named vs 0.082 blinded; LitQA2 slope
  +0.147, p=0.004) are context only, never claimed as reproduced.

### 6. #100 RE-EXAMINATION TRIGGER (standing)
If an author package (prompts/responses/scripts repo, Zenodo record, or
attached supplementary files) for arXiv:2610.36510 is located later, this G1
verdict MUST be re-examined before any repo request. A later package
discovery converts this PASS into a re-adjudication, not an automatic KILL —
but no repo request may proceed on the old verdict after such a discovery.

## 2026-11-01 ~22:40 PKT — HEADLINE OUTCOME: PASS (appended after the run)
- Pilot (seed 120001): all gates P1–P5 passed; one pre-lock harness fix
  (passage-corruption flag was a no-op; fixed before PREREG lock, verified
  at item level). See PILOT_RESULT.md.
- PREREG locked before headline; headline seed 120002, 2000 bootstraps.
- All locked bars passed: D1 gap 0.7333 [0.6750, 0.7917]; D2 gap 0.0000;
  D3 gradient 0.5437; M1 positive control 0.9500 [0.9200, 0.9750];
  M2 probe contrast 0.8000; M3 telemetry blinded hits 0/240, named 192/240;
  B1 blinded STRONG 0.9708 [0.9458, 0.9917]. Determinism digest
  27176248d5bc33cb1f4c705f300679ede2948855d81bf82d5e223b3c34ada4b3;
  rerun byte-identical; pytest 10 passed.
- Payload staged here; PAPER.md + DRAFT ONLY LinkedIn draft written to the
  goal hidden_files. No push, no repo creation, no repo request from this
  builder. The #100 re-examination trigger still stands.
