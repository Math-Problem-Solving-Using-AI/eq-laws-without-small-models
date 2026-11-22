# 17. Read the arXiv abstract page of 2609.05690 ("Trace-Tree Magmas")

- Date: 2026-11-22
- Status label: literature check (S5 of `docs/shared/VERIFICATION_PROTOCOL.md`) of one lead, at
  the level of its abstract page only. No label of our nine laws changes.
- Commit(s): see `git log -- steps/17-arxiv-trace-tree-magmas.md`

## In plain words

1. **The question.** A *magma* is a set with one operation `*` that combines two elements. A *law*
   is a rule such as `f(x*(y*z)) = y` that must hold for every choice of the letters; a structure
   where it holds is a *model*. Four of our laws use, besides `*`, a second operation `f` that
   takes one element (a *unary* operation; algebras with one two-place and one one-place operation
   are said to be of *type (2,1)*). We think these four laws are *Austin laws*: they have models
   with more than one element, but only infinite ones. In step 15 a web search showed a 2026 paper,
   arXiv 2609.05690, "Trace-Tree Magmas: Proof-Producing Infinite Countermodels and 28 New
   Order-Five Austin Classifications", but we had seen only a search result line. Does its own
   summary page talk about unary operations, type (2,1), or laws shaped like ours?

2. **What was done, in order.**
   1. **Read arXiv's `robots.txt`** (the file where a site says what programs may fetch) in its own
      request, 2026-11-22 20:27:56 UTC. It allows `/abs` for all programs, asks for
      `Crawl-delay: 15` (15 seconds between requests), and forbids `/search`, `/api` and others.
   2. **Waited 20 seconds** (counted from the robots.txt request; the run 9 mistake was to count
      from the wrong moment), then **fetched the abstract page** `https://arxiv.org/abs/2609.05690`
      once, 2026-11-22 20:28:25 UTC. Nothing else was requested from arXiv: not the PDF, not the
      HTML full text.
   3. **Took the title, authors, dates, subjects and abstract** out of the page with a small
      scratch script (the page itself was kept in the session's scratch folder, not in the
      repository).
   4. **Searched the abstract and the whole page by machine** for words that would show a unary
      operation or our law shapes (`unary`, `(2,1)`, `type`, `signature`, `constant`,
      `function symbol`, `f(`, `x*`, `groupoid`). To test that this search can find something, ran
      it once more on a copy of the page where the word "unary" had been put in by hand: it then
      reported it (a *mutation test*, a deliberately corrupted input that a working check must
      notice).
   5. **Compared the paper's model family**, as the abstract describes it, with our own infinite
      models of steps 06 and 07, by reading `term_models_z3.py`.

3. **A small example.** Our infinite model for `(f(x)*y)*z = y` (step 06) has as elements all
   formal expressions built from one starting symbol `G`, a formal `F(t)` and a formal pair
   `P(a, b)`. By default `u*z` is just the pair `P(u, z)`; the one exception is: if `u` is the pair
   `P(F(t), y)`, then `u*z = y`. So `(f(x)*y)*z = P(F(x), y)*z = y`, which is the law. The paper's
   abstract describes its magmas the same way: elements are trees built by constructors, "The
   default product pairs its arguments; finitely many positive Horn clauses define exceptions"
   (a *Horn clause* here is a rule of the form "if the arguments have this shape, the product is
   that").

4. **What came out, and what it means.**
   - **The page, quoted** (version v3, "Submitted on 4 Sep 2026 (v1), last revised 22 Sep 2026
     (this version, v3)"): authors Jiaming Zhao, Bing Wu, Tong Yang, Xu Miao (Yanbiao Lab,
     DataCanvas Co., Ltd., Beijing; Peking University). Subjects "Logic in Computer Science
     (cs.LO); Logic (math.LO)". Comments: "34 pages, 2 figures, 7 tables. Code and reproducibility
     artifacts:" with a link to `github.com/YanbiaoLab/trace-tree-magmas`.
   - **Abstract, first sentences, word for word:** "Finite model finders cannot witness an Austin
     law: an identity whose finite models are all trivial but which has a nontrivial infinite
     model. We introduce rank-decreasing sparse trace-tree magmas, finitely presented total
     operations on a countably infinite constructor-tree carrier. The default product pairs its
     arguments; finitely many positive Horn clauses define exceptions." Further on: "it proves
     functionality of the exceptional relation by descent on constructor size, proves the
     identity by exhaustive symbolic case analysis, and emits a self-contained Lean 4 certificate."
     And: "On ETP's 96 order-five Austin candidates, we discover and Lean-verify infinite
     countermodels for 28 identities with no prior public classification in our audit."
   - **Answer to the question: no.** The abstract speaks of magmas and identities only. None of
     the words `unary`, `(2,1)`, `type`, `signature`, `constant`, `function symbol`, nor the
     shapes `f(` or `x*`, occurs in the abstract; `unary`, `(2,1)` and `signature` occur nowhere
     on the page. So, as far as the summary page goes, the paper is about one operation `*`, not
     about type (2,1), and it does not mention our four laws.
   - **A close relative in method.** The paper's model family (constructor trees, pairing by
     default, finitely many exceptions) has the same shape as our term models of steps 06 and 07,
     and it adds what we lack: a proof of each model in Lean 4. Its definition of "Austin law"
     agrees with the ETP blueprint's (step 13). This makes the paper a useful lead for the blocked
     Lean item (queue item 1), not a source of our results: our models were built in steps 06 and
     07 without reading it.
   - It does NOT mean the body of the paper says nothing about unary operations: only the
     abstract page was read. It does NOT mean our laws are new, and it does not change any label.

