from util import code, topic, diagram, callout


def state() -> str:
    return f'''
<section class="block" id="state" data-search="State Management decision tree Context Redux Zustand" data-stype="Section" data-cat="architecture">
  <p class="kicker">Ownership</p>
  <h2 class="section-title">State Management</h2>
  <p class="lede">The senior question is never “Redux or Context?” It is “what is the lifetime, the writer, the reader set, and the sync source of truth?”</p>
  {topic("st-tree", "What state belongs where", "state decision tree URL local context server", "State", f'''
  {diagram('''Is it on the server / shared with others?
  YES → server-state cache (query layer). UI mirrors it.
  NO  → Is it shareable / bookmarkable?
          YES → URL (search params, path)
          NO  → Is it needed by distant, unrelated subtrees?
                YES → app store or split context (slow-changing)
                NO  → lift to nearest common parent, else local useState''')}
  <table>
    <tr><th>Example</th><th>Home</th><th>Why / failure mode</th></tr>
    <tr><td>Modal open/close</td><td>Local</td><td>Global modal store becomes a junk drawer</td></tr>
    <tr><td>Issue search JQL / filters</td><td>URL</td><td>Share, back button, analytics. Local-only filters cannot be reproduced</td></tr>
    <tr><td>Authenticated user</td><td>App/session (rarely Context)</td><td>Slow-changing; do not mix with high-churn board data</td></tr>
    <tr><td>Fetched Jira issues</td><td>Server cache</td><td>Redux-duplicating server data without invalidation = stale bugs</td></tr>
    <tr><td>Theme</td><td>Context or tiny store</td><td>OK in context if split from user/tickets</td></tr>
    <tr><td>Draft comment</td><td>Local + persist (localStorage/IDB)</td><td>Not Redux unless many screens edit the same draft</td></tr>
    <tr><td>Selected issue on a board</td><td>URL</td><td><code>/board?selected=ISSUE-12</code></td></tr>
    <tr><td>Optimistic column position</td><td>Cache overlay</td><td>Rollback on 409</td></tr>
  </table>
  <p><b>Context problems:</b> any <code>value={{}}</code> new object, or a fat value, re-renders every consumer. Split providers. Or use a store with selectors (Zustand/Redux).</p>
  <p><b>Redux problems:</b> everything in one store, including form keystrokes and server lists. Boilerplate without Toolkit. Use it when many writers, time-travel/debug, or complex transitions need a single event log.</p>
  <p><b>Zustand:</b> less ceremony, still easy to create an implicit global god-store. Same ownership rules apply.</p>
  <p><b>External stores / useSyncExternalStore:</b> right for non-React sources (browser history, a module singleton). Must snapshot immutably to avoid tearing.</p>
  {callout("Redux is not automatically better than Context. Context is not automatically simpler than a 30-line Zustand store. Server state is not automatically global state.")}
  ''', "topics")}
</section>
'''


