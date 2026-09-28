#!/usr/bin/env python3
from pathlib import Path

from header import html_head, html_foot
from start import dashboard, howto, role
from plan import plan
from lessons import (
    observe, plugins, patternfly, signals, perses, korrel8r,
    tools, repos, skip, senior,
)
from k8s import k8s
from queries import promql, logql, traceql
from ux import ux
from practical import practical
from questions import feq
from drills import drills
from rest import mock, progress, readiness, resources, glossary

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "gotta-learn.html"


def main() -> None:
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    js = (ROOT / "app.js").read_text(encoding="utf-8")
    parts = [
        html_head(css),
        dashboard(),
        howto(),
        plan(),
        role(),
        observe(),
        k8s(),
        plugins(),
        patternfly(),
        signals(),
        promql(),
        logql(),
        traceql(),
        ux(),
        perses(),
        korrel8r(),
        tools(),
        repos(),
        skip(),
        senior(),
        practical(),
        feq(),
        drills(),
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
