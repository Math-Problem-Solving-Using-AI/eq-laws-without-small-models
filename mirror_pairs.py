"""Check the mirror pairs among the nine laws by machine.

Mirror of a term: read every product a*b as b*a, everywhere (f stays as it is). Mirror of a
structure: the same elements and the same f, with the new product x *' y := y * x. Evaluating a
term in the mirror structure gives the same element as evaluating its mirror term in the original
structure, so a structure satisfies a law exactly when its mirror structure satisfies the mirror
law. A law and its mirror law therefore have the same answer (collapse, finite model, or only
infinite models). That argument is by hand; this script checks what can be checked:

Part 1 (plain Python): mirror each law of results/zero_model_laws.json, rename its variables in
  order of first appearance, and find the law of the list with the same normal form (a law s = t
  is the same law as t = s, so both orientations are tried). Every law must have exactly one
  partner, and the pairs must be the ones the README states (EXPECTED below).
Part 2 (plain Python): the two 4-element models, with their tables transposed (that is the mirror
  structure), satisfy the partner law, checked on every assignment.
Part 3 (z3, all terms): each of the four infinite term models of term_models_z3.py, mirrored,
  satisfies the partner law as stored in the list. The law is turned into z3 terms from its text,
  not written by hand. Status of a pass: z3-only.

Optional: --laws-list PATH reads a JSON list of entries with a "text" field (for example
data/laws_3.json of eq-unary-magma-laws) and reports how many of its laws have their mirror in the
same list.

Usage (from the repository root):
  python mirror_pairs.py
  python mirror_pairs.py --selftest      (corrupted mirrors, pairs and models must FAIL)
  python mirror_pairs.py --laws-list ../eq-unary-magma-laws/data/laws_3.json
"""
import copy
import json
import sys
from pathlib import Path

import z3

from check_derivation import equation, show
import term_models_z3 as tm

LAWS_FILE = Path(__file__).resolve().parent / "results" / "zero_model_laws.json"
NAMES = "xyzwuv"

# The mirror pairs stated in README.md (step 07). A self-mirror law is its own partner.
EXPECTED = {
    "f(x*(y*z)) = y": "f((x*y)*z) = y",
    "x*(y*f(z)) = y": "(f(x)*y)*z = y",
    "f(x)*(y*z) = y": "(x*y)*f(z) = y",
    "(x*y)*(y*x) = y": "(x*y)*(y*x) = y",
    "(x*y)*(y*z) = y": "(x*y)*(y*z) = y",
}
EXPECTED.update({b: a for a, b in list(EXPECTED.items())})

# The four infinite models of term_models_z3.py: (law of the model, product, f).
TERM_MODELS = [
    ("f(x*(y*z)) = y", tm.mulA, tm.fA),
    ("x*(y*f(z)) = y", tm.mulB, tm.fB),
    ("(f(x)*y)*z = y", tm.mulC, tm.fC),
    ("f((x*y)*z) = y", tm.mulD, tm.fD),
]


def mirror(t):
    if t[0] == "v":
        return t
    if t[0] == "f":
        return ("f", mirror(t[1]))
    return ("*", mirror(t[2]), mirror(t[1]))


def rename(t, names):
    if t[0] == "v":
        if t[1] not in names:
            names[t[1]] = ("v", NAMES[len(names)])
        return names[t[1]]
    return (t[0],) + tuple(rename(c, names) for c in t[1:])


def normal(lhs, rhs):
    """The same text for laws that differ only by variable names or by the side they are written on."""
    forms = []
    for a, b in ((lhs, rhs), (rhs, lhs)):
        names = {}
        a, b = rename(a, names), rename(b, names)
        forms.append(f"{show(a)} = {show(b)}")
    return min(forms)


def mirror_law(text, mirror_fn=mirror):
    lhs, rhs = equation(text)
    return mirror_fn(lhs), mirror_fn(rhs)


def partners(laws, mirror_fn=mirror, normal_fn=normal):
    """For each law, the laws of the list whose normal form equals that of its mirror."""
    key = {text: normal_fn(*equation(text)) for text in laws}
    return {text: [o for o in laws if key[o] == normal_fn(*mirror_law(text, mirror_fn))] for text in laws}


def check_pairs(laws, mirror_fn=mirror, normal_fn=normal, expected=EXPECTED, verbose=True):
    ok = True
    for text, found in partners(laws, mirror_fn, normal_fn).items():
        m = mirror_law(text, mirror_fn)
        good = found == [expected.get(text)] if text in expected else found == []
        if verbose:
            print(f"  {text:18s} mirror {show(m[0])} = {show(m[1])}  partner in list: "
                  f"{', '.join(found) or 'none'}  {'ok' if good else 'FAILED'}")
        ok = ok and good
    for text in laws:
        lhs, rhs = equation(text)
        ok = ok and mirror(mirror(lhs)) == lhs and mirror(mirror(rhs)) == rhs
    return ok


def ev(t, env, mul, f):
    if t[0] == "v":
        return env[t[1]]
    if t[0] == "f":
        return f[ev(t[1], env, mul, f)]
    return mul[ev(t[1], env, mul, f)][ev(t[2], env, mul, f)]


def variables(t):
    return {t[1]} if t[0] == "v" else set().union(*(variables(c) for c in t[1:]))


