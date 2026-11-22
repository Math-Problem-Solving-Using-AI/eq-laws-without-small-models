# State

push: ask   (commit locally only; the owner pushes. Change to `allowed` to let loop sessions push.)

## Focus

Decide, for each of the nine laws with no model of size 2 or 3, whether it collapses every structure
to one element, has a finite model, or has only infinite models.

## Queue (take the first item)

1. **Six open laws**: `((x*y)*z)*x = w`, `(f(x)*y)*z = y`, `(x*y)*f(z) = y`, `f((x*y)*z) = y`,
   `f(x*(y*z)) = y`, `x*(y*f(z)) = y`. For each: look for a hand proof of collapse split into lemmas that
   z3 checks one by one (see `lemma_chain_f_x_yz.py`), or an infinite model (see `infinite_models.py`).
   Useful pattern from the two cases already analyzed: a law of the form "y is recoverable from a
   product" forces an injection, which in a finite structure forces a bijection, which then
   contradicts the law. For `(x*y)*f(z) = y` an attempted infinite model by formal terms ran into a
   conflict, so it may collapse: test with z3 first.
2. **Review of the two finite-versus-general leads** (`f(x*(y*z)) = y`, `x*(y*f(z)) = y`): the counting
   argument is about all finite structures and needs a human reviewer or a Lean proof. Write the
   Lean statement with an English reading next to it and check it as in `docs/shared/LEAN_CAVEATS.md`
   (statement fidelity first).
3. **Use the infinite models to refute implications:** for law A with an infinite model M, a law B that
   fails in M at explicit elements gives a certificate that A does not imply B. Define a certificate
   format (elements as terms, evaluation by plain code), verify it independently with mutation tests,
   and report the counts to https://github.com/MauroBCardoso/eq-unary-magma-laws so its table can be updated.
4. **Cross-check the two `*`-only laws** (`(x*y)*(y*x) = y`, `(x*y)*(y*z) = y`) against the Equational
   Theories Project data. Unknown until read from the primary source.
5. **Literature check** before any novelty claim.

## Done

- 2026-11-22: steps 01 to 03, see `steps/`. Collapse of `f(x)*(y*z) = y` shown (z3-only), two laws
  have verified models of size 4, two leads recorded.

## Last iteration

(none yet)

## Blocked

(nothing)
