from util import topic, callout, code, esc

RESUME_FOLLOWUPS = [
    "How did you measure this — metric, tool, and baseline period?",
    "What was slow or broken before you started?",
    "What exactly did you change (code, architecture, process)?",
    "How did you establish the baseline?",
    "What alternatives did you consider and reject?",
    "What trade-off did you accept (complexity, staleness, cost, time)?",
    "What was your role vs the team's — what did you personally own?",
    "What was the scale (users, teams, QPS, data size, regions)?",
    "How did you validate the improvement held over time?",
    "What would you do differently with hindsight?",
]

INTERROGATION_QS = [
    ("Product", "Who was the user and what pain did this project remove?"),
    ("Product", "What would have happened if you had not shipped this?"),
    ("Product", "How did you decide scope — what did you cut and why?"),
    ("Architecture", "Draw the main components and data flow in one minute."),
    ("Architecture", "Where are the boundaries between frontend, API, and async workers?"),
    ("Architecture", "What is the source of truth vs derived/cached data?"),
    ("Implementation", "What was the hardest bug or edge case you hit?"),
    ("Implementation", "Walk through one critical code path as if pair-programming."),
    ("Implementation", "What would break first if someone changed X without telling you?"),
    ("Scale", "How many users, requests, or records did this handle at peak?"),
    ("Scale", "What happens at 10× load — what degrades first?"),
    ("Scale", "Where would sharding or partitioning enter if growth continued?"),
    ("Performance", "How did you profile or measure before optimizing?"),
    ("Performance", "What was the bottleneck and how did you prove it?"),
    ("Performance", "What did you deliberately not optimize?"),
    ("Security", "How is authn/authz enforced — server vs UI only?"),
    ("Security", "What sensitive data exists and how is it protected?"),
    ("Testing", "What did you test automatically vs manually vs in staging?"),
    ("Testing", "What failure mode did you add a test for after an incident?"),
    ("Observability", "How would you know this feature failed in production tonight?"),
    ("Observability", "What metrics or logs would you alert on?"),
    ("Trade-offs", "Name one decision you would reverse and why."),
    ("Trade-offs", "What did you choose not to build and how did stakeholders react?"),
    ("Failures", "Tell me about something that went wrong during this project."),
    ("Failures", "How did you communicate a miss or rollback?"),
    ("Leadership", "Who disagreed with you and how did you resolve it?"),
    ("Leadership", "How did you unblocked others or changed the team's bar?"),
]

