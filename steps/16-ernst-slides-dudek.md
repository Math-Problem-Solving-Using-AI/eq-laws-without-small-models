# 16. Re-read the Ernst slides on Dudek's identity `(e*x)*y = x`

- Date: 2026-11-22
- Status label: literature check (S5 of `docs/shared/VERIFICATION_PROTOCOL.md`) of one cited
  source: the quote in the README is now read from the primary file (before: read only by a
  subagent in the main repository). The slides' infinite model is checked on a sample by plain
  Python; "no model with 2 to 6 elements" is a finite search. No label of our nine laws changes.
- Commit(s): see `git log -- steps/16-ernst-slides-dudek.md dudek_slides_check.py`

## In plain words

1. **The question.** A *magma* is a set with one operation `*` that combines two elements. A *law*
   (or *identity*) is a rule such as `(e*x)*y = x` that must hold for every choice of the letters
   `x` and `y`; here `e` is a *constant*, one fixed element named in advance. A structure where the
   law holds is a *model* of it. Our README cites slides by Zachary Ernst (2008) for this: "Dudek's
   identity `(e*x)*y = x` has models with more than one element, but all of them are infinite".
   That quote came from a helper program (a *subagent*) in the main repository, and nobody here had
   read the slides. Do the slides really say that?

2. **What was done, in order.**
   1. **Found the address** in the main repository's `docs/PRIOR_WORK.md`:
      `https://www.cs.unm.edu/~veroff/ADAM/2008/ernst08.pdf`.
   2. **Read the site's `robots.txt`** (the file where a web site says what programs may fetch) in
      its own request, 2026-11-22 20:21:37 UTC. It allows everything except `/cgi-bin/` for all
      programs and gives no waiting time. We still waited 15 seconds before the next request.
   3. **Downloaded the slides** (one request, 2026-11-22 20:21:59 UTC) and turned them into text
      with `pdftotext`. The text lost some symbols (the sign `≠`, small raised numbers), so the
      one unclear line was decoded from the file's own font table (item 4 below).
   4. **Wrote `dudek_slides_check.py`**, a small plain-Python program (no automatic prover), to
      check that we read the slides' formulas right: their infinite model must satisfy the law,
      and no small table may satisfy it.
   5. **Mutation test** (a *mutation* is a deliberately corrupted input; a checker that accepts it
      is useless): 7 corrupted variants, all rejected, each for the intended reason (printed).
      A corrupted input also makes the program exit with code 1 (tested twice).

3. **A small example.** Why can a finite table not work? Take any 2-element table on `{0, 1}` with
   `e = 0`. The law says `(e*x)*y = x`. If `e*0` and `e*1` were the same element `a`, then `a*y`
   would have to be both `0` and `1`, impossible. So `e*0` and `e*1` are different, and every
   element is `e*x` for some `x`. Then each row of the table is constant: row `e*x` is all `x`. Now
   row `e` is constant too, so `e*0 = e*1`, which we just ruled out. Our program tries all 2-element
   and 3-element tables (and, using the rule "row `e*x` is constant `x`", all tables up to 6
   elements) and finds none. In the slides' infinite model, on the numbers `0, 1, 2, ...`, with
   `e = 3`: `3*x = 2^x`, and `(2^x)*y = x`, so `(3*x)*y = x`. For example `(3*2)*7 = 4*7 = 2`.

