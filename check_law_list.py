"""The main repository's stored list of short laws is all and only the short laws, each once.

Steps 11 and 12 use the main repository's file data/laws_3.json (712 laws). Its own count check,
src/check_laws_count.py, compares a brute-force count with the generator laws.py, not with the
stored file, and it removes repeats before comparing (step 21). This script reads the file itself:

  1. ids are exactly 1..N in order; every entry is a law: two term trees built from
     ['v', k], ['f', a], ['m', a, b], with different sides, 1 to 3 operations in all, and the
     stored 'order' and 'vars' fields equal to what the trees give;
  2. no two entries are the same law up to renaming the variables and swapping the sides;
  3. the set of entries, up to renaming and swapping, is exactly the set built here by brute force
     (every pair of terms with 1 to 3 operations in all over variables 0..4, sides different).

"Same law up to renaming and swapping" is computed in two ways, and the run checks they agree on
the brute-force list: the smallest form over all permutations of the variables and both side
orders, and the smallest over both side orders of the renaming by first appearance.

Plain Python, written here; it does not import the main repository's code.

Usage:
  python check_law_list.py [path/to/laws_3.json]
  python check_law_list.py --selftest [path/to/laws_3.json]
"""
import copy
import itertools
import json
import sys
from pathlib import Path

MAX_ORDER = 3
DEFAULT_LAWS = Path(__file__).resolve().parent.parent / "eq-unary-magma-laws" / "data" / "laws_3.json"


class Bad(Exception):
    pass


def terms(k, nvars, top_f=True):
    """All terms with exactly k operations over variables 0..nvars-1."""
    if k == 0:
        return [("v", i) for i in range(nvars)]
    out = [("f", t) for t in terms(k - 1, nvars)] if top_f else []
    for i in range(k):
        for a in terms(i, nvars):
            for b in terms(k - 1 - i, nvars):
                out.append(("m", a, b))
    return out


def ops(t):
    return 0 if t[0] == "v" else 1 + sum(ops(c) for c in t[1:])


def variables(t, acc):
    if t[0] == "v":
        acc.add(t[1])
    else:
        for c in t[1:]:
            variables(c, acc)
    return acc


def relabel(t, p):
    if t[0] == "v":
        return ("v", p[t[1]])
    return (t[0],) + tuple(relabel(c, p) for c in t[1:])


def key_perm(l, r):
    """Smallest (l, r) over all variable permutations and both side orders."""
    vs = sorted(variables(r, variables(l, set())))
    best = None
    for image in itertools.permutations(range(len(vs))):
        p = dict(zip(vs, image))
        a, b = relabel(l, p), relabel(r, p)
        best = min(x for x in (best, (a, b), (b, a)) if x is not None)
    return best


def first_appearance(l, r):
    p = {}
    for t in (l, r):
        stack = [t]
        while stack:  # left to right, depth first
            s = stack.pop()
            if s[0] == "v":
                p.setdefault(s[1], len(p))
            else:
                stack.extend(reversed(s[1:]))
    return relabel(l, p), relabel(r, p)


def key_first(l, r):
    """Smallest over both side orders of the renaming by first appearance."""
    return min(first_appearance(l, r), first_appearance(r, l))


def brute_force(top_f=True):
    """key_perm -> order, for every law with 1..MAX_ORDER operations; checks the two keys agree."""
    nv = MAX_ORDER + 2  # at most MAX_ORDER + 2 leaves in a law
    by_perm, by_first = {}, {}
    for total in range(1, MAX_ORDER + 1):
        for k1 in range(total + 1):
            for l in terms(k1, nv, top_f):
                for r in terms(total - k1, nv, top_f):
                    if l == r:
                        continue
                    kp, kf = key_perm(l, r), key_first(l, r)
                    by_perm[kp] = total
                    if by_first.setdefault(kf, kp) != kp:
                        raise Bad(f"the two keys disagree on {l} = {r}")
    if len(by_first) != len(by_perm):
        raise Bad(f"the two keys give {len(by_first)} and {len(by_perm)} classes")
    return by_perm


def tree(t):
    """Stored JSON tree -> tuple term, rejecting anything that is not a term."""
    if not isinstance(t, list) or not t:
        raise Bad(f"not a term: {t!r}")
    if t[0] == "v" and len(t) == 2 and isinstance(t[1], int) and t[1] >= 0:
        return ("v", t[1])
    if t[0] == "f" and len(t) == 2:
        return ("f", tree(t[1]))
    if t[0] == "m" and len(t) == 3:
        return ("m", tree(t[1]), tree(t[2]))
    raise Bad(f"not a term: {t!r}")


