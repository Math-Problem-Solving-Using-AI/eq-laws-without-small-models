"""Plain-Python checks of our reading of Peng's preprint on the Austin identities E5093 and E5107.

The preprint ("Seeded infinite models of the Austin identities E5093 and E5107", Y. J. Peng,
version 2, 2026-11-19, Zenodo record 24360387, read in step 25 from its LaTeX source) is about
magmas (one binary operation, no unary operation). This script checks, without a solver:

  1. the eight law texts the paper writes (E5093, E5107, E40951 and the five conclusions of its
     Table 2) are the lines of those numbers in the ETP's data/eq_size5.txt;
  2. the five failures of its Table 2 come out as printed when every product is looked up in the
     paper's 12-entry seed table (the paper says every product used is a seed entry); E40951 is
     evaluated in the opposite operation a*b := b(seed)a, as the paper does;
  3. no magma with 2 or 3 elements satisfies E5093, E5107 or E40951 (every table tried);
  4. none of E5093, E5107, E40951 is a substitution instance of one of our four candidate Austin
     laws with f(t) replaced by a magma term in t (at most 3 operations, which covers every case:
     f occurs once and the targets have 5 operations). Two ETP laws that step 15 found to be such
     instances (Equation28770 and Equation17522) are positive controls.
  5. with --paper PATH (the downloaded E5093-paper-v2.tex), that the quotes used in step 25 occur
     exactly once in it and that the word "unary" does not occur.

Part 3 is a finite search, not a proof for all sizes; part 2 checks the paper's arithmetic, not
that the seed extends to a model (the paper's Theorem 1, Lean-checked by its author, not here).

Usage:
  python zenodo_e5093_check.py [--paper path/to/E5093-paper-v2.tex] [path/to/equational_theories]
  python zenodo_e5093_check.py --selftest [path/to/equational_theories]
"""
import itertools
import sys
from pathlib import Path

DEFAULT_ETP = Path(__file__).resolve().parent.parent / "_external" / "equational_theories"


class Bad(Exception):
    pass


PAPER = {  # law texts as printed in the paper, its \op written as *
    5093: "x = y*(y*(y*(x*(z*y))))", 5107: "x = y*(y*(y*(z*(x*y))))",
    40951: "x = ((((y*x)*z)*y)*y)*y", 10218: "x = y*((x*y)*((z*x)*y))",
    5012: "x = y*(x*(z*(z*(y*z))))", 40070: "x = (((y*(x*z))*y)*x)*y",
    4916: "x = y*(x*(x*(y*(z*z))))", 22818: "x = (y*(z*y))*((x*x)*y)",
}
SEED = {(0, 0): 1, (0, 1): 5, (0, 3): 4, (0, 4): 0, (0, 5): 3, (0, 6): 1,
        (1, 0): 2, (1, 2): 3, (2, 1): 7, (2, 3): 6, (6, 3): 7, (7, 0): 8}
# (conclusion, opposite operation?, (x, y, z), (left side, right side)) from the paper's Table 2
TABLE2 = [(10218, False, (0, 0, 0), (0, 4)), (5012, False, (2, 0, 0), (2, 1)),
          (40070, True, (0, 2, 0), (0, 7)), (4916, True, (3, 0, 0), (3, 8)),
          (22818, False, (0, 2, 1), (0, 7))]
NO_SMALL = [5093, 5107, 40951]
LAWS = ["f(x*(y*z)) = y", "x*(y*f(z)) = y", "(f(x)*y)*z = y", "f((x*y)*z) = y"]
TERMS = ["z", "z*z", "z*(z*z)", "(z*z)*z", "z*(z*(z*z))", "z*((z*z)*z)", "(z*z)*(z*z)",
         "(z*(z*z))*z", "((z*z)*z)*z"]  # all magma terms in z with at most 3 operations
# step 15: these ETP laws are instances of our law with f(z) := the given term
CONTROLS = {28770: ("x = (((y*y)*y)*x)*(y*z)", ("(f(x)*y)*z = y", "(z*z)*z")),
            17522: ("x = (y*z)*(x*(z*(z*z)))", ("x*(y*f(z)) = y", "z*(z*z)"))}
