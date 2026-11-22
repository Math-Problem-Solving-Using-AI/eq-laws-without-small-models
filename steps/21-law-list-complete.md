# 21. The main repository's list of 712 short laws is complete and has no repeats

- Date: 2026-11-22
- Status label: statement fidelity (S1 of `docs/shared/VERIFICATION_PROTOCOL.md`) of the law list
  `data/laws_3.json` that steps 11 and 12 use. Checked by two plain-Python brute-force counts: the
  main repository's `src/check_laws_count.py` (which checks its generator, not the file) and the new
  `check_law_list.py` here (which checks the file). Both mutation-tested, neither reviewed. No
  mathematical label changes: the 2,828 non-implications of step 11 stay `z3-only`.
- Commit(s): see `git log -- check_law_list.py steps/21-law-list-complete.md`

## In plain words

1. **The question.** Our structures have two operations: `*`, which combines two elements into
   one, and `f`, which turns one element into another. A *law* is a rule such as `f(x)*y = x` that
   must hold for every choice of the letters. A *short law* here is one with 1 to 3 operation
   symbols in all (each `*` and each `f` counts one). Two laws count as the same when one becomes
   the other by renaming letters (`f(x) = y` and `f(y) = x`) or by swapping the two sides
   (`f(x) = y` and `y = f(x)`). The main repository (`eq-unary-magma-laws`) stores a list of 712
   short laws in the file `data/laws_3.json`. Steps 11 and 12 tested our four infinite structures
   against every law of that list. Question: is that list really every short law, with none
   missing and none listed twice?

2. **What was done, in order.**
   1. **Ran the main repository's own count check** (`src/check_laws_count.py 3`, with `python -B`
      so it writes nothing there; its working tree stayed clean). It builds every pair of terms by
      brute force and compares with the main repository's generator `laws.py`. Output: 7, 62 and
      643 laws with 1, 2 and 3 operations, 712 in all, "MATCH", exit code 0, in 0.6 seconds.
   2. **Read that check's code.** Two gaps showed up. (a) It never opens `data/laws_3.json`; it
      checks the program that wrote the file, not the file. (b) It puts the generator's laws into
      a dictionary keyed by their standard form before comparing, so a law listed twice would be
      counted once.
   3. **Tested that check by breaking copies of it** (a *mutation test*: a deliberately corrupted
      input; a working check must notice it). The copies sat in a scratch folder; the main
      repository was not touched. Three corrupted generators: one that keeps laws with equal sides
      (caught: "MISMATCH", exit 1), one that drops terms starting with `f` at 3 operations (caught,
      exit 1), and one that forgets that swapping sides gives the same law. The last one produces
      1,418 entries, each law about twice, and the check still printed "MATCH" with exit 0. So the
      main check cannot see repeats. That does not make the real list wrong; it means that check
      alone does not prove "no repeats".
   4. **Wrote `check_law_list.py` here**, which reads the file itself. It checks that the ids are
      exactly 1 to 712 in order; that each entry is a well-formed law with different sides, 1 to 3
      operations, and correct stored "order" and "vars" fields; that no two entries are the same
      law; and that the set of entries equals a brute-force list built here (every pair of terms
      with 1 to 3 operations over 5 letters). "Same law" is computed in two different ways (try all
      renamings of the letters, or rename letters by order of first appearance), and the run checks
      that the two ways agree on the brute-force list.
   5. **Mutation test of the new check**: 13 corrupted inputs (a law dropped, a renamed copy added,
      a side-swapped copy added, one law replaced by a copy of another, a law with equal sides, a
      law with 4 operations, a law with none, wrong "order" or "vars" field, a gap in the ids, an
      unknown operation, a brute force that forgets `f`, a "same law" test that forgets side
      swapping). All 13 rejected, each for the intended reason (printed and read). Two harmless
      changes (a law with its letters renamed, a law with its sides swapped) are accepted, as they
      must be. A corrupted copy of the file on disk (one law removed, ids renumbered) made the
      program exit with code 1.
   6. **Ran all 22 LOOP gates and the two new ones**: all 24 exit 0.

3. **A small example.** With 1 operation the brute force finds 7 classes, and the file has exactly
   these 7 entries (ids 1 to 7, printed from the file): `f(x) = x`, `f(x) = y`, `x*x = x`,
   `x*x = y`, `x*y = x`, `x*y = y`, `x*y = z`. (`x*y = x*y` is not a law here: equal sides. `x = y`
   is not short: 0 operations.) Take `f(x) = y`.
   Brute force also builds `f(y) = x`, `y = f(x)`, `f(z) = x` and so on. Renaming by first
   appearance turns `f(z) = x` into `f(x) = y`, and `y = f(x)` with sides swapped is again
   `f(x) = y`; so all of them fall into one class, and the file must hold exactly one of them. If a
   second entry `f(y) = x` were added, the check stops with "id 713 is the same law as id 2".

4. **What it means and what it does NOT mean.**
   - It means: the 712 laws that steps 11 and 12 used are every law with 1 to 3 operations, up to
     renaming and swapping sides, each exactly once, as the file stands today (main repository
     commit `4e95da1`, file SHA-256
     `f209c037e305090b6e18ce91a792df58db79a4b7a5450029522b58690dda4db0`, same as step 12). So "707 of
     711 targets refuted" in step 11 is out of the right set of targets.
   - It does NOT check anything about the four infinite models or the certificates (still
     `z3-only`), or the finite hand argument.
   - It does NOT mean the two brute-force checks are independent thinking: both use the same
     definition of "short law", written down from the main repository's `laws.py` docstring
     ("Laws are deduplicated up to variable renaming and swapping the two sides. Trivial laws
     (lhs == rhs) are dropped.") A different definition (for example, counting `x = y` as a law with
     0 operations) would give a different list. The main repository leaves out 0-operation laws;
     so does this check.
   - The weakness of the main repository's count check (blind to repeats) is reported for the owner
     under "For other repositories" in `docs/LOG.md`; nothing was changed there.