4. **What came out, and what it means.**
   - **The quote is right.** Slide "Dudek's Algebra (1)" says, word for word: "Dudek's algebra D
     has the identity: (ex)y = x. Although this system has non-trivial models, they are all
     infinite." Slide "Dudek's Algebra (2)" gives the model `x*y = 2^y if x = 3`, `x*y = i if
     x = 2^i for some i`, `x*y = x otherwise`, `e = 3`, and ends "It is a model: (ex)y = (3x)y =
     2^x y = x".
   - **Our reading of the model is right on a sample**: the law holds for all `x, y` below 40, and
     `e, e*e, e*(e*e), e*(e*(e*e))` are `3, 8, 256, 2^256`, all different, as the slides' argument
     needs. For all numbers it follows by the one-line computation above (a hand argument, checked
     by reading).
   - **A small slip in the slides, or in our reading.** The slides write `ee = 2^5` and
     `e(ee) = 2^(2^5)` (the raised number is the character `5` of the font CMSS8 in the PDF's font
     table; we could not render the page as a picture). By the slides' own table `ee = 3*3 = 2^3 = 8`.
     So either the slide has a typo or our decoding of the raised number is wrong. This does not
     touch the main claim.
   - **The slides give no reference for Dudek**: no paper, no year, no first name. Which Dudek and
     which paper: unknown (queued).
   - It does NOT mean anything new about our nine laws. It confirms one source for the README's
     remark that a short law with an extra symbol (here a constant, in our laws the operation `f`)
     can have only infinite models with more than one element.
   - "No model with 2 to 6 elements" is a finite search, not a proof for all sizes. The slides'
     own argument for all finite sizes (pairs `e_n`, `e_m` with `n ≠ m`) was read but its symbols
     were partly lost in the text; it is not machine-checked here.

5. **How a reader can re-check it.**
   ```
   python dudek_slides_check.py             # "... 2**256, pairwise different", sizes 1 to 6, then "ALL PASS: ..."
   python dudek_slides_check.py --selftest  # "selftest: 7 of 7 corrupted inputs rejected", ALL PASS
   ```
   The slides: `https://www.cs.unm.edu/~veroff/ADAM/2008/ernst08.pdf` (SHA-256 below), slides 5
   and 6.

## Goal

Queue item 2 (STATE.md before this run): find the Ernst slides' address, read the site's
robots.txt in its own step, read the slides and quote what they say about Dudek's `(ex)y = x`,
with date.

## Command(s)

```
curl -sS -D robots.headers -o robots.txt https://www.cs.unm.edu/robots.txt        # 2026-11-22T20:21:37Z
python -c "import time; time.sleep(15)"
curl -sS -D pdf.headers -o ernst08.pdf https://www.cs.unm.edu/~veroff/ADAM/2008/ernst08.pdf   # 2026-11-22T20:21:59Z
pdftotext -layout ernst08.pdf ernst08.txt
pdftotext -enc UTF-8 -f 5 -l 6 -raw ernst08.pdf p56.txt
python -I <scratch script>  # lists text pieces with font and size from the page's content stream, and the font object /F14.0
python dudek_slides_check.py
python dudek_slides_check.py --selftest
python -c "import dudek_slides_check as d; d.check_infinite.__defaults__ = (d.slides_op, 2, 40); d.main()"   # exit 1
python -c "import dudek_slides_check as d; d.check_finite.__defaults__ = (3, 6, lambda op, e, x, y: op(op(e, x), y) == y, d.forced_models); d.main()"   # exit 1
```
The downloads were kept in the session's scratch folder, not in the repository. Plus all 22 LOOP
gates (all exit 0; none of their inputs changed).

## Inputs

- `robots.txt` of `www.cs.unm.edu`: HTTP 200, `Last-Modified: Fri, 04 Sep 2026 17:01:25 GMT`,
  250 bytes. Content for `User-agent: *`: `Disallow:` (empty) and `Disallow: /cgi-bin/`; five named
  crawlers are disallowed everywhere; no `Crawl-delay`.
- `ernst08.pdf`: HTTP 200, `Last-Modified: Fri, 01 Aug 2008 15:55:21 GMT`, 406,620 bytes, SHA-256
  `23bf7d768aee5beed1cffc4218edb3be47ef633a647ace5cc7305110bf470e6f`, PDF 1.3. Title slide:
  "Syntax of the Finite Model Property", Zachary Ernst, University of Missouri-Columbia, July 23,
  2008. 16 slide titles in the text (title, Preliminaries, An Example (from last year), Makinson's
  Modal Logic, Dudek's Algebra (1) and (2), UCTA Evaluation, Example Evaluation (1) to (5), Limits
  of UCTA (1) and (2), Questions).
- `pdftotext` 4.00 (Glyph & Cog, Git for Windows), Python 3.12.10, `curl`.

## Output

- New script `dudek_slides_check.py` (with `--selftest`). Not a LOOP gate and not in CI, like the
  other literature-check scripts (`etp_specializations*.py`): it checks our reading of a source,
  not a result of ours.
- Quotes (slide 5, "Dudek's Algebra (1)"), word for word from the text extraction: "Dudek's algebra
  D has the identity: (ex)y = x. Although this system has non-trivial models, they are all
  infinite." "So any non-trivial model has to map each ei onto a different element of its domain."
  (`ei` is `e` with a lowered `i`; `e_n` is `e(e(...e(ee)...))` with `n` letters `e`, "n times".)
