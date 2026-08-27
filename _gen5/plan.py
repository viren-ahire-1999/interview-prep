DAYS = [
  {"n": 1, "title": "What frontend system design is",
   "learn": "FE SD vs backend SD vs “just React”. Users, surfaces, critical path, rejected options.",
   "do": "Write a one-page definition: what you will and will not draw in a 45-minute FE interview.",
   "verbal": "An interviewer says “design Instagram.” What do you clarify in the first four minutes?",
   "rev": "Phase 2: state ownership tree. URL vs server cache vs local."},
  {"n": 2, "title": "The 16-step interview framework",
   "learn": "Timing, clarifying questions, NFRs, assumptions, architecture, API, state, cache, fail, a11y, trade-offs.",
   "do": "Speak the 16 steps from memory. Time yourself. Then read the Framework section.",
   "verbal": "What do you do if they only gave you 30 minutes?",
   "rev": "Yesterday’s “what I will not draw” list."},
  {"n": 3, "title": "Requirements and frontend scale",
   "learn": "Functional vs non-functional. Capacity that matters on the client: DOM nodes, payload, tabs, collaborators.",
   "do": "Estimate a Jira-like board: cards on screen, filter size, collaborators, plugin iframes. Write the numbers you would say.",
   "verbal": "Why is “10 million users” a weak FE scale statement by itself?",
   "rev": "16 steps in 60 seconds."},
  {"n": 4, "title": "Rendering models",
   "learn": "CSR, SSR, SSG, ISR, streaming, islands, resumability. Hydration cost. When CSR is the adult answer.",
   "do": "Pick a rendering model for: marketing site, Jira board, Confluence read view, Confluence editor, checkout.",
   "verbal": "Why can SSR make INP worse if you hydrate a 2MB tree?",
   "rev": "LCP vs TTFB vs hydration long task."},
  {"n": 5, "title": "Routing, shells, and splitting",
   "learn": "App shell, route-level split, component split, prefetch, waterfalls, shared chrome.",
   "do": "Draw the route graph for a workspace: home, board, issue, search, admin. Mark what is in the shell vs lazy.",
   "verbal": "When is route-based code splitting not enough?",
   "rev": "Rendering choice from day 4 for the same workspace."},
  {"n": 6, "title": "State architecture",
   "learn": "URL as source of truth. Server cache. Local UI. Ephemeral (drag, caret). Context pitfalls.",
   "do": "Classify 16 states on an issue view. Put each in URL / cache / local / ephemeral.",
   "verbal": "Why is “we use Redux” not a state architecture?",
   "rev": "Phase 2 decision tree. Recite it."},
  {"n": 7, "title": "Week 1 review + 30-min mock",
   "learn": "Framework + rendering + state mixed.",
   "do": "Timed mock: any design prompt. Speak 16 steps. Save debrief.",
   "verbal": "Design autocomplete in 12 minutes: clarify, API, a11y, abort.",
   "rev": "Mark weak theory Review. Do not add a new library today."},
  {"n": 8, "title": "Data fetching and cache keys",
   "learn": "Lifecycle, keys, staleTime vs HTTP cache, invalidation, pagination, cancellation, optimistic updates.",
   "do": "Write cache keys + invalidation map for board + issue + comments + current user.",
   "verbal": "User changes JQL twice in 200ms. What races, and how do you kill them?",
   "rev": "AbortController + generation token."},
  {"n": 9, "title": "BFF, REST, GraphQL, and the client contract",
   "learn": "Overfetch, underfetch, N+1 widgets, batching, versioning, errors as data.",
   "do": "Design the first three endpoints for a 100-widget dashboard. Avoid 100 waterfalls.",
   "verbal": "When would you add a BFF, and when is it ceremony?",
   "rev": "Cache keys from yesterday."},
  {"n": 10, "title": "Realtime",
   "learn": "Poll, SSE, WebSocket, push. Presence vs document. Fan-in, reconnect, backpressure, at-least-once.",
   "do": "Design notifications + presence for a board. Name the degrade path when WS dies.",
   "verbal": "Why is “just use WebSockets” a junior opening?",
   "rev": "Optimistic UI vs confirmed event."},
  {"n": 11, "title": "Performance as architecture",
   "learn": "CRP, LCP, INP, CLS, long tasks, virtualization, workers, budgets.",
   "do": "For a feed, list one concrete change that moves each of LCP, INP, CLS.",
   "verbal": "How do you debug a laggy React app in 15 minutes?",
   "rev": "Virtualize vs paginate vs window."},
  {"n": 12, "title": "Offline, sync, and conflicts",
   "learn": "Drafts, queues, idempotency, last-write, CRDT, “you are offline” UX.",
   "do": "Design comment drafts across two tabs + a flight-mode commute.",
   "verbal": "How does the frontend deal with eventual consistency without lying to the user?",
   "rev": "Idempotency keys on retry."},
  {"n": 13, "title": "Design systems and multi-team UI",
   "learn": "Tokens, composition, versioning, theming, a11y in the kit, contribution model.",
   "do": "Write an ADR: button API (variants vs infinite props) for 12 product teams.",
   "verbal": "How do you stop a design system from becoming a junk drawer?",
   "rev": "Tokens vs hardcoded hex in features."},
  {"n": 14, "title": "Week 2 review + 45-min mock",
   "learn": "Data + realtime + performance + offline.",
   "do": "45-min design: news feed or notifications. Save debrief.",
   "verbal": "Recite cache key + invalidation for issue list + detail.",
   "rev": "Weak performance or realtime topic."},
  {"n": 15, "title": "Collaboration and conflict",
   "learn": "Locks, OT, CRDT, presence, cursors. Honest limits of “Google Docs in 45 minutes.”",
   "do": "Design Confluence-like page edit: save, version, conflict, read vs edit split.",
   "verbal": "What do you say if they ask you to implement CRDT on a whiteboard?",
   "rev": "If-Match / version tokens."},
  {"n": 16, "title": "Auth, tenancy, and permissions",
   "learn": "Session vs token, cookie, CSRF, tenant isolation, UI that hides vs server that denies.",
   "do": "Draw authz checks for issue transition + plugin iframe + export.",
   "verbal": "Why must the client never be the source of truth for permissions?",
   "rev": "Phase 2: why not access tokens in localStorage."},
  {"n": 17, "title": "Security architecture",
   "learn": "XSS in React, HTML, markdown, plugins. CSP, CSRF, clickjacking, supply chain.",
   "do": "Threat-model a macro/iframe host. Write three concrete controls.",
   "verbal": "dangerouslySetInnerHTML is not the only XSS path. Name two more.",
   "rev": "Sanitize vs encode vs CSP as layers."},
  {"n": 18, "title": "Accessibility as architecture",
   "learn": "POUR, semantics first, focus, combobox, grid, live regions, design-system ownership.",
   "do": "Specify keyboard model for a board (roving tabindex, move, announce).",
   "verbal": "When is ARIA required, and when is it a smell?",
   "rev": "Focus restore on modal close."},
  {"n": 19, "title": "Observability, flags, experiments",
   "learn": "RUM, errors, correlation ids, sampling, flags as architecture, experiment flicker.",
   "do": "Define 8 metrics for a board launch. Which are SLIs vs product?",
   "verbal": "How do you ship a flag without a CLS banner jump?",
   "rev": "Error boundary vs page death."},
  {"n": 20, "title": "Micro-frontends — mostly when not to",
   "learn": "Build-time packages vs runtime iframes vs module federation. People-scale vs runtime cost.",
   "do": "ADR: plugin host for a Jira-like app. Pick iframe or package and defend.",
   "verbal": "A staff engineer says “we should federate everything.” How do you answer?",
   "rev": "Modular monolith first."},
  {"n": 21, "title": "Week 3 review + 60-min mock",
   "learn": "Collab + auth + security + a11y + MFE.",
   "do": "60-min full loop: Jira-like board or Confluence editor. Score the rubric.",
   "verbal": "Name two options you rejected in that design.",
   "rev": "Readiness checklist first pass. Honest."},
  {"n": 22, "title": "Case studies — feeds and media",
   "learn": "News feed, YouTube watch, Netflix browse, gallery.",
   "do": "Complete two case studies. Draw each architecture before reading the answer.",
   "verbal": "What is the critical path of a feed’s first paint?",
   "rev": "Virtualization + image LCP."},
  {"n": 23, "title": "Case studies — work software",
   "learn": "Board, document, chat, email, data grid, dashboard.",
   "do": "Complete two work-software cases. Write one ADR sentence per case.",
   "verbal": "Board vs document: what is different about state and realtime?",
   "rev": "Plugin isolation from day 17."},
  {"n": 24, "title": "Case studies — hard surfaces",
   "learn": "Canvas/Figma honesty, maps, uploader, command palette, comments.",
   "do": "Complete the canvas case and the uploader case. Be honest about 45-minute scope.",
   "verbal": "How do you scope Figma in an interview without bluffing CRDT?",
   "rev": "Workers for hash/encode."},
  {"n": 25, "title": "Question bank — theory",
   "learn": "Rendering, state, data, performance questions.",
   "do": "Answer 20 Q&A standing up. Mark complete only if you can teach the short answer.",
   "verbal": "SSR vs CSR in 90 seconds, with one product example each.",
   "rev": "Weak Qs to Review."},
  {"n": 26, "title": "Question bank — senior judgment",
   "learn": "Security, a11y, MFE, collab, observability questions.",
   "do": "Answer 20 more Q&A. Write three “I would not do X because.”",
   "verbal": "localStorage tokens — why not, and what instead?",
   "rev": "CSP as defense in depth."},
  {"n": 27, "title": "Design bank grind",
   "learn": "Timed prompts from the Design Bank.",
   "do": "Three 20-minute designs. Reveal after each. Status: attempted / solved.",
   "verbal": "Pick the weakest of the three and redo the first 8 minutes.",
   "rev": "16-step framework under time pressure."},
  {"n": 28, "title": "Gate + full mock",
   "learn": "Readiness checklist. Honest score.",
   "do": "60-min mock. Then light revision only. Do not start a new topic.",
   "verbal": "Teach the 16-step framework to a rubber duck with no notes.",
   "rev": "Due-today revision queue."},
]


