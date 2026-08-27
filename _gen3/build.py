#!/usr/bin/env python3
from pathlib import Path

from header import html_head, html_foot
from dashboard import dashboard
from plan import plan
from fundamentals import fundamentals, framework, estimation
from api_db import api, database, sql, nosql
from distributed import distributed, consistency, cap, caching, redis, queues, kafka, pubsub
from scale_svc import (
    loadbalancing, proxy_cdn, ratelimit, reliability, idempotency, locks,
    replication, distxact, microservices, communication, gateway, auth,
    realtime, files, search, notifications, pipelines, observability, security,
)
from node_ex import nodejs, exercises
from cases import cases
from sdq import sysdesign
from beq import beq
from adrs import adrs
from glossary import glossary
from rest import mock, progress, readiness, resources

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "phase3-atlassian-system-design.html"


def main() -> None:
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    js = (ROOT / "app.js").read_text(encoding="utf-8")
    parts = [
        html_head(css),
        dashboard(),
        plan(),
        fundamentals(),
        framework(),
        estimation(),
        api(),
        database(),
        sql(),
        nosql(),
        distributed(),
        consistency(),
        cap(),
        caching(),
        redis(),
        queues(),
        kafka(),
        pubsub(),
        loadbalancing(),
        proxy_cdn(),
        ratelimit(),
        reliability(),
        idempotency(),
        locks(),
        replication(),
        distxact(),
        microservices(),
        communication(),
        gateway(),
        auth(),
        realtime(),
        files(),
        search(),
        notifications(),
        pipelines(),
        observability(),
        security(),
        nodejs(),
        exercises(),
        cases(),
        sysdesign(),
        beq(),
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
