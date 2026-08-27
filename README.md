# Interview Prep

Personal study hub. Live site:

**https://viren-ahire-1999.github.io/interview-prep/**

Open that URL on any machine. The home page lists every track. Each phase is still a single HTML file. Progress is stored in the browser (`localStorage`) on this site’s origin.

To add a future company or topic: add a track in `index.html` (`TRACKS`), then rebuild and push.

**Frontend System Design (expert course):** `frontend-system-design.html` — theory, 18 case studies, 24 design prompts, 80+ Q&A. Progress key: `fe-sd-v1`. Rebuild: `python3 _gen5/build.py`.

**DSA using JavaScript (from scratch → expert):** `dsa-javascript.html` — implement structures in JS, patterns, practical studies, problem bank, Q&A. Progress key: `dsa-js-v1`. Rebuild: `python3 _gen6/build.py`.

**AI Engineer (basics → production):** `ai-engineer.html` — foundations, classical ML, deep learning, RAG, agents, eval, safety, MLOps. Progress key: `ai-eng-v1`. Rebuild: `python3 _gen7/build.py`.

---

# Atlassian Senior SWE Interview Prep

Self-contained study sites. Use the hub above, or open the HTML files locally — no install, no server.

Target: Atlassian · Senior SWE / Senior Frontend / Full-stack  
Stack: React · TypeScript · JavaScript · Node.js · 7 years  
Cadence: ~2 hours/day · 6 days/week · 30 days (Phase 1–2) · 45 days (Phase 3) · 14-day final loop (Phase 4)

| Phase | File | Focus |
|---|---|---|
| 1 | `phase1-atlassian-prep.html` | DSA + JavaScript runtime |
| 2 | `phase2-atlassian-frontend-architecture.html` | Frontend architecture + React + large-scale web |
| 3 | `phase3-atlassian-system-design.html` | System design + distributed systems + backend architecture |
| 4 | `phase4-atlassian-interview-mastery.html` | Interview execution + behavioral + mocks + offer |

Resource Library links are optional and need the network. All teaching content is already in the HTML.

---

# Phase 4 — Interview Mastery

**Title:** ATlassian Senior SWE — Phase 4  
**Subtitle:** Interview Execution + Behavioral + Mock Interviews

Open `phase4-atlassian-interview-mastery.html`. Progress key: **`atl-phase4-v1`**.

Official Atlassian process and values are labeled **official** and linked. Everything else is practice — not a guaranteed loop and not official questions.

## How to use Phase 4

1. Write **your** stories in the Story Bank. Do not invent metrics.
2. Draft TMAY and Why Atlassian from the frameworks (not canned bios).
3. Run coding, craft, system-design, and project-interrogation mocks.
4. Complete at least one **Full Interview Loop**.
5. Follow the **14-Day Plan**. Last three days are light.
6. Leave when Readiness is honestly ~85% and the score band is Interview Ready or better.

Score weights (transparent): Technical 30% · System design 20% · Frontend 15% · Behavioral 15% · Communication 10% · Values 5% · Execution 5%.  
Bands: &lt;50 Not Ready · 50–69 Needs Work · 70–84 Interview Ready · ≥85 Strongly Ready.

Rebuild: `python3 _gen4/build.py`

---

# Phase 3 — System Design

**Title:** ATlassian Senior SWE — Phase 3  
**Subtitle:** System Design + Distributed Systems + Backend Architecture

Open `phase3-atlassian-system-design.html` (double-click or drag onto a browser).

Progress is stored in `localStorage` under **`atl-phase3-v1`**.

## How to use Phase 3

1. Start on the **Dashboard**. This phase is not “become a backend specialist” — it is senior judgment across the API boundary.
2. Open the **45-Day Plan**. Each day: 10 min revision, 45 min concept, 45 min design/exercise, 20 min verbal.
3. Calculate estimates on paper before revealing answers.
4. Speak the 16-step interview framework. Name the option you rejected.
5. Weekly: **Mock Interview Mode** (15 / 30 / 45 / 60 min). Score the rubric. Save a debrief.
6. Do not leave Phase 3 until **Readiness** is honestly ~85%.

## What is in the Phase 3 file