- Slide 6, "Dudek's Algebra (2)": the table quoted in "In plain words" item 4. Raised and lowered
  symbols lost in the text were read from the content stream: in `ee = 2^5` the raised `5` is
  character code 53 of font `/F14.0` = `BPCQFJ+CMSS8`, `/Encoding /MacRomanEncoding`,
  `/FirstChar 50 /LastChar 53` (the digits 2 to 5).
- `dudek_slides_check.py` output: law holds for all `x, y < 40`; chain `3, 8, 256, 2^256`; models of
  size 1: 1 (both searches); sizes 2 and 3 (every table): 0; sizes 2 to 6 (row search): 0; the row
  search looked at `n * n!` rows of `e` per size, as it should.

## Checks done (and what each one can and cannot catch)

- Law check of the slides' model for all `x, y < 40`: catches a misread case of the table or a
  wrong `e`. It cannot cover all numbers; that part is the hand computation `(3*x)*y = (2^x)*y = x`.
  The case "x otherwise" is never used by the law (`3*x` is always a power of 2), so a misread
  value there would not be caught; it also does not matter.
- Chain `e, e*e, ...` pairwise different: catches a model where the chain repeats.
- Sizes 2 and 3 by trying every table and every `e` (no reasoning used): catches a misread law
  that has small models.
- Sizes 2 to 6 by the row search: uses the rule "row `e*x` is constant `x`", read off the law;
  every table it builds is re-checked by plain evaluation, and the number of rows of `e` it tried
  must be `n * n!` (every constant `e` times every one-to-one row).
- 7 mutations, each rejected for the intended reason (printed): `e = 2`; row 3 changed to
  `2^y + 1`; row `2^i` changed to `i + 1`; `e*e = e` with the law test skipped (caught by the chain
  test); the law `(e*x)*y = y` (finite models exist, caught by the full search at size 2); the row
  search without its conflict test (caught by the re-check of built tables); a row search that
  skips sizes 2 and up (caught by the row count). Two exit-code tests (wrong `e`, wrong law): exit 1.

## NOT verified

- The slides were not seen as pictures (no PDF renderer on this machine: `pdftoppm` and Python PDF
  libraries are missing). The `≠` signs, raised and lowered symbols were reconstructed from the
  text and the font table; the `ee = 2^5` reading in particular is unconfirmed.
- The slide "Makinson's Modal Logic" gave no text (probably a picture): what it says is unknown.
- Dudek's original paper: which Dudek, which paper, which year, what it proves: unknown. The slides
  give no reference.
- The slides' argument that every finite model has one element (via `e_n = e_m` forcing `ee = e`)
  was not checked step by step; our own one-paragraph argument (example above) is a hand argument.
- "No model with 2 to 6 elements" is a finite search; it says nothing about size 7 and up on its
  own.
- That the slides are the right source for the main repository's citation (same file, same
  address): yes by address; whether the subagent read the same version: unknown, but the file's
  `Last-Modified` date is 2008-08-01.

## Surprises, errors, dead ends

- `pdftotext -bbox` (positions of words) does not exist in this `pdftotext` (Glyph & Cog 4.00, not
  Poppler). Dead end; used a small scratch script that lists the text pieces of the page's content
  stream with font name and size instead.
- A first scratch script written through a shell here-document lost a backslash (`b'\\'` became
  `b'\'`) and did not run. Written with the file tool instead.
- First selftest draft had a mutation ("row search that keeps only size 1") that could never be
  rejected: a search that finds nothing looks the same as a correct search, because the correct
  answer is "nothing". Fixed by making the row search count the rows it tried (`n * n!`).
- In the first selftest run two mutations were rejected for the wrong reason: `e*e = e` was caught
  by the law test, not the chain test, and the search without its conflict test was caught by the
  row count, not by the re-check of built tables. Fixed (law test skipped for the first, checks
  reordered for the second) and re-run: each is now caught by its own check.
- Surprise: the slides seem to have a slip (`ee = 2^5` where their table gives `2^3`), or our
  decoding is wrong.

## Next

Queue: read the arXiv abstract page of 2609.05690 (after arXiv's robots.txt and its crawl delay);
find Dudek's primary source (new item).
