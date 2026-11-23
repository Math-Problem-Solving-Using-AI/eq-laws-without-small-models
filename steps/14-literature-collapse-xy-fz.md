# 14. Literature check: the collapse of `(x*y)*f(z) = y` and its mirror

- Date: 2026-11-22
- Status label: literature check (S5 of `docs/shared/VERIFICATION_PROTOCOL.md`), shallow: "not found
  in searches" for the two laws themselves; their magma special cases are `known` (ETP). No
  mathematical label changes: both collapses stay `z3-only` plus our own derivation checker.
- Commit(s): see `git log -- steps/14-literature-collapse-xy-fz.md etp_specializations.py`

## In plain words

1. **The question.** A *magma* is a set with one operation `*` that combines two elements. Our
   structures also have an operation `f` that changes one element. A *law* is a rule such as
   `(x*y)*f(z) = y` that must hold for every choice of the letters. A law *collapses* when every
   structure that satisfies it has only one element. Steps 05 and 08 found that `(x*y)*f(z) = y`
   and its *mirror* `f(x)*(y*z) = y` (the same law with every product read backwards) collapse.
   Before anyone calls that new: has someone written it down before?

2. **What was done, in order.**
   1. **Special cases in the Equational Theories Project (ETP).** The ETP settled, for 4,694 short
      magma laws (no `f`), which ones imply which. If our law collapses, then so does every magma
      law we get by putting a fixed formula in place of `f`: for example `f(z) := z` gives
      `(x*y)*z = y`. Reason: a magma that satisfies `(x*y)*z = y` becomes a structure for our law
      if we let `f` do nothing, so it has one element. Such special cases must therefore appear in
      the ETP as laws that force one element. This is a consistency test: if the ETP had a
      special case with a bigger model, our proof would be wrong.
   2. **Wrote `etp_specializations.py`**, which forms the special cases for `f(z) := z`, `z*z`,
      `z*(z*z)` and `(z*z)*z` (all special cases with at most 4 operations, the ETP's size limit),
      finds each one in the ETP's equation list (up to letter names and the side it is written on),
      and reads in the ETP's table of outcomes whether that equation implies `x = y` (the ETP's
      *Equation2*, the *singleton law*). It first checks that it reads the table the right way round.
   3. **Mutation test of the script** (a *mutation* is a deliberately corrupted input; a checker
      that accepts it is useless): 7 corrupted variants, all rejected, each for the intended
      reason. A wrong expectation also makes the script exit with code 1.
   4. **Web searches** (6 queries, listed below) and **GitHub searches** (2 repository searches,
      2 code searches) for the law, for its shape ("one binary and one unary operation, identity
      forces a one-element algebra"), and for the ETP's special case.

3. **A small example.** Take the two-element magma where `a*b = b` for all `a`, `b` (the product
   is always the right-hand element), and let `f` do nothing. Then `(x*y)*f(z) = y*z = z`, which
   is not `y` when `y = 0` and `z = 1`. So this structure breaks the law, as it must: the law
   allows only one element. The same table read with `f(z) := z` is the ETP's Equation30
   `x = (y ◇ x) ◇ z` (with letters renamed), and the ETP records Equation30 as forcing one element.

4. **What came out, and what it means.**
   - The 8 special cases are ETP Equations 30, 174, 1508, 1711 (from `(x*y)*f(z) = y`) and 15, 178,
     1933, 2136 (from `f(x)*(y*z) = y`). The ETP's outcome table records all 8 as implying
     Equation2 (4 by an explicit proof, 4 by a chain of implications). Equations 15 and 30 are
     each other's mirrors in the ETP's own list of mirror pairs (`data/duals.json`, line 9:
     `[15, 30]`), as our laws are.
   - It means: our collapse result agrees with the ETP everywhere the two can be compared. The
     special cases are **known** (ETP).
   - It does NOT mean that our laws are known, or that they are new. A special case collapsing
     says nothing about the law with a general `f`: the direction goes from our law to the
     special case, not back.
   - It does NOT mean the ETP proved anything about our laws. We did not run or read the ETP's
     Lean proofs (no Lean on this machine).
   - The searches found **nothing** about `(x*y)*f(z) = y`, `f(x)*(y*z) = y`, or a general result
     that would cover them. "Not found" is not "does not exist": 6 web queries and 4 GitHub
     queries are a shallow search, and no paper database (zbMATH Open, MathSciNet) was searched.

5. **How a reader can re-check it.** With a clone of `github.com/teorth/equational_theories` at
   `../_external/equational_theories` (or its path as the argument):
   ```
   python etp_specializations.py              # 8 lines, then "ALL PASS: 8 special cases, ..."
   python etp_specializations.py --selftest   # "selftest: 7 of 7 corrupted inputs rejected", ALL PASS
   ```
   On Windows set `PYTHONIOENCODING=utf-8` first (the ETP writes `◇`). The searches are listed
   below with their date; a reader can repeat them.

## Goal

Queue item 2: literature check of the collapse of `(x*y)*f(z) = y` (and its mirror
`f(x)*(y*z) = y`) by shape, on GitHub, and in the ETP's collapse list for the `f = identity` case.

## Command(s)

```
python etp_specializations.py
python etp_specializations.py --selftest
python -c "import etp_specializations as e; e.EXPECTED[('(x*y)*f(z) = y','z')] = 31; e.main([])"   # must exit 1
grep -rn "theorem Equation\(30\|15\|174\|178\|1508\|1711\|1933\|2136\)_implies_Equation[0-9]* " ../_external/equational_theories/equational_theories
sed -n 9p ../_external/equational_theories/data/duals.json
gh search repos "unary magma" --limit 20
gh search repos "type (2,1) algebra identities" --limit 10
gh search repos "magma unary operation equational" --limit 15
gh search code "f(x) ◇ (y ◇ z)" --limit 10
gh search code "\"(x*y)*f(z)\"" --limit 15
gh search code "\"x*(y*z) = y\" unary" --limit 10
```
Web searches (search engine tool of this session, 2026-11-22, standard mode):
1. `identity "(xy)f(z) = y" OR "(x*y)*f(z) = y" binary and unary operation trivial algebra`
2. `algebras of type (2,1) identity implies one-element algebra trivial variety unary operation`
3. `"singleton variety" OR "trivializing identity" OR "trivial variety" single identity binary unary operation characterization`
4. `equational laws magma with unary operation implications "unary" equational theories project extension`
5. `"one binary and one unary operation" single identity "only trivial models" OR "one-element" Prover9 Mace4`
6. `"x = (y ◇ x) ◇ z" OR "Equation30" equational theories singleton law`

Plus all 22 LOOP gates (all exit 0; none of their inputs changed).

## Inputs

- Local ETP clone `../_external/equational_theories`, commit `dbc9a2b` (2026-11-19 22:45 -0800),
  read only. SHA-256: `data/equations.txt` `8351d54e8820c84f4cae94ef8a90ec5a2d5e5d472c1b3eaf23bcef34d4f07c09`;
  `data/2024-11-10-outcomes.json.zip` `eb8707f4de2d1487973a76200ced237ddb2650c1c483e12b826e0e1f49185cd0`
  (its one member `outcomes.json` is dated 2024-11-10 inside the zip: a snapshot from during the
  project, not its final state); `data/duals.json` `2257eb972d163b25f29732243eecffa31c7f567b0ea1040da4b1f118f15ed481`.
- Parser `check_derivation.py` and normal form `mirror_pairs.normal` (both unchanged).
- Python of the project virtual environment; `gh` CLI.

## Output

- New script `etp_specializations.py` (with `--selftest`). Not in CI and not a LOOP gate: it needs
  the ETP clone (a 500 MB table inside a zip), and it checks consistency with published data, not
  a result of ours.
- The 8 special cases and their ETP outcomes (section "In plain words", item 4).
- Search record: no source found for either law or for a general theorem covering them.
- In the local clone, the ETP's Lean files contain theorems named
  `Equation1508_implies_Equation2`, `Equation1711_implies_Equation2`,
  `Equation1933_implies_Equation2` and `Equation2136_implies_Equation2`
  (`equational_theories/Generated/MagmaEgg/small/_002.lean`); for 15, 30, 174, 178 no direct
  theorem to Equation2 was found by that grep (the outcome table says "implicit", that is, by a
  chain of implications).
- README and llms.txt: the literature status of the two collapses.

## Checks done (and what each one can and cannot catch)

- Orientation of the outcome table: the row of Equation2 is all true and Equation1 does not imply
  Equation2 (both must hold if row means "implies" and column means "is implied"). Catches a table
  read the wrong way round. Cannot catch an error in the ETP's own data.
- Each special case matches exactly one ETP equation. Every one of the 4,694 ETP lines was read by
  our parser without error. Catches a wrong substitution, a wrong normal form, a shifted list.
  Cannot catch two different laws with the same normal form (not seen: one id per special case).
- 7 mutations, each rejected for the intended reason (printed): a law that does not collapse
  (`(x*y)*f(z) = x`, special case Equation27, which the table records as not implying Equation2),
  table read transposed, equation list shifted by one, expected ids off by one, `f` replaced only
  at the top of a side, a normal form that ignores swapped sides, the row of Equation1 read in place
  of Equation2's. Exit code 1 on a failing check tested separately.
- The searches: result lists only. No result looked like it concerned these laws, so no primary
  page was opened. The search tool's one-paragraph summaries were not used as facts.

## NOT verified

- The ETP's outcome table and Lean proofs were not re-checked here (no Lean). That the 8 special
  cases force one element is the ETP's claim, labelled `known` on their word.
- Whether the ETP's final data (after 2024-11-10) still lists these 8 as implying Equation2: not
  checked against a later file (true implications are not expected to change, but that is an
  expectation, not a check).
- Paper databases (zbMATH Open, MathSciNet, Google Scholar) were not searched; MathSciNet is on
  ams.org, which this project does not fetch. Books on universal algebra and on "algebras of type
  (2,1)" were not consulted. Whether the two laws appear there: unknown.
- `gh search code` printed nothing for all three queries. Whether it searched properly (code
  search needs a logged-in account and has its own query syntax) or truly found nothing: unknown.
- Special cases with 3 or more operations in place of `f(z)` (beyond the ETP's limit) and special
  cases with a constant in place of `f` (structures with a constant, not magmas) were not looked up.
- The collapse proofs themselves are unchanged and still not reviewed by a human, nor by Lean.

## Surprises, errors, dead ends

- First run of the script crashed under Windows' default console encoding on the `◇` character;
  run with `PYTHONIOENCODING=utf-8`.
- First draft of the selftest read the outcome rows only for the 8 expected ids, so the mutation
  "a law that does not collapse" crashed with a `KeyError` instead of being rejected. It was not
  counted as caught (the selftest stops on any error other than the checker's own); fixed by
  loading the rows the mutation needs too.
- No dead end in the searches, only no hits.

## Next

Queue item "literature check: the four candidate Austin laws" (by text and by shape). A deeper
search for the collapses (zbMATH Open, after its robots.txt) is queued as its own item.
