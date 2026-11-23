"""Independent check of the refutation certificates made from the four infinite term models.

Plain Python, no z3. The models are written out again here from their definitions (README, step 06
and 07), not imported; the target laws are read from their TEXT with the parser of
check_derivation.py, while refute_by_term_models.py read them from the JSON term trees.

Elements are constructor terms G, F(t), P(a,b) (different terms are different elements).
  A  law f(x*(y*z)) = y:  x*y = P(x,y);  f(t) = b if t = P(x,P(b,z)), else t
  B  law x*(y*f(z)) = y:  f(t) = F(t);   x*w = b if w = P(b,F(z)), else P(x,w)
  C  law (f(x)*y)*z = y:  f(t) = F(t);   u*z = b if u = P(F(t),b), else P(u,z)
  D  law f((x*y)*z) = y:  x*y = P(x,y);  f(t) = b if t = P(P(a,b),z), else t

Checks:
  1. the file names exactly these four models with these laws and mirror partners (A-D, B-C);
  2. sanity: each model here satisfies its law on every triple of the 17 terms with at most 5
     constructors (a sample; the all-terms check is term_models_z3.py, z3-only);
  3. every certificate: known model, the elements cover exactly the target's variables, the target
     FAILS there, and the stored values of both sides are the computed ones;
  4. coverage: per model, certificates plus `not_refuted` name 711 different laws, the model's own
     law is not among them, and the four models cover the same 712 laws;
  5. every `not_refuted` target is the model's law with its variables replaced by terms (a
     substitution instance), so the model's law implies it in one step of equational logic;
  6. mirror: each certificate, read backwards (every a*b as b*a, in the law and in the elements),
     is a valid certificate for the partner model, and the partner's refuted and not refuted laws
     are exactly the mirrors of this model's.

Usage:
  python check_refutations.py results/refutations_term_models.json
  python check_refutations.py --selftest results/refutations_term_models.json  (corrupted input must FAIL)
"""
import copy
import json
import sys

from check_derivation import Bad, equation

LAWS = {"A": "f(x*(y*z)) = y", "B": "x*(y*f(z)) = y", "C": "(f(x)*y)*z = y", "D": "f((x*y)*z) = y"}
PARTNER = {"A": "D", "D": "A", "B": "C", "C": "B"}
G = ("G",)


# --- elements -------------------------------------------------------------------------------

def element(text):
    s = text.replace(" ", "")
    t, i = _element(s, 0)
    if i != len(s):
        raise Bad(f"trailing text in element {text!r}")
    return t


def _element(s, i):
    if s.startswith("G", i):
        return G, i + 1
    for k, arity in (("F", 1), ("P", 2)):
        if s.startswith(k + "(", i):
            i += 2
            args = []
            for n in range(arity):
                a, i = _element(s, i)
                args.append(a)
                sep = "," if n < arity - 1 else ")"
                if i >= len(s) or s[i] != sep:
                    raise Bad(f"expected {sep!r} in element at {i}")
                i += 1
            return (k, *args), i
    raise Bad(f"bad element text at {i}: {s[i:i + 10]!r}")


def show_element(t):
    return "G" if t == G else f"{t[0]}({','.join(show_element(c) for c in t[1:])})"


# --- the four models, written from their definitions ----------------------------------------

def pair(a, b):
    return ("P", a, b)


def formal_f(t):
    return ("F", t)


def f_A(t):  # f(P(x, P(b, z))) = b
    if t[0] == "P":
        inner = t[2]
        if inner[0] == "P":
            return inner[1]
    return t


def mul_B(x, w):  # x * P(b, F(z)) = b
    if w[0] == "P" and w[2][0] == "F":
        return w[1]
    return ("P", x, w)


def mul_C(u, z):  # P(F(t), b) * z = b
    if u[0] == "P" and u[1][0] == "F":
        return u[2]
    return ("P", u, z)


def f_D(t):  # f(P(P(a, b), z)) = b
    if t[0] == "P":
        inner = t[1]
        if inner[0] == "P":
            return inner[2]
    return t


MODELS = {"A": (pair, f_A), "B": (mul_B, formal_f), "C": (mul_C, formal_f), "D": (pair, f_D)}


def value(t, at, model):
    mul, f = model
    if t[0] == "v":
        return at[t[1]]
    if t[0] == "f":
        return f(value(t[1], at, model))
    return mul(value(t[1], at, model), value(t[2], at, model))


def variables(t):
    return {t[1]} if t[0] == "v" else set().union(*(variables(c) for c in t[1:]))


def small_terms(n):
    if n == 1:
        return [G]
    out = [("F", t) for t in small_terms(n - 1)]
    for i in range(1, n - 1):
        out += [("P", a, b) for a in small_terms(i) for b in small_terms(n - 1 - i)]
    return out


# --- laws: normal form, mirror, instances ---------------------------------------------------

