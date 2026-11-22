# 23. Read the HTML full text of arXiv 2609.05690v3 ("Trace-Tree Magmas")

- Date: 2026-11-22
- Status label: literature check (S5 of `docs/shared/VERIFICATION_PROTOCOL.md`) of one lead, now at
  the level of its full text (HTML version). The comparison with our models is a hand reading. No
  label of our nine laws changes.
- Commit(s): see `git log -- steps/23-arxiv-trace-tree-full-text.md`

## In plain words

1. **The question.** A *magma* is a set with one operation `*` that combines two elements into one.
   A *law* is a rule such as `(f(x)*y)*z = y` that must hold for every choice of the letters; a
   structure where it holds is a *model* of the law. Our structures have, besides `*`, a second
   operation `f` that turns one element into another (a *unary* operation; structures with one
   two-input and one one-input operation are said to be of *type (2,1)*). Four of our laws are
   *candidate Austin laws*: they have an infinite model, but (by a hand argument) no finite model
   with two or more elements. In step 17 we read only the summary page of a 2026 paper, arXiv
   2609.05690, which builds infinite models of Austin laws for magmas. This step reads the paper's
   full text and asks: does it mention unary operations or laws like ours anywhere? How do its
   models compare with ours? Does it quote Kisielewicz's definition of "Austin identity" (still
   unknown, step 18)?

2. **What was done, in order.**
   1. **Read arXiv's `robots.txt`** (the file where a site says what programs may fetch) in its own
      request, 21:06:17 UTC. Unchanged since step 17: `/html` is allowed for everyone,
      `Crawl-delay: 15` (15 seconds between requests), `/search` and `/api` are forbidden. No line
      names Claude or Anthropic.
   2. **Waited 20 seconds** (inside the command), then **fetched the full text once**,
      `https://arxiv.org/html/2609.05690v3`, 21:06:43 UTC. Only this one page: no pictures, no PDF,
      no other arXiv page. That makes two arXiv requests in this run.
   3. **Turned the page into plain text** with a small scratch script (formulas kept in their
      LaTeX form) and **read** the introduction, sections 2 and 3 (definitions), 6 (the models
      found), 8 (related work), 9 (limits), the appendix list of laws and the reference list.
   4. **Checked by machine** that every sentence quoted below occurs word for word in the page
      text, and counted words that would show a unary operation of the algebra or laws like ours.
      To show that this check can fail, ran it on a copy where two quotes were damaged and the
      words "unary operation of type (2,1)" were planted: it reported both damaged quotes, counted
      the planted words and exited 1 (a *mutation test*: a deliberately corrupted input that a
      working check must notice). The first try of the mutation was itself wrong (see Surprises).
   5. **Compared the paper's models with our four infinite models** by reading
      `term_models_z3.py` (hand reading, not a machine check).
   6. **Ran all 24 LOOP gates** (the repository's own checks): all exit 0.

3. **A small example.** The paper's elements are trees built from a starting symbol `e`, a
   one-place builder `k(...)` and a pair builder `<a, b>`. Our infinite models use the same three
   builders, called `G`, `F(...)` and `P(a, b)`. In both, a product `a*b` is by default just the
   pair `<a, b>`, and a few rules say when it is something else. Take our model C for
   `(f(x)*y)*z = y`: `f(t)` is `F(t)`, and `u*z` is `b` when `u` has the shape `P(F(t), b)`, else
   `P(u, z)`. Then `f(x)*y = P(F(x), y)` (the exception cannot apply, because `F(x)` is not a pair),
   and `P(F(x), y)*z = y`. The paper's model for its law E7755,
   `x = y*(y*((z*(x*x))*y))`, works the same way with one rule: if the inner part has a certain
   pair shape, the outer product returns `x`. The difference: in the paper, the builder `k` is never
   the value of an operation; it only shows that there are infinitely many elements (`e`, `k(e)`,
   `k(k(e))`, ...). In our models B and C, `f` *is* the builder `F`.

4. **What came out, and what it means.**
   - **Magmas only.** The paper starts: "A magma consists of a carrier and one binary operation."
     Its definition of Austin law is for magmas: "A law $E$ is an Austin law if every finite magma
     satisfying $E$ is trivial and some infinite magma satisfies $E$ ." The word "unary" occurs 5
     times, every time for the tree builder `k` ("a unary constructor", "the unary tower"), never
     for an operation of the algebra. "(2,1)", "function symbol", "term model" and "Dudek" do not
     occur. None of our nine laws and no law with a second operation appears.
   - **Kisielewicz's definition: not quoted.** The paper gives its own definition (above) and only
     says, in its related work: "Austin and Kisielewicz established and analyzed identities with no
     nontrivial finite models", citing Austin 1965 and 1966 and Kisielewicz 1990 and 1997. So
     Kisielewicz's own definition stays unknown.
   - **Two references, read in the paper's list (not the papers):** "A. K. Austin (1965) A note on
     models of identities. Proceedings of the American Mathematical Society 16, pp. 522–523." (the
     paper step 22 found on ams.org) and "A. K. Austin (1966) Finite models for laws in two
     variables. Proceedings of the American Mathematical Society 17, pp. 1410–1412." (new to us).
   - **The models are close relatives of ours (hand reading).** Same kind of carrier (constant,
     one-place builder, pair builder), same default (the free pair), finitely many exceptions. Our
     models B and C, if `f` is read as the builder, are exceptions to the free pair given by one rule
     each. Our models A and D are outside the paper's family: there the product is always the free
     pair and the exception sits in `f` (by default `f(t) = t`); the paper has no second operation
     to put it in. The paper's section 6.4 ("normal-form models": the elements are the trees in
     which no rule applies, and "On normal inputs, multiplication chooses a matching root-rule
     output when one exists and otherwise forms a free pair.") is the closest to the ETP's
     "canonizer" method of step 20. The paper proves each model in Lean 4 ("Judge v3 revision
     380d1b2c, Lean 4.33.1, and Mathlib revision 0df444a3"); our models are checked by z3 and on a
     sample by plain Python only.
   - **A new lead for queue item on canonizers:** the paper says: "A saturated unit-equational
     clause set can sometimes be read as a convergent rewrite presentation of an explicit, possibly
     infinite model." and credits Janota, Rawson and Schulz, "Case study: saturations as explicit
     models in equational theories", arXiv 2602.16324 (2026). Queued (abstract page only first).
   - **The Zenodo lead (queue):** E5093 and E5107 are not among the paper's 32 laws (the strings
     occur 0 times). The paper does not list ETP's 96 candidates, so whether they are among them is
     unknown.
   - It does NOT mean our laws are new, and it does NOT check our models: the comparison is my
     reading. The paper's own claims (28 new Austin classifications, Lean certificates) were not
     checked either.

