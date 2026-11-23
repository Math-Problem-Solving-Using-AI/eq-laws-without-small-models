"""Magma special cases of the four candidate Austin laws, looked up in the Equational Theories Project data.

The four laws f(x*(y*z)) = y, x*(y*f(z)) = y, (f(x)*y)*z = y and f((x*y)*z) = y have, by our hand
argument, no finite model with 2 or more elements. If that is right, then neither has any magma law
obtained by putting a magma term in z in place of f(z): a finite magma satisfying such a special
case, with f defined by that term, would be a finite model of the law. This script checks that the
published data agrees, for f(z) replaced by each magma term in z with at most 3 operations:

  1. special cases with at most 4 operations: each is exactly one equation of the ETP's list
     (data/equations.txt, up to letter names and sides), and the ETP's outcome table records it
     as implying Equation2 (x = y). The ETP blueprint says no law of order 4 or less is an Austin
     law, so for these "no nontrivial finite model" and "implies Equation2" are the same;
  2. special cases with 5 operations: each is exactly one equation of data/eq_size5.txt, none is
     in the three tables of blueprint/src/chapter/order_5.tex (Austin laws; no nontrivial finite
     model, infinite unknown; finite unknown), and z3 proves that it implies x = y (`z3-only`);
  3. Kisielewicz's Austin laws Equation28770 and Equation374794 (texts from the blueprint) and the
     mirror of 28770, Equation17522, are substitution instances of a special case of our laws
     (f(z) := (z*z)*z, or z*(z*z) for the mirror). This only records how the shapes are related.

A consistency check against published data, not a proof: it could refute our hand argument (a
special case with a nontrivial finite model), never confirm it. The ETP data is read only, from a
clone of github.com/teorth/equational_theories (default ../_external/equational_theories). Not in CI.

Usage:
  python etp_specializations_austin.py [path/to/equational_theories]
  python etp_specializations_austin.py --selftest [path/to/equational_theories]
"""
import re
import sys
from pathlib import Path

import z3

from check_derivation import Bad, equation, parse, show, substitute
from etp_specializations import DEFAULT_ETP, TRUE, outcome_rows, put_term, special_case

LAWS = ["f(x*(y*z)) = y", "x*(y*f(z)) = y", "(f(x)*y)*z = y", "f((x*y)*z) = y"]
TERMS = ["z", "z*z", "z*(z*z)", "(z*z)*z", "z*(z*(z*z))", "z*((z*z)*z)", "(z*z)*(z*z)",
         "(z*(z*z))*z", "((z*z)*z)*z"]  # all magma terms in z with at most 3 operations
EXPECTED = {  # (law, term put in place of f(z)) -> ETP equation id, found in step 15
    ("f(x*(y*z)) = y", "z"): 15, ("f(x*(y*z)) = y", "z*z"): 21654,
    ("x*(y*f(z)) = y", "z"): 15, ("x*(y*f(z)) = y", "z*z"): 70,
    ("x*(y*f(z)) = y", "z*(z*z)"): 493, ("x*(y*f(z)) = y", "(z*z)*z"): 696,
    ("x*(y*f(z)) = y", "z*(z*(z*z))"): 5016, ("x*(y*f(z)) = y", "z*((z*z)*z)"): 5893,
    ("x*(y*f(z)) = y", "(z*z)*(z*z)"): 6770, ("x*(y*f(z)) = y", "(z*(z*z))*z"): 7647,
    ("x*(y*f(z)) = y", "((z*z)*z)*z"): 8524,
    ("(f(x)*y)*z = y", "z"): 30, ("(f(x)*y)*z = y", "z*z"): 282,
    ("(f(x)*y)*z = y", "z*(z*z)"): 2948, ("(f(x)*y)*z = y", "(z*z)*z"): 3151,
    ("(f(x)*y)*z = y", "z*(z*(z*z))"): 37547, ("(f(x)*y)*z = y", "z*((z*z)*z)"): 38424,
    ("(f(x)*y)*z = y", "(z*z)*(z*z)"): 39301, ("(f(x)*y)*z = y", "(z*(z*z))*z"): 40178,
    ("(f(x)*y)*z = y", "((z*z)*z)*z"): 41055,
    ("f((x*y)*z) = y", "z"): 30, ("f((x*y)*z) = y", "z*z"): 24285,
}
# (ETP id, its text, our law, term for f(z), substitution of our law's letters)
INSTANCES = [
    (28770, "x = (((y*y)*y)*x)*(y*z)", "(f(x)*y)*z = y", "(z*z)*z", {"x": "y", "y": "x", "z": "y*z"}),
    (374794, "x = (((y*y)*y)*x)*((y*y)*z)", "(f(x)*y)*z = y", "(z*z)*z",
     {"x": "y", "y": "x", "z": "(y*y)*z"}),
    (17522, "x = (y*z)*(x*(z*(z*z)))", "x*(y*f(z)) = y", "z*(z*z)", {"x": "y*z", "y": "x", "z": "z"}),
]
LETTERS = "abcdeghijklmnopqrstuvwxyz"  # no f: order-5 equations have up to 7 letters
TABLE_SIZES = (10, 96, 24)  # rows of the three tables in order_5.tex, as its text counts them


