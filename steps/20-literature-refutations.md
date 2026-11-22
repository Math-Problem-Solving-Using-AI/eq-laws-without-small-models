# 20. Literature check: the 2,828 non-implications of step 11

- Date: 2026-11-22
- Status label: literature check (S5 of `docs/shared/VERIFICATION_PROTOCOL.md`), shallow. The 2,828
  non-implications themselves: "not found in searches" (queries and dates below). The method that
  builds the four infinite models: `known` for magmas (ETP report, section "Canonization", read in the
  local clone); that our four models have this shape is our own reading (`hand-argument`, a lead).
  No mathematical label changes: each non-implication stays `z3-only`.
- Commit(s): see `git log -- steps/20-literature-refutations.md`

## In plain words

1. **The question.** Our structures have two operations: `*`, which combines two elements into
   one, and `f`, which turns one element into another. A *law* is a rule such as
   `x*(y*f(z)) = y` that must hold for every choice of the letters. A *model* of a law is a
   structure where the law holds. Law A *implies* law B when every model of A is also a model of B.
   In step 11, four infinite models (called A, B, C, D) showed 2,828 times that "law A does not
   imply law B": the model satisfies A, and B fails at stored elements (the *witness*). Has anyone
   published these results, or the way the models were built?

2. **What was done, in order.**
   1. **Read the Equational Theories Project's own texts in the local clone** (commit `dbc9a2b`,
      2026-11-19). The *ETP* is a large public project that settled which short laws imply which,
      for structures with `*` only (*magmas*). We wanted to know whether our way of building models
      is already a known method, because a known method is part of the literature check. It is:
      the ETP report has a section "Canonization" that builds "a special kind of syntactic model"
      by rewriting every instance of the law's left side to its right side and leaving every other
      term as it is (quotes below). The ETP blueprint has the same idea under "Confluent theories".
   2. **Compared that method with our four models** (by reading `check_refutations.py`, lines
      84 to 109). Each of our models does exactly that: model B, for example, multiplies formally,
      except that `x * P(y, F(z))` gives `y`, which is the law `x*(y*f(z)) = y` read left to right.
      This comparison is a reading, not a machine check.
   3. **Web searches** (6 queries, Springer, AMS and zbMATH excluded because the loop does not
      fetch them) for: the phrase "identities of type (2,1)" with implication and term model; our
      law shapes with "free algebra"; equational laws with one binary and one unary operation and
      infinite term models; the ETP's "confluent" and "anti-implication" words; free groupoids with
      a unary operation and the word problem; one-generated free algebras used to refute
      implications. Only the summaries and titles were seen; no page was opened.
   4. **OpenAlex** (an open index of research papers): its `robots.txt` (the file where a site
      says what programs may fetch) was read first in its own request (`Allow: /`), then 5
      searches by words, 10 seconds apart, 15 titles each, saved and fingerprinted.
   5. **GitHub**: 3 repository searches and 3 code searches (two with our law texts), plus two
      control searches that must find something (they did), so that "0 hits" means something.
   6. **A small scratch check with a mutation test** (a *mutation* is a deliberately corrupted
      input; a working check must notice it). A script confirmed that each of the 5 quotes below
      occurs exactly once in its file, and scanned the 75 OpenAlex titles for the words "Austin",
      "term model", "canoniz", "unary", "(2,1)" and "f(x". With one quote corrupted it printed
      "FAIL" and exited 1.
   7. **Ran all 22 LOOP gates** (the repository's own checks): all exit 0.

3. **A small example of the method.** In model B, `f(t)` is the formal term `F(t)`, and `x*w` is
   the formal pair `P(x, w)`, except when `w` is a pair `P(y, F(z))`; then `x*w` is `y`. Check the
   law `x*(y*f(z)) = y` at `x = y = z = G` (`G` is a starting element): `f(G) = F(G)`;
   `G*F(G) = P(G, F(G))`, because `F(G)` is not a pair; then `G*P(G, F(G)) = G`, which is `y`. So
   the law holds here. The commutative law `x*y = y*x` fails: `G*F(G) = P(G, F(G))` but
   `F(G)*G = P(F(G), G)`, two different terms. That is one of the 2,828 witnesses: law
   `x*(y*f(z)) = y` does not imply `x*y = y*x`. The ETP report gives the same kind of model for the
   magma law `y*(x*(y*(y*y))) = x`: send every term of the form `w*(v*(w*(w*w)))` to `v` and leave
   all other terms unchanged.

4. **What came out, and what it means.**
   - **The method is known (for magmas).** The ETP report calls it *canonization* and proves that
     it gives a model when three conditions hold (the rewrite only shortens a term to a part of
     itself, it applies to every instance of the law's left side, and it never applies inside the
     left side; their words below). Our four models have this shape, with `f` added. We did not
     check the three conditions by machine, and the ETP's theorem is stated for `*` alone, so
     carrying it over to `f` is our own step. So far it is a second, hand-level reason why our
     models satisfy their laws, next to the z3 check of step 06 and 07.
   - **The 2,828 results themselves were not found** in any source seen: no paper, no repository
     states implications or non-implications between laws with one binary and one unary operation
     of our kind. The only search hit about such laws was the main repository of this project
     (our own work).
   - It does NOT mean the results are new. The search was shallow: no paper database but OpenAlex,
     titles only, no reviews (zbMATH is blocked for the loop, see STATE.md), no books.
   - It does NOT raise any label. Each non-implication is still `z3-only`.

5. **How a reader can re-check it.**
   ```
   grep -n "Canonization\|weakly collapsing, a weak canonizer" ../_external/equational_theories/paper/metatheorems.tex
   curl -s -G https://api.openalex.org/works --data-urlencode "search=identities of type (2,1)" --data-urlencode "per-page=15" --data-urlencode "select=id,display_name,publication_year"
   python check_refutations.py results/refutations_term_models.json
   ```
   The first needs a clone of `teorth/equational_theories` next to this repository and prints lines
   54 and 95. The second lists titles (the first one seen on 2026-11-22: "The Order of
   Hypersubstitutions of Type (2,1)", 2011); results of an index change over time. The third ends
   with exit code 0 and re-checks all 2,828 witnesses.

## Goal

Queue item 2 (STATE.md before this run): literature check of the 2,828 non-implications of step 11,
with search terms such as "term model", "free algebra", "identities of type (2,1)". Item 1 (Lean) is
still blocked.

## Command(s)

Local reading (no network), in the ETP clone at commit `dbc9a2b` (2026-11-19):
```
grep -rIn -i "canoniz" --include=*.tex .          # paper/metatheorems.tex, paper/conclusions.tex
sed -n 54,122p paper/metatheorems.tex
sed -n 96,169p blueprint/src/chapter/abstract_nonsense.tex
sed -n 1,96p blueprint/src/chapter/rewriting.tex
```
Network, 2026-11-22, times UTC:
```
WebSearch x6, standard mode, roughly 20:40 to 20:52, times not recorded per query (springer, ams, zbmath excluded):
  "identities of type (2,1)" implication term model non-implication
  free algebra binary and unary operation identity "f(x(yz))" OR "x(yf(z))" infinite model
  equational laws one binary one unary operation implications counterexample infinite term model rewriting normal forms
  "confluent" "anti-implication" free magma normal forms equational theories project
  "word problem" OR "free algebra" "groupoid with a unary operation" identity rewriting normal form
  one-generated free algebra infinite model refute implications between short identities unary binary signature automated
curl https://api.openalex.org/robots.txt                              # 20:46:15, 200, "User-agent: * / Allow: /"
curl -G https://api.openalex.org/works search=<q> per-page=15         # 20:46:23 to 20:47:07, 10 s apart, all 200
  q1 "identities of type (2,1)"                          count 74,888
  q2 "groupoids with a unary operation identities"       count 1,109
  q3 "equational implications binary and unary operation" count 6,337
  q4 "free algebra term model refutes identity implication" count 3,720
  q5 "canonizer equational law magma"                     count 15
gh search repos "equational theories unary operation"     # 20:47:43, 0
gh search repos "magma unary operation implications"      # 0
gh search repos "canonizer equational"                    # 2, both unrelated (equation-solving utilities)
gh search code '"x*(y*f(z)) = y"'                         # 0
gh search code '"(f(x)*y)*z = y"'                         # 0
gh search code '"unary operation" "magma" implication law' # 0
gh search repos "groupoid identities unary"               # 0
gh search repos "equational theories"                     # control: teorth/equational_theories first
gh search code "Equation167" --repo teorth/equational_theories   # control: 3 files
```
Scratch check (session scratch folder, not the repository):
```
python -I quotes20.py <ETP clone> <OpenAlex results>          # exit 0, 5 quotes found once each
python -I quotes20.py <ETP clone> <OpenAlex results> mutate   # exit 1, corrupted quote found 0 times
```
Plus all 22 LOOP gates (all exit 0).

## Inputs

- ETP clone, commit `dbc9a2b` (2026-11-19). Quotes, verbatim (LaTeX as in the files):
  - `paper/metatheorems.tex` line 56: "One possible way of obtaining refutations of a given
    implication $\E \models \E'$ between equational laws is by building a special kind of syntactic
    model, via certain involutions on elements of the free magma $\Magma_X$ we call
    \emph{canonizers}."
  - line 95 (theorem): "Whenever $R$ is weakly collapsing, a weak canonizer, and non-overlapping,
    then $C_R$ is a canonizer." The definitions (lines 76 to 79): weakly collapsing, "for every word
    $w$, $R(w)$ is a (not necessarily proper) sub-word of $w$"; weak canonizer, "for any
    substitution $\theta$, $R(\varphi_\theta l)=\varphi_\theta r$"; non-overlapping, "for every word
    $w\in M_X$ which is a strict sub-word of $l$ that is not in $X$, and any substitution $\theta$,
    $R(\varphi_\theta w) = \varphi_\theta w$".
  - line 119: "if this transformation is \emph{terminating} and \emph{confluent} (intuitively,
    rewrites cannot go on forever, or diverge forever), then one may simply pick the transformation
    which sends a term to its normal form as a canonizer."
  - line 121: "we leave the investigation of the precise relationship of the classical theory with
    the above technique as future work."
  - `blueprint/src/chapter/abstract_nonsense.tex` line 127 (corollary "Criterion for
    anti-implication"): "Then a law $w \formaleq w'$ is a consequence of $\Gamma$ if and only if
    $w,w'$ have the same normal form reduction."
  - `blueprint/src/chapter/rewriting.tex` line 75, a non-confluent example: "\[ x \cdot (y \cdot z)
    \rightarrow y \]" (the magma relative of our `f(x*(y*z)) = y`).
- OpenAlex result files, SHA-256: q1 `6db35e801edf31629e7fe2f8b4ca0634df0703e0c43ea155c000c8ae5701a532`,
  q2 `b018f8dfeb9dd52d775651ca1a76eb5b9ceb332e8f84dba967d11fb62924c55f`,
  q3 `67a9dbb63fec2223bf808f2d9fae8cef941daf7f5e1f54cf4a028211f9a2dfa4`,
  q4 `223d7ef1cc48fe75cae46cb699da96bcb8cdf3b9b83c0dbb5fde0f4f7e30aa78`,
  q5 `b94edfe5fe2a5b1123c29940b178b579a6f434ee130a95887ec6d1663d759547` (the files themselves were
  scratch and are not kept). Titles about type (2,1) seen: "The Order of
  Hypersubstitutions of Type (2,1)" (2011, W2901291365), "An elegant 3-basis for inverse
  semigroups" (2010, W2040021389), "Axioms for Unary Semigroups via Division Operations" (2012,
  W2005109419). None is about our laws by title; no abstract was read. q5 returned the ETP report
  (W7111183655) and unrelated works.