5. **How a reader can re-check it.** Open `https://arxiv.org/html/2609.05690v3` in a browser. Expect
   section 2.1 with Definition 1 (magmas only), section 3.1 with "a unary constructor", section 8
   with the sentence on Austin and Kisielewicz, and references [1], [2], [15], [17], [18] as quoted
   above. A search of the page for "(2,1)" finds nothing. No script in the repository belongs to this
   step.

## Goal

Queue item 3 (STATE.md before this run): read only `/html/2609.05690v3`, after arXiv's robots.txt
in its own request and 15 seconds from every request; record whether the body mentions unary
operations, other types of algebra, or laws like ours, how its trace-tree magmas compare with our
term models, and whether it quotes Kisielewicz's definition of "Austin identity". Items 1 and 2 wait
for the owner (no Lean, no second prover; `command -v lean lake elan vampire eprover` found nothing
again this run).

## Command(s)

In the session's scratch folder (not the repository):
```
curl -sS -D robots.headers -o robots.txt https://arxiv.org/robots.txt          # 2026-11-22T21:06:17Z
python -c "import time; time.sleep(20)"
curl -sS -D html.headers -o full.html https://arxiv.org/html/2609.05690v3      # 2026-11-22T21:06:43Z
python -I totext.py full.html full.txt          # HTML to text, formulas as their LaTeX alttext
python -I check23.py full.txt                   # exit 0: 12 of 12 quotes found, keyword counts
python -I check23.py full_mut.txt               # exit 1: 2 damaged quotes MISSING, planted '(2,1)' counted
```
Plus all 24 LOOP gates from `LOOP.md` (all exit 0).

## Inputs

- arXiv `robots.txt`: HTTP 200, `last-modified: Mon, 15 May 2023 19:02:53 GMT`, SHA-256
  `eda2bc852443f3f29d31eb04d37b26476654dc33b29256fb882819da23d189a5`.
- Full text page: HTTP 200, 539,362 bytes, SHA-256
  `f8f44da8f0ae51533b292bc4f474732ef34bb1103887697ab6daaf518da6e7c5`, header
  `last-modified: Wed, 23 Sep 2026 00:46:57 GMT`, page line "arXiv:2609.05690v3 [cs.LO] 22 Sep 2026".
  Text made from it: 105,053 characters, SHA-256
  `ad4ff7a05ee06ada64fff3486d4b3eaf1eca37b420508b6d85ac39868f3d20ad`.