CODING_PROBLEMS = [
    {
        "id": "code-1",
        "title": "Concurrent meeting peak",
        "search": "meeting intervals overlap concurrent peak calendar",
        "stmt": "Given an array of meetings `[start, end)` as half-open integer minutes, return the maximum number of meetings happening at the same time. Meetings touching at an endpoint do not overlap (e.g. [0,5) and [5,10) → peak 1).",
        "clarify": "Are inputs sorted? Can end ≤ start? Empty input? Integer overflow on count?",
        "hints": "Sort by start time. Sweep line: +1 at start, −1 at end. Track running max.",
        "solution": """function maxConcurrent(meetings: [number, number][]): number {
  if (meetings.length === 0) return 0;
  const events: [number, number][] = [];
  for (const [s, e] of meetings) {
    if (e <= s) continue;
    events.push([s, 1], [e, -1]);
  }
  events.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  let cur = 0, best = 0;
  for (const [, d] of events) {
    cur += d;
    if (cur > best) best = cur;
  }
  return best;
}""",
        "complexity": "O(n log n) time for sort, O(n) space for events.",
        "edges": "Empty; single meeting; all nested; all disjoint; duplicate intervals; end equals start.",
        "comms": "State half-open convention. Mention brute force pairwise O(n²). Offer sweep after sort.",
    },
    {
        "id": "code-2",
        "title": "Versioned config merge",
        "search": "config merge layers precedence override",
        "stmt": "You receive config layers as objects (string → unknown). Later layers override earlier keys. If a value is the sentinel `{ \"__delete__\": true }`, remove that key from the merged result (even if a prior layer set it). Return the merged flat object.",
        "clarify": "Deep merge or flat only? Nested objects? Key types? Mutate inputs?",
        "hints": "Single pass over layers in order. Track current map. Deletes remove keys outright.",
        "solution": """const DELETE = { __delete__: true } as const;

function isDelete(v: unknown): v is typeof DELETE {
  return !!v && typeof v === "object" && (v as any).__delete__ === true;
}

function mergeConfigs(layers: Record<string, unknown>[]): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const layer of layers) {
    for (const [k, v] of Object.entries(layer)) {
      if (isDelete(v)) delete out[k];
      else out[k] = v;
    }
  }
  return out;
}""",
        "complexity": "O(total keys across layers) time and space.",
        "edges": "No layers; delete never set; delete then re-set in later layer; empty strings as keys.",
        "comms": "Clarify flat vs deep merge early. Mention production uses schema validation after merge.",
    },
    {
        "id": "code-3",
        "title": "Sliding window request counts",
        "search": "sliding window rate limit per user timestamp",
        "stmt": "Implement `RateWindow` with `record(userId, tsMs)` and `count(userId, nowMs, windowMs)` returning how many events from that user fall in `(nowMs - windowMs, nowMs]`. Assume timestamps are non-decreasing within a single user's calls.",
        "clarify": "Per-user isolation? Memory bound? Thread-safe? Exact vs approximate?",
        "hints": "Deque of timestamps per user. Drop from front while ts ≤ now − window.",
        "solution": """class RateWindow {
  private buckets = new Map<string, number[]>();

  record(userId: string, tsMs: number): void {
    const q = this.buckets.get(userId) ?? [];
    q.push(tsMs);
    this.buckets.set(userId, q);
  }

  count(userId: string, nowMs: number, windowMs: number): number {
    const q = this.buckets.get(userId);
    if (!q) return 0;
    const cutoff = nowMs - windowMs;
    while (q.length && q[0] <= cutoff) q.shift();
    return q.length;
  }
}""",
        "complexity": "Amortized O(1) per record; count may evict stale in O(k). Space O(events retained).",
        "edges": "WindowMs = 0; first event; burst at boundary; unknown user returns 0.",
        "comms": "Compare fixed window vs sliding. Mention Redis ZSET for distributed version.",
    },
    {
        "id": "code-4",
        "title": "Comment thread flatten with depth",
        "search": "tree flatten nested comments depth preorder",
        "stmt": "Given nested comments `{ id, body, replies[] }`, return a flat array of `{ id, body, depth }` in pre-order (parent before children). `depth` starts at 0 for roots.",
        "clarify": "Max depth? Cycle detection? Stable order among siblings? Empty replies?",
        "hints": "DFS. Pass depth+1 to children. Iterative stack if recursion depth is a concern.",
        "solution": """type Comment = { id: string; body: string; replies?: Comment[] };
type Flat = { id: string; body: string; depth: number };

function flattenComments(roots: Comment[]): Flat[] {
  const out: Flat[] = [];
  const walk = (nodes: Comment[], depth: number) => {
    for (const n of nodes) {
      out.push({ id: n.id, body: n.body, depth });
      if (n.replies?.length) walk(n.replies, depth + 1);
    }
  };
  walk(roots, 0);
  return out;
}""",
        "complexity": "O(n) time and output space for n nodes.",
        "edges": "Empty forest; single node; very deep thread; missing replies field.",
        "comms": "Offer iterative version if stack overflow is mentioned. Discuss pagination for UI.",
    },
    {
        "id": "code-5",
        "title": "Top K movers in a stream",
        "search": "top k frequency stream heap hashmap",
        "stmt": "Process a stream of `(userId, delta)` score updates. After each update, be ready to return the top K userIds by total score (ties broken by lexicographic userId ascending). Implement `update(userId, delta)` and `topK()`.",
        "clarify": "Can scores go negative? K vs number of users? Return fewer if < K users?",
        "hints": "HashMap totals. For topK, sort entries O(u log u) or min-heap of size K when K ≪ u.",
        "solution": """class TopKMovers {
  private scores = new Map<string, number>();

  update(userId: string, delta: number): void {
    this.scores.set(userId, (this.scores.get(userId) ?? 0) + delta);
  }

  topK(k: number): string[] {
    return [...this.scores.entries()]
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, k)
      .map(([id]) => id);
  }
}""",
        "complexity": "Update O(1). topK sort O(u log u); heap variant O(u log k).",
        "edges": "K = 0; negative deltas; tie on score; update same user many times.",
        "comms": "Ask if topK is hot path. Mention heap + lazy deletion for production leaderboard.",
    },
    {
        "id": "code-6",
        "title": "Path normalization checker",
        "search": "file path normalize dot dot segments",
        "stmt": "Given a Unix-style path string (segments separated by `/`, may include `.` and `..`), return the normalized absolute path starting with `/`, or `\"\"` if the path escapes above root (more `..` than prior segments allow). No trailing slash except root `/`.",
        "clarify": "Windows paths? Multiple slashes? Empty string? Relative vs absolute input?",
        "hints": "Split on `/`, filter empty and `.`, stack push/pop on `..`.",
        "solution": """function normalizePath(path: string): string {
  const stack: string[] = [];
  for (const part of path.split("/")) {
    if (!part || part === ".") continue;
    if (part === "..") {
      if (stack.length === 0) return "";
      stack.pop();
    } else stack.push(part);
  }
  return "/" + stack.join("/");
}""",
        "complexity": "O(n) time and space for n characters.",
        "edges": "Already normalized; only dots; deep nesting; root path `/`.",
        "comms": "Relate to browser/router path handling. Mention symlink semantics out of scope.",
    },
    {
        "id": "code-7",
        "title": "Bijection pattern match",
        "search": "pattern match bijection word pattern isomorphic",
        "stmt": "Given a pattern of uppercase letters `A-Z` and a space-separated sentence, return whether each letter maps bijectively to exactly one word (same length as pattern). Same letter → same word; different letters → different words.",
        "clarify": "Case sensitivity? Extra spaces? Pattern length must match word count?",
        "hints": "Two maps: char→word and word→char. On conflict return false.",
        "solution": """function matchesPattern(pattern: string, sentence: string): boolean {
  const words = sentence.trim().split(/\\s+/);
  if (words.length !== pattern.length) return false;
  const c2w = new Map<string, string>();
  const w2c = new Map<string, string>();
  for (let i = 0; i < pattern.length; i++) {
    const c = pattern[i], w = words[i];
    const prevW = c2w.get(c);
    const prevC = w2c.get(w);
    if (prevW !== undefined && prevW !== w) return false;
    if (prevC !== undefined && prevC !== c) return false;
    c2w.set(c, w);
    w2c.set(w, c);
  }
  return true;
}""",
        "complexity": "O(L + W) time; O(unique letters + words) space.",
        "edges": "Length mismatch; repeated words with different letters; single char pattern.",
        "comms": "Connect to permission key aliasing or URL slug bijection in product code.",
    },
    {
        "id": "code-8",
        "title": "Task cooldown scheduler",
        "search": "task scheduler cooldown idle intervals",
        "stmt": "You have tasks labeled `A-Z` in an array `tasks` and a cooldown `n` (minimum idle slots between two identical tasks). One slot executes one task or idle. Return the minimum number of slots to finish all tasks.",
        "clarify": "Only one CPU? Tasks all length 1? What if n = 0?",
        "hints": "Count frequencies. Greedily place most frequent with gaps. Formula: max(len, (maxFreq-1)*(n+1)+countMax).",
        "solution": """function leastInterval(tasks: string[], n: number): number {
  const freq = new Map<string, number>();
  for (const t of tasks) freq.set(t, (freq.get(t) ?? 0) + 1);
  let maxF = 0, maxCount = 0;
  for (const f of freq.values()) {
    if (f > maxF) { maxF = f; maxCount = 1; }
    else if (f === maxF) maxCount++;
  }
  const part = (maxF - 1) * (n + 1) + maxCount;
  return Math.max(tasks.length, part);
}""",
        "complexity": "O(t) to count, O(1) extra for 26 letters.",
        "edges": "Single task type; n larger than task count; all unique tasks.",
        "comms": "Walk small example on whiteboard. Mention heap simulation if they want explicit schedule.",
    },
]

