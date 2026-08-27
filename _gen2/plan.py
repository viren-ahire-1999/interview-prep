DAYS = [
  {"n": 1, "title": "Architecture fundamentals",
   "learn": "Coupling, cohesion, dependency direction, boundaries, contracts. Monolith vs modular monolith.",
   "do": "Sketch two folder structures for a 20-engineer React app (feature-sliced vs layered) and list what each makes easy/hard.",
   "verbal": "How would you structure a large React application used by 20 engineers?",
   "rev": "Phase 1: closures + event loop in 5 minutes so the runtime model stays warm."},
  {"n": 2, "title": "Folder structures and DDD-lite",
   "learn": "Feature-based vs domain-driven vs layered. When entities/ vs features/ pays off. Public APIs between packages.",
   "do": "Draw package boundaries for Jira-like: issues, boards, search, admin. Mark allowed imports.",
   "verbal": "What is a boundary, and how do you enforce it without a monorepo police state?",
   "rev": "Yesterday’s coupling/cohesion definitions out loud."},
  {"n": 3, "title": "Production React architecture",
   "learn": "Smart vs presentational (updated: container hooks), service layer, API client, error boundaries, feature flags, config.",
   "do": "Write a one-page architecture for a Confluence-like space home: routes, services, feature flags, analytics.",
   "verbal": "Where do permissions, analytics, and logging live so features do not each reinvent them?",
   "rev": "Dependency direction: UI → application → domain → infra."},
  {"n": 4, "title": "React internals — Fiber mental model",
   "learn": "Element vs Fiber, virtual DOM myth, render phase, commit phase, scheduling, priorities.",
   "do": "Draw the setState() pipeline from update object to DOM to useEffect.",
   "verbal": "What happens when setState is called? Walk interruptible render.",
   "rev": "Phase 1: microtasks vs tasks — React 18 batches across them."},
  {"n": 5, "title": "Concurrent rendering and Suspense",
   "learn": "Transitions, deferred values, Suspense for data (conceptually), batching, useTransition vs useDeferredValue.",
   "do": "Design a Jira filter panel that stays snappy while a 10k-issue list updates (transition + virtualization plan).",
   "verbal": "Why must rendering be treated as potentially interruptible?",
   "rev": "Render vs commit: which can be thrown away?"},
  {"n": 6, "title": "Reconciliation and keys",
   "learn": "Identity, keys, remount vs reuse, index keys, conditionals, position changes.",
   "do": "Predict 6 key/conditional examples in the Reconciliation section before revealing.",
   "verbal": "What happens when key A becomes key B on the same component type?",
   "rev": "Fiber = instance identity. Key is how you name the instance."},
  {"n": 7, "title": "Week 1 review + 30-min mock",
   "learn": "Architecture + internals + keys mixed.",
   "do": "Timed mock: React internals category. Then re-teach Fiber to a rubber duck.",
   "verbal": "Explain render vs commit and why keys exist, without notes.",
   "rev": "Mark weak topics Review. Do not add new libraries today."},
  {"n": 8, "title": "State ownership decision tree",
   "learn": "Local, lifted, URL, context, Redux/Zustand, server cache. What belongs where.",
   "do": "Classify 12 states for a Jira issue view (filter, modal, user, issues, theme, draft comment…).",
   "verbal": "Context vs Redux — when does each become the wrong tool?",
   "rev": "Server state is not global UI state."},
  {"n": 9, "title": "Data fetching architecture",
   "learn": "Lifecycle, cache, invalidation, optimistic updates, pagination, cancellation, races, dedupe.",
   "do": "Design a cache key + invalidation map for issue list + issue detail + board columns.",
   "verbal": "How do you prevent a race when the user changes JQL quickly?",
   "rev": "AbortController + ignore stale generation tokens."},
  {"n": 10, "title": "React performance — judgment",
   "learn": "Why memo everywhere fails. Colocation, selectors, context split, derived state, virtualization.",
   "do": "Refactor a before/after example: context that holds {user, theme, tickets}.",
   "verbal": "When does useCallback make things worse?",
   "rev": "Profile first. Memo last."},
  {"n": 11, "title": "Performance debugging scenarios",
   "learn": "20k-row table, laggy search, context storms, 5MB bundle, 4s TTI.",
   "do": "Walk scenarios 1–5 in Perf Debugging. Write the first DevTools click for each.",
   "verbal": "How would you debug a slow React app in 15 minutes?",
   "rev": "INP vs LCP — which metric for the search box?"},
  {"n": 12, "title": "Browser architecture / CRP",
   "learn": "DNS→TCP→TLS→HTTP, HTML parse, CSSOM, render tree, layout, paint, composite, priorities.",
   "do": "Annotate a waterfall for a Confluence page: what blocks LCP?",
   "verbal": "Explain the critical rendering path as if drawing on a whiteboard.",
   "rev": "Forced reflow from Phase 1 JS section."},
  {"n": 13, "title": "Core Web Vitals as engineering",
   "learn": "LCP, INP, CLS, TTFB, FCP, long tasks. Connect each to a code decision.",
   "do": "For a Jira board, list one concrete change that moves each vital.",
   "verbal": "Why can INP be bad when Lighthouse LCP looks fine?",
   "rev": "Long tasks > 50ms. Yield, workers, debounce."},
  {"n": 14, "title": "Week 2 review + architecture mock",
   "learn": "State + fetch + performance + vitals.",
   "do": "30-min architecture mock. Save debrief.",
   "verbal": "What state belongs where? Recite the decision tree.",
   "rev": "Weak performance scenario again."},
  {"n": 15, "title": "Networking and HTTP cache",
   "learn": "H1/H2/H3, CDN, Cache-Control, ETag, SWR, compression.",
   "do": "Write cache headers for: hashed JS assets, issue JSON, user session, avatars.",
   "verbal": "Explain cache invalidation trade-offs without saying 'just hash everything.'",
   "rev": "stale-while-revalidate vs React Query staleTime."},
  {"n": 16, "title": "Offline and resilience",
   "learn": "Service workers, backoff, optimistic UI, conflicts, graceful degradation.",
   "do": "Design offline comment draft + retry for Confluence. Conflict: two tabs.",
   "verbal": "How does the frontend deal with eventual consistency?",
   "rev": "Idempotency keys on writes."},
  {"n": 17, "title": "Design systems",
   "learn": "Tokens, composition, theming, versioning, breaking changes, headless vs styled, multi-team adoption.",
   "do": "Specify a Button API (props, a11y, variants) and a versioning policy for a breaking change.",
   "verbal": "How do you roll a design system across 12 product teams without a rewrite?",
   "rev": "Atlassian Design System is a reference, not a requirement to memorize."},
  {"n": 18, "title": "Micro-frontends — decision, not fashion",
   "learn": "Why/why not, runtime vs build-time, module federation, shared deps, auth, routing costs.",
   "do": "Write an ADR: modular monolith for Jira vs MFE. You must pick and defend.",
   "verbal": "When would you refuse micro-frontends in a senior interview?",
   "rev": "Team boundaries ≠ deployable JS bundles."},
  {"n": 19, "title": "Frontend security",
   "learn": "XSS, CSRF, CORS, CSP, cookies, token storage, OAuth/JWT, supply chain — defensive only.",
   "do": "Threat-model a Jira comment field + plugin iframe. List mitigations.",
   "verbal": "Where do you store tokens and why is localStorage usually the wrong default?",
   "rev": "CSP is defense in depth, not a substitute for encoding."},
  {"n": 20, "title": "Accessibility as architecture",
   "learn": "Semantics, focus, ARIA, live regions, modals, dynamic content, contrast.",
   "do": "Fix the BAD modal example. Write a focus-trap checklist.",
   "verbal": "How do you make accessibility a design-time constraint, not a sprint-end ticket?",
   "rev": "ARIA is a last resort after native HTML fails."},
  {"n": 21, "title": "Week 3 review + 45-min design mock",
   "learn": "Security + a11y + MFE + DS.",
   "do": "45-min system design: autocomplete or notifications. Use the 15-step script.",
   "verbal": "Recite the communication framework from memory.",
   "rev": "XSS + focus management — two sentences each."},
  {"n": 22, "title": "Testing strategy",
   "learn": "Pyramid, RTL philosophy, E2E cost, contracts, visual regression, what not to test.",
   "do": "Write a test plan for an IssueCreateModal: unit / RTL / Playwright / what you skip.",
   "verbal": "What should you not test in a React unit test?",
   "rev": "User-centric queries over implementation details."},
  {"n": 23, "title": "Observability",
   "learn": "Logs, metrics, traces, error tracking, RUM, correlation IDs. Debug: 'Jira issue page is randomly slow.'",
   "do": "Write the investigation playbook for that symptom (10 steps).",
   "verbal": "How do you correlate a user-reported slowness to a trace?",
   "rev": "INP + long tasks + API p95 — three signals, one story."},
  {"n": 24, "title": "Case study — Jira-like board",
   "learn": "Read the full Jira-like case study. Virtualization, realtime, permissions.",
   "do": "Timebox 50 min: whiteboard the board without looking at the answer, then compare.",
   "verbal": "How do you keep a 400-card board interactive?",
   "rev": "Column = virtualizer + query key + optimistic move."},
  {"n": 25, "title": "Case studies — Confluence + Trello + dashboard",
   "learn": "Document app, board, 100-widget dashboard — skim all three, deep-dive one.",
   "do": "Pick Confluence or dashboard. Write NFRs and the first 3 bottlenecks.",
   "verbal": "Collaborative editor: CRDT vs OT vs 'don't, use comments' — trade-offs.",
   "rev": "Widget dashboards die from N+1 fetches and layout shift."},
  {"n": 26, "title": "System design drills",
   "learn": "Autocomplete, file uploader, notifications, plugin architecture — read four cards.",
   "do": "45 min: design multi-GB uploader out loud. Then compare to the bank.",
   "verbal": "How do you resume a failed 4GB upload?",
   "rev": "Chunk + etag + idempotency + progress store."},
  {"n": 27, "title": "ADRs and speaking like an owner",
   "learn": "All ADR examples. Communication phrases.",
   "do": "Write a 1-page ADR: REST vs GraphQL for issue search. Then say it in 3 minutes.",
   "verbal": "Why did you choose this architecture? (no library-name answers)",
   "rev": "Start with context and constraints, then decision."},
  {"n": 28, "title": "60-minute full mock",
   "learn": "Full round: 15 min React internals + 45 min Jira board or collaborative doc.",
   "do": "Record yourself (phone). Score the debrief honestly.",
   "verbal": "Entire 15-step framework, timed.",
   "rev": "Notes on where you went silent."},
  {"n": 29, "title": "Debug simulator + weak topics",
   "learn": "All 10 debug scenarios. Close gaps from readiness.",
   "do": "Run 5 simulator cases without peeking clues first.",
   "verbal": "React app slow after 20 tabs — systematic answer.",
   "rev": "Memory leaks: listeners, detached DOM, caches."},
  {"n": 30, "title": "Readiness gate",
   "learn": "Checklist only if you can do it today without this file.",
   "do": "One Easy React verbal + one 45-min design. Complete the checklist honestly.",
   "verbal": "Teach Fiber, keys, state ownership, XSS, INP, and modular monolith in 12 minutes.",
   "rev": "If score < 85%, schedule another week — do not fake Phase 3."},
]


