# State

push: ask   (commit locally only; the owner pushes. Change to `allowed` to let loop sessions push.)

finished: yes (2026-11-23)   (the finish line in `LOOP.md` holds; loop sessions stop.)

## Focus

Decide, for each of the nine laws with no model of size 2 or 3, whether it collapses every structure
to one element, has a finite model, or has only infinite models.
Answered for all nine (2026-11-23): 3 collapse, 2 have a 4-element model, 4 have an infinite model
and no model of size 2 to 6. For those four, "no finite model of any size" is a hand argument only;
machine-checking it is item 1 of "Optional later".

## Queue (take the first item)

(empty: finished, see the finish line in `LOOP.md`)

## Optional later (loop sessions never take these; only the owner moves one to the queue)

Moved here from the queue on 2026-11-23 by the owner's decision. None of them changes an answer:
items 1 and 2 raise labels (Lean, a second prover), item 5 is a second route to a check that
exists, the rest are literature leads. Lean 4.36.0 (elan, no Mathlib) is installed on the owner's
machine since 2026-11-23, so items 1 and 2 are no longer blocked by a missing tool.

1. **Review of the four finite-versus-general leads** (`f(x*(y*z)) = y`, `x*(y*f(z)) = y`,
   `(f(x)*y)*z = y`, `f((x*y)*z) = y`): the counting
   argument is about all finite structures and needs a human reviewer or a Lean proof. Write the
   Lean statement with an English reading next to it and check it as in `docs/shared/LEAN_CAVEATS.md`
   (statement fidelity first). Waits for the owner, see Blocked (no Lean on this machine).
2. **Second independent check of the collapse proofs** (`check_derivation.py` was written in the same
   session as the proof): a Lean proof following `docs/shared/LEAN_CAVEATS.md`, or a second prover.
   Installing a new tool needs the owner. The same Lean file could prove the mirror rule used in
   step 09 (a structure satisfies a law exactly when its mirror satisfies the mirror law), which is
   a hand argument so far.
   Since step 10 each collapse has two stored derivations (the second is the partner's proof read
   backwards); a second checker should check all four. Waits for the owner, see Blocked (step 22:
   no second prover is installed, z3 is the only one).
3. **Retry the Wrocław university digital library** (`digilab.uwr.edu.pl`) for its record of
   Kisielewicz, "Austin identities" (1997): its robots.txt answered 502 twice on 2026-11-22 (step 18).
   Read robots.txt first; fetch nothing if it cannot be read. If the record has the text, read how
   "Austin identity" is defined (any type of algebra, or groupoids only).
   Same run, same rules: retry KoreaScience for J. R. Cho and J. Dudek, "A note on the Austin's
   groupoids" (2006), record `cn=E1BGBB_2006_v22n2_215`, which cites Dudek's 1988 note (step 19):
   its robots.txt gave an empty reply on both domains on 2026-11-22. If readable, record what it
   says about Dudek 1988 and whether it quotes `(ex)y = x`.
4. **Confirm the raised number in Ernst's slides** (`ee = 2^5` where their table gives `2^3`, step
   16): look whether a PDF renderer is already installed (install nothing); if one is, render that
   slide as a picture and read it.
5. **Check by machine that the four infinite models fit the ETP's canonization conditions** (step
   20, a hand reading so far): the ETP report (`paper/metatheorems.tex`, lines 54 to 121 in the
   clone at `dbc9a2b`) proves that a rewrite `R` that is "weakly collapsing, a weak canonizer, and
   non-overlapping" gives a syntactic model, for magmas. Write the three conditions for our models
   with `f` (models A and D rewrite `f`, B and C rewrite `*`), check them with z3 on all terms and
   on a sample by plain code, with a mutation test, and say whether the ETP proof carries over to
   `f` (hand argument until checked). This would be a second route to "the model satisfies its
   law", next to `term_models_z3.py`.