QUOTES = [
    r"A model of either identity with more than one element, all of whose finite",
    r"models are trivial, makes the identity an \emph{Austin identity}.",
    r"A magma is a set with one binary operation \(\op\).",
    r"on the natural numbers by completing finite partial tables",
    r"finite seed: every admissible finite table extends to a model on the natural",
    r"described the question as open; we missed the thread when checking for prior",
    r"translation-invariant operation on a free group",
    r"Both use Lean~4.24.0 with only",
    r"library and the official \code{JudgeProblem} module~\cite{sairjudge}.",
    r"\href{https://github.com/SAIRcompetition/equational-theories-lean-stage2/tree/817a4653bf762584931d49c6714c9fcfab7df66a}",
    r"official stage-2 checker on Lean~4.33.1. This is a local check, not a",
    r"OpenAI Codex assisted in developing the",
    r"\textbf{38} (1997), 324--328.",
    r"Write \(L_y(t)=y\op t\), and let \(L_y^k\) denote its \(k\)-fold iterate.",
]


def parse(s):
    """'lhs = rhs' -> (lhs, rhs); a term is a letter, ('*', a, b) or ('f', a)."""
    s = s.replace("◇", "*").replace(" ", "")
    pos = 0

    def atom():
        nonlocal pos
        if s[pos] == "(" or s.startswith("f(", pos):
            head = "f" if s[pos] == "f" else None
            pos += 2 if head else 1
            t = term()
            if s[pos:pos + 1] != ")":
                raise Bad(f"missing ) in {s}")
            pos += 1
            return ("f", t) if head else t
        if not s[pos].isalpha():
            raise Bad(f"unexpected {s[pos]!r} in {s}")
        pos += 1
        return s[pos - 1]

    def term():
        nonlocal pos
        left = atom()
        while s[pos:pos + 1] == "*":
            pos += 1
            left = ("*", left, atom())
        return left

    lhs = term()
    if s[pos:pos + 1] != "=":
        raise Bad(f"no = in {s}")
    pos += 1
    rhs = term()
    if pos != len(s):
        raise Bad(f"trailing text in {s}")
    return lhs, rhs


def ev(t, env, op):
    return env[t] if isinstance(t, str) else op(ev(t[1], env, op), ev(t[2], env, op))


def count_models(law, size):
    lhs, rhs = parse(law)
    count = tables = 0
    for flat in itertools.product(range(size), repeat=size * size):
        tables += 1
        op = lambda p, q: flat[p * size + q]  # noqa: E731
        if all(ev(lhs, dict(zip("xyz", v)), op) == ev(rhs, dict(zip("xyz", v)), op)
               for v in itertools.product(range(size), repeat=3)):
            count += 1
    if tables != size ** (size * size):
        raise Bad("not every table was tried")
    return count


def sub(t, s):
    return s.get(t, t) if isinstance(t, str) else ("*", sub(t[1], s), sub(t[2], s))


def put_f(t, body):
    if isinstance(t, str):
        return t
    if t[0] == "f":
        return sub(body, {"z": put_f(t[1], body)})
    return ("*", put_f(t[1], body), put_f(t[2], body))


def match(p, t, s):
    if isinstance(p, str):
        if p in s:
            return s if s[p] == t else None
        return {**s, p: t}
    if isinstance(t, str) or p[0] != t[0]:
        return None
    s = match(p[1], t[1], s)
    return None if s is None else match(p[2], t[2], s)


def instance_of(target, laws):
    """(law, term) pairs such that target is an instance of law with f(z) := term."""
    ta, tb = parse(target)
    hits = []
    for law in laws:
        la, lb = parse(law)
        for term in TERMS:
            body = parse(term + "=z")[0]
            pa, pb = put_f(la, body), put_f(lb, body)
            for qa, qb in ((pa, pb), (pb, pa)):
                s = match(qa, ta, {})
                if s is not None and match(qb, tb, s) is not None:
                    hits.append((law, term))
    return hits


