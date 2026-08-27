#!/usr/bin/env python3
from pathlib import Path

from header import html_head, html_foot
from dashboard import dashboard
from plan import plan
from foundations import howto, jsmodel, bigo
from linear import arrays, strings, hashmap
from lists import linked, stacks
from trees import recursion, trees, heaps
from graphs import graphs
from patterns import sort_search, twopointer, window, backtrack, dp, expert
from practical import practical
from problems import problems
from questions import feq
from rest import mock, progress, readiness, resources, glossary

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "dsa-javascript.html"


def main() -> None:
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    js = (ROOT / "app.js").read_text(encoding="utf-8")
    parts = [
        html_head(css),
        dashboard(),
        plan(),
        howto(),
        jsmodel(),
        bigo(),
        arrays(),
        strings(),
        hashmap(),
        linked(),
        stacks(),
        recursion(),
        trees(),
        heaps(),
        graphs(),
        sort_search(),
        twopointer(),
        window(),
        backtrack(),
        dp(),
        expert(),
        practical(),
        problems(),
        feq(),
        mock(),
        progress(),
        readiness(),
        resources(),
        glossary(),
        html_foot(js),
    ]
    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
