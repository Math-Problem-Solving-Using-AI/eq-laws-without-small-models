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
| `f(x)*(y*z) = y` | **collapses**. Short hand proof below, written as 11 steps in `results/collapse_fx_yz.json` and accepted by our plain-Python checker `check_derivation.py` (step 08); a second, different 12-step proof, the proof of `(x*y)*f(z) = y` read backwards, is accepted too (step 10); z3 accepts each lemma. `z3-only` plus our own checker, no human review, no Lean. |
| `(x*y)*(y*x) = y` | **does not collapse**: a model with 4 elements, re-checked by plain evaluation (`model-verified`). **Known**: ETP Equation167, *Stein's third law*. Structures satisfying it are "centrist groupoids", and OEIS A128934 counts 0 of them with 2 or 3 elements and 58 with 4. **Row fully decided** (step 04): 710 targets refuted by certificates, 1 implication proved by the ETP. |
| `(x*y)*(y*z) = y` | **does not collapse**, same evidence. **Known**: this is ETP Equation168, the *central groupoid law* (Evans; Knuth 1970, as cited in the ETP paper). Finite central groupoids have n^2 elements, so 4 is the smallest size above 1. **Row fully decided** (step 04): 707 refuted, 4 implications proved by the ETP. |
| `((x*y)*z)*x = w` | **collapses, trivially** (step 04): `w` occurs only on the right, so put `x = y = z = a` and get `a = ((a*a)*a)*a = b` for any `a`, `b`. The ETP data agrees (Equation303 implies `x = y`). Our z3 run had missed it. |
| `(f(x)*y)*z = y` | **does not collapse** (step 06): an infinite model of formal terms, law checked on all terms by z3 (`z3-only`) and on a sample by plain Python. No finite model with 2 or more elements by a counting argument (`hand-argument`; z3 agrees for sizes 2 to 6). Candidate Austin law, see leads below. **Row decided for general implication** (step 11): 707 targets fail in the infinite model (witnesses checked by plain code, `z3-only` because the model itself is), 4 are instances of the law. |
| `(x*y)*f(z) = y` | **collapses** (step 05). Short hand proof below, written as 12 steps in `results/collapse_xy_fz.json` and accepted by our plain-Python checker `check_derivation.py` (mutation-tested); a second 11-step proof, the proof of `f(x)*(y*z) = y` read backwards, is accepted too (step 10); z3 accepts each lemma. `z3-only` plus our own checker, no human review, no Lean. |
| `f((x*y)*z) = y` | **does not collapse** (step 07): infinite model of formal terms, law checked on all terms by z3 (`z3-only`) and on a sample by plain Python. No finite model with 2 or more elements by a counting argument (`hand-argument`; z3 agrees for sizes 2 to 6). It is the mirror image of `f(x*(y*z)) = y` (read every product backwards), so the two laws have the same answer. Candidate Austin law. **Row decided for general implication** (step 11), as for `(f(x)*y)*z = y`. |
| `f(x*(y*z)) = y` | lead, see below: infinite model checked on all terms by z3 (`z3-only`), finite part `hand-argument`. **Row decided for general implication** (step 11), as above. |
| `x*(y*f(z)) = y` | lead, same; row decided for general implication (step 11). |

"No model up to size 6" does not rule out larger or infinite models.

**What the four infinite models refute** (step 11): for each of the four laws with an infinite
model, 707 of the other 711 laws of the main repository's list fail in that model at explicit
elements, so the law does not imply them (2,828 certificates in
`results/refutations_term_models.json`, recomputed by plain Python in `check_refutations.py`,
mutation-tested, each also checked read backwards in the mirror model). The other 4 per law are
the law itself with letters made equal, so they are implied. Label `z3-only`, because that the
model satisfies its law is checked on all terms only by z3. This is implication over all
structures; for finite structures these laws (by the hand argument below) imply every law.
The 712 law texts and ids in that file are the main repository's: each text equals the main
repository's text for its id and reads back to its stored term tree (step 12, `check_copied_laws.py`,
which needs the main repository next to this one).

