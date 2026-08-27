from util import callout

DBG = [
    ("20 tabs", "React application becomes slow after opening 20 issue tabs.",
     ["Heap climbing; later tabs hitch.", "Issue bodies stay mounted (keep-alive unbounded).", "Query cache unbounded; listeners per editor.", "Detached ProseMirror/editor views.", "Cap keep-alive at 3–5; abort hidden queries; WeakMap caches."]),
    ("Fat context", "Toggling theme rerenders the whole board.",
     ["Profiler: all consumers of AppContext.", "value={{user, theme, tickets}} new object.", "Tickets update at 1Hz presence.", "Split providers / selector store.", "Theme in CSS vars so React may not need to rerender at all."]),
    ("Search lag", "Typing JQL feels sticky.",
     ["Input and 10k filter share a parent.", "Each keystroke setState at the board root.", "No debounce on the network; races.", "Colocate; debounce fetch; transition the list.", "Virtualize results."]),
    ("Plugin INP", "Issue page INP worse for customers with many apps.",
     ["RUM slice by plugin count.", "Sync init in the host.", "postMessage chatty; resize loops.", "Budget per slot; idle-init offscreen; isolate errors.", "Sandbox + cap."]),
    ("Memory leak", "Leave the board, memory does not fall.",
     ["Heap compare: Detached HTMLElement, listeners.", "setInterval in a feature without cleanup.", "WS still subscribed.", "Effect cleanup; abort; close WS.", "Why-did-you-retain."]),
    ("CLS banner", "A top banner makes the board jump.",
     ["CLS attribution: unexpected layout shift.", "Banner late from flags.", "Reserve min-height; boot flag before paint.", "Tokens for chrome height.", "Plugins cannot grow chrome unbounded."]),
    ("5MB", "Main JS 5MB parsed.",
     ["Coverage: admin+editor+moment in main.", "No route split.", "Icons imported as *.", "Analyze, split, per-icon import, lazy editor.", "Budget in CI."]),
    ("Hydration hitch", "SSR page freezes after HTML.",
     ["Long task during hydrate.", "Huge tree hydrate at once.", "Mismatch warnings.", "Stream; islands; reduce client JS on read view.", "CSR may be better for this surface."]),
    ("Upload jank", "Hashing a 2GB file freezes the tab.",
     ["Main-thread hash.", "Move to worker; chunk.", "Progress setState every byte.", "Throttle progress to rAF.", "IDB persist parts."]),
    ("WS storm", "Presence updates rerender the issue description.",
     ["setState at IssuePage on every heartbeat.", "Colocate presence stack.", "Throttle 1–2s.", "Don’t touch document store.", "Refs for cursors."]),
]


def debug_sim() -> str:
    cards = []
    for i, (title, symptom, clues) in enumerate(DBG, 1):
        clue_html = []
        for j, c in enumerate(clues):
            clue_html.append(f'<div class="clue reveal" data-clue id="dbg-{i}-c{j}"><b>Clue {j+1}.</b> {c}</div>')
        cards.append(f'''
<article class="topic" id="dbg-{i}" data-search="{title} debug" data-stype="Debug scenario">
  <div class="meta-row"><span class="badge badge-medium">Simulator</span></div>
  <h3>{i}. {title}</h3>
  <p><b>Symptom.</b> {symptom}</p>
  <p>Reason first (leaks, listeners, large DOM, unnecessary renders). Then reveal clues one at a time.</p>
  <p><button type="button" class="toggle-btn dbg-next">Reveal next clue</button></p>
  {''.join(clue_html)}
  <p><button type="button" class="toggle-btn" data-complete="reactTopics" data-cid="dbg-{i}">Mark complete</button></p>
</article>''')
    return f'''
<section class="block" id="debug-sim" data-search="Performance Debugging Simulator" data-stype="Section" data-cat="performance">
  <p class="kicker">10 scenarios</p>
  <h2 class="section-title">Performance Debugging Simulator</h2>
  <p class="lede">Read the symptom. Speak a hypothesis. Reveal clues progressively. Then write the fix as an ADR sentence.</p>
  {''.join(cards)}
</section>
'''


