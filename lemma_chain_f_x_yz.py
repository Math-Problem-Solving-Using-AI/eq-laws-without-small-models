"""Check a HAND-DERIVED proof sketch by z3, one lemma at a time.

Law L:  f(x)*(y*z) = y
Hand sketch (unverified until this script and an independent checker agree):
  Lemma 1: a*b = c*d  implies  a = c.
           Reason: a = f(x)*(a*b) = f(x)*(c*d) = c.
  Lemma 2: f(a) = f(b) for all a, b.
           Reason: any element y equals f(a)*(y*z) and f(b)*(y*z); apply Lemma 1.
  Lemma 3: x = y for all x, y (the law collapses every structure to one element).
Each lemma is checked as: assumptions AND NOT(lemma) is unsat.

A chain of z3 'unsat' answers has status z3-only. It is NOT an independent certificate.

Run from repo root: .venv/Scripts/python.exe problems/laws-without-small-models/lemma_chain_f_x_yz.py
"""
import z3

S = z3.DeclareSort("S")
mul = z3.Function("mul", S, S, S)
f = z3.Function("f", S, S)


def V(*names):
    return [z3.Const(n, S) for n in names]


x, y, z = V("x", "y", "z")
L = z3.ForAll([x, y, z], mul(f(x), mul(y, z)) == y)


def check(name, assumptions, negated_goal, timeout=20000):
    s = z3.Solver()
    s.set("timeout", timeout)
    for a in assumptions:
        s.add(a)
    s.add(negated_goal)
    r = str(s.check())
    print(f"{name}: {r}  (unsat = lemma holds)")
    return r == "unsat"


a, b, c, d = V("a", "b", "c", "d")

# Lemma 1
l1_stmt = z3.ForAll([a, b, c, d], z3.Implies(mul(a, b) == mul(c, d), a == c))
ok1 = check("Lemma 1 (a*b = c*d -> a = c)", [L], z3.And(mul(a, b) == mul(c, d), a != c))

# Lemma 2
l2_stmt = z3.ForAll([a, b], f(a) == f(b))
ok2 = check("Lemma 2 (f constant)", [L, l1_stmt], f(a) != f(b))

# Lemma 3 first attempt (no hint). z3 returned 'unknown': the proof needs L instantiated at y*z.
ok3_nohint = check("Lemma 3 no hint (collapse x = y)", [L, l1_stmt, l2_stmt], a != b, timeout=5000)

# Lemma 3 revised. Hand proof: let e = y*z. Instance of L at (x:=a, y:=e, z:=z):
#   f(a)*(e*z) = e = y*z.   Lemma 1 on  f(a)*(e*z) = y*z  gives  f(a) = y.
# So every y equals f(a), hence any two elements are equal.
inst = mul(f(a), mul(mul(b, c), c)) == mul(b, c)  # L at x:=a, y:=b*c, z:=c  (a plain instance of L)
ok3a = check("Lemma 3a (f(a) = b)", [L, l1_stmt, inst], f(a) != b)
l3a_stmt = z3.ForAll([a, b], f(a) == b)
ok3 = ok3a and check("Lemma 3 (collapse c = d)", [l3a_stmt], c != d)

print("CHAIN COMPLETE (z3-only)" if (ok1 and ok2 and ok3) else "CHAIN NOT COMPLETE")
