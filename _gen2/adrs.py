from util import callout


ADRS = [
    ("Redux vs Context",
     "Multiple teams, growing issue view, some want a store.",
     "Default: server cache + URL + local + split context. Redux Toolkit only if many writers need a single event log / debug story.",
     "Context-only; Zustand; Redux; signals.",
     "Context is simpler until values churn. Redux is not automatically better; a god-store is worse than fat context.",
     "If we pick Redux, tickets still do not live there — they live in the query cache."),
    ("REST vs GraphQL",
     "Issue page needs issue + comments + watchers.",
     "REST + BFF with partial success and timeouts. GraphQL if we will staff a graph and many clients need custom shapes.",
     "Client N+1; GraphQL; BFF REST; tRPC.",
     "GraphQL is not automatically better; first-paint mega-queries are a failure mode.",
     "Measure TTFB. Split extras from LCP path."),
    ("Monolith vs micro-frontends",
     "20 engineers, one product, plugins exist.",
     "Modular monolith + iframe plugins for untrusted code. No Module Federation rewrite.",
     "One SPA; MFE runtime; iframes only.",
     "MFEs are not automatically better. Plugins already give isolation.",
     "Revisit if a team is blocked on release cadence and the contract is small."),
    ("CSR vs SSR",
     "Logged-in issue view vs marketing.",
     "CSR + skeleton for the app; SSR/ISR for public docs/marketing. Hydration cost is real.",
     "CSR; SSR; streaming RSC.",
     "SSR is not automatically faster INP. Hydration can hurt.",
     "Revisit if LCP of body text is the metric and HTML helps."),
    ("Client cache vs server/CDN cache",
     "Issue JSON vs hashed JS vs HTML.",
     "Hashed assets: CDN immutable. User JSON: app cache + short HTTP. HTML: private/no-store.",
     "Cache everything at CDN; cache nothing; SW for all.",
     "Invalidation vs hit-rate. No instant global consistency.",
     "Wrong HTML cache is a SEV."),
    ("Local vs global state",
     "Modal, filters, user, issues.",
     "Decision tree: server → URL → nearest parent → local. Global is a last resort.",
     "All Redux; all local; all URL.",
     "Global is not automatically scalable.",
     "Document the tree in the README of the feature."),
    ("WebSocket vs polling",
     "Board presence and remote moves.",
     "Poll 15–30s if freshness allows; WS if presence/moves are product-critical; always REST catch-up.",
     "WS only; SSE; poll; Firestore.",
     "WS is not automatically ‘realtime senior.’ Infra and degrade matter.",
     "Measure disconnects before celebrating."),
    ("Pagination vs infinite scroll",
     "Search vs feed.",
     "Search/admin: numbered or cursor pages in the URL. Feeds: infinite + virtualize + load-more fallback.",
     "Always infinite; always pages.",
     "Infinite is not automatically better UX (a11y, memory, share).",
     "Virtualize either."),
    ("MUI vs custom DS",
     "Need buttons now; 12 teams later.",
     "Headless a11y primitives + custom tokens/composites. Full MUI if time-to-market dominates and theming is enough.",
     "MUI; fully custom; copy Atlassian DS.",
     "Custom is not automatically more senior.",
     "A11y of combobox is the buy-vs-build hinge."),
]


def adrs() -> str:
    cards = []
    for i, (title, ctx, dec, alt, trade, cons) in enumerate(ADRS, 1):
        cards.append(f'''
<article class="topic adr" id="adr-{i}" data-search="ADR {title}" data-stype="ADR">
  <h3>ADR: {title}</h3>
  <p><b>Context.</b> {ctx}</p>
  <p><b>Decision.</b> {dec}</p>
  <p><b>Alternatives.</b> {alt}</p>
  <p><b>Trade-offs.</b> {trade}</p>
  <p><b>Consequences.</b> {cons}</p>
  <p><button type="button" class="toggle-btn" data-complete="topics" data-cid="adr-{i}">Mark complete</button></p>
</article>''')
    return f'''
<section class="block" id="adrs" data-search="Architecture Decision Records" data-stype="Section" data-cat="architecture">
  <p class="kicker">Why, not what</p>
  <h2 class="section-title">Architecture Decision Records</h2>
  <p class="lede">Practice answering “Why this architecture?” Template: Context → Decision → Alternatives → Trade-offs → Consequences. Redux/GraphQL/MFE/SSR are not automatically correct.</p>
  {''.join(cards)}
</section>
'''


def comms() -> str:
    steps = [
        ("Clarify requirements", "“I’d first clarify whether this needs real-time updates or eventual consistency, and whether plugins can run on the page.”"),
        ("Define users", "“The primary user is an engineer triaging 50 issues a day; the secondary is a manager opening a shared board URL.”"),
        ("Define scale", "“I’ll assume 400 visible cards, 10k in the filter, and up to 20 plugins — tell me if that’s wrong.”"),
        ("Identify critical flows", "“The money path is drag-to-transition and open-issue. I’ll optimize those first.”"),
        ("High-level architecture", "“I’d start with a modular monolith: shell, feature packages, query cache, design system. I would not introduce micro-frontends unless team deploy independence requires it.”"),
        ("Component boundaries", "“BoardPage composes virtualized columns; cards are presentational; useMoveIssue owns the mutation.”"),
        ("Data flow", "“URL is the filter source of truth. Snapshot GET, optimistic PATCH, invalidate issue+board keys.”"),
        ("State management", "“I’d keep server state separate from ephemeral UI state. Modal local; JQL in the URL; issues in the cache; theme in a tiny provider.”"),
        ("Caching", "“Hashed assets immutable at the CDN. Issue JSON short SWR. HTML private.”"),
        ("Performance", "“Virtualize first. Then isolate context. Memo is a last step after a Profiler recording.”"),
        ("Failures", "“409 rollback, WS drop to poll, plugin crash in an error boundary, kill switch via version.json.”"),
        ("Security", "“UI hides; server enforces. Encode issue HTML. HttpOnly session. Sandbox plugins.”"),
        ("Accessibility", "“Roving tabindex, live region on move, one Modal primitive, no color-only status.”"),
        ("Observability", "“Correlation id on the transition, drag INP mark, plugin crash rate, RUM slice by issue size.”"),
        ("Trade-offs", "“I accepted poll over WS to reduce infra cost; we can revisit if presence is a committed roadmap item.”"),
    ]
    body = []
    for i, (t, s) in enumerate(steps, 1):
        body.append(f'<div class="comm-step"><div class="comm-num">{i}</div><div><h3>{t}</h3><p class="say">{s}</p></div></div>')
    return f'''
<section class="block" id="comms" data-search="Interview Communication frontend system design" data-stype="Section">
  <p class="kicker">How you talk</p>
  <h2 class="section-title">Interview Communication</h2>
  <p class="lede">A repeatable 15-step frontend system-design script. Silence looks stuck. Naming rejected options looks senior.</p>
  {''.join(body)}
  {callout("Phrases to keep: “I’d start with a modular monolith and evolve toward independently deployed boundaries only when needed.” “I’d avoid micro-frontends unless team boundaries and deployment independence justify the complexity.”")}
</section>
'''