6. **Read the Knuth-Bendix paper (1970)**, "Simple word problems in universal algebras", in the
   open copy at `www.cs.tufts.edu/~nr/cs257/archive/don-knuth/knuth-bendix.pdf` (robots.txt first,
   in its own request): a web-search summary (step 20, not read) says it has an example with a
   unary operator. Record whether it treats free algebras of one binary and one unary operation and
   whether any of our laws or models appear. Needs a way to read the PDF text with tools already
   installed; install nothing.
7. **Read the arXiv abstract page of 2602.16324** (M. Janota, M. Rawson, S. Schulz, "Case study:
   saturations as explicit models in equational theories", 2026, cited in step 23): only `/abs`,
   after arXiv's robots.txt in its own request and 15 seconds from every request. Step 23 quotes
   arXiv 2609.05690 saying "A saturated unit-equational clause set can sometimes be read as a
   convergent rewrite presentation of an explicit, possibly infinite model." Record whether this is
   the same kind of model as our four term models and whether its conditions (termination,
   confluence) could check them; a lead for item 5 (canonization conditions).
8. **Find an open copy of A. K. Austin, "Finite models for laws in two variables"** (Proc. AMS 17,
   1966, pp. 1410–1412, as cited in arXiv 2609.05690, step 23): look up its record in OpenAlex
   (robots.txt `Allow: /`, read again first, 10 seconds between requests) and record where it is
   open. If only on ams.org, add it to the owner's ams.org question under Blocked; fetch nothing
   from ams.org.
9. **Find where `JudgeProblem` of `YanbiaoLab/trace-tree-magmas` is stated** (step 24: every
   certificate starts `import JudgeProblem`, which is not among the repository's 993 files): read
   `arxiv-v1/experiments/unrestricted_four_search_20260904/runner/vendor/solver_runtime_sandbox/judge.py`
   and `scripts/submit_judge_v3.py` with `gh api` (two seconds between requests). Record how their
   Lean goal ("the law has a model with two different elements") is written, if it is shown, as a
   pattern for the Lean statement of blocked item 1. Also unknown from step 24: what `lean-4a7ab54d`
   in their Judge version string names (not a Lean commit).
   Step 25: Peng's preprint says its certificates import "the official `JudgeProblem` module" of
   `github.com/SAIRcompetition/equational-theories-lean-stage2` (revision `817a465`), checked on
   Lean 4.33.1. Look there first (`gh api`, two seconds between requests); that it is the same file
   the trace-tree certificates import is a guess until both are compared.
10. **Could the greedy table-filling method give a second model for one of our four laws?** Peng's
   preprint (step 25) builds models of E5093 and E5107 on 0, 1, 2, ... by filling a partial table
   one cell at a time under seven conditions. Read its Section 2 again and write down, by hand, what
   the conditions would be for one of our laws with `f` (for example `(f(x)*y)*z = y`), or why the
   method does not carry over. A lead for an independent second route to "the law has an infinite
   model" (ours rests on z3, `z3-only`); hand reading until checked by machine.

## Done

- 2026-11-22: steps 01 to 03, see `steps/`. Collapse of `f(x)*(y*z) = y` shown (z3-only), two laws
  have verified models of size 4, two leads recorded.

- 2026-11-22: step 04. The three laws without `f` are settled with the ETP data and the 4-element
  models: `((x*y)*z)*x = w` collapses (trivial), the two others have fully decided rows.

- 2026-11-22: step 05 (loop run 1). `(x*y)*f(z) = y` collapses: hand proof stored as 12 checkable
  steps, accepted by the new plain-Python checker `check_derivation.py` (37 of 37 corrupted copies
  rejected), z3 accepts each lemma. Label `z3-only` plus our own checker. Queue item "five open laws"
  split; four laws remain.

- 2026-11-22: step 06 (loop run 2). `(f(x)*y)*z = y` does not collapse: an infinite model of formal
  terms, checked on all terms by z3 (new `term_models_z3.py`, `z3-only`) and on a sample by plain
  Python. No finite model with 2 or more elements by a counting argument (`hand-argument`). Third
  candidate Austin law. Also fixed: `infinite_models.py` exited 0 even on failure; it now has a
  mutation selftest and fails properly. One law is still open; three are leads whose finite part
  needs a Lean proof or a human review.

- 2026-11-22: step 07 (loop run 3). `f((x*y)*z) = y` does not collapse: an infinite model of
  formal terms, checked on all terms by z3 (`z3-only`) and on a sample by plain Python. No finite
  model with 2 or more elements by a counting argument (`hand-argument`). Fourth candidate Austin
  law. Noticed that the nine laws come in mirror pairs (read `a*b` as `b*a`); this law is the
  mirror of `f(x*(y*z)) = y`. No law is fully open any more.

- 2026-11-22: step 08 (loop run 4). The collapse proof of `f(x)*(y*z) = y` is now stored as 11
  checkable steps in `results/collapse_fx_yz.json` and accepted by `check_derivation.py` (34 of 34
  corrupted copies rejected, each for the intended reason). Label raised from `z3-only` to
  `z3-only` plus our own checker. Added to CI and the LOOP gates.

- 2026-11-22: step 09 (loop run 5). The mirror pairs are checked by machine (`mirror_pairs.py`, in
  CI and the LOOP gates, 9 of 9 mutations rejected): the pairs of step 07 are right, the transposed
  4-element tables are models of the partner law (plain evaluation), the four mirrored infinite
  models are models of the partner law (z3 on all terms, `z3-only`). `x*(y*(z*x)) = w` is not among
  the nine because z3 proves its collapse but not that of its mirror `((x*y)*z)*x = w`. The main
  repository's 712 laws and its 216 laws with no small model are closed under mirroring.

- 2026-11-22: step 10 (loop run 6). Each of the two collapsing laws now has a second stored proof:
  the other law's proof read backwards (`mirror_derivation.py`, `results/*_by_mirror.json`), accepted
  by the unchanged `check_derivation.py` (37 of 37 and 34 of 34 corrupted copies rejected; 10 of 10
  deliberately wrong mirrors rejected). Label unchanged: `z3-only` plus our own checker. In CI and
  the LOOP gates.

- 2026-11-22: step 11 (loop run 7). The four infinite term models refute 707 of 711 targets each
  (2,828 certificates in `results/refutations_term_models.json`, made by `refute_by_term_models.py`,
  recomputed by the new plain-Python `check_refutations.py`, 15 of 15 corruptions rejected, mirror
  cross-check A-D and B-C). The other 4 targets per law are substitution instances of the law
  (implied). Label `z3-only`. General implication only, nothing about finite structures.

- 2026-11-22: step 12 (loop run 8). The 712 law texts and ids copied into
  `results/refutations_term_models.json` are the main repository's: each text equals its text and,
  read by our checker's parser, gives its stored term tree (new `check_copied_laws.py`, 13 of 13
  corrupted inputs rejected, LOOP gate, not in CI because it needs the main repository). The main
  repository's own text check passes on its list (712, 0 mismatches). Labels of step 11 unchanged.

- 2026-11-22: step 13 (loop run 9). Queue item "literature check" split into four items. First
  piece done: the term "Austin law" is defined in the ETP blueprint ("a law which admits infinite
  models, but no nontrivial finite models"), for magmas only; the ETP's published report does not
  use the term. README now says our use for type (2,1) is a carry-over. Kisielewicz's own
  definition not read (unknown). No label changed.

- 2026-11-22: step 14 (loop run 10). Literature check of the collapse of `(x*y)*f(z) = y` and its
  mirror: 6 web and 4 GitHub searches found nothing about the two laws. Their 8 magma special cases
  (`f` replaced by a formula in one letter, up to 4 operations) are ETP equations that the ETP records
  as forcing one element (new `etp_specializations.py`, 7 of 7 corrupted inputs rejected). Agrees
  with our collapse, does not prove it. No label changed.

- 2026-11-22: step 15 (loop run 11). Literature check of the four candidate Austin laws, first
  piece: 5 web and 4 GitHub searches found nothing about the laws. Their 22 magma special cases (up
  to 5 operations) all force one element (ETP table up to order 4, z3 for order 5), as our finite
  argument requires (new `etp_specializations_austin.py`, 13 of 13 corrupted inputs rejected).
  Kisielewicz's Austin laws (ETP Equation28770 and 374794) are instances of a special case of
  `(f(x)*y)*z = y`, with the same finite argument. No label changed. Ernst slides and an arXiv lead
  queued separately.

- 2026-11-22: step 16 (loop run 12). Re-read Ernst's 2008 slides from the primary PDF (after the
  site's robots.txt): the README's quote on Dudek's `(ex)y = x` is word for word right, and the
  slides' infinite model checks on a sample by plain Python (new `dudek_slides_check.py`, 7 of 7
  corrupted inputs rejected); no structure with 2 to 6 elements satisfies the identity (finite
  search). The slides give no reference for Dudek (queued) and print `ee = 2^5` where their table
  gives `2^3`. No label of our laws changed.

- 2026-11-22: step 17 (loop run 13). Read the arXiv abstract page of 2609.05690v3 ("Trace-Tree
  Magmas", 2026), after arXiv's robots.txt: it is about magmas only (no unary operation, no type
  (2,1), none of our law shapes, by reading and by a keyword search with one mutation). Its model
  family (constructor trees, pairing by default, finitely many exceptions, Lean 4 certificates) has
  the shape of our term models. Full text and code repository queued. No label changed.

- 2026-11-22: step 18 (loop run 14). Looked for Kisielewicz's own definition of "Austin identity"
  in open sources: the Wrocław digital library was down (502), zbMATH Open disallows the loop's
  agent, and his publication list, Crossref and OpenAlex have no copy and no abstract of either
  paper (both closed). Definition still unknown. Found on the way: his 1990 chapter cites Dudek,
  "A note on models of identities" (1988), a lead for Dudek's source. No label changed.

- 2026-11-22: step 19 (loop run 15). Looked for Dudek's source for `(ex)y = x` in open places:
  Crossref, OpenAlex and Ježek's universal-algebra bibliography agree that Józef Dudek wrote "A note
  on models of identities", Algebra Universalis 25 (1988), 400-401 (a candidate source). No text,
  abstract or review is open, so what it proves is still unknown. A 2006 paper by Cho and Dudek that
  cites it was found; its site (KoreaScience) did not answer, so it was not read. No label changed.

- 2026-11-22: step 20 (loop run 16). Literature check of the 2,828 non-implications of step 11
  (shallow: 6 web, 5 OpenAlex and 6 GitHub searches, titles and summaries only): none found stated
  anywhere, which does not make them new. The way our four infinite models are built is a known
  method for magmas, the ETP report's "canonizers" (read in the local clone); that our models meet
  its three conditions is a hand reading, queued for a machine check. No label changed.

- 2026-11-22: step 21 (loop run 17). The main repository's list of 712 short laws, used in steps 11
  and 12, is every law with 1 to 3 operations up to renaming letters and swapping sides, each once:
  its own count check passes (712, MATCH), and the new `check_law_list.py` here compares the stored
  file itself with its own brute force (13 of 13 corrupted inputs rejected). A mutation test showed
  the main repository's check cannot see a law listed twice (reported for the owner). No label changed.

- 2026-11-22: step 22 (loop run 18). Title search in the open paper index OpenAlex (14 requests,
  after its robots.txt) for the two collapsing laws and the four candidate Austin laws: nothing found
  about them; three control searches found their known papers, so the search works. New lead: a 2026
  Zenodo preprint on infinite models of two magma Austin identities (queued). Austin 1965 and Stein
  1963 are open only on ams.org, which the loop does not fetch. Queue item 2 moved to Blocked (no
  second prover installed). No label changed.

- 2026-11-22: step 23 (loop run 19). Read the HTML full text of arXiv 2609.05690v3 ("Trace-Tree
  Magmas"), after arXiv's robots.txt: it is about magmas only ("unary" always means a tree builder,
  never an operation of the algebra), none of our laws appears, and it does not quote Kisielewicz's
  definition of "Austin identity" (still unknown). Its models use the same three tree builders and
  the same free-pair default as ours (hand reading). Two leads queued: Janota, Rawson and Schulz
  (arXiv 2602.16324) and Austin 1966. No label changed.

- 2026-11-22: step 24 (loop run 20). Read the code repository of the "Trace-Tree Magmas" paper on
  GitHub (through the API, after both GitHub robots.txt files): its Lean certificates are
  Apache-2.0, the paper's text is all rights reserved; each certificate builds trees from `e`, `k`,
  `p` and proves `k(e) ≠ e`, but imports a `JudgeProblem` file that is not published, so their
  statements cannot be checked from the repository. The Mathlib commit matches "Lean 4.33.1"; the
  Lean part of their version string is not a Lean commit (unknown). Nothing copied. No label changed.

- 2026-11-23: step 25 (loop run 21). Read the Zenodo record and LaTeX source of Peng's 2026
  preprint (after Zenodo's robots.txt): E5093 and E5107 are magma laws (no unary operation), listed
  in the ETP clone as "trivial finite models, unknown infinite models"; the preprint builds infinite
  models by filling a table on 0, 1, 2, ... cell by cell, a different method from our term models,
  and credits an earlier model by "vkg". None of its laws is a special case of ours (new
  `zenodo_e5093_check.py`, 8 of 8 corrupted inputs rejected). It names a public home of
  `JudgeProblem` (added to queue item 9). No label changed.

## Last iteration

2026-11-23 (owner session, after loop run 21): the repository reached its finish line. Every one of the nine laws has an answer, each answer has a machine check, and the README explains it in plain words.
No more loop runs: the remaining work only raises how well the answers are checked or reads more papers, so it moved to "Optional later" for the owner to pick from.

## Blocked

- Optional item 1 and the Lean part of item 2: Lean 4.36.0 was installed by the owner on 2026-11-23
  (elan, toolchain `stable`, no Mathlib yet). Still open for the owner: should a Lean file here
  follow the certificate pattern of `YanbiaoLab/trace-tree-magmas` (Apache-2.0, which asks to keep
  its notice), or be written without looking at it? Whether to add Mathlib, and which version.
- Optional item 2 (second check of the collapse proofs), the part without Lean: no second prover is
  installed either (16 names looked for, only z3 found, 2026-11-22, run 18). Decision needed: may the
  loop install one (for example Vampire, E, Prover9 or Twee), and which?
- zbMATH Open (the part of the literature search of the two collapses that step 22 could not do,
  and the Dudek question closed in step 19): its robots.txt (read 2026-11-22, run 14) says
  `Disallow: /` for `anthropic-ai`, `ClaudeBot` and `Claude-Web`. Decision needed: should the loop
  leave zbMATH alone (current behaviour), or may the owner look up the reviews of Kisielewicz 1990
  and 1997 and Dudek 1988 by hand and save them in the repository? (Step 19: what Dudek 1988 proves
  has no open source either; only a review or the paper itself can tell.)
  Same question for two open papers on ams.org, which the loop does not fetch (step 22): A. K. Austin,
  "A Note on Models of Identities" (Proc. AMS 1965) and S. K. Stein, "Finite Models of Identities"
  (Proc. AMS 1963); may the owner read or save them by hand?