5. **How a reader can re-check it.** With the main repository cloned next to this one:
   ```
   python check_law_list.py
   # "brute force: 712 laws up to renaming and swapping (two keys agree)",
   # "file: 712 entries, each a different law, by order {1: 7, 2: 62, 3: 643}", ALL PASS, exit 0
   python check_law_list.py --selftest
   # 13 lines "mutation ...: rejected (...)", 2 lines "control ...: accepted",
   # "selftest: 13 of 13 corrupted inputs rejected, 2 of 2 harmless changes accepted", ALL PASS
   python -B ../eq-unary-magma-laws/src/check_laws_count.py 3
   # "brute force by order: {1: 7, 2: 62, 3: 643} total 712", "laws.py total 712", MATCH
   ```
   The first takes about 4 seconds, the selftest about 11.

## Goal

Queue item 2 (STATE.md before this run): re-run the main repository's count check on
`data/laws_3.json` and record whether its 712 laws are all and only the short laws (step 12, "NOT
verified"). Item 1 (Lean) is still blocked.

## Command(s)

```
python -B ../eq-unary-magma-laws/src/check_laws_count.py 3      # exit 0, 0.59 s (Measure-Command)
# mutation test of that check, on copies of check_laws_count.py and laws.py in a scratch folder,
# each change applied in Python with an assert that the replaced text occurs exactly once:
#   trivial: drop "if l == r: continue" in enumerate_laws     -> laws.py total 715, MISMATCH, exit 1
#   nof:     no ('f', s) shapes at 3 operations               -> only brute force 47, MISMATCH, exit 1
#   noswap:  key = a instead of min(a, b)                     -> MATCH, exit 0 (len(enumerate_laws(3)) = 1418)
#   clean copy                                                -> MATCH, exit 0
python check_law_list.py                                         # exit 0, 4.3 s
python check_law_list.py --selftest                              # exit 0, 11 s
python check_law_list.py <scratch copy with one law removed>     # "FAIL: 1 short laws missing", exit 1
```
Plus all 22 LOOP gates (all exit 0).

## Inputs

`../eq-unary-magma-laws/data/laws_3.json` and `src/check_laws_count.py`, `src/laws.py` (read only;
main repository commit `4e95da1`, working tree clean before and after; file SHA-256 above).
Python 3.12.10. No z3.

## Output

- `check_law_list.py` (new, plain Python, does not import the main repository's code), two new
  LOOP gate commands, README and llms.txt lines. No results or certificates changed.
- Numbers: 712 classes by brute force (7, 62, 643 by number of operations); the file has 712
  entries, all different, all short, none missing.

## Checks done (and what each one can and cannot catch)

- Main repository's count check: brute force against its generator. Catches a generator that
  misses or adds a class. Cannot catch repeats (shown by the `noswap` mutation) and does not read
  the stored file.
- `check_law_list.py`: catches a missing law, an extra non-short or trivial law, a repeat up to
  renaming or side swap, wrong order/vars fields, id gaps, malformed trees; the two "same law" keys
  must agree on all brute-force pairs, which catches an error in one of them (mutation: side swap
  forgotten in the second key gives 1,418 against 712 classes). Cannot catch an error in the
  definition of "short law" shared by both repositories.
- Mutation tests: 3 on copies of the main check (2 caught, 1 not, as reported), 13 on the new
  check (13 caught) plus 2 harmless changes accepted, plus one corrupted file on disk (exit 1).

## NOT verified

- `check_law_list.py` is unreviewed and written in the same session as this record.
- The definition of "short law" (1 to 3 operations, sides different, up to renaming and swapping)
  is taken from the main repository's docstring; whether it is the definition the main problem
  intends was not checked against any outside source.
- The two checks use similar algorithms (enumerate terms, canonical form); they agree, but they are
  not independent ideas. No third method (for example a counting formula) was used.
- The main repository's check was not changed and was not re-run with a fix; its blindness to
  repeats is only reported.
- The docstring of the main check says "3 takes about a minute"; it took 0.6 s here. Not
  investigated (perhaps written before an optimisation, perhaps for another machine).
- Not in CI: the check needs the main repository, which CI does not clone.
- Nothing here touches the `z3-only` part of step 11 or the finite hand argument.

## Surprises, errors, dead ends

- The main repository's count check accepts a generator that lists every law about twice (1,418
  entries): it removes repeats before comparing. Reported for the owner in `docs/LOG.md`.
- My first attempt at one scratch mutation used `sed` with a `\n` in the pattern; `sed` works line
  by line, so it changed nothing. It was redone in Python with an assert that the text occurs once
  (the lesson from step 19, applied here before any result was read).
- The main check ran in 0.6 s, not "about a minute" as its docstring says; re-measured with
  PowerShell's `Measure-Command` after Git Bash's `time` showed 0 user time, and the output was
  checked to be complete.

## Next

Queue: item 1 (Lean) and the Lean part of item 3 still wait for the owner; next free item is the
OpenAlex search for the two collapses.
