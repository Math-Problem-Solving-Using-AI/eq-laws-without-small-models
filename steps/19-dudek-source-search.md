# 19. Look for Dudek's primary source for the identity `(e*x)*y = x`

- Date: 2026-11-22
- Status label: literature check (S5 of `docs/shared/VERIFICATION_PROTOCOL.md`) of one citation,
  partly done: **which paper** is now known from two independent metadata sources (a lead with a
  name, year, journal and pages); **what it proves** is still **unknown** (no text, abstract or
  review read). No label of our nine laws changes.
- Commit(s): see `git log -- steps/19-dudek-source-search.md`

## In plain words

1. **The question.** A *magma* is a set with one operation `*` that combines two elements. A *law*
   (or *identity*) is a rule such as `(e*x)*y = x` that must hold for every choice of the letters
   `x` and `y`; `e` is a *constant*, one fixed element named in advance. A structure where the law
   holds is a *model*; a model is *trivial* when it has only one element. Slides by Z. Ernst
   (2008, read in step 16) say that "Dudek's" identity `(ex)y = x` has nontrivial models, but only
   infinite ones. Our README uses that as an example next to our own four laws with the same
   behaviour. The slides give no reference: no first name, no paper, no year. Which Dudek, which
   paper, and what does it prove?

2. **What was done, in order.** Each site's `robots.txt` (the file where a site says what programs
   may fetch) was read in its own request before any page of that site.
   1. **Crossref** (the open registry of DOIs, permanent document identifiers). Step 18 had found,
      in the reference list of Kisielewicz's 1990 chapter, the entry "J. Dudek, [1988], A note on
      models of identities, Algebra Universalis, 25, 400-401" with DOI `10.1007/BF01229987`.
      Read Crossref's robots.txt (404: no file, so the site states no limits), then the record of
      that DOI. It confirms author Józef Dudek, the title, journal, volume, pages, and December
      1988. It has **no abstract**, and lists 2 references: A. K. Austin, "A note on models of
      identities" (1965), and W. Taylor, "Some interesting identities" (1980).
   2. **OpenAlex** (an open index of research papers). Read its robots.txt (`Allow: /` for all),
      then the record of the same DOI: no abstract, marked `closed` (no open copy known to it),
      author affiliation University of Wrocław. Then the list of works that cite it: two, both
      closed. One is Kisielewicz's 1990 chapter (known from step 18). The other is new:
      J. R. Cho and J. Dudek, "A note on the Austin's groupoids", 2006, with a landing page on
      KoreaScience.
   3. **Two web searches** (Springer, AMS and zbMATH excluded): one for the 1988 title, one for the
      2006 title. The first pointed to the open universal-algebra bibliography of J. Ježek
      (Charles University, Prague). The second gave only a search-engine summary of a
      ResearchGate listing (a lead, not read; ResearchGate was not opened).
   4. **Ježek's bibliography** (`ka.karlin.mff.cuni.cz/jezek/bibua.tex`), after the site's
      robots.txt (404, no limits stated). It lists, under the heading "Dudek J.", entry
      "[88] A note on models of identities. Algebra Universalis 25, 400-401." This is a second
      source, independent of Crossref, that the 1988 note is Dudek's.
   5. **KoreaScience** (for the 2006 paper). Its robots.txt could not be read: both
      `http://www.koreascience.or.kr/robots.txt` and `https://www.koreascience.kr/robots.txt`
      returned an empty reply. So no page of that site was fetched (see `docs/shared/LESSONS.md`:
      a robots.txt that cannot be read means the site is unreadable for that run).
   6. **A small scratch check with a mutation test** (a *mutation* is a deliberately corrupted
      input; a working check must notice it). A script printed the author heading under which
      the title sits in Ježek's file, and the author, pages and "has abstract" flag of the
      Crossref record. On the real files: "Dudek J.", "Dudek", no abstract. On corrupted copies
      (heading renamed to "Someone X.", Crossref author changed and a fake abstract added) it
      printed the corrupted values, so it does read those fields.

3. **A small example of what the paper is about (from step 16, not from the paper).** On a
   2-element set `{0, 1}` with `e = 0`, the law `(e*x)*y = x` cannot hold: if `e*0 = e*1 = a`,
   then `a*y` would have to equal both `0` and `1`. So `e*0` and `e*1` differ and cover both
   elements, every row `e*x` must then be the constant row `x`, row `e` itself is constant, and
   `e*0 = e*1` after all, a contradiction. The slides' infinite model on `0, 1, 2, ...` with
   `e = 3` works: `3*x = 2^x` and `(2^x)*y = x`. Whether Dudek's 1988 note proves this, or
   something else, is exactly what we could not read.