def fetching() -> str:
    return f'''
<section class="block" id="fetching" data-search="Server State Data Fetching cache invalidation" data-stype="Section" data-cat="architecture">
  <p class="kicker">Server state</p>
  <h2 class="section-title">Server State / Data Fetching</h2>
  <p class="lede">Libraries (TanStack Query, SWR, Relay, Apollo) are adapters over one architecture: a keyed cache, a stale policy, and a way to invalidate. Learn the architecture; the library is an implementation.</p>
  {topic("fetch-arch", "Request lifecycle and cache", "caching invalidation optimistic pagination race", "Data fetching", f'''
  <p><b>Lifecycle:</b> idle → fetching → success | error. Retries with backoff on idempotent GETs. Mutations need an explicit policy (retry POST is dangerous without idempotency keys).</p>
  <p><b>Cache key</b> is the identity of a query: <code>["issue", id]</code>, <code>["search", jql, page]</code>. If two screens use the same key, they share data. That is a feature (dedupe) and a bug (accidental coupling) — design keys like APIs.</p>
  <ul class="tight">
    <li><b>Stale vs fresh:</b> stale-while-revalidate shows last data and refetches. Fresh means do not hit network. <code>staleTime</code> is a product decision (issue detail: 30s; presence: 0).</li>
    <li><b>Invalidation:</b> after transitionIssue, invalidate <code>["issue", id]</code> and <code>["board", boardId]</code>. Over-invalidation thrashes; under-invalidation lies to users.</li>
    <li><b>Optimistic updates:</b> write cache immediately, rollback on failure. Only when the happy path is obvious and conflict is rare — or you show a merge UI.</li>
    <li><b>Pagination / infinite:</b> page params in the key, or an infinite query that concatenates pages. Don’t put 10k issues in one GET.</li>
    <li><b>Prefetch:</b> on hover/route intent. Cheap for issue titles; expensive for full editor payload.</li>
    <li><b>Dedup:</b> in-flight map: same key, one network call. All waiters share the promise.</li>
    <li><b>Cancellation / races:</b> AbortController on unmount or key change. Also a generation token: ignore responses older than the latest requested JQL. Both, not one.</li>
  </ul>
  {code("TypeScript", '''let gen = 0;
async function search(jql: string, ac: AbortSignal) {
  const my = ++gen;
  const res = await issuesApi.search(jql, { signal: ac });
  if (my !== gen) return; // stale generation
  setRows(res);
}''')}
  <p>GraphQL clients add a normalized cache (entities by id). Great for overlapping issue objects; costly to reason about (gc, stale fields). REST + a document cache is simpler until overlap hurts.</p>
  {callout("Do not couple the interview to one library. Say: “I’d use a keyed server cache with SWR, explicit mutation invalidation, and abort+generation to prevent races.\"")}
  <h4>Library concepts without marrying a vendor</h4>
  <table>
    <tr><th>Idea</th><th>TanStack Query / SWR-ish</th><th>GraphQL client-ish</th></tr>
    <tr><td>Identity</td><td>Array key <code>["issue", id]</code></td><td>Normalized entity <code>Issue:id</code></td></tr>
    <tr><td>Freshness</td><td>staleTime / dedupingInterval</td><td>Cache policies per field</td></tr>
    <tr><td>Write</td><td>invalidate / setQueryData</td><td>updater / refetch queries</td></tr>
    <tr><td>Cost</td><td>Simpler reasoning, more refetch</td><td>Less overfetch, harder GC/staleness</td></tr>
  </table>
  <p><b>Optimistic update recipe:</b> snapshot → write cache → mutate → on success keep / on error rollback + toast. Only when the happy path is obvious. Irreversible transitions (delete space) should not be optimistic.</p>
  <p><b>Pagination vs infinite:</b> page params in the URL if shareable (“page 3 of search”). Infinite for feeds where the cursor is not a product object. Don’t mix both on the same surface without a story for “open this item later.”</p>
  ''', "topics")}
</section>
'''


