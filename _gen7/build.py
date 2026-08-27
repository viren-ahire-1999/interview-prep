#!/usr/bin/env python3
from pathlib import Path

from header import html_head, html_foot
from dashboard import dashboard
from plan import plan
from start import howto, role
from foundations import field_map, python_ai, math_need, data_leak
from classical import supervised, models, metrics, features
from deep import neural, cnn_seq, transformers
from genai import embeddings, llms, prompting, rag, finetune, agents, evaluation, safety
from production import serving, mlops, design
from practical import practical
from problems import problems
from questions import feq
from rest import mock, progress, readiness, resources, glossary

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "ai-engineer.html"


def main() -> None:
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    js = (ROOT / "app.js").read_text(encoding="utf-8")
    parts = [
        html_head(css),
        dashboard(),
        plan(),
        howto(),
        role(),
        field_map(),
        python_ai(),
        math_need(),
        data_leak(),
        supervised(),
        models(),
        metrics(),
        features(),
        neural(),
        cnn_seq(),
        transformers(),
        embeddings(),
        llms(),
        prompting(),
        rag(),
        finetune(),
        agents(),
        evaluation(),
        safety(),
        serving(),
        mlops(),
        design(),
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
