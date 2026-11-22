# Log

Running notes of the loop: decisions, mistakes, dead ends, and notes for the owner.

## Decisions taken by the loop

- 2026-11-22 (run 1): queue item 1 ("five open laws") is too big for one session. Split it: this
  run took `(x*y)*f(z) = y` first, because the queue note pointed to it as a likely collapse.
  The other four laws went back to the queue as separate items.
- 2026-11-22 (run 1): the derivation format (`results/collapse_xy_fz.json`) and its checker
  (`check_derivation.py`) are new files in this repository only. No published format of another
  repository was changed. The main repository's queue has a similar item ("Derivations for
  implications"), so the format may need to be aligned later; that is the owner's call.
- 2026-11-22 (run 1): label kept at `z3-only` plus "accepted by our own checker", not raised to
  `independent-prover`. Reason: the checker is new, written in the same session as the proof,
  and unreviewed.
- 2026-11-22 (run 2): queue item 1 (`(f(x)*y)*z = y`) taken whole; it fitted one session. Besides
  the sample check the queue asked for, added `term_models_z3.py`, which checks the infinite models
  on all terms with z3 datatypes, and ran it on the two older infinite models too. Reason: a sample
  is weak evidence for an infinite model, and the z3 question has no quantifiers. No published
  format changed; new files only, plus new CI steps and LOOP gates.
- 2026-11-22 (run 2): label for "does not collapse" kept at `z3-only` (plus a plain-code sample
  check), not higher, because the all-terms check rests on z3 alone.

- 2026-11-22 (run 3): queue item 1 (`f((x*y)*z) = y`) taken whole; it fitted one session. The
  infinite model was added to the two existing checkers (no new format, nothing published). Label
  for "does not collapse" kept at `z3-only`, finite part `hand-argument`, as in run 2.
- 2026-11-22 (run 3): the mirror-pair observation is recorded as a hand argument only. Checking it
  by machine was added to the queue as its own item rather than done in this run, to keep one item
  per run.
- 2026-11-22 (run 4): queue item 1 (store the collapse proof of `f(x)*(y*z) = y` as a derivation)
  taken whole. Of the two routes the queue mentioned, stored the README's own hand proof (step 03)
  rather than the mirror of `results/collapse_xy_fz.json`, so that the proof the README shows is
  the proof that is checked; the mirror route is left to the mirror-pair queue item. New data file
  only, checker unchanged, nothing published. Label kept below `independent-prover`, as in run 1,
  because the checker is our own and unreviewed.

- 2026-11-22 (run 5): queue item 1 (check the mirror pairs by machine) taken whole; it fitted one
  session. New script `mirror_pairs.py` only (imports the parser of `check_derivation.py` and the
  models of `term_models_z3.py`, both unchanged), added to CI and the LOOP gates; nothing published,
  no format changed. Besides the infinite models the queue asked for, it also checks the transposed
  4-element tables, because that costs nothing and tests the pairing on real data. The main
  repository was only read (with `python -B`, so no bytecode was written there). Mirroring the
  stored derivations was left out of this run and put in the queue as its own item.
- 2026-11-22 (run 5): the next queue item (Lean review of the four leads) cannot move: `lean`,
  `lake` and `elan` are not on this machine, and installing a new tool needs the owner. Moved to
  Blocked with the question; the new item "mirror the stored derivations" goes first, since it needs
  nothing new.
- 2026-11-22 (run 6): queue item 1 (mirror the stored derivations) taken: it changes no published
  format, publishes nothing and costs nothing. New data files `results/*_by_mirror.json` beside the
  originals (the originals and `check_derivation.py` unchanged), new script `mirror_derivation.py`,
  added to CI and the LOOP gates. Label of both collapses unchanged (same checker for all four
  proofs). Next free item is 3 (refutation certificates from the infinite models).

