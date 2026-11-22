# 12. The copied law texts match the main repository's term trees

- Date: 2026-11-22
- Status label: statement fidelity (S1 of `docs/shared/VERIFICATION_PROTOCOL.md`) of the law texts
  in `results/refutations_term_models.json`, checked by two parsers: the main repository's
  `src/check_laws_text.py` (its own list) and the new `check_copied_laws.py` here (our copies).
  Both are plain Python and mutation-tested; neither is reviewed. The labels of the 2,828
  non-implications of step 11 do not change (`z3-only`).
- Commit(s): see `git log -- check_copied_laws.py steps/12-copied-law-texts.md`

## In plain words

1. **The question.** A *law* is a rule such as `f(x*(y*z)) = y` that must hold for every choice of
   the letters; here `*` combines two elements and `f` changes one element. The main repository
   (`eq-unary-magma-laws`) keeps a list of 712 short laws, each with a number (*id*), a text, and
   the same law stored as a *term tree* (a nested list a program reads, for example
   `[["f", ["m", ["v",0], ["m", ["v",1], ["v",2]]]], ["v",1]]`, where `m` means `*` and `v,0` is
   the first letter `x`). In step 11 the search program read the laws from the trees, but the
   results file keeps only ids and texts, and the checking program reads the laws from the texts.
   Question: are the texts in our results file really the main repository's laws, so that the
   search and the checker talked about the same laws?

2. **What was done, in order.**
   1. **Ran the main repository's own check** (`src/check_laws_text.py`, run with `python -B` so it
      writes nothing there). It reads every text of its list with its own small parser and
      compares with the stored tree: "712 laws checked, 0 mismatches". To be sure this check can
      fail, ran it on a corrupted copy of the list (one text changed, kept in a temporary folder):
      it printed `MISMATCH 450 f(x*(y*z)) = z` and exited with code 1.
   2. **Wrote `check_copied_laws.py` here.** For every law our results file names (2,848
      references: the 2,828 certificates, the 16 laws not refuted, and the four models' own laws
      with the ids recorded in step 11), it checks that the id exists in the main list and always
      has the same text in our file, that the text is exactly the main list's text, and that the
      text, read by the very parser our checker `check_refutations.py` uses, gives exactly the main
      list's tree. Finally it checks that the ids used are exactly 1 to 712.
   3. **Tested it by breaking things** (a *mutation test*): 13 deliberately corrupted inputs (texts
      with letters swapped, sides swapped, brackets moved, ids shifted or out of range, a changed
      tree in the main list, a missing or repeated law, the letter order changed). All 13 rejected;
      the reason printed for each was read. A corrupted results file and a corrupted main list on
      disk both made it exit with code 1.
   4. **Added it to the LOOP gates**, not to CI, because CI does not have the main repository.

3. **A small example.** Law 450 in the main list has the text `f(x*(y*z)) = y` and the tree
   `[["f", ["m", ["v",0], ["m", ["v",1], ["v",2]]]], ["v",1]]`. Letter 0 is `x`, 1 is `y`, 2 is `z`.
   So the tree says: `f` of (`x` times (`y` times `z`)) equals `y`. Our parser reads the text into
   the same shape, so they agree. If the text had been copied as `f((x*y)*z) = y` (brackets moved,
   which is law 336, a different law), the check would stop with "carries two texts".

4. **What it means and what it does NOT mean.**
   - It means: the search (which read trees) and the checker (which read texts) of step 11 worked
     on the same 712 laws, with the same ids as the main repository. A misreading of a law text
     cannot be hiding behind the 2,828 certificates.
   - It does NOT check that the main repository's list is the right list of all short laws (its
     own counting check, `src/check_laws_count.py`, was not re-run here).
   - It does NOT make any non-implication stronger than `z3-only`: the infinite models are still
     checked on all terms only by z3.
   - The letter order `xyzwuvabcdefgh` is copied from the main repository's `src/laws.py` (line 16,
     read today); if that file changes, the check must be re-run.
   - It checks the main repository as it is on this machine today (commit `4e95da1`, file
     `data/laws_3.json` with SHA-256 `f209c037e305090b6e18ce91a792df58db79a4b7a5450029522b58690dda4db0`).

