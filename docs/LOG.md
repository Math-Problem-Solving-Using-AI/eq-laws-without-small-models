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
