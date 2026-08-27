from util import callout


def mock() -> str:
    return r'''
<section class="block" id="mock" data-search="Mock Interview Mode frontend system design" data-stype="Section">
  <p class="kicker">Timed practice</p>
  <h2 class="section-title">Mock Interview Mode</h2>
  <p class="lede">Draws a random practice item from the design bank and Q&amp;A (<code>data-mock</code>). Speak the 16-step framework. Reveal after you have a plan. Save a debrief.</p>
  <div class="card" style="margin-bottom:16px">
    <p>Category
      <select id="mock-cat">
        <option value="all">All</option>
        <option value="architecture">Architecture</option>
        <option value="performance">Performance</option>
        <option value="security">Security</option>
        <option value="feed">Feed</option>
        <option value="work">Work software</option>
        <option value="search">Search</option>
        <option value="realtime">Realtime</option>
        <option value="data">Data</option>
        <option value="commerce">Commerce</option>
        <option value="media">Media</option>
        <option value="canvas">Canvas</option>
        <option value="platform">Platform</option>
      </select>
    </p>
    <div class="status-btns">
      <button type="button" class="toggle-btn" data-start-mock="15">15-min question</button>
      <button type="button" class="toggle-btn" data-start-mock="30">30-min design</button>
      <button type="button" class="toggle-btn" data-start-mock="45">45-min design</button>
      <button type="button" class="toggle-btn" data-start-mock="60">60-min full</button>
    </div>
    <div id="mock-panel"><p class="stat-sub">Pick a duration. Speak the 16 steps. Reveal only after you have boxes and a rejected option.</p></div>
  </div>
  <div class="card">
    <h3>Debrief rubric</h3>
    <label class="task"><input type="checkbox" id="mock-q-trade" /> <span>I named alternatives and trade-offs (not just a library)</span></label>
    <label class="task"><input type="checkbox" id="mock-q-time" /> <span>I hit failure, a11y, and security within time</span></label>
    <label class="task"><input type="checkbox" id="mock-q-a11y" /> <span>I mentioned a11y or security without being prompted</span></label>
    <p>Notes<br /><textarea id="mock-notes" rows="3" style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:inherit"></textarea></p>
    <p>Confidence
      <select id="mock-confidence">
        <option value="1">1</option><option value="2">2</option>
        <option value="3" selected>3</option><option value="4">4</option><option value="5">5</option>
      </select>
    </p>
    <p><button type="button" class="toggle-btn" id="save-mock">Save mock</button></p>
  </div>
  <div class="card" style="margin-top:16px"><h3>History</h3><div id="mock-history"></div></div>
</section>
'''


def progress() -> str:
    return r'''
<section class="block" id="progress" data-search="Progress Tracker frontend system design" data-stype="Section">
  <p class="kicker">localStorage fe-sd-v1</p>
  <h2 class="section-title">Progress Tracker</h2>
  <div class="grid grid-2">
    <div class="card"><h3>Daily tasks</h3><p id="track-days">0</p></div>
    <div class="card"><h3>Theory topics</h3><p id="track-arch">0</p><div class="bar"><span id="bar-cat-arch"></span></div></div>
    <div class="card"><h3>Case studies</h3><p id="track-react">0</p><div class="bar"><span id="bar-cat-react"></span></div></div>
    <div class="card"><h3>Interview questions</h3><p id="track-qs">0</p></div>
    <div class="card"><h3>Design prompts</h3><p id="track-sd">0</p><div class="bar"><span id="bar-cat-sd"></span></div></div>
    <div class="card"><h3>ADR / talk drills</h3><p id="track-ex">0</p></div>
    <div class="card"><h3>Performance</h3><div class="bar"><span id="bar-cat-perf"></span></div></div>
    <div class="card"><h3>Security</h3><div class="bar"><span id="bar-cat-sec"></span></div></div>
  </div>
  <p style="margin-top:18px"><button type="button" class="danger-btn" id="reset-progress">Reset all Frontend SD progress</button></p>
</section>
<section class="block" id="revision" data-search="Revision spaced repetition frontend SD" data-stype="Section">
  <p class="kicker">Remember on purpose</p>
  <h2 class="section-title">Revision System</h2>
  <p class="lede">Solved items review at 1 → 3 → 7 → 14 → 30 days. Attempted/failed → tomorrow. Mastered parks at 30 days.</p>
  <div class="grid grid-2">
    <div class="card"><h3>Due today</h3><ul class="tight" id="rev-today"></ul></div>
    <div class="card"><h3>Due this week</h3><ul class="tight" id="rev-week"></ul></div>
    <div class="card"><h3>Recently failed</h3><ul class="tight" id="rev-failed"></ul></div>
    <div class="card"><h3>Weak areas</h3><ul class="tight" id="rev-weak"></ul></div>
    <div class="card"><h3>Mastered</h3><ul class="tight" id="rev-mastered"></ul></div>
  </div>
</section>
'''


