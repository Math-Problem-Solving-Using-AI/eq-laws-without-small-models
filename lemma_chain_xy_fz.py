"""Check a HAND-DERIVED collapse proof by z3, one lemma at a time.

Law L:  (x*y)*f(z) = y
Hand proof (step 05; the same proof is stored step by step in results/collapse_xy_fz.json and
checked without z3 by check_derivation.py):
  Lemma 1: b*f(d) = f(c) for all b, c, d.
           Reason: L at (x:=a, y:=b, z:=c) gives (a*b)*f(c) = b. L at (x:=a*b, y:=f(c), z:=d)
           gives ((a*b)*f(c))*f(d) = f(c). Replace (a*b)*f(c) by b in the second.
  Lemma 2: b = f(c) for all b, c.
           Reason: L gives (a*b)*f(d) = b, Lemma 1 at b:=a*b gives (a*b)*f(d) = f(c).
  Lemma 3: b = e for all b, e (collapse).
Each lemma is checked as: assumptions AND NOT(lemma) is unsat.

A chain of z3 'unsat' answers has status z3-only. It is NOT an independent certificate.

Run from repo root: python lemma_chain_xy_fz.py
"""
import z3

S = z3.DeclareSort("S")
mul = z3.Function("mul", S, S, S)
f = z3.Function("f", S, S)


def V(*names):
    return [z3.Const(n, S) for n in names]


x, y, z = V("x", "y", "z")
L = z3.ForAll([x, y, z], mul(mul(x, y), f(z)) == y)


def check(name, assumptions, negated_goal, timeout=20000):
    s = z3.Solver()
    s.set("timeout", timeout)
    for a in assumptions:
        s.add(a)
    s.add(negated_goal)
    r = str(s.check())
    print(f"{name}: {r}  (unsat = lemma holds)")
    return r == "unsat"


a, b, c, d, e = V("a", "b", "c", "d", "e")

# Lemma 1, with the two instances of L from the hand proof given as plain assumptions
i1 = mul(mul(a, b), f(c)) == b
i2 = mul(mul(mul(a, b), f(c)), f(d)) == f(c)
ok1 = check("Lemma 1 (b*f(d) = f(c))", [L, i1, i2], mul(b, f(d)) != f(c))
l1_stmt = z3.ForAll([b, c, d], mul(b, f(d)) == f(c))

# Lemma 2
ok2 = check("Lemma 2 (b = f(c))", [L, l1_stmt], b != f(c))
l2_stmt = z3.ForAll([b, c], b == f(c))

# Lemma 3
ok3 = check("Lemma 3 (collapse b = e)", [l2_stmt], b != e)

# The whole claim in one call, no hints (informational: z3 may or may not find it alone)
check("Whole claim without lemmas (informational)", [L], b != e, timeout=5000)

print("CHAIN COMPLETE (z3-only)" if (ok1 and ok2 and ok3) else "CHAIN NOT COMPLETE")
