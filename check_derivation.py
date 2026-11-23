"""Independent check of a collapse derivation (a chain of equational rewriting steps).

Self-contained: own parser, own term code, no z3, no numpy. It checks that every step of a stored
derivation follows by one rule of equational logic from the law or from earlier steps, and that
the last step says two DIFFERENT variables are equal (so the law forces every structure to have
one element).

Rules (each step has "id", "rule", "claim" = "s = t"):
  law      "subst": {var: term}            claim is  subst(lhs) = subst(rhs)  of the law
  inst     "from": id, "subst": {...}      claim is  the earlier equation with subst applied
  sym      "from": id                      claim is  the earlier equation reversed
  trans    "from": [id1, id2]              s = t and t = u  give  s = u
  rewrite  "from": id, "in": term, "at": [i, ...]
           the subterm of "in" at the path equals the left side l of the earlier equation l = r;
           claim is  in = in[path := r].  Path entries: 1 = left factor / argument of f, 2 = right factor.
Only earlier steps may be referenced. The law text must be one of the laws in the results file.

Law text grammar:  term := factor ['*' factor];  factor := VAR | 'f(' term ')' | '(' term ')'
Variables are single letters other than f.

Usage:
  python check_derivation.py results/collapse_xy_fz.json
  python check_derivation.py --selftest results/collapse_xy_fz.json   (corrupted input must FAIL)
"""
import copy
import json
import sys
from pathlib import Path

LAWS_FILE = Path(__file__).resolve().parent / "results" / "zero_model_laws.json"


class Bad(Exception):
    pass


def parse(text):
    s = text.replace(" ", "")
    t, i = _term(s, 0)
    if i != len(s):
        raise Bad(f"trailing text in {text!r}")
    return t


def _term(s, i):
    a, i = _factor(s, i)
    if i < len(s) and s[i] == "*":
        b, i = _factor(s, i + 1)
        a = ("*", a, b)
    return a, i


def _factor(s, i):
    if i >= len(s):
        raise Bad("unexpected end of term")
    if s[i] == "(":
        t, i = _term(s, i + 1)
        if i >= len(s) or s[i] != ")":
            raise Bad("missing )")
        return t, i + 1
    if s.startswith("f(", i):
        t, i = _term(s, i + 2)
        if i >= len(s) or s[i] != ")":
            raise Bad("missing ) after f(")
        return ("f", t), i + 1
    if s[i].isalpha() and s[i] != "f":
        return ("v", s[i]), i + 1
    raise Bad(f"unexpected {s[i]!r}")


def show(t):
    if t[0] == "v":
        return t[1]
    if t[0] == "f":
        return f"f({show(t[1])})"
    a, b = (show(c) if c[0] != "*" else f"({show(c)})" for c in t[1:])
    return f"{a}*{b}"


def equation(text):
    parts = text.split("=")
    if len(parts) != 2:
        raise Bad(f"not an equation: {text!r}")
    return parse(parts[0]), parse(parts[1])


def substitute(t, sub):
    if t[0] == "v":
        return sub.get(t[1], t)
    return (t[0],) + tuple(substitute(c, sub) for c in t[1:])


def subterm(t, path):
    for k in path:
        if t[0] == "v" or not (1 <= k < len(t)):
            raise Bad(f"bad path {path}")
        t = t[k]
    return t


def replace(t, path, new):
    if not path:
        return new
    k = path[0]
    if t[0] == "v" or not (1 <= k < len(t)):
        raise Bad(f"bad path {path}")
    return t[:k] + (replace(t[k], path[1:], new),) + t[k + 1:]


def parse_subst(d):
    out = {}
    for var, term in d.items():
        if len(var) != 1 or not var.isalpha() or var == "f":
            raise Bad(f"bad variable {var!r}")
        out[var] = parse(term)
    return out


