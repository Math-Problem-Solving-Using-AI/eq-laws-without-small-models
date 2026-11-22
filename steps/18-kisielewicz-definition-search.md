# 18. Look for Kisielewicz's own definition of "Austin identity" in open sources

- Date: 2026-11-22
- Status label: literature check (S5 of `docs/shared/VERIFICATION_PROTOCOL.md`) of one term, with a
  negative outcome: the definition was **not found** (unknown). No label of our nine laws changes.
- Commit(s): see `git log -- steps/18-kisielewicz-definition-search.md`

## In plain words

1. **The question.** A *magma* is a set with one operation `*` that combines two elements. Our
   structures also have a second operation `f` that changes one element; structures with one
   two-input and one one-input operation are said to be of *type (2,1)*. A *law* (or *identity*)
   is a rule such as `(f(x)*y)*z = y` that must hold for every choice of the letters; a structure
   where it holds is a *model*, and a model is *trivial* when it has only one element. An *Austin
   law* is a law with models of more than one element, but only infinite ones. The ETP blueprint
   (the long write-up of the Equational Theories Project, read in step 13) defines the term for
   magmas only. The name seems to come from A. Kisielewicz's paper "Austin identities" (1997) and
   his chapter "Varieties of algebras with no nontrivial finite members" (1990). Question: does
   Kisielewicz define the term for every type of algebra (which would cover our laws with `f`) or
   for magmas only? We may not fetch the publisher's pages (Springer), so: is there an open copy,
   an open abstract or an open review that says it?

2. **What was done, in order.** Every site's `robots.txt` (the file where a site says what
   programs may fetch) was read in its own request before any page, and at least 10 seconds
   passed between requests to the same site.
   1. **Wrocław university digital library** (`digilab.uwr.edu.pl`, the lead from step 15).
      `https://www.digilab.uwr.edu.pl/robots.txt` answered "moved" to
      `https://digilab.uwr.edu.pl/robots.txt`, which answered **502 Bad Gateway** (the server
      behind the site did not respond), twice, 66 seconds apart. Without a readable robots.txt no
      page was fetched there. The library may simply have been down at that moment.
   2. **zbMATH Open** (an open review database for mathematics), `robots.txt` read: it says
      `Disallow: /` for the agents `anthropic-ai`, `ClaudeBot` and `Claude-Web`, that is, for
      programs of the company that makes the assistant running this loop. So **no zbMATH page was
      fetched**, and the zbMATH search planned in queue item 7 cannot be done either without the
      owner (see STATE.md, Blocked).
   3. **Two web searches** for the two titles (Springer, AMS and zbMATH excluded). They found
      Kisielewicz's own publication list at his university, and the DOIs (permanent document
      identifiers) of both papers, quoted in the reference list of arXiv 2609.05690.
   4. **Kisielewicz's publication list** (`prac.im.pwr.edu.pl/~kisielewicz/bibl.html`, after its
      robots.txt, which does not exist: answer 404, so the site states no limits). The list gives
      both papers as citations, with **no link to a copy** (some other papers on the list have
      one).
   5. **Crossref** (the open registry of DOIs; its data are free to reuse) for both DOIs, after its
      robots.txt (also 404). Both records have **no abstract**. The 1990 chapter's record carries
      its reference list (17 entries); the 1997 paper's record has none.
   6. **OpenAlex** (an open index of research papers, data free to reuse) for both DOIs, after its
      robots.txt (`Allow: /` for all). Both records have no abstract, and OpenAlex marks both as
      `closed` (no open copy known to it, `any_repository_has_fulltext: false`).
   7. **Checked the reader of the abstract field**: a small scratch script that prints the
      abstract of a Crossref or OpenAlex record printed nothing for the four real records, and
      printed the text when a fake abstract was put into copies of two of them (a *mutation test*:
      a deliberately corrupted input that a working check must notice).

3. **A small example of what the answer would change.** Our law `(f(x)*y)*z = y` has an infinite
   model with more than one element (step 06, checked by the solver z3) and, by a hand argument,
   no finite one with more than one element. If Kisielewicz defines "Austin identity" for any type
   of algebra, then the name fits this law as it stands. If he defines it for groupoids (another
   word for magmas) only, then the name, used for our law, is our own extension, as the README
   already says. The mathematics is the same either way; only the right to use the name is at
   stake.

