# 05. The law `(x*y)*f(z) = y` forces one element

- Date: 2026-11-22
- Status label: `z3-only`, plus a derivation accepted by our own plain-Python checker
  (`check_derivation.py`, mutation-tested). Not Lean, not reviewed by a human, not literature-checked.
- Commit(s): see `git log -- results/collapse_xy_fz.json check_derivation.py lemma_chain_xy_fz.py steps/05-collapse-xy-fz.md`

## In plain words

1. **The question.** A *magma* here is a set with two operations: `*`, which takes two elements and
   gives one, and `f`, which takes one element and gives one. A *law* is a rule that must hold for
   every choice of the letters, here `(x*y)*f(z) = y`. A structure that obeys the law is a *model*
   of it. The question: does this law *collapse*, meaning that every model has only one element?
   Earlier runs found no model with 2 to 6 elements, but that left larger and infinite models open.

2. **What was done, in order.**
   1. I looked for a short argument by hand. The law says: multiply any product `x*y` on the
      right by any `f(z)`, and you get back `y`. The trick is to use the law on a product whose
      second factor is itself an `f(...)` (details in "Output" below). It gives a short proof that
      every element equals `f(c)`, so all elements are equal.
   2. A hand proof can hide a skipped step (it happened in step 03). So I wrote the proof down as
      12 small steps in a file, `results/collapse_xy_fz.json`. Each step is one rule of equational
      reasoning: use the law with letters replaced, replace letters in an earlier step, read an
      earlier step backwards, chain two steps, or replace a piece of an expression by something
      equal to it.
   3. I wrote a small checker, `check_derivation.py`, in plain Python (no solver), that reads the
      file and checks that every step follows from the law or from earlier steps by one of those
      rules, and that the last step says two *different* letters are equal.
   4. A checker that never says "no" proves nothing. So the checker also builds 37 damaged copies
      of the proof (changed law, changed substitution, wrong position, swapped sides, missing
      step, a proof that ends in `b = b`, a reference to a later step) and must reject every one.
      This is a *mutation test*. It rejected all 37, each for the expected reason.
   5. As a second, unrelated tool I asked *z3* (an automatic solver) to confirm each of the three
      lemmas of the hand proof (`lemma_chain_xy_fz.py`). It confirmed all three. Asked to find the
      whole proof by itself in 5 seconds, it said `unknown`: it needed the hints.
   6. I re-ran the repository's standard checks. All pass.

3. **A small example.** Take two elements, 0 and 1. Let `x*y = y` (the product is always the right
   factor) and `f(x) = x`. Then `(x*y)*f(z) = y*z = z`, and the law wants `y`. With `y = 0`, `z = 1`
   the left side is 1 and the right side is 0: the law fails. The proof shows this is not bad luck
   of one table: whatever table you pick, `b*f(d)` would have to equal `f(c)` for every `c`, so
   `f` gives the same value everywhere, and then every element would have to be that value.

4. **What it means and what it does not mean.** If the proof is right, the law
   `(x*y)*f(z) = y` has no model with more than one element, of any size, finite or infinite. So
   it implies every other law of the family (all 711 targets of this row in the main repository).
   It does **not** mean the result is certain at the highest level: the label is `z3-only` plus a
   check by a checker we wrote ourselves in this same session. Nobody else has reviewed the
   checker or the proof, there is no Lean proof, and no literature search was done for this law,
   so it is not claimed to be new.

5. **How to re-check it.** From the repository root:
   ```
   python check_derivation.py results/collapse_xy_fz.json
   ```
   expected last two lines: `... 12 steps checked, last step b = e: COLLAPSE DERIVED` and `ALL PASS`.
   ```
   python check_derivation.py --selftest results/collapse_xy_fz.json
   ```
   expected: `selftest: 37 of 37 corrupted copies rejected` and `ALL PASS`.
   ```
   python lemma_chain_xy_fz.py
   ```
   expected: three lines ending in `unsat`, then `CHAIN COMPLETE (z3-only)` (the informational
   "whole claim" line may say `unknown`; z3 results can vary between runs).

