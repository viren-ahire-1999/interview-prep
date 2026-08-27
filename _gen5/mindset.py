from util import topic, diagram, callout, code


def mindset() -> str:
    t1 = topic("ms-what", "Frontend system design is product ownership on the client",
               "what is frontend system design", "Theory", f'''
  <p>Backend system design asks: how do we store, replicate, and serve data at scale. Frontend system design asks: how do humans use a surface that is <b>slow, hostile, and interruptible</b> — a browser tab, a network that lies, a DOM that is expensive, and a team that will ship plugins into your page.</p>
  <p>The unit of design is not “a React app.” It is a <b>critical path</b>: the first useful pixel, the first interaction that must feel instant, and the failure the user will actually see. If you cannot name those three, you are decorating a box diagram.</p>
  <p>What you own in 45–60 minutes:</p>
  <ul>
    <li><b>Users and jobs.</b> Who, on which device, doing what how often.</li>
    <li><b>The surface.</b> Routes, chrome, overlays, empty and error states.</li>
    <li><b>The contract.</b> APIs, cache keys, events, authz. Not Kubernetes.</li>
    <li><b>The runtime budget.</b> JS kb, DOM nodes, long tasks, LCP element, INP on the money click.</li>
    <li><b>Degrade paths.</b> Poll if WS dies. Read-only if save conflicts. Hide the plugin if it throws.</li>
  </ul>
  {callout("<b>Senior tell.</b> You name two options you rejected and why. “We’ll use GraphQL + Redis + Kafka” with no client architecture is a fail at this level.")}
  {diagram("""Interviewer prompt
    → users + job + device
    → critical path (first paint, first interaction, first failure)
    → rendering + shell + routes
    → state map (URL / server cache / local / ephemeral)
    → API + cache + races
    → perf + a11y + security + observe
    → trade-offs + what you would measure next week""")}
  <p>Related files on this hub: Phase 2 (React runtime, folders, Profiler). Phase 3 (distributed systems — use it when the prompt becomes “fan-out notifications to 10M devices,” not when the prompt is “design the bell icon”).</p>
  ''', "topics")

    t2 = topic("ms-not", "What you will not do in a frontend interview",
               "frontend vs backend interview scope", "Theory", f'''
  <p>Do not start with a region × AZ × Kafka picture. If they wanted that, they said “design the notification platform.” If they said “design the notification inbox,” they want unread badges, pagination, mark-read, deep links, a11y live regions, and what happens when the socket drops.</p>
  <p>Do not invent a company. Do not claim you shipped a specific Atlassian feature unless it is on your resume. Use “Jira-like” and “Confluence-like” as <b>shape</b>, and label practice questions as practice.</p>
  <ul>
    <li>Skip inventing 12 microservices. One BFF + existing APIs is a valid senior start.</li>
    <li>Skip picking Redux vs Zustand in minute two. Place the state first.</li>
    <li>Skip “we’ll virtualize everything.” Virtualize the list you measured as large.</li>
    <li>Skip CRDT unless they insist on multi-caret editing. Say the honest alternative (lock, version, last-write + diff).</li>
  </ul>
  {code("TypeScript", '''// Interview-sized scope for "design Google Docs"
// You own: read vs edit split, draft persistence, versioned PUT, conflict UX.
// You do not own: a production OT/CRDT implementation on the whiteboard.
type PageSave = {
  pageId: string;
  baseVersion: number; // If-Match
  body: unknown;
  clientMutationId: string; // idempotent retry
};''')}
  ''', "topics")

    return f'''
<section class="block" id="mindset" data-search="What frontend system design is" data-stype="Section">
  <p class="kicker">Orientation</p>
  <h2 class="section-title">What this course is</h2>
  <p class="lede">A frontend system-design expert can take an underspecified product prompt and, in under an hour, produce a defendable client architecture — including what they will not build.</p>
  {t1}{t2}
</section>
'''