4. **What came out, and what it means.**
   - **The definition was not found.** None of the five open sources gave the text of either
     paper or an abstract. The question stays **unknown**. The README sentence "Whether
     Kisielewicz's papers define the term for all types of algebra is unknown (not read)" stays
     true; it now points to this step.
   - **Something found on the way (a lead, not a fact about the papers' content):** the reference
     list of the 1990 chapter, as Crossref gives it, includes
     "J. Dudek, [1988], A note on models of identities, Algebra Universalis, 25, 400-401"
     (DOI `10.1007/BF01229987`), two other Dudek items, and "S. Burris, [1972], Models in
     equational theories of unary algebras". Ernst's slides (step 16) attribute the identity
     `(ex)y = x` to "Dudek" with no reference; the 1988 note is a candidate for it (queue item 3).
     That the chapter cites a paper on unary algebras hints that it is not about magmas only, but
     its text was not read, so this is a guess and is recorded as one.
   - It does NOT mean the papers do not exist in open form somewhere; it means these five sources
     did not have them. It does NOT change any label of our laws.

5. **How a reader can re-check it.** In a browser or with `curl`:
   ```
   curl -s https://api.crossref.org/works/10.1007/s000120050057        # "abstract" absent
   curl -s https://api.crossref.org/works/10.1007/978-1-4899-2608-1_14 # 17 references, 4th to 6th are Dudek
   curl -s https://api.openalex.org/works/doi:10.1007/s000120050057    # "oa_status":"closed"
   curl -s https://zbmath.org/robots.txt                               # ClaudeBot: Disallow: /
   ```
   And open `https://prac.im.pwr.edu.pl/~kisielewicz/bibl.html`: both titles are listed with no
   link. (Records can change over time; the dates and checksums below say what was seen.)

## Goal

Queue item 2 (STATE.md before this run): find out how Kisielewicz defines "Austin identity"
(1990, 1997), for any type of algebra or for groupoids only, from an open source; read robots.txt
first; label what could not be read.

## Command(s)

Run in the session's scratch folder (not the repository), times UTC on 2026-11-22:
```
curl -sS -D robots.headers -o robots.txt https://www.digilab.uwr.edu.pl/robots.txt   # 20:31:57, 301
curl -sS -D robots2.headers -o robots2.txt https://digilab.uwr.edu.pl/robots.txt     # 20:32:13, 502
curl -sS -D robots3.headers -o robots3.txt https://digilab.uwr.edu.pl/robots.txt     # 20:33:19, 502
curl -sS -D zb_robots.headers -o zb_robots.txt https://zbmath.org/robots.txt         # 20:33:25, 200
WebSearch x2 (titles of the 1997 paper and the 1990 chapter; springer, ams, zbmath excluded)
curl https://prac.im.pwr.edu.pl/robots.txt        # 20:33:51, TLS error, no HTTP answer
Invoke-WebRequest https://prac.im.pwr.edu.pl/robots.txt                # 20:34:10, 404
Invoke-WebRequest https://prac.im.pwr.edu.pl/~kisielewicz/bibl.html     # 20:34:29, 200
curl https://api.crossref.org/robots.txt                                # 20:34:42, 404
curl https://api.crossref.org/works/10.1007/s000120050057               # 20:34:59, 200
curl https://api.crossref.org/works/10.1007/978-1-4899-2608-1_14        # 20:35:18, 200
curl https://api.openalex.org/robots.txt                                # 20:35:28, 200
curl https://api.openalex.org/works/doi:10.1007/s000120050057           # 20:35:45, 200
curl https://api.openalex.org/works/doi:10.1007/978-1-4899-2608-1_14    # 20:36:02, 200
python -I abs_check.py cr97.json cr90.json oa97.json oa90.json cr97_mut.json oa97_mut.json
```
Plus all 22 LOOP gates (all exit 0; no input of theirs changed).

## Inputs

- `zbmath.org/robots.txt`: HTTP 200, `last-modified: Thu, 09 Oct 2025 17:07:26 GMT`. For
  `User-agent: *` only `/pdf/` and `/pdfoutput/` are disallowed; for `anthropic-ai`, `ClaudeBot`,
  `Claude-Web` (and others such as `GPTBot`, `PerplexityBot`): `Disallow: /`.
- Publication list: HTTP 200, `Last-Modified: Sun, 14 Sep 2025 09:37:06 GMT`, 18,576 bytes,
  SHA-256 `1d0cd9ee3559b03f14562510c54139ad78ebf8bd7caa0cd2efb516126fcc6048`. Entries, verbatim:
  "Austin identities, *Algebra Universalis* **38** (1997), 324-328." and "Varieties of algebras
  with no nontrivial finite members, in *Lattices, semigroups, and universal algebra (Lisbon,
  1988), (J. Almeida et al. eds),* Plenum Press, New York, London, 1990, pp. 129-136."
- Crossref, 1997 paper: SHA-256 `9aed9fb40090f2ba96cd9ee0da40dc7283cb30db35174c4e6ea3ed701ac09839`;
  title "Austin identities", author A. Kisielewicz, Algebra Universalis 38(3), 324-328,
  published-print 1997-05-01; `abstract` absent; `reference-count` 0.
- Crossref, 1990 chapter: SHA-256 `43e7f3455dd394ce9348e0cc94c86d181e43f3808bec272d27c62c519bfdf2b9`;
  title "Varieties of Algebras with no Nontrivial Finite Members", author Andrzej Kisielewicz,
  book-chapter in "Lattices, Semigroups, and Universal Algebra", pp. 129-136, 1990; `abstract`
  absent; `reference-count` 17. References 14_CR1 to 14_CR6, verbatim: A.K. Austin 1965 "A note on
  models of identities"; A.K. Austin 1966 "Finite models for laws in two variables"; S. Burris
  1972 "Models in equational theories of unary algebras", Algebra Universalis 1, 386-392;
  J. Dudek 1982 "On the variety V ∞ (+, 0)", Math. Sem. Notes 10, 9-15; J. Dudek 1985
  "Polynomially infinite varieties of algebras I", Math. Inst. Univ. Wroclaw, Preprint no 30;
  J. Dudek 1988 "A note on models of identities", Algebra Universalis, 25, 400-401
  (DOI `10.1007/BF01229987`). Also 14_CR7 J. Dudek and A. Kisielewicz, "On finite models of
  regular identities", Notre Dame J. Formal Logic, to appear.
- OpenAlex: W4243732956 (1997), SHA-256 `b358bf7a4c605d2d70cb697225a26091ec4ff035b1a66911f102e1e4dd358ea9`;
  W2162997299 (1990), SHA-256 `663703a6595189c1c392214081d441a91d1da85837ab31807461ab55a57ab867`.
  Both: no `abstract_inverted_index`, `oa_status` "closed", `any_repository_has_fulltext` false.
- `curl` (Git for Windows), Windows PowerShell 5.1 `Invoke-WebRequest`, Python 3.12.10.

## Output

- This step file; one README sentence (Kisielewicz's definition: still unknown, see step 18) and
  the README step list. No code, results or certificates changed.

## Checks done (and what each one can and cannot catch)

- robots.txt read in its own request on every site before any page; 10 seconds or more between
  requests to one site. Catches a request a site forbids. For digilab the robots.txt could not be
  read, so nothing else was requested there.
- Abstract reader with a positive control (fake abstract in two copies, both printed): catches a
  reader that cannot see an abstract when one is there. It cannot catch an abstract that the
  registries do not hold.
- Reference list quoted from the Crossref record as deposited by the publisher: catches a misquote
  of the list. It cannot show that the list matches the printed chapter, nor what the chapter
  says about each reference.
- All 22 LOOP gates rerun, all exit 0.

## NOT verified

- Kisielewicz's definition of "Austin identity" (1990, 1997): **unknown**. Neither text, nor an
  abstract, nor a review was read.
- The Wrocław digital library record (lead of step 15): not read; the site answered 502 on two
  attempts at 20:32 and 20:33 UTC. Whether it holds the full text: unknown.
- zbMATH Open reviews of both papers: not read, because zbMATH's robots.txt disallows the
  assistant's agents. Whether a review exists and what it says: unknown.
- Whether Dudek's 1988 note "A note on models of identities" contains the identity `(ex)y = x`:
  unknown (a lead for queue item 3, only the title was seen).
- Whether the 1990 chapter treats unary algebras: unknown (its reference list cites a paper on
  them; that is a hint, not a reading).
- The reference list and bibliography of arXiv 2609.05690 were seen only as a web-search result
  line; whether its body quotes Kisielewicz's definition: unknown (queue item 8 reads its body).
- Other open places not searched in this run: Ježek's universal-algebra bibliography (seen as a
  search result), Google Books, the proceedings volume's front matter, library catalogues.

## Surprises, errors, dead ends

- zbMATH Open, the database queue item 7 was going to search, disallows the assistant's own agents
  in its robots.txt (`anthropic-ai`, `ClaudeBot`, `Claude-Web`). Item 7 had been queued since
  step 14 without reading that file. Recorded in `docs/LOG.md` with a lesson for the hub; item 7's
  zbMATH part is now under Blocked.
- `curl` could not open `prac.im.pwr.edu.pl` (`SSL certificate problem: unable to get local issuer
  certificate`: the server does not send the full certificate chain). Certificate checking was not
  turned off; Windows PowerShell's `Invoke-WebRequest`, which completes the chain from the
  Windows certificate store, was used instead, with its default user agent.
- Dead end: digilab answered 502 (server down). Not retried more than once in this run.

## Next

Queue: Dudek's source (item 3, now with the lead Dudek 1988); a retry of the Wrocław digital
library when it answers again (new item). The zbMATH part of item 7 waits for the owner.
