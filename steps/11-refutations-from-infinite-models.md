# 11. Using the infinite models to show what the four laws do not imply

- Date: 2026-11-22
- Status label: each of the 2,828 non-implications is `z3-only`: the target law's failure at the
  stored elements is checked by plain Python (`check_refutations.py`), but the fact that the model
  satisfies its own law rests on z3 (`term_models_z3.py`, all terms) plus a one-line hand argument.
  The 16 implications (a law implies its own substitution instances) are checked by our own
  plain-Python matcher, not reviewed. "Implies" here means over all structures, infinite ones
  included; nothing is claimed for finite structures only.
- Commit(s): see `git log -- check_refutations.py refute_by_term_models.py steps/11-refutations-from-infinite-models.md`

## In plain words

1. **The question.** A *magma* here is a set with two operations: `*`, which takes two elements
   and gives one, and `f`, which takes one element and gives one. A *law* is a rule such as
   `f(x*(y*z)) = y` that must hold for every choice of the letters. A *model* of a law is a magma
   where the law holds. Law A *implies* law B when every model of A is also a model of B. To show
   that A does NOT imply B, one model of A where B fails is enough; the elements where B fails are
   the *witness*. Four of our nine laws (`f(x*(y*z)) = y`, `x*(y*f(z)) = y`, `(f(x)*y)*z = y`,
   `f((x*y)*z) = y`) have no finite model with 2 or more elements (a hand argument), but each has an
   infinite model, built in steps 06 and 07 and called A, B, C, D. The main repository lists 712
   short laws. The question: for each of the four laws and each of the other 711 laws, can its
   infinite model show "does not imply"?

2. **What was done, in order.**
   1. **Fixed how to write elements down.** The elements of the four models are *terms* built
      from three symbols: `G` (a starting element), `F(t)` and `P(a,b)` (a formal pair). Two
      different terms are always different elements. These symbols are names of elements, not
      the operations of the model: in model A, `f(G)` is `G`, while `F(G)` is a different element.
   2. **Wrote a search program, `refute_by_term_models.py`.** For each model and each of the 711
      other laws, it tries every way to put the 89 terms with at most 7 symbols into the law's
      letters, and stops at the first choice where the two sides of the law come out different.
      Where this finds nothing, it asks *z3* (an automatic solver) to search all terms. It reads
      the laws from the main repository's stored term trees, not from the law texts.
   3. **Wrote a separate checking program, `check_refutations.py`.** It does not import the search
      program. It writes the four models out again from their definitions, reads each law from its
      text, and for each stored witness computes both sides again and confirms they differ. It also
      checks that its own copy of each model satisfies the model's law on all 4,913 triples of the
      17 smallest terms, that every one of the 711 laws per model is accounted for exactly once,
      and that the four models cover the same 712 laws.
   4. **Looked at the laws that were not refuted.** There are 4 per model, and each is the
      model's own law with some letters made equal (a *substitution instance*), for example
      `f(x*(x*y)) = x` is `f(x*(y*z)) = y` with `x` for `y` and `y` for `z`. A law always implies
      its instances. The checker confirms by plain matching that each of the 16 is an instance.
   5. **Used the mirror pairs (step 09).** The *mirror* of a law reads every product backwards
      (`a*b` becomes `b*a`). Models A and D are mirrors of each other, and so are B and C. The
      checker reads each witness backwards (it swaps the two parts of every pair `P(a,b)` and
      mirrors the law) and confirms it is a witness for the partner model too; and it confirms
      that the laws refuted in D are exactly the mirrors of those refuted in A, and the same for
      B and C. The search had run on all four models separately, so this is a cross-check.
   6. **Tested the checker by breaking things** (a *mutation test*): 15 deliberately corrupted
      inputs or corrupted copies of the checker's models; all 15 rejected, each for the intended
      reason (reasons printed and read).
   7. **Added both checker commands to CI and the LOOP gates.**

3. **A small example.** In model B, `f(t)` is `F(t)` and a product `x*w` is the formal pair
   `P(x,w)` except when `w` is a pair whose second part starts with `F`. Take the law
   `x*y = y*x`. Put `x = G`, `y = F(G)`. Left side: `G*F(G)`; `F(G)` is not a pair, so the result is
   `P(G,F(G))`. Right side: `F(G)*G` = `P(F(G),G)`. These are different terms, so different
   elements: `x*y = y*x` fails in model B, and since model B satisfies `x*(y*f(z)) = y`, that law
   does not imply `x*y = y*x`.
   A harder one: `f(f(x)) = f(x)` in model A. In A, `f` of `P(x,P(b,z))` is `b`, and `f` leaves
   every other element alone. The search over small terms found no failure; z3 found
   `x = P(G,P(P(G,P(G,G)),G))`. Then `f(x) = P(G,P(G,G))`, and `f(f(x)) = G`, which is not `f(x)`.