def mock() -> str:
    return r'''
<section class="block" id="mock" data-search="Mock Interview Mode" data-stype="Section">
  <p class="kicker">Timed practice</p>
  <h2 class="section-title">Mock Interview Mode</h2>
  <p class="lede">Draws a random practice item from system-design cards and interview questions (<code>data-mock</code>). Timer modes match senior loops. Save a debrief.</p>
  <div class="card" style="margin-bottom:16px">
    <p>Category
      <select id="mock-cat">
        <option value="all">All</option>
        <option value="react">React</option>
        <option value="architecture">Architecture / system design</option>
        <option value="performance">Performance</option>
        <option value="security">Security</option>
        <option value="browser">Browser</option>
      </select>
    </p>
    <div class="status-btns">
      <button type="button" class="toggle-btn" data-start-mock="15">15-min quick</button>
      <button type="button" class="toggle-btn" data-start-mock="30">30-min architecture</button>
      <button type="button" class="toggle-btn" data-start-mock="45">45-min system design</button>
      <button type="button" class="toggle-btn" data-start-mock="60">60-min full</button>
    </div>
    <div id="mock-panel"><p class="stat-sub">Pick a duration. Speak the 15-step framework. Reveal answers only after you have a plan.</p></div>
  </div>
  <div class="card">
    <h3>Debrief</h3>
    <label class="task"><input type="checkbox" id="mock-q-trade" /> <span>I named alternatives and trade-offs (not just a library)</span></label>
    <label class="task"><input type="checkbox" id="mock-q-time" /> <span>I hit the important paths within time</span></label>
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
<section class="block" id="progress" data-search="Progress Tracker Phase 2" data-stype="Section">
  <p class="kicker">localStorage atl-phase2-v1</p>
  <h2 class="section-title">Progress Tracker</h2>
  <div class="grid grid-2">
    <div class="card"><h3>Daily tasks</h3><p id="track-days">0</p></div>
    <div class="card"><h3>Architecture topics</h3><p id="track-arch">0</p><div class="bar"><span id="bar-cat-arch"></span></div></div>
    <div class="card"><h3>React topics</h3><p id="track-react">0</p><div class="bar"><span id="bar-cat-react"></span></div></div>
    <div class="card"><h3>Interview questions</h3><p id="track-qs">0</p></div>
    <div class="card"><h3>System designs</h3><p id="track-sd">0</p><div class="bar"><span id="bar-cat-sd"></span></div></div>
    <div class="card"><h3>Exercises</h3><p id="track-ex">0</p></div>
    <div class="card"><h3>Performance</h3><div class="bar"><span id="bar-cat-perf"></span></div></div>
    <div class="card"><h3>Browser</h3><div class="bar"><span id="bar-cat-browser"></span></div></div>
    <div class="card"><h3>Security</h3><div class="bar"><span id="bar-cat-sec"></span></div></div>
    <div class="card"><h3>Testing</h3><div class="bar"><span id="bar-cat-test"></span></div></div>
  </div>
  <p style="margin-top:18px"><button type="button" class="danger-btn" id="reset-progress">Reset all Phase 2 progress</button></p>
</section>
<section class="block" id="revision" data-search="Revision spaced repetition" data-stype="Section">
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
        ("Architecture", [
            ("r-large", "Design a large React application and name the packages"),
            ("r-bound", "Explain boundaries and how you enforce them"),
            ("r-own", "Explain state ownership with the decision tree"),
            ("r-dep", "Explain dependency direction with an example"),
            ("r-mod", "Defend modular monolith vs MFE"),
            ("r-adr", "Speak an ADR without saying only a library name"),
        ]),
        ("React", [
            ("r-ren", "Explain rendering as a calculation"),
            ("r-rec", "Explain reconciliation and keys with a board example"),
            ("r-fiber", "Explain Fiber conceptually (not source files)"),
            ("r-rc", "Explain render vs commit and what can be discarded"),
            ("r-upd", "Walk setState from update to effects"),
            ("r-keys", "Predict key A→B, index keys, remount"),
            ("r-fx", "Explain effects vs layout effects"),
            ("r-sus", "Explain Suspense conceptually"),
        ]),
        ("Performance", [
            ("r-unr", "Diagnose unnecessary renders with Profiler"),
            ("r-bun", "Diagnose a 5MB bundle"),
            ("r-virt", "Explain when and how to virtualize"),
            ("r-cwv", "Connect LCP/INP/CLS to code decisions"),
            ("r-crp", "Draw the critical rendering path"),
            ("r-inp", "Diagnose a slow click (INP)"),
        ]),
        ("System design", [
            ("r-board", "Design a Jira-like board in 45 minutes"),
            ("r-ac", "Design autocomplete with abort + a11y"),
            ("r-not", "Design notifications with degrade"),
            ("r-up", "Design a multi-GB uploader"),
            ("r-collab", "Discuss collaborative editing trade-offs honestly"),
            ("r-dash", "Design a 100-widget dashboard without N+1"),
        ]),
        ("Security", [
            ("r-xss", "Explain XSS in React (including HTML/plugins)"),
            ("r-csrf", "Explain CSRF vs CORS"),
            ("r-csp", "Explain CSP as depth"),
            ("r-tok", "Explain token storage (why not localStorage)"),
            ("r-sess", "Explain session vs JWT-in-SPA"),
        ]),
        ("Accessibility", [
            ("r-sem", "Prefer semantic HTML over ARIA"),
            ("r-kbd", "Keyboard: modal trap, roving tab"),
            ("r-focus", "Focus management restore"),
            ("r-aria", "When ARIA is required (combobox)"),
        ]),
        ("Testing", [
            ("r-unit", "What belongs in unit vs RTL"),
            ("r-int", "MSW / integration"),
            ("r-e2e", "Playwright money paths only"),
            ("r-strat", "Say the pyramid and what you skip"),
        ]),
        ("Senior behavior", [
            ("r-trade", "Explain trade-offs and rejected options"),
            ("r-chal", "Challenge requirements (realtime? plugins?)"),
            ("r-dec", "Make a decision under uncertainty"),
            ("r-alt", "Name two alternatives you did not pick"),
            ("r-scale", "Discuss people-scale (CI, ownership) not only QPS"),
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
<section class="block" id="readiness" data-search="Phase 2 Readiness Checklist" data-stype="Section">
  <p class="kicker">Gate</p>
  <h2 class="section-title">Final Phase 2 Readiness Checklist</h2>
  <p class="lede">Check only if you can do it <i>today</i> without this file. Stay until ~85%.</p>
  <p class="stat">Score: <span id="ready-score">0%</span></p>
  <div class="bar"><span id="bar-ready-final"></span></div>
  <p id="ready-gate" class="stat-sub"></p>
  {''.join(html)}
</section>
'''


