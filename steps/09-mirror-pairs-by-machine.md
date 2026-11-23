# 09. The mirror pairs, checked by machine

- Date: 2026-11-22
- Status label: the pairing of the nine laws: checked by our own plain-Python code (a statement
  about the law texts, nothing to prove beyond that). The mirrored 4-element models:
  `model-verified` (plain evaluation of every assignment). The mirrored infinite models: `z3-only`
  (all terms). The general rule "a structure satisfies a law exactly when its mirror satisfies the
  mirror law": still a `hand-argument` (short, by induction on terms; not machine-proven).
  Why `x*(y*(z*x)) = w` is not among the nine: z3 proves it collapses (`z3-only`, three runs of
  the main repository's own query), and a two-line hand argument agrees.
- Commit(s): see `git log -- mirror_pairs.py steps/09-mirror-pairs-by-machine.md`

## In plain words

1. **The question.** A *magma* here is a set with two operations: `*`, which takes two elements and
   gives one, and `f`, which takes one element and gives one. A *law* is a rule such as
   `f(x*(y*z)) = y` that must hold for every choice of the letters. A structure that obeys the law
   is a *model* of it. The *mirror* of a law is the law you get by reading every product backwards:
   `a*b` becomes `b*a`, everywhere, also inside brackets. Step 07 noticed, by hand, that the nine
   laws of this repository come in mirror pairs, and that a law and its mirror always have the same
   answer. The question for this step: is that pairing right, checked by a program, and do the
   models found earlier really turn into models of the mirror laws? A second question from the
   queue: one law, `((x*y)*z)*x = w`, has a mirror `x*(y*(z*x)) = w` that is not among the nine.
   Why not?

2. **What was done, in order.**
   1. **Wrote `mirror_pairs.py`.** For each of the nine laws it builds the mirror law, renames the
      letters in the order they first appear (so that `f((z*y)*x) = y` and `f((x*y)*z) = y` count
      as the same law), and looks the result up among the nine. This is needed because by eye it is
      easy to mix up which letter goes where.
   2. **Mirrored the two 4-element models.** The mirror of a structure is the same set with the
      same `f`, but the new product of `x` and `y` is the old product of `y` and `x`. For a table
      this means swapping rows and columns (the *transpose*). The script checks the transposed
      tables against the partner law on every choice of letters.
   3. **Mirrored the four infinite models.** These are the structures of steps 03, 06 and 07 whose
      elements are formal expressions. The script asks the solver z3 (an automatic prover) whether
      the mirrored structure breaks the partner law for any expressions at all. The partner law is
      read from its text, not written out by hand, so a typo in a hand-written version cannot hide
      a mistake.
   4. **Checked that the script can say no** (a *mutation test*): 9 deliberately broken versions,
      for example a "mirror" that reverses only the outermost product, a lookup that forgets to
      rename letters, a table with one changed entry, a model that is not mirrored. All 9 were
      rejected, and I printed each rejection to see it was rejected for the intended reason. A
      damaged copy of the script (one wrong pair) made it exit with code 1, so the automatic check
      on every push (CI) would fail.
   5. **Looked up the missing mirror in the main repository's data** (read only). Its list of 712
      laws contains `x*(y*(z*x)) = w`, and its table of small models shows that this law has no model
      with 2 or 3 elements, just like its mirror. The nine laws are the ones of that kind for which
      z3 could *not* prove a collapse (step 04 of the main repository). I re-ran the main
      repository's own z3 query three times with its 5-second limit: z3 proved the collapse of
      `x*(y*(z*x)) = w` every time, and gave up ("unknown") on `((x*y)*z)*x = w` every time. So the
      mirror was left out because z3 happened to succeed on it, not because it behaves differently.
   6. **Checked the main repository's whole list** with the new script: all 712 laws have their
      mirror in the list (54 are their own mirror), and the 216 laws with no model of size 2 or 3
      are also closed under mirroring.

3. **A small example.** Take the 2-element set `{0, 1}` and the product "always give the left
   element": `0*0 = 0`, `0*1 = 0`, `1*0 = 1`, `1*1 = 1`. It obeys the law `x*y = x`. It breaks the
   law `x*y = y`, because `0*1 = 0`, not `1`. Now transpose the table (swap rows and columns):
   `0*0 = 0`, `0*1 = 1`, `1*0 = 0`, `1*1 = 1`, "always give the right element". It obeys
   `x*y = y`, which is the mirror of `x*y = x`, and breaks `x*y = x`. (These two laws are not among
   the nine, which have no 2-element models at all; they only show the idea.) For the nine laws the
   script found the pairs `f(x*(y*z)) = y` with `f((x*y)*z) = y`, `x*(y*f(z)) = y` with
   `(f(x)*y)*z = y`, `f(x)*(y*z) = y` with `(x*y)*f(z) = y`; the two laws with 4-element models are
   their own mirrors; and `((x*y)*z)*x = w` has no partner among the nine.

4. **What it means and what it does not mean.** It means the pairs stated in step 07 are right,
   and that each infinite model, read backwards, is a model of the partner law (z3 on all
   expressions, so `z3-only`), and each 4-element table, transposed, is a model of the partner law
   (checked by plain evaluation). It explains why `x*(y*(z*x)) = w` is not on the list: z3 settled
   it. It does **not** prove the general rule "a law and its mirror have the same answer" by
   machine: that rule is a short hand argument (evaluating an expression in the mirrored structure
   gives the same element as evaluating the mirrored expression in the original one), not checked
   by Lean or a second tool. It does not raise the label of any of the nine results: a z3 answer
   stays z3-only, a hand argument stays a hand argument. And "z3 proved the collapse of
   `x*(y*(z*x)) = w`" is a z3-only fact, which the two-line hand argument in "Output" agrees with.

5. **How to re-check it.** From the repository root:
   ```
   python mirror_pairs.py
   ```
   expected: nine lines in Part 1 ending in `ok`, two lines in Part 2 ending in `ok`, four lines in
   Part 3 with `unsat` twice each, then `ALL PASS`.
   ```
   python mirror_pairs.py --selftest
   ```
   expected: nine `mutation ...: rejected` lines, `selftest: 9 of 9 corrupted checks rejected`,
   `ALL PASS`.
   With the main repository cloned next to this one:
   ```
   python mirror_pairs.py --laws-list ../eq-unary-magma-laws/data/laws_3.json
   ```
   expected: `712 laws, 712 different normal forms, 54 are their own mirror, 712 have their mirror
   in the list, 0 do not`.

## Goal

Queue item 1: check the mirror pairs by machine (pairing, mirrored infinite models with z3 on all
terms), and find out from the main repository's data why `x*(y*(z*x)) = w` is not among the nine.

## Command(s)

```
python mirror_pairs.py
python mirror_pairs.py --selftest
python mirror_pairs.py --laws-list ../eq-unary-magma-laws/data/laws_3.json
```
plus all gates of `LOOP.md`. Not committed, run in a terminal:
- the mutation checks again with `verbose=True`, to read why each was rejected;
- a scratch copy of `mirror_pairs.py` with one wrong entry in `EXPECTED`, to check the exit code;
- the main repository's own collapse query, three times, read only, from its `src/` folder with
  `python -B` so that nothing is written there:
  `prove.task_collapse((i, prove.tuplify(d[i]['law']), 5000))` for the entries 618
  (`x*(y*(z*x)) = w`) and 109 (`((x*y)*z)*x = w`) of `data/laws_3.json`;
- a short script reading `data/o3_sat.npy` of the main repository to list the 216 laws with no
  model of size 2 or 3 and look up the mirror of each of the nine among them.

## Inputs

- `results/zero_model_laws.json` (the nine laws and the two 4-element tables).
- `term_models_z3.py` (the four infinite term models, imported unchanged) and `check_derivation.py`
  (its parser and printer, imported unchanged).
- Main repository eq-unary-magma-laws at commit `4e95da1`: `data/laws_3.json`, `data/o3_sat.npy`,
  `src/prove.py`, `steps/04-collapse-laws.md`. Read only.
- Python 3.12.10, z3-solver 5.4.1.

## Output

- New `mirror_pairs.py`; `.github/workflows/verify.yml` and `LOOP.md` run it and its selftest.
- Part 1: all nine laws `ok`. Pairs: `f(x*(y*z)) = y` / `f((x*y)*z) = y`, `x*(y*f(z)) = y` /
  `(f(x)*y)*z = y`, `f(x)*(y*z) = y` / `(x*y)*f(z) = y`; `(x*y)*(y*x) = y` and `(x*y)*(y*z) = y`
  are their own mirrors; `((x*y)*z)*x = w` (mirror `x*(z*(y*x)) = w`, renamed `x*(y*(z*x)) = w`)
  has no partner among the nine.
- Part 2: both transposed tables differ from the original tables and satisfy the (same, self-mirror)
  law.
- Part 3: each of the four term models satisfies its own law read from text (`unsat`) and, mirrored,
  the partner law (`unsat`).
- Selftest: `9 of 9 corrupted checks rejected`, each for the intended reason (read one by one).
  Damaged copy: Part 1 printed `FAILED` for the two laws of the changed pair, exit code 1 (Part 3
  then stopped with a `KeyError` on the missing pair, which also gives exit code 1).
- Main list: `712 laws, 712 different normal forms, 54 are their own mirror, 712 have their mirror
  in the list, 0 do not`. The 216 laws with no model of size 2 or 3: all 216 have their mirror among
  the 216.
- z3 collapse query of the main repository, 5 s, three runs: `x*(y*(z*x)) = w` code 1 (`unsat`,
  collapse proved) in all three; `((x*y)*z)*x = w` code 0 (`unknown`) in all three.
- Hand argument for `x*(y*(z*x)) = w`, the mirror of step 04's: `w` occurs only on the right, so
  put `x = y = z = a`; then `a*(a*(a*a)) = w` for every `w`, so all elements equal one element.

## Checks done (and what each one can and cannot catch)

- Part 1 (pairing): catches a wrong pair in the README, a law with two partners, and a pairing that
  only works for some renaming. It relies on the parser of `check_derivation.py`; a parser bug that
  changes laws consistently would not be caught, but the law texts round-trip in that checker.
- Part 2 (tables): catches a transposed table that breaks the partner law. Plain evaluation of all
  assignments, no solver.
- Part 3 (term models): catches a mirrored model that breaks the partner law for some terms. Rests
  on z3's datatype reasoning (`z3-only`), with the accessor guards of `term_models_z3.py`.
- Involution check: mirroring each law twice gives the law back.
- Mutation test with reasons printed, and the exit code with a damaged copy: catches a script that
  cannot fail or whose failure would not fail CI. Covers only the 9 kinds of damage listed.
- Comparison with the main repository's data: the 216 laws with no small model are closed under
  mirroring, which is what the mirror rule predicts (a transposed small model would be a small model
  of the mirror law). A mismatch would have pointed to a bug in either repository; there was none.

## NOT verified

- The general mirror rule (a structure satisfies a law exactly when its mirror structure satisfies
  the mirror law) is a hand argument by induction on terms. Not machine-proven, not in Lean.
- Why `x*(y*(z*x)) = w` was left out is inferred from the main repository's step 04 (its list of 9
  unresolved laws) and from re-running its z3 query in this run. The file with its stored per-law
  collapse flags, `data/o3_collapse.npy`, is not in that repository, so it was not read.
