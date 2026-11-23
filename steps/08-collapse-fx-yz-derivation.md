# 08. The collapse proof of `f(x)*(y*z) = y`, written as steps a plain checker can verify

- Date: 2026-11-22
- Status label: collapse of `f(x)*(y*z) = y`: `z3-only` plus our own derivation checker (was
  `z3-only`). Not `independent-prover`: the checker was written in this repository (step 05) and
  nobody else has reviewed it. Not Lean, not reviewed by a human, not literature-checked.
- Commit(s): see `git log -- results/collapse_fx_yz.json steps/08-collapse-fx-yz-derivation.md`

## In plain words

1. **The question.** A *magma* here is a set with two operations: `*`, which takes two elements and
   gives one, and `f`, which takes one element and gives one. A *law* is a rule that must hold for
   every choice of the letters. A structure that obeys the law is a *model* of it. A law
   *collapses* when every model has exactly one element, that is, the law forces any two elements
   to be equal. Step 03 showed by hand that the law `f(x)*(y*z) = y` collapses, and the solver z3
   (an automatic prover) accepted each part of that proof. But a z3 answer is only as good as z3,
   so the label was `z3-only`. The question for this step: can the same proof be written as small
   steps that a short, separate program can check without any solver?

2. **What was done, in order.**
   1. **Wrote the proof as 11 single steps** in the file `results/collapse_fx_yz.json`, in the same
      format as the earlier proof for `(x*y)*f(z) = y` (step 05). Each step is one of five simple
      moves: use the law with the letters replaced by expressions ("law"), replace letters in an
      earlier result ("inst"), turn an equation around ("sym"), chain `s = t` and `t = u` into
      `s = u` ("trans"), or replace a part of an expression by something it equals ("rewrite").
      The proof is the one in the README, with its "Lemma 1" spelled out as ordinary steps.
   2. **Checked it with `check_derivation.py`**, the plain-Python checker from step 05. It has its
      own reader for expressions, uses no solver, and checks that every step follows from the law
      or from earlier steps by exactly the stated move, and that the last step says two different
      letters are equal. It accepted all 11 steps. The checker was not changed in this step.
   3. **Checked that the checker can say no** (a *mutation test*): it made 34 damaged copies of the
      proof (a wrong law, a changed replacement, a removed step, a swapped equation, and so on) and
      rejected all 34. I printed the reason for every rejection: each one was rejected at the step
      that was damaged, for the intended reason, not because of some unrelated earlier check. I
      also damaged one claim by hand in a scratch copy (step D8 claiming `b = f(d)`): the checker
      printed `REJECTED` and exited with code 1, so the automatic check on every push (CI) would
      fail.
   4. **Added the two new checks** to CI and to the list of required checks in `LOOP.md`, and re-ran
      every check of the repository. All pass.

3. **A small example.** The proof, in words. Take any elements `a, b, c, d, e`.
   - D1: the law with `x := a`, `y := b*c`, `z := c` says `f(a)*((b*c)*c) = b*c`.
   - D2: the law with `x := d`, `y := f(a)`, `z := (b*c)*c` says `f(d)*(f(a)*((b*c)*c)) = f(a)`.
   - D3 to D5: inside D2, replace `f(a)*((b*c)*c)` by `b*c` (allowed by D1). So `f(d)*(b*c) = f(a)`.
   - D6 and D7: the law with `x := d`, `y := b`, `z := c` says `f(d)*(b*c) = b`.
   - D8: the same expression `f(d)*(b*c)` equals both `b` and `f(a)`, so `b = f(a)`.
   - D9 to D11: the same with `e` in place of `b` gives `e = f(a)`, so `b = e`.
   Since `b` and `e` were any two elements, all elements are equal. Concretely, on two elements
   `{0, 1}` the law already fails for every choice of tables: D8 says every element equals `f(a)`,
   but `f(a)` is one element, and there are two.

4. **What it means and what it does not mean.** It means the collapse of `f(x)*(y*z) = y` no longer
   rests on z3 alone: a short program with no solver, which was shown to reject damaged proofs,
   re-checked every step. Both collapse proofs with `f` in this repository now have this form. It
   does **not** mean the result is proved beyond doubt: the checker was written in this repository
   by the same kind of session, and no human, no second independent checker and no Lean proof has
   looked at it. So the label is `z3-only` plus our own checker, not higher. No literature check
   was done, so the result is not claimed to be new.

