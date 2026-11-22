# 01. Find the nine laws

- Date: 2026-11-22
- Status label: z3-only (for the collapse proofs that removed the other 207)
- Commit(s): 3afde82

## Goal
Isolate the laws with no model of size 2 or 3 that z3 could not prove collapse.

## How
See `../../unary-magma-laws/steps/04-collapse-laws.md`: 216 laws have no model of size 2 or 3,
207 were proved to collapse by z3 (accumulated over runs), 9 were not.

## NOT verified
That the other 207 really collapse (z3 only, no stored proof).
That these nine are the same nine on every z3 run: z3 results are unstable between runs. Two
laws, `(x*y)*(z*x) = w` and `f(x)*(x*x) = y`, failed to prove at 60 s in one run but proved at
5 s in another. The set listed in the README is from the accumulated state.

## Next
Step 02: search larger models.
