#!/usr/bin/env python3
from pathlib import Path

from header import html_head, html_foot
from core import dashboard, process, positioning
from behavior import framework, stories, matrix, senior, values, hm
from bq import bq
from mocks import resume, interrogation, coding, craft, sdmock, loop
from career import comms, unknown, ask, recruiter, offer, day, techcheck, rejection
from plan_ready import plan, readiness, progress, resources

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "phase4-atlassian-interview-mastery.html"


def main() -> None:
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    js = (ROOT / "app.js").read_text(encoding="utf-8")
    parts = [
        html_head(css),
        dashboard(),
        process(),
        positioning(),
        framework(),
        stories(),
        matrix(),
        bq(),
        senior(),
        values(),
        hm(),
        resume(),
        interrogation(),
        coding(),
        craft(),
        sdmock(),
        loop(),
        comms(),
        unknown(),
        ask(),
        recruiter(),
        offer(),
        day(),
        techcheck(),
        rejection(),
        plan(),
        progress(),
        readiness(),
        resources(),
        html_foot(js),
    ]
    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