def readiness() -> str:
    groups = [
        ("Framework", [
            ("r-16", "Speak the 16 steps without notes"),
            ("r-30", "Cut a design to 30 minutes without dropping fail/a11y"),
            ("r-ask", "Ask three clarifying questions that fork the architecture"),
            ("r-num", "Guess client-scale numbers and label them as guesses"),
            ("r-v1", "Cut any prompt to a v1 money path in 20 seconds"),
        ]),
        ("Theory", [
            ("r-ren", "Choose CSR/SSR/SSG/islands for five surfaces and defend"),
            ("r-hyd", "Explain hydration mismatch and when CSR is honest"),
            ("r-url", "Explain the URL as a public API with examples"),
            ("r-st", "Place 12 states into URL / cache / local / ephemeral"),
            ("r-key", "Write cache keys and invalidation for board + issue"),
            ("r-race", "Explain abort + generation for typeahead/JQL"),
            ("r-bff", "Explain when a BFF/batch is warranted"),
            ("r-ws", "Pick poll/SSE/WS from a freshness SLA and degrade"),
            ("r-vit", "Connect LCP/INP/CLS to concrete code changes"),
            ("r-off", "Design drafts + conflict without lying"),
        ]),
        ("Products", [
            ("r-feed", "Design a feed in 45 minutes"),
            ("r-board", "Design a Jira-like board in 45 minutes"),
            ("r-doc", "Design a document read/edit split"),
            ("r-chat", "Design chat window + reconnect"),
            ("r-ac", "Design autocomplete with combobox + abort"),
            ("r-not", "Design notifications with REST as truth"),
            ("r-up", "Design a multi-GB uploader"),
            ("r-grid", "Design a 50k-row grid and define select-all"),
            ("r-pay", "Explain why checkout JS stays tiny"),
            ("r-fig", "Scope Figma honestly without bluffing CRDT"),
        ]),
        ("Security & a11y", [
            ("r-xss", "Name XSS paths beyond dangerouslySetInnerHTML"),
            ("r-csrf", "Explain CSRF vs CORS"),
            ("r-tok", "Explain why not localStorage access tokens"),
            ("r-plug", "Threat-model a plugin iframe host"),
            ("r-kbd", "Specify board keyboard + live region"),
            ("r-combo", "Name the APG combobox pattern"),
            ("r-focus", "Explain focus restore"),
        ]),
        ("Senior behavior", [
            ("r-rej", "Name two rejected options in every mock"),
            ("r-deg", "Say a degrade sentence without being prompted"),
            ("r-adr", "Speak a 60-second ADR with a consequence"),
            ("r-idk", "Handle an unknown (CRDT, map SDK) without freezing"),
            ("r-end", "Close with v1, rejects, metrics, and a question"),
        ]),
    ]
    html = []
    for title, items in groups:
        html.append(f"<h3>{title}</h3>")
        for id_, label in items:
            html.append(
                f'<label class="task"><input type="checkbox" data-id="{id_}" data-group="readiness" /><span>{label}</span></label>'
            )
    return f'''
<section class="block" id="readiness" data-search="Frontend system design readiness checklist" data-stype="Section">
  <p class="kicker">Gate</p>
  <h2 class="section-title">Readiness checklist</h2>
  <p class="lede">Check only if you can do it <i>today</i> without this file. Stay until ~85% and 8+ mocks.</p>
  <p class="stat">Score: <span id="ready-score">0%</span></p>
  <div class="bar"><span id="bar-ready-final"></span></div>
  <p id="ready-gate" class="stat-sub"></p>
  {''.join(html)}
</section>
'''