def performance() -> str:
    return f'''
<section class="block" id="performance" data-search="React Performance memo useMemo virtualization" data-stype="Section" data-cat="performance">
  <p class="kicker">Judgment</p>
  <h2 class="section-title">React Performance</h2>
  <p class="lede">useMemo everywhere is not a strategy. It is a tax. Profile, then apply the cheapest structural fix (colocate state, split context, virtualize, split the bundle).</p>
  {topic("perf-model", "Render cost vs commit cost vs JS cost", "unnecessary renders memoization virtualization", "Performance", f'''
  <p>A render is JS. A commit is DOM + layout. Users feel <b>INP</b> (handler + render + paint) and <b>LCP</b> (bytes + main thread). Optimizing the wrong one is common.</p>
  <p><b>Unnecessary renders</b> happen when a parent re-renders and children are not isolated, or context value identity changes. They are free if the subtree is tiny; they are death if 8,000 rows run function bodies.</p>
  <p><b>memo / useMemo / useCallback:</b> they skip work when deps are referentially equal. They <i>add</i> work to compare deps and allocate the hook. They fail when you pass inline objects/functions from an un-memoized parent. They hide bugs when you put the wrong deps.</p>
  {code("TypeScript", '''// BEFORE: one context, everything rerenders on any ticket change
const AppCtx = React.createContext(null);
function App() {
  const [user, setUser] = useState(u);
  const [tickets, setTickets] = useState([]);
  const [theme, setTheme] = useState("dark");
  return (
    <AppCtx.Provider value={{ user, tickets, theme, setUser, setTickets, setTheme }}>
      <Shell />
    </AppCtx.Provider>
  );
}
// AFTER: split by change rate + selector store for tickets
<ThemeProvider value={theme}>
  <UserProvider value={user}>
    <TicketStoreProvider>  {/* zustand / query */}
      <Shell />
    </TicketStoreProvider>
  </UserProvider>
</ThemeProvider>''')}
  <ul class="tight">
    <li><b>Colocate state</b> so a keystroke in a filter does not re-render the board.</li>
    <li><b>Derive</b> instead of storing (filtered list from query + URL).</li>
    <li><b>Selectors</b> subscribe to a slice, not the whole store.</li>
    <li><b>Virtualize</b> any list that can exceed ~100 complex rows (board, search, dashboards).</li>
    <li><b>Lazy / code-split</b> editors, admin, charts. Prefetch on intent.</li>
    <li><b>Images:</b> right size, modern format, priority on LCP image only.</li>
    <li><b>Workers:</b> JQL parse, markdown, huge JSON transform — not React render itself.</li>
  </ul>
  {callout("When useCallback makes things worse: you wrap every handler, deps are wrong or change every render anyway, and you have added noise without a memoized child. Measure first.", "warn")}
  ''', "reactTopics")}
  {topic("perf-anti", "Memoization is not a strategy — before / after", "useMemo useCallback anti-patterns virtualization", "Performance", f'''
  <p><b>Why “useMemo everywhere” fails.</b> Each hook is extra comparison work and extra deps to get wrong. It does not fix a fat context, a 20k-row DOM, or a 5MB parse. Seniors change <i>structure</i> first: colocate, split, virtualize, split the bundle. Memo is a scalpel after a profile.</p>
  <table>
    <tr><th>Symptom</th><th>Wrong first move</th><th>Right first move</th></tr>
    <tr><td>Typing lags</td><td>memo every row</td><td>Colocate input; transition the list; debounce the network</td></tr>
    <tr><td>Theme toggle janks</td><td>memo the app</td><td>Split context or CSS variables</td></tr>
    <tr><td>Scroll janks on a table</td><td>useCallback on cells</td><td>Virtualize; cheap cells; don’t measure per row</td></tr>
    <tr><td>Slow load</td><td>micro-optimize renders</td><td>Code-split; shrink JS; preload LCP</td></tr>
  </table>
  {code("TypeScript", '''// BEFORE: 20k IssueRow mounts. memo changes nothing about DOM size.
{rows.map((r) => <IssueRow key={r.id} row={r} onOpen={() => open(r.id)} />)}

// AFTER: windowed list + stable handler + cheap row
const onOpen = useCallback((id: string) => open(id), [open]);
<VirtualList
  count={rows.length}
  rowHeight={36}
  renderRow={(i) => <IssueRow row={rows[i]} onOpen={onOpen} />}
/>''')}
  <p><b>When memo <i>does</i> earn its keep:</b> a heavy child (editor, chart, board column) whose props are stable, sitting under a chatty parent you cannot colocate yet. Prove it with the Profiler: commit duration drops, and the child does not light up.</p>
  <p><b>Derived state.</b> Do not store <code>filtered</code> in state if it is <code>rows.filter</code> of query + URL. Stored derived state goes stale. Compute it (memoize only if the Profiler says the filter is expensive).</p>
  <p><b>Workers.</b> Move CPU (markdown parse, huge JSON, search index) off the main thread. Do not try to “React-render in a worker.” The DOM and React stay on the main thread; you ship results back.</p>
  {callout("Senior sentence: “I would record the interaction, fix the structural cost, then memoize the one child the profile still flags. I would not sprinkle useMemo as a house style.\"")}
  ''', "reactTopics")}
</section>
'''


