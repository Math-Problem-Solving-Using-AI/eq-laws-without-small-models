# 10. A second proof of each collapse, by reading the other proof backwards

- Date: 2026-11-22
- Status label: unchanged for both laws: `z3-only` plus our own checker. Each of the two
  collapsing laws, `f(x)*(y*z) = y` and `(x*y)*f(z) = y`, now has two different stored
  derivations, both accepted by `check_derivation.py`. The checker is the same program for all four
  derivations and was written in this repository (step 05), so this is not a second independent
  checker and not `independent-prover`.
- Commit(s): see `git log -- mirror_derivation.py steps/10-mirror-collapse-proofs.md`

## In plain words

1. **The question.** A *magma* here is a set with two operations: `*`, which takes two elements
   and gives one, and `f`, which takes one element and gives one. A *law* is a rule such as
   `f(x)*(y*z) = y` that must hold for every choice of the letters. A law *collapses* when it can
   only hold in a set with a single element: from the law alone one can derive `b = e` for any two
   letters `b` and `e`. Two of our nine laws collapse, and each has a stored *derivation*: a list of
   small steps, each one an instance of the law or a basic rule of equality (turn an equation
   around, chain two equations, replace a piece by something equal to it). The program
   `check_derivation.py` checks every step. The *mirror* of a law reads every product backwards
   (`a*b` becomes `b*a`), and the two collapsing laws are mirrors of each other (step 09). The
   question: if we read one stored derivation backwards, do we get a correct derivation for the
   other law? That would give each law a second, different proof.

2. **What was done, in order.**
   1. **Wrote `mirror_derivation.py`.** It takes a stored derivation and reads every term in it
      backwards: every equation, every term that is plugged in for a letter, every term that is
      rewritten. Two details needed care. A rewrite step says where in a term the replacement
      happens, as a *path* (1 = left factor or the inside of `f`, 2 = right factor); reading
      backwards swaps left and right, so 1 and 2 are swapped wherever the path passes through a
      product, but not where it passes through `f`. And the mirror of `(x*y)*f(z) = y` is
      `f(z)*(y*x) = y`, which is the stored law `f(x)*(y*z) = y` with the letters `x` and `z`
      exchanged; so in steps that use the law, the letters are renamed to match the stored text.
      The script finds that renaming by matching the two laws symbol by symbol and stops with an
      error if they do not match.
   2. **Did not trust the script.** Its output goes to `check_derivation.py`, unchanged since step
      08, which checks every step from scratch. If the script had a bug, a step would not follow
      and the checker would say so.
   3. **Ran it on both stored proofs.** `results/collapse_xy_fz.json` (12 steps, a proof for
      `(x*y)*f(z) = y`) became `results/collapse_fx_yz_by_mirror.json`, a 12-step proof for
      `f(x)*(y*z) = y`. `results/collapse_fx_yz.json` (11 steps) became
      `results/collapse_xy_fz_by_mirror.json`, an 11-step proof for `(x*y)*f(z) = y`. The checker
      accepted both, and its own corruption test rejected 37 of 37 and 34 of 34 broken copies of
      them.
   4. **Checked that a wrong mirror is caught** (a *mutation test*). The script's `--selftest`
      builds the mirrored proofs with five deliberate mistakes (paths not swapped, letters not
      renamed, plugged-in terms not mirrored, rewritten terms not mirrored, equations not
      mirrored). The checker rejected all 10 (5 mistakes times 2 proofs), and the printed reasons
      show each was caught at the step the mistake touches. A sixth planned mistake, "do not mirror
      inside `f`", changed nothing, because in these proofs `f` only ever wraps a single letter; it
      was dropped (see Surprises).
   5. **Added a consistency check.** `--check` confirms that the stored mirrored files are exactly
      what the script writes now, and that reading a mirrored proof backwards once more gives back
      the original proof, step for step.
   6. **Added everything to CI and the LOOP gates.**

3. **A small example.** The first step of the proof for `(x*y)*f(z) = y` is the law with `a`, `b`,
   `c` plugged in: `(a*b)*f(c) = b`. Read backwards: `f(c)*(b*a) = b`. That is the law
   `f(x)*(y*z) = y` with `c` for `x`, `b` for `y` and `a` for `z`. So the mirrored step is again
   "the law with letters plugged in", only for the other law and with the letters in different
   places. A rewrite step in the original proof replaces the left factor (path `[1]`) of
   `((a*b)*f(c))*f(d)`. In the mirrored term `f(d)*(f(c)*(b*a))` the same piece is the right
   factor, so the path becomes `[2]`.