- 2026-11-22 (run 7): queue item "use the infinite models to refute implications" taken whole; it
  fitted one session. New certificate format (`results/refutations_term_models.json`: model, target
  law id and text, elements as constructor terms `G`, `F(t)`, `P(a,b)`, both sides' values) and new
  files only; nothing published, no format of another repository changed. The queue said to
  "report the counts" to the main repository: written below under "For other repositories" for the
  owner instead, since the loop does not write there. Label `z3-only` for the non-implications, not
  `model-verified`, because the model is infinite and its law is checked on all terms only by z3.
  The 4 targets per law that were not refuted turned out to be substitution instances of the law;
  the checker now proves that by matching, which decides the four rows. A new queue item checks
  that the copied law texts match the main repository's term trees.
- 2026-11-22 (run 8): queue item 2 (copied law texts) offered two ways: re-run the main
  repository's `src/check_laws_text.py` or write a comparison here. Did both: the main check only
  covers the main list itself, not our copies, so `check_copied_laws.py` compares our ids and texts
  with the main list and reads each text with the parser `check_refutations.py` uses. Added to the
  LOOP gates but not to CI, because CI does not clone the main repository (changing CI to fetch
  another repository was not needed). Nothing published, no format changed.
- 2026-11-22 (run 9): queue item 1 (Lean review) is still blocked, so took item 2 (literature
  check). Too big for one session: split into four items (collapse of `(x*y)*f(z) = y`; the four
  candidate Austin laws; Kisielewicz's definition; the 2,828 non-implications). This run did the
  piece the queue named explicitly, re-reading the source of the term "Austin law". Sources read:
  the local ETP clone (no web request) and one arXiv `/html` page. Nothing published, no format
  changed, only the README paragraph and a new step file.
- 2026-11-22 (run 10): queue item 1 (Lean review) is still blocked, so took item 2 (literature check of
  the collapse of `(x*y)*f(z) = y`). Did it at the depth one run allows: the ETP special cases
  offline, 6 web queries, 4 GitHub queries. A deeper search (zbMATH Open) went back to the queue as
  its own item instead of stretching the run. The ETP lookup became a script with a selftest
  (`etp_specializations.py`) but not a LOOP gate or CI step, because it needs the ETP clone with a
  500 MB table and checks consistency with published data, not a result of ours. Nothing published,
  no format changed.
- 2026-11-22 (run 11): queue item 1 (Lean review) is still blocked, so took item 2 (literature check
  of the four candidate Austin laws). Split: this run did the offline ETP part (special cases up to
  5 operations, the blueprint's Austin chapters), 5 web and 4 GitHub queries; re-reading the Ernst
  slides and opening the arXiv lead 2609.05690 went back to the queue as separate items, because
  each needs a robots.txt step first. Wrote a new script `etp_specializations_austin.py` instead of
  extending `etp_specializations.py`, so the checker of step 14 stays unchanged. Not a LOOP gate or
  CI step (needs the ETP clone). Nothing published, no format changed.
- 2026-11-22 (run 12): queue item 1 (Lean review) is still blocked, so took item 2 (re-read the
  Ernst slides). Two requests to `www.cs.unm.edu` (robots.txt, then the PDF 22 seconds later),
  nothing sent but the two addresses. Wrote `dudek_slides_check.py` to check our reading of the
  slides' formulas; not a LOOP gate and not in CI, like the other literature-check scripts. The
  missing reference for Dudek became its own queue item. Nothing published, no format changed.
- 2026-11-22 (run 13): queue item 1 (Lean review) is still blocked, so took item 2 (arXiv abstract
  page of 2609.05690). Two requests to `arxiv.org` (robots.txt, then `/abs/2609.05690` 29 seconds
  later), nothing sent but the two addresses. Kept to the abstract page as the item said; the HTML
  full text and the paper's code repository became two new queue items at the end, so the older
  items (Kisielewicz, Dudek) keep their turn. No script added: the result is a quote, checked by a
  keyword search with one mutation in the scratch folder. README gained one paragraph and the
  missing step 16 in its step list. Nothing published, no format changed.

- 2026-11-22 (run 14): queue item 1 (Lean review) is still blocked, so took item 2 (Kisielewicz's
  definition of "Austin identity"). Only open sources, each after its robots.txt: the Wrocław
  digital library (robots.txt answered 502 twice, so nothing fetched), zbMATH Open (robots.txt
  disallows the assistant's agents, so nothing fetched), the author's publication list, Crossref and
  OpenAlex (metadata only, no abstract). Nothing sent but the addresses; no e-mail address in the
  Crossref requests, although Crossref asks for one for its faster service. The item is closed with
  the answer "unknown"; a retry of the library became a new queue item, and the zbMATH question went
  to Blocked, because using a site against its robots.txt or through a side door is the owner's
  call. Nothing published, no format changed.

- 2026-11-22 (run 15): queue item 1 (Lean review) is still blocked, so took item 2 (Dudek's source
  for `(ex)y = x`). Only open metadata and one open bibliography, each after its robots.txt: Crossref,
  OpenAlex, Ježek's `bibua.tex`; KoreaScience's robots.txt gave an empty reply, so nothing fetched
  there. Nothing sent but the addresses. Closed the item with "which paper: a candidate by metadata;
  what it proves: unknown", because the remaining part needs the paper or a review, and those are
  behind Springer or zbMATH (owner's call, already under Blocked). The KoreaScience retry joined the
  library retry item, and the PDF-renderer part of the old item became its own small item. No script
  added to the repository: the result is a citation, checked by a scratch script with a mutation.
  Nothing published, no format changed.

## Mistakes and dead ends

- 2026-11-22 (run 1): first draft of the derivation checker's mutation test had two weak
  mutations. (a) Changing the law to `(x*y)*f(z) = x` was rejected only because that text is not
  in the law list, so the step checks were never exercised. Fixed by lifting the law-list guard
  for every mutation except the one that tests it. (b) The "proof ends in `b = b`" mutation was
  rejected because its added step was itself wrong, not because of the final-step guard. Fixed by
  adding valid steps that end in `b = b`. Both found by printing the rejection reason of every
  mutation, not only the count.
- 2026-11-22 (run 1): z3 alone returned `unknown` on the whole collapse of `(x*y)*f(z) = y` at
  5 s, while each lemma was `unsat` at once. An `unknown` from z3 on a collapse question says
  nothing about whether the law collapses.
- 2026-11-22 (run 2): `infinite_models.py` printed "SOME FAILED" but always exited 0, so its CI
  step could never fail and the "independent check" gate was weaker than it looked. Found while
  adding a selftest. Fixed: exit code 1 on failure, and a mutation selftest (6 corrupted models).
- 2026-11-22 (run 2): a planned mutation for Model C (drop the test "first part of the pair is an
  `F(...)`") does not break the law: "a pair times anything gives back its second part" is also a
  model of `(f(x)*y)*z = y`. Not a mutation; replaced by others.

- 2026-11-22 (run 3): runs 1 and 2 worked out `(x*y)*f(z) = y` and `(f(x)*y)*z = y` from scratch,
  although each is the mirror image (read `a*b` as `b*a`) of a law settled earlier
  (`f(x)*(y*z) = y`, `x*(y*f(z)) = y`). Not wrong, only repeated work; it now gives an independent
  second route to each result.

- 2026-11-22 (run 5): a planned mutation "normal form that tries only one side of the equation" was
  not caught on the nine laws, because all nine are written as expression = letter. Dropped from the
  selftest rather than counted.
- 2026-11-22 (run 5): `((x*y)*z)*x = w` reached the list of nine only because z3 is not symmetric
  under mirroring: its mirror `x*(y*(z*x)) = w` was proved to collapse by the same query, three
  times out of three, while z3 gave up on `((x*y)*z)*x = w` three times out of three. A mirror
  check at the time would have settled it at once.

- 2026-11-22 (run 6): two planned mutations of `mirror_derivation.py --selftest` were not useful.
  "Do not mirror inside `f`" produced identical output, because in both proofs `f` only wraps a
  single letter; dropped. "Mirror only the outermost product" was rejected by the script's own
  law-matching guard, so it never reached the checker; replaced by mutations that do (subst terms,
  rewritten terms, claims not mirrored). Found by printing every rejection reason.

- 2026-11-22 (run 7): asking z3 about every law in every infinite model (10 s limit each) did not
  finish the first model in 10 minutes; stopped. A plain search over the 89 terms with at most 7
  symbols found 2,826 of the 2,828 witnesses in seconds; z3 is now used only for the 18 leftovers,
  where it answers at once. `f(f(x)) = f(x)` fails in models A and D only at a term with 9 symbols.
- 2026-11-22 (run 7): a hand-made corrupted file for the exit-code test was not corrupted: the value
  written in was the stored value already. Same mistake as the run 6 lesson; caught because the run
  printed ALL PASS where a failure was expected.
- 2026-11-22 (run 8): the first selftest draft of `check_copied_laws.py` counted a `KeyError`,
  `IndexError` or `StopIteration` as "rejected", so a broken mutation (for example one that looked
  for a certificate that does not exist) would have counted as caught. Changed to count only the
  checker's own `Bad` failure before the first run.
- 2026-11-22 (run 9): the arXiv page (`/html/2512.07087v2`) was requested 7 seconds after
  `robots.txt` on the same site, which asks for `Crawl-delay: 15`. robots.txt was read in its own
  step, as required, but the delay was not counted from that request. One request; no more arXiv
  requests in this run.
- 2026-11-22 (run 10): the first selftest draft of `etp_specializations.py` loaded outcome rows only
  for the expected equations, so the mutation "law that does not collapse" crashed with a `KeyError`.
  It was not counted as caught, because the selftest counts only the checker's own failure (the run 8
  lesson worked). Fixed by loading the rows the mutation needs.
- 2026-11-22 (run 10): no web or GitHub hit for either collapsing law. `gh search code` printed
  nothing at all for three queries; whether code search ran properly is unknown, so it is recorded as
  "no output", not as "no code exists".
- 2026-11-22 (run 11): `mirror_pairs.normal` crashed on order-5 ETP equations (its renaming alphabet
  has 6 letters, some equations have 7). The new script uses its own longer alphabet.
- 2026-11-22 (run 11): an exit-code test replaced a module-level list after import; the function had
  bound that list as a default argument at definition time, so the test changed nothing and seemed
  to show a corrupted input accepted. Re-tested by passing the corrupted list as an argument:
  rejected. The checker was fine, the test was wrong.
- 2026-11-22 (run 11): a mutation draft shifted one of two copies of the same list, so it would have
  been caught by a consistency guard instead of the check it was meant to test. Fixed before running.
- 2026-11-22 (run 12): `pdftotext -bbox` does not exist in the installed `pdftotext` (Glyph & Cog
  4.00, not Poppler), and no PDF renderer is installed, so raised and lowered symbols on the slides
  were read from the page's content stream and font table instead.
- 2026-11-22 (run 12): a Python script passed through a shell here-document lost a backslash and
  did not run; written with the file tool instead.
- 2026-11-22 (run 12): a selftest mutation ("row search that finds nothing for sizes 2 and up")
  could not be rejected, because the right answer is "nothing". Fixed by counting the rows the
  search tries. Two other mutations were first caught by the wrong check; fixed and re-run.
- 2026-11-22 (run 12): the slides write `ee = 2^5` where their own table gives `2^3`; either a typo
  in the slides or our decoding of the raised number is wrong (not rendered as a picture).
- 2026-11-22 (run 13): the keyword script crashed on the Windows console when printing `⋄`
  (`UnicodeEncodeError`, code page cp1252). Printed the keys with `ascii()` instead.
- 2026-11-22 (run 13): the README's step list had stopped at step 15; step 16 had not been added in
  run 12. Added with step 17.

- 2026-11-22 (run 14): queue item 7 (search zbMATH Open) had been queued since run 10 without
  reading zbMATH's robots.txt; read now, it disallows `anthropic-ai`, `ClaudeBot` and `Claude-Web`.
  The item could not be done as planned.
- 2026-11-22 (run 14): `curl` refused `prac.im.pwr.edu.pl` (`SSL certificate problem: unable to get
  local issuer certificate`, incomplete chain sent by the server). Used PowerShell's
  `Invoke-WebRequest` (Windows completes the chain) instead of turning certificate checks off.
- 2026-11-22 (run 14): dead end: `digilab.uwr.edu.pl` answered 502 Bad Gateway to its robots.txt at
  20:32 and 20:33 UTC.

- 2026-11-22 (run 15): the waits between requests to Crossref, OpenAlex and Ježek's server were 6
  to 7 seconds, below the 10 seconds kept in run 14. No site asked for a delay, but it is below our
  own practice.
- 2026-11-22 (run 15): a `sed` mutation of a copy of `bibua.tex` changed only line endings (shell
  quoting of `\A`), so the first mutation run printed the real author. Redone in Python with an
  assert that the text occurs once.
- 2026-11-22 (run 15): dead end: KoreaScience (`www.koreascience.or.kr`, `www.koreascience.kr`) gave
  an empty reply to its robots.txt at 20:40 and 20:41 UTC.

## For other repositories

- eq-unary-magma-laws (for the owner): `(x*y)*f(z) = y` collapses (step 05 here, `z3-only` plus
  our derivation checker). Its 711 targets are implications. Codes 5 for this row can be updated
  when the owner accepts this label.
- eq-unary-magma-laws (for the owner): `(f(x)*y)*z = y` does not collapse (step 06 here, infinite
  model, `z3-only` on all terms). So its row is not "all 711 implications"; implications from it
  must be decided one by one. Its finite part (no finite model with 2 or more elements) is a
  `hand-argument`, so in the finite sense it may still imply everything.

- eq-unary-magma-laws (for the owner): `f((x*y)*z) = y` does not collapse (step 07 here, infinite
  model, `z3-only` on all terms); same situation as `(f(x)*y)*z = y` above. It is the mirror image
  of `f(x*(y*z)) = y`. If the main repository's law list is closed under mirroring, its results
  for one law of a mirror pair may transfer to the other; not checked.

- eq-unary-magma-laws (for the owner): the collapse of `f(x)*(y*z) = y` now has a stored derivation
  (`results/collapse_fx_yz.json`, step 08 here) accepted by our checker, like `(x*y)*f(z) = y`. Its
  label here is `z3-only` plus our own checker; if the main repository records that row as
  `z3-only`, it can be updated when the owner accepts this label.

- eq-unary-magma-laws (for the owner): its 712 laws are closed under mirroring (read every `a*b` as
  `b*a`; 54 laws are their own mirror), and so are its 216 laws with no model of size 2 or 3
  (the 712 by `python mirror_pairs.py --laws-list ../eq-unary-magma-laws/data/laws_3.json`, the 216
  by a one-off script; step 09 here). By
  the mirror rule (a hand argument), A implies B exactly when mirror(A) implies mirror(B), so its
  status matrix could be checked for mirror consistency, and any result for one law of a pair
  transfers to the other. Also: `x*(y*(z*x)) = w` was proved to collapse by its z3 query, and its
  mirror `((x*y)*z)*x = w` collapses by the same two-line argument (step 04 here).

- eq-unary-magma-laws (for the owner): each of the two collapsing laws `f(x)*(y*z) = y` and
  `(x*y)*f(z) = y` now has a second stored derivation, the other law's proof read backwards
  (`results/*_by_mirror.json`, step 10 here), accepted by the same checker. No label change.

- eq-unary-magma-laws (for the owner): the four rows `f(x*(y*z)) = y` (id 450), `x*(y*f(z)) = y`
  (id 639), `(f(x)*y)*z = y` (id 135) and `f((x*y)*z) = y` (id 336), code 5 in its status table, are
  decided for implication over all structures (step 11 here): in each row, 707 targets are NOT
  implied (2,828 certificates in `results/refutations_term_models.json`, witnesses in an infinite
  term model, recomputed by plain Python; label `z3-only` because the model's own law is checked on
  all terms only by z3), and 4 targets are substitution instances of the law (implied). Counts per
  row: 707 not implied, 4 implied. The certificates use the main repository's law ids and texts.
  Updating codes 5 for these rows would need a new code or certificate kind there (infinite models
  are not tables), which is the owner's call.
- eq-unary-magma-laws (for the owner): its `docs/PRIOR_WORK.md` A3(c) quotes the ETP blueprint's
  definition of "Austin law" correctly (re-read here at commit `dbc9a2b` of the ETP clone, step 13).
  Two things it could add: the definition is stated for magmas only, so "candidate Austin laws in
  type (2,1)" is our carry-over; and the ETP's published report (arXiv 2512.07087v2) never uses
  the term, only the blueprint does.
- eq-unary-magma-laws (for the owner): the magma special cases of the two collapsing laws (replace
  `f` by `z`, `z*z`, `z*(z*z)`, `(z*z)*z`) are ETP Equations 30, 174, 1508, 1711 and 15, 178, 1933,
  2136, all recorded by the ETP outcome table (2024-11-10 snapshot) as implying Equation2 (step 14
  here, `etp_specializations.py`). Its `docs/PRIOR_WORK.md` A3(a) names Equation15 only; the other
  seven, and the mirror law `(x*y)*f(z) = y` (Equation30), could be added. No literature hit for the
  laws themselves in 6 web and 4 GitHub queries.


- eq-unary-magma-laws (for the owner): its `docs/PRIOR_WORK.md` could record that Kisielewicz's Austin
  laws, as given in the ETP blueprint (Equation28770 `x = (((y*y)*y)*x)*(y*z)` and Equation374794
  `x = (((y*y)*y)*x)*((y*y)*z)`), are instances of `(f(x)*y)*z = y` (its id 135) with
  `f(t) := (t*t)*t`, and that the blueprint's finite argument for 28770 is the one used here for
  id 135 (step 15 here, `etp_specializations_austin.py`). The 22 magma special cases of ids 135,
  336, 450 and 639 all force one element (ETP table up to order 4, z3 for order 5).
- eq-unary-magma-laws (for the owner): the Ernst slides quote in its `docs/PRIOR_WORK.md` (marked
  "read by subagent") is word for word right: re-read from the primary PDF on 2026-11-22 (step 16
  here, SHA-256 `23bf7d76...470e6f`, `Last-Modified` 2008-08-01). The mark could become "read,
  re-checked". The slides give no reference for Dudek's paper, and print `ee = 2^5` where their
  table gives `2^3` (probable typo, not rendered).

- eq-unary-magma-laws (for the owner): zbMATH Open's robots.txt (last-modified 2025-10-09, read
  2026-11-22) disallows `anthropic-ai`, `ClaudeBot` and `Claude-Web` on the whole site; any queued
  zbMATH search there needs the owner's decision too. Also a lead for its `docs/PRIOR_WORK.md`:
  Kisielewicz's 1990 chapter cites J. Dudek, "A note on models of identities", Algebra Universalis
  25 (1988), 400-401 (DOI `10.1007/BF01229987`), a candidate source for Dudek's `(ex)y = x`
  (title only seen, via Crossref; step 18 here).

## Lessons for the hub

- When a mutation test reports "N of N caught", print the reason each mutation was rejected. A
  mutation can be caught for the wrong reason (an earlier guard, or a broken mutation), which
  leaves the check it was meant to test untested.
- A checker script must exit with a non-zero code when it finds a failure. A script that only prints
  "FAILED" and exits 0 passes every CI run, so the gate is not a gate. Check the exit code with a
  corrupted input as part of the mutation test.
- z3 accessors (`left`, `right` of a datatype) applied to the wrong constructor give unspecified
  values, which z3 chooses freely. When modelling term algebras in z3, guard every accessor with its
  `is_...` test, or the check can fail or pass for a junk reason.
- Before working on a law, look for its mirror image (read every product `a*b` as `b*a`) and its
  other symmetric variants among the laws already settled. A model of a law, with its products read
  backwards, is a model of the mirror law, so their answers are the same. Here two loop runs redid
  work that a mirror would have given at once.

- A solver is not symmetric under mirroring. The same z3
  query with the same time limit proved the collapse of `x*(y*(z*x)) = w` every time and gave up on
  its mirror every time. When a list of "unresolved" laws is built from solver runs, close it under
  the obvious symmetries first: a law whose mirror was settled is settled too.
- Before counting a mutation as caught, check that its output differs from the unmutated output. A
  mutation of a rule the data never exercises (here: mirroring inside `f`, when `f` only wraps
  letters) changes nothing and can only be "not caught"; a count that silently skipped it would
  overstate what was tested.

- To refute implications with an infinite term model, try a plain search over small terms before
  asking a solver: here every witness but two used terms with at most 7 symbols, and the search
  took seconds where z3 on every query did not finish in 10 minutes. Ask the solver only for the
  leftovers, and check its witnesses with plain code.
- When a law is not refuted by a model of itself, check first whether it is just a substitution
  instance of that law (letters made equal). Such targets are implied in one step and need no
  solver.

- A mutation selftest should count as "rejected" only the checker's own failure type. Catching
  generic errors (missing key, index out of range) lets a mutation that crashed while being built
  pass as caught.

- A site's crawl delay counts from every request to it, including the one that fetched
  `robots.txt`. Reading robots.txt "in its own step" is not enough: wait the delay before the first
  page as well.

- A law with an extra operation can be tested against data for the plain operation: replace the extra
  operation by each short formula and look the result up. If the law forces one element, every such
  special case must too. This is a cheap consistency check against published data (it can refute our
  claim, never prove it), and it lists which known results are only special cases of ours.

- A test that corrupts a module-level constant after import does not reach a function that took the
  constant as a default argument (`def check(..., items=ITEMS)` binds the object when the function is
  defined; reassigning `module.ITEMS` later changes nothing). Pass the corrupted value as an
  argument, or the test can report a false alarm or, worse, a false pass.
- When a law has an extra operation, look for published laws of the plain operation that are its
  instances with the extra operation replaced by a formula. Here Kisielewicz's 1997 Austin law turned
  out to be one of our laws with `f(t) := (t*t)*t`, and its published finite argument is ours.
- A search whose correct answer is "nothing found" cannot be told apart from a search that never
  ran. Give it a positive control: count what it tried and compare with the number it must try
  (here every constant times every one-to-one row, `n * n!`), or run it on a variant that does have
  answers.
- When a PDF's text extraction loses raised or lowered symbols and no renderer is available, the
  page's content stream lists each text piece with its font; the font object's encoding tells which
  character a code is. Record that the reading was reconstructed, not seen.
- A keyword search that finds nothing in a source ("the abstract never says unary") is only worth
  something if the same search, run on a copy with the word put in, finds it. Run that positive
  control, and print non-ASCII search keys with `ascii()` on Windows consoles.
- When a step adds a file to a list kept by hand (a README step list), check the list in the same
  commit; here one step was missing for a whole run.
- Read a site's robots.txt when a queue item that needs the site is written, not only when it is
  done. Here a zbMATH search sat in the queue for four runs, and the site disallows the assistant's
  agents. Some sites single out AI agents by name, so "the site is open to everyone" is not enough.
- When a robots.txt cannot be read (server error such as 502), treat the site as unreadable for that
  run; do not fetch pages on the guess that nothing is disallowed. A 404 is different: by the usual
  convention it means the site states no limits.
- A citing-works list from an open index (OpenAlex `filter=cites:`) is a cheap way to find who
  quotes a closed paper; here it turned up a 2006 paper not seen in any earlier search.
- When a mutation is applied with a shell tool, first check that the corrupted copy differs from the
  original where intended (an assert on the count of the replaced text). A mutation that silently
  did nothing looks like a checker failure, or worse, like a pass.
- Put the wait between requests to one site into the command itself (for example a `sleep` inside
  the script that makes the requests), not into the operator's memory.
