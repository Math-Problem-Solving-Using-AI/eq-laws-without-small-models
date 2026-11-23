# 25. Read the Zenodo preprint on the Austin identities E5093 and E5107

- Date: 2026-11-23
- Status label: literature check (S5 of `docs/shared/VERIFICATION_PROTOCOL.md`) of one lead, read
  from its primary record and its LaTeX source; our reading checked by plain code
  (`zenodo_e5093_check.py`). A lead, not a source of our results. No label of our nine laws changes.
- Commit(s): see `git log -- steps/25-zenodo-e5093-preprint.md`

## In plain words

1. **The question.** A *magma* is a set with one operation `*` that combines two elements into one.
   A *law* is a rule such as `x = y*(y*(y*(x*(z*y))))` that must hold for every choice of the
   letters; a structure where it holds is a *model* of the law. An *Austin law* (or "Austin
   identity") is a law with models of two or more elements, all of them infinite. Four of our laws
   (which also use a one-input operation `f`) look like Austin laws. In step 22 a 2026 preprint
   turned up by its title only: "Seeded infinite models of the Austin identities E5093 and E5107",
   on *Zenodo* (a public archive for papers and data, run by CERN). E5093 and E5107 are law numbers
   in the *ETP* (Equational Theories Project, a large public project that sorted all short magma
   laws). The questions: what are E5093 and E5107, how are the preprint's infinite models built
   compared with ours, and does it use a one-input operation like our `f`?

2. **What was done, in order.**
   1. **Read Zenodo's `robots.txt`** (the file where a site says what programs may fetch), in its
      own request (10:46:30 UTC). It forbids `/search`, `/api` (except record files) and
      `/records/*/preview`, and asks for 10 seconds between requests. Record pages and record files
      are allowed. Two more requests followed, each more than 10 seconds after the one before.
   2. **Fetched the record page** `zenodo.org/records/24340685` (10:46:51). Zenodo forwarded it to
      record `24360387`. The page's own data says why: `24340685` is the "parent" number that
      stands for all versions, and `24360387` is version 2, published 2026-11-19. Read its
      description, file list and license.
   3. **Fetched the paper's LaTeX source** (`E5093-paper-v2.tex`, 23,193 bytes, 10:47:29): the
      text the PDF is made from, readable without a PDF reader. Its MD5 checksum is the one the
      record page lists, so it is the file the record holds. Read it in full. Nothing else fetched
      (no PDF, no Lean files, no zip).
   4. **Looked up the ETP's tables** in the local ETP clone (commit `dbc9a2b`, read only), to see
      where E5093 and E5107 stand there.
   5. **Checked our reading by plain code** with a new script, `zenodo_e5093_check.py` (no solver):
      the paper's 8 law texts equal the ETP's lines; the paper's 5 worked failures come out as
      printed from its 12-entry starting table; no magma with 2 or 3 elements satisfies E5093,
      E5107 or E40951 (every table tried); none of the three is a special case of our four laws;
      14 quotes used here occur once each in the paper, and the word "unary" does not occur.
      *Mutation test* (deliberately corrupted inputs that a working check must notice): 8 of 8
      rejected.
   6. **Ran all 24 LOOP gates** (the repository's own checks): all exit 0.

3. **A small example.** Take the 2-element magma on `{0, 1}` where `a*b = b` (the product is always
   the right-hand input). In E5093, `x = y*(y*(y*(x*(z*y))))`, every product on the right returns
   its right input, so the right side is `z*y = y`, then `x*y = y`, and so on: the right side is
   always `y`. The law then says `x = y` for all `x, y`, which fails for `x = 0, y = 1`. The script
   tries all 16 tables of size 2 and all 19,683 of size 3 this way: none satisfies E5093. The
   paper's own example, from its starting table ("seed"): with `0*0 = 1`, `1*0 = 2`, `1*2 = 3`,
   `0*3 = 4`, the law E10218 at `x = y = z = 0` has right side
   `0*((0*0)*((0*0)*0)) = 0*(1*(1*0)) = 0*(1*2) = 0*3 = 4`, while its left side is `0`. So any model
   that contains these entries breaks E10218. The script recomputes this and the four other cases.

4. **What came out, and what it means.**
   - **The two laws.** E5093 is `x = y*(y*(y*(x*(z*y))))` and E5107 is `x = y*(y*(y*(z*(x*y))))`
     (paper and ETP clone agree, by machine). They are magma laws, with no one-input operation.
     The paper defines a magma as "a set with one binary operation", and the word "unary" does not
     occur in it. `L_y(t) = y*t` in the paper is a shorthand for "multiply by `y` on the left", not
     an operation of the algebra.
   - **Status in the ETP.** In the ETP clone's blueprint (its long write-up), E5093 and E5107, and
     their mirror images E41179 and E40951 (paired in the same rows; E41179 checked as the mirror of
     E5093 by reading the texts), sit in the table "Trivial finite models, unknown
     infinite models". This answers an unknown of step 23. The clone's note on E5093 calls it "A
     conjectural Austin law".
   - **Their answer.** Kisielewicz showed that no finite magma with 2 or more elements satisfies
     E5093 (the paper cites Kisielewicz, "Austin identities", Algebra Universalis 38 (1997),
     324–328, the same paper as in steps 13 and 18). The preprint builds an infinite model of each
     law, so both are Austin laws. It says it was not first: "vkg" announced a model of E5093 on the
     Lean Zulip forum on 5 August 2026, and version 1 of the preprint "described the question as
     open; we missed the thread when checking for prior work".
   - **How their models are built, compared with ours.** Theirs: the elements are the numbers
     0, 1, 2, ...; the product table starts empty (or from a given finite "seed") and is filled one
     cell at a time, each time with fresh numbers, while seven conditions keep the partial table
     extendable ("completing finite partial tables"). Ours (steps 06, 07): the elements are formal
     expressions (terms), and the product is "write the two terms side by side" unless a fixed
     rewrite rule applies. Both give countably infinite models, but by different methods; theirs
     is the greedy table-filling method, ours the term-model method (the ETP's "canonizers", step
     20). The paper's seeded version can also force a chosen finite pattern into the model, which
     is how it refutes five open implications from a public problem set (SAIR). This is our
     reading, not a machine comparison.
   - **Definition of "Austin identity".** The paper says: "A model of either identity with more
     than one element, all of whose finite models are trivial, makes the identity an Austin
     identity". This is the paper's own wording for magmas; it does not quote Kisielewicz's
     definition, which stays unknown (step 18).
   - **For us.** None of E5093, E5107, E40951 is a special case of our four laws (by machine: `f`
     replaced by every magma term with up to 3 operations, every way of matching). So the paper
     says nothing directly about our laws. Its greedy method is a possible second, independent
     way to build models of our four laws (queued as a lead).
   - **A lead for queue item 10.** Its Lean certificates import "the official `JudgeProblem`
     module" of `github.com/SAIRcompetition/equational-theories-lean-stage2` (revision `817a465`),
     checked "on Lean 4.33.1". Step 24 found that the trace-tree certificates also import a
     `JudgeProblem` that their repository does not contain, and also name Lean 4.33.1. That they
     are the same file is a guess, not checked; it is added to queue item 10.
   - It does NOT mean the preprint's proofs are right: its Lean files were not fetched or run, and
     its Theorem 1 (every admissible seed extends to a model) was read, not checked. Our size 2 and
     3 search is a finite search, not a proof for all sizes (the paper's own Proposition 3 is a hand
     proof for all finite sizes, read, not checked).

5. **How a reader can re-check it.** Without downloads (needs the ETP clone at
   `../_external/equational_theories`): `python zenodo_e5093_check.py`. Expect four numbered lines
   and `OK`. `python zenodo_e5093_check.py --selftest` should end with
   `selftest: 8 of 8 corrupted inputs rejected`. To check the quotes too, download
   `https://zenodo.org/records/24360387/files/E5093-paper-v2.tex?download=1` (after Zenodo's
   robots.txt), then run `python zenodo_e5093_check.py --paper E5093-paper-v2.tex`: expect a fifth
   line, `5. 14 quotes found once each in the paper, no 'unary'`, and `OK`.

## Goal

Queue item 3 (STATE.md before this run): read the Zenodo record of the 2026 preprint "Seeded infinite
models of the Austin identities E5093 and E5107" (`doi:10.5281/zenodo.24340685`) after Zenodo's
robots.txt; record what E5093 and E5107 are, how its seeded models compare with our term models, and
whether it mentions a unary operation. Items 1 and 2 wait for the owner (no Lean, no second prover).

## Command(s)

In the session's scratch folder (not the repository), times UTC on 2026-11-23:
```
curl -s https://zenodo.org/robots.txt                                   # 10:46:30, HTTP 200
curl -s -L https://zenodo.org/records/24340685                          # 10:46:51, HTTP 200, ends at /records/24360387
curl -s -L "https://zenodo.org/records/24360387/files/E5093-paper-v2.tex?download=1"   # 10:47:29, HTTP 200
python -I check25.py z25 <ETP>/data/eq_size5.txt          # exit 0 (after two fixes, see Surprises)
python -I check25.py z25 <ETP>/data/eq_size5.txt mutate   # exit 1, FAIL 9 (6 kinds of plant, all caught)
```
From the repository root:
```
python zenodo_e5093_check.py --paper <scratch>/z25/paper.tex   # exit 0, five lines and OK
python zenodo_e5093_check.py                                   # exit 0, four lines and OK
python zenodo_e5093_check.py --selftest                        # exit 0, 8 of 8 rejected
grep -n "5093\|5107\|40951\|caption" ../_external/equational_theories/blueprint/src/chapter/order_5.tex
```
Plus all 24 LOOP gates from `LOOP.md` (all exit 0).

## Inputs

- Zenodo `robots.txt`, SHA-256 `56e9fc51dcc0170c0cea188ef1f8d8906e1123f5a061a68d17d3067b781b04da`.
- Record page (version v2, record 24360387, parent 24340685), 98,306 bytes, SHA-256
  `0885b4a24f9c84fef10ce8014931076ed48e47d4a7703006b5d95fac40561db7`; its text (tags removed,
  scratch only) `3fa0c9c472735bc4aa6ccbd9efff215f9005c43b42cd6002c9bd05b82981fe7b`. Quoted from it:
  "Published November 19, 2026", "Version v2", author "Peng, Yancheng Jason" ("Independent
  Researcher"), license "Creative Commons Attribution 4.0 International", created November 19,
  modified November 20, 2026. Files listed: `E5093-paper-v2.pdf`, `E5093-paper-v2.tex`,
  `E5093.lean`, `lean-toolchain`, `Replay.lean`, `SAIR-five-countermodels.zip`.
- `E5093-paper-v2.tex`, 23,193 bytes, MD5 `f95a933d78cc09317417b3b44c3a58ac` (equal to the record's
  listing), SHA-256 `9715ffb85ebf09b1b675cc3f6a00eaeee8dabcd4a2795397ddb5ca38847caf8e`. Not stored in
  the repository.
- ETP clone at `../_external/equational_theories`, commit `dbc9a2bf0c939e7c646841e679f0f7fb6cfe4e15`
  (`data/eq_size5.txt`, `blueprint/src/chapter/order_5.tex`, `commentary/Equation5093.md`).
- Scratch script `check25.py` (not kept), SHA-256
  `e108ce6150aa2945838819532a01f2485c934d560f0dab6718422f9e844fe8be`; the kept
  `zenodo_e5093_check.py`, SHA-256 `7d7f5ce381e538fd39cac2d5584debf05da20f6a66048ebccdec17e76d08123b`
  at the time of this step.
- `curl` (Git for Windows), Python 3.12.10.

## Output

- New `zenodo_e5093_check.py` (with `--selftest`, needs the ETP clone, not in CI); this step file;
  README: the Zenodo sentence, the related-method paragraph, step list, Files and Reproduce.
- Quoted from the paper (each found once by machine):
  - "A model of either identity with more than one element, all of whose finite models are
    trivial, makes the identity an \emph{Austin identity}." (line break in the source)
  - "on the natural numbers by completing finite partial tables"; "finite seed: every admissible
    finite table extends to a model on the natural numbers" (abstract)
  - "Bruno Le Floch described that model as a greedy translation-invariant operation on a free
    group" (about vkg's earlier model; line break in the source)
  - "Both use Lean~4.24.0 with only the core library and \code{Std}." (its two Lean developments)
  - "library and the official \code{JudgeProblem} module~\cite{sairjudge}", with the reference
    `github.com/SAIRcompetition/equational-theories-lean-stage2/tree/817a4653bf762584931d49c6714c9fcfab7df66a`;
    "official stage-2 checker on Lean~4.33.1. This is a local check, not a recorded online
    submission" (line break in the source)
  - "OpenAI Codex assisted in developing the construction, formalizing the proofs and preparing the
    manuscript."
- ETP blueprint (clone): E5093/E41179 and E5107/E40951 are rows of the table captioned "Trivial
  finite models, unknown infinite models" (`order_5.tex` lines 50, 51, 95); line 40: "This set
  includes \Equareffull{5093}, another equation mentioned in \cite{Kisielewicz2} as having only
  trivial finite models, and it being unknown whether it allows infinite models." The clone is a
  shallow copy (one commit, `dbc9a2b`, dated 2026-11-19, the same day as version 2), so when these
  lines were last changed is unknown. They still say "unknown", although vkg's post (August 2026,
  by the preprint's account) came earlier: the blueprint had not been updated, or the account is
  wrong; not checked.

## Checks done (and what each one can and cannot catch)

- robots.txt read in its own request before the two other requests; 10-second wait kept (12 s
  inside each command). Catches a forbidden path; `/records/<id>` and `/records/<id>/files/...` are
  not forbidden.
- MD5 of the downloaded `.tex` equals the record's listing: the file read is the one the record
  holds. It cannot say the `.tex` and the PDF say the same thing (the PDF was not read).
- `zenodo_e5093_check.py`: law texts against the ETP's lines (parsed, so spacing does not matter);
  the 5 failures of the paper's Table 2 recomputed from its 12 seed entries (a missing entry is an
  error, so it also checks the paper's claim that every product used is a seed entry); every table
  of size 2 and 3 for E5093, E5107, E40951 (the count of tables tried is checked); instance search
  of the three laws in our four laws with two positive controls from step 15 (E28770, E17522),
  each required with the exact law and `f` term step 15 found; quotes and "unary" when `--paper` is
  given. Selftest: 8 of 8 mutations rejected (ETP line changed, seed entry changed, seed entry
  removed, a law with small models, a known instance as target, a control's law removed, a quote
  broken, "unary" planted). It cannot catch a misreading of the parts I did not encode (the seven
  conditions, the proofs), and it does not check that the seed extends to a model.
- 24 LOOP gates: all exit 0 (nothing of ours changed; they show the new file broke nothing).

## NOT verified

- The preprint's proofs: Theorem 1 (seeded completion), Lemma 2 (one-cell extension), Proposition 3
  (finite models trivial) and the seed's admissibility were read, not checked. Its Lean files,
  zip, `check_diagram.py` and PDF were not fetched or run.
- vkg's earlier model on the Lean Zulip (5 August 2026) and Le Floch's description of it: only as
  the preprint reports them; the thread was not read. That vkg was first is the preprint's account.
- That the `JudgeProblem` of the SAIR stage-2 repository is the same file the trace-tree
  certificates import (step 24): a guess from the same name and the same Lean version, not checked.
- The SAIR problem collections on Hugging Face: not read; that the five implications are open
  problems there is the preprint's statement.
- Whether E5093 and E5107 relate to our laws in any way other than "special case": not looked at
  (for example whether one of our laws implies one of them, or the other way). The instance search
  covers E5093, E5107, E40951, not E41179 (E5093's mirror); E41179 is covered only through the mirror
  rule (our four laws come in mirror pairs), which is a hand argument.
- Whether the greedy table-filling method works for a law with a one-input operation `f`: not tried.
- Kisielewicz's own definition of "Austin identity": still unknown (the preprint gives its own).
- No magma of size 4 or more was searched for E5093/E5107 here (sizes 2 and 3 only).
- The comparison "their models differ from our term models" is my reading of the two methods, not a
  proof that no term model exists for E5093.

## Surprises, errors, dead ends

- The DOI in OpenAlex (step 22) is the parent number of all versions; Zenodo forwarded it to version
  2, published 2026-11-19, three days before step 22 found the record (2026-11-22). Version 1 was not
  read; the record says version 1 "described the E5093 question as open".
- The ETP clone, a shallow copy dated 2026-11-19, still lists E5093 and E5107 as "unknown infinite
  models", while the preprint says vkg answered E5093 in August 2026. Recorded, not resolved.
- Slip: one quote in the scratch check was copied across a line break of the source ("standard" sat
  on the line before), so the first run reported it missing. The check worked; the quote was cut to
  the part on one line.
- Slip: the first mutation of an ETP text in the scratch check replaced `z ◇ z`, which does not occur
  in E5012, so the mutation changed nothing and the check rightly passed it. Caught by reading the
  list of failures (5 of 6 plant kinds were visible, one missing). Fixed with an assert that the
  plant really changes the text.
- Slip: in the repository script's first selftest, "remove one of our laws" was not rejected: both
  controls also match with `f(t) := t` in a second law. The control now requires the exact law and
  term step 15 recorded; then 8 of 8.
- The scratch check printed "FAIL" before "all checks pass" on success (cosmetic); fixed.

## Next

Queue: Wrocław and KoreaScience retry, Ernst's slide, the canonizer check, Knuth-Bendix,
Janota-Rawson-Schulz, Austin 1966, then `JudgeProblem` (now with the SAIR stage-2 repository as the
first place to look). New, last: whether the greedy table-filling method of this preprint could give
an independent second model for one of our four laws (with `f`).
