"""Independent check of the structures stored in results/zero_model_laws.json.

Self-contained: own parser, own evaluator, no z3, no numpy. For every entry with a structure it
checks that the structure satisfies the law (so the law does NOT force one element).

Law text grammar:  term := factor ['*' factor];  factor := VAR | 'f(' term ')' | '(' term ')'
Variables: letters of VARS.

Usage:
  python verify_models.py results/zero_model_laws.json
  python verify_models.py --selftest results/zero_model_laws.json   (corrupted input must FAIL)
"""
import copy
import itertools
import json
import sys

VARS = "xyzwuvabcdefgh"


def parse_term(s, i):
    a, i = parse_factor(s, i)
    if i < len(s) and s[i] == "*":
        b, i = parse_factor(s, i + 1)
        a = ("m", a, b)
    return a, i


def parse_factor(s, i):
    if s[i] == "(":
        t, i = parse_term(s, i + 1)
        assert s[i] == ")"
        return t, i + 1
    if s.startswith("f(", i):
        t, i = parse_term(s, i + 2)
        assert s[i] == ")"
        return ("f", t), i + 1
    return ("v", VARS.index(s[i])), i + 1


def parse_law(text):
    lhs, rhs = text.split(" = ")
    l, i = parse_term(lhs, 0)
    r, j = parse_term(rhs, 0)
    assert i == len(lhs) and j == len(rhs), text
    return l, r


def variables(t, acc):
    if t[0] == "v":
        acc.add(t[1])
    else:
        for c in t[1:]:
            variables(c, acc)
    return acc


def ev(t, env, mul, f):
    if t[0] == "v":
        return env[t[1]]
    if t[0] == "f":
        return f[ev(t[1], env, mul, f)]
    return mul[ev(t[1], env, mul, f)][ev(t[2], env, mul, f)]


def holds(mul, f, law):
    vs = sorted(variables(law[0], set()) | variables(law[1], set()))
    for vals in itertools.product(range(len(f)), repeat=len(vs)):
        env = dict(zip(vs, vals))
        if ev(law[0], env, mul, f) != ev(law[1], env, mul, f):
            return False
    return True


def well_formed(m):
    n = len(m["f"])
    return (n >= 2 and len(m["mul"]) == n and all(len(r) == n for r in m["mul"])
            and all(0 <= v < n for r in m["mul"] for v in r) and all(0 <= v < n for v in m["f"]))


def verify(report):
    ok = bad = 0
    for e in report:
        if not e.get("model"):
            continue
        m = e["model"]
        if well_formed(m) and holds(m["mul"], m["f"], parse_law(e["law"])):
            ok += 1
        else:
            bad += 1
            print("FAILED:", e["law"])
    return ok, bad


def selftest(report):
    entries = [e for e in report if e.get("model")]
    assert entries, "no structures to test"
    caught = 0
    for e in entries:
        # the structure must violate a law that it was not built for
        other = parse_law("x*y = x") if e["law"] != "x*y = x" else parse_law("x*y = y")
        if not holds(e["model"]["mul"], e["model"]["f"], other):
            caught += 1
    m = copy.deepcopy(entries[0]["model"])
    broken = 0
    n = len(m["f"])
    law = parse_law(entries[0]["law"])
    for i in range(n):
        for j in range(n):
            mm = copy.deepcopy(m)
            mm["mul"][i][j] = (mm["mul"][i][j] + 1) % n
            if not holds(mm["mul"], mm["f"], law):
                broken += 1
    print(f"selftest: wrong-law caught for {caught}/{len(entries)} structures; "
          f"{broken}/{n * n} single-entry corruptions of the first structure break its law")
    if caught == 0 or broken == 0:
        print("SELFTEST FAILED: the checker did not react to corrupted input")
        sys.exit(1)
    print("selftest passed")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    report = json.load(open(args[0]))
    if "--selftest" in sys.argv:
        selftest(report)
        return
    ok, bad = verify(report)
    print(f"{ok} structures verified, {bad} failed")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
