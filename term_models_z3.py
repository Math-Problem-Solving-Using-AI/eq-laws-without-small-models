"""Check the four infinite term models of infinite_models.py on ALL terms, with z3.

infinite_models.py tests the models on a finite sample of terms. Here the elements are the terms of
a z3 algebraic datatype T with constructors
    G           the generator
    F(t)        formal f
    P(a, b)     formal pair
z3 reads such a datatype as the set of all finite terms built from G, F and P, with different
terms always different (constructors are injective and distinct, no cycles). That is exactly the
set of elements of the models. The operations * and f are written below as if-then-else
expressions over the constructors, with no quantifiers, so z3 decides the question completely.
For each model, z3 is asked for terms x, y, z where the law FAILS. `unsat` means none exists.

Model A, law  f(x*(y*z)) = y:   x*y := P(x, y);  f(t) := b if t = P(x, P(b, z)), else t
Model B, law  x*(y*f(z)) = y:   f(t) := F(t);    x*w := b if w = P(b, F(z)), else P(x, w)
Model C, law  (f(x)*y)*z = y:   f(t) := F(t);    u*z := b if u = P(F(t), b), else P(u, z)
Model D, law  f((x*y)*z) = y:   x*y := P(x, y);  f(t) := b if t = P(P(a, b), z), else t

Nontrivial: z3 is also asked whether G = F(G); `unsat` means the model has at least two elements.

Mutation test: each corrupted model (or wrong law) below must give `sat` (z3 finds a failure).

Status of a pass: z3-only. It relies on z3's datatype reasoning being correct.

Run from repo root: python term_models_z3.py
"""
import sys

import z3

T = z3.Datatype("T")
T.declare("G")
T.declare("F", ("farg", T))
T.declare("P", ("left", T), ("right", T))
T = T.create()
G, F, P = T.G, T.F, T.P
isF, isP = T.is_F, T.is_P
left, right = T.left, T.right


# Model A
def mulA(x, y):
    return P(x, y)


def fA(t):
    return z3.If(z3.And(isP(t), isP(right(t))), left(right(t)), t)


# Model B
def fB(t):
    return F(t)


def mulB(x, w):
    return z3.If(z3.And(isP(w), isF(right(w))), left(w), P(x, w))


# Model C
def fC(t):
    return F(t)


def mulC(u, z):
    return z3.If(z3.And(isP(u), isF(left(u))), right(u), P(u, z))


# Model D
def mulD(x, y):
    return P(x, y)


def fD(t):
    return z3.If(z3.And(isP(t), isP(left(t))), right(left(t)), t)


def lawA(m, f, x, y, z):
    return f(m(x, m(y, z))) == y


def lawB(m, f, x, y, z):
    return m(x, m(y, f(z))) == y


def lawC(m, f, x, y, z):
    return m(m(f(x), y), z) == y


def lawD(m, f, x, y, z):
    return f(m(m(x, y), z)) == y


def failure_exists(mul, f, law, timeout=60000):
    """z3's answer to: are there terms x, y, z where the law fails?"""
    x, y, z = z3.Consts("x y z", T)
    s = z3.Solver()
    s.set("timeout", timeout)
    s.add(z3.Not(law(mul, f, x, y, z)))
    r = str(s.check())
    witness = s.model() if r == "sat" else None
    return r, witness


def main():
    ok = True
    for name, mul, f, law in [
        ("Model A f(x*(y*z)) = y", mulA, fA, lawA),
        ("Model B x*(y*f(z)) = y", mulB, fB, lawB),
        ("Model C (f(x)*y)*z = y", mulC, fC, lawC),
        ("Model D f((x*y)*z) = y", mulD, fD, lawD),
    ]:
        r, _ = failure_exists(mul, f, law)
        print(f"{name}: failing terms exist? {r}  (unsat = law holds on all terms)")
        ok = ok and r == "unsat"
    s = z3.Solver()
    s.add(G == F(G))
    r = str(s.check())
    print(f"G = F(G)? {r}  (unsat = at least two elements)")
    ok = ok and r == "unsat"
    return ok


def selftest():
    def fA_bad(t):  # returns z instead of y
        return z3.If(z3.And(isP(t), isP(right(t))), right(right(t)), t)

    def mulB_bad(x, w):  # returns f(z) instead of y
        return z3.If(z3.And(isP(w), isF(right(w))), right(w), P(x, w))

    def mulC_bad(u, z):  # returns f(t) instead of y
        return z3.If(z3.And(isP(u), isF(left(u))), left(u), P(u, z))

    def fC_bad(t):  # f is the identity
        return t

    def fD_bad(t):  # returns z instead of y
        return z3.If(z3.And(isP(t), isP(left(t))), right(t), t)

    mutations = [
        ("A: f returns z", mulA, fA_bad, lawA),
        ("B: * returns f(z)", mulB_bad, fB, lawB),
        ("C: * returns f(t)", mulC_bad, fC, lawC),
        ("C: f is the identity", mulC, fC_bad, lawC),
        ("C checked against (f(x)*y)*z = z", mulC, fC, lambda m, f, x, y, z: m(m(f(x), y), z) == z),
        ("A checked against law C", mulA, fA, lawC),
        ("D: f returns z", mulD, fD_bad, lawD),
        ("D: f is the identity", mulD, fC_bad, lawD),
        ("D checked against law A", mulD, fD, lawA),
    ]
    caught = 0
    for name, mul, f, law in mutations:
        r, w = failure_exists(mul, f, law)
        print(f"mutation {name}: {r}" + (f"  witness {w}" if w is not None else ""))
        caught += r == "sat"
    print(f"selftest: {caught} of {len(mutations)} corrupted models rejected")
    return caught == len(mutations)


if __name__ == "__main__":
    passed = selftest() if "--selftest" in sys.argv else main()
    print("ALL PASS (z3-only)" if passed else "SOME FAILED")
    sys.exit(0 if passed else 1)
