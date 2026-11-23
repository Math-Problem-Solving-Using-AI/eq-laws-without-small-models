"""Mirror a stored collapse derivation: a second route to the collapse of the mirror law.

Mirror of a term: read every product a*b as b*a, everywhere (f stays as it is). If a derivation
proves x = y from law L, then the same derivation with every term mirrored proves x = y from the
mirror of L. This script builds that mirrored derivation step by step:
  - every claim, every "in" term and every substituted term is mirrored;
  - every rewrite path has 1 and 2 swapped where it passes through a product (not through f);
  - the mirror law is matched against the stored law text of its partner, and the substitutions
    of "law" steps are renamed to the partner's variable names (an error if the match fails).
The output is NOT trusted: check_derivation.py checks it like any other derivation. This script
only writes it, and with --check confirms that the stored files are what it would write now and
that mirroring twice gives back the source derivation. --selftest builds the mirrored derivations
with deliberately broken mirror rules and confirms that check_derivation.py rejects every one, and
that --check notices a stored file that differs.

Usage (from the repository root):
  python mirror_derivation.py           (writes the two mirrored files listed in JOBS)
  python mirror_derivation.py --check   (exit 1 if a stored file differs or mirroring twice fails)
  python mirror_derivation.py --selftest
"""
import json
import sys
from pathlib import Path

import check_derivation
from check_derivation import Bad, equation, parse, show

ROOT = Path(__file__).resolve().parent
# (source derivation, partner law as stored in results/zero_model_laws.json, output file)
JOBS = [
    ("results/collapse_xy_fz.json", "f(x)*(y*z) = y", "results/collapse_fx_yz_by_mirror.json"),
    ("results/collapse_fx_yz.json", "(x*y)*f(z) = y", "results/collapse_xy_fz_by_mirror.json"),
]


def mirror(t):
    if t[0] == "v":
        return t
    if t[0] == "f":
        return ("f", mirror(t[1]))
    return ("*", mirror(t[2]), mirror(t[1]))


def mirror_path(t, path):
    out = []
    for k in path:
        if t[0] == "*":
            out.append(3 - k)
        elif t[0] == "f" and k == 1:
            out.append(1)
        else:
            raise Bad(f"bad path {path} in {show(t)}")
        t = t[k]
    return out


def match(p, t, names):
    """Rename the variables of p so that p becomes t; names is filled with p-variable -> t-variable."""
    if p[0] == "v":
        if t[0] != "v" or names.setdefault(p[1], t[1]) != t[1]:
            raise Bad("mirror law does not match the partner law")
        return
    if p[0] != t[0]:
        raise Bad("mirror law does not match the partner law")
    for a, b in zip(p[1:], t[1:]):
        match(a, b, names)


def mirror_text(text):
    return show(mirror(parse(text)))


def mirror_cert(cert, partner):
    lhs, rhs = equation(cert["law"])
    plhs, prhs = equation(partner)
    names = {}
    match(mirror(lhs), plhs, names)
    match(mirror(rhs), prhs, names)
    if len(set(names.values())) != len(names):
        raise Bad("variable renaming is not one-to-one")
    steps = []
    for st in cert["steps"]:
        new = {"id": st["id"], "rule": st["rule"]}
        if "from" in st:
            new["from"] = st["from"]
        if st["rule"] == "law":
            new["subst"] = {names[v]: mirror_text(t) for v, t in st["subst"].items()}
        elif "subst" in st:
            new["subst"] = {v: mirror_text(t) for v, t in st["subst"].items()}
        if st["rule"] == "rewrite":
            new["in"] = mirror_text(st["in"])
            new["at"] = mirror_path(parse(st["in"]), st["at"])
        new["claim"] = " = ".join(mirror_text(side) for side in st["claim"].split(" = "))
        steps.append(new)
    return {
        "law": partner,
        "comment": f"Mirror (every a*b read as b*a) of the derivation in {cert['source_file']}, built by "
                   f"mirror_derivation.py; variables of the mirror law renamed to those of the stored law "
                   f"{dict(sorted(names.items()))}. "
                   "Checked by check_derivation.py, not trusted on its own.",
        "steps": steps,
    }


def load(path):
    cert = json.loads((ROOT / path).read_text(encoding="utf-8"))
    cert["source_file"] = path
    return cert


def dump(cert):
    lines = ",\n".join("  " + json.dumps(st, ensure_ascii=False) for st in cert["steps"])
    return (f'{{\n "law": {json.dumps(cert["law"])},\n "comment": {json.dumps(cert["comment"])},\n'
            f' "steps": [\n{lines}\n ]\n}}\n')


def check_stored(out, text):
    path = ROOT / out
    return path.exists() and path.read_text(encoding="utf-8") == text


def selftest():
    """Broken mirror rules must give derivations that check_derivation.py rejects."""
    global mirror, mirror_path, match, check_stored
    good = (mirror, mirror_path, match, check_stored)

    def no_swap_path(t, path):
        return list(path)

    def no_rename(p, t, names):
        for v in "xyzw":
            names[v] = v

    def keep(field):
        """Undo the mirroring of one field: every step gets the source step's value back."""
        def undo(new, old):
            for a, b in zip(new["steps"], old["steps"]):
                if field in b:
                    a[field] = dict(zip(a[field], b[field].values())) if field == "subst" else b[field]
        return undo

    broken = [
        ("rewrite paths not swapped", dict(mirror_path=no_swap_path), None),
        ("law variables not renamed", dict(match=no_rename), None),
        ("substituted terms not mirrored", {}, keep("subst")),
        ("rewritten terms not mirrored", {}, keep("in")),
        ("claims not mirrored", {}, keep("claim")),
    ]
    laws = [e["law"] for e in json.loads(check_derivation.LAWS_FILE.read_text(encoding="utf-8"))]
    ok = True
    for src, partner, out in JOBS:
        for name, patch, undo in broken:
            mirror, mirror_path, match, check_stored = good
            globals().update(patch)
            try:
                new = mirror_cert(load(src), partner)
                if undo:
                    undo(new, load(src))
                check_derivation.check(new, laws)
                print(f"  {src}, {name}: NOT CAUGHT")
                ok = False
            except (Bad, KeyError, TypeError, IndexError) as e:
                print(f"  {src}, {name}: rejected ({e})")
        mirror, mirror_path, match, check_stored = good
        text = dump(mirror_cert(load(src), partner))
        changed = text.replace('"b = e"', '"e = b"', 1)
        caught = changed != text and not check_stored(out, changed)
        print(f"  {out}, stored file changed: {'noticed' if caught else 'NOT NOTICED'}")
        ok = ok and caught
    print("ALL PASS" if ok else "FAILED")
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    check = "--check" in argv
    ok = True
    for src, partner, out in JOBS:
        cert = load(src)
        new = mirror_cert(cert, partner)
        text = dump(new)
        if check:
            same = check_stored(out, text)
            back = mirror_cert(dict(new, source_file=out), cert["law"])
            twice = back["steps"] == cert["steps"]
            print(f"{out}: {'same as a fresh mirror' if same else 'DIFFERS from a fresh mirror'}; "
                  f"mirroring twice gives back {src}: {'yes' if twice else 'NO'}")
            ok = ok and same and twice
        else:
            (ROOT / out).write_text(text, encoding="utf-8")
            print(f"{src} -> {out}: law {partner!r}, {len(new['steps'])} steps")
    if check:
        print("ALL PASS" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
