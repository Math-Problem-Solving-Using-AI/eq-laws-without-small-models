# 22. Title search in OpenAlex for the two collapsing laws and the four candidate Austin laws

- Date: 2026-11-22
- Status label: literature check (S5 of `docs/shared/VERIFICATION_PROTOCOL.md`), shallow: titles
  only, one open index. For the two collapsing laws and the four candidate Austin laws: "not found
  in searches" (queries, times and fingerprints below). No mathematical label changes.
- Commit(s): see `git log -- steps/22-openalex-title-search.md`

## In plain words

1. **The question.** Our structures have two operations: `*`, which combines two elements into
   one, and `f`, which turns one element into another (mathematicians call this "type (2,1)": one
   operation with two inputs, one with one input). A *law* is a rule such as `(x*y)*f(z) = y` that
   must hold for every choice of the letters. Two of our laws *collapse*: they force every
   structure that obeys them to have a single element (`(x*y)*f(z) = y` and `f(x)*(y*z) = y`). Four
   others are *candidate Austin laws*: they have an infinite structure that obeys them, but, by a
   hand argument, no finite one with two or more elements. Has anyone published papers about these
   laws? Earlier searches (steps 14, 15) used only web search and GitHub. This step searches the
   titles in one open index of research papers.

2. **What was done, in order.**
   1. **Checked first whether queue item 2 could go ahead.** It asks for a second proof checker
      (Lean or another prover) for the two collapse proofs. Looked for 16 prover programs on this
      machine (`lean`, `lake`, `elan`, `vampire`, `eprover`, `prover9`, `mace4`, `twee`, `maude`,
      `coqc`, `isabelle`, `cvc5`, `cvc4`, `yices`, `metis`, `waldmeister`) and at the installed
      Python packages (`numpy`, `PyYAML`, `z3-solver`, `pip`): none is there except z3, which
      already checks these proofs. Installing one needs the owner, so item 2 went to "Blocked" and
      this run took item 3.
   2. **Read OpenAlex's robots.txt** in its own request. *OpenAlex* is a free, open index of
      research papers (titles, authors, years, links). A *robots.txt* is the file where a site
      says what programs may fetch. It says `User-agent: *` / `Allow: /` (everyone may fetch
      everything). Waited 10 seconds before the first search and between all requests (the wait
      was inside the command).
   3. **Eight searches** (q1 to q8, 25 results each): title words "identities of type (2,1)",
      "algebras of type (2,1)", "groupoids with a unary operation" (a *groupoid* is an old name
      for a structure with one two-input operation); two free-text searches with words like
      "forces one-element trivial algebra" and "infinite model no finite model"; and three
      *control* searches whose answer we already knew: "Austin identities" (must find
      Kisielewicz 1997), "Austin's groupoids" (must find Cho and Dudek 2006), "models of identities"
      (must find Dudek 1988). A control shows that the search works; without it, "nothing found"
      could just mean the search never ran.
   4. **Six more requests** (r1 to r6): shorter title words, because the first title searches gave 0
      results ("type (2,1)", 50 results; "unary operation identities"; "groupoids unary"), and the
      index records of three titles that looked relevant.
   5. **A small scratch script with a mutation test** (a *mutation* is a deliberately damaged input;
      a working check must notice it). It confirms the three control papers are in the saved
      results and lists every title containing "unary", "type (2,1)", "one-element", "trivial",
      "f(x", "collaps", "austin identit" or "austin's groupoid". Every one of the 16 titles it
      lists was read by hand. With one control removed and one made-up title planted, it printed
      "FAIL" and exited 1.
   6. **Ran all 24 LOOP gates** (the repository's own checks): all exit 0.

3. **A small example of what was looked for.** The law `(x*y)*f(z) = y` collapses in three lines
   (README): put `x = a*b` and `y = f(c)` to get `b*f(d) = f(c)` for all `b`, `c`, `d`; then
   `(a*b)*f(d)` is both `b` (the law) and `f(c)` (the line before), so every `b` equals `f(c)`, and
   any two elements are equal. A paper on this law would most likely say "identity", "unary
   operation", "type (2,1)" or "trivial" (one-element) in its title, so those were the search words.
   No title in the results was about a law of this shape.

4. **What came out, and what it means.**
   - **Not found:** no title in 155 results is about the two collapsing laws or the four
     candidate Austin laws, or about laws of type (2,1) that force one element.
   - **Controls worked:** the three known papers were found (Kisielewicz, "Austin identities",
     1997; Cho and Dudek, "A note on the Austin's groupoids", 2006; Dudek, "A note on models of
     identities", 1988). So the search itself works.
   - **New leads, not read:**
     - "Seeded infinite models of the Austin identities E5093 and E5107", Jason Peng, 2026, a
       preprint on Zenodo, `doi:10.5281/zenodo.24340685` (OpenAlex W7236434571). By its title it
       is about two magma laws of the ETP (the Equational Theories Project numbers laws as
       `E` plus a number), not about `f`. Queued.
     - A. K. Austin, "A Note on Models of Identities", Proc. AMS 1965 (W1974536096), and S. K.
       Stein, "Finite Models of Identities", Proc. AMS 1963 (W1994863171). OpenAlex marks both as
       free to read, but only on ams.org, which this loop does not fetch. Austin 1965 is likely the
       paper that gave Austin laws their name (our guess from the title, author and year; not read).
   - It does NOT mean the laws are new. Only titles were seen, in one index, 25 or 50 results per
     search. No abstract, no review (zbMATH is blocked for the loop), no book was read.
   - It does NOT change any label. The collapses stay `z3-only` plus our own checker, the four
     candidate Austin laws stay `hand-argument` (finite part) and `z3-only` (infinite part).

5. **How a reader can re-check it.**
   ```
   curl -s -G https://api.openalex.org/works --data-urlencode "filter=title.search:Austin identities" --data-urlencode "per-page=25" --data-urlencode "select=id,display_name,publication_year"
   curl -s https://api.openalex.org/works/W7236434571
   ```
   The first lists "Austin identities" (1997) first and the 2026 Zenodo preprint second (as seen on
   2026-11-22; an index changes over time). The second shows the preprint's record (author, DOI).

## Goal

Queue item 3 (STATE.md before this run): search an open index that allows our agent (OpenAlex) by
title words for the two collapses, and for the four candidate Austin laws; record queries, dates and
what could not be read. Items 1 and 2 wait for the owner (no Lean, no second prover installed).

## Command(s)

Tool check (no network):
```
pip list                                   # numpy 2.5.5, pip 25.0.1, PyYAML 6.0.4, z3-solver 5.4.1.0
command -v lean lake elan vampire eprover prover9 mace4 twee maude coqc isabelle cvc5 cvc4 yices metis waldmeister   # none found
```
Network, 2026-11-22, times UTC, every request 10 s or more after the one before (sleep in the
command); `per-page=25` and `select=id,display_name,publication_year,doi,open_access` for q1 to q8:
```
curl https://api.openalex.org/robots.txt                         # 20:59:03, 200, "User-agent: * / Allow: /"
q1 filter=title.search:identities of type (2,1)                  # 20:59:24, 200, count 0
q2 filter=title.search:algebras of type (2,1)                    # 20:59:34, 200, count 2
q3 filter=title.search:groupoids with a unary operation          # 20:59:44, 200, count 0
q4 search=identity binary and unary operation forces one-element trivial algebra   # 20:59:55, 200, count 1,185
q5 search=nontrivial model identity groupoid unary operation infinite model no finite model   # 21:00:06, 200, count 171
q6 filter=title.search:Austin identities                          # 21:00:16, 200, count 100 (control)
q7 filter=title.search:Austin's groupoids                         # 21:00:27, 200, count 1 (control)
q8 filter=title.search:models of identities                       # 21:00:38, 200, count 7,010 (control)
r1 filter=title.search:type (2,1), per-page=50                    # 21:01:17, 200, count 96
r2 filter=title.search:unary operation identities, per-page=50    # 21:01:34, 200, count 0
r3 filter=title.search:groupoids unary, per-page=50               # 21:01:44, 200, count 2
r4 works/W7236434571 (authorships, locations)                     # 21:01:55, 200
r5 works/W1974536096                                              # 21:02:05, 200
r6 works/W1994863171                                              # 21:02:16, 200
```
Scratch check (session scratch folder, not the repository; script SHA-256
`67c0a84f7bf1fb65034ae0c4504aaef0dcb47ed8aa907ceff7dc4ebeed926e75`):
```
python -I scan22.py <OpenAlex results>          # exit 0: 3 controls found, 155 titles, 16 hits, all read by hand
python -I scan22.py <OpenAlex results> mutate   # exit 1: control "Cho-Dudek 2006" MISSING, planted title flagged
```
Plus all 24 LOOP gates (all exit 0).

## Inputs

- OpenAlex result files, SHA-256 (the files were scratch and are not kept):
  q1 `e8ecf1abf3cde116e6c8528b58cdc7824edbf6f02fc56dc062b12f0313b775c2`,
  q2 `32720e76361bb01ddee9b22e6b278ffb55e7fa89544f07495df7b9450615c190`,
  q3 `4b0482eb0a2384676e373a8df7fd96ccf3ca062deaed6ca2048f95e257ef5f92`,
  q4 `5c77b7a5ab9b7b651a5251e67be63d8fa793356be4608a629280d51cdce86ab5`,
  q5 `eda2f9bfe625a00bec51f30d32a6d00b10b5eb47bfcfe43c5cebe1b2843971bc`,
  q6 `c95e86c8e3ac9c9c993a1c4e482473b8bbe4775d106fab1277cc9128e7ac24d0`,
  q7 `599eee84a3112e5417d6edbf2ffe0b84f293da92d20572deed2ddc1a48c5f317`,
  q8 `bb5eb2b51ccf3c7caf0a8855ebd805695879080a9e58bdb7f1cbb0886380bb2f`,
  r1 `508d6ab4c7efe2438d0d1e666634208933739de33a4479dc5c229ba5727be019`,
  r2 `7694fec69482059d2f98133dfafb600ab8659faf18467dac100799fce4161f57`,
  r3 `c3204d3a962bdb24100e641c2d9215d0357eb52387471058ea7f11b13d18624e`,
  r4 `33ad1c167844bf4c6eac4be7d5521c2d941a9e8c82ba5d267dfdfc855a618d82`,
  r5 `3486c7b1f7d803d524a5d369e55f268c3dd7181e76f01f47084aab2cc4bb0a04`,
  r6 `10229bf684cb773dd3b10b42ca9325234f3310dcf384c6aa29244f658cbbf98a`.
- Records read (OpenAlex metadata, quoted):
  - r4: "Seeded infinite models of the Austin identities E5093 and E5107", 2026, type `preprint`,
    author "Jason Peng", DOI `https://doi.org/10.5281/zenodo.24340685`, source "Zenodo (CERN
    European Organization for Nuclear Research)", `oa_status` "green".
  - r5: "A Note on Models of Identities", 1965, author "A. K. Austin", "Proceedings of the American
    Mathematical Society", DOI `10.1090/s0002-9939-1965-0174649-7`, `oa_status` "bronze", PDF on
    `www.ams.org` (not fetched).
  - r6: "Finite Models of Identities", 1963, author "Sherman K. Stein", same journal, DOI
    `10.1090/s0002-9939-1963-0144995-x`, `oa_status` "bronze", PDF on `www.ams.org` (not fetched).
- Hits listed by the scratch scan and read by hand. On topic or leads: W4243732956 "Austin
  identities" (1997, control), W120008873 "A NOTE ON THE AUSTIN'S GROUPOIDS" (2006, control),
  W7236434571 (above), W2901291365 "The Order of Hypersubstitutions of Type (2,1)" (2011, already
  seen in step 20, about hypersubstitutions by title), W3036815777 "On the complexity of the lattices
  of subvarieties and congruences. II. Differential groupoids and unary algebras" (2020),
  W4250477728 "The Residual Character of Finitely Generated Varieties of Unary Algebras and
  Groupoids, and Applications to t..." (2012; title cut by our script). Neither of the last two is
  about our laws by title (they treat whole classes of structures, not single laws). Unrelated
  (chemistry, permutations, geometry, history, cryptography): W1520471804, W1974816166, W1987129084,
  W2001346827, W2033378011, W2248325483, W2891385154, W2963865898, W3025205802, W4393977744.
  W2148692680 (Dudek 1988, control) was found by its id, not by a keyword.
- `curl` 7.79.1 (Git for Windows), Python 3.12.10.

## Output

- This step file; one README sentence (literature status of the two collapses and the four
  candidate Austin laws) and the README step list. No code, results or certificates changed.

## Checks done (and what each one can and cannot catch)

- Three control searches found the three known papers. Catches a search that silently returns
  nothing or a broken filter. Cannot show that the index holds every paper (books and many old
  papers are missing or have no title words we used).
- Scratch scan with a mutation (one control removed, one title planted): exit 1 with the two
  intended messages. Catches a lost control and a keyword hit that was not read by hand. Cannot see
  abstracts, or a relevant title that uses none of the keywords.
- robots.txt read in its own request first; 10 s or more between all OpenAlex requests.
- All 24 LOOP gates rerun, all exit 0.

## NOT verified

- Abstracts and full texts of every hit: not read. Only the first 25 (q1 to q8) or 50 (r1 to r3)
  results per search were looked at; the free-text searches q4 and q5 had 1,185 and 171 results.
- The Zenodo preprint W7236434571: only its OpenAlex record; its content, what E5093 and E5107 are,
  and whether it mentions unary operations: unknown (queued).
- Austin 1965 and Stein 1963: not read (ams.org is not fetched by the loop). That Austin 1965 is the
  source of the name "Austin law" is our guess from author, title and year.
- zbMATH, MathSciNet, Springer, books: not searched.
- Whether OpenAlex `title.search` with several words needs all words in the title, or treats them
  as a phrase: not checked; the 0 results of q1, q3 and r2 may come from that (see Surprises).
- That OpenAlex covers the journals where such a law would appear (Algebra Universalis, Demonstratio
  Mathematica, Mathematica Slovaca ...): not checked.

## Surprises, errors, dead ends

- Three title searches returned 0 results (q1, q3, r2), while the shorter "type (2,1)" returned 96.
  A title search with several words is narrow; the controls show it works, but a 0 from a long
  phrase says little. Shorter title words were tried in the same run (r1 to r3).
- The scratch scan's list of hand-read hits was first written before all hits had been read, so the
  first real run printed "FAIL" for 10 unrelated titles. Each was then read and added to the list;
  the second run passed and the mutation run still failed for the intended reasons only.
- Queue item 2 cannot go ahead without the owner: z3 is the only prover installed.

## Next

Queue: the remaining items as before; new item: read the Zenodo record of the 2026 preprint
"Seeded infinite models of the Austin identities E5093 and E5107" (robots.txt first) and compare
its models with our term models and its laws with our candidates' magma special cases.
