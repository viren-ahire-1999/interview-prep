from util import topic, diagram, callout, code


def realtime() -> str:
    t1 = topic("rt-modes", "Poll, SSE, WebSocket, push — pick the freshness",
               "websocket SSE polling notifications presence", "Theory", f'''
  <p>Realtime is a <b>freshness SLA</b>, not a technology preference.</p>
  <table>
    <tr><th>Channel</th><th>Good for</th><th>Cost</th></tr>
    <tr><td>Poll 15–60s</td><td>Badges, dashboards, “good enough”</td><td>Simple, cacheable, easy to degrade to</td></tr>
    <tr><td>SSE</td><td>Server→client streams, one way</td><td>Auto-reconnect in EventSource; proxies</td></tr>
    <tr><td>WebSocket</td><td>Bidirectional, presence, collab</td><td>Sticky conns, backpressure, reconnect protocol</td></tr>
    <tr><td>Push (SW)</td><td>Background / mobile</td><td>Permission UX, not a replacement for in-app inbox</td></tr>
  </table>
  {diagram("""Need <1s and bidirectional? → WS + reconnect + seq numbers
Need server push, client silent? → SSE
Need “eventually”? → poll
Need closed tab? → push + inbox REST still required""")}
  <p>Always keep a <b>REST inbox</b> (or equivalent) as source of truth. The socket is a hint. Duplicate events by id. After reconnect, fetch “since cursor” or a snapshot — do not assume the socket was lossless.</p>
  {callout("<b>Presence vs document.</b> Heartbeats must not setState on the issue body. Colocate presence. Throttle. A caret is ephemeral; a comment is not.")}
  {code("TypeScript", '''type InboxEvent = { id: string; type: string; createdAt: string; payload: unknown };
function applyEvent(cache: Map<string, InboxEvent>, e: InboxEvent) {
  if (cache.has(e.id)) return; // at-least-once
  cache.set(e.id, e);
}''')}
  ''', "topics")

    t2 = topic("rt-degrade", "Degrade is the design",
               "websocket reconnect degrade poll", "Theory", f'''
  <p>Write the sentence: “If the socket dies, the bell still opens, we poll every 30s, and we show ‘Live updates paused.’” That sentence is more senior than a box labeled Kafka.</p>
  <p>Backpressure: if presence arrives at 20Hz, you sample to 1–2Hz for React. The canvas layer (if any) can take higher frequency in a ref.</p>
  ''', "topics")

    return f'''
<section class="block" id="realtime" data-search="Realtime WebSocket SSE polling presence" data-stype="Section" data-cat="architecture">
  <p class="kicker">Freshness</p>
  <h2 class="section-title">Realtime</h2>
  <p class="lede">Choose a freshness SLA. Keep a REST source of truth. Degrade in public.</p>
  {t1}{t2}
</section>
'''


def performance() -> str:
    t1 = topic("pf-vitals", "Vitals are architecture, not a Lighthouse trophy",
               "LCP INP CLS critical rendering path virtualization", "Theory", f'''
  <p>The critical rendering path is still: bytes → parse HTML → CSSOM → render tree → layout → paint → composite. Your JS can steal the main thread at any point after it downloads.</p>
  <table>
    <tr><th>Vital</th><th>Typical FE cause</th><th>Typical fix</th></tr>
    <tr><td>LCP</td><td>Late hero image, blocked HTML, huge JS before content</td><td>Priority image, SSR/edge HTML, less main JS</td></tr>
    <tr><td>INP</td><td>Handler does too much, huge rerender, layout thrash</td><td>Colocate, transition list, virtualize, yield, worker</td></tr>
    <tr><td>CLS</td><td>Late banner, no image size, webfont swap</td><td>Reserve space, boot flags early, font-display strategy</td></tr>
  </table>
  <p><b>Virtualize</b> when the p95 list is large <i>and</i> you measured it. Virtualization costs: scroll jump, measure, a11y (you must still provide a keyboard model and not lie about the document length). Paginate when the user thinks in pages. Window when they think in a board.</p>
  {diagram("""INP click
  → event delay (main thread busy)
  → processing (your handler + React render)
  → present delay (paint)
Fix the longest of the three. Profiler + Performance panel. Not guess + memo.""")}
  {code("TypeScript", '''// Transition the expensive list; keep the input urgent
const [q, setQ] = useState("");
const [deferredQ, setDeferredQ] = useState("");
function onChange(v: string) {
  setQ(v);
  startTransition(() => setDeferredQ(v));
}''')}
  ''', "topics")

    t2 = topic("pf-budget", "Budgets, long tasks, and workers",
               "performance budget long task web worker", "Theory", f'''
  <p>A budget is a CI number: JS kb for the board route, LCP on a lab profile, INP on a RUM slice. Without it the bundle only grows.</p>
  <p>Long tasks (&gt;50ms) are how INP dies. Break work: idle callbacks, scheduling, workers for hash/encode/parse of large files. Do not <code>setState</code> every byte of an upload; rAF-throttle progress.</p>
  {callout("memo / useCallback are last. First: less work, smaller trees, smaller props, no fat context, virtualize the giant list. Phase 2 on this hub drills the React details — here you decide <i>where</i> the work is allowed to live.")}
  ''', "topics")

    return f'''
<section class="block" id="performance" data-search="Performance LCP INP CLS virtualization budget" data-stype="Section" data-cat="performance">
  <p class="kicker">Budgets</p>
  <h2 class="section-title">Performance architecture</h2>
  <p class="lede">Name the LCP element and the money interaction. Then pick virtualize / split / worker.</p>
  {t1}{t2}
</section>
'''