4. **What it means and what it does NOT mean.**
   - For each of the four laws, 707 of the 711 other laws are not implied by it, each with a
     witness anyone can recompute; the other 4 are implied (they are instances). So the four rows
     of the main repository's table are now decided, as far as these labels go.
   - It does NOT make the non-implications `model-verified`: that label is for finite tables
     checked by plain evaluation. Here the model is infinite, and that it satisfies its law is
     checked on all terms only by z3 (`z3-only`), backed by a short hand argument. The failure of
     the target law is checked by plain code.
   - It says nothing about finite structures. If the hand argument of steps 06 and 07 is right,
     in finite structures each of these laws forces one element and so implies every law. The main
     repository asks about all structures, so infinite witnesses count there.
   - The checker was written in this session by the same author as the search, and no one has
     reviewed it. Its copy of each model is separate code, but not separate thinking.
   - No literature check was done for any of these non-implications.

5. **How a reader can re-check it.** From the repository root:
   ```
   python check_refutations.py results/refutations_term_models.json
   # four lines "model X (...): 707 laws fail in it (certificates checked), 4 not refuted, ...",
   # "2828 certificates checked, and each one read backwards in the partner model", ALL PASS
   python check_refutations.py --selftest results/refutations_term_models.json
   # 15 lines "mutation ...: rejected (...)", "selftest: 15 of 15 corrupted inputs rejected", ALL PASS
   ```
   Regenerating the file needs the main repository next to this one:
   `python refute_by_term_models.py` (about 10 seconds; it reproduced the stored file byte for byte).

## Goal

Queue item 2: for each law with an infinite model, refute implications to other laws with explicit
elements, in a certificate format checked by plain code with mutation tests, and use the mirror
pairs. Reporting the counts to the main repository is a note for the owner (docs/LOG.md).

## Command(s)

```
python refute_by_term_models.py            # reads ../eq-unary-magma-laws/data/laws_3.json
python check_refutations.py results/refutations_term_models.json
python check_refutations.py --selftest results/refutations_term_models.json
```
plus all LOOP gates.

## Inputs

`../eq-unary-magma-laws/data/laws_3.json` (712 laws, read only), the model definitions of
`term_models_z3.py` (unchanged). Python 3.12.10, z3 5.4.1. The checker does not use z3.

## Output

- `refute_by_term_models.py`, `check_refutations.py` (new).
- `results/refutations_term_models.json`: 2,828 certificates (707 per model; 2,826 found by the
  plain search, 2 by z3: `f(f(x)) = f(x)` in A and in D), and 16 laws not refuted (4 per model,
  z3 says each holds on all terms of its model; the checker shows each is an instance).
- Main-repository law ids of the four laws: 450 (`f(x*(y*z)) = y`), 639 (`x*(y*f(z)) = y`),
  135 (`(f(x)*y)*z = y`), 336 (`f((x*y)*z) = y`).
- CI and LOOP gates: two new commands. All 20 gate commands exit 0.

## Checks done (and what each one can and cannot catch)

- Plain recomputation of every witness (both sides, compared with the stored values). Catches a
  wrong witness or a search bug. Cannot catch a model that does not really satisfy its law: that
  rests on `term_models_z3.py` (z3) and a sample check in the checker (17 smallest terms).
- Coverage and uniqueness per model. Catches a missing, extra or duplicated law.
- Instance check for the 16 not refuted. Catches a refutable law hiding as "not refuted".
- Mirror check. Catches inconsistency between the four separate searches, and an error in either
  model's code that breaks the mirror correspondence.
- Laws read from term trees by the search and from texts by the checker: a misreading on one side
  would make witnesses fail on the other.
- Mutation test: 15 of 15 rejected, reasons read. The exit code was checked on a corrupted file
  (exit 1).
- Regeneration reproduced the stored file byte for byte.

## NOT verified

- That each model satisfies its law on all terms is `z3-only` plus a hand argument; the checker
  only samples 4,913 triples.
- The checker is unreviewed and written in the same session as the search.
- The texts in the results file are copied from the main repository's list; that each text matches
  its stored term tree is the main repository's check (`src/check_laws_text.py`), not re-run here.
- Nothing about finite implication (the finite part of the four leads is still a hand argument,
  Blocked item).
- The general mirror rule is still a hand argument; the mirror check here is on these data only.
- No literature check of any of the 2,844 decided pairs.
- The rows in the main repository's table were not changed (other repository; note for the owner).

## Surprises, errors, dead ends

- A first try asked z3 for every law and every model with a 10-second limit. After 10 minutes the
  first model had not finished, so it was stopped. The plain search over 89 small terms found 2,826
  of the 2,828 witnesses in about 3 seconds; z3 is used only for the 18 leftovers, where it answers
  at once.
- `f(f(x)) = f(x)` fails in A and D only at a term with 9 symbols, so the plain search (7 symbols)
  missed it; z3 found it.
- My first corrupted-file test of the exit code passed, because the "corrupted" value I wrote was
  already the stored value. Repeated with a value that really differs: exit 1. Same lesson as
  run 6: check that a mutation changes something.
- A mutation "certificate of B filed under C" was rejected by the duplicate guard, not by the
  witness check: the law also fails in C, so the certificate is still a valid witness there. That
  is the right guard; it is recorded so nobody reads it as a witness-check test.

## Next

Queue item 2 (check that the 712 copied law texts match the main repository's term trees), then
the literature check (item 3). The Lean items wait for the owner.