- Fundamentals, interview framework, 10 estimation drills
- API design, PostgreSQL, SQL, NoSQL
- Distributed systems, consistency, CAP
- Caching, Redis, queues, Kafka, pub/sub
- Load balancing, CDN, rate limiting, reliability, idempotency, locks, sharding
- Microservices, gateway, auth, realtime, files, search, notifications, pipelines, observability, security
- Node.js architecture + 13 backend exercises
- 20 large-scale case studies (Jira / Confluence / Trello and others)
- 42 system-design practice questions, 57 backend interview questions, 12 ADRs
- Mock interviews, spaced repetition, 290+ glossary terms, official-source library

Practice items are not claimed official Atlassian questions.

Rebuild: `python3 _gen3/build.py`

---

# Phase 2 — Frontend Architecture

**Title:** ATlassian Senior SWE — Phase 2  
**Subtitle:** Frontend Architecture + React + Large-Scale Web Engineering

Open `phase2-atlassian-frontend-architecture.html` (double-click or drag onto Chrome / Safari / Firefox / Edge).

Progress is stored in `localStorage` under **`atl-phase2-v1`** (separate from Phase 1).

## How to use Phase 2

1. Start on the **Dashboard**. Confirm objectives. Watch the top progress bar.
2. Open **30-Day Phase 2 Plan**. Expand today’s day. Check every box:
   - 10 min revision
   - 45 min concept / architecture
   - 45 min hands-on or design
   - 20 min verbal explanation
3. Study the named section (do not only highlight — draw the diagram).
4. Practice: interview questions, system-design cards, coding exercises, debug simulator.
5. Weekly: **Mock Interview Mode** (15 / 30 / 45 / 60 min). Speak the 15-step framework. Save a debrief.
6. Do not leave Phase 2 until **Readiness** is honestly ~85%.

Days 7, 14, 21, 28, and 30 are review + mock / gate days.

If you miss a day: finish that day’s verbal + one exercise. Do not double architecture volume.

## What is in the Phase 2 file

- Dashboard, 30-day plan, progress bars, search, light/dark theme
- Architecture fundamentals, production React architecture, component design, scalability
- React internals (Fiber, render vs commit, setState pipeline, lanes, Suspense)
- Reconciliation with key / remount examples
- State decision tree; server-state / fetching architecture
- React performance + production debugging scenarios
- Browser CRP, Core Web Vitals, HTTP caching, offline / resilience
- Design systems, micro-frontends (when not to use them)
- Security (defensive), accessibility, testing strategy, observability
- 10 large-scale case studies (Jira / Confluence / Trello-shaped and others)
- 30 frontend system-design practice problems (full 20-part answers)
- 130 React / frontend interview questions
- 15 hands-on coding exercises with solutions
- ADRs + interview communication phrases
- Mock interviews, 10-scenario debug simulator, spaced repetition, glossary (280+), official-source library

Practice items are labeled **practice question** — not claimed official Atlassian questions.

## Phase 2 progress fields

Theme, daily checkboxes, topic completions, question / design / exercise completions, mock history, spaced-repetition dates, readiness checklist.

**Progress → Reset all Phase 2 progress** clears `atl-phase2-v1` (theme is kept).

## Optional Phase 2 generator

```bash
python3 _gen2/build.py
```

---

# Phase 1 — DSA + JavaScript

Open `phase1-atlassian-prep.html`. Progress key: **`atl-phase1-v1`**.

## How to use the Phase 1 plan

1. Revision (10 min)
2. Named DSA problems (50–60 min) — Problem Bank, mark status
3. Named JavaScript topic (40–45 min)
4. Verbal question (10–15 min)

Days 7, 14, 21, 28, and 30 are review + mock days.

## What is in the Phase 1 file

- DSA curriculum (including Big O) and 12-pattern library
- 77 interview-style problems with TypeScript solutions
- JavaScript deep dive + 24 event-loop traces
- 80+ JS interview questions and 13 coding exercises
- Communication script, mock mode, spaced repetition, readiness gate

Do not start Phase 2 until the Phase 1 readiness checklist is honestly ~85%+.

## Optional Phase 1 generator

```bash
python3 _gen/build.py
```
