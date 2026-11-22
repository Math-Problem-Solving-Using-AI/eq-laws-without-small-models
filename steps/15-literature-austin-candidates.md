# 15. Literature check: the four candidate Austin laws (first piece)

- Date: 2026-11-22
- Status label: literature check (S5 of `docs/shared/VERIFICATION_PROTOCOL.md`), shallow: "not found
  in searches" for the four laws themselves; their magma special cases are `known` (ETP) for order 4
  or less and `z3-only` for order 5. No mathematical label changes: finite part still
  `hand-argument`, infinite part still `z3-only`.
- Commit(s): see `git log -- steps/15-literature-austin-candidates.md etp_specializations_austin.py`

## In plain words

1. **The question.** A *magma* is a set with one operation `*` that combines two elements. Our
   structures also have an operation `f` that changes one element. A *law* is a rule such as
   `(f(x)*y)*z = y` that must hold for every choice of the letters; a structure where it holds is
   a *model* of the law. Four of our laws, `f(x*(y*z)) = y`, `x*(y*f(z)) = y`, `(f(x)*y)*z = y`
   and `f((x*y)*z) = y`, seem to have models only when the model is infinite or has one element
   (steps 06 and 07). For magmas such a law is called an *Austin law*. Has anyone written about
   these four laws, or does published data contradict what we believe about them?

2. **What was done, in order.**
   1. **Special cases.** If we put a fixed formula in place of `f`, for example `f(z) := (z*z)*z`,
      the law becomes a magma law (a *special case*). Every finite magma model of the special case
      would give a finite model of our law (let `f` compute the formula). So if our counting
      argument is right, no special case can have a finite model with 2 or more elements. The
      Equational Theories Project (ETP) has published data on many magma laws; if it listed a
      special case with such a model, our argument would be wrong. This is a test that could catch
      a mistake, not a proof.
   2. **Wrote `etp_specializations_austin.py`.** It puts each of the 9 formulas in one letter with
      at most 3 operations in place of `f`, keeps the special cases with at most 5 operations
      (22 of them), and finds each in the ETP's equation lists (letters renamed, sides swapped as
      needed). For the ones with at most 4 operations it reads the ETP's table of outcomes. For the
      ones with 5 operations there is no such table, so it reads the three tables of the ETP
      blueprint's chapter "Order 5 Austin laws" (the laws whose finite or infinite models were not
      settled there) and asks z3 (an automatic prover) whether the special case forces one element.
   3. **Mutation test** (a *mutation* is a deliberately corrupted input; a checker that accepts it
      is useless): 13 corrupted variants, all rejected, each for the intended reason (printed).
      A wrong expectation also makes the script exit with code 1 (tested).
   4. **Read the ETP blueprint's two chapters on Austin laws** in the local clone, and noticed that
      Kisielewicz's Austin laws there are close relatives of our `(f(x)*y)*z = y` (item 4 below).
      The script checks that relation too.
   5. **Web searches** (5 queries) and **GitHub searches** (3 repository searches, 1 code search).

3. **A small example.** Take the two-element magma on `{0, 1}` where `a*b = b` (the product is
   always the right-hand element) and let `f(z) := (z*z)*z`, which here is just `z`. Then
   `(f(x)*y)*z = z`, which is not `y` for `y = 0`, `z = 1`. So this structure breaks
   `(f(x)*y)*z = y`, as our argument says every finite structure with 2 or more elements must. The
   special case `(((x*x)*x)*y)*z = y` is the ETP's Equation3151, and the ETP records that it forces
   one element, so the ETP agrees for this formula.

4. **What came out, and what it means.**
   - All 22 special cases are fine: the 8 with at most 4 operations (ETP Equations 15, 30, 70,
     282, 493, 696, 2948, 3151) are recorded by the ETP as forcing one element; the 12 with 5
     operations (Equations 5016, 5893, 6770, 7647, 8524, 21654, 24285, 37547, 38424, 39301, 40178,
     41055) are in none of the blueprint's three unsettled tables, and z3 proves each forces one
     element (`z3-only`). The remaining 2 entries of the 22 repeat Equations 15 and 30.
   - **The Kisielewicz connection.** The blueprint gives Kisielewicz's two Austin laws as
     `x = (((y*y)*y)*x)*((y*y)*z)` (Equation374794, from his 1990 paper) and
     `x = (((y*y)*y)*x)*(y*z)` (Equation28770, from "Austin identities", 1997). Both are our law
     `(f(x)*y)*z = y` with `f(t) := (t*t)*t` and with `z` replaced by `(y*y)*z` or `y*z` (checked by
     the script). The blueprint's proof that 28770 has no finite model with 2 or more elements is
     the same argument as ours for `(f(x)*y)*z = y`: `x -> y³*x` is one-to-one, hence onto in a
     finite set, hence `y*z` does not depend on `z`. The mirror law of 28770, Equation17522, is
     `x*(y*f(z)) = y` with `f(t) := t*(t*t)` and letters substituted. So our counting argument is a
     known kind of argument, and our law `(f(x)*y)*z = y` is a version of Kisielewicz's shape
     with the cube `y³` replaced by a free operation `f`.
   - It does NOT mean our laws are known: no source we found states them. It also does NOT mean
     they are new: 5 web queries and 4 GitHub queries are a shallow search, and no paper database
     was searched.
   - It does NOT prove our finite argument. The special cases are much stronger laws (they force
     one element outright), so their agreeing is weak evidence. It does not touch our infinite
     models either: Kisielewicz's infinite models satisfy weaker laws and are not models of ours.
   - It does NOT mean anything for special cases with 6 or more operations: not looked at.