5. **How a reader can re-check it.** Open `https://arxiv.org/abs/2609.05690` (or `.../2609.05690v3`)
   in a browser and read the abstract. Expect the title and the sentences quoted above, and no
   mention of a unary operation. There is no script in the repository for this step.

## Goal

Queue item 2 (STATE.md before this run): read the arXiv abstract page of 2609.05690, only `/abs`,
after arXiv's robots.txt and 15 seconds from every request; record whether it mentions unary
operations, type (2,1), or the shapes of our four laws.

## Command(s)

Run in the session's scratch folder (not the repository):
```
curl -sS -D robots.headers -o robots.txt https://arxiv.org/robots.txt          # 2026-11-22T20:27:56Z
python -c "import time; time.sleep(20)"
curl -sS -D abs.headers -o abs.html https://arxiv.org/abs/2609.05690           # 2026-11-22T20:28:25Z
grep -o '<meta name="citation_[a-z_]*" content="[^"]*"' abs.html
python -I <scratch script>   # title, authors, abstract, dateline, comments, subjects, history, MSC
python -I kw.py abs.html     # keyword counts in the abstract and the whole page
sed 's/finitely presented total operations/finitely presented total unary operations/' abs.html > abs_mut.html
python -I kw.py abs_mut.html # mutation: must report 'unary' once in the abstract
```
Plus all 22 LOOP gates (all exit 0; no input of theirs changed).

## Inputs

- `robots.txt` of `arxiv.org`: HTTP 200, `last-modified: Mon, 15 May 2023 19:02:53 GMT`, 5,854
  bytes. For `User-agent: *`: `Crawl-delay: 15`, `Allow: /abs`, `Allow: /pdf`, `Allow: /html`,
  `Disallow: /search`, `Disallow: /api` and others.
- Abstract page: HTTP 200, 44,211 bytes, SHA-256
  `826f442a98ca5d9e0fe5a203f7fe2b9d76d350d22b74d957d9080f531f8066ac`, version v3. Meta tags:
  `citation_date` 2026/09/04, `citation_online_date` 2026/09/22. Submission history: v1 Fri,
  4 Sep 2026 19:58:40 UTC; v2 Mon, 21 Sep 2026 13:05:27 UTC; v3 Tue, 22 Sep 2026 10:55:59 UTC
  (55 KB each). MSC classes: "68V15 (Primary) 08B05, 03B35, 03C05 (Secondary)". DOI
  `10.48550/arXiv.2609.05690`. The page links an HTML full text, `/html/2609.05690v3`.
- `curl` (Git for Windows), Python 3.12.10; our `term_models_z3.py` (read only).

## Output

- This step file, a README paragraph (section "Leads from hand analysis") and the README step list
  (steps 16 and 17 added; 16 was missing there).
- Keyword counts in the abstract: `unary` 0, `(2,1)` 0, `(2, 1)` 0, `type` 0, `signature` 0,
  `constant` 0, `function symbol` 0, `f(` 0, `x*` 0, `x⋄` 0, `groupoid` 0; `operation` 1,
  `magma` 1, `Austin` 3, `Lean` 4, `ETP` 1, `order-five` 1. Whole page: `unary`, `(2,1)`,
  `(2, 1)`, `signature` together 0.
- Mutated copy: `unary` 1 in the abstract (3 on the whole page, because the sentence also stands in
  two meta tags). The search can see the word when it is there.

## Checks done (and what each one can and cannot catch)

- robots.txt read in its own request, page fetched 29 seconds later (headers: 20:27:58 and the
  fetch at 20:28:25 UTC): catches a request to a disallowed path or too soon. Only `/abs` was
  requested.
- Keyword search by machine plus one mutation: catches a mention I missed by reading. It cannot
  catch a unary operation described in other words (for example "a function `g`"); the abstract
  was also read in full by eye, and it describes only "the default product" and identities.
- Comparison of the model family with `term_models_z3.py`: by reading only. It can show that the
  shapes agree at the level of the abstract's words; it cannot show that the paper's definitions
  (rank-decreasing, sparse, least fixed point) match ours in detail.

## NOT verified

- The body of the paper (PDF or HTML full text) was not read: whether it treats unary operations,
  other types of algebra, or laws like ours anywhere: unknown (queued).
- The claims of the abstract (28 new Austin classifications, Lean certificates, 636 certificates
  accepted by "Judge v3", the comparison with Vampire, E and Twee) were not checked.
- The code repository `github.com/YanbiaoLab/trace-tree-magmas` was not opened: its contents,
  license, and whether its Lean certificates could serve as a template for our blocked Lean item:
  unknown (queued).
- Whether our 22 magma special cases (step 15) are among "ETP's 96 order-five Austin candidates":
  not checked against the paper's list. Step 15 checked them against the blueprint's 130 order-5
  equations (none is there), and all 22 force one element, so they should not be Austin
  candidates; the paper's list itself was not seen.
- Whether the paper is peer reviewed: unknown (arXiv preprint, no journal reference on the page).

## Surprises, errors, dead ends

- The first run of the keyword script crashed printing the symbol `⋄` on the Windows console
  (`UnicodeEncodeError: 'charmap' codec can't encode character '⋄'`). Fixed by printing the
  keys with `ascii()`; counts unchanged in meaning (the crash happened before any count was used).
- Surprise: the paper's model family is the same shape as ours (pairs by default, few exceptions),
  found by the authors for magmas; ours were found independently for type (2,1) in steps 06 and 07.

## Next

Queue: read the HTML full text of 2609.05690v3 (only `/html`, 15 seconds apart) for unary
operations and how its models compare with ours; read the README of
`github.com/YanbiaoLab/trace-tree-magmas` with `gh api`. Before those: Kisielewicz's definition and
Dudek's source (older queue items).
