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

## For other repositories

- eq-unary-magma-laws (for the owner): `(x*y)*f(z) = y` collapses (step 05 here, `z3-only` plus
  our derivation checker). Its 711 targets are implications. Codes 5 for this row can be updated
  when the owner accepts this label.
- eq-unary-magma-laws (for the owner): `(f(x)*y)*z = y` does not collapse (step 06 here, infinite
  model, `z3-only` on all terms). So its row is not "all 711 implications"; implications from it
  must be decided one by one. Its finite part (no finite model with 2 or more elements) is a
  `hand-argument`, so in the finite sense it may still imply everything.

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