## Goal

Decide whether `(x*y)*f(z) = y` collapses (queue item 1, first piece; the queue suggested this
law first because an infinite model by formal terms had run into a conflict).

## Command(s)

```
python check_derivation.py results/collapse_xy_fz.json
python check_derivation.py --selftest results/collapse_xy_fz.json
python lemma_chain_xy_fz.py
python verify_models.py results/zero_model_laws.json
python verify_models.py --selftest results/zero_model_laws.json
python infinite_models.py
```

## Inputs

- `results/zero_model_laws.json` (the checker only accepts a law that is listed there, as a
  guard against a typo in the law text).
- Python 3.12.10, z3-solver 5.4.1.0.

## Output

The hand proof (call the law L):
1. L at `x:=a, y:=b, z:=c`: `(a*b)*f(c) = b`.
2. L at `x:=a*b, y:=f(c), z:=d`: `((a*b)*f(c))*f(d) = f(c)`.
3. Replace `(a*b)*f(c)` by `b` (step 1) inside step 2: `b*f(d) = f(c)`, for all `b, c, d`.
4. L at `x:=a, y:=b, z:=d`: `(a*b)*f(d) = b`. Step 3 with `b:=a*b`: `(a*b)*f(d) = f(c)`.
   So `b = f(c)` for all `b, c`.
5. Any two elements `b`, `e` both equal `f(c)`, so `b = e`.

- `results/collapse_xy_fz.json`: the same proof as 12 checkable steps (E1 to E12).
- `check_derivation.py`: `12 steps checked, last step b = e: COLLAPSE DERIVED`, selftest
  `37 of 37 corrupted copies rejected`.
- `lemma_chain_xy_fz.py`: Lemma 1, 2, 3 `unsat`; whole claim without hints `unknown` (5 s).
- Gates: `2 structures verified, 0 failed`, `selftest passed`, `ALL PASS` (infinite models).

## Checks done (and what each one can and cannot catch)

- `check_derivation.py` on the certificate: catches any step that is not an instance of a rule,
  a wrong substitution, a wrong position, a missing step, and a last step that is not between two
  different letters. It cannot catch an error in the checker's own rules (each rule is a standard
  rule of equational logic, but the code is unreviewed), and it trusts that the law text in
  `results/zero_model_laws.json` is the law meant (that file comes from the main repository's
  enumeration, whose text round-trip is checked there).
- Mutation test: 37 corrupted copies, all rejected; the rejection reason of each was printed
  and read (each is the expected one). The law-list guard is tested by one mutation and lifted
  for the others, so the step checks themselves must catch the damage.
- z3 lemma chain: an independent tool agrees with every lemma. `z3-only` evidence.
- The checker reads the law with its own parser and checks that it prints back to the same text.

## NOT verified

- No human has read the proof or the checker.
- No Lean proof. No independent prover other than z3 (for example Vampire or Prover9) was run.
- The checker was written in the same session as the proof, by the same agent: an error shared
  by both is possible in principle.
- No literature check for this law. Not claimed to be new.
- The 711 implications of this row are only implied by the collapse; the main repository's table
  has not been updated (note left in `docs/LOG.md` for the owner).
- The derivation format is new and not yet used for the other collapse, `f(x)*(y*z) = y`.

## Surprises, errors, dead ends

- z3 alone said `unknown` on the whole claim in 5 s, but each lemma took well under a second.
  Again a hint (here the instance of the law at `x:=a*b, y:=f(c)`) makes the difference.
- The queue note said an infinite model by formal terms "ran into a conflict". The proof explains
  why: the law applied at `y:=f(c)` forces `b*f(d)` to be the same for all `b`.
- First draft of the mutation test had two weak mutations: a changed law was rejected only
  because it is not in the law list, and the "ends in `b = b`" case was rejected for a different
  reason than intended. Both fixed before the first commit (see `docs/LOG.md`).

## Next

Four laws remain open (two of them are the finite-versus-general leads). Next in the queue:
`(f(x)*y)*z = y`.