def check(cert, laws):
    """Return the final equation (as text) if every step checks, else raise Bad."""
    if cert["law"] not in laws:
        raise Bad(f"law {cert['law']!r} is not one of the laws in {LAWS_FILE.name}")
    lhs, rhs = equation(cert["law"])
    if f"{show(lhs)} = {show(rhs)}" != cert["law"]:
        raise Bad("law text does not round-trip through the parser")
    proved = {}
    last = None
    for st in cert["steps"]:
        sid, rule = st["id"], st["rule"]
        if sid in proved:
            raise Bad(f"{sid}: duplicate id")
        claim = equation(st["claim"])

        def get(ref):
            if ref not in proved:
                raise Bad(f"{sid}: refers to {ref!r}, which is not an earlier step")
            return proved[ref]

        if rule == "law":
            sub = parse_subst(st["subst"])
            expect = (substitute(lhs, sub), substitute(rhs, sub))
        elif rule == "inst":
            s, t = get(st["from"])
            sub = parse_subst(st["subst"])
            expect = (substitute(s, sub), substitute(t, sub))
        elif rule == "sym":
            s, t = get(st["from"])
            expect = (t, s)
        elif rule == "trans":
            (s, t), (t2, u) = get(st["from"][0]), get(st["from"][1])
            if t != t2:
                raise Bad(f"{sid}: trans needs matching middle terms, got {show(t)} and {show(t2)}")
            expect = (s, u)
        elif rule == "rewrite":
            l, r = get(st["from"])
            T = parse(st["in"])
            path = list(st["at"])
            if subterm(T, path) != l:
                raise Bad(f"{sid}: subterm at {path} of {show(T)} is {show(subterm(T, path))}, not {show(l)}")
            expect = (T, replace(T, path, r))
        else:
            raise Bad(f"{sid}: unknown rule {rule!r}")
        if claim != expect:
            raise Bad(f"{sid}: claim {st['claim']!r} does not match the rule, which gives "
                      f"{show(expect[0])} = {show(expect[1])}")
        proved[sid] = claim
        last = claim
    if last is None:
        raise Bad("no steps")
    s, t = last
    if not (s[0] == "v" and t[0] == "v" and s != t):
        raise Bad(f"last step {show(s)} = {show(t)} is not an equation between two different variables")
    return f"{show(s)} = {show(t)}"


def mutations(cert):
    """Corrupted copies of a certificate. Every one of them must be rejected."""
    out = []

    def mut(name, fn):
        c = copy.deepcopy(cert)
        fn(c)
        out.append((name, c))

    steps = cert["steps"]
    mut("law changed to (x*y)*f(z) = x", lambda c: c.update(law="(x*y)*f(z) = x"))
    mut("law changed to a law with a 4-element model", lambda c: c.update(law="(x*y)*(y*z) = y"))
    mut("law text not in the results file", lambda c: c.update(law="(x*y)*f(z)=y"))
    for k, st in enumerate(steps):
        if "subst" in st:
            var = sorted(st["subst"])[0]
            mut(f"{st['id']}: substitution for {var} changed",
                lambda c, k=k, var=var: c["steps"][k]["subst"].__setitem__(var, "f(" + c["steps"][k]["subst"][var] + ")"))
        if st["rule"] == "rewrite":
            mut(f"{st['id']}: rewrite position changed",
                lambda c, k=k: c["steps"][k].__setitem__("at", c["steps"][k]["at"] + [1]))
        if st["rule"] == "trans":
            mut(f"{st['id']}: trans premises swapped",
                lambda c, k=k: c["steps"][k].__setitem__("from", c["steps"][k]["from"][::-1]))
        mut(f"{st['id']}: claim sides swapped",
            lambda c, k=k: c["steps"][k].__setitem__("claim", " = ".join(c["steps"][k]["claim"].split(" = ")[::-1])))
        if k > 0:
            mut(f"{steps[k - 1]['id']}: step removed", lambda c, k=k: c["steps"].pop(k - 1))
    last = steps[-1]
    a, b = last["claim"].split(" = ")
    mut("valid extra steps ending in v = v", lambda c: c["steps"].extend([
        {"id": "Z0", "rule": "sym", "from": last["id"], "claim": f"{b} = {a}"},
        {"id": "Z1", "rule": "trans", "from": [last["id"], "Z0"], "claim": f"{a} = {a}"}]))
    mut("forward reference", lambda c: c["steps"][0].update(rule="sym", **{"from": c["steps"][-1]["id"]}))
    return out


def main(argv):
    selftest = "--selftest" in argv
    paths = [a for a in argv if a != "--selftest"]
    laws = [e["law"] for e in json.loads(LAWS_FILE.read_text(encoding="utf-8"))]
    ok = True
    for p in paths:
        cert = json.loads(Path(p).read_text(encoding="utf-8"))
        try:
            final = check(cert, laws)
            print(f"{p}: law {cert['law']!r}: {len(cert['steps'])} steps checked, last step {final}: COLLAPSE DERIVED")
        except (Bad, KeyError, TypeError, IndexError) as e:
            print(f"{p}: REJECTED: {e}")
            ok = False
            continue
        if selftest:
            muts = mutations(cert)
            caught = 0
            for name, c in muts:
                try:
                    # the law-list guard is tested by one mutation only; for the others it is
                    # lifted, so that the step checks themselves must catch the corruption
                    check(c, laws if name.startswith("law text") else laws + [c["law"]])
                    print(f"  MUTATION NOT CAUGHT: {name}")
                except (Bad, KeyError, TypeError, IndexError):
                    caught += 1
            print(f"  selftest: {caught} of {len(muts)} corrupted copies rejected")
            ok = ok and caught == len(muts)
    print("ALL PASS" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
