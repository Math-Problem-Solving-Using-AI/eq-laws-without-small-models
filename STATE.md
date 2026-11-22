# State

push: ask   (commit locally only; the owner pushes. Change to `allowed` to let loop sessions push.)

## Focus

Decide, for each of the nine laws with no model of size 2 or 3, whether it collapses every structure
to one element, has a finite model, or has only infinite models.

## Queue (take the first item)

1. **`(f(x)*y)*z = y`**: collapse, or an infinite model? Untested hand idea from run 1 (a lead,
   not a result): `(f(x)*y)*z = y` means `f(x)*y` determines `y`, which in a finite structure
   should rule out 2 or more elements; for infinite structures try formal terms: `f(t)` formal,
   `u*z := y` when `u` is the formal pair `(f(x), y)`, otherwise the formal pair `(u, z)`.
   Check any construction with plain code (as in `infinite_models.py`) before any claim.
2. **`f((x*y)*z) = y`**: collapse (hand proof written as a derivation for `check_derivation.py`,
   plus a z3 lemma chain) or an infinite model.
3. **Store the collapse proof of `f(x)*(y*z) = y` as a derivation** in the format of
   `results/collapse_xy_fz.json` and check it with `check_derivation.py` (it is `z3-only` today).
4. **Review of the two finite-versus-general leads** (`f(x*(y*z)) = y`, `x*(y*f(z)) = y`): the counting
   argument is about all finite structures and needs a human reviewer or a Lean proof. Write the
   Lean statement with an English reading next to it and check it as in `docs/shared/LEAN_CAVEATS.md`
   (statement fidelity first).
5. **Use the infinite models to refute implications:** for law A with an infinite model M, a law B that
   fails in M at explicit elements gives a certificate that A does not imply B. Define a certificate
   format (elements as terms, evaluation by plain code), verify it independently with mutation tests,
   and report the counts to https://github.com/Math-Problem-Solving-Using-AI/eq-unary-magma-laws so its table can be updated.
6. **Literature check** before any novelty claim (in progress in eq-unary-magma-laws `docs/PRIOR_WORK.md`),
   now also for the collapse of `(x*y)*f(z) = y`.
7. **Second independent check of the collapse proofs** (`check_derivation.py` was written in the same
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

## Last iteration

2026-11-22 (loop run 1): showed that the rule `(x*y)*f(z) = y` allows only one-element structures, and had a small program check each step of the proof.
Next run: the rule `(f(x)*y)*z = y`; four of the nine rules are still undecided.

## Blocked

(nothing)