**Mirror pairs** (noticed in step 07, checked by machine in step 09): reading every product `a*b`
as `b*a` turns a model of one law into a model of its mirror law. `f(x*(y*z)) = y` and
`f((x*y)*z) = y` are mirrors, so are `x*(y*f(z)) = y` and `(f(x)*y)*z = y`, and `f(x)*(y*z) = y`
and `(x*y)*f(z) = y`; the two laws with 4-element models are their own mirrors. `mirror_pairs.py`
confirms these pairs from the law texts, checks the transposed 4-element tables by plain
evaluation, and checks the four mirrored infinite models on all terms with z3 (`z3-only`). The
general rule "a law and its mirror have the same answer" is still a hand argument (short induction
on terms). The pairs were worked out independently here, which gives a second route to each result.
The mirror of `((x*y)*z)*x = w` is `x*(y*(z*x)) = w`; it is not among the nine because z3 proved its
collapse in the main repository (three re-runs of that query in step 09 agree), while it gave up on
`((x*y)*z)*x = w`. z3 is not symmetric under mirroring.

### Leads from hand analysis (NOT machine-proven): candidate Austin laws

Vocabulary (source re-read in step 13): the ETP blueprint (`blueprint/src/chapter/infinite_models.tex`,
read in a clone at commit `dbc9a2b`, 2026-11-19) defines: "An *Austin law* is a law which admits
infinite models, but no nontrivial finite models". That definition is for magmas (one operation
`*`); the ETP's published report (arXiv 2512.07087v2) does not use the term. Carrying it over to
our laws with `f` is our own step. Known magma examples: Austin (1965, order 9), Kisielewicz (1990,
order 6; 1997, order 5), and 10 laws of order 5 in the ETP blueprint, which also says "no law of
order four or less is an Austin law" (magmas only). With a unary operation, size 3 seems enough,
much as a short identity with a constant, `(ex)y = x` (Dudek; slides read only by a subagent in the
main repository), has only infinite nontrivial models. So the four laws below are **candidate
Austin laws in type (2,1)**. Whether Kisielewicz's papers define the term for all types of algebra
is unknown (not read). We found nothing about the first two specific laws; no search was done for
the third, `(f(x)*y)*z = y`, or the fourth, `f((x*y)*z) = y`.
The arguments for the first two were re-read step by step on 2026-11-22 (second reading, still not
a human reviewer, not Lean); the third and fourth have had one reading each.

For `f(x*(y*z)) = y`, `x*(y*f(z)) = y`, `(f(x)*y)*z = y` (step 06) and `f((x*y)*z) = y` (step 07)
I think the answer is: **no finite structure with 2 or
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
then `p(y) = p^-1(f(z))` for all y, impossible for n at least 2. For `(f(x)*y)*z = y`: `f(x)*y`
determines `y`, so `y -> c*y` (with `c = f(a)`) is a bijection, so `u*z` does not depend on `z` for
any `u`, in particular `c*z`, which contradicts injectivity for n at least 2. For `f((x*y)*z) = y`
(the mirror of the first): `x*y` determines `y`, so `x*y = p(y)` for all `x`, and then
`f(p(z)) = y` for every `y`, impossible for n at least 2. z3 agrees for sizes 2 to 6.