def offline() -> str:
    t1 = topic("off-queue", "Drafts, queues, and not lying",
               "offline sync service worker conflict idempotency", "Theory", f'''
  <p>Offline is a product: which mutations are allowed with no network? Almost always <b>drafts</b> (comments, doc body). Rarely “move 400 issues and reconcile later” unless you have a real sync engine.</p>
  <ul>
    <li>Persist drafts in IndexedDB, not only memory.</li>
    <li>Queue mutations with idempotency keys. Show “waiting to send.”</li>
    <li>On conflict: show both, or last-write with a toast and a link to history — do not silently clobber.</li>
    <li>Service workers: cache the shell and immutable assets. Do not cache personalized HTML as if it were public.</li>
  </ul>
  {diagram("""online  → optimistic + confirm
offline → IDB draft / queue + banner
reconnect → flush queue in order → 409 → conflict UI
two tabs → BroadcastChannel or lock so you do not double-send""")}
  {code("TypeScript", '''type QueuedMutation = {
  id: string; // clientMutationId
  url: string;
  body: unknown;
  createdAt: number;
};''')}
  ''', "topics")

    return f'''
<section class="block" id="offline" data-search="Offline sync drafts service worker" data-stype="Section" data-cat="architecture">
  <p class="kicker">Resilience</p>
  <h2 class="section-title">Offline and sync</h2>
  <p class="lede">Decide what works offline. Persist it. Conflict in the open.</p>
  {t1}
</section>
'''


def design_systems() -> str:
    t1 = topic("ds-api", "A design system is an API with versioning",
               "design system tokens theming contribution", "Theory", f'''
  <p>Tokens (color, space, type, elevation) are the contract. Components compose tokens. Features must not invent hex. Theming is token swaps, not <code>if (dark)</code> in 400 files.</p>
  <p>Component APIs: variants and slots beat 40 boolean props. Accessibility lives in the kit (focus rings, dialog, combobox) so product teams do not reimplement APG badly.</p>
  <p>Contribution: RFC + visual review + a11y review + versioning. Breaking a Button padding is a semver event. A junk drawer of “just this once” variants is how the system dies.</p>
  {callout("Atlassian Design System (atlassian.design) is a public example of tokens and components — use it as taste, not as a script of interview answers.")}
  {code("TypeScript", '''type ButtonProps = {
  appearance: "default" | "primary" | "subtle" | "danger";
  isDisabled?: boolean;
  type?: "button" | "submit";
  children: React.ReactNode;
};
// Not: isBig isHero isNav isCompact2 isCompact3''')}
  ''', "topics")

    return f'''
<section class="block" id="ds" data-search="Design systems tokens theming" data-stype="Section" data-cat="architecture">
  <p class="kicker">Multi-team UI</p>
  <h2 class="section-title">Design systems</h2>
  <p class="lede">Tokens, tight APIs, a11y in the kit, versioning. Not a folder of pretty buttons.</p>
  {t1}
</section>
'''


def collab() -> str:
    t1 = topic("co-models", "Locks, versions, OT, CRDT — honesty first",
               "OT CRDT collaborative editing conflict", "Theory", f'''
  <p>Collaborative editing is a spectrum. Most work software is not Figma.</p>
  <table>
    <tr><th>Model</th><th>UX</th><th>When</th></tr>
    <tr><td>Last write + toast</td><td>Someone overwrote you</td><td>Low contention settings</td></tr>
    <tr><td>Version / If-Match</td><td>409 + reload or diff</td><td>Pages, tickets, most Confluence-like</td></tr>
    <tr><td>Soft lock</td><td>“Aisha is editing”</td><td>You can tolerate waiting</td></tr>
    <tr><td>OT / CRDT</td><td>Simultaneous carets</td><td>True multiplayer docs/canvas — a product, not a 15-minute box</td></tr>
  </table>
  <p>In an interview, own <b>read vs edit split</b>, draft persistence, versioned save, conflict UI, and presence as a separate channel. If they push CRDT, say: “I would not invent one on the whiteboard. I would use a known engine and spend the hour on the client integration: awareness, undo, offline, and permissions.” That is senior, not evasion.</p>
  {diagram("""read view  → static/SSR HTML, no editor JS
click Edit → lazy editor + draft in IDB
save       → PUT If-Match: version
409        → show theirs vs yours
presence   → other channel, throttled, not in the document store""")}
  ''', "topics")

    return f'''
<section class="block" id="collab" data-search="Collaboration OT CRDT locks versions" data-stype="Section" data-cat="architecture">
  <p class="kicker">Multiplayer</p>
  <h2 class="section-title">Collaboration</h2>
  <p class="lede">Most products need versions and a conflict UX, not a CRDT lecture.</p>
  {t1}
</section>
'''
