"""Magma special cases of the two collapsing laws, looked up in the Equational Theories Project data.

If a law with f collapses (forces x = y), then so does every magma law obtained from it by putting
a magma term in place of f: a magma satisfying the special case, with f defined by that term, is a
model of the law with f. So each such special case must be equivalent to the singleton law
Equation2 (x = y) in the ETP. This script checks that for the two laws that collapse here and for
f(z) replaced by z, z*z, z*(z*z) and (z*z)*z (all special cases with at most 4 operations, the
ETP's limit):

  1. each special case, up to letter names and the side it is written on, is exactly one
     equation of the ETP's list (data/equations.txt);
  2. the ETP's outcome table (data/2024-11-10-outcomes.json.zip) records that equation as
     implying Equation2. The table's orientation (row implies column) is checked first: the row
     of Equation2 is all true, and Equation1 (x = x) does not imply Equation2.

This is a consistency check against published data, not a proof: the ETP's collapse of a special
case says nothing about the law with a general f. The ETP data is read only, from a clone of
github.com/teorth/equational_theories (default ../_external/equational_theories). Not in CI.

Usage:
  python etp_specializations.py [path/to/equational_theories]
  python etp_specializations.py --selftest [path/to/equational_theories]
"""
import json
import sys
import zipfile
from pathlib import Path

from check_derivation import Bad, equation, parse, substitute
from mirror_pairs import normal

LAWS = ["(x*y)*f(z) = y", "f(x)*(y*z) = y"]
TERMS = ["z", "z*z", "z*(z*z)", "(z*z)*z"]  # magma terms in z with at most 2 operations
EXPECTED = {  # (law, term put in place of f(z)) -> ETP equation id, found in step 14
    ("(x*y)*f(z) = y", "z"): 30, ("f(x)*(y*z) = y", "z"): 15,
    ("(x*y)*f(z) = y", "z*z"): 174, ("f(x)*(y*z) = y", "z*z"): 178,
    ("(x*y)*f(z) = y", "z*(z*z)"): 1508, ("f(x)*(y*z) = y", "z*(z*z)"): 1933,
    ("(x*y)*f(z) = y", "(z*z)*z"): 1711, ("f(x)*(y*z) = y", "(z*z)*z"): 2136,
}
DEFAULT_ETP = Path(__file__).resolve().parent.parent / "_external" / "equational_theories"
TRUE = {"explicit_proof_true", "implicit_proof_true"}


def put_term(t, term):
    """Replace every f(u) in t by term with z := u."""
    if t[0] == "v":
        return t
    if t[0] == "f":
        return substitute(term, {"z": put_term(t[1], term)})
    return ("*", put_term(t[1], term), put_term(t[2], term))


def special_case(law, term_text, put=put_term):
    term = parse(term_text)
    lhs, rhs = equation(law)
    return put(lhs, term), put(rhs, term)


def etp_index(lines, normal_fn=normal):
    index = {}
    for k, line in enumerate(lines, 1):
        index.setdefault(normal_fn(*equation(line.replace("◇", "*"))), []).append(k)
    return index


def outcome_rows(etp, wanted):
    """Rows of the ETP outcome table for the equation ids in wanted (1-based), and the id names."""
    with zipfile.ZipFile(etp / "data" / "2024-11-10-outcomes.json.zip") as zf:
        raw = zf.read("outcomes.json").decode()
    names = json.loads(raw[raw.index("[", raw.rindex('"equations"')):raw.rindex("]") + 1])
    rows, pos = {}, raw.index("[[") + 1
    for k in range(1, len(names) + 1):
        start = raw.index("[", pos)
        end = raw.index("]", start)
        if k in wanted:
            rows[k] = json.loads(raw[start:end + 1])
        pos = end + 1
    return rows, names


def check(lines, rows, names, value=None, laws=LAWS, put=put_term, normal_fn=normal,
          expected=EXPECTED, verbose=False):
    if value is None:
        value = lambda i, j: rows[i][j - 1]  # row i implies column j
    if len(names) != len(lines) or any(n != f"Equation{k}" for k, n in enumerate(names, 1)):
        raise Bad("outcome table ids are not Equation1..EquationN in the order of equations.txt")
    if any(value(2, j) not in TRUE for j in range(1, len(names) + 1)):
        raise Bad("orientation: the row of Equation2 is not all true")
    if value(1, 2) in TRUE:
        raise Bad("orientation: Equation1 recorded as implying Equation2")
    index = etp_index(lines, normal_fn)
    for law in laws:
        for term in TERMS:
            key = normal_fn(*special_case(law, term, put))
            ids = index.get(key, [])
            if ids != [expected.get((law, term))]:
                raise Bad(f"{law} with f(z) := {term}: ETP ids {ids}, expected {expected.get((law, term))}")
            i = ids[0]
            if value(i, 2) not in TRUE:
                raise Bad(f"Equation{i} ({lines[i - 1]}) -> Equation2 is {value(i, 2)}")
            if verbose:
                print(f"{law} with f(z) := {term}: Equation{i}  {lines[i - 1]}  -> Equation2: {value(i, 2)}")


def load(argv, extra=lambda lines: {}):
    etp = Path(argv[0]) if argv else DEFAULT_ETP
    lines = (etp / "data" / "equations.txt").read_text(encoding="utf-8").splitlines()
    rows, names = outcome_rows(etp, set(EXPECTED.values()) | set(extra(lines).values()) | {1, 2})
    return lines, rows, names


def main(argv):
    lines, rows, names = load(argv)
    try:
        check(lines, rows, names, verbose=True)
    except Bad as e:
        print(f"FAILED: {e}")
        sys.exit(1)
    print(f"ALL PASS: {len(EXPECTED)} special cases, each one ETP equation that implies Equation2")


BAD_LAW = "(x*y)*f(z) = x"  # does not collapse: x*y = x and any f is a model


def bad_law_ids(lines):
    index = etp_index(lines)
    return {(BAD_LAW, t): index[normal(*special_case(BAD_LAW, t))][0] for t in TERMS}


def selftest(argv):
    lines, rows, names = load(argv, bad_law_ids)
    check(lines, rows, names)  # the real data must pass first

    def no_f_inside(t, term):  # replaces only an f at the top of a side
        return substitute(term, {"z": t[1]}) if t[0] == "f" else t

    def one_side(lhs, rhs):  # normal form that ignores the side a law is written on
        return normal(lhs, rhs) + "|" + str(lhs[0] == "v")

    shifted = {k: v + 1 for k, v in EXPECTED.items()}
    mutations = [
        ("law (x*y)*f(z) = x, which does not collapse",
         lambda: check(lines, rows, names, laws=[BAD_LAW], expected=bad_law_ids(lines))),
        ("table read transposed", lambda: check(lines, rows, names, value=lambda i, j: rows[j][i - 1])),
        ("equation list shifted by one", lambda: check(lines[1:] + lines[:1], rows, names)),
        ("expected ids off by one", lambda: check(lines, rows, names, expected=shifted)),
        ("f replaced only at the top", lambda: check(lines, rows, names, put=no_f_inside)),
        ("normal form ignores swapped sides", lambda: check(lines, rows, names, normal_fn=one_side)),
        ("row of Equation1 read for Equation2",
         lambda: check(lines, rows, names, value=lambda i, j: rows[1 if i == 2 else i][j - 1])),
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
