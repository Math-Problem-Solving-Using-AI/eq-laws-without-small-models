# State

push: ask   (commit locally only; the owner pushes. Change to `allowed` to let loop sessions push.)

## Focus

Decide, for each of the nine laws with no model of size 2 or 3, whether it collapses every structure
to one element, has a finite model, or has only infinite models.

## Queue (take the first item)

1. **`f((x*y)*z) = y`**: collapse (hand proof written as a derivation for `check_derivation.py`,
   plus a z3 lemma chain) or an infinite model.
2. **Store the collapse proof of `f(x)*(y*z) = y` as a derivation** in the format of
   `results/collapse_xy_fz.json` and check it with `check_derivation.py` (it is `z3-only` today).
3. **Review of the three finite-versus-general leads** (`f(x*(y*z)) = y`, `x*(y*f(z)) = y`,
   `(f(x)*y)*z = y`): the counting
   argument is about all finite structures and needs a human reviewer or a Lean proof. Write the
   Lean statement with an English reading next to it and check it as in `docs/shared/LEAN_CAVEATS.md`
   (statement fidelity first).
4. **Use the infinite models to refute implications:** for law A with an infinite model M, a law B that
   fails in M at explicit elements gives a certificate that A does not imply B. Define a certificate
   format (elements as terms, evaluation by plain code), verify it independently with mutation tests,
   and report the counts to https://github.com/Math-Problem-Solving-Using-AI/eq-unary-magma-laws so its table can be updated.
5. **Literature check** before any novelty claim (in progress in eq-unary-magma-laws `docs/PRIOR_WORK.md`),
   now also for the collapse of `(x*y)*f(z) = y` and the candidate Austin law `(f(x)*y)*z = y`.
   Also re-read the source of the term "Austin law" (eq-unary-magma-laws `docs/PRIOR_WORK.md` and the
   primary page it cites) before using it further.
6. **Second independent check of the collapse proofs** (`check_derivation.py` was written in the same
   session as the proof): a Lean proof following `docs/shared/LEAN_CAVEATS.md`, or a second prover.
   Installing a new tool needs the owner.

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

## Last iteration

2026-11-22 (loop run 2): showed that the rule `(f(x)*y)*z = y` has an endless (infinite) structure that obeys it, so it does not force one element, while a paper argument says no finite structure with two or more elements obeys it.
Next run: the rule `f((x*y)*z) = y`, the only one of the nine rules with no answer or lead yet.

## Blocked

(nothing)
