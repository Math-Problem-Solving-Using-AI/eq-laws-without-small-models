"""Statement fidelity of the law texts copied into results/refutations_term_models.json.

refute_by_term_models.py read each law from the main repository's stored term tree; the results
file keeps only its id and its text, and check_refutations.py reads the law back from that text
(with the parser of check_derivation.py). This script closes the gap between the two readings:

  1. every id in the results file (certificates, not_refuted, and the four model laws with the
     ids recorded in step 11) is an id of the main repository's list, and always carries the same
     text;
  2. that text is exactly the main repository's text for that id;
  3. the text, read by the parser check_refutations.py uses, is exactly the main repository's term
     tree for that id (tree variable k is letter k of "xyzwuvabcdefgh", the main repository's
     laws.VARS);
  4. the ids used are exactly the main repository's ids 1..712.

It needs the main repository next to this one (read only). Not in CI for that reason.

Usage:
  python check_copied_laws.py results/refutations_term_models.json [path/to/laws_3.json]
  python check_copied_laws.py --selftest results/refutations_term_models.json [path/to/laws_3.json]
"""
import copy
import json
import sys
from pathlib import Path

from check_derivation import Bad, equation

VARS = "xyzwuvabcdefgh"  # eq-unary-magma-laws src/laws.py, line 16
MODEL_LAW_IDS = {"A": 450, "B": 639, "C": 135, "D": 336}  # step 11
DEFAULT_LAWS = Path(__file__).resolve().parent.parent / "eq-unary-magma-laws" / "data" / "laws_3.json"


def from_tree(t, vars_=VARS):
    """Main-repository tree ['m', a, b] / ['f', a] / ['v', k] -> check_derivation's form."""
    if t[0] == "v":
        return ("v", vars_[t[1]])
    if t[0] == "f":
        return ("f", from_tree(t[1], vars_))
    if t[0] == "m":
        return ("*", from_tree(t[1], vars_), from_tree(t[2], vars_))
    raise Bad(f"unknown tree node {t[0]!r}")


def used_laws(data):
    """(id, text, where) for every law the results file names."""
    out = []
    for name, m in data["models"].items():
        if name not in MODEL_LAW_IDS:
            raise Bad(f"unknown model {name!r}")
        out.append((MODEL_LAW_IDS[name], m["law"], f"model {name}"))
    for c in data["certificates"]:
        out.append((c["target_id"], c["target"], f"certificate {c['model']}"))
    for c in data["not_refuted"]:
        out.append((c["target_id"], c["target"], f"not_refuted {c['model']}"))
    return out


def check(data, main, vars_=VARS):
    by_id = {e["id"]: e for e in main}
    if len(by_id) != len(main):
        raise Bad("main repository list has a repeated id")
    seen = {}
    for i, text, where in used_laws(data):
        if i not in by_id:
            raise Bad(f"{where}: id {i} not in the main repository list")
        if seen.setdefault(i, text) != text:
            raise Bad(f"{where}: id {i} carries two texts {seen[i]!r} and {text!r}")
        e = by_id[i]
        if text != e["text"]:
            raise Bad(f"{where}: id {i} text {text!r} is not the main repository's {e['text']!r}")
        tree = tuple(from_tree(side, vars_) for side in e["law"])
        if equation(text) != tree:
            raise Bad(f"{where}: id {i} text {text!r} does not read back to its term tree")
    if set(seen) != set(by_id) or set(by_id) != set(range(1, 713)):
        raise Bad(f"ids used {len(seen)}, main list {len(by_id)}; they are not the same 1..712")
    return len(seen), sum(1 for _ in used_laws(data))


def load(argv):
    res = json.load(open(argv[0]))
    main = json.load(open(argv[1] if len(argv) > 1 else DEFAULT_LAWS))
    return res, main


def main(argv):
    res, laws = load(argv)
    try:
        n, refs = check(res, laws)
    except Bad as e:
        print("FAIL:", e)
        sys.exit(1)
    print(f"{refs} law references in the results file, {n} different ids")
    print("each text equals the main repository's text and reads back to its term tree")
    print("ALL PASS")


def selftest(argv):
    res, laws = load(argv)

    def mutate_res(fn):
        def run():
            d = copy.deepcopy(res)
            fn(d)
            return check(d, laws)
        return run

    def mutate_main(fn):
        def run():
            m = copy.deepcopy(laws)
            fn(m)
            return check(res, m)
        return run

    def at(d, model, target_id):
        return next(c for c in d["certificates"] if c["model"] == model and c["target_id"] == target_id)

    def set_text(model, target_id, text):
        def fn(d):
            at(d, model, target_id)["target"] = text
        return fn

    def shift_id(d):  # the id of one certificate off by one
        at(d, "B", 2)["target_id"] = 3

    def unknown_id(d):
        at(d, "C", 5)["target_id"] = 713

    def text_everywhere(d):  # every copy of id 2 changed the same way, so no copy disagrees
        for c in d["certificates"]:
            if c["target_id"] == 2:
                c["target"] = "f(y) = x"

    def not_refuted_text(d):
        d["not_refuted"][0]["target"] = "f(x*(x*y)) = y"

    def model_law(d):
        d["models"]["A"]["law"] = "f((x*y)*z) = y"

    def main_tree(m):  # the main list's tree changed, its text not: text no longer reads back
        e = next(e for e in m if e["id"] == 450)
        e["law"][1] = ["v", 2]

    def main_text_and_res(m):  # main text changed alone: results text no longer equal
        next(e for e in m if e["id"] == 1)["text"] = "f(y) = y"

    def main_drop(m):
        m.pop()

    def main_repeat(m):
        m.append(copy.deepcopy(m[0]))

    swapped = "yxzwuvabcdefgh"
    mutations = [
        ("certificate text with two variables swapped", mutate_res(set_text("A", 2, "f(y) = x"))),
        ("certificate text with sides swapped", mutate_res(set_text("A", 2, "y = f(x)"))),
        ("certificate text bracketed differently", mutate_res(set_text("D", 450, "f((x*y)*z) = y"))),
        ("text changed in every copy of one id", mutate_res(text_everywhere)),
        ("certificate id off by one", mutate_res(shift_id)),
        ("certificate id outside the list", mutate_res(unknown_id)),
        ("not_refuted text changed", mutate_res(not_refuted_text)),
        ("model law text of A replaced by D's", mutate_res(model_law)),
        ("main list tree changed", mutate_main(main_tree)),
        ("main list text changed", mutate_main(main_text_and_res)),
        ("main list missing its last law", mutate_main(main_drop)),
        ("main list with a repeated id", mutate_main(main_repeat)),
        ("variable order x, y swapped", lambda: check(res, laws, swapped)),
    ]
    rejected = 0
    for name, run in mutations:
        try:
            run()
            print(f"mutation {name}: NOT rejected")
        except Bad as e:
            rejected += 1
            print(f"mutation {name}: rejected ({e})")
    print(f"selftest: {rejected} of {len(mutations)} corrupted inputs rejected")
    if rejected != len(mutations):
        print("SELFTEST FAILED")
        sys.exit(1)
    print("ALL PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest(sys.argv[2:])
    else:
        main(sys.argv[1:])