def holds_table(mul, f, text):
    lhs, rhs = equation(text)
    vs = sorted(variables(lhs) | variables(rhs))
    n = len(f)
    for k in range(n ** len(vs)):
        env = {v: (k // n ** i) % n for i, v in enumerate(vs)}
        if ev(lhs, env, mul, f) != ev(rhs, env, mul, f):
            return False
    return True


def transpose(mul):
    return [list(col) for col in zip(*mul)]


def check_tables(report, mirror_table=transpose, expected=EXPECTED, verbose=True):
    ok = True
    for e in report:
        if not e.get("model"):
            continue
        mul, f = e["model"]["mul"], e["model"]["f"]
        partner = expected[e["law"]]
        good = holds_table(mirror_table(mul), f, partner)
        if verbose:
            same = "same table" if mirror_table(mul) == mul else "a different table"
            print(f"  {e['law']}: transposed table ({same}) satisfies {partner}: {'ok' if good else 'FAILED'}")
        ok = ok and good
    return ok


def zev(t, env, mul, f):
    if t[0] == "v":
        return env[t[1]]
    if t[0] == "f":
        return f(zev(t[1], env, mul, f))
    return mul(zev(t[1], env, mul, f), zev(t[2], env, mul, f))


def failure_exists(mul, f, text, timeout=60000):
    """z3's answer to: are there terms where the law (given as text) fails in the model?"""
    lhs, rhs = equation(text)
    env = {v: z3.Const(v, tm.T) for v in sorted(variables(lhs) | variables(rhs))}
    s = z3.Solver()
    s.set("timeout", timeout)
    s.add(zev(lhs, env, mul, f) != zev(rhs, env, mul, f))
    return str(s.check())


def mirrored(mul):
    return lambda x, y: mul(y, x)


def check_term_models(models=TERM_MODELS, mirror_mul=mirrored, expected=EXPECTED, verbose=True):
    ok = True
    for law, mul, f in models:
        r_own = failure_exists(mul, f, law)
        r_mir = failure_exists(mirror_mul(mul), f, expected[law])
        if verbose:
            print(f"  model of {law}: fails its own law (from text)? {r_own};  mirrored, fails "
                  f"{expected[law]}? {r_mir}  (unsat = holds on all terms)")
        ok = ok and r_own == "unsat" and r_mir == "unsat"
    return ok


def main(report):
    laws = [e["law"] for e in report]
    print("Part 1: mirror pairs among the nine laws (plain Python)")
    ok1 = check_pairs(laws)
    print("Part 2: the 4-element models, mirrored (plain Python, every assignment)")
    ok2 = check_tables(report)
    print("Part 3: the infinite term models, mirrored (z3 on all terms, z3-only)")
    ok3 = check_term_models()
    return ok1 and ok2 and ok3


def selftest(report):
    laws = [e["law"] for e in report]

    def no_swap(t):  # products not reversed
        return t

    def swap_top(t):  # only the outermost product reversed
        if t[0] == "*":
            return ("*", t[2], t[1])
        return (t[0],) + tuple(swap_top(c) for c in t[1:]) if t[0] == "f" else t

    def no_rename(lhs, rhs):  # variable names not normalised
        return min(f"{show(lhs)} = {show(rhs)}", f"{show(rhs)} = {show(lhs)}")

    wrong_pairs = dict(EXPECTED)
    wrong_pairs["f(x*(y*z)) = y"] = "(f(x)*y)*z = y"
    wrong_pairs["(f(x)*y)*z = y"] = "f(x*(y*z)) = y"

    report_bad = copy.deepcopy(report)
    for e in report_bad:
        if e.get("model"):
            row = e["model"]["mul"][1]
            row[2] = (row[2] + 1) % len(row)

    def bad_model(mul):  # mirrored model with the wrong product for (x, x)
        return lambda x, y: z3.If(x == y, tm.F(x), mul(y, x))

    mutations = [
        ("mirror that reverses no product", lambda: check_pairs(laws, mirror_fn=no_swap, verbose=False)),
        ("mirror that reverses only the outermost product", lambda: check_pairs(laws, mirror_fn=swap_top, verbose=False)),
        ("normal form without renaming variables", lambda: check_pairs(laws, normal_fn=no_rename, verbose=False)),
        ("wrong expected pairs", lambda: check_pairs(laws, expected=wrong_pairs, verbose=False)),
        ("4-element tables with one entry changed", lambda: check_tables(report_bad, verbose=False)),
        ("4-element tables checked against a wrong law", lambda: check_tables(
            report, expected={e["law"]: "f(x*(y*z)) = y" for e in report}, verbose=False)),
        ("term models not mirrored", lambda: check_term_models(mirror_mul=lambda m: m, verbose=False)),
        ("term models mirrored, checked against wrong pairs", lambda: check_term_models(expected=wrong_pairs, verbose=False)),
        ("term models mirrored with a wrong product on (x, x)", lambda: check_term_models(mirror_mul=bad_model, verbose=False)),
    ]
    caught = 0
    for name, run in mutations:
        passed = run()
        print(f"mutation {name}: {'NOT CAUGHT' if passed else 'rejected'}")
        caught += not passed
    print(f"selftest: {caught} of {len(mutations)} corrupted checks rejected")
    return caught == len(mutations)


def laws_list(path):
    texts = [e["text"] for e in json.load(open(path))]
    keys = {normal(*equation(t)) for t in texts}
    missing = [t for t in texts if normal(*mirror_law(t)) not in keys]
    selfm = [t for t in texts if normal(*mirror_law(t)) == normal(*equation(t))]
    print(f"{len(texts)} laws, {len(keys)} different normal forms, {len(selfm)} are their own mirror, "
          f"{len(texts) - len(missing)} have their mirror in the list, {len(missing)} do not")
    for t in missing[:20]:
        print("  mirror not in list:", t)
    return True


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--laws-list" in args:
        passed = laws_list(args[args.index("--laws-list") + 1])
    else:
        report = json.load(open(LAWS_FILE))
        passed = selftest(report) if "--selftest" in args else main(report)
    print("ALL PASS" if passed else "SOME FAILED")
    sys.exit(0 if passed else 1)
