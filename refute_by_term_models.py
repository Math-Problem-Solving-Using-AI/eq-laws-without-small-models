"""Use the four infinite term models to show that a law does NOT imply other laws.

If a structure M satisfies law A and some law B fails in M at explicit elements, then A does not
imply B ("implies" over all structures, infinite ones included, as in the main repository). The
four models A to D of term_models_z3.py satisfy the four laws below (z3-only on all terms).

For every law of the main repository's list (712 laws) and every model, this script looks for
elements where the law fails:
  1. plain search: every assignment of the law's variables to the 89 terms with at most 7
     constructors (G, F(t), P(a, b)), smallest first;
  2. for laws where the search finds nothing: z3 on all terms (60 s). `sat` gives the elements,
     `unsat` means the law holds in the model on all terms (z3-only), so this model cannot refute it.
The laws are read from the JSON term trees of the list (not from the law texts), so that the
checker, which reads only the texts, does not share this script's reading of the laws.

Elements are written in constructor notation: G, F(t), P(a,b). These name elements of the term
model; they are not operations of the model (in model A, f(G) is G, while F(G) is another element).

Output: results/refutations_term_models.json. Re-check with check_refutations.py (plain Python).

Usage: python refute_by_term_models.py [path to eq-unary-magma-laws/data/laws_3.json]
"""
import itertools
import json
import sys
from pathlib import Path

import z3

import term_models_z3 as tm

ROOT = Path(__file__).resolve().parent
LAWS_DEFAULT = ROOT.parent / "eq-unary-magma-laws" / "data" / "laws_3.json"
OUT = ROOT / "results" / "refutations_term_models.json"
VARS = "xyzwuvabcdefgh"  # variable i of a term tree is printed as VARS[i] in the law texts
MAX_SIZE = 7

# model name: (law of the model, product, f) as plain-Python functions on tuples
G = ("G",)


def _isP(t):
    return t[0] == "P"


def _isF(t):
    return t[0] == "F"


MODELS = {
    "A": ("f(x*(y*z)) = y", lambda x, y: ("P", x, y),
          lambda t: t[2][1] if _isP(t) and _isP(t[2]) else t),
    "B": ("x*(y*f(z)) = y", lambda x, w: w[1] if _isP(w) and _isF(w[2]) else ("P", x, w),
          lambda t: ("F", t)),
    "C": ("(f(x)*y)*z = y", lambda u, z: u[2] if _isP(u) and _isF(u[1]) else ("P", u, z),
          lambda t: ("F", t)),
    "D": ("f((x*y)*z) = y", lambda x, y: ("P", x, y),
          lambda t: t[1][2] if _isP(t) and _isP(t[1]) else t),
}
Z3_MODELS = {"A": (tm.mulA, tm.fA), "B": (tm.mulB, tm.fB), "C": (tm.mulC, tm.fC), "D": (tm.mulD, tm.fD)}
DEFINITIONS = {
    "A": "x*y = P(x,y);  f(t) = b if t = P(x,P(b,z)), else t",
    "B": "f(t) = F(t);  x*w = b if w = P(b,F(z)), else P(x,w)",
    "C": "f(t) = F(t);  u*z = b if u = P(F(t),b), else P(u,z)",
    "D": "x*y = P(x,y);  f(t) = b if t = P(P(a,b),z), else t",
}
PARTNER = {"A": "D", "D": "A", "B": "C", "C": "B"}


def terms(n):
    """All constructor terms with exactly n constructors."""
    if n == 1:
        return [G]
    out = [("F", t) for t in terms(n - 1)]
    for i in range(1, n - 1):
        out += [("P", a, b) for a in terms(i) for b in terms(n - 1 - i)]
    return out


POOL = [t for n in range(1, MAX_SIZE + 1) for t in terms(n)]


def ev(t, vals, mul, f):
    if t[0] == "v":
        return vals[t[1]]
    if t[0] == "f":
        return f(ev(t[1], vals, mul, f))
    return mul(ev(t[1], vals, mul, f), ev(t[2], vals, mul, f))


def name(t):
    if t[0] == "G":
        return "G"
    return f"{t[0]}({','.join(name(c) for c in t[1:])})"


def from_z3(e):
    k = e.decl().name()
    if k == "G":
        return G
    return (k,) + tuple(from_z3(c) for c in e.children())


def zev(t, env, mul, f):
    if t[0] == "v":
        return env[t[1]]
    if t[0] == "f":
        return f(zev(t[1], env, mul, f))
    return mul(zev(t[1], env, mul, f), zev(t[2], env, mul, f))


def tuplify(t):
    return (t[0],) + tuple(c if isinstance(c, int) else tuplify(c) for c in t[1:])


def refute(model, entry):
    """(elements, how) where the law fails in the model, or (None, z3 answer)."""
    _, mul, f = MODELS[model]
    lhs, rhs = (tuplify(s) for s in entry["law"])
    for vals in itertools.product(POOL, repeat=entry["vars"]):
        if ev(lhs, vals, mul, f) != ev(rhs, vals, mul, f):
            return vals, "search"
    zmul, zf = Z3_MODELS[model]
    env = [z3.Const(VARS[i], tm.T) for i in range(entry["vars"])]
    s = z3.Solver()
    s.set("timeout", 60000)
    s.add(zev(lhs, env, zmul, zf) != zev(rhs, env, zmul, zf))
    r = str(s.check())
    if r == "sat":
        return tuple(from_z3(s.model().eval(c, model_completion=True)) for c in env), "z3"
    return None, r


def main(laws_path):
    entries = json.load(open(laws_path))
    by_text = {e["text"]: e for e in entries}
    certificates, not_refuted = [], []
    for model, (law, mul, f) in MODELS.items():
        source = by_text[law]
        counts = {}
        for e in entries:
            if e["id"] == source["id"]:
                continue
            vals, how = refute(model, e)
            counts[how] = counts.get(how, 0) + 1
            if vals is None:
                not_refuted.append({"model": model, "target_id": e["id"], "target": e["text"], "z3": how})
                continue
            lhs, rhs = (tuplify(s) for s in e["law"])
            certificates.append({
                "model": model, "target_id": e["id"], "target": e["text"],
                "at": {VARS[i]: name(v) for i, v in enumerate(vals)},
                "lhs": name(ev(lhs, vals, mul, f)), "rhs": name(ev(rhs, vals, mul, f)),
                "found_by": how,
            })
        print(f"model {model} ({law}, law id {source['id']}): {counts}", flush=True)
    out = {
        "about": "Each certificate says: in the term model `model`, which satisfies the model's law "
                 "(z3-only, term_models_z3.py), the target law fails at the elements `at`; so the "
                 "model's law does not imply the target law (over all structures, infinite ones "
                 "included). `lhs` and `rhs` are the two sides' values there. `not_refuted` lists "
                 "targets for which no failure was found; `z3` is z3's answer to 'does the target "
                 "fail somewhere in the model' (unsat = it holds on all terms, z3-only).",
        "laws": f"{len(entries)} laws of eq-unary-magma-laws data/laws_3.json",
        "elements": "constructor terms: G, F(t), P(a,b); different terms are different elements",
        "models": {m: {"law": MODELS[m][0], "definition": DEFINITIONS[m], "mirror_partner": PARTNER[m]}
                   for m in MODELS},
        "certificates": certificates,
        "not_refuted": not_refuted,
    }
    json.dump(out, open(OUT, "w"), indent=1)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(certificates)} certificates, {len(not_refuted)} not refuted")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else LAWS_DEFAULT)
