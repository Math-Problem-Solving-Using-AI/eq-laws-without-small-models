# 13. Where the term "Austin law" comes from, read at the source

- Date: 2026-11-22
- Status label: literature check (S5 of `docs/shared/VERIFICATION_PROTOCOL.md`), first piece only:
  the source of one term. No mathematical label changes. The four laws stay at `z3-only` (infinite
  model) plus `hand-argument` (no finite model with 2 or more elements).
- Commit(s): see `git log -- steps/13-source-of-austin-law.md`

## In plain words

1. **The question.** A *magma* is a set with one operation `*` that combines two elements. Our
   structures also have a second operation `f` that changes one element (the type of such a
   structure is called *type (2,1)*: one operation with two inputs, one with one input). A *law* is
   a rule such as `f(x*(y*z)) = y` that must hold for every choice of the letters. A *model* of a
   law is a structure where the law holds; it is *trivial* when it has only one element (or none).
   Since step 06 the README calls four of our laws "candidate Austin laws". Question: who defines
   the term "Austin law", in what words, and for which kind of structure? Are we using it the way
   its source does?

2. **What was done, in order.**
   1. **Listed where this repository uses the term**: README (section "Leads from hand analysis"),
      steps 06 and 07, STATE.md. Steps 06 and 07 both say the term was taken from the main
      repository's notes (`eq-unary-magma-laws`, `docs/PRIOR_WORK.md`) without reading its source.
   2. **Read the main repository's notes** (`docs/PRIOR_WORK.md`, section A3(c)). They name the
      Equational Theories Project (ETP) blueprint, file `infinite_models.tex`, as the source.
   3. **Read that file and its neighbours in a local copy of the ETP repository** (a clone of
      `github.com/teorth/equational_theories` kept next to this repository, at commit `dbc9a2b` of
      2026-11-19; it is a shallow clone with that one commit, so when each sentence was written is
      unknown). The blueprint is the ETP's long technical write-up. Quotes below are verbatim.
   4. **Read the ETP's published report** (arXiv 2512.07087, version 2, the HTML page, fetched
      2026-11-22 after reading arXiv's `robots.txt`) and searched its text for "Austin".
   5. **Compared** the source's definition with how the README uses it, and rewrote the README
      paragraph so it says only what the sources say.

3. **What the sources say.**
   - ETP blueprint, `blueprint/src/chapter/infinite_models.tex`, section "Austin laws":
     "The singleton or empty magma satisfies all equational laws. It is natural to ask whether an
     equational law admits nontrivial finite or infinite models. If no model exists, then the law
     is equivalent to [Equation 2]. An *Austin law* is a law which admits infinite models, but no
     nontrivial finite models: the law is equivalent to [Equation 2] for finite magmas."
     (Equation 2 is the law `x = y`, which only trivial magmas satisfy.)
   - Same file: "Austin [Austin 1965] established the first such law, namely the order 9 law ...",
     then a law of order 6 from Kisielewicz (1990) and one of order 5 from Kisielewicz (1997),
     and "In that paper a computer search was also used to show that no law of order four or less
     is an Austin law." (*Order* = number of `*` in the law.)
   - ETP blueprint, `blueprint/src/chapter/order_5.tex`: "an *Austin law* is a law which admits
     infinite models, but no nontrivial finite models. Austin laws have order 5 or greater
     [Kisielewicz 1997]." And: "106 allow only trivial finite models. Of these, 10 are Austin
     laws, and it is unknown whether the remaining 96 admit infinite models."
   - ETP report, arXiv 2512.07087v2: the words "Austin law" do **not** appear (4 matches of
     "Austin": one sentence, "as observed by Austin [6], the converse is not true in general",
     about finite versus general implication, and three bibliography entries). The report links
     to the blueprint page "order-5-austin-laws" and lists Kisielewicz's 1997 paper, whose title
     is "Austin identities" (Algebra Universalis 38(3), 324–328).
   - Kisielewicz 1990 ("Varieties of algebras with no nontrivial finite members") and 1997
     ("Austin identities"), and Austin 1965: **not read**. The 1997 paper is on
     link.springer.com, which this project does not fetch; the 1990 book chapter has no online
     text we know of; Austin 1965 is on ams.org, also not fetched.

4. **What it means and what it does NOT mean.**
   - It means: the definition we quoted in the README is the ETP blueprint's, word for word, and it
     is stated **for magmas** (one operation `*`). Our laws also have `f`. So "Austin law" for our
     laws is the same property (infinite models exist, finite models are all trivial) carried over
     to type (2,1) by us. The README now says so, and keeps the word "candidate", because for each
     of the four laws the finite half is a hand argument and the infinite half is `z3-only`.
   - It means: the ETP's "no law of order four or less is an Austin law" is about magma laws only.
     It says nothing for or against short laws with `f`; our laws having only three operations is
     no conflict with it.
   - It does NOT tell us whether Kisielewicz, who seems to have coined the name (the title
     "Austin identities"), defined it for any type of algebra or for magmas only. The 1990 title
     speaks of "algebras" in general, but the text was not read: **unknown**.
   - It does NOT say anything about the four specific laws. No source read today mentions them.
     It is not a literature check of the laws themselves (those pieces stay in the queue).
   - It does NOT support the README's old sentence "This kind of result is known in general",
     which was vague; it was replaced by what the sources actually list.