4. **What came out, and what it means.**
   - **Which Dudek and which paper (lead, metadata only):** Józef Dudek (University of Wrocław),
     "A note on models of identities", Algebra Universalis 25 (1988), 400-401, DOI
     `10.1007/BF01229987`. Two independent sources agree (Crossref, Ježek's bibliography). Its
     title repeats Austin's 1965 note, which it cites; that fits a note on identities with only
     infinite nontrivial models, but it is a guess from titles.
   - **What it proves: unknown.** No text, no abstract, no review was read. We do NOT know that
     the note contains `(ex)y = x`; Ernst's slides do not cite it, and Dudek has other papers in
     the same area (step 18 lists two more in Kisielewicz's references).
   - A new lead: Cho and Dudek (2006), "A note on the Austin's groupoids", cites the 1988 note.
     Not read.
   - The README now names the 1988 note as a candidate source, labelled as a lead.
   - It does NOT change any label of our laws, and it is not a literature check of our laws.

5. **How a reader can re-check it.**
   ```
   curl -s https://api.crossref.org/works/10.1007/BF01229987          # author Dudek, pages 400-401, no "abstract"
   curl -s "https://api.openalex.org/works?filter=cites:W2148692680"   # 2 citing works, both "closed"
   curl -s https://ka.karlin.mff.cuni.cz/jezek/bibua.tex | grep -n "models of identities"
   ```
   The last command prints two lines: Austin's 1965 note (line 648) and Dudek's 1988 note (line
   3556, under the heading `\A{Dudek J.}` at line 3542). Records can change over time; the dates
   and checksums below say what was seen.

## Goal

Queue item 2 (STATE.md before this run): find Dudek's primary source for `(ex)y = x`: which Dudek,
which paper and year, what it proves, from open sources, robots.txt first, label what could not be
read. Lead from step 18: Dudek 1988, DOI `10.1007/BF01229987`.

## Command(s)

Run in the session's scratch folder (not the repository), times UTC on 2026-11-22:
```
curl https://api.crossref.org/robots.txt                                   # 20:39:13, 404
curl https://api.crossref.org/works/10.1007/BF01229987                     # 20:39:19, 200
curl https://api.openalex.org/robots.txt                                   # 20:39:31, 200
curl https://api.openalex.org/works/doi:10.1007/BF01229987                 # 20:39:37, 200
curl "https://api.openalex.org/works?filter=cites:W2148692680"             # 20:39:44, 200
WebSearch x2 (titles of the 1988 note and the 2006 paper; springer, ams, zbmath excluded)
curl https://ka.karlin.mff.cuni.cz/robots.txt                              # 20:40:04, 404
curl https://ka.karlin.mff.cuni.cz/jezek/bibua.tex                         # 20:40:10, 200
curl -L http://www.koreascience.or.kr/robots.txt                           # 20:40:31, empty reply
curl -L https://www.koreascience.kr/robots.txt                             # 20:41:09, empty reply
python -I author_of.py bibua.tex cr88.json                 # real files
python -I author_of.py bibua_mut.tex cr88_mut.json         # corrupted copies
```
Plus all 22 LOOP gates (all exit 0; no input of theirs changed).

## Inputs

- Crossref record of `10.1007/BF01229987`: SHA-256
  `f34be0784d196d4ecc74cc3edd07386901e1685289c62a13facd719efa38a927`, deposited
  2019-04-30T12:01:18Z, indexed 2022-04-01T20:22:00Z. Title "A note on models of identities";
  author given "J�zef" (the replacement character is in the record itself; "Józef" in other
  sources), family "Dudek"; Algebra Universalis 25(1), 400-401, published-print 1988-12;
  `abstract` absent; `reference-count` 2. References, verbatim (`?` as in the record): "A. K.
  Austin,A note on models of identities, Proc. Amer. Math. Soc.16 (1965), 522?523." and
  "W. Taylor,Some interesting identities, An. Inst. Mat. Univ. Nac. Aut�noma M�xico,20
  (1980), 127?156."
- OpenAlex W2148692680: SHA-256 `4bd94a612ac56b6c75d34fabe4c632510745a6902777eb2c3b8d81c7a3e58f2c`,
  `updated_date` 2026-11-14; no `abstract_inverted_index`; `oa_status` "closed",
  `any_repository_has_fulltext` false; institution University of Wrocław; `cited_by_count` 2.
- OpenAlex citing works: SHA-256 `d658f6c146a3d3556fbbf0f05ef84a29be33b26abac59a598b449d9e00d1ee55`.
  W2162997299 (Kisielewicz 1990, closed) and W120008873 ("A NOTE ON THE AUSTIN'S GROUPOIDS",
  Jung-R. Cho and Jo Dudek, 2006, no DOI, closed, landing page
  `http://www.koreascience.or.kr/article/ArticleFullRecord.jsp?cn=E1BGBB_2006_v22n2_215`).
- Ježek's `bibua.tex`: HTTP 200, `Last-Modified: Thu, 16 Jun 2011 15:16:08 GMT`, 748,847 bytes,
  SHA-256 `358bbaac930fef84a9ca4788d23c855c1450c9036598fb044ec813623bfbfbcc`. Line 3542
  `\A{Dudek J.}`, line 3556 `\B{88}{A note on models of identities.}{\AU {\bf 25}, 400-401.}`
  (`\AU` is defined in the file as "Algebra Universalis"); line 648, under Austin,
  `\B{65}{A note on models of identities.}{\PAMS {\bf 16},522--523.}`.
- `curl` (Git for Windows), Python 3.12.10.

## Output

- This step file; one README sentence (a candidate source for Dudek, a lead) and the README step list. No
  code, results or certificates changed.

## Checks done (and what each one can and cannot catch)

- robots.txt read in its own request before any page on each of four sites; for KoreaScience it
  could not be read, so nothing else was requested there. Catches a request a site forbids.
- Two independent sources for the attribution (Crossref, deposited by the publisher; Ježek's
  hand-made bibliography). Catches a wrong author or wrong pages in one of them. Cannot show what
  the note says.
- Scratch attribution script with a mutation (heading renamed, author changed, fake abstract
  added): all three corruptions showed up in its output. Catches a script that prints a fixed or
  wrong field. Cannot catch an abstract that the registries do not hold.
- All 22 LOOP gates rerun, all exit 0.

## NOT verified

- What Dudek's 1988 note proves, and whether it contains `(ex)y = x` at all: **unknown** (no text,
  abstract or review read).
- Whether the identity of Ernst's slides is from this note or from another Dudek paper (for
  example "On the variety V∞(+, 0)", 1982, or the 1985 Wrocław preprint, both cited by Kisielewicz
  1990): unknown.