def mirror_term(t):
    if t[0] == "v":
        return t
    if t[0] == "f":
        return ("f", mirror_term(t[1]))
    return ("*", mirror_term(t[2]), mirror_term(t[1]))


def mirror_element(t):
    if t == G:
        return G
    if t[0] == "F":
        return ("F", mirror_element(t[1]))
    return ("P", mirror_element(t[2]), mirror_element(t[1]))


def _rename(t, names):
    if t[0] == "v":
        names.setdefault(t[1], "v%d" % len(names))
        return ("v", names[t[1]])
    return (t[0],) + tuple(_rename(c, names) for c in t[1:])


def normal(lhs, rhs):
    """Same key for laws that differ only by variable names or by which side is written first."""
    keys = []
    for a, b in ((lhs, rhs), (rhs, lhs)):
        names = {}
        keys.append(repr((_rename(a, names), _rename(b, names))))
    return min(keys)


def match(pattern, t, sub):
    """Extend sub so that pattern with sub applied is t; False if impossible."""
    if pattern[0] == "v":
        if pattern[1] in sub:
            return sub[pattern[1]] == t
        sub[pattern[1]] = t
        return True
    return pattern[0] == t[0] and len(pattern) == len(t) and all(
        match(p, c, sub) for p, c in zip(pattern[1:], t[1:]))


def is_instance(law, target):
    (a, b), (s, t) = law, target
    for x, y in ((s, t), (t, s)):
        sub = {}
        if match(a, x, sub) and match(b, y, sub):
            return True
    return False


# --- the check ------------------------------------------------------------------------------

def check_one(c, models, mirror_el=mirror_element, mirror_tm=mirror_term):
    if c["model"] not in models:
        raise Bad(f"unknown model {c['model']!r}")
    lhs, rhs = equation(c["target"])
    vs = variables(lhs) | variables(rhs)
    if set(c["at"]) != vs:
        raise Bad(f"elements given for {sorted(c['at'])}, target variables are {sorted(vs)}")
    at = {v: element(e) for v, e in c["at"].items()}
    model = models[c["model"]]
    left, right = value(lhs, at, model), value(rhs, at, model)
    if left == right:
        raise Bad(f"target {c['target']!r} does not fail in model {c['model']} at {c['at']}")
    if (show_element(left), show_element(right)) != (element_text(c["lhs"]), element_text(c["rhs"])):
        raise Bad(f"stored values differ from computed values for {c['target']!r}")
    # the same certificate read backwards, in the partner model
    partner = models[PARTNER[c["model"]]]
    mat = {v: mirror_el(e) for v, e in at.items()}
    if value(mirror_tm(lhs), mat, partner) == value(mirror_tm(rhs), mat, partner):
        raise Bad(f"mirror of the certificate for {c['target']!r} does not fail in model {PARTNER[c['model']]}")


def element_text(text):
    return show_element(element(text))


def check(data, models=MODELS, mirror_el=mirror_element, mirror_tm=mirror_term):
    """Return per-model counts if everything checks, else raise Bad."""
    got = {m: (d["law"], d["mirror_partner"]) for m, d in data["models"].items()}
    want = {m: (LAWS[m], PARTNER[m]) for m in LAWS}
    if got != want:
        raise Bad(f"models block {got} is not {want}")
    pool = [t for n in range(1, 6) for t in small_terms(n)]
    for m, law in LAWS.items():
        lhs, rhs = equation(law)
        for x, y, z in ((x, y, z) for x in pool for y in pool for z in pool):
            at = {"x": x, "y": y, "z": z}
            if value(lhs, at, models[m]) != value(rhs, at, models[m]):
                raise Bad(f"sanity: model {m} fails its own law {law} at {at}")
    for c in data["certificates"]:
        check_one(c, models, mirror_el, mirror_tm)
    refuted, kept, text_of, raw = {m: set() for m in LAWS}, {m: set() for m in LAWS}, {}, {}
    for kind, rows in (("certificates", data["certificates"]), ("not_refuted", data["not_refuted"])):
        for c in rows:
            key = normal(*equation(c["target"]))
            raw[c["target_id"]] = c["target"]
            if text_of.setdefault(c["target_id"], key) != key:
                raise Bad(f"law id {c['target_id']} has two different texts")
            if c["target_id"] in refuted[c["model"]] | kept[c["model"]]:
                raise Bad(f"law id {c['target_id']} appears twice for model {c['model']}")
            (refuted if kind == "certificates" else kept)[c["model"]].add(c["target_id"])
    ids_by_key = {k: i for i, k in text_of.items()}
    all_ids = set(text_of)
    for m, law in LAWS.items():
        own = ids_by_key.get(normal(*equation(law)))
        ids = refuted[m] | kept[m]
        if len(ids) != 711 or own is None or own in ids or ids | {own} != all_ids or len(all_ids) != 712:
            raise Bad(f"model {m}: {len(ids)} targets, own law id {own}, {len(all_ids)} laws in all")
    for c in data["not_refuted"]:
        if not is_instance(equation(LAWS[c["model"]]), equation(c["target"])):
            raise Bad(f"not refuted {c['target']!r} is not an instance of {LAWS[c['model']]}")
    mirror_key = {i: normal(*(mirror_tm(s) for s in equation(raw[i]))) for i in all_ids}
    for m in LAWS:
        p = PARTNER[m]
        for mine, theirs in ((refuted[m], refuted[p]), (kept[m], kept[p])):
            if {mirror_key[i] for i in mine} != {text_of[i] for i in theirs}:
                raise Bad(f"model {p} is not the mirror of model {m}")
    return {m: (len(refuted[m]), len(kept[m])) for m in LAWS}