CRAFT_QS = [
    ("React", "Why might this component render 200 times after one parent state update?",
     "Reconciliation scope, context, unstable props, list without memo where it matters.",
     "Name render vs commit; find whether child is in the same subtree; check new object/function props each render; check context provider value identity.",
     "1–5: vague blame of React. 6–8: names a mechanism. 9–10: systematic Profiler plan + structural fix."),
    ("React", "What happens when setState is called inside useEffect without proper deps?",
     "Effect lifecycle, stale closures, infinite loops, Strict Mode double invoke.",
     "Effect runs after paint; missing deps → stale values; wrong deps → loop; functional updates when deriving from prev state.",
     "1–5: 'it re-renders.' 6–8: deps + stale closure. 9–10: draws timeline + fix (deps, ref, event handler extraction)."),
    ("TypeScript", "When is `any` acceptable in a senior codebase — and when is it a failure?",
     "Type safety at boundaries, gradual migration, code gen.",
     "Accept at untyped JS boundary with immediate narrowing; reject in domain models. Prefer unknown + guards.",
     "1–5: 'never' or 'whenever.' 6–8: boundary vs core. 9–10: example guard + lint rule + team policy."),
    ("JavaScript", "Explain microtasks vs macrotasks and where Promise.then sits.",
     "Event loop ordering, starvation, React 18 batching context.",
     "Microtasks drain fully before next macrotask; setTimeout(0) after Promise; rAF between tasks; long microtask chain blocks input.",
     "1–5: 'async is async.' 6–8: correct ordering with example. 9–10: INP impact + fix (chunk, defer)."),
    ("Performance", "A search box feels laggy — first 15 minutes of debugging?",
     "INP, long tasks, network races, re-render storms.",
     "Reproduce; Performance panel long tasks; React Profiler on keystroke; check debounce vs controlled input cost; abort stale fetches.",
     "1–5: 'add debounce' only. 6–8: measure first. 9–10: ordered checklist with metric targets."),
    ("Browser", "Why can LCP look good while INP is terrible on the same page?",
     "Different metrics, main-thread contention, hydration.",
     "LCP is one paint; INP is interaction latency. Heavy JS after load, large hydration, sync handlers hurt INP only.",
     "1–5: conflates metrics. 6–8: defines both. 9–10: concrete Jira-board-style example + fix."),
    ("State", "How would you design state for a Jira issue page (detail + comments + sidebar)?",
     "Local vs URL vs server cache vs UI ephemeral.",
     "URL: selected tab/filters; server cache: issue+comments with keys; local: draft comment; avoid one mega context.",
     "1–5: 'Redux for everything.' 6–8: split by lifetime. 9–10: invalidation + optimistic comment + permission source."),
    ("Architecture", "When would you refuse to add GraphQL to a React app?",
     "Complexity, caching, authz, team boundaries.",
     "BFF already fits; few clients; heavy caching needs; auth on server simpler with REST; operational cost of schema federation.",
     "1–5: technology preference. 6–8: constraints first. 9–10: ADR-style decision with revert plan."),
    ("Architecture", "How do micro-frontends change your frontend error and observability story?",
     "Blast radius, shared vendors, routing, independent deploys.",
     "Separate bundles → separate error boundaries and release tags; need correlation id across MFEs; shared design system version skew.",
     "1–5: 'they scale teams.' 6–8: ops downsides. 9–10: concrete observability contract between shells."),
    ("Testing", "What should you not test with React Testing Library on a modal form?",
     "Implementation details vs user outcomes; E2E for real browser focus.",
     "Skip testing internal state hooks; skip snapshotting entire tree; do test label+submit+error messages; E2E for focus trap across browsers.",
     "1–5: 'test everything.' 6–8: user-centric list. 9–10: pyramid placement + what to defer to Playwright."),
    ("Testing", "How do you test a data-fetching hook with race conditions?",
     "Abort, act, fake timers, MSW.",
     "MSW delayed responses; assert only latest request wins; test abort on unmount; use findBy for async UI.",
     "1–5: 'mock fetch once.' 6–8: stale response case. 9–10: full test list including error + retry."),
    ("a11y", "What breaks if you only manage focus inside a modal but ignore aria-modal on the backdrop page?",
     "Screen reader virtual cursor, inert, focus escape.",
     "Background still navigable for SR users; need aria-modal + ideally inert on root; restore focus on close.",
     "1–5: 'tab trap is enough.' 6–8: SR issue named. 9–10: checklist: role, label, focus, inert, escape."),
    ("a11y", "How do live regions relate to optimistic UI updates?",
     "aria-live politeness, duplicate announcements, toast vs polite.",
     "Polite for non-critical success; assertive sparingly; avoid announcing every keystroke; tie to user-visible outcome.",
     "1–5: never heard of live regions. 6–8: polite vs assertive. 9–10: example comment posted + error rollback announcement."),
    ("React", "Explain why index keys on a sortable list cause subtle bugs.",
     "Fiber identity, state attached to wrong row.",
     "Reorder remaps state to wrong item; inputs swap values; fix with stable ids from server.",
     "1–5: 'keys are for performance.' 6–8: identity explanation. 9–10: demo scenario + migration plan."),
    ("Performance", "Virtualization fixes scrolling — what new problems does it introduce?",
     "a11y, dynamic height, selection, scroll restoration.",
     "aria-rowcount; scrollToIndex; measured height cache; shift+click selection across non-mounted rows; URL scroll restore.",
     "1–5: 'virtualize always.' 6–8: two downsides. 9–10: board column design with overscan + a11y."),
    ("JavaScript", "How do closures cause memory leaks in SPAs — and how do you prove one?",
     "Detached DOM, listeners, caches, DevTools heap snapshot.",
     "Listener on window referencing component state; global Map holding DOM nodes; prove with heap snapshot + retainer path.",
     "1–5: 'JS is garbage collected so no leaks.' 6–8: one pattern. 9–10: debug steps with Chrome Memory tab."),
]