def ops(t):
    return 0 if t[0] == "v" else ops(t[1]) + (ops(t[2]) + 1 if t[0] == "*" else 0)


def rename(t, names):
    if t[0] == "v":
        if t[1] not in names:
            names[t[1]] = ("v", LETTERS[len(names)])
        return names[t[1]]
    return (t[0],) + tuple(rename(c, names) for c in t[1:])


def normal(lhs, rhs):
    """The same text for laws that differ only by letter names or by the side they are written on."""
    forms = []
    for a, b in ((lhs, rhs), (rhs, lhs)):
        names = {}
        forms.append(f"{show(rename(a, names))} = {show(rename(b, names))}")
    return min(forms)


def etp_index(lines, normal_fn=normal):
    index = {}
    for k, line in enumerate(lines, 1):
        index.setdefault(normal_fn(*equation(line.replace("◇", "*"))), []).append(k)
    return index


def table_ids(tex):
    """Equation ids in the three tables of order_5.tex, one list per table."""
    tables = re.findall(r"\\begin\{tabular\}(.*?)\\end\{tabular\}", tex, re.S)
    ids = [[int(n) for n in re.findall(r"\$ \((\d+)\)", t)] for t in tables]
    if tuple(len(t) for t in ids) != TABLE_SIZES:
        raise Bad(f"order_5.tex tables have {[len(t) for t in ids]} rows, its text says {TABLE_SIZES}")
    return ids


def z3_collapses(lhs, rhs, timeout=20000):
    """z3 answer to: does the magma law lhs = rhs imply x = y? 'unsat' means yes (z3-only)."""
    m_sort = z3.DeclareSort("M")
    mul = z3.Function("mul", m_sort, m_sort, m_sort)
    letters = {}

    def ev(t):
        if t[0] == "v":
            return letters.setdefault(t[1], z3.Const(t[1], m_sort))
        if t[0] != "*":
            raise Bad("z3 check is for magma laws only")
        return mul(ev(t[1]), ev(t[2]))

    law = ev(lhs) == ev(rhs)
    s = z3.Solver()
    s.set("timeout", timeout)
    s.add(z3.ForAll(list(letters.values()), law))
    a, b = z3.Consts("a b", m_sort)
    s.add(a != b)
    return str(s.check())


def check(lines4, lines5, rows, names, tex, defs, value=None, laws=LAWS, terms=TERMS, put=put_term,
          normal_fn=normal, expected=EXPECTED, instances=INSTANCES, collapses=z3_collapses,
          verbose=False):
    if value is None:
        value = lambda i, j: rows[i][j - 1]  # row i implies column j
    if len(names) != len(lines4) or any(n != f"Equation{k}" for k, n in enumerate(names, 1)):
        raise Bad("outcome table ids are not Equation1..EquationN in the order of equations.txt")
    if any(value(2, j) not in TRUE for j in range(1, len(names) + 1)):
        raise Bad("orientation: the row of Equation2 is not all true")
    if value(1, 2) in TRUE:
        raise Bad("orientation: Equation1 recorded as implying Equation2")
    if lines5[:len(lines4)] != lines4:
        raise Bad("eq_size5.txt does not start with the equations of equations.txt")
    index4, index5 = etp_index(lines4, normal_fn), etp_index(lines5, normal_fn)
    in_tables = {i: k for k, t in enumerate(table_ids(tex), 1) for i in t}
    count = 0
    for law in laws:
        for term in terms:
            lhs, rhs = special_case(law, term, put)
            order = ops(lhs) + ops(rhs)
            if order > 5:
                continue
            key = normal_fn(lhs, rhs)
            ids = (index4 if order <= 4 else index5).get(key, [])
            want = expected.get((law, term))
            if ids != [want]:
                raise Bad(f"{law} with f(z) := {term}: ETP ids {ids}, expected {want}")
            i = ids[0]
            if order <= 4:
                if value(i, 2) not in TRUE:
                    raise Bad(f"Equation{i} ({lines4[i - 1]}) -> Equation2 is {value(i, 2)}")
                how = f"ETP outcome table: {value(i, 2)}"
            else:
                if i in in_tables:
                    raise Bad(f"Equation{i} is in table {in_tables[i]} of order_5.tex")
                answer = collapses(lhs, rhs)
                if answer != "unsat":
                    raise Bad(f"Equation{i} ({lines5[i - 1]}): z3 says {answer} to 'implies x = y'")
                how = "in no order_5.tex table; z3: implies x = y (unsat)"
            count += 1
            if verbose:
                print(f"{law} with f(z) := {term}: order {order}, Equation{i}  {lines5[i - 1]}  {how}")
    for i, text, law, term, sub in instances:
        etp_text = lines5[i - 1] if i <= len(lines5) else defs.get(i)
        if etp_text is None:
            raise Bad(f"Equation{i} is in neither eq_size5.txt nor the blueprint's definitions")
        if normal_fn(*equation(etp_text.replace("◇", "*"))) != normal_fn(*equation(text)):
            raise Bad(f"Equation{i}: text {text!r} is not the ETP's {etp_text!r}")
        lhs, rhs = special_case(law, term, put)
        sub = {k: parse(v) for k, v in sub.items()}
        if normal_fn(substitute(lhs, sub), substitute(rhs, sub)) != normal_fn(*equation(text)):
            raise Bad(f"Equation{i} is not {law} with f(z) := {term} and that substitution")
        if verbose:
            print(f"Equation{i}  {text}  is an instance of {law} with f(z) := {term}")
    return count


