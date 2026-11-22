# 06. The law `(f(x)*y)*z = y`: no finite model with two or more elements, but an infinite one

- Date: 2026-11-22
- Status label: "does not collapse": infinite model built by hand, law checked on **all** terms
  by z3 (`z3-only`) and on a sample by plain Python. "No finite model with 2 or more elements":
  `hand-argument` (a counting argument), z3 agrees for sizes 2 to 6 only. Not Lean, not reviewed
  by a human, not literature-checked.
- Commit(s): see `git log -- infinite_models.py term_models_z3.py steps/06-f-x-y-z-infinite-model.md`

## In plain words

1. **The question.** A *magma* here is a set with two operations: `*`, which takes two elements and
   gives one, and `f`, which takes one element and gives one. A *law* is a rule that must hold for
   every choice of the letters. A structure that obeys the law is a *model* of it. The law here is
   `(f(x)*y)*z = y`: take `f` of anything, multiply it by `y`, then multiply the result by
   anything, and you must get `y` back. The question: does this law *collapse* (every model has
   exactly one element), or is there a model with more elements?

2. **What was done, in order.**
   1. **Finite structures, by hand.** The law says the product `f(x)*y` remembers `y`: if
      `f(x)*y` and `f(x')*y'` are the same element, then multiplying both by any `z` gives `y = y'`.
      So for a fixed `c = f(a)`, the map "y goes to `c*y`" never sends two elements to the same
      place. In a finite set such a map hits every element. Then every element `u` is `c*y` for
      some `y`, and `u*z = y` does not depend on `z`. In particular `c*z` does not depend on `z`.
      But `c*z` was just shown to give different results for different `z`. Both can only be true
      if there is one element. So **no finite model has two or more elements**. This is an
      argument on paper, not machine-checked.
   2. **Infinite structures.** Because the finite argument used "finite" in an essential way, an
      infinite model might exist. I built one from *formal terms*: expressions that are never
      simplified. Start from one element `g`. `f(t)` is the new expression `F(t)`. A product `u*z`
      is the new expression `P(u, z)` (a "formal pair"), with one exception: when `u` is a pair
      whose first part is an `F(...)`, that is `u = P(F(t), y)`, then `u*z` is `y`. The law then
      holds by construction: `f(x)*y` is `P(F(x), y)` (the exception cannot apply, because
      `F(x)` is not a pair), and `P(F(x), y)*z` is `y` by the exception.
   3. **Plain-code check on a sample.** I added this model ("Model C") to `infinite_models.py`,
      which builds the 144 terms reachable from `g` in 3 rounds and tests the law on 300,000
      random triples. 0 failures. A sample is not all terms, so:
   4. **z3 check on all terms.** *z3* is an automatic solver. It has a built-in notion of formal
      terms (an *algebraic datatype*), whose elements are exactly all finite expressions built from
      `G`, `F` and `P`, with different expressions always different. I wrote `term_models_z3.py`,
      which defines `*` and `f` as plain if-then-else rules over these terms and asks z3 for
      terms `x, y, z` where the law fails. z3 says `unsat`: there are none. It also says `G` and
      `F(G)` are different, so the model has more than one element. I ran the same check on the
      two older infinite models (laws `f(x*(y*z)) = y` and `x*(y*f(z)) = y`): also `unsat`.
   5. **The checkers must be able to say no.** Both scripts got a `--selftest` with 6 damaged
      models (for example `*` returning the wrong part, or `f` doing nothing, or a model tested
      against the wrong law). Each must be caught. Both scripts caught 6 of 6. This is a
      *mutation test*. I also found that `infinite_models.py` always ended with exit code 0, even
      after printing "SOME FAILED", so CI could never fail on it. Fixed: it now exits with 1.
   6. Re-ran all the repository's standard checks. All pass.

3. **A small example.** Two elements 0 and 1, with `f(x) = 0` and `x*y = y` (the product is always
   the right factor). Then `(f(x)*y)*z = y*z = z`, and the law wants `y`. With `y = 0`, `z = 1` it
   fails. The counting argument says every 2-element table fails in some such way. In the
   infinite model, by contrast: `f(g) = F(g)`, `F(g)*g = P(F(g), g)`, and
   `P(F(g), g)*z = g` for every `z`. The law holds, and `g`, `F(g)`, `P(F(g), g)` are three
   different elements.

4. **What it means and what it does not mean.** If both parts are right, this law is a
   *candidate Austin law* (the literature's name, recorded in the main repository's
   `docs/PRIOR_WORK.md`, for a law with infinite models but no finite model with more than one
   element). The infinite part means the law does **not** collapse: it does not imply `x = y`,
   so it does not imply every other law. The finite part means that, among finite structures
   only, it behaves as if it collapsed. It does **not** mean either part is certain: the infinite
   model rests on z3 (`z3-only`) plus a sample check; the finite part is a hand argument about all
   finite sizes, which z3 cannot check (z3 only confirmed sizes 2 to 6). No human and no Lean
   proof has checked either. No literature search was done for this law, so it is not claimed
   to be new.