- `check_refutations.py` lines 84 to 109 (our four models: `f_A`, `mul_B`, `mul_C`, `f_D`).
- `gh` (GitHub CLI), `curl` (Git for Windows), Python 3.12.10.

## Output

- This step file; one README sentence (literature status of the 2,828 results and the known method)
  and the README step list. No code, results or certificates changed.

## Checks done (and what each one can and cannot catch)

- Quotes: scratch script found each of the 5 quotes exactly once in its file; with one quote
  corrupted it reported 0 occurrences and exited 1. Catches a misquote. Cannot catch a quote taken
  out of context.
- OpenAlex titles scanned for keywords: no title contains "austin", "term model", "canoniz" or
  "f(x"; the "(2,1)" and "unary" hits are listed above and are by title not about our laws. Catches
  an obvious hit in the saved titles. Cannot see abstracts or anything below the first 15 results.
- GitHub "0 hits" backed by two control searches that did find known items. Cannot catch code
  that GitHub has not indexed, or laws written with other letters or symbols.
- robots.txt of OpenAlex read in its own request before its pages; waits of 10 seconds between
  OpenAlex requests (inside the command).
- All 22 LOOP gates rerun, all exit 0.

## NOT verified

- That our four models satisfy the three conditions of the ETP canonization theorem: read by hand
  only, not checked by machine, and not reviewed. The theorem is stated for magmas; whether its
  proof carries over to a signature with `f` was not checked (our models' correctness still rests
  on z3, `term_models_z3.py`).