5. **How a reader can re-check it.**
   With a clone of `github.com/teorth/equational_theories` (any recent commit):
   ```
   grep -n "Austin law" blueprint/src/chapter/infinite_models.tex blueprint/src/chapter/order_5.tex
   # 17 lines; infinite_models.tex:8 and order_5.tex:4 carry the definition quoted above
   grep -c "Austin law" paper/*.tex
   # 0 in each of the 17 files: the report's source does not use the term
   ```
   And the published report: open `https://arxiv.org/html/2512.07087v2` and search the page for
   "Austin": four matches, none of them "Austin law".

## Goal

Queue item 2 (literature check), first piece: re-read the source of the term "Austin law" before
using it further, as STATE.md asked.

## Command(s)

```
grep -rn -i "austin" --include=*.md --include=*.txt --include=*.py --include=*.json .
grep -rn -i "austin" ../_external/equational_theories/blueprint/src/chapter/*.tex
grep -rn -i "austin" ../_external/equational_theories/paper/*.tex
sed -n 1,90p ../_external/equational_theories/blueprint/src/chapter/infinite_models.tex
sed -n 1,24p ../_external/equational_theories/blueprint/src/chapter/order_5.tex
curl -s https://arxiv.org/robots.txt            # its own step, read before the next request
curl -s https://arxiv.org/html/2512.07087v2     # saved outside the repository, searched for "Austin"
```
plus all 22 LOOP gates (all exit 0, none changed).

## Inputs

- Local ETP clone `../_external/equational_theories`, commit `dbc9a2b` (2026-11-19), shallow (one
  commit), working tree clean. SHA-256 of `blueprint/src/chapter/infinite_models.tex`:
  `49def1d0d42714dbd1175f039b25c789c05c0adb9c25689f82e00119cc2283be`; of `order_5.tex`:
  `1fa2b36135837603fb0c42dd7c392ebae7d77c07fd72b341893137d9bb9169fb`.
- arXiv 2512.07087v2 HTML, fetched 2026-11-22 20:02:59 UTC, HTTP 200, 1,416,781 bytes, SHA-256
  `c2bc85166e575960ad82710de99257d95ed0a704657f64779210f7f3aed6618c` (not stored in the repository).
- arXiv `robots.txt` read 2026-11-22 20:02:52 UTC: `/html` and `/abs` allowed for all agents,
  `Crawl-delay: 15`.
- Main repository `docs/PRIOR_WORK.md` at commit `4e95da1` (read only).

## Output

- README paragraph "Leads from hand analysis" rewritten: source named with file and commit, the
  definition marked as one for magmas, our use marked as our carry-over to type (2,1), the vague
  sentence removed. No status label changed.
- This step file. No code or results changed.

## Checks done (and what each one can and cannot catch)

- Quotes copied from the files themselves, not from the main repository's notes; they agree with
  the main repository's quotes in `docs/PRIOR_WORK.md` A3(c) (word for word for the definition, the
  order-4 sentence and the "106 ... 10" sentence). Catches a misquote. Cannot tell whether the
  blueprint itself reports Kisielewicz correctly.
- Searched the whole published report (HTML stripped to text) for "Austin", "nontrivial finite
  model", "no nontrivial finite", "trivial finite models". Catches a definition in the report that
  the blueprint does not have. Cannot catch the term in a figure or in the PDF only.
- All 22 LOOP gates rerun, all exit 0 (nothing they check changed in this run).

## NOT verified

- Kisielewicz 1990 and 1997 and Austin 1965 were not read (Springer and AMS are not fetched; the
  1990 chapter has no known online text). Whether "Austin identity" is defined there for every
  type of algebra or for groupoids only: unknown.
- When the quoted blueprint sentences were written: unknown (shallow clone, one commit). The local
  clone may differ from the blueprint web page; the web page was not fetched.
- Whether the ETP's "order 5 or greater" result has an analogue with a unary operation (the
  shortest type (2,1) law with this property): not searched; possibly our size-3 laws, unknown.
- The comparison with Dudek's identity `(ex)y = x` in the README still rests on slides read by a
  subagent in the main repository (Z. Ernst, 2008), not re-read here.
- No search for the four specific laws, for the collapse of `(x*y)*f(z) = y`, or for the 2,828
  non-implications (still queued).
- Nothing here checks any mathematics: the finite halves stay `hand-argument`, the infinite halves
  `z3-only`.

## Surprises, errors, dead ends

- The published ETP report does not use the term "Austin law" at all; only the blueprint does.
  The main repository's notes cite the blueprint correctly, but a reader looking for the term in
  the report would not find it.
- Mistake: the arXiv page was requested 7 seconds after `robots.txt`, which asks for 15 seconds
  between requests (`Crawl-delay: 15`). The robots file was read in its own step, as the rules ask,
  but the delay was not counted from that first request. One page, read once; no further arXiv
  request was made in this run. Recorded in `docs/LOG.md` with a lesson for the hub.

## Next

The rest of queue item 2, now separate items: the collapse of `(x*y)*f(z) = y`, the four candidate
Austin laws by name and by shape, the scope of Kisielewicz's definition, and the 2,828
non-implications.