def main(path):
    data = json.load(open(path))
    counts = check(data)
    for m, (r, k) in counts.items():
        print(f"model {m} ({LAWS[m]}): {r} laws fail in it (certificates checked), "
              f"{k} not refuted, each an instance of the model's law")
    print(f"{len(data['certificates'])} certificates checked, and each one read backwards in the partner model")
    return True


def selftest(path):
    data = json.load(open(path))
    one_var = next(i for i, c in enumerate(data["certificates"]) if list(c["at"]) == ["x"])

    def edit(fn):
        def run():
            d = copy.deepcopy(data)
            fn(d)
            return check(d)
        return run

    def models_with(**changes):
        ms = dict(MODELS)
        ms.update(changes)
        return lambda: check(data, models=ms)

    def stored_value(d):
        d["certificates"][0]["lhs"] = d["certificates"][0]["rhs"]

    def holding_target(d):  # a target that holds everywhere
        d["certificates"][one_var]["target"] = "f(x) = f(x)"

    def drop_variable(d):
        d["certificates"][0]["at"].pop(sorted(d["certificates"][0]["at"])[0])

    def drop_certificate(d):
        d["certificates"].pop(0)

    def duplicate(d):
        d["certificates"].append(copy.deepcopy(d["certificates"][0]))

    def unknown_model(d):
        d["certificates"][0]["model"] = "E"

    def wrong_law(d):
        d["models"]["A"]["law"] = "f(x*(y*z)) = z"

    def wrong_partner(d):
        d["models"]["B"]["mirror_partner"] = "D"

    def bad_element(d):
        c = d["certificates"][0]
        c["at"][sorted(c["at"])[0]] = "Q(G)"

    def certificate_to_not_refuted(d):
        c = d["certificates"].pop(0)
        d["not_refuted"].append({"model": c["model"], "target_id": c["target_id"], "target": c["target"]})

    def move_model(d):  # a certificate of model B filed under model C
        c = next(c for c in d["certificates"] if c["model"] == "B")
        c["model"] = "C"

    def f_A_returns_z(t):
        if t[0] == "P" and t[2][0] == "P":
            return t[2][2]
        return t

    def mul_C_no_test(u, z):
        if u[0] == "P" and u[1][0] == "F":
            return u[1]
        return ("P", u, z)

    def no_swap(t):
        return t

    mutations = [
        ("stored value of a side changed", edit(stored_value)),
        ("target replaced by a law that always holds", edit(holding_target)),
        ("a variable left without an element", edit(drop_variable)),
        ("one certificate deleted", edit(drop_certificate)),
        ("one certificate duplicated", edit(duplicate)),
        ("unknown model name", edit(unknown_model)),
        ("law of model A changed in the file", edit(wrong_law)),
        ("wrong mirror partner in the file", edit(wrong_partner)),
        ("element text not a constructor term", edit(bad_element)),
        ("a refuted law listed as not refuted", edit(certificate_to_not_refuted)),
        ("a certificate of B filed under C", edit(move_model)),
        ("checker's model A: f returns z", models_with(A=(pair, f_A_returns_z))),
        ("checker's model C: product returns F(t)", models_with(C=(mul_C_no_test, formal_f))),
        ("mirror does not swap elements", lambda: check(data, mirror_el=no_swap)),
        ("mirror does not swap laws", lambda: check(data, mirror_tm=no_swap)),
    ]
    caught = 0
    for name, run in mutations:
        try:
            run()
            print(f"mutation {name}: NOT CAUGHT")
        except (Bad, KeyError, ValueError) as e:
            print(f"mutation {name}: rejected ({type(e).__name__}: {e})")
            caught += 1
    print(f"selftest: {caught} of {len(mutations)} corrupted inputs rejected")
    return caught == len(mutations)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--selftest"]
    path = args[0] if args else "results/refutations_term_models.json"
    try:
        passed = selftest(path) if "--selftest" in sys.argv else main(path)
    except Bad as e:
        print("FAILED:", e)
        passed = False
    print("ALL PASS" if passed else "SOME FAILED")
    sys.exit(0 if passed else 1)