- Scratch scripts (not kept): `totext.py` SHA-256
  `ae7c4981d22df9a7f647e4739319fe895d46086e7471bab316ebd479fbfec501`, `check23.py` SHA-256
  `1c961ab49375f2b006aaa3eb01036adbaa6903a34e9aafa60c3559a74fd77d3d`.
- Our `term_models_z3.py` (read only). `curl` (Git for Windows), Python 3.12.10.

## Output

- This step file; README paragraph "Related method" updated (full text read) and step list.
- Keyword counts in the page text: `unary` 5 (all about the builder `k`), `(2,1)` 0, `(2, 1)` 0,
  `signature` 1 ("Despite this minimal signature", about magmas), `function symbol` 0,
  `Kisielewicz` 3, `Dudek` 0, `canoniz` 0, `term model` 0, `free algebra` 0, `E5093` 0,
  `E5107` 0, `variet` 1 (Kisielewicz's 1990 title), `Austin` 49.
- Section headings: 1 Introduction, 2 Problem setting, 3 A search language for infinite tree
  magmas, 4 Proof-producing trace search, 5 Correctness and the Lean trust boundary, 6 Mathematical
  structure of the synthesized models, 7 Evaluation, 8 Related work, 9 Limitations and future work,
  10 Conclusion, Appendix A (the 32 certified Austin identities), References (32 entries).
- Other quotes checked by the script: "The default product is the ordered pair of its arguments.";
  "Failure to find a model proves nothing."; "The finite-model half is the published ETP
  classification: every finite magma satisfying any of these 28 laws is trivial".

## Checks done (and what each one can and cannot catch)

- robots.txt in its own request, then one page 26 seconds later: catches a forbidden path or a too
  early request. Only `/html/2609.05690v3` was fetched.
- Quote check by machine (12 quotes, whitespace collapsed) plus a mutation (two quotes damaged,
  words planted): catches a quote I copied wrongly into this file and a keyword I missed by eye.
  It cannot catch a unary operation described in other words; sections 1, 2, 3, 6, 8, 9, 10, the
  appendix and the references were read in full by eye, 5.2 and 7.4 in part, 4 not at all.
- Two strings were also looked up in the raw HTML (`Austin and Kisielewicz established` 1, `unary`
  5, `Kisielewicz` 3): the text conversion did not invent or lose them.
- The comparison of models: by reading only. It cannot show that our models fit the paper's
  definitions in detail (for example whether a rule with no premises is allowed in its family).

## NOT verified

- Section 4 (search algorithm) was not read; of sections 5 (soundness chain) and 7 (evaluation)
  only 5.2 and part of 7.4 were read. Figures shown as pictures were not fetched.
- Whether our models B and C are members of the paper's "trace-tree" family (a clause with zero
  premises, patterns with `k`): hand reading, not checked against Definition 3.
- The paper's claims: 28 new Austin classifications, 636 accepted certificates, its Lean proofs,
  its comparison with Vampire, E and Twee: not checked.
- Austin 1965 and 1966, Kisielewicz 1990 and 1997: only their entries in this reference list were
  read, not the papers. Where Austin 1966 can be read openly: unknown (queued).
- Janota, Rawson and Schulz, arXiv 2602.16324: only the one sentence about it in this paper (queued).
- Whether E5093 and E5107 are among ETP's 96 order-five candidates: unknown.
- Whether Lean 4.33.1 contains the fix for the kernel bug of `docs/shared/LEAN_CAVEATS.md` C6:
  unknown (the caveats file does not know which stable release has the fix).
- Whether the paper has been peer reviewed: unknown.

## Surprises, errors, dead ends

- The first mutation command stopped on its own safety check: it replaced quotes in the raw text,
  where two of them are split across lines, so `count == 1` failed and no corrupted copy was
  written. The check script then failed only because the file was missing, which is not the failure
  the test is meant to see. Fixed by applying the mutation to the whitespace-collapsed text, the
  same form the check reads. Lesson for the hub in `docs/LOG.md`.
- The abstract in the HTML full text is worded differently from the abstract on the `/abs` page that
  step 17 quoted (for example "a finitely presented class of total operations" and "while finitely
  many positive Horn clauses define exceptional outputs", against step 17's "finitely presented
  total operations" and "; finitely many positive Horn clauses define exceptions"). Both are v3.
  The README keeps step 17's quote and says it is from the `/abs` page.
- Surprise: the paper uses the same three tree builders as our models (constant, one-place, pair),
  but its one-place builder is never an operation value. Our type (2,1) laws make use of it.

## Next

Queue: the GitHub README of `YanbiaoLab/trace-tree-magmas` (unchanged), the Zenodo preprint, and
two new items: the abstract page of arXiv 2602.16324 (Janota, Rawson, Schulz), and an open copy of
Austin 1966 looked up in OpenAlex.
