"""Test hand-built INFINITE models for three of the open laws, on a large finite sample of elements.

An infinite model cannot be checked exhaustively. This script only checks the law on every triple
(x, y, z) drawn from a pool of terms up to a size limit. A pass is a sanity check of a construction
that is argued by hand in the README, not a proof.

Elements are nested tuples. Generator: ('g',).

Model A, law  f(x*(y*z)) = y :
    x*y := ('p', x, y)                      formal pair, no collapsing
    f(t) := y   if t == ('p', x, ('p', y, z))
            t   otherwise
Model B, law  x*(y*f(z)) = y :
    f(t) := ('f', t)                        formal
    x*w  := y   if w == ('p', y, ('f', z))
            ('p', x, w)  otherwise
Model C, law  (f(x)*y)*z = y :
    f(t) := ('f', t)                        formal
    u*z  := y   if u == ('p', ('f', t), y)
            ('p', u, z)  otherwise

Run from repo root: python infinite_models.py
Mutation test:      python infinite_models.py --selftest   (corrupted models must show failures)
"""
import itertools
import sys

G = ("g",)


def pool(model_mul, model_f, depth):
    """All elements reachable from the generator in `depth` rounds of f and *."""
    elems = {G}
    for _ in range(depth):
        new = set(elems)
        for a in elems:
            new.add(model_f(a))
        for a, b in itertools.product(elems, repeat=2):
            new.add(model_mul(a, b))
        elems = new
    return elems


# Model A
def mulA(x, y):
    return ("p", x, y)


def fA(t):
    if isinstance(t, tuple) and t[0] == "p" and isinstance(t[2], tuple) and t[2][0] == "p":
        return t[2][1]
    return t


# Model B
def fB(t):
    return ("f", t)


def mulB(x, w):
    if isinstance(w, tuple) and w[0] == "p" and isinstance(w[2], tuple) and w[2][0] == "f":
        return w[1]
    return ("p", x, w)


# Model C
def fC(t):
    return ("f", t)


def mulC(u, z):
    if isinstance(u, tuple) and u[0] == "p" and isinstance(u[1], tuple) and u[1][0] == "f":
        return u[2]
    return ("p", u, z)


def check(name, mul, f, law, depth, limit=300_000):
    import random

    E = sorted(pool(mul, f, depth), key=repr)
    total = len(E) ** 3
    if total <= limit:
        triples = itertools.product(E, repeat=3)
        how = "all"
    else:
        rng = random.Random(0)
        triples = ((rng.choice(E), rng.choice(E), rng.choice(E)) for _ in range(limit))
        how = f"{limit} random"
    bad = 0
    n = 0
    for x, y, z in triples:
        n += 1
        if not law(mul, f, x, y, z):
            bad += 1
            if bad <= 3:
                print("  FAIL", x, y, z)
    print(f"{name}: {len(E)} distinct elements (depth {depth}), {n} triples tested ({how}), {bad} failures")
    return bad == 0


lawA = lambda m, f, x, y, z: f(m(x, m(y, z))) == y
lawB = lambda m, f, x, y, z: m(x, m(y, f(z))) == y
lawC = lambda m, f, x, y, z: m(m(f(x), y), z) == y


def selftest():
    """Each corrupted model (or wrong law) must give at least one failure."""
    def fA_bad(t):  # returns z instead of y
        if isinstance(t, tuple) and t[0] == "p" and isinstance(t[2], tuple) and t[2][0] == "p":
            return t[2][2]
        return t

    def mulB_bad(x, w):  # returns f(z) instead of y
        if isinstance(w, tuple) and w[0] == "p" and isinstance(w[2], tuple) and w[2][0] == "f":
            return w[2]
        return ("p", x, w)

    def mulC_bad(u, z):  # returns f(t) instead of y
        if isinstance(u, tuple) and u[0] == "p" and isinstance(u[1], tuple) and u[1][0] == "f":
            return u[1]
        return ("p", u, z)

    def fC_bad(t):  # f not formal: f(t) = t
        return t

    mutations = [
        ("A: f returns z", mulA, fA_bad, lawA),
        ("B: * returns f(z)", mulB_bad, fB, lawB),
        ("C: * returns f(t)", mulC_bad, fC, lawC),
        ("C: f is the identity", mulC, fC_bad, lawC),
        ("C checked against (f(x)*y)*z = z", mulC, fC, lambda m, f, x, y, z: m(m(f(x), y), z) == z),
        ("A checked against law C", mulA, fA, lawC),
    ]
    caught = 0
    for name, mul, f, law in mutations:
        ok = check("mutation " + name, mul, f, law, depth=2)
        caught += not ok
    print(f"selftest: {caught} of {len(mutations)} corrupted models rejected")
    return caught == len(mutations)


if "--selftest" in sys.argv:
    passed = selftest()
    print("ALL PASS" if passed else "SOME FAILED")
    sys.exit(0 if passed else 1)

okA = check("Model A f(x*(y*z)) = y", mulA, fA, lawA, depth=3)
okB = check("Model B x*(y*f(z)) = y", mulB, fB, lawB, depth=3)
okC = check("Model C (f(x)*y)*z = y", mulC, fC, lawC, depth=3)

# the models must not be trivial: more than one element, so the laws do not collapse
print("nontrivial (more than one element):",
      len(pool(mulA, fA, 2)) > 1, len(pool(mulB, fB, 2)) > 1, len(pool(mulC, fC, 2)) > 1)
nontrivial = all(len(pool(m, f, 2)) > 1 for m, f in [(mulA, fA), (mulB, fB), (mulC, fC)])
passed = okA and okB and okC and nontrivial
print("ALL PASS" if passed else "SOME FAILED")
sys.exit(0 if passed else 1)