def resources() -> str:
    rows = [
        ("web.dev performance", "https://web.dev/explore/performance", "LCP, INP, CLS, optimize guides.", "Pairs with Performance architecture.", "Vitals", False),
        ("web.dev INP", "https://web.dev/articles/inp", "Interaction to Next Paint.", "The money metric for laggy UIs.", "Performance", False),
        ("MDN Web Docs", "https://developer.mozilla.org/", "HTML, HTTP, a11y, Fetch, workers.", "Platform source of truth.", "Browser", False),
        ("MDN HTTP caching", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching", "Cache-Control, validators.", "With Data and caching.", "Network", False),
        ("MDN CSP", "https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP", "Content-Security-Policy.", "After Security.", "Security", True),
        ("WCAG 2.2", "https://www.w3.org/WAI/WCAG22/quickref/", "Official criteria.", "POUR + money path, not memorizing numbers.", "A11y", False),
        ("WAI-ARIA APG", "https://www.w3.org/WAI/ARIA/apg/", "Combobox, dialog, grid.", "Say the pattern by name.", "A11y", False),
        ("OWASP Cheat Sheet Series", "https://cheatsheetseries.owasp.org/", "XSS, CSRF, session.", "Defensive checklists.", "Security", True),
        ("React docs — Learn", "https://react.dev/learn", "Rendering model, effects.", "Runtime detail lives in Phase 2 on this hub.", "React", True),
        ("TanStack Query", "https://tanstack.com/query/latest/docs/framework/react/overview", "Keys, staleTime, invalidation.", "One implementation of the data chapter.", "Server state", True),
        ("Atlassian Design System", "https://atlassian.design/", "Tokens, components, a11y.", "Taste. Not a question dump.", "DS", True),
        ("Atlassian Engineering blog", "https://www.atlassian.com/blog/atlassian-engineering", "How they write about frontend scale.", "Culture, not official questions.", "Company", True),
        ("Chrome DevTools performance", "https://developer.chrome.com/docs/devtools/evaluate-performance", "Performance panel.", "How you actually debug INP.", "Perf", False),
        ("web.dev images", "https://web.dev/learn/images", "Responsive images, LCP.", "Feeds and PDPs.", "LCP", True),
    ]
    cards = []
    for name, url, what, why, topic, opt in rows:
        badge = '<span class="badge badge-opt">Optional</span>' if opt else '<span class="badge badge-pattern">Primary</span>'
        cards.append(f'''
<article class="card" data-search="{name}" data-stype="Resource">
  <div class="meta-row">{badge}</div>
  <h3><a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a></h3>
  <p><b>Teaches.</b> {what}</p>
  <p><b>Why open it.</b> {why}</p>
  <p><b>Course topic.</b> {topic}</p>
</article>''')
    return f'''
<section class="block" id="resources" data-search="Resource library frontend system design" data-stype="Section">
  <p class="kicker">Official first</p>
  <h2 class="section-title">Resource Library</h2>
  <p class="lede">This HTML already contains the teaching. Links are for specs and signatures. Phase 2 on the hub is the React-runtime companion.</p>
  <div class="grid grid-2">{''.join(cards)}</div>
</section>
'''


def glossary() -> str:
    terms = [
        ("App shell", "Always-on chrome. Must stay small."),
        ("BFF", "Backend-for-frontend: a view-model or batch layer for one client."),
        ("Bootstrap payload", "First response with user + critical flags to kill waterfalls."),
        ("Cache key", "Identity of a server fact in the client cache."),
        ("Capability token", "Short-lived scoped credential for a plugin slot."),
        ("CLS", "Cumulative Layout Shift — visual jump."),
        ("Combobox", "APG pattern for typeahead / command palette."),
        ("Critical path", "First paint, first money interaction, first failure."),
        ("CRDT / OT", "True multiplayer sync. Rarely a 45-minute implementation."),
        ("CSR", "Client-side render. Honest for logged-in tools."),
        ("Cursor pagination", "Stable paging for mutating lists and feeds."),
        ("Degrade", "The job still completes when the fancy channel dies."),
        ("Ephemeral state", "Drag, caret, hover — usually refs, not document store."),
        ("Generation token", "Monotonic id so stale responses are dropped."),
        ("Hydration", "Attaching client runtime to server HTML."),
        ("Idempotency key", "clientMutationId so retries do not double-apply."),
        ("If-Match", "Optimistic concurrency via version."),
        ("INP", "Interaction to Next Paint — lag."),
        ("Island", "Small interactive widget on mostly static HTML."),
        ("ISR", "Incremental static regeneration — public pages at the edge."),
        ("LCP", "Largest Contentful Paint — main content appeared."),
        ("Modular monolith", "Packages and import rules without runtime MFEs."),
        ("N+1 (client)", "One request per row/widget instead of a batch."),
        ("SWR", "Show stale, revalidate in background — also a library name."),
        ("SSR", "HTML for this request. Watch hydration cost."),
        ("SSG", "Prebuilt HTML. CDN-friendly."),
        ("staleTime", "How long a client cache is trusted before refetch. Not HTTP cache."),
        ("Virtualize", "Render only visible rows. Costs measure + a11y work."),
    ]
    items = []
    for name, defn in terms:
        items.append(f'<article class="card glossary-item" data-search="{name}"><h3>{name}</h3><p>{defn}</p></article>')
    return f'''
<section class="block" id="glossary" data-search="Glossary frontend system design" data-stype="Section">
  <p class="kicker">Language</p>
  <h2 class="section-title">Glossary</h2>
  <p><input id="glossary-filter" type="search" placeholder="Filter terms..." style="width:100%;max-width:360px;padding:8px 10px;border-radius:8px;border:1px solid var(--border);background:var(--bg);color:inherit" /></p>
  <div class="grid grid-2" style="margin-top:16px">{''.join(items)}</div>
</section>
'''