- The collapse of `x*(y*(z*x)) = w` rests on z3 and a two-line hand argument; no derivation file was
  written for it (it is not one of the nine, so `check_derivation.py` would refuse it).
- The mirror route as a second proof was not used: mirroring the stored derivation for
  `(x*y)*f(z) = y` into one for `f(x)*(y*z) = y` (and back) and checking it is left as a queue item.
- The parser and printer used are those of `check_derivation.py`, written in this repository and not
  reviewed by anyone else.
- No literature check about mirror symmetry for type (2,1) laws (the idea is standard for magmas, as
  "dual" or "opposite" magmas; not checked against a source in this run, so not cited).

## Surprises, errors, dead ends

- z3 is not symmetric under mirroring: with the same query and time limit it proves the collapse of
  `x*(y*(z*x)) = w` every time and gives up on its mirror `((x*y)*z)*x = w` every time. That is why
  `((x*y)*z)*x = w` reached the list of nine at all. Lesson in `docs/LOG.md`: when a solver settles
  one law of a mirror pair, use it for the other.
- A planned mutation "normal form that tries only one side of the equation" was not caught on the
  nine laws, because all nine are written as expression = letter. It only matters for lists that
  write laws both ways (the `--laws-list` check). Dropped from the selftest, not counted.
- The first `diff` of the damaged scratch copy showed every line as changed: the file has Windows
  line endings and the copy made with `sed` did not keep them. Only one line was really different.

## Next

Queue: mirror the two stored collapse derivations and check the mirrored proofs with
`check_derivation.py`. The Lean review of the four finite-versus-general leads waits for the owner:
Lean is not installed on this machine (see Blocked in `STATE.md`).
