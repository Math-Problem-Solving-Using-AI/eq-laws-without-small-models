# 07. The law `f((x*y)*z) = y`: no finite model with two or more elements, but an infinite one

- Date: 2026-11-22
- Status label: "does not collapse": infinite model built by hand, law checked on **all** terms
  by z3 (`z3-only`) and on all 17,576 triples of a 26-element sample by plain Python. "No finite
  model with 2 or more elements": `hand-argument` (a counting argument), z3 agrees for sizes 2 to
  6 only. Not Lean, not reviewed by a human, not literature-checked.
- Commit(s): see `git log -- infinite_models.py term_models_z3.py steps/07-f-xy-z-infinite-model.md`

## In plain words

1. **The question.** A *magma* here is a set with two operations: `*`, which takes two elements and
   gives one, and `f`, which takes one element and gives one. A *law* is a rule that must hold for
   every choice of the letters. A structure that obeys the law is a *model* of it. The law here is
   `f((x*y)*z) = y`: multiply `x` by `y`, multiply the result by anything, apply `f`, and you must
   get `y` back. The question: does this law *collapse* (every model has exactly one element), or
   is there a model with more elements? It was the last of the nine laws with no answer and no
   lead.

2. **What was done, in order.**
   1. **Finite structures, by hand.** The law says the product `x*y` remembers `y`: if `x*y` and
      `x'*y'` are the same element, then multiplying both by any `z` and applying `f` gives
      `y = y'`. So for each `y`, the set of products `{x*y : x any element}` is not shared with any
      other `y'`. In a finite set with `n` elements there are `n` such sets, none empty, no two
      overlapping, all inside `n` elements. So each set has exactly one element: `x*y` does not
      depend on `x`. Write `x*y = p(y)`. Then the law reads `f(p(z)) = y` for every `y` and `z`.
      The left side does not depend on `y`, so all elements `y` are equal. So **no finite model
      has two or more elements**. This is an argument on paper, not machine-checked.
   2. **Infinite structures.** The argument used "finite" in an essential way (n sets in n
      places), so an infinite model might exist. I built one from *formal terms*: expressions that
      are never simplified. Start from one element `g`. A product `x*y` is the new expression
      `P(x, y)` (a "formal pair"), always. `f(t)` returns `y` when `t` has the shape
      `P(P(x, y), z)`, and returns `t` unchanged otherwise. The law holds by construction:
      `(x*y)*z` is `P(P(x, y), z)`, and `f` of that is `y`.
   3. **Plain-code check on a sample.** I added this model ("Model D") to `infinite_models.py`. It
      builds the 26 terms reachable from `g` in 3 rounds and tests the law on all 17,576 triples
      of them. 0 failures. A sample is not all terms, so:
   4. **z3 check on all terms.** *z3* is an automatic solver. It has a built-in notion of formal
      terms (an *algebraic datatype*), whose elements are exactly all finite expressions, with
      different expressions always different. `term_models_z3.py` now also defines Model D as
      if-then-else rules over these terms and asks z3 for terms `x, y, z` where the law fails. z3
      says `unsat`: there are none. The model has more than one element (for example `g` and
      `P(g, g)` are different terms).
   5. **The checkers must be able to say no.** Each script got 3 more damaged models for Model D
      (`f` returns `z` instead of `y`; `f` does nothing; Model D tested against a different law).
      Both scripts caught 9 of 9 damaged models. This is a *mutation test*. I read z3's
      *witness* (the failing terms it found) for each new damaged model: each one fails for the
      intended reason. I also made damaged copies of both scripts in a scratch folder (not
      committed): each printed `SOME FAILED` and exited with code 1, so CI would fail.
   6. **A shortcut noticed afterwards: mirror images.** Swap the two sides of every product (read
      `a*b` as `b*a`). The law `f(x*(y*z)) = y` (a lead from step 03) then becomes
      `f((z*y)*x) = y`, which is this law with the letters renamed. So any model of one law,
      with its products read backwards, is a model of the other, and the two laws have exactly
      the same answer. Model D is the mirror image of the older Model A, and the finite argument
      above is the mirror image of the older one. The same holds for two other pairs among the
      nine laws (see "Surprises"). This is a short hand argument, not machine-checked.
   7. Re-ran all the repository's standard checks. All pass.