5. **How to re-check it.** From the repository root:
   ```
   python check_derivation.py results/collapse_fx_yz.json
   ```
   expected: `results/collapse_fx_yz.json: law 'f(x)*(y*z) = y': 11 steps checked, last step b = e:
   COLLAPSE DERIVED`, then `ALL PASS`.
   ```
   python check_derivation.py --selftest results/collapse_fx_yz.json
   ```
   expected: the same line, then `selftest: 34 of 34 corrupted copies rejected`, then `ALL PASS`.

## Goal

Queue item 1: store the collapse proof of `f(x)*(y*z) = y` as a derivation and check it with
`check_derivation.py` (it was `z3-only`).

## Command(s)

```
python check_derivation.py results/collapse_fx_yz.json
python check_derivation.py --selftest results/collapse_fx_yz.json
python verify_models.py results/zero_model_laws.json
python verify_models.py --selftest results/zero_model_laws.json
python infinite_models.py
python infinite_models.py --selftest
python term_models_z3.py
python term_models_z3.py --selftest
python check_derivation.py results/collapse_xy_fz.json
python check_derivation.py --selftest results/collapse_xy_fz.json
```

Plus, not committed: a short script in a terminal that called `check_derivation.mutations` and
printed the rejection reason of each mutation, and a damaged copy of the derivation in a scratch
folder.

## Inputs

- The hand proof in `README.md` (section "Hand proof that `f(x)*(y*z) = y` collapses", step 03).
- `check_derivation.py` (unchanged since step 05) and `results/zero_model_laws.json` (its law list).
- Python 3.12.10, z3-solver 5.4.1 (z3 is used only by the other gates, not by this check).

## Output

- New file `results/collapse_fx_yz.json`: law `f(x)*(y*z) = y`, 11 steps D1 to D11, last step
  `b = e`.
- `check_derivation.py`: `11 steps checked, last step b = e: COLLAPSE DERIVED`, `ALL PASS`, exit 0.
- Selftest: `34 of 34 corrupted copies rejected`. Rejection reasons read one by one: each at the
  damaged step (or, for a removed step, at the first step that refers to it), with the matching
  message ("does not match the rule", "not an earlier step", "trans needs matching middle terms",
  "subterm at [2, 1] ... is f(a)", "b = b is not an equation between two different variables",
  "not one of the laws").
- Damaged copy (D8 claims `b = f(d)`): `REJECTED: D8: claim 'b = f(d)' does not match the rule,
  which gives b = f(a)`, `FAILED`, exit code 1.
- Other gates: `2 structures verified, 0 failed`, `selftest passed`, `ALL PASS` with `9 of 9`
  for both infinite-model scripts, `ALL PASS (z3-only)` for the z3 term models, `37 of 37` for the
  older derivation.
- `.github/workflows/verify.yml` and `LOOP.md` now run the two new checks.

## Checks done (and what each one can and cannot catch)

- `check_derivation.py`: catches any step that does not follow by its stated rule, a reference to
  a later or missing step, and a proof that does not end in two different variables being equal.
  It cannot catch a bug in the checker itself that accepts a wrong step of a kind the mutations
  do not produce.
- Mutation test with reasons printed: catches a checker that accepts everything, or that rejects
  for an unrelated reason. Covers only the mutation kinds in `mutations()`.
- Exit code with a damaged file: catches a checker whose failure would not fail CI.
- The law text in the derivation must be one of the nine laws in `results/zero_model_laws.json`
  and must read back identically through the parser: catches a typo in the law.

## NOT verified

- `check_derivation.py` itself has not been reviewed by anyone other than the session that wrote it
  (step 05). No second, independent derivation checker was run.
- No Lean proof, no human review of the derivation.
- The rules of the checker (law instance, substitution into an earlier equation, symmetry,
  transitivity, rewriting inside a term) were taken as the standard rules of equational logic; I
  did not check this against a textbook in this run. Reflexivity and congruence are not separate
  rules; rewriting covers what the proofs here need.
- The step-01 claim that this law has no model of size 2 or 3 was not re-checked here (the collapse
  makes it follow anyway).
- No literature check for this law. Not claimed to be new.
- The mirror route (reading every product backwards turns the stored proof for `(x*y)*f(z) = y`
  into a proof for this law) was not used or checked; the stored proof is the README proof
  instead. A machine check of mirrors is queue item "Check the mirror pairs by machine".

## Surprises, errors, dead ends

- None. The derivation was accepted on the first run. The README's "Lemma 1" (if `a*b = c*d` then
  `a = c`) is a conditional statement, which the checker's rules cannot state directly; it was
  written as its one use instead (steps D2 to D5), which is a plain chain of equations.

## Next

Queue: check the mirror pairs by machine (a script that mirrors the nine laws, confirms the pairs,
and checks the mirrored infinite models with z3 on all terms).