def resources() -> str:
    rows = [
        ("React docs — Learn", "https://react.dev/learn", "Official mental model: rendering, effects, hooks.", "Source of truth for APIs. This file teaches interview judgment.", "React", False),
        ("React docs — Reference", "https://react.dev/reference/react", "useTransition, useDeferredValue, useSyncExternalStore.", "Look up exact signatures after you have the model.", "React internals", True),
        ("React blog (concurrent / 18)", "https://react.dev/blog", "Shipping notes on concurrent features and versions.", "Optional historical context.", "Internals", True),
        ("MDN Web Docs", "https://developer.mozilla.org/", "HTML, HTTP, a11y APIs, Fetch, SW.", "Canonical platform reference.", "Browser / a11y / network", False),
        ("web.dev performance", "https://web.dev/explore/performance", "INP, LCP, CLS, optimize guides.", "Pairs with Web Performance section.", "Vitals", True),
        ("web.dev INP", "https://web.dev/articles/inp", "Interaction to Next Paint.", "The metric for laggy React.", "Performance", False),
        ("Chrome Developers — rendering", "https://developer.chrome.com/docs/devtools/evaluate-performance", "Performance panel.", "How you actually debug.", "Perf debugging", False),
        ("WCAG 2.2", "https://www.w3.org/WAI/WCAG22/quickref/", "Official criteria.", "Don’t memorize numbers; know POUR + patterns.", "Accessibility", False),
        ("WAI-ARIA APG", "https://www.w3.org/WAI/ARIA/apg/", "Combobox, dialog, grid patterns.", "When you must use ARIA.", "A11y", False),
        ("OWASP Cheat Sheet Series", "https://cheatsheetseries.owasp.org/", "XSS, CSRF, session.", "Defensive checklists. Optional depth.", "Security", True),
        ("MDN CSP", "https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP", "CSP reference.", "After the Security table.", "Security", True),
        ("TanStack Query docs", "https://tanstack.com/query/latest/docs/framework/react/overview", "Keyed cache, staleTime, invalidation.", "One implementation of the fetching architecture.", "Server state", True),
        ("SWR docs", "https://swr.vercel.app/", "SWR mental model.", "Optional alternative library.", "Server state", True),
        ("Redux Toolkit", "https://redux-toolkit.js.org/", "Official Redux today.", "Only if you chose a store. Not required.", "State", True),
        ("Zustand", "https://docs.pmnd.rs/zustand/getting-started/introduction", "Tiny store.", "Optional.", "State", True),
        ("Playwright", "https://playwright.dev/docs/intro", "E2E.", "Money-path tests.", "Testing", True),
        ("Testing Library", "https://testing-library.com/docs/react-testing-library/intro/", "RTL.", "User-centric tests.", "Testing", False),
        ("Atlassian Engineering blog", "https://www.atlassian.com/blog/atlassian-engineering", "How they write about scale and frontend.", "Culture, not a question dump.", "Company", True),
        ("Atlassian Design System", "https://atlassian.design/", "Tokens, components, a11y.", "Taste for Phase 2+ UI conversations. Optional to memorize.", "DS", True),
        ("Atlassian careers", "https://www.atlassian.com/company/careers", "Role descriptions.", "Confirm the loop with your recruiter.", "Positioning", False),
        ("web.dev security", "https://web.dev/explore/secure", "Web security basics.", "Optional beside OWASP.", "Security", True),
        ("HTML spec event loop", "https://html.spec.whatwg.org/multipage/webappapis.html#event-loop-processing-model", "Host event loop.", "Phase 1 carry-over. Optional.", "Browser", True),
        ("MDN HTTP caching", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching", "Cache-Control, validators.", "With Networking section.", "Network", False),
        ("web.dev images", "https://web.dev/learn/images", "Responsive images, LCP.", "Optional.", "LCP", True),
        ("React Testing Library queries", "https://testing-library.com/docs/queries/about/", "By role/label.", "Don’t getByClassName.", "Testing", True),
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
  <p><b>Phase 2 topic.</b> {topic}</p>
</article>''')
    return f'''
<section class="block" id="resources" data-search="Resource Library React MDN web.dev" data-stype="Section">
  <p class="kicker">Official first</p>
  <h2 class="section-title">Resource Library</h2>
  <p class="lede">This HTML already contains the teaching. Links are for signatures, specs, and company flavor. Labeled Optional when you do not need them to finish Phase 2.</p>
  <div class="grid grid-2">{''.join(cards)}</div>
</section>
'''