SD_PROMPTS = [
    ("Jira-like issue board",
     "Design a kanban board for 500 issues per project, drag-and-drop, filters, real-time updates for collaborators on the same board.",
     ["Requirements & NFRs", "API contracts", "Data model", "Real-time fan-out", "Optimistic UI + conflicts", "Caching", "Permissions", "Observability", "Trade-offs", "Communication"]),
    ("Collaborative document editor",
     "Design a Confluence-like page editor with 20 simultaneous editors, comments, version history, and offline draft sync.",
     ["Consistency model", "Storage & diff", "Presence", "Conflict resolution", "Search indexing lag", "Security", "Scale", "Failure modes", "Trade-offs", "Communication"]),
    ("Multi-channel notification system",
     "Design notifications for issue assigned, mentioned, and watched — email, in-app, mobile push — with user preferences and deduplication.",
     ["Event ingestion", "Fan-out", "Idempotency", "Rate limits", "Template + i18n", "Delivery guarantees", "Observability", "Privacy", "Trade-offs", "Communication"]),
    ("Analytics dashboard",
     "Design a dashboard showing team velocity, cycle time, and SLA breaches — data refreshed within 5 minutes for 10k teams.",
     ["Ingestion vs query", "Warehouse vs stream", "Multi-tenant isolation", "Freshness vs cost", "Chart API", "Caching", "Security", "Scale", "Trade-offs", "Communication"]),
    ("Multi-GB file uploader",
     "Design resumable attachment upload from browser and mobile, virus scan, and attachment linked to an issue.",
     ["Multipart upload", "Pre-signed URLs", "Progress + resume", "Metadata store", "Async scan pipeline", "CDN", "Failure recovery", "Security", "Trade-offs", "Communication"]),
    ("Real-time chat for a workspace",
     "Design Slack-like channels and DMs for a 50k-person org — history search, presence, and mobile push.",
     ["Message store", "Fan-out read paths", "Ordering", "Presence", "Search index", "Push pipeline", "Moderation", "Scale", "Trade-offs", "Communication"]),
    ("Issue search",
     "Design full-text search over issues with filters (project, assignee, JQL-like syntax), permissions enforced, p95 < 300ms.",
     ["Index design", "Authz filter", "Query parser", "Consistency with OLTP", "Ranking", "Caching", "Failure degradation", "Observability", "Trade-offs", "Communication"]),
    ("Distributed rate limiter",
     "Design a rate limiter for public REST APIs — 1000 req/min per API key, fair across regions, minimal false positives.",
     ["Algorithm choice", "Storage", "Clock skew", "Burst handling", "Fail open/closed", "Observability", "Hot keys", "Testing", "Trade-offs", "Communication"]),
]

