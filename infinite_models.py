"""Test hand-built INFINITE models for two of the open laws, on a large finite sample of elements.

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

Run from repo root: .venv/Scripts/python.exe problems/laws-without-small-models/infinite_models.py
"""
import itertools

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


okA = check("Model A f(x*(y*z)) = y", mulA, fA, lambda m, f, x, y, z: f(m(x, m(y, z))) == y, depth=3)
okB = check("Model B x*(y*f(z)) = y", mulB, fB, lambda m, f, x, y, z: m(x, m(y, f(z))) == y, depth=3)

# the models must not be trivial: more than one element, so the laws do not collapse
print("nontrivial (more than one element):", len(pool(mulA, fA, 2)) > 1, len(pool(mulB, fB, 2)) > 1)
print("ALL PASS" if okA and okB else "SOME FAILED")