5. **How to re-check it.** From the repository root:
   ```
   python infinite_models.py
   ```
   expected: a line `Model C (f(x)*y)*z = y: 144 distinct elements (depth 3), 300000 triples
   tested (300000 random), 0 failures`, then `ALL PASS`.
   ```
   python term_models_z3.py
   ```
   expected: three lines ending in `unsat  (unsat = law holds on all terms)`, the line
   `G = F(G)? unsat`, then `ALL PASS (z3-only)`.
   ```
   python infinite_models.py --selftest
   python term_models_z3.py --selftest
   ```
   expected: `selftest: 6 of 6 corrupted models rejected` from each, then `ALL PASS`.

## Goal

Queue item 1: decide whether `(f(x)*y)*z = y` collapses or has an infinite model.

## Command(s)

```
python infinite_models.py
python infinite_models.py --selftest
python term_models_z3.py
python term_models_z3.py --selftest
python verify_models.py results/zero_model_laws.json
python verify_models.py --selftest results/zero_model_laws.json
python check_derivation.py results/collapse_xy_fz.json
python check_derivation.py --selftest results/collapse_xy_fz.json
```

## Inputs

- The model definitions in `infinite_models.py` and `term_models_z3.py` (written by hand).
- `results/zero_model_laws.json`: z3 found no model of sizes 4, 5, 6 for this law (earlier step).
- Python 3.12.10, z3-solver 5.4.1.0.

## Output

Finite part (hand argument), law L = `(f(x)*y)*z = y`, structure with n elements, n finite:
1. If `f(x)*y = f(x')*y'` then `y = (f(x)*y)*z = (f(x')*y')*z = y'` (L twice, any `z`).
2. Fix `a`, let `c = f(a)`. The map `y -> c*y` is injective by 1, so a bijection (finite set).
3. Any `u` is `c*y` for some `y`, so `u*z = (c*y)*z = y` for all `z`: `u*z` does not depend on `z`.
4. With `u = c`: `c*z` is the same for all `z`. With 2 (injective): n = 1.

Infinite part: Model C, elements = all finite terms over `G`, `F(.)`, `P(.,.)`,
`f(t) = F(t)`, `u*z = y` if `u = P(F(t), y)`, else `P(u, z)`.
- `infinite_models.py`: Model C, 144 elements, 300,000 random triples, 0 failures; Models A and B
  unchanged (26 elements all 17,576 triples, 144 elements 300,000 triples, 0 failures).
- `term_models_z3.py`: failing terms exist? `unsat` for Models A, B, C; `G = F(G)?` `unsat`.
- Both selftests: 6 of 6 corrupted models rejected (the reason for each was printed and read:
  plain Python lists failing triples, z3 gives a witness).
- Gates: `2 structures verified, 0 failed`, `selftest passed`, derivation checker
  `COLLAPSE DERIVED`, `37 of 37 corrupted copies rejected`.

## Checks done (and what each one can and cannot catch)

- Sample check by plain Python: catches a construction error that shows up among small terms. It
  cannot rule out a failure on a larger term.
- z3 datatype check: covers all terms, with no quantifiers (the operations are if-then-else over
  constructors), a kind of question z3 decides completely. It relies on z3's datatype reasoning
  and on the z3 encoding matching the Python one (both written by hand from the same description,
  compared by reading).
- Junk values (as in `docs/shared/LEAN_CAVEATS.md` C3): in z3, `left(t)` of a term that is not a
  pair is an unspecified value. The selftest witnesses show z3 really does choose such values.
  Every use of `left`/`right` in the three real models is guarded by an `is_P` test in the same
  condition or branch, so unspecified values cannot change the answer. Checked by reading.
- Mutation tests in both scripts: catch a checker that never reports a failure.
- Finite part: z3 found no model of sizes 2 to 6 (earlier steps). That is consistent with the
  argument but checks only those sizes.

## NOT verified

- The finite part (no finite model with 2 or more elements) is a hand argument about all finite
  sizes. Not machine-checked, not reviewed by a human, no Lean proof.
- The infinite model is `z3-only` on all terms; no second prover, no Lean.
- That the z3 encoding and the Python encoding define the same model was checked only by reading.
- No literature check for this law. Not claimed to be new. "Austin law" is the term recorded in
  the main repository; I did not re-read its source in this run.
- The consequences for the 711 targets of this row in the main repository (refuting implications
  with this infinite model) are not computed. That is queue item "use the infinite models".

## Surprises, errors, dead ends

- `infinite_models.py` printed "SOME FAILED" but still exited with code 0, so the CI step could
  never fail. Fixed in this step (exit code 1 on failure); recorded in `docs/LOG.md`.
- Dropping the condition "the first part is an `F(...)`" from Model C does **not** break the law
  (a pair times anything gives back its second part is also a model). So that is not a valid
  mutation; I used other mutations.
- The finite argument is the same counting idea as for the two earlier leads, so this law is the
  third candidate of the same kind.

## Next

Queue: `f((x*y)*z) = y` (collapse or infinite model). The Lean review item now covers three
finite-versus-general leads.
