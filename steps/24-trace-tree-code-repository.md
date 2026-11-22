# 24. Read the code repository of "Trace-Tree Magmas" (`YanbiaoLab/trace-tree-magmas`) on GitHub

- Date: 2026-11-22
- Status label: literature check (S5 of `docs/shared/VERIFICATION_PROTOCOL.md`) of one lead, a
  reading of its public code repository. A lead for the blocked Lean item, not a source of our
  results. No label of our nine laws changes.
- Commit(s): see `git log -- steps/24-trace-tree-code-repository.md`

## In plain words

1. **The question.** A *magma* is a set with one operation `*` that combines two elements into one.
   A *law* is a rule such as `(f(x)*y)*z = y` that must hold for every choice of the letters; a
   structure where it holds is a *model* of the law. Four of our laws have, as far as we can tell,
   an infinite model but no finite model with two or more elements. The finite half of that is a
   hand argument; turning it into a machine-checked proof needs *Lean* (a program that checks
   mathematical proofs written in its own language), which is not installed here (see Blocked in
   `STATE.md`). A 2026 paper, arXiv 2609.05690 ("Trace-Tree Magmas", read in steps 17 and 23),
   proves infinite models of magma laws in Lean and publishes its code on GitHub. This step asks:
   what do its Lean proofs (it calls them *certificates*) look like, which versions of Lean and of
   *Mathlib* (Lean's shared library of mathematics) do they use, and under which *license* (the
   terms that say what others may do with the files) is the code published?