5. **How a reader can re-check it.** With the main repository cloned next to this one:
   ```
   python check_copied_laws.py results/refutations_term_models.json
   # "2848 law references in the results file, 712 different ids", ..., ALL PASS
   python check_copied_laws.py --selftest results/refutations_term_models.json
   # 13 lines "mutation ...: rejected (...)", "selftest: 13 of 13 corrupted inputs rejected", ALL PASS
   python -B ../eq-unary-magma-laws/src/check_laws_text.py ../eq-unary-magma-laws/data/laws_3.json
   # "712 laws checked, 0 mismatches"
   ```

## Goal

Queue item 2: confirm that the 712 law texts and ids copied into
`results/refutations_term_models.json` match the main repository's term trees.

## Command(s)

```
python -B ../eq-unary-magma-laws/src/check_laws_text.py ../eq-unary-magma-laws/data/laws_3.json
python check_copied_laws.py results/refutations_term_models.json
python check_copied_laws.py --selftest results/refutations_term_models.json
```
plus all LOOP gates (22 commands, all exit 0).

## Inputs

`../eq-unary-magma-laws/data/laws_3.json` (read only; main repository commit `4e95da1`, working tree
clean, SHA-256 above), `results/refutations_term_models.json` (unchanged), the parser in
`check_derivation.py` (unchanged). Python 3.12.10. No z3.

## Output

- `check_copied_laws.py` (new), two new LOOP gate commands.
- Main repository check: 712 laws, 0 mismatches. Ours: 2,848 references, 712 ids, all equal to the
  main list's texts and trees. No results file changed.

## Checks done (and what each one can and cannot catch)

- Main repository's round trip (text to tree, its own parser) on its list. Catches a text that does
  not match its tree in the main list. Mutation (one changed text) caught, exit 1.
- Ours: id exists, same text everywhere in our file, equal to the main text, read back by
  `check_refutations.py`'s parser equals the main tree, ids are exactly 1..712. Catches a wrong
  copy, a shifted id, a lost or extra law, and a disagreement between the two readings used in
  step 11. Cannot catch an error shared by both parsers in the same direction (for example, if
  both read `x*y*z` the same wrong way; such texts do not occur, every product is bracketed).
- Mutation test: 13 of 13 rejected. Some were caught by the "same text everywhere" guard before
  the main-text comparison (each id appears in all four models); a mutation that changes every copy
  of one id was added so the main-text comparison itself is exercised, and it was.

## NOT verified

- The main repository's enumeration (that its 712 laws are all and only the short laws up to
  renaming) was not re-checked here (`src/check_laws_count.py` not run).
- `check_copied_laws.py` is unreviewed and written by the same author as the results file.
- The two parsers are separate code but follow the same grammar; they are not independent thinking.
- Not in CI: it needs the main repository, which CI does not clone.
- The letter order and the ids of the four model laws (450, 639, 135, 336) are typed into the
  script from the main repository and step 11; the run confirms they agree with the main list
  today, nothing more.
- Nothing here touches the `z3-only` part of step 11 or the finite hand argument.

## Surprises, errors, dead ends

- None in the result. In the mutation test, several mutations were caught by an earlier guard
  ("carries two texts") rather than the check they aimed at, because each id appears in all four
  models; one more mutation was added so that the main-text comparison is also exercised.
- A first draft of the selftest caught any `KeyError`/`IndexError`/`StopIteration` as "rejected".
  That would have counted a broken mutation as a success; changed to count only the checker's own
  failure (`Bad`).

## Next

Queue item 3 (literature check). The Lean items wait for the owner.