- Model A and model D change `f`, not `*`, and leave `f(t) = t` by default instead of a formal
  `F(t)`; whether that still fits the ETP definitions word for word was not checked.
- The ETP report's PDF or arXiv version was not read; only the LaTeX source in the clone (it may
  differ from the published version).
- Every web search result: only the search engine's summary and titles were seen, no page opened.
  The summaries mention Tao's 2024 blog post on "free magmas associated to 'confluent' equational
  laws" and the Knuth-Bendix paper (1970) with "a unary operator" example: both leads, not read.
- Abstracts of the OpenAlex hits: not read. Only 15 results per query were looked at.
- zbMATH, MathSciNet, Springer: not searched (blocked or not fetched by the loop).
- Books on universal algebra or term rewriting (for example Baader and Nipkow, which the ETP
  cites): not read.
- Whether any of the 2,828 non-implications has a magma special case recorded in the ETP: not
  checked (possible further cross-check).

## Surprises, errors, dead ends

- The scratch quote checker first lost its backslashes (LaTeX quotes written as ordinary Python
  strings, so `\G`, `\[` became escape sequences) and reported two quotes as missing. Fixed with raw
  strings; the mutation run then failed for the intended reason only.
- `python -I` ignores `PYTHONIOENCODING`, so printing a Greek letter from an OpenAlex title crashed
  on the Windows console. Fixed with `sys.stdout.reconfigure(encoding="utf-8")`.
- One web search returned the main repository of this project as its best hit: our own work, not
  a source.

## Next

Queue: the rest as before; new items: check by machine that the four models fit the ETP
canonization conditions (with `f`), and read the Knuth-Bendix 1970 paper for examples with a unary
operation.