LOOP_ROUNDS = [
    ("Round 1 — Coding", "45 min · data structures + clean code", "coding"),
    ("Round 2 — Frontend craft", "45 min · React/TS/perf/architecture depth", "craft"),
    ("Round 3 — System design", "60 min · scalable architecture + trade-offs", "sd"),
    ("Round 4 — Hiring manager / behavioral", "45–60 min · stories + scope + collaboration", "hm"),
    ("Round 5 — Values", "45 min · alignment with published values + STAR", "values"),
]

LOOP_DIMS = [
    "problem solving", "technical depth", "architecture", "frontend", "system design",
    "communication", "leadership", "customer", "values", "confidence", "clarity",
]


def _problem_card(p: dict) -> str:
    return f'''
<article class="problem" id="{p["id"]}" data-mock-code data-search="{esc(p["search"])}" data-stype="Coding mock">
  <h3>{p["title"]}</h3>
  <p>{p["stmt"]}</p>
  <p><b>Clarify first.</b> {p["clarify"]}</p>
  <button type="button" class="toggle-btn reveal-btn" data-reveal="{p["id"]}-hints">Reveal hints</button>
  <div class="reveal" id="{p["id"]}-hints"><p class="clue">{p["hints"]}</p></div>
  <button type="button" class="toggle-btn reveal-btn" data-reveal="{p["id"]}-sol">Reveal solution</button>
  <div class="reveal" id="{p["id"]}-sol">
    {code("TypeScript", p["solution"])}
    <p><b>Complexity.</b> {p["complexity"]}</p>
    <p><b>Edge cases.</b> {p["edges"]}</p>
  </div>
  <p><b>Communication checklist.</b> {p["comms"]}</p>
</article>'''