5. **How a reader can re-check it.** With a clone of `github.com/teorth/equational_theories` at
   `../_external/equational_theories` (or its path as the argument), on Windows after
   `set PYTHONIOENCODING=utf-8`:
   ```
   python etp_specializations_austin.py              # 22 lines, 3 instance lines, then "ALL PASS: 22 special cases, ..."
   python etp_specializations_austin.py --selftest   # "selftest: 13 of 13 corrupted inputs rejected", ALL PASS
   ```

## Goal

Queue item 2: literature check of the four candidate Austin laws, by text and by shape. First
piece only: ETP data and blueprint, web and GitHub searches. Re-reading the Ernst slides (Dudek's
`(ex)y = x`) is split off as its own queue item.

## Command(s)

```
python etp_specializations_austin.py
python etp_specializations_austin.py --selftest
python -c "import etp_specializations_austin as e; e.EXPECTED[('(f(x)*y)*z = y','z')] = 31; e.main([])"   # exit 1
sed -n 1,123p ../_external/equational_theories/blueprint/src/chapter/order_5.tex
sed -n 5,100p ../_external/equational_theories/blueprint/src/chapter/infinite_models.tex
grep -n "Equadef{374794}\|Equadef{28770}" ../_external/equational_theories/blueprint/src/chapter/equations.tex
gh search repos "Austin law" --limit 10
gh search repos "austin identities magma" --limit 10
gh search repos "infinite models magma unary" --limit 10
gh search code "Austin law unary" --limit 10
gh api repos/YanbiaoLab/Order5-Austin-Law-Proofs/readme
```
Web searches (search tool of this session, 2026-11-22, standard mode):
1. `"f(x(yz)) = y" OR "x(yf(z)) = y" OR "(f(x)y)z = y" identity unary operation no finite models`
2. `Austin identity algebra of type (2,1) binary and unary operation only infinite nontrivial models`
3. `Kisielewicz "Austin identities" Algebra Universalis 1997 unary operation`
4. `"varieties of algebras with no nontrivial finite members"`
5. `single identity "no nontrivial finite models" "infinite models" unary operation semigroup groupoid equational theories project extension`

Plus all 22 LOOP gates and `etp_specializations.py` with `--selftest` (all exit 0; none of their
inputs changed).

## Inputs

- Local ETP clone `../_external/equational_theories`, commit `dbc9a2b` (2026-11-19 22:45 -0800),
  read only. SHA-256: `data/eq_size5.txt` `c39b84a595ea2453b106cfeed300c7f1153fc3d4b4d605f65ec3b873f1951b3c`
  (62,576 lines, the first 4,694 equal to `data/equations.txt`, checked by the script);
  `blueprint/src/chapter/order_5.tex` `1fa2b36135837603fb0c42dd7c392ebae7d77c07fd72b341893137d9bb9169fb`;
  `blueprint/src/chapter/equations.tex` `50831908a11145d5a46109413db74a8e278e28e599cd9880f0652080dbe79a45`;
  `blueprint/src/chapter/infinite_models.tex` `49def1d0d42714dbd1175f039b25c789c05c0adb9c25689f82e00119cc2283be`;
  `data/equations.txt` and the outcome zip as in step 14.
- Parser `check_derivation.py`, helpers of `etp_specializations.py` (both unchanged).
- Python 3.12.10, z3 version string `5.4.1` (as printed by `z3.get_version_string()`), `gh` CLI.

## Output

- New script `etp_specializations_austin.py` (with `--selftest`). Not in CI and not a LOOP gate,
  for the same reason as `etp_specializations.py` (needs the ETP clone).