def check(lines, paper=PAPER, seed=SEED, no_small=NO_SMALL, laws=LAWS, tex=None):
    """Raise Bad on the first failure; return the lines to print."""
    out = []
    for n, text in paper.items():
        if parse(lines[n - 1]) != parse(text):
            raise Bad(f"E{n}: paper {text} vs ETP {lines[n - 1]}")
    out.append(f"1. {len(paper)} law texts of the paper equal the ETP's eq_size5.txt lines")
    for n, opposite, (x, y, z), want in TABLE2:
        lhs, rhs = parse(paper[n])
        op = (lambda a, b: seed[(b, a)]) if opposite else (lambda a, b: seed[(a, b)])
        env = {"x": x, "y": y, "z": z}
        try:
            got = (ev(lhs, env, op), ev(rhs, env, op))
        except KeyError as e:
            raise Bad(f"E{n} at {(x, y, z)}: product {e.args[0]} is not a seed entry")
        if got != want:
            raise Bad(f"E{n} at {(x, y, z)}: sides {got}, paper says {want}")
    out.append(f"2. the {len(TABLE2)} failures of Table 2 come out as printed from the seed")
    for n in no_small:
        for size in (2, 3):
            c = count_models(paper[n], size)
            if c:
                raise Bad(f"E{n} has {c} models with {size} elements")
    out.append(f"3. no magma with 2 or 3 elements satisfies E{', E'.join(map(str, no_small))}")
    for n, (text, pair) in CONTROLS.items():
        if parse(lines[n - 1]) != parse(text):
            raise Bad(f"control E{n}: text differs from the ETP's line")
        if pair not in instance_of(text, laws):
            raise Bad(f"control E{n} is not found as an instance of {pair} (step 15: it is)")
    for n in no_small:
        hits = instance_of(paper[n], laws)
        if hits:
            raise Bad(f"E{n} is an instance of {hits}")
    out.append(f"4. E{', E'.join(map(str, no_small))}: not instances of our four laws "
               f"(controls E{' and E'.join(map(str, CONTROLS))} found)")
    if tex is not None:
        for q in QUOTES:
            if tex.count(q) != 1:
                raise Bad(f"quote found {tex.count(q)} times in the paper: {q[:50]}")
        if "unary" in tex:
            raise Bad("the paper contains the word 'unary'")
        out.append(f"5. {len(QUOTES)} quotes found once each in the paper, no 'unary'")
    return out


def read_lines(etp):
    return (etp / "data" / "eq_size5.txt").read_text(encoding="utf-8").splitlines()


def main(args):
    tex = None
    if args[:1] == ["--paper"]:
        tex, args = Path(args[1]).read_text(encoding="utf-8"), args[2:]
    etp = Path(args[0]) if args else DEFAULT_ETP
    try:
        for line in check(read_lines(etp), tex=tex):
            print(line)
    except Bad as e:
        print(f"FAIL: {e}")
        sys.exit(1)
    print("OK")


def selftest(args):
    lines = read_lines(Path(args[0]) if args else DEFAULT_ETP)
    wrong_line = list(lines)
    wrong_line[5012 - 1] = wrong_line[5012 - 1].replace("y ◇ z", "y ◇ x")
    mutations = {
        "ETP line changed": dict(lines=wrong_line),
        "seed entry changed": dict(seed={**SEED, (1, 2): 4}),
        "seed entry removed": dict(seed={k: v for k, v in SEED.items() if k != (7, 0)}),
        "law with small models": dict(paper={**PAPER, 1: "x = x*(x*x)"}, no_small=[1],
                                      lines=["x = x ◇ (x ◇ x)"] + lines[1:]),
        "known instance as target": dict(paper={**PAPER, 28770: CONTROLS[28770][0]},
                                         no_small=[28770], lines=lines),
        "control law removed": dict(laws=LAWS[:1] + LAWS[2:]),
        "quote broken": dict(tex="\n".join(QUOTES).replace("more than one", "more than two")),
        "word unary planted": dict(tex="\n".join(QUOTES) + " unary"),
    }
    rejected = 0
    for name, kw in mutations.items():
        kw.setdefault("lines", lines)
        try:
            check(**kw)
            print(f"NOT rejected: {name}")
        except Bad as e:
            rejected += 1
            print(f"rejected: {name}: {e}")
    print(f"selftest: {rejected} of {len(mutations)} corrupted inputs rejected")
    sys.exit(0 if rejected == len(mutations) else 1)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest(sys.argv[2:])
    else:
        main(sys.argv[1:])