def resume() -> str:
    slots = []
    for i in range(5):
        qs = "".join(f"<li>{q}</li>" for q in RESUME_FOLLOWUPS)
        slots.append(f'''
<article class="card story-card" data-rb="{i}" data-search="resume bullet deep dive" data-stype="Resume slot">
  <h3>Bullet slot {i + 1}</h3>
  <div class="field"><label>Paste resume bullet</label><textarea data-rf="bullet" placeholder="e.g. Improved checkout latency by 35% by…"></textarea></div>
  <p><b>Interrogation prompts (generic — apply to any bullet).</b></p>
  <ul class="tight">{qs}</ul>
  <p><b>Likely next questions (stay generic until you fill the bullet).</b></p>
  <ul class="tight">
    <li>Walk me through the architecture diagram you would draw for this.</li>
    <li>What broke in production related to this work?</li>
    <li>Who was unhappy with your approach and why?</li>
    <li>If we asked your teammate, what would they say you owned?</li>
  </ul>
  <div class="field"><label>Your prep notes (saved locally)</label><textarea data-rf="notes" placeholder="Answers to the prompts above — facts only."></textarea></div>
</article>''')
    follow_list = "".join(f"<li>{q}</li>" for q in RESUME_FOLLOWUPS[:6])
    return f'''
<section class="block" id="resume" data-search="Resume deep dive bullets interrogation" data-stype="Section">
  <p class="kicker">Every line will be probed</p>
  <h2 class="section-title">Resume Deep Dive</h2>
  <p class="lede">Paste up to five bullets. For each, answer the generic follow-ups before the interview — not the night before. Metrics you cannot defend become a values problem. Autosaves per slot.</p>
  {callout("Teaching list: interviewers compress resume bullets into the same probes — measurement, baseline, alternatives, trade-offs, your role, scale, validation.")}
  <ul class="tight">{follow_list}</ul>
  {''.join(slots)}
</section>
'''