Infinite part: models built by formula, sample-checked by `infinite_models.py`, and checked on all
terms by z3 in `term_models_z3.py` (z3's algebraic datatypes are exactly the formal terms; `z3-only`).
- `f(x*(y*z)) = y`: elements are nested pairs, `x*y` is the formal pair, `f` of a formal pair
  `(x, (y, z))` returns `y`, `f` of anything else returns it unchanged. The law holds by
  construction. Checked on all 17,576 triples from 26 elements, 0 failures.
- `x*(y*f(z)) = y`: `f(t)` is the formal term, `x*w` returns `y` when `w` is the formal pair
  `(y, f(z))`, otherwise the formal pair `(x, w)`. The law holds by construction. Checked on
  300,000 random triples from 144 elements, 0 failures.
- `(f(x)*y)*z = y`: `f(t)` is the formal term, `u*z` returns `y` when `u` is the formal pair
  `(f(t), y)`, otherwise the formal pair `(u, z)`. The law holds by construction. Checked on
  300,000 random triples from 144 elements, 0 failures.
- `f((x*y)*z) = y`: the mirror of the first model. `x*y` is the formal pair, `f` of a formal pair
  `((x, y), z)` returns `y`, `f` of anything else returns it unchanged. The law holds by
  construction. Checked on all 17,576 triples from 26 elements, 0 failures.

Status of the four leads: finite part `hand-argument`; infinite part `z3-only` on all terms plus a
plain-code sample check. Not checked by anyone else, not Lean, not literature-checked. The counting
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

Checked by: Claude reading it, z3 on each lemma (`lemma_chain_f_x_yz.py`), and since step 08 the
derivation checker `check_derivation.py` on the 11 single steps in `results/collapse_fx_yz.json`
(rejects 34 of 34 corrupted copies). Not checked by a human mathematician, a second independent
proof checker, or Lean. Literature (step 14, shallow search): nothing found about this law; its
magma special cases (`f(x)` replaced by `x`, `x*x`, `x*(x*x)`, `(x*x)*x`) are ETP Equations 15, 178,
1933, 2136, all recorded by the ETP as forcing one element, which agrees with the collapse but does
not prove it (`python etp_specializations.py`, needs a clone of the ETP). A first attempt at step 4 without the instance in step 2 was too weak: z3 returned
`unknown`, because my sketch had skipped the instantiation.

## Hand proof that `(x*y)*f(z) = y` collapses

Call the law (L). Plain English: multiplying any product `x*y` on the right by any `f(z)` gives
back `y`.

1. (L) at `x:=a, y:=b, z:=c`: `(a*b)*f(c) = b`.
2. (L) at `x:=a*b, y:=f(c), z:=d`: `((a*b)*f(c))*f(d) = f(c)`. By step 1 the left side is
   `b*f(d)`, so `b*f(d) = f(c)` for all `b`, `c`, `d`.
3. (L) at `x:=a, y:=b, z:=d`: `(a*b)*f(d) = b`. Step 2 with `b:=a*b` says the same left side is
   `f(c)`. So `b = f(c)` for all `b`, `c`.
4. Any two elements equal `f(c)`, so they are equal.

Checked by: the derivation checker `check_derivation.py` (written in this repository, plain
Python, rejects 37 of 37 corrupted copies) and z3 on each lemma (`lemma_chain_xy_fz.py`). Not
checked by a human, Lean, or another prover. Literature (step 14, shallow search: 6 web and 4
GitHub queries, no paper database): nothing found about this law; its magma special cases are ETP
Equations 30, 174, 1508, 1711 (`f(z)` replaced by `z`, `z*z`, `z*(z*z)`, `(z*z)*z`), all recorded
by the ETP as forcing one element. That agrees with the collapse but does not prove it, and "not
found" does not mean new. Details in `steps/05-collapse-xy-fz.md`.

## Steps (granular record)

`steps/`:
1. `01-find-the-laws.md`
2. `02-search-larger-models.md`
3. `03-hand-proof-f-x-yz.md`
4. `04-etp-and-the-three-f-free-laws.md`
5. `05-collapse-xy-fz.md`
6. `06-f-x-y-z-infinite-model.md`
7. `07-f-xy-z-infinite-model.md`
8. `08-collapse-fx-yz-derivation.md`
9. `09-mirror-pairs-by-machine.md`
10. `10-mirror-collapse-proofs.md`
11. `11-refutations-from-infinite-models.md`
12. `12-copied-law-texts.md`
13. `13-source-of-austin-law.md`
14. `14-literature-collapse-xy-fz.md`

## Files

- `zero_model_laws.py` searches for models of size 4 to 6. Output: `results/zero_model_laws.json`
  (the two models found are stored there as tables).
- `lemma_chain_f_x_yz.py` z3 check of the hand proof for `f(x)*(y*z) = y`.
- `lemma_chain_xy_fz.py` z3 check of the hand proof for `(x*y)*f(z) = y`.
- `infinite_models.py` sample check of the four infinite models (plain Python), `--selftest`.
- `term_models_z3.py` z3 check of the four infinite models on all terms, `--selftest`.
- `mirror_pairs.py` mirror pairs of the nine laws and the mirrored models (plain Python and z3),
  `--selftest`, and `--laws-list PATH` for the main repository's law list.
- `mirror_derivation.py` reads a stored collapse proof backwards to get a proof of the mirror law
  (`results/*_by_mirror.json`), `--check`, `--selftest`; its output is checked by `check_derivation.py`.
- `check_derivation.py` plain-Python checker of a stored step-by-step collapse proof
  (`results/collapse_xy_fz.json`, `results/collapse_fx_yz.json`), with `--selftest` (corrupted
  copies must be rejected).
- `refute_by_term_models.py` searches the four infinite models for elements where each law of the
  main repository's list fails (plain search, then z3). Output: `results/refutations_term_models.json`.
- `check_refutations.py` plain-Python checker of those certificates (own copy of the models, laws
  read from their texts, mirror cross-check), with `--selftest`.
- `check_copied_laws.py` checks that the law ids and texts in that results file are the main
  repository's and read back to its term trees, with `--selftest`. Needs the main repository.
- `etp_specializations.py` looks up the magma special cases of the two collapsing laws in the
  ETP data and checks that the ETP records each as forcing one element, with `--selftest`. Needs a
  clone of the ETP; not in CI.
- Depends on the engine in `src/` of [eq-unary-magma-laws](https://github.com/Math-Problem-Solving-Using-AI/eq-unary-magma-laws) (clone it next to this repository) and its generated data.

## Reproduce

Self-contained checks (CI runs them on every push):

```
pip install -r requirements.txt
python verify_models.py results/zero_model_laws.json            # the two structures, independent evaluator
python verify_models.py --selftest results/zero_model_laws.json # corrupted input must fail
python infinite_models.py                                       # sample check of the infinite constructions
python infinite_models.py --selftest                            # corrupted models must fail
python term_models_z3.py                                        # z3 on all terms of the infinite constructions
python term_models_z3.py --selftest                             # corrupted models must fail
python check_derivation.py results/collapse_xy_fz.json            # step-by-step collapse proof, no solver
python check_derivation.py --selftest results/collapse_xy_fz.json # corrupted proofs must be rejected
python check_derivation.py results/collapse_fx_yz.json            # the same for f(x)*(y*z) = y
python check_derivation.py --selftest results/collapse_fx_yz.json
python mirror_derivation.py --check                              # mirrored proofs match a fresh run
python mirror_derivation.py --selftest                           # broken mirrors must be rejected
python check_derivation.py results/collapse_fx_yz_by_mirror.json results/collapse_xy_fz_by_mirror.json
python check_derivation.py --selftest results/collapse_fx_yz_by_mirror.json results/collapse_xy_fz_by_mirror.json
python mirror_pairs.py                                           # mirror pairs and mirrored models
python mirror_pairs.py --selftest                                # corrupted mirrors must fail
python check_refutations.py results/refutations_term_models.json            # 2,828 non-implications
python check_refutations.py --selftest results/refutations_term_models.json # corrupted input must fail
python lemma_chain_xy_fz.py                                      # z3 on the second hand proof
python lemma_chain_f_x_yz.py                                    # z3 on the hand proof (results vary between runs)
```

Regenerating `results/zero_model_laws.json` needs the engine and generated data of
[eq-unary-magma-laws](https://github.com/Math-Problem-Solving-Using-AI/eq-unary-magma-laws). Clone it next to this repository, reproduce its steps, then:

```
P=../eq-unary-magma-laws
python zero_model_laws.py $P/data/laws_3.json $P/data/o3 6 15000     # or set EQ_ENGINE to its src/
```

The copied law texts are checked against the main repository's term trees (not in CI, it needs
that repository):

```
python check_copied_laws.py results/refutations_term_models.json            # 2,848 references, 712 ids
python check_copied_laws.py --selftest results/refutations_term_models.json # corrupted input must fail
```

The magma special cases of the two collapses are looked up in the ETP data (not in CI, it needs a
clone of `github.com/teorth/equational_theories` at `../_external/equational_theories`):

```
python etp_specializations.py              # 8 special cases, each an ETP equation implying x = y
python etp_specializations.py --selftest   # corrupted input must fail
```

## Contributing

Open an issue with a reference if you know existing results. Work items are in [`STATE.md`](STATE.md),
protocol in [`LOOP.md`](LOOP.md). Every claim keeps the label it earned.
