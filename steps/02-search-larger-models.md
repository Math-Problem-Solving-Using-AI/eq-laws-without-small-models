# 02. Search structures of size 4 to 6

- Date: 2026-11-22
- Status label: `model-verified` for the two models found, `z3-only` for the "none found" results
- Commit(s): see this repository's history; engine history in eq-unary-magma-laws

## Goal
For each of the nine laws, look for a model with 4, 5 or 6 elements. A model proves the law
does not collapse.

## Command(s)
```
P=../eq-unary-magma-laws
python zero_model_laws.py $P/data/laws_3.json $P/data/o3 6 15000
```

## Inputs
z3 with a finite enumeration sort for each size. Tables for `*` and `f` are unknown functions,
the law is instantiated for every assignment of elements. Timeout 15 s per size.

## Output
`results/zero_model_laws.json`.
- `(x*y)*(y*x) = y` and `(x*y)*(y*z) = y`: a model of size 4 each, stored as tables.
- The other seven: z3 answered `unsat` at sizes 4, 5 and 6, each in under a second.

## Checks done
- Both models were re-checked by `findmodel.check_model`, a plain-Python evaluator over every
  assignment, independent of z3. Both passed (`independently_verified: true`). That proves these
  two laws do not collapse. Catches: a wrong model returned by the solver.

## NOT verified
- "No model up to size 6" for the other seven is a solver answer. It is not an independent check
  and says nothing about sizes 7 and up or infinite structures.
- Whether the two `*`-only laws were already settled in the Equational Theories Project data.

## Surprises, errors, dead ends
- First run crashed: z3 refuses to declare an enumeration sort with a name already used. Fixed by
  unique names per call. Recorded in `docs/shared/LESSONS.md`.

## Next
Step 03: look for proofs of collapse for the seven.
