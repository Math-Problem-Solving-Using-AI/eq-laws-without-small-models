# Nine laws with no small model: do they collapse?

> Part of [math-curiosity](https://github.com/Math-Problem-Solving-Using-AI/math-curiosity): open, reproducible experiments on equational laws, one repository per problem.
> **LLMs and tools:** read [`llms.txt`](llms.txt). **Autonomous sessions:** [`LOOP.md`](LOOP.md) and [`STATE.md`](STATE.md). License: Apache-2.0.

Belongs to [eq-unary-magma-laws](https://github.com/Math-Problem-Solving-Using-AI/eq-unary-magma-laws). Kept as its own problem because it is a self-contained open
question, and because settling it decides 6,399 implication pairs of the main problem
(9 laws, 711 candidate targets each).

## The problem

Setting: structures with one binary operation `*` and one unary operation `f`, no assumptions.
Nine short laws have **no model with 2 or 3 elements**, and z3 did not prove that they force
every structure down to one element ("collapse", the law proves `x = y`).

For each of the nine: does it collapse, or does it have some model (of any size)?

A law that collapses implies every other law. A law with a bigger model does not.

## Current status

Labels are defined in `docs/shared/VERIFICATION_PROTOCOL.md`. No row is Lean-checked.

| Law | Status |
|-----|--------|
| `f(x)*(y*z) = y` | **collapses**. Short hand proof below, every step accepted by z3. `z3-only`. |
| `(x*y)*(y*x) = y` | **does not collapse**: a model with 4 elements, re-checked by plain evaluation (`model-verified`). **Known**: ETP Equation167, *Stein's third law*. Structures satisfying it are "centrist groupoids", and OEIS A128934 counts 0 of them with 2 or 3 elements and 58 with 4. **Row fully decided** (step 04): 710 targets refuted by certificates, 1 implication proved by the ETP. |
| `(x*y)*(y*z) = y` | **does not collapse**, same evidence. **Known**: this is ETP Equation168, the *central groupoid law* (Evans; Knuth 1970, as cited in the ETP paper). Finite central groupoids have n^2 elements, so 4 is the smallest size above 1. **Row fully decided** (step 04): 707 refuted, 4 implications proved by the ETP. |
| `((x*y)*z)*x = w` | **collapses, trivially** (step 04): `w` occurs only on the right, so put `x = y = z = a` and get `a = ((a*a)*a)*a = b` for any `a`, `b`. The ETP data agrees (Equation303 implies `x = y`). Our z3 run had missed it. |
| `(f(x)*y)*z = y` | open. No model of size 4, 5, 6 (z3 `unsat`, `z3-only`). Collapse unproven. |
| `(x*y)*f(z) = y` | open, same |
| `f((x*y)*z) = y` | open, same |
| `f(x*(y*z)) = y` | open, same |
| `x*(y*f(z)) = y` | open, same |

"No model up to size 6" does not rule out larger or infinite models.

### Leads from hand analysis (NOT machine-proven): candidate Austin laws

Vocabulary (literature check, eq-unary-magma-laws `docs/PRIOR_WORK.md`): a law with infinite models
but no nontrivial finite model is called an **Austin law**. ETP blueprint: "no law of order four or
less is an Austin law" for magmas. With a unary operation, size 3 seems enough, much as a short
identity with a constant, `(ex)y = x` (Dudek), has only infinite nontrivial models. So the two laws
below are **candidate Austin laws in type (2,1)**. This kind of result is known in general. We found
nothing about these two specific laws. The arguments were re-read step by step on 2026-11-22
(second reading, still not a human reviewer, not Lean).

For `f(x*(y*z)) = y` and `x*(y*f(z)) = y` I think the answer is: **no finite structure with 2 or
more elements satisfies the law, yet the law does not collapse, because an infinite structure
satisfies it.** If true, each law "forces one element" for finite structures but not in general,
the same kind of finite-versus-general gap the Equational Theories Project reported.

Finite part (counting argument, shown for `f(x*(y*z)) = y`):
1. If `y*z = y'*z'` then `y = f(x*(y*z)) = f(x*(y'*z')) = y'`. So the product `y*z` determines `y`.
2. In a finite structure with n elements, the n sets `{y*z : z}` (one per y) are then disjoint,
   non-empty, and sit inside n elements, so each has exactly one element: `y*z = p(y)` for a
   bijection `p`.
3. Then `f(x*(y*z)) = f(p(x)) = y` for every y, impossible when n is at least 2.
The same counting works for `x*(y*f(z)) = y`: `y*f(z) = p(y)`, so `x*w = p^-1(w)` for all x, w, and
then `p(y) = p^-1(f(z))` for all y, impossible for n at least 2. z3 agrees for sizes 2 to 6.

Infinite part: models built by formula, sample-checked by `infinite_models.py`.
- `f(x*(y*z)) = y`: elements are nested pairs, `x*y` is the formal pair, `f` of a formal pair
  `(x, (y, z))` returns `y`, `f` of anything else returns it unchanged. The law holds by
  construction. Checked on all 17,576 triples from 26 elements, 0 failures.
- `x*(y*f(z)) = y`: `f(t)` is the formal term, `x*w` returns `y` when `w` is the formal pair
  `(y, f(z))`, otherwise the formal pair `(x, w)`. The law holds by construction. Checked on
  300,000 random triples from 144 elements, 0 failures.

Status of both leads: `hand-argument`, construction sample-checked by plain code, **not**
machine-proven, not checked by anyone else, not Lean, not literature-checked. The counting
argument is a statement about all finite structures, which z3 cannot prove, so it needs a Lean
proof or a careful human review.

## Hand proof that `f(x)*(y*z) = y` collapses

Call the law (L). Plain English: multiplying `f(anything)` on the left of a product `y*z` gives
back `y`.

1. **Lemma 1:** if `a*b = c*d` then `a = c`.
   `a = f(x)*(a*b)` by (L), `= f(x)*(c*d)` by assumption, `= c` by (L).
2. Take any `a`, `b`, `c`. Let `e = b*c`. (L) at `x:=a, y:=e, z:=c` gives `f(a)*(e*c) = e`,
   that is `f(a)*((b*c)*c) = b*c`.
3. Apply Lemma 1 to the equation in step 2: `f(a) = b`.
4. `a` and `b` were arbitrary, so every element equals `f(a)`. Any two elements are equal.

Checked by: Claude reading it, and z3 on each lemma (`lemma_chain_f_x_yz.py`). Not checked by a
human mathematician, an independent proof checker, or Lean. Not yet checked against the
literature. A first attempt at step 4 without the instance in step 2 was too weak: z3 returned
`unknown`, because my sketch had skipped the instantiation.

## Steps (granular record)

`steps/`:
1. `01-find-the-laws.md`
2. `02-search-larger-models.md`
3. `03-hand-proof-f-x-yz.md`
4. `04-etp-and-the-three-f-free-laws.md`

## Files

- `zero_model_laws.py` searches for models of size 4 to 6. Output: `results/zero_model_laws.json`
  (the two models found are stored there as tables).
- `lemma_chain_f_x_yz.py` z3 check of the hand proof above.
- Depends on the engine in `src/` of [eq-unary-magma-laws](https://github.com/Math-Problem-Solving-Using-AI/eq-unary-magma-laws) (clone it next to this repository) and its generated data.

## Reproduce

Self-contained checks (CI runs them on every push):

```
pip install -r requirements.txt
python verify_models.py results/zero_model_laws.json            # the two structures, independent evaluator
python verify_models.py --selftest results/zero_model_laws.json # corrupted input must fail
python infinite_models.py                                       # sample check of the infinite constructions
python lemma_chain_f_x_yz.py                                    # z3 on the hand proof (results vary between runs)
```

Regenerating `results/zero_model_laws.json` needs the engine and generated data of
[eq-unary-magma-laws](https://github.com/Math-Problem-Solving-Using-AI/eq-unary-magma-laws). Clone it next to this repository, reproduce its steps, then:

```
P=../eq-unary-magma-laws
python zero_model_laws.py $P/data/laws_3.json $P/data/o3 6 15000     # or set EQ_ENGINE to its src/
```

## Contributing

Open an issue with a reference if you know existing results. Work items are in [`STATE.md`](STATE.md),
protocol in [`LOOP.md`](LOOP.md). Every claim keeps the label it earned.
