# State

push: ask   (commit locally only; the owner pushes. Change to `allowed` to let loop sessions push.)

## Focus

Decide, for each of the nine laws with no model of size 2 or 3, whether it collapses every structure
to one element, has a finite model, or has only infinite models.

## Queue (take the first item)

1. **Second route to each collapse proof through the mirror** (step 09 left it out): write a small
   script that mirrors a stored derivation (every term read backwards, paths with 1 and 2 swapped
   under `*`, law variables renamed to match the stored law text), apply it to
   `results/collapse_xy_fz.json` to get a proof of `f(x)*(y*z) = y` and to
   `results/collapse_fx_yz.json` to get one of `(x*y)*f(z) = y`, and check both with
   `check_derivation.py`. New data files only; the checker stays unchanged.
2. **Review of the four finite-versus-general leads** (`f(x*(y*z)) = y`, `x*(y*f(z)) = y`,
   `(f(x)*y)*z = y`, `f((x*y)*z) = y`): the counting
   argument is about all finite structures and needs a human reviewer or a Lean proof. Write the
   Lean statement with an English reading next to it and check it as in `docs/shared/LEAN_CAVEATS.md`
   (statement fidelity first). Waits for the owner, see Blocked (no Lean on this machine).
3. **Use the infinite models to refute implications:** for law A with an infinite model M, a law B that
   fails in M at explicit elements gives a certificate that A does not imply B. Define a certificate
   format (elements as terms, evaluation by plain code), verify it independently with mutation tests.
   A certificate for one law gives one for its mirror law (mirror both laws and the model).
   Report the counts to https://github.com/Math-Problem-Solving-Using-AI/eq-unary-magma-laws so its table can be updated.
4. **Literature check** before any novelty claim (in progress in eq-unary-magma-laws `docs/PRIOR_WORK.md`),
   now also for the collapse of `(x*y)*f(z) = y` and the candidate Austin laws `(f(x)*y)*z = y` and
   `f((x*y)*z) = y`.
   Also re-read the source of the term "Austin law" (eq-unary-magma-laws `docs/PRIOR_WORK.md` and the
   primary page it cites) before using it further.
5. **Second independent check of the collapse proofs** (`check_derivation.py` was written in the same
   session as the proof): a Lean proof following `docs/shared/LEAN_CAVEATS.md`, or a second prover.
   Installing a new tool needs the owner. The same Lean file could prove the mirror rule used in
   step 09 (a structure satisfies a law exactly when its mirror satisfies the mirror law), which is
   a hand argument so far.

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

## Last iteration

2026-11-22 (loop run 5): a new program read each of the nine rules backwards and confirmed by machine which rules are mirror images of each other, and that the structures found earlier, read backwards, still obey the mirror rule; it also showed that one rule's mirror is missing from the list only because the solver happened to settle that mirror and not the original.
Next run: read the two stored collapse proofs backwards, which should give a second, independent proof for each mirror rule, and let our checking program check them (the Lean review waits for the owner, because Lean is not installed).

## Blocked

- Queue item 2 (Lean review of the four finite-versus-general leads) and the Lean part of item 5:
  Lean is not installed on this machine (`lean`, `lake`, `elan` not found, 2026-11-22, run 5), and
  installing a new tool needs the owner's decision: should the loop install Lean (elan) and Mathlib,
  and which version?