def framework() -> str:
    steps = [
        ("1. Restate the product", "One sentence. Users, surface, success. Confirm you heard them."),
        ("2. Clarifying questions", "Realtime? Mobile? SEO? Plugins? How many items on screen? Offline? Auth model? Timebox."),
        ("3. Functional requirements", "Must-have vs later. Write them. Cut if time is 30 minutes."),
        ("4. Non-functional", "LCP/INP targets, a11y (keyboard + SR), security (XSS/authz), availability of the money path."),
        ("5. Assumptions and scale", "Say numbers: 400 cards visible, 10k in filter, 50 collaborators, 200KB HTML, 3 tabs."),
        ("6. High-level architecture", "Shell, routes, feature modules, BFF, push channel. Boxes a PM could follow."),
        ("7. Components and ownership", "Who owns board snapshot vs issue vs drag overlay. Package names if useful."),
        ("8. Data flow", "Load → render → interact → mutate → reconcile. Draw arrows, not only boxes."),
        ("9. API sketch", "3–7 endpoints or queries. Errors, pagination, idempotency. Not 40 fields."),
        ("10. State map", "URL / server cache / local / ephemeral. If it is shareable, it is probably URL."),
        ("11. Caching and races", "Keys, invalidation, abort, generation tokens, optimistic rollback."),
        ("12. Performance", "What is virtualized, split, deferred, workered. Name the LCP element."),
        ("13. Failures", "409, timeout, WS drop, quota, plugin crash. What the user sees."),
        ("14. Security + a11y", "Unprompted. Encode HTML, server authz, CSP, combobox/grid/focus."),
        ("15. Observability", "2–4 metrics you would watch in week one. Correlation id."),
        ("16. Trade-offs and close", "Two rejected options. What you would build in v1 vs v2. Ask if they want depth."),
    ]
    rows = "".join(f"<tr><td>{s[0]}</td><td>{s[1]}</td></tr>" for s in steps)
    t = topic("fw-16", "The 16-step loop you speak out loud",
              "frontend system design interview framework", "Theory", f'''
  <p>Memorize this until it is boring. In a 45-minute loop: steps 1–5 in ~8 minutes, 6–12 in ~25, 13–16 in ~10, leave 2 minutes for their follow-up. In 30 minutes, collapse 7–8 into the architecture box and still do 13–16. Interviewers hire the person who reaches failure and a11y, not the person who names 14 libraries.</p>
  <table>
    <tr><th>Step</th><th>What you say</th></tr>
    {rows}
  </table>
  {callout("<b>30-minute cut.</b> One rendering choice, one state map, three APIs, one performance bet, one failure, one a11y pattern, one rejected option. Do not start a component inventory.")}
  <p><b>Opening script (practice, not a canned bio).</b> “I’ll confirm users and the money path, write NFRs, assume scale numbers you can correct, then design the client: shell, data, and the interaction that must stay fast. I’ll call out what I would not build in v1.”</p>
  {diagram("""45 min
  0–8   clarify + FR/NFR + numbers
  8–20  shell / routes / modules
  20–33 API + state + cache + races
  33–43 perf + fail + a11y + security + metrics
  43–45 rejected options + questions for them""")}
  ''', "topics")

    t2 = topic("fw-questions", "Clarifying questions that change the design",
               "clarifying questions frontend design", "Theory", f'''
  <p>Ask questions whose answers <b>fork the architecture</b>. “What’s the company’s QPS?” rarely forks a board UI. These do:</p>
  <ul>
    <li>Is the first visit SEO-critical, or is this behind login?</li>
    <li>Do we need character-level multiplayer editing, or is last-write + versions enough?</li>
    <li>Are third-party apps in-process JS or sandboxed iframes?</li>
    <li>Mobile: same app or a reduced surface?</li>
    <li>How many entities are on screen in the p95 case? (Not “how many users exist.”)</li>
    <li>Must unread badges be &lt;1s fresh, or is 30s polling acceptable?</li>
    <li>Offline: drafts only, or full mutation queue?</li>
  </ul>
  <p>If they say “you decide,” pick the <b>stricter interesting constraint</b> and say so. Example: “I’ll assume logged-in, 400 visible cards, polling is OK, plugins are iframes, no CRDT.” Write it. They will correct you if they care.</p>
  ''', "topics")

    return f'''
<section class="block" id="framework" data-search="16 step frontend interview framework" data-stype="Section">
  <p class="kicker">How to run the hour</p>
  <h2 class="section-title">Interview framework</h2>
  <p class="lede">This is the spine of every case and every mock. If you freeze, return to the next unused step.</p>
  {t}{t2}
</section>
'''