- Cho and Dudek (2006), "A note on the Austin's groupoids": not read; KoreaScience's robots.txt
  gave an empty reply twice. The search summary of a ResearchGate listing (abstract about linear
  terms in groupoids satisfying Austin's identity) is a lead only and was not opened.
- The raised number in the slides' `ee = 2^5` (step 16): still not rendered; no PDF renderer was
  looked for in this run.
- Whether "Jo Dudek" (OpenAlex, 2006) and "Józef Dudek" (1988) are the same person: likely by
  name and field, not checked.
- zbMATH and MathSciNet reviews: not read (zbMATH disallows the assistant's agents, see Blocked;
  MathSciNet is on ams.org, which the loop does not fetch).

## Surprises, errors, dead ends

- Waits between requests to one site were 6 to 7 seconds (Crossref, OpenAlex, Ježek's server),
  shorter than the 10 seconds step 18 kept. No site asked for a delay and the binding rules set
  one only for OEIS and arXiv, but it is below our own practice; recorded in `docs/LOG.md`.
- A `sed` command meant to corrupt the heading in a copy of Ježek's file changed nothing except
  line endings (backslash quoting in the shell), so the first mutation run printed the real author
  and looked like a failed check. Done with Python on bytes instead, with an assert that the
  replaced text occurs exactly once.
- KoreaScience: empty reply from both its old and its new domain; treated as unreadable.
- The 1988 note has the same title as Austin's 1965 note, so title searches return Austin first.

## Next

Queue: Cho and Dudek (2006) via KoreaScience when its robots.txt can be read (new item, joined
with the Wrocław library retry); the rest of the queue as before.