- The 22 special cases and the 3 instance relations (section "In plain words", item 4).
- Search record: no source found for any of the four laws, or for Austin-type laws with a unary
  operation. Leads found (not read as primary sources, see "NOT verified"):
  - arXiv 2609.05690, "Trace-Tree Magmas: Proof-Producing Infinite Countermodels and 28 New
    Order-Five Austin Classifications" (2026); by the search summary about magmas only.
  - GitHub `YanbiaoLab/Order5-Austin-Law-Proofs` (created 2026-09-08, last push 2026-09-17), README
    read with `gh api`: Lean files for the 130 equations of the blueprint's order-5 tables, magmas
    only (its own words: "`∀ (G : Type) [Magma G] [Finite G], EquationN G → Equation2 G`"). None
    of our 22 special cases is among those 130 (the script checks the blueprint's tables).
  - A record of Kisielewicz, "Austin identities", Algebra Universalis 38 (1997), in the Wrocław
    university digital library (`digilab.uwr.edu.pl`), seen in a result list only; whether it holds
    the full text is unknown. Useful for queue item 3.

## Checks done (and what each one can and cannot catch)

- Orientation of the outcome table and the id order, as in step 14 (shared code).
- Each special case matches exactly one ETP equation; all 62,576 lines of `eq_size5.txt` were read
  by our parser (letters renamed from a 25-letter alphabet, because order-5 equations have up to 7
  letters and `mirror_pairs.normal` only knows 6). Catches a wrong substitution, normal form or
  shifted list.
- The three blueprint tables are read with the row counts the blueprint's own text gives (10, 96,
  24). Catches a table lost by the parser.
- z3 collapse queries: magma laws only (an `f` left in would raise an error); `unsat` is required.
- The 3 instance relations: the stated text equals the ETP's (from `eq_size5.txt`, or for 374794
  from the blueprint's `\Equadef`), and applying the stated substitution to the special case gives
  that text up to letter names and sides.
- 13 mutations, each rejected for the intended reason (printed): a law with finite models
  (`(f(x)*y)*z = z`, special case Equation34, recorded as not forcing one element), the same law
  for order 5 only (z3 answers `sat`), table transposed, equation list shifted, order-5 list
  shifted, expected ids off by one, `f` replaced only at the top, normal form that ignores swapped
  sides, one of our ids put into a blueprint table, the third table cut off, z3 answer replaced by
  `unknown`, an instance with a wrong substitution, an instance with a wrong id. Separately: an
  instance with id 374795 (not defined anywhere) and one with a changed text are rejected.

## NOT verified

- The ETP's outcome table, its Lean proofs and its blueprint text were not re-checked here (no
  Lean). That Kisielewicz's laws are Austin laws is the blueprint's claim, labelled `known` on its
  word; Kisielewicz's papers themselves were not read.
- For the 12 order-5 special cases only z3 says they force one element (`z3-only`, no derivation
  stored, not checked by a second tool).
- That the blueprint's three order-5 tables are complete and up to date: not checked. The
  YanbiaoLab README says some table entries have since been settled (for example Equations 5834
  and 40037 force one element), so the tables are a 2024 snapshot. This does not affect our check,
  because none of our special cases is in them.
- Special cases with 6 or more operations, and special cases where `f` is replaced by something
  other than a formula in one letter (for example a formula with a constant), were not looked at.
- arXiv 2609.05690 was not opened (only a search result line and summary); the Wrocław library
  record was not opened. What they say: unknown.
- No paper database (zbMATH Open, MathSciNet, Google Scholar) was searched; Dudek's work and the
  Ernst slides were not re-read (split off as a queue item). Whether the four laws appear in the
  literature on algebras of type (2,1): unknown.
- `gh search code` again printed nothing; whether code search ran properly is unknown (as in step 14).
- The counting argument itself is unchanged and still `hand-argument`, not reviewed by a human
  and not in Lean.

## Surprises, errors, dead ends

- First prototype crashed with an `IndexError` in `mirror_pairs.normal`: its renaming alphabet has
  6 letters and some order-5 ETP equations have 7. The new script has its own renaming with a
  longer alphabet; `mirror_pairs.py` is unchanged.
- A first exit-code test replaced the module's `INSTANCES` list after import and seemed to show a
  wrong id accepted. The cause was the test, not the checker: `check` binds `instances=INSTANCES`
  as a default when the function is defined, so the replacement never reached it. Re-tested by
  passing the corrupted list as an argument: rejected. (The `EXPECTED` test worked because that
  dict was changed in place.)
- A first draft of the mutation "equation list shifted by one" shifted `equations.txt` but not the
  same lines inside `eq_size5.txt`, so it would have been rejected by the prefix check rather than
  by the id lookup it was meant to test. Fixed before the first selftest run.
- Not a dead end, but a surprise: the "Austin law" literature already contains our finite
  argument, in Kisielewicz's 1997 law, with a cube in the place of our `f`.

## Next

Queue: re-read the Ernst slides (Dudek's `(ex)y = x`) after that site's robots.txt; read the
arXiv 2609.05690 abstract page (after arXiv's robots.txt and its crawl delay); queue item 3
(Kisielewicz's definition) now has a lead in the Wrocław library.