3. **A small example.** Two elements 0 and 1, with `x*y = y` (the product is always the right
   factor) and `f(x) = x`. Then `f((x*y)*z) = z`, and the law wants `y`. With `y = 0`, `z = 1` it
   fails. The counting argument says every 2-element table fails in some such way. In the infinite
   model, by contrast: `g*g = P(g, g)`, `(g*g)*g = P(P(g, g), g)`, and `f` of that is `g`, as the
   law wants. And with `y = P(g, g)`: `(g*y)*g = P(P(g, P(g, g)), g)`, `f` of that is `P(g, g)`.

4. **What it means and what it does not mean.** If both parts are right, this law is a fourth
   *candidate Austin law* (the literature's name, recorded in the main repository's
   `docs/PRIOR_WORK.md`, for a law with infinite models but no finite model with more than one
   element). The infinite part means the law does **not** collapse: it does not imply `x = y`, so
   it does not imply every other law. The finite part means that, among finite structures only,
   it behaves as if it collapsed. It does **not** mean either part is certain: the infinite model
   rests on z3 (`z3-only`) plus a sample check; the finite part is a hand argument about all
   finite sizes, which z3 cannot check (z3 only confirmed sizes 2 to 6). No human and no Lean
   proof has checked either. No literature search was done for this law, so it is not claimed to
   be new. With this step none of the nine laws is fully open any more, but four of them rest on
   a hand argument for their finite part.

5. **How to re-check it.** From the repository root:
   ```
   python infinite_models.py
   ```
   expected: a line `Model D f((x*y)*z) = y: 26 distinct elements (depth 3), 17576 triples tested
   (all), 0 failures`, then `ALL PASS`.
   ```
   python term_models_z3.py
   ```
   expected: four lines ending in `unsat  (unsat = law holds on all terms)`, the line
   `G = F(G)? unsat`, then `ALL PASS (z3-only)`.
   ```
   python infinite_models.py --selftest
   python term_models_z3.py --selftest
   ```
   expected: `selftest: 9 of 9 corrupted models rejected` from each, then `ALL PASS`.

## Goal

Queue item 1: decide whether `f((x*y)*z) = y` collapses or has an infinite model.

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
- `results/zero_model_laws.json`: z3 found no model of sizes 4, 5, 6 for this law (earlier step);
  the main repository found no model of sizes 2 and 3 (step 01; how that search works was not
  re-read in this run).
- `../eq-unary-magma-laws/data/laws_3.json` (read only, to look up a mirror law).
- Python and z3 versions as in step 06 (Python 3.12.10, z3-solver 5.4.1.0; not re-printed in
  this run).

## Output

Finite part (hand argument), law L = `f((x*y)*z) = y`, structure with n elements, n finite:
1. If `x*y = x'*y'` then `y = f((x*y)*z) = f((x'*y')*z) = y'` (L twice, any `z`).
2. The n sets `S_y = {x*y : x}` are non-empty and pairwise disjoint by 1, inside n elements, so
   each is a single element: `x*y = p(y)` for all `x`.
3. L becomes `f(p(z)) = y` for all `y`, `z`. Fix `z`: every `y` equals `f(p(z))`. So n = 1.

Infinite part: Model D, elements = all finite terms (in z3: over `G`, `F(.)`, `P(.,.)`; in plain
Python: generated from `g` by the operations, which yields only `g` and pairs),
`x*y = P(x, y)`, `f(t) = y` if `t = P(P(x, y), z)`, else `t`.
- `infinite_models.py`: Model D, 26 elements, all 17,576 triples, 0 failures. Models A, B, C
  unchanged.