def blueprint_text(etp, name):
    return (etp / "blueprint" / "src" / "chapter" / name).read_text(encoding="utf-8")


def definitions(tex):
    """Equation texts defined in the blueprint by \\Equadef{id}{text}, with * for the operation."""
    return {int(i): t.replace("\\op", "*") for i, t in re.findall(r"\\Equadef\{(\d+)\}\{(.*)\}", tex)}


def load(argv, extra=()):
    etp = Path(argv[0]) if argv else DEFAULT_ETP
    lines4 = (etp / "data" / "equations.txt").read_text(encoding="utf-8").splitlines()
    lines5 = (etp / "data" / "eq_size5.txt").read_text(encoding="utf-8").splitlines()
    small = {i for i in EXPECTED.values() if i <= len(lines4)}
    rows, names = outcome_rows(etp, small | set(extra) | {1, 2})
    return (lines4, lines5, rows, names, blueprint_text(etp, "order_5.tex"),
            definitions(blueprint_text(etp, "equations.tex")))


def main(argv):
    data = load(argv)
    try:
        n = check(*data, verbose=True)
    except Bad as e:
        print(f"FAILED: {e}")
        sys.exit(1)
    print(f"ALL PASS: {n} special cases, each one ETP equation that implies x = y "
          f"(order 4 or less: ETP table; order 5: z3-only), {len(INSTANCES)} instances confirmed")


BAD_LAW = "(f(x)*y)*z = z"  # has nontrivial finite models: x*y = y and any f


def bad_law_ids(lines):
    index = etp_index(lines)
    return {(BAD_LAW, t): index[normal(*special_case(BAD_LAW, t))][0] for t in TERMS
            if sum(map(ops, special_case(BAD_LAW, t))) <= 4}


def selftest(argv):
    etp = Path(argv[0]) if argv else DEFAULT_ETP
    lines4 = (etp / "data" / "equations.txt").read_text(encoding="utf-8").splitlines()
    bad4 = bad_law_ids(lines4)
    data = load(argv, bad4.values())
    lines4, lines5, rows, names, tex, defs = data
    check(*data)  # the real data must pass first
    shifted4 = lines4[1:] + lines4[:1]

    def no_f_inside(t, term):  # replaces only an f at the top of a side
        return substitute(term, {"z": t[1]}) if t[0] == "f" else t

    def one_side(lhs, rhs):  # normal form that ignores the side a law is written on
        return normal(lhs, rhs) + "|" + str(lhs[0] == "v")

    bad5 = {(BAD_LAW, t): etp_index(lines5)[normal(*special_case(BAD_LAW, t))][0] for t in TERMS[4:]}
    shifted = {k: v + 1 for k, v in EXPECTED.items()}
    our_id_in_table = tex.replace("(4916)", "(21654)", 1)
    wrong_sub = [(i, t, law, term, dict(sub, z="z")) for i, t, law, term, sub in INSTANCES]
    wrong_text = [(i + 1, t, law, term, sub) for i, t, law, term, sub in INSTANCES]
    mutations = [
        ("law (f(x)*y)*z = z, which has finite models (order 4 or less)",
         lambda: check(*data, laws=[BAD_LAW], expected=bad4)),
        ("law (f(x)*y)*z = z, order 5 only (z3 must not prove x = y)",
         lambda: check(*data, laws=[BAD_LAW], terms=TERMS[4:], expected=bad5)),
        ("table read transposed", lambda: check(*data, value=lambda i, j: rows[j][i - 1])),
        ("equation list shifted by one",
         lambda: check(shifted4, shifted4 + lines5[len(lines4):], rows, names, tex, defs)),
        ("order-5 list shifted by one", lambda: check(lines4, lines4 + lines5[len(lines4) + 1:],
                                                      rows, names, tex, defs)),
        ("expected ids off by one", lambda: check(*data, expected=shifted)),
        ("f replaced only at the top", lambda: check(*data, put=no_f_inside)),
        ("normal form ignores swapped sides", lambda: check(*data, normal_fn=one_side)),
        ("one of our order-5 ids put into table 1 of order_5.tex",
         lambda: check(lines4, lines5, rows, names, our_id_in_table, defs)),
        ("table 3 of order_5.tex cut off", lambda: check(lines4, lines5, rows, names,
                                                         tex[:tex.rindex("\\begin{tabular}")], defs)),
        ("z3 answer replaced by unknown", lambda: check(*data, collapses=lambda l, r: "unknown")),
        ("Kisielewicz instance with z := z", lambda: check(*data, instances=wrong_sub)),
        ("Kisielewicz instance with the wrong ETP id", lambda: check(*data, instances=wrong_text)),
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