4. **What it means and what it does not mean.**
   - It means each collapsing law now has two different step-by-step proofs, both accepted by the
     checker. The new proof of `f(x)*(y*z) = y` follows another route than the old one (it first
     shows `f(d)*b = f(c)`, where the old one plugs a product `b*c` in for `y`).
   - The new proofs are checked directly, so they do not rely on the general mirror rule of step
     09 (which is still a hand argument). They are one more worked instance of that rule.
   - It does NOT add a new checker. All four proofs are checked by the same program, written in
     this repository and not reviewed by anyone else. A bug in that program could pass all four.
   - It does NOT make the collapses "proved" in the sense of the repository's labels: no Lean, no
     human review, no literature check. The label stays `z3-only` plus our own checker.
   - The mirrored proofs are not new ideas: each is the other law's proof read backwards.

5. **How a reader can re-check it.** From the repository root:
   ```
   python mirror_derivation.py --check      # ends with ALL PASS
   python mirror_derivation.py --selftest   # 10 lines "rejected (...)", 2 lines "noticed", ALL PASS
   python check_derivation.py results/collapse_fx_yz_by_mirror.json results/collapse_xy_fz_by_mirror.json
   # two lines "... COLLAPSE DERIVED", then ALL PASS
   python check_derivation.py --selftest results/collapse_fx_yz_by_mirror.json results/collapse_xy_fz_by_mirror.json
   # "37 of 37" and "34 of 34 corrupted copies rejected", ALL PASS
   ```
   `python mirror_derivation.py` (no option) rewrites the two mirrored files from the originals.

## Goal

Queue item 1: mirror the two stored collapse derivations into derivations of the partner laws and
check them with the unchanged `check_derivation.py`.

## Command(s)

```
python mirror_derivation.py
python mirror_derivation.py --check
python mirror_derivation.py --selftest
python check_derivation.py results/collapse_fx_yz_by_mirror.json results/collapse_xy_fz_by_mirror.json
python check_derivation.py --selftest results/collapse_fx_yz_by_mirror.json results/collapse_xy_fz_by_mirror.json
```
plus all LOOP gates.

## Inputs

`results/collapse_xy_fz.json`, `results/collapse_fx_yz.json` (unchanged), `results/zero_model_laws.json`
(law list, unchanged), `check_derivation.py` (unchanged). Python 3.12.10. These commands do not
use z3; the other gates ran with z3 5.4.1 (`z3.get_version_string()`).

## Output

- `mirror_derivation.py` (new).
- `results/collapse_fx_yz_by_mirror.json`: 12 steps, law `f(x)*(y*z) = y`, last step `b = e`.
- `results/collapse_xy_fz_by_mirror.json`: 11 steps, law `(x*y)*f(z) = y`, last step `b = e`.
- Law-variable renaming in both directions: `x -> z`, `y -> y`, `z -> x` (mirror-law letter to
  stored-law letter).
- CI and LOOP gates: six new commands. All 20 gate commands exit 0.

## Checks done (and what each one can and cannot catch)

- `check_derivation.py` on both new files: every step follows by its rule; catches any error of
  the mirror script that produces a wrong step. Cannot catch a bug in the checker itself.
- `check_derivation.py --selftest` on both new files: 37/37 and 34/34 corrupted copies rejected;
  shows the checker still says no on these inputs.
- `mirror_derivation.py --selftest`: 10/10 broken mirrors rejected by the checker, reasons printed
  and read (each at the first step the mistake touches); a changed stored file is noticed. Cannot
  catch mistakes the five mutations do not model.
- `mirror_derivation.py --check`: stored files equal a fresh run; mirroring twice is the identity on
  the steps. Catches hand edits and drift between script and data. Exit code 1 was observed once
  for real, when the comment wording changed before the files were regenerated.
- All earlier gates rerun, all pass.

## NOT verified

- The checker `check_derivation.py` has not been reviewed by anyone but its author session; all
  four collapse derivations depend on it.
- No Lean proof, no second prover, no human review of either collapse.
- The general mirror rule (a structure satisfies a law exactly when its mirror satisfies the mirror
  law) is still a hand argument; this step checks two instances at the level of derivations only.
- The mutation "do not mirror inside `f`" could not be tested on these proofs (no product inside
  `f` occurs), so a bug of that kind in `mirror_derivation.py` would go unnoticed on other proofs
  until the checker rejects the output.
- No literature check of either collapse (queue item 4).

## Surprises, errors, dead ends

- A planned mutation "terms inside `f` not mirrored" was not caught, because it was no mutation:
  in both proofs `f` only ever wraps a single letter, so the output was identical. Dropped, not
  counted, recorded in `docs/LOG.md`.
- A planned mutation "only the outermost product mirrored" was rejected by the script's own
  law-matching guard before the checker saw anything. It tested the guard, not the checker, so it
  was replaced by mutations that reach the checker (found by printing the reasons, the step 05
  lesson).
- The new proof of `f(x)*(y*z) = y` is a genuinely different route from the step 08 one, which
  the earlier hand work had not noticed.

## Next

Queue item 3 (use the infinite models to refute implications) is the first item that can move
without the owner; items 2 and 5 wait for Lean (Blocked).
