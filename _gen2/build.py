#!/usr/bin/env python3
from pathlib import Path

from header import html_head, html_foot
from dashboard import dashboard
from plan import plan
from arch import fundamentals, react_arch
from react_core import internals, reconciliation
from state_perf import state, fetching, performance, perf_debug
from platform import browser_and_web, design_mfe, sec_a11y_test_obs
from cases import cases
from sdq import sysdesign
from feq import feq
from exercises import exercises
from adrs import adrs, comms
from glossary import glossary
from rest import debug_sim, mock, progress, readiness, resources

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "phase2-atlassian-frontend-architecture.html"


def main() -> None:
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    js = (ROOT / "app.js").read_text(encoding="utf-8")
    parts = [
        html_head(css),
        dashboard(),
        plan(),
        fundamentals(),
        react_arch(),
        internals(),
        reconciliation(),
        state(),
        fetching(),
        performance(),
        perf_debug(),
        browser_and_web(),
        design_mfe(),
        sec_a11y_test_obs(),
        cases(),
        sysdesign(),
        feq(),
        exercises(),
        adrs(),
        comms(),
        mock(),
        debug_sim(),
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