def check(laws, expected):
    if [e["id"] for e in laws] != list(range(1, len(laws) + 1)):
        raise Bad("ids are not exactly 1..N in order")
    seen = {}
    for e in laws:
        l, r = (tree(s) for s in e["law"])
        if l == r:
            raise Bad(f"id {e['id']}: both sides are the same term")
        o = ops(l) + ops(r)
        if not 1 <= o <= MAX_ORDER:
            raise Bad(f"id {e['id']}: {o} operations, outside 1..{MAX_ORDER}")
        if e["order"] != o or e["vars"] != len(variables(r, variables(l, set()))):
            raise Bad(f"id {e['id']}: stored order or vars field does not match the tree")
        k = key_perm(l, r)
        if k in seen:
            raise Bad(f"id {e['id']} is the same law as id {seen[k]} up to renaming and swapping")
        seen[k] = e["id"]
    missing = set(expected) - set(seen)
    extra = set(seen) - set(expected)
    if missing or extra:
        raise Bad(f"{len(missing)} short laws missing from the file, {len(extra)} entries not short laws")
    by = {}
    for k in seen:
        by[expected[k]] = by.get(expected[k], 0) + 1
    return len(seen), dict(sorted(by.items()))


def main(argv):
    laws = json.load(open(argv[0] if argv else DEFAULT_LAWS))
    try:
        expected = brute_force()
        n, by = check(laws, expected)
    except Bad as e:
        print("FAIL:", e)
        sys.exit(1)
    print(f"brute force: {len(expected)} laws up to renaming and swapping (two keys agree)")
    print(f"file: {n} entries, each a different law, by order {by}")
    print("the file is all and only the short laws, each once")
    print("ALL PASS")


def selftest(argv):
    laws = json.load(open(argv[0] if argv else DEFAULT_LAWS))
    expected = brute_force()

    def on_file(fn):
        def run():
            m = copy.deepcopy(laws)
            fn(m)
            return check(m, expected)
        return run

    def by_id(m, i):
        return next(e for e in m if e["id"] == i)

    def append(m, law, order, nvars):
        m.append({"id": len(m) + 1, "text": "", "order": order, "vars": nvars, "law": law})

    def drop_last(m):
        m.pop()

    def renamed_copy(m):  # law 2 is f(x) = y; append f(y) = x
        append(m, [["f", ["v", 1]], ["v", 0]], 1, 2)

    def swapped_copy(m):  # append y = f(x)
        append(m, [["v", 1], ["f", ["v", 0]]], 1, 2)

    def replaced(m):  # count stays the same, one law lost, one repeated
        by_id(m, 712)["law"] = copy.deepcopy(by_id(m, 1)["law"])
        by_id(m, 712)["order"], by_id(m, 712)["vars"] = 1, 1

    def trivial(m):
        append(m, [["f", ["v", 0]], ["f", ["v", 0]]], 2, 1)

    def order_four(m):
        append(m, [["f", ["f", ["f", ["f", ["v", 0]]]]], ["v", 0]], 4, 1)

    def no_operation(m):
        append(m, [["v", 0], ["v", 1]], 0, 2)

    def wrong_order(m):
        by_id(m, 100)["order"] += 1

    def wrong_vars(m):
        by_id(m, 100)["vars"] += 1

    def id_gap(m):
        by_id(m, 712)["id"] = 713

    def bad_node(m):
        by_id(m, 5)["law"][0][0] = "g"

    def key_first_without_swap():  # the second key made wrong: brute force must notice
        global key_first
        saved = key_first
        key_first = first_appearance
        try:
            return brute_force()
        finally:
            key_first = saved

    mutations = [
        ("last law dropped", on_file(drop_last)),
        ("renamed copy of a law added", on_file(renamed_copy)),
        ("side-swapped copy of a law added", on_file(swapped_copy)),
        ("one law replaced by a copy of another", on_file(replaced)),
        ("law with equal sides added", on_file(trivial)),
        ("law with 4 operations added", on_file(order_four)),
        ("law with no operation added", on_file(no_operation)),
        ("order field off by one", on_file(wrong_order)),
        ("vars field off by one", on_file(wrong_vars)),
        ("id gap", on_file(id_gap)),
        ("unknown operation in a tree", on_file(bad_node)),
        ("brute force without f at the top of a side", lambda: check(laws, brute_force(top_f=False))),
        ("first-appearance key without the side swap", key_first_without_swap),
    ]
    rejected = 0
    for name, run in mutations:
        try:
            run()
            print(f"mutation {name}: NOT rejected")
        except Bad as e:
            rejected += 1
            print(f"mutation {name}: rejected ({e})")

    def renamed_in_place(m):  # f(x) = y stored as f(y) = x: the same law, must pass
        by_id(m, 2)["law"] = [["f", ["v", 1]], ["v", 0]]

    def swapped_in_place(m):  # stored as y = f(x): the same law, must pass
        by_id(m, 2)["law"] = [["v", 1], ["f", ["v", 0]]]

    controls = [("law 2 renamed in place", on_file(renamed_in_place)),
                ("law 2 sides swapped in place", on_file(swapped_in_place))]
    passed = 0
    for name, run in controls:
        try:
            run()
            passed += 1
            print(f"control {name}: accepted, as it must be")
        except Bad as e:
            print(f"control {name}: wrongly rejected ({e})")
    print(f"selftest: {rejected} of {len(mutations)} corrupted inputs rejected, "
          f"{passed} of {len(controls)} harmless changes accepted")
    if rejected != len(mutations) or passed != len(controls):
        print("SELFTEST FAILED")
        sys.exit(1)
    print("ALL PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest(sys.argv[2:])
    else:
        main(sys.argv[1:])