- `term_models_z3.py`: failing terms exist? `unsat` for Models A, B, C, D; `G = F(G)?` `unsat`.
- Both selftests: 9 of 9 corrupted models rejected. z3 witnesses for the new mutations:
  `f returns z`: `y = G, z = F(G)`; `f is the identity`: `x = y = z = G`; `checked against law A`:
  `x = P(G, G), y = F(G), z = G` (f sees the shape `P(P(G,G), ...)` and returns `G`, not `y`).
- Damaged copies (scratch, not committed): `infinite_models.py` with Model D's `f` returning `z`
  printed 16,900 failures, `SOME FAILED`, exit code 1; `term_models_z3.py` with the same damage
  printed `sat` for Model D, `SOME FAILED`, exit code 1.
- Gates: `2 structures verified, 0 failed`, `selftest passed`, derivation checker `ALL PASS`,
  `37 of 37 corrupted copies rejected`.

Mirror duality (hand argument): for a magma `(M, *, f)` define `a *' b = b * a`. Then
`f((x *' y) *' z) = f(z * (y * x))`, which is `y` whenever `(M, *, f)` satisfies
`f(x*(y*z)) = y` (put `x := z`, `z := x`). The converse is the same computation. So
`f((x*y)*z) = y` and `f(x*(y*z)) = y` have models of exactly the same sizes.

## Checks done (and what each one can and cannot catch)

- Sample check by plain Python (all triples of 26 terms): catches a construction error among
  small terms. Cannot rule out a failure on a larger term.
- z3 datatype check: covers all terms, with no quantifiers, a kind of question z3 decides
  completely. Relies on z3's datatype reasoning and on the z3 encoding matching the Python one
  (both written from the same description, compared by reading).
- Junk values: Model D's `f` uses `left(t)` only under `is_P(t)` and `right(left(t))` only under
  `is_P(left(t))`, in the same condition. Checked by reading.
- Mutation tests and witness reading: catch a checker that never reports a failure, or one that
  rejects for the wrong reason.
- Exit codes: damaged copies exit with code 1 (see Output).
- Finite part: z3 found no model of sizes 4 to 6, the main repository none of sizes 2 and 3. Consistent with
  the argument but covers only those sizes.
- Mirror duality: consistent with the data, since `f(x*(y*z)) = y` and this law have identical
  rows in `results/zero_model_laws.json` (`unsat` for 4, 5, 6). That does not check the argument.

## NOT verified

- The finite part (no finite model with 2 or more elements) is a hand argument about all finite
  sizes. Not machine-checked, not reviewed by a human, no Lean proof.
- The infinite model is `z3-only` on all terms; no second prover, no Lean.
- That the z3 and Python encodings define the same model was checked only by reading.
- The mirror-duality argument is a hand argument; not machine-checked.
- Why the mirror of `((x*y)*z)*x = w`, which is `x*(y*(z*x)) = w` in the engine's law list, is not
  among the nine laws: not checked. Possibly it is one of the 207 laws z3 proved to collapse
  (step 01), which would fit its trivial collapse; that is a guess.
- No literature check for this law. Not claimed to be new. The term "Austin law" was not re-read
  at its source in this run.
- Consequences for the 711 targets of this row in the main repository: not computed (queue item
  "use the infinite models").

## Surprises, errors, dead ends

- **The nine laws come in mirror pairs, and earlier runs did not notice.** Reading every product
  backwards turns `f(x*(y*z)) = y` into this law, `x*(y*f(z)) = y` into `(f(x)*y)*z = y` (step 06),
  and `f(x)*(y*z) = y` into `(x*y)*f(z) = y` (step 05). `(x*y)*(y*x) = y` and `(x*y)*(y*z) = y` are
  their own mirrors. So steps 05 and 06 could each have been read off from an earlier step. They
  were done independently, which now serves as a second, independent route to each result, but
  the duality itself is a hand argument. Recorded in `docs/LOG.md` as a lesson for the hub.
- No dead ends in this step: the first model tried passed every check.

## Next

Queue: store the collapse proof of `f(x)*(y*z) = y` as a derivation for `check_derivation.py`. The
Lean review item now covers four finite-versus-general leads.
