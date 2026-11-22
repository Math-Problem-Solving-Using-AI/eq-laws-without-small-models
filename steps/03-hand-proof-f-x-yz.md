# 03. Hand proof that `f(x)*(y*z) = y` collapses

- Date: 2026-11-22
- Status label: `z3-only`
- Commit(s): see this repository's history; engine history in eq-unary-magma-laws

## Goal
Replace "z3 timed out" for one of the seven open laws with a human-readable argument whose every
step is separately machine-checked.

## How the proof was found
By reading the law as "left-multiplying by `f(anything)` recovers the left factor" and asking
what that forces: the left factor of a product is determined (Lemma 1), and every element is a
product. The statement of the proof is in `../README.md`.

## Command(s)
```
python lemma_chain_f_x_yz.py
```

## Output
```
Lemma 1 (a*b = c*d -> a = c): unsat
Lemma 2 (f constant): unsat
Lemma 3 no hint (collapse x = y): unknown
Lemma 3a (f(a) = b): unsat
Lemma 3 (collapse c = d): unsat
CHAIN COMPLETE (z3-only)
```

## Checks done
- z3 accepts each lemma from the earlier ones. Catches: a wrong step in the hand sketch.
- It DID catch one: my first sketch jumped from Lemma 2 to the collapse and z3 returned
  `unknown`. The missing step was applying the law at the product `y*z`. The corrected proof
  (README, steps 2 to 4) does not need Lemma 2 at all, which the script still checks.

## NOT verified
- Not checked by an independent prover or checker, not in Lean.
- Not checked by a human mathematician.
- Not searched in the literature (the argument is short, it may well be classical).
- z3 results vary between runs, rerun before relying on this.

## Next
Try the same method on the other six laws.
