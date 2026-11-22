"""Plain-Python checks of what Ernst's slides (2008) say about Dudek's identity (e*x)*y = x.

The slides ("Syntax of the Finite Model Property", Z. Ernst, 2008-07-23, read in step 16) say that
the identity (e*x)*y = x, with e a constant, has models with more than one element and that they
are all infinite. They give an infinite model on the numbers 0, 1, 2, ...:

    x*y = 2**y  if x = 3,   x*y = i  if x = 2**i,   x*y = x  otherwise;   e = 3.

This script checks our reading of the slides, without a solver:

  1. the slides' model satisfies (e*x)*y = x for all x, y below a bound (a sample, not all
     numbers), and the terms e, e*e, e*(e*e), e*(e*(e*e)) are pairwise different there;
  2. no structure with 2 to 6 elements satisfies the identity: by trying every table for sizes 2
     and 3, and for sizes 2 to 6 by trying every constant e and every row of e (the identity says
     that row e*x is constant x, and puts no condition on the other rows). Every model the search
     builds is re-checked by plain evaluation of all x, y.

Part 2 is a finite search, not a proof for all sizes. The slides' own argument and Dudek's paper
are not checked here.

Usage:
  python dudek_slides_check.py
  python dudek_slides_check.py --selftest
"""
import itertools
import math
import sys


class Bad(Exception):
    pass


E = 3
BOUND = 40  # x, y in 0 .. BOUND-1 for the infinite model


def slides_op(x, y):
    if x == 3:
        return 2 ** y
    if x > 0 and x & (x - 1) == 0:  # x = 2**i
        return x.bit_length() - 1
    return x


def dudek(op, e, x, y):
    return op(op(e, x), y) == x


def check_infinite(op=slides_op, e=E, bound=BOUND):
    for x in range(bound):
        for y in range(bound):
            if not dudek(op, e, x, y):
                raise Bad(f"infinite model: (e*{x})*{y} = {op(op(e, x), y)}, not {x}")
    chain = [e]
    for _ in range(3):
        chain.append(op(e, chain[-1]))
    if len(set(chain)) != len(chain):
        raise Bad(f"infinite model: e, e*e, e*(e*e), ... not pairwise different: {chain}")
    return chain


def is_model(table, e, law=dudek):
    op = lambda a, b: table[a][b]
    n = len(table)
    return all(law(op, e, x, y) for x in range(n) for y in range(n))


def naive_models(n, law=dudek):
    """Every table and every constant: n**(n*n) * n structures."""
    for cells in itertools.product(range(n), repeat=n * n):
        table = [cells[i * n:(i + 1) * n] for i in range(n)]
        for e in range(n):
            if is_model(table, e, law):
                yield table, e


def forced_models(n, conflicts=True, stats=None):
    """For each e and each row of e: row e*x must be constant x. Free rows are set to 0.
    stats["rows"] counts the rows of e that pass the conflict test (the one-to-one rows)."""
    for e in range(n):
        for row in itertools.product(range(n), repeat=n):
            forced = {}
            ok = True
            for x in range(n):
                a = row[x]
                if conflicts and forced.get(a, x) != x:
                    ok = False
                    break
                forced[a] = x
            if not ok:
                continue
            if stats is not None:
                stats["rows"] = stats.get("rows", 0) + 1
            table = [[0] * n for _ in range(n)]
            for a, x in forced.items():
                table[a] = [x] * n
            if e not in forced or not conflicts:
                table[e] = list(row)
            elif table[e] != list(row):
                continue
            yield table, e


def check_finite(naive_up_to=3, forced_up_to=6, law=dudek, search=forced_models):
    counts = {}
    for n in range(1, naive_up_to + 1):
        found = list(naive_models(n, law))
        counts[("naive", n)] = len(found)
        if n >= 2 and found:
            raise Bad(f"size {n}: the full search found a model, e = {found[0][1]}, table {found[0][0]}")
    for n in range(1, forced_up_to + 1):
        stats = {}
        found = list(search(n, stats=stats))
        for table, e in found:
            if not is_model(table, e):
                raise Bad(f"size {n}: the search built a table that is not a model: e = {e}, {table}")
        if stats.get("rows") != n * math.factorial(n):  # e times the one-to-one rows
            raise Bad(f"size {n}: the row search looked at {stats.get('rows')} rows of e, "
                      f"expected {n * math.factorial(n)}")
        counts[("forced", n)] = len(found)
        if n >= 2 and found:
            raise Bad(f"size {n}: the row search found a model, e = {found[0][1]}, table {found[0][0]}")
    if counts[("naive", 1)] != 1 or counts[("forced", 1)] != 1:
        raise Bad(f"size 1: expected exactly one model, got {counts}")
    return counts


def main():
    try:
        chain = check_infinite()
        print(f"infinite model: (e*x)*y = x for all x, y < {BOUND}; e, e*e, e*(e*e), e*(e*(e*e)) = "
              f"{chain[:3]} and 2**{chain[2]}, pairwise different")
        counts = check_finite()
        for (method, n), c in sorted(counts.items()):
            print(f"size {n}, {method} search: {c} model(s)")
    except Bad as e:
        print("FAILED:", e)
        sys.exit(1)
    print("ALL PASS: the slides' model checks on the sample; no model with 2 to 6 elements")


def selftest():
    check_infinite()
    check_finite()  # the real checks must pass first

    def op_e2(x, y):
        return slides_op(x, y) if x != 3 else 2 ** y + 1

    def law_y(op, e, x, y):  # (e*x)*y = y, which has finite models (x*y = y)
        return op(op(e, x), y) == y

    mutations = [
        ("constant e = 2 instead of 3", lambda: check_infinite(e=2)),
        ("row 3 is 2**y + 1", lambda: check_infinite(op=op_e2)),
        ("row of 2**i gives i + 1", lambda: check_infinite(
            op=lambda x, y: slides_op(x, y) + (1 if x != 3 and x > 0 and x & (x - 1) == 0 else 0))),
        ("e*e = e (chain collapses), law test skipped", lambda: check_infinite(
            op=lambda x, y: 3 if (x, y) == (3, 3) else slides_op(x, y), bound=0)),
        ("law (e*x)*y = y", lambda: check_finite(law=law_y, forced_up_to=1)),
        ("row search without the conflict test", lambda: check_finite(
            naive_up_to=1, search=lambda n, stats: forced_models(n, conflicts=False, stats=stats))),
        ("row search that skips sizes 2 and up", lambda: check_finite(
            naive_up_to=1, search=lambda n, stats: forced_models(n, stats=stats) if n == 1 else iter([]))),
    ]
    rejected = 0
    for name, run in mutations:
        try:
            run()
            print(f"mutation {name}: NOT rejected")
        except Bad as e:
            rejected += 1
            print(f"mutation {name}: rejected ({e})")
    print(f"selftest: {rejected} of {len(mutations)} corrupted inputs rejected")
    if rejected != len(mutations):
        print("SELFTEST FAILED")
        sys.exit(1)
    print("ALL PASS")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        main()