def plan() -> str:
    cards = []
    for d in DAYS:
        n = d["n"]
        body = [
            f'<label class="task"><input type="checkbox" data-id="d{n}-rev" data-group="checks" /><span><b>Revision</b> {d["rev"]}</span></label>',
            f'<label class="task"><input type="checkbox" data-id="d{n}-learn" data-group="checks" /><span><b>Concept</b> {d["learn"]}</span></label>',
            f'<label class="task"><input type="checkbox" data-id="d{n}-do" data-group="checks" /><span><b>Exercise</b> {d["do"]}</span></label>',
            f'<label class="task"><input type="checkbox" data-id="d{n}-verbal" data-group="checks" /><span><b>Verbal</b> {d["verbal"]}</span></label>',
        ]
        cards.append(f'''<article class="day" id="fesd-day-{n}">
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
<section class="block" id="plan" data-search="28-Day Frontend System Design Plan" data-stype="Section">
  <p class="kicker">Schedule</p>
  <h2 class="section-title">28-Day Expert Plan</h2>
  <p class="lede">Six days a week is enough; day 28 is a gate. Expand a day; checkboxes persist. If you miss a day, finish the verbal + one exercise — do not binge three case studies to “catch up.”</p>
  <div class="card" style="margin-bottom:16px">
    <h3>Daily cadence</h3>
    <table>
      <tr><th>Time</th><th>Block</th><th>Rule</th></tr>
      <tr><td>10 min</td><td>Revision</td><td>Yesterday’s diagram or a weak checklist item. No new topics.</td></tr>
      <tr><td>45 min</td><td>Concept</td><td>Read the named section. Draw. Do not only highlight.</td></tr>
      <tr><td>45 min</td><td>Exercise</td><td>Design on paper or speak. Reveal answers after you have a plan.</td></tr>
      <tr><td>20 min</td><td>Verbal</td><td>Answer standing up. Then uncover the bank.</td></tr>
    </table>
  </div>
  {''.join(cards)}
</section>
'''