def requirements() -> str:
    t1 = topic("rq-nfr", "Frontend NFRs are user-visible budgets",
               "frontend non functional requirements scale", "Theory", f'''
  <p>Backend NFRs are often latency, throughput, durability. Frontend NFRs are those plus <b>main-thread time, memory per tab, and human time</b>.</p>
  <table>
    <tr><th>NFR</th><th>Say a number</th><th>What it forces</th></tr>
    <tr><td>LCP</td><td>p75 &lt; 2.5s on mid mobile / mid desktop you name</td><td>LCP element, SSR/edge, image priority, less JS before paint</td></tr>
    <tr><td>INP</td><td>p75 &lt; 200ms on the money interaction</td><td>Colocate state, virtualize, transition the list, no sync plugin init</td></tr>
    <tr><td>CLS</td><td>Reserve chrome, banners, images</td><td>Flag-boot before paint; aspect-ratio; no late webfont swap on hero</td></tr>
    <tr><td>Memory</td><td>Cap keep-alive tabs (3–5)</td><td>Destroy editors; abort hidden queries</td></tr>
    <tr><td>A11y</td><td>Keyboard complete for the money path</td><td>Semantics, focus, APG pattern</td></tr>
    <tr><td>Security</td><td>No trusted HTML from users/plugins</td><td>Encode, sanitize, CSP, sandbox</td></tr>
    <tr><td>Authz</td><td>UI hide ≠ allow</td><td>Server denies; client only pretties 403</td></tr>
  </table>
  {callout("<b>Scale that matters.</b> “10M MAU” does not tell you whether to virtualize. “p95 board has 8k issues in filter and 400 DOM cards” does.")}
  ''', "topics")

    t2 = topic("rq-est", "Capacity estimation for a client",
               "frontend capacity estimation DOM payload", "Theory", f'''
  <p>Do the napkin math they expect, but on the <b>client</b>:</p>
  <ul>
    <li><b>DOM.</b> 400 cards × 30 nodes ≈ 12k nodes — usually fine. 8k cards × 30 nodes ≈ 240k nodes — virtualize or you will jank.</li>
    <li><b>JSON.</b> 10k issues × 2KB = 20MB parse. Don’t fetch the universe. Fields on the card vs fields on the overlay.</li>
    <li><b>JS.</b> 200KB gz main is a different product than 2MB gz. Editor and admin must not ride with the board.</li>
    <li><b>Connections.</b> One WS per tab × 10 tabs × 50k users is a backend problem — mention it, then return to the inbox UI.</li>
    <li><b>Collaborators.</b> 50 presence dots is a list. 500 caret streams on one document is a different product.</li>
  </ul>
  {code("TypeScript", '''// Say this out loud, then let them correct the numbers
const boardGuess = {
  visibleCards: 400,
  filterHits: 10_000,
  bytesPerCardSummary: 800,
  firstFetchBytes: 400 * 800, // ~320KB — acceptable
  fullFilterBytes: 10_000 * 800, // ~8MB — do not
};''')}
  <p>Always label guesses as guesses. The interviewer is testing whether you <b>think in constraints</b>, not whether 800 bytes is exact.</p>
  ''', "topics")

    return f'''
<section class="block" id="requirements" data-search="Requirements NFRs frontend scale estimation" data-stype="Section" data-cat="architecture">
  <p class="kicker">Before boxes</p>
  <h2 class="section-title">Requirements and scale</h2>
  <p class="lede">Write NFRs that change code. Invent client-scale numbers. Invite correction.</p>
  {t1}{t2}
</section>
'''
