# 26. Primary sources supplied by the owner

- Date: 2026-11-23
- Status label: literature read (primary texts, read in full or as noted). No mathematical label changed.
- Commit(s): the commit that adds this file.

## In plain words

1. **The question.** Earlier steps could not read five old papers (they are on sites the loop does
   not visit, or behind a paywall). The owner downloaded them. What do they say about our nine laws?
   In particular: had anyone already shown that one of our laws has infinite examples but no finite
   example with two or more elements?
2. **What was done.** The owner saved five PDF files. Their text was extracted with `pdftotext` and
   read; one page of one paper was also read as an image. The PDFs are copyrighted, so they are
   **not** in this repository: only the references, short quotes and what each says.
3. **Example: the main finding.** A 1990 chapter by A. Kisielewicz (p. 130) says: "in Dudek [1988] it
   is shown, that the single identity (x'y)z = y in type <1,2> yields also a variety with the same
   property". "Type <1,2>" means one operation with one input and one with two inputs, our setting.
   Writing `x'` as `f(x)`, the law is `(f(x)*y)*z = y`, one of our four laws. "The same property"
   means: some structure with two or more elements obeys it, but no finite one does. So that answer
   was **already known in 1988**. By the mirror rule (read every `a*b` as `b*a`; our hand argument,
   step 07) the same holds for `x*(y*f(z)) = y`.
4. **What it means, and what it does NOT mean.** Our answers do not change: they agree with the
   literature. Two of our four "infinite only" laws are known results (one directly, one through the
   mirror rule), so we must not present them as new. We have **not** read Dudek's 1988 paper itself
   (paywalled): the claim comes from Kisielewicz's summary of it. The other two laws, `f(x*(y*z)) = y`
   and `f((x*y)*z) = y`, are not mentioned in any of these five texts, which does not make them new.
5. **How a reader can re-check.** Look up the references below (DOIs given) and read the quoted
   pages. There is no command to run for this step.

## Sources read

| # | Reference | What was available | DOI |
|---|-----------|--------------------|-----|
| S1 | A. K. Austin, "A note on models of identities", Proc. AMS 16 (1965), 522-523 | full text | 10.1090/s0002-9939-1965-0174649-7 |
| S2 | S. K. Stein, "Finite models of identities", Proc. AMS 14 (1963), 216-222 | full text | 10.1090/s0002-9939-1963-0144995-x |
| S3 | A. K. Austin, "Finite models for laws in two variables", Proc. AMS 17 (1966), 1410-1412 | full text | 10.1090/s0002-9939-1966-0199134-9 |
| S4 | A. Kisielewicz, "Varieties of algebras with no nontrivial finite members", in J. Almeida et al. (eds.), *Lattices, Semigroups, and Universal Algebra*, Plenum/Springer 1990, pp. 129-136 | **pages 129-130 only** (the file has two pages) | 10.1007/978-1-4899-2608-1_14 |
| S5 | J. R. Cho, J. Dudek, "A note on the Austin's groupoids", East Asian Math. J. 22 (2006), No. 2, 215-221 | full text | (KoreaScience record `E1BGBB_2006_v22n2_215`) |

Not available (paywalled, owner 2026-11-23): J. Dudek, "A note on models of identities", Algebra
Universalis 25 (1988), 400-401 (`10.1007/BF01229987`), and A. Kisielewicz, "Austin identities",
Algebra Universalis 38 (1997), 324-328 (`10.1007/s000120050057`).

## What each source says (quotes from the extracted text)

- **S1, Austin 1965.** One binary operation only. Theorem: "The identity
  ((yyy)x)((yy(yyy))z) = x has infinite models but no finite models other than the model with only
  one element." The finite part is proved with left and right translations: one is one-to-one, the
  other onto, and "Since G is finite, both are bijections", the same kind of counting as our hand
  argument (README, "Finite part").
- **S2, Stein 1963.** Groupoids (one binary operation). Theorem 2.2: "There exists a nontrivial
  variety having only one finite member" (with infinitely many identities). In passing (section 3) it
  uses two unary functions: for `f(g(x)) = x`, "In any finite model of this identity f and g are
  bijections inverse to each other ... For infinite models this is not necessarily the case." None
  of our laws appears.
- **S3, Austin 1966.** "any law involving only two variables, at least one of which occurs on both
  sides of the law, and n-ary operators, n>0, has a finite model" (finite model = "of order at least
  two"). Theorem 2 covers several operators of any arity at least 1, so it includes our type (2,1).
  All four of our "infinite only" laws have three letters, so the theorem does not apply to them, and
  there is no conflict. It also says the result fails with a constant (nullary operator), with the
  example "yxpapap = x" in postfix notation, that is `((y*x)*a)*a = x` for a constant `a`, which has
  no nontrivial model at all.
- **S4, Kisielewicz 1990, pp. 129-130.** Considers algebras of any type, not only groupoids: it lists
  examples of "varieties with no nontrivial finite members" in types <1,2>, <0,2>, unary algebras and
  <0,0,1,1,1,3>. The two key sentences: "In turn, in Dudek [1988] it is shown, that the single
  identity (x'y)z = y (4) in type <1,2> yields also a variety with the same property, as well as the
  identity (Cx)y = x (5) in type <0,2> (Dudek [1985])." Theorem 1 (p. 130): "The identity
  ((y²y)x)(y²z) = x has infinite models, but no nontrivial finite model", the 1990 law listed in our
  README. Pages 131-136 were not available, so whether the chapter defines "Austin identity" is
  still unknown.
- **S5, Cho and Dudek 2006.** Groupoids only. Calls `((y²y)x)((y²(y²y))z) = x` "the Austin's identity",
  says it "appeared in many papers ([3], [4], [5], [6], [8])", where [4] is Dudek 1988, and that "In
  [7] [Kisielewicz 1997] ... the identity ((y2y)x)(y2z) = x is the shortest groupoid identity which
  has no nontrivial finite models" (exponents as extracted; not checked against the page image). It
  does not quote `(ex)y = x` and says nothing about type (2,1).

## Consequences for this repository

- `(f(x)*y)*z = y`: known, Dudek 1988, as reported by Kisielewicz 1990 (S4). Our infinite model and
  counting argument are an independent re-derivation of a known result.
- `x*(y*f(z)) = y`: its mirror, so known up to the mirror rule (hand argument, step 07).
- `f(x*(y*z)) = y` and `f((x*y)*z) = y`: not in S1-S5.
- Step 19 guessed that Dudek's `(ex)y = x` came from Dudek 1988. S4 credits `(Cx)y = x` in type
  <0,2> to **Dudek [1985]** instead, and credits Dudek 1988 with the type <1,2> law. The README
  sentence is corrected.
- "Austin law" for a type other than one binary operation: S4 treats "no nontrivial finite members"
  for any type, which supports carrying the idea over to type (2,1). Pages 129-130 do not call such laws
  "Austin identities"; they cite Austin 1965 only as the first magma example (pages 131-136 not read).

## Checks done (and what each one can and cannot catch)

- Read the extracted text of all five files and the two page images of S4. Catches what the papers
  say; text extraction can garble formulas, so every formula quoted above was compared with the
  surrounding text, and the two S4 formulas with the page image.
- Compared S4's law (7) with the README's 1990 law: `((y²y)x)(y²z) = x` is
  `(((y*y)*y)*x)*((y*y)*z) = x`. They agree.
- Read-only check of the main repository's data (`eq-unary-magma-laws`, `data/o3_sat.npy` and
  `data/laws_3.json`) against S3: of its 216 laws with no model of size 2 or 3, exactly one has at most
  two letters with a letter on both sides, `(x*y)*(y*x) = y`, and it has a 4-element model. So no
  conflict with Austin 1966.

## NOT verified

- Dudek 1988 itself: not read. That it proves the type <1,2> result is Kisielewicz's statement.
- That Dudek's `x'` is a unary operation applied to `x`: read from "type <1,2>" and the notation; the
  paper's own definitions were not seen.
- S4 pages 131-136, Kisielewicz 1997, and any zbMATH review.
- The Cho-Dudek formula attributed to Kisielewicz 1997 (exponents from text extraction only).
- No search was made for later papers citing Dudek 1988 that may cover our other two laws.

## Surprises, errors, dead ends

- Surprise: one of our four laws is exactly a published 1988 example. The repository never claimed
  novelty, but the README called all four "candidate Austin laws" with "nothing found" in the
  literature; that is now corrected for two of them.
- Correction: the source of `(ex)y = x` (step 19's guess) was wrong; see above.

## Next

Nothing for the loop (the repository is finished). Optional later: Dudek 1988 or a review of it, to
read the type <1,2> result first-hand; S4 pages 131-136.
