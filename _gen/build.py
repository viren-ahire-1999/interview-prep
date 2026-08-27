#!/usr/bin/env python3
from pathlib import Path

from header import html_head, html_foot
from dashboard import dashboard
from plan import plan
from dsa import dsa_curriculum
from patterns import patterns
from problems import problems
from js_dive import js_dive
from eventloop import eventloop
from jsq import jsq
from exercises import exercises
from rest import rest

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "phase1-atlassian-prep.html"

def main() -> None:
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    js = (ROOT / "app.js").read_text(encoding="utf-8")
    parts = [
        html_head(css),
        dashboard(),
        plan(),
        dsa_curriculum(),
        patterns(),
        problems(),
        js_dive(),
        eventloop(),
        jsq(),
        exercises(),
        rest(),
        html_foot(js),
    ]
    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