def perf_debug() -> str:
    scenarios = [
        ("table", "A React table with 20,000 rows is slow",
         "Scroll jank, INP &gt; 200ms, fans spin.",
         "Full render of 20k rows; no virtualization; expensive cells; inline objects; layout thrash on resize.",
         "React Profiler: commit duration on scroll. Performance panel: long tasks. Why did this render?",
         "Virtualize (window + overscan). Memo cells. Don’t measure layout per row. Paginate if the product allows. Trade-off: jump-to-row and a11y need extra work (aria-rowcount, tab stops)."),
        ("search", "Typing in a search box causes lag",
         "Each keystroke feels sticky.",
         "Each change filters 20k in the same component as the input; no debounce; no transition; context updates the world.",
         "Profiler on keydown. See if the input’s parent is the board root.",
         "Colocate input state. Debounce the query (not the input paint). useTransition for the list. Web worker if the filter is heavy. Trade-off: debounce vs feeling of live search."),
        ("context", "Entire app re-renders when a small context value changes",
         "Profiler shows all consumers on a theme toggle or a single ticket patch.",
         "Fat context; new object each render; tickets in the same provider as theme.",
         "Highlight updates in React DevTools. Search who consumes the context.",
         "Split providers. Selector store. Trade-off: more provider nesting vs a store library."),
        ("bundle", "Initial JS is 5 MB",
         "Poor TTI/LCP on mid-range laptops. Atlassian-like plugin bundles.",
         "One main chunk; moment.js; unused icons; admin+editor in the critical path; source maps in prod (rare); no tree-shake.",
         "Coverage in DevTools. webpack-bundle-analyzer / source-map-explorer. Network waterfalls.",
         "Route and widget split. Drop moment. Icon imports per-icon. Plugin code async. Trade-off: more round trips vs H2/H3 multiplexing."),
        ("tti", "Page takes 4 seconds to become interactive",
         "Users click, nothing happens. LCP maybe OK if a hero image is fast.",
         "Long hydration; sync third-party; huge JS; main-thread CSS; font block; waterfall of API then render.",
         "Lighthouse, Performance, RUM INP/TTI-ish metrics. Server TTFB vs client JS.",
         "SSR/stream critical HTML if it helps LCP; defer non-critical JS; break long tasks; prefetch data in parallel with JS. Trade-off: SSR complexity vs CSR + skeleton."),
        ("tabs", "Slow after opening 20 issue tabs (SPA)",
         "Memory climbs; later tabs hitch.",
         "Caches unbounded; listeners per tab not removed; detached editors; hidden trees still mounted.",
         "Memory heap snapshots. Performance monitor.",
         "Keep-alive with a cap; virtualize tab bodies; abort queries; WeakMaps. Trade-off: instant tab switch vs memory."),
    ]
    cards = []
    for sid, title, sym, causes, method, fix in scenarios:
        cards.append(f'''
<article class="topic" id="pd-{sid}" data-search="{title}" data-stype="Perf scenario" data-cat="performance">
  <h3>{title}</h3>
  <p><b>1. Symptoms.</b> {sym}</p>
  <p><b>2. Possible causes.</b> {causes}</p>
  <p><b>3–6. Debugging.</b> {method} Use React DevTools Profiler + browser Performance + Network. Record a 3s interaction, not a 30s guess.</p>
  <p><b>7–8. Fixes and trade-offs.</b> {fix}</p>
  <p><button type="button" class="toggle-btn" data-complete="reactTopics" data-cid="pd-{sid}">Mark complete</button></p>
</article>''')
    return f'''
<section class="block" id="perf-debug" data-search="Performance Debugging scenarios" data-stype="Section" data-cat="performance">
  <p class="kicker">Production</p>
  <h2 class="section-title">Performance Debugging</h2>
  <p class="lede">Practice the first click in DevTools. Seniors do not start with useMemo; they start with a recording.</p>
  {''.join(cards)}
</section>
'''