2. **What was done, in order.**
   1. **Read the `robots.txt` files** (the file where a site says what programs may fetch), each in
      its own request. `api.github.com/robots.txt` (21:12:09 UTC) answered 404: there is none, so
      the API (the address `gh api` talks to) states no limits. `github.com/robots.txt` (21:12:14)
      names `Claude-User` and `ClaudeBot` with `Crawl-delay: 1` (one second between requests) and
      says "We also provide an extensive API". So everything below went through the API, at least
      two seconds apart (the wait was inside each command).
   2. **Fetched with `gh api`** (GitHub's command-line tool), 18 requests from 21:12:21 to 21:15:35:
      the repository's description, its top README, the file list of the top folder and of
      `arxiv-v1/`, that folder's README, `LICENSE.md`, `NOTICE` and `FROZEN.md`, the README,
      `REPRODUCIBILITY.md` and `config/judge_contract.json` of the main experiment, the full list of
      file names (993 entries), the smallest of the 636 "trace" certificates (7,210 bytes) and one
      problem file. Then three look-ups to compare version names: the Lean tag `v4.33.1`, the Lean
      commit `4a7ab54d` and the Mathlib commit `0df444a360ea`, and finally the repository's newest
      commit. Nothing else: no other certificate, no PDF, no clone.
   3. **Read** all of it by eye.
   4. **Checked by machine** that each of 15 quotes below occurs exactly once in the file it is
      quoted from, and that the certificate contains none of the words `native_decide`, `sorry`,
      `admit` (Lean shortcuts that `docs/shared/LEAN_CAVEATS.md` warns about), "unary operation" or
      "(2,1)". *Mutation test* (a deliberately corrupted input that a working check must notice):
      one version string changed, one license name changed, `native_decide` planted. The check
      reported all three and exited 1.
   5. **Ran all 24 LOOP gates** (the repository's own checks): all exit 0.

3. **A small example: what one certificate says.** The certificate
   `E38303_to_E2__2793cbb1cbfc.lean` is about the magma law `x = ((y*((x*z)*x))*y)*y` (read off its
   theorem `source_holds`, where the letters are `x`, `v0`, `v1`), number 38303 of the Equational
   Theories Project (ETP) by the file name (not looked up: the local ETP clone's Lean files have no
   `Equation38303`, they stop at 4 operations).
   "to E2" means: it shows the law does not imply `x = y` (ETP law 2), that is, the law has a model
   with more than one element. The model's elements are trees built from three pieces, exactly as in
   step 23: a starting symbol `e`, a one-place builder `k(...)` and a pair builder `p(a, b)`. The
   product `a*b` is the pair `p(a, b)` unless one stated exception applies. The last six lines show
   that the model has two different elements: they take `k(e)` and `e` and prove they are not equal
   (a tree that starts with `k` is not the bare symbol `e`). Our own infinite models would need the
   same three pieces plus our second operation `f` (the one-input operation of our laws).

4. **What came out, and what it means.**
   - **License: several, by part.** The top `LICENSE.md` of the frozen release begins "This is a
     multi-licensed research repository." The README says: "Author-created search/verification code
     and generated Lean certificates use Apache-2.0" and documentation uses CC BY 4.0, while "The
     manuscript remains all rights reserved". GitHub's own license field for the repository is
     empty (it did not recognise the mix). Copying their Lean code into this repository as a model
     for our own would therefore come under Apache-2.0 (keep their notice): that is a license
     question for the owner, not for the loop. Nothing was copied.
   - **Versions.** The Judge's version string in `config/judge_contract.json` is
     `"service_revision": "judge-v3-repl-380d1b2c0dd5-lean-4a7ab54d-mathlib-0df444a360ea"`. The paper
     (step 23) names "Lean 4.33.1, and Mathlib revision 0df444a3". The Mathlib part agrees: commit
     `0df444a360ea...` of Mathlib exists, dated 2026-08-21, with the message "chore: bump toolchain
     to v4.33.1". The Lean part does not match anything I could find: the tag `v4.33.1` of Lean
     points to commit `819816b2...`, and GitHub answers "No commit found for SHA: 4a7ab54d" in the
     Lean repository. So what `lean-4a7ab54d` names is **unknown** (it is not a Lean commit; it may be
     a hash of something else, which I did not find out). No file read here names "4.33.1" itself.
   - **How the certificates are built (one read in full).** Each certificate is one Lean file that
     starts `import JudgeProblem`, defines the tree type (`inductive CM` with `e`, `k`, `p`), defines
     the exceptions as a pair of linked rules (`Code` and `Step`), defines the product with
     `noncomputable def eval (a b : CM) : CM := by classical ...` (it picks the exception output when
     one exists, else the pair), proves each exception has only one output by a size count, proves
     the law (`source_holds`), and ends with a proof that `k(e) ≠ e`. The allowed axioms (basic
     assumptions Lean may use) are listed in the contract as `"Classical.choice", "Quot.sound",
     "propext"`, the three standard ones. The certificate read uses no `native_decide`, `sorry` or
     `admit`.
   - **The statement is not in the repository.** `JudgeProblem` (which defines what a magma is and
     what the goal is) is not among the 993 files; the certificates are checked by a remote service
     ("access to remote Judge v3" is a stated requirement of a rerun). So, following
     `docs/shared/LEAN_CAVEATS.md`, the *statement fidelity* of their certificates (does the Lean
     goal say what the paper says?) cannot be checked from this repository alone. Their offline
     verifier checks file hashes, counts and receipts, not the Lean proofs themselves (by its README;
     not run here).
   - **For us.** The certificate is a usable pattern for a future Lean proof of our four infinite
     models (they would add `f`). It is not a proof of anything about our laws, and the finite half
     (no finite model), which is what our blocked item 1 needs, is not what these certificates do:
     they show only that a model with two elements or more exists.
   - It does NOT mean their certificates are correct: I did not run Lean, did not see `JudgeProblem`,
     and read one certificate of 731.

5. **How a reader can re-check it.** With the GitHub command-line tool `gh`:
   `gh api repos/YanbiaoLab/trace-tree-magmas/contents/arxiv-v1/experiments/unrestricted_four_search_20260904/config/judge_contract.json --jq .content`
   and decode the base64 text (for example with `base64 -d`): expect the `service_revision` line
   quoted above. `gh api repos/leanprover/lean4/git/ref/tags/v4.33.1` should show commit
   `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`, and
   `gh api repos/leanprover-community/mathlib4/commits/0df444a360ea --jq .commit.message` should
   start "chore: bump toolchain to v4.33.1". No script in the repository belongs to this step.

## Goal

Queue item 3 (STATE.md before this run): read the README of `github.com/YanbiaoLab/trace-tree-magmas`
with `gh api`: what its Lean certificates look like, which Lean and Mathlib versions, which license;
compare with "Judge v3 revision 380d1b2c, Lean 4.33.1, and Mathlib revision 0df444a3" from the
paper. Items 1 and 2 wait for the owner (no Lean, no second prover installed).

## Command(s)

In the session's scratch folder (not the repository), times UTC on 2026-11-22:
```
curl -s https://api.github.com/robots.txt                     # 21:12:09, HTTP 404 (none)
curl -s https://github.com/robots.txt                         # 21:12:14, Claude-User etc.: Crawl-delay 1
gh api repos/YanbiaoLab/trace-tree-magmas                     # 21:12:21
gh api repos/YanbiaoLab/trace-tree-magmas/readme              # 21:12:29
gh api repos/YanbiaoLab/trace-tree-magmas/contents/           # 21:12:41
gh api repos/YanbiaoLab/trace-tree-magmas/contents/arxiv-v1   # 21:12:44
gh api .../contents/arxiv-v1/{README.md,LICENSE.md,NOTICE,FROZEN.md}            # 21:12:52 to 21:13:00
gh api .../contents/arxiv-v1/experiments/unrestricted_four_search_20260904/README.md   # 21:13:14
gh api "repos/YanbiaoLab/trace-tree-magmas/git/trees/main?recursive=1"           # 21:13:28
gh api .../unrestricted_four_search_20260904/{config/judge_contract.json,REPRODUCIBILITY.md,
       results/certificates/trace_depth_sweep_soundfix_v5/E38303_to_E2__2793cbb1cbfc.lean}  # 21:13:42 to 21:13:47
gh api .../same_resource_atp_baselines_20260904/judge_canary/problem.json        # 21:14:13
gh api repos/leanprover/lean4/git/ref/tags/v4.33.1                               # 21:14:16
gh api repos/leanprover/lean4/commits/4a7ab54d                                   # 21:14:26, HTTP 422
gh api repos/leanprover-community/mathlib4/commits/0df444a360ea                  # 21:14:29
gh api repos/YanbiaoLab/trace-tree-magmas/commits/main                           # 21:15:35
python -I quotes24.py gh24          # exit 0: 15 of 15 quotes found once, 5 words 0 times
python -I quotes24.py gh24 mutate   # exit 1: FAIL 3 (2 quotes missing, planted native_decide counted)
```
Plus all 24 LOOP gates from `LOOP.md` (all exit 0).

## Inputs

- Repository `YanbiaoLab/trace-tree-magmas`, newest commit `cb07143b47d96676ee6b28e1a2152388dd73ad05`
  (2026-10-14T08:00:59Z), created 2026-09-02, description "Reproducibility package for "Trace-Tree
  Magmas": proof-producing infinite countermodels with Lean 4 certificates and 28 new order-five
  Austin classifications.", language Lean, `license: null`. Top folders: `arxiv-v1/`, `arxiv-v2/`,
  `arxiv-v3/`; all 732 `.lean` files are under `arxiv-v1/` (none under v3; the top README says v2
  "Updated the author contributions statement" and v3 "Updated the author list").
- `arxiv-v1/FROZEN.md`: "immutable snapshot prepared on 2026-09-05".
- Fetched files, SHA-256 of the decoded text:
  - top `README.md`: `cf1821b0fd1944a1ded8097710b66324ebc4ef2a9ba51beee2f4cc64717f63df`
  - `arxiv-v1/README.md`: `ad889b555ab693508a81861ec778b3d12af6d5b269531fa704c80bf34edc1e4f`
  - `arxiv-v1/LICENSE.md`: `4dec9d5ba8e354a93f1014ec1e2b3a51aa6ad2278aa53edd208981a63ab7f300`
  - `arxiv-v1/NOTICE`: `a4c2842869ccf6795dc7c57561970691c3e2d225b4d0db8ad4d5ce265dbc5913`
  - `arxiv-v1/FROZEN.md`: `921382bbdade83d187428cc9e91776159f4388a5d6d4aa3fa839357259913f32`
  - experiment `README.md`: `1958936ec1a4b0f309db951a1e756a9ad21980397bc7deb32abb71ad91cbba5a`
  - `REPRODUCIBILITY.md`: `d2e9d34831f568d34264960d11e6a466198b113a762e2c0c0918776deefde6d9`
  - `config/judge_contract.json`: `ddb10a544816e3bdf4bb6c61dffe6f95d97baf2be0cf8313c5259738cfb585a5`
  - certificate: `2793cbb1cbfc38458de4f17b0acf5fe31dbf115e523f7545eab1ac6734b36974` (its file name
    ends with the first 12 characters of this hash, so the name is a hash prefix)
  - `judge_canary/problem.json`: `05a10021b822af63df0f86a975e6e4113984bcd71fcf74ae08562f07b85b02b8`
- Scratch script `quotes24.py` (not kept), SHA-256
  `761ce28f6e13cae6981b1f6c7dde03758f25e8ab57068ed2d9c30f1002ac28ae`.
- `gh` (GitHub CLI), `curl` (Git for Windows), Python 3.12.10.

## Output

- This step file; README paragraph "Related method" gained one sentence; step list updated.
- Certificate counts by folder (from the file list): 636 `trace_depth_sweep_soundfix_v5`, 60
  `completion_hybrid_soundfix_v5`, 17 `cnf_nf16_..._sound_v3`, 12 `trace_fluctuation_archive`, 3
  `completion_indexed_all_v1`, 2 `guarded_contract_first_v1`, 1 `completion_generalized_index0_full_v1`,
  1 `judge_canary`: 732 `.lean` files. The README says "all 731 Lean certificate/receipt pairs"
  (whether the canary is the one not counted: unknown, not looked at).
- Problem file format (the canary): `"equation1": "x = y * (x * (y * (y * (z * y))))"`,
  `"equation2": "x = y"`, with ETP numbers `4952` and `2`.

## Checks done (and what each one can and cannot catch)

- robots.txt of both GitHub hosts read, each in its own request, before any other request: catches a
  forbidden path. The API host has none; the web host asks one second between requests, kept (two
  seconds or more inside each command).
- Quote and word check by machine with a mutation (3 of 3 plants caught): catches a quote I copied
  wrongly into this file and a forbidden shortcut in the certificate I missed by eye. It cannot
  catch a shortcut in the other 731 `.lean` files, which were not fetched.
- Version comparison through GitHub's own records of the Lean and Mathlib repositories: catches a
  version name I would otherwise have accepted from the paper. It cannot say what `4a7ab54d` is.
- Hash prefix in the certificate's file name equals its SHA-256 start: the file I read is the one the
  release names.

## NOT verified

- The certificates' Lean proofs: not run (no Lean here), and 731 of 732 `.lean` files not read.
- `JudgeProblem` (their Lean statement of "magma", "law", goal): not in the repository; where it is
  published, if anywhere, is unknown. Their statement fidelity is therefore not checked.
- What `lean-4a7ab54d` in the Judge's version string names: unknown. That the Judge used Lean 4.33.1
  rests on the paper's sentence and on the Mathlib commit message, not on a file that says so.
- Their offline verifier `verify_all.py`: not fetched, not run; its scope is taken from the README.
- The other experiment folders (`novelty_audit_...`, `same_resource_atp_...`) and their reports:
  not read beyond file names and the canary problem.
- The license reading is mine, not legal advice; whether copying their Lean pattern into this
  repository is wanted, and under which notice, is the owner's decision.
- Whether the `arxiv-v2/` and `arxiv-v3/` folders change anything but the author lines: only the
  top README's one-line descriptions were read.
- Whether our four models fit their certificate pattern once `f` is added: not tried.

## Surprises, errors, dead ends

- The version string's Lean part is not a Lean commit, while its Mathlib part is a Mathlib commit
  whose message names the Lean version the paper gives. Recorded as unknown, not guessed.
- The first run of the quote script crashed on printing the arrow `→` (Windows console code page
  cp1252) before reaching the verdict, in both the normal and the mutated run. Both exited 1, which
  in the normal run looks like a failed check and in the mutated run like a passing mutation test.
  Fixed by printing with `ascii()`, then rerun. Lesson for the hub in `docs/LOG.md`.
- Slip: the first draft of "Inputs" gave the file hashes as "first 8 ... last 2" characters, and the
  last two were written from memory, not copied; most were wrong. Replaced by the full hashes, and a
  command then found each of the 11 hashes of the scratch files exactly once in this file.
- My first print of the tree request labelled its `sha` field "commit tree sha"; it is the commit
  (`cb07143b...`, the same as `commits/main`), the tree is `fccaff32...`. Only the label was wrong.

## Next

Queue: the Zenodo preprint (now first of the items the loop can do), then the Wrocław and
KoreaScience retry, Ernst's slide, the canonizer check, Knuth-Bendix, Janota-Rawson-Schulz, Austin
1966. New, last: find where `JudgeProblem` is published (by reading the vendored `judge.py` and
`scripts/submit_judge_v3.py` of the same repository), to see how their Lean goal is stated.
