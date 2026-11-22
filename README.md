# Nine laws with no small model: do they collapse?

Belongs to `../unary-magma-laws`. Kept as its own problem because it is a self-contained open
question, and because settling it decides 6,399 implication pairs of the main problem
(9 laws, 711 candidate targets each).

## The problem

Setting: structures with one binary operation `*` and one unary operation `f`, no assumptions.
Nine short laws have **no model with 2 or 3 elements**, and z3 did not prove that they force
every structure down to one element ("collapse", the law proves `x = y`).

For each of the nine: does it collapse, or does it have some model (of any size)?

A law that collapses implies every other law. A law with a bigger model does not.

## Current status

Labels are defined in `docs/VERIFICATION_PROTOCOL.md`. No row is Lean-checked.

| Law | Status |
|-----|--------|
| `f(x)*(y*z) = y` | **collapses**. Short hand proof below, every step accepted by z3. `z3-only`. |
| `(x*y)*(y*x) = y` | **does not collapse**: a model with 4 elements, re-checked by plain evaluation. `model-verified`. Contains no `f`, so already inside the Equational Theories Project's scope, NOT yet cross-checked against its data. |
| `(x*y)*(y*z) = y` | same as above: model with 4 elements, `model-verified`, not cross-checked against ETP. |
| `((x*y)*z)*x = w` | open. No model of size 4, 5, 6 (z3 `unsat`, `z3-only`). Collapse unproven. |
| `(f(x)*y)*z = y` | open, same |
| `(x*y)*f(z) = y` | open, same |
| `f((x*y)*z) = y` | open, same |
| `f(x*(y*z)) = y` | open, same |
| `x*(y*f(z)) = y` | open, same |

"No model up to size 6" does not rule out larger or infinite models.

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

## Files

- `zero_model_laws.py` searches for models of size 4 to 6. Output: `results/zero_model_laws.json`
  (the two models found are stored there as tables).
- `lemma_chain_f_x_yz.py` z3 check of the hand proof above.
- Depends on the engine in `../unary-magma-laws/src` and its generated data.

## Reproduce

From the repo root, after reproducing the main problem's steps:

```
P=problems/unary-magma-laws
.venv/Scripts/python.exe problems/laws-without-small-models/zero_model_laws.py $P/data/laws_3.json $P/data/o3 6 15000
.venv/Scripts/python.exe problems/laws-without-small-models/lemma_chain_f_x_yz.py
```

## Next

- Try to find hand proofs (or larger models) for the six open laws, each with a lemma chain.
- Store derivations that a tiny independent checker can verify (the protocol's S2).
- Cross-check the two `*`-only laws with the ETP data.
