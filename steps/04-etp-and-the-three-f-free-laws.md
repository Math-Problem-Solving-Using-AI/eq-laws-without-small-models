# 04. The three laws without `f`: cross-check with the ETP, and their full rows

- Date: 2026-11-22
- Status label: `((x*y)*z)*x = w` collapses (two-line hand proof, ETP data agrees). The rows of
  `(x*y)*(y*x) = y` and `(x*y)*(y*z) = y` are fully decided: non-implications `model-verified`,
  implications `known (ETP)`. `(x*y)*(y*z) = y` is the known central groupoid law.
- Commit(s): see `git log -- steps/04-etp-and-the-three-f-free-laws.md`. The computations are in the
  main repository eq-unary-magma-laws, steps 08 and 09.

## Goal

Three of the nine laws do not mention `f`, so they are ordinary magma laws. The Equational Theories
Project (ETP) settled all implications between magma laws with at most 4 operations. Use that, and
the 4-element models found in step 02, to settle these three.

## Command(s)

In eq-unary-magma-laws (see its steps 08 and 09 for the inputs and hashes):
```
python src/etp_crosscheck.py <ETP>/data/equations.txt general_outcomes.json.gz results/etp_crosscheck.json
python src/refute_from_ffree_models.py results/witnesses_ffree_models.json
python src/verify_witnesses.py results/witnesses_ffree_models.json
```

## Output

| Law | ETP number | What we now know |
|-----|------------|------------------|
| `((x*y)*z)*x = w` | Equation303 `x = ((y ◇ z) ◇ w) ◇ y` | Collapses. Hand proof: for any `a`, `b`, put `x = y = z = a`. The law with `w = a` gives `((a*a)*a)*a = a`, and with `w = b` gives `((a*a)*a)*a = b`, so `a = b`. The ETP says Equation303 implies Equation2 `x = y` (`implicit_proof_true`). |
| `(x*y)*(y*x) = y` | Equation167 `x = (y ◇ x) ◇ (x ◇ y)` | ETP `data/smallest_magma.txt` lists `167 4`, matching our 4-element model. Of its 711 targets, 710 are refuted by a 4-element certificate (the known table plus a chosen `f`), and 1 (`(x*x)*(x*x) = x`) is an implication proved by the ETP. |
| `(x*y)*(y*z) = y` | Equation168 `x = (y ◇ x) ◇ (x ◇ z)` | The **central groupoid law**. The ETP paper (`paper/intro.tex`, commit dbc9a2b) says it "is an order-3 law introduced by Evans and studied further by Knuth", and that "all finite central groupoids have order equal to a perfect square n^2". ETP `smallest_magma.txt` lists `168 4`. 707 targets refuted by certificates, 4 are implications proved by the ETP. |

## Checks done (and what each one can and cannot catch)

- See the main repository, steps 08 and 09: the mapping to ETP numbers was checked for
  completeness and self-tested, and the certificates were re-checked by the independent verifier
  and mutation-tested. None of our certificates contradicts an ETP implication.
- The hand proof for `((x*y)*z)*x = w` is two substitutions. The only thing to check is that `w`
  does not occur on the left, which is visible in the text.

## NOT verified

- The ETP's own Lean proofs and closure tool (we use the published data).
- Evans' and Knuth's papers (only cited through the ETP paper).
- The five implications are not re-proved by us.

## Surprises, errors, dead ends

- `((x*y)*z)*x = w` should never have been on the "open" list. Any law with a variable that occurs
  only alone on one side collapses at once. Our z3 run gave `unknown` at 5 s, and nobody looked at the
  law. Lesson recorded in the hub's `docs/LESSONS.md`.
- Five laws remain open, all with `f` (two of them are the finite-versus-general leads).

## Next

The five open laws, all with `f` (queue in `STATE.md`).