def interrogation() -> str:
    items = []
    for i, (cat, q) in enumerate(INTERROGATION_QS):
        items.append(f'<li class="reveal" data-iq="{i}" data-cat="{esc(cat)}"><span class="badge badge-pattern">{cat}</span> {q}</li>')
    return f'''
<section class="block" id="interrogation" data-search="Project interrogation mock deep dive" data-stype="Section">
  <p class="kicker">One question at a time</p>
  <h2 class="section-title">Project Interrogation Mode</h2>
  <p class="lede">Enter a real project. Questions reveal progressively — answer out loud before scrolling. Categories: Product, Architecture, Implementation, Scale, Performance, Security, Testing, Observability, Trade-offs, Failures, Leadership.</p>
  <div class="card">
    <div class="grid grid-2">
      <div class="field"><label>Project name</label><input id="iq-project" data-iqf="project" placeholder="Internal codename is fine" /></div>
      <div class="field"><label>Technologies</label><input id="iq-tech" data-iqf="tech" placeholder="React, Node, Postgres, Kafka…" /></div>
    </div>
    <div class="field"><label>Resume bullet or one-line summary</label><textarea id="iq-bullet" data-iqf="bullet"></textarea></div>
    <p><button type="button" class="toggle-btn" id="start-interrogation">Start interrogation</button></p>
  </div>
  <div id="interrogation-panel" class="hidden">
    <div class="q-step card">
      <p class="stat-sub">Question <span id="iq-num">0</span> / {len(INTERROGATION_QS)}</p>
      <ol id="interrogation-qs" class="tight">{''.join(items)}</ol>
      <p><button type="button" class="toggle-btn" id="iq-next">Next question</button></p>
    </div>
    <div class="card">
      <div class="field"><label>Answer notes</label><textarea id="iq-notes" data-iqf="notes"></textarea></div>
      <div class="grid grid-2">
        <div class="field"><label>Self-score (1–5)</label>
          <select id="iq-score" data-iqf="score">
            <option value="1">1 — blank</option>
            <option value="2">2 — vague</option>
            <option value="3" selected>3 — ok</option>
            <option value="4">4 — strong</option>
            <option value="5">5 — teach it</option>
          </select>
        </div>
        <div class="field"><label>Confidence</label>
          <select id="iq-confidence" data-iqf="confidence">
            <option value="low">Low</option>
            <option value="medium" selected>Medium</option>
            <option value="high">High</option>
          </select>
        </div>
      </div>
      <p><button type="button" class="toggle-btn" id="save-interrogation">Save session</button></p>
      <div id="iq-history" class="stat-sub"></div>
    </div>
  </div>
</section>
'''


def coding() -> str:
    cards = "".join(_problem_card(p) for p in CODING_PROBLEMS)
    return f'''
<section class="block" id="coding" data-search="Coding mock interview timer practice" data-stype="Section">
  <p class="kicker">Speak while you code</p>
  <h2 class="section-title">Coding Mock Interview</h2>
  <p class="lede">Eight original practice problems (not copied LeetCode statements). Pick a timer, draw a problem, clarify, then reveal hints/solution only after you have a plan. Use the Tech Checklist during the session.</p>
  <div class="card" style="margin-bottom:16px">
    <p><b>Timer</b></p>
    <div class="status-btns">
      <button type="button" data-start-code="30">30 min</button>
      <button type="button" data-start-code="45">45 min</button>
      <button type="button" data-start-code="60">60 min</button>
      <button type="button" class="toggle-btn" id="code-stop">Stop</button>
    </div>
    <p class="timer" id="code-timer">—</p>
    <div id="code-panel"><p class="stat-sub">Start a timer, then pick a problem below. Narrate the 10-step communication framework from the Communication section.</p></div>
  </div>
  {cards}
</section>
'''


