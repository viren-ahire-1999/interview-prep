#!/usr/bin/env python3
from pathlib import Path

from header import html_head, html_foot
from dashboard import dashboard
from plan import plan
from mindset import mindset, framework, requirements
from theory1 import rendering, routing, state, data
from theory2 import realtime, performance, offline, design_systems, collab
from theory3 import auth, security, a11y, observability, mfe, media
from cases import cases
from designs import sysdesign
from questions import feq
from comms import comms, adrs
from rest import mock, progress, readiness, resources, glossary

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "frontend-system-design.html"


def main() -> None:
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    js = (ROOT / "app.js").read_text(encoding="utf-8")
    parts = [
        html_head(css),
        dashboard(),
        plan(),
        mindset(),
        framework(),
        requirements(),
        rendering(),
        routing(),
        state(),
        data(),
        realtime(),
        performance(),
        offline(),
        design_systems(),
        collab(),
        auth(),
        security(),
        a11y(),
        observability(),
        mfe(),
        media(),
        cases(),
        sysdesign(),
        feq(),
        comms(),
        adrs(),
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