def plan() -> str:
    cards = []
    for d in DAYS:
        n = d["n"]
        tasks = [
            ("Learn (45 min)", d["learn"]),
            ("Hands-on / design (45 min)", d["do"]),
            ("Verbal (20 min)", d["verbal"]),
            ("Revision (10 min)", d["rev"]),
        ]
        body = []
        for i, (label, text) in enumerate(tasks):
            body.append(
                f'<label class="task"><input type="checkbox" data-id="p2d{n}-t{i}" data-group="checks" />'
                f"<span><b>{label}</b>{text}</span></label>"
            )
        cards.append(f'''<article class="day" id="p2-day-{n}">
  <button type="button" class="day-head">
    <div>
      <h3>Day {n} — {d["title"]}</h3>
      <div class="day-meta">~2 hours · 10 revision · 45 concept · 45 exercise · 20 speaking</div>
    </div>
    <span class="badge badge-pattern">Day {n}</span>
  </button>
  <div class="day-body">{''.join(body)}</div>
</article>''')
    return f'''
<section class="block" id="plan" data-search="30-Day Phase 2 Plan" data-stype="Section">
  <p class="kicker">Schedule</p>
  <h2 class="section-title">30-Day Phase 2 Plan</h2>
  <p class="lede">Six days a week. Days 7, 14, 21, 28, 30 are mocks/gates. Expand a day; checkboxes persist. If you miss a day, finish the verbal + one exercise — do not double architecture volume.</p>
  <div class="card" style="margin-bottom:16px">
    <h3>Daily cadence</h3>
    <table>
      <tr><th>Time</th><th>Block</th><th>Rule</th></tr>
      <tr><td>10 min</td><td>Revision</td><td>Yesterday’s diagram or weak checklist item. No new topics.</td></tr>
      <tr><td>45 min</td><td>Concept</td><td>Read the named section. Draw. Do not only highlight.</td></tr>
      <tr><td>45 min</td><td>Exercise</td><td>Implement or design. Speak as if an interviewer is present.</td></tr>
      <tr><td>20 min</td><td>Verbal</td><td>Answer the day’s question standing up. Then uncover the bank answer.</td></tr>
    </table>
  </div>
  {''.join(cards)}
</section>
'''