def craft() -> str:
    cards = []
    for i, (cat, q, testing, strong, rubric) in enumerate(CRAFT_QS, 1):
        cards.append(f'''
<article class="q" id="craft-{i}" data-mock-craft data-search="{esc(q)}" data-stype="Craft mock">
  <div class="meta-row"><span class="badge badge-pattern">{cat}</span></div>
  <h3>{q}</h3>
  <button type="button" class="toggle-btn reveal-btn" data-reveal="craft-{i}-r">Reveal rubric</button>
  <div class="reveal" id="craft-{i}-r">
    <p><b>What they are testing.</b> {testing}</p>
    <p><b>Strong answer points.</b> {strong}</p>
    <p><b>Rubric.</b> {rubric}</p>
  </div>
</article>''')
    return f'''
<section class="block" id="craft" data-search="Frontend craft mock React TypeScript performance" data-stype="Section">
  <p class="kicker">Depth, not trivia</p>
  <h2 class="section-title">Frontend Craft Mock</h2>
  <p class="lede">Sixteen practice questions across React, TypeScript, JavaScript, performance, browser, state, architecture, testing, and a11y. Answer out loud, then reveal the rubric. Pair with Phase 2 content — this section tests interview delivery.</p>
  {''.join(cards)}
</section>
'''


def sdmock() -> str:
    cards = []
    for i, (title, prompt, dims) in enumerate(SD_PROMPTS, 1):
        dim_li = "".join(f"<li>{d}</li>" for d in dims)
        cards.append(f'''
<article class="problem" id="sdmock-{i}" data-mock-sd data-search="{esc(title)} system design mock" data-stype="SD mock">
  <h3>{title}</h3>
  <p class="lede">{prompt}</p>
  <p><b>Rubric dimensions — score yourself after a 45–60 min whiteboard.</b></p>
  <ul class="tight">{dim_li}</ul>
  <div class="field"><label>Session notes</label><textarea data-sdf="notes-{i}" placeholder="FR/NFR, numbers you used, what you forgot…"></textarea></div>
  <div class="grid grid-2">
    <div class="field"><label>Self-score (1–5)</label><select data-sdf="score-{i}"><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select></div>
    <div class="field"><label>Confidence</label><select data-sdf="conf-{i}"><option>Low</option><option selected>Medium</option><option>High</option></select></div>
  </div>
</article>''')
    return f'''
<section class="block" id="sdmock" data-search="System design mock interview simulation" data-stype="Section">
  <p class="kicker">45–60 minutes each</p>
  <h2 class="section-title">System Design Mock</h2>
  <p class="lede">Eight prompts aligned with collaboration software — not generic URL shorteners. Use Phase 3 frameworks. Timebox, then debrief against the rubric dimensions.</p>
  {''.join(cards)}
</section>
'''


def loop() -> str:
    rounds = "".join(
        f'<div class="loop-round" data-round="{kind}"><b>{title}</b><br /><span class="stat-sub">{sub}</span></div>'
        for title, sub, kind in LOOP_ROUNDS
    )
    score_rows = []
    for d in LOOP_DIMS:
        sid = d.replace(" ", "-")
        score_rows.append(f'''
<div class="field"><label>{d.title()}</label>
  <select data-loop-score="{sid}">
    <option value="1">1</option><option value="2">2</option>
    <option value="3" selected>3</option><option value="4">4</option><option value="5">5</option>
  </select>
</div>''')
    return f'''
<section class="block" id="loop" data-search="Full mock interview loop scorecard" data-stype="Section">
  <p class="kicker">Simulate the day</p>
  <h2 class="section-title">Full Mock Interview Loop</h2>
  <p class="lede">Five rounds in order: coding → craft → system design → HM/behavioral → values. Take breaks between rounds as you would on interview day. Save the scorecard — patterns in weak dimensions beat one strong round.</p>
  <div class="card">
    <p><button type="button" class="toggle-btn" id="start-loop">Start Full Interview Loop</button></p>
    <div id="loop-panel" class="hidden">
      {rounds}
      <div class="card" style="margin-top:16px">
        <h3>Scorecard</h3>
        <div class="grid grid-2">{''.join(score_rows)}</div>
        <div class="field"><label>Strengths</label><textarea id="loop-strengths" data-loopf="strengths"></textarea></div>
        <div class="field"><label>Weaknesses / next revision</label><textarea id="loop-weaknesses" data-loopf="weaknesses"></textarea></div>
        <p><button type="button" class="toggle-btn" id="save-loop">Save loop debrief</button></p>
        <div id="loop-history" class="stat-sub"></div>
      </div>
    </div>
  </div>
  {callout("HM/behavioral round: pull from Story Bank — do not invent. Values round: behavior first, value name only if they use it.")}
</section>
'''
