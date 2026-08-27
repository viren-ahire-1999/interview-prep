from util import topic, diagram, callout, code


def rendering() -> str:
    t1 = topic("ren-spectrum", "The rendering spectrum is a product decision",
               "CSR SSR SSG ISR streaming islands hydration", "Theory", f'''
  <p>Pick a default for <b>this surface</b>, not “the company stack.” A logged-in Jira board and a public marketing page should not share a religion.</p>
  <table>
    <tr><th>Model</th><th>What the browser gets first</th><th>Use when</th><th>Cost</th></tr>
    <tr><td>CSR</td><td>Shell JS, then data</td><td>Logged-in tools, highly interactive, SEO does not matter</td><td>Slow first content if JS is fat; simple ops</td></tr>
    <tr><td>SSR</td><td>HTML for this request</td><td>First paint / LCP, personalized but crawlable</td><td>Hydration; TTFB; cache is harder</td></tr>
    <tr><td>SSG / ISR</td><td>Prebuilt HTML</td><td>Mostly public, stable, CDN-friendly</td><td>Stale content; rebuild/revalidate story</td></tr>
    <tr><td>Streaming SSR</td><td>Shell then chunks</td><td>You can flush chrome before slow data</td><td>Complexity; careful suspense boundaries</td></tr>
    <tr><td>Islands</td><td>Static HTML + small interactive widgets</td><td>Read-mostly pages with a few hot spots</td><td>Great for docs/marketing; awkward for a full SPA</td></tr>
    <tr><td>Resumability</td><td>HTML + serialized listeners</td><td>You are betting on a specific framework story</td><td>Do not bluff this in an interview unless you have used it</td></tr>
  </table>
  {callout("<b>Hydration is not free.</b> SSR that hydrates a 2MB tree can win LCP and lose INP. The senior move is often <i>read view without the editor</i>, not “SSR everything.”")}
  {diagram("""Public PDP / docs     → SSG/ISR + islands for cart widget
Logged-in board       → CSR or light SSR shell + client data
Article read          → SSR/stream HTML, lazy editor
Editor                → CSR chunk, never on the read path
Checkout              → SSR or CSR with tiny JS, reliability > novelty""")}
  ''', "topics")

    t2 = topic("ren-hydrate", "Hydration, mismatch, and when CSR is the adult answer",
               "hydration mismatch CSR vs SSR", "Theory", f'''
  <p>Hydration attaches listeners and resumes React (or similar) on server HTML. It fails when server HTML ≠ first client render: <code>Date.now()</code>, <code>window</code>, random IDs, locale that differs, a flag that flips after paint.</p>
  <ul>
    <li>Use <code>useId</code> for label/input pairing across server and client.</li>
    <li>Boot critical flags with the HTML, not a later <code>/flags</code> that rewrites chrome (CLS).</li>
    <li>If the page is a tool behind login and the bundle is already large, CSR + HTTP cache + a skeleton can beat a fake-SSR story.</li>
  </ul>
  {code("TypeScript", '''// Bad: server HTML says "Good morning", client hydrates "Good evening"
function Greeting() {
  const hour = new Date().getHours(); // mismatch risk
  return <p>{hour < 12 ? "Good morning" : "Good evening"}</p>;
}
// Better: render a stable shell, set the greeting after mount, or pass hour from the server.''')}
  ''', "topics")

    return f'''
<section class="block" id="rendering" data-search="Rendering CSR SSR SSG hydration islands" data-stype="Section" data-cat="architecture">
  <p class="kicker">First paint</p>
  <h2 class="section-title">Rendering models</h2>
  <p class="lede">Say the model, the LCP element, and what you refuse to hydrate.</p>
  {t1}{t2}
</section>
'''


def routing() -> str:
    t1 = topic("rt-shell", "App shell, routes, and what must not be in main.js",
               "app shell code splitting routing prefetch", "Theory", f'''
  <p>The <b>shell</b> is chrome that is always there: product switcher, nav, search trigger, help, user menu. It should be small, cached, and boring. Features are routes (and sometimes overlays).</p>
  {diagram("""shell (chrome, auth boot, flags)
  /home
  /board/:id          ← virtualized list
  /issue/:id          ← overlay or route, lazy
  /search
  /admin/*            ← never in the board bundle
  /edit/:pageId       ← editor chunk, not on read""")}
  <p>Split at <b>route</b> first. Split at <b>component</b> when a route still contains an editor, a map, or a charting kit. Prefetch on hover/intent for the next likely route. Do not prefetch the admin graph from the board.</p>
  <p>Waterfalls: shell waits on user, user waits on flags, flags wait on layout, layout waits on 12 widgets. Collapse with a BFF “bootstrap” or parallelize what is independent. Name this in the interview — it is how TTI dies.</p>
  {code("TypeScript", '''const Board = lazy(() => import("./board/BoardPage"));
const Editor = lazy(() => import("./editor/EditorPage"));
// Prefetch editor only when the user clicks Edit, not on every page view.''')}
  ''', "topics")

    t2 = topic("rt-url", "The URL is a public API",
               "URL state deep link shareable", "Theory", f'''
  <p>If two people can share it, it belongs in the URL: board id, JQL, selected issue, tab, modal that is a real place, locale if it is not in the user profile. If it is a drag ghost or a caret, it does not.</p>
  <p>Deep links are a requirement, not a nice-to-have. Back button is a requirement. Restore scroll on back is a requirement on feeds. Design the router before the store.</p>
  {callout("A Redux store that is the only place the selected issue lives is how you break share and back. Put <code>?selected=ISSUE-18</code> in the URL and treat the store as a cache of server data.")}
  ''', "topics")

    return f'''
<section class="block" id="routing" data-search="Routing app shell code splitting URL" data-stype="Section" data-cat="architecture">
  <p class="kicker">Navigation</p>
  <h2 class="section-title">Routing and splitting</h2>
  <p class="lede">Shell stays small. Features load when the user is going there. The URL is shareable state.</p>
  {t1}{t2}
</section>
'''


def state() -> str:
    t1 = topic("st-map", "Four buckets, not one store",
               "state architecture URL server cache local ephemeral", "Theory", f'''
  <p>Every piece of state goes in exactly one bucket. If you cannot place it, you do not understand the product yet.</p>
  <table>
    <tr><th>Bucket</th><th>Examples</th><th>Tooling</th></tr>
    <tr><td>URL</td><td>board, filter, selected issue, page, sort</td><td>Router</td></tr>
    <tr><td>Server cache</td><td>issues, user, comments, flags payload</td><td>Query client / SWR / HTTP cache</td></tr>
    <tr><td>Local UI</td><td>sidebar width, “compose open”, unsaved draft pointer</td><td>useState, tiny store, IDB for drafts</td></tr>
    <tr><td>Ephemeral</td><td>drag overlay, hover, caret, in-flight pulse</td><td>refs, gesture store, do not rerender the document</td></tr>
  </table>
  {diagram("""Shareable? → URL
From the server and reusable? → server cache (keyed)
Only this session / this widget? → local
High-frequency pointer/gesture? → ephemeral / refs""")}
  <p>Context is a broadcast. <code>value=&#123;&#123;user, theme, tickets&#125;&#125;</code> rerenders the board when a presence heartbeat arrives. Split providers or use a selector store. Theme can be CSS variables so React does not need to know.</p>
  {code("TypeScript", '''type IssueViewState = {
  // URL
  issueId: string;
  tab: "comments" | "history";
  // server cache
  issue: Issue;          // query key ["issue", id]
  comments: Comment[];   // ["issue", id, "comments"]
  // local
  draft: string;
  // ephemeral
  draggingMention: boolean;
};''')}
  ''', "topics")

    t2 = topic("st-own", "Ownership and writes",
               "state ownership single writer optimistic", "Theory", f'''
  <p>One writer per fact. The board snapshot is not allowed to invent a new description for an issue the overlay also edits. The overlay mutation updates the issue key; the board card reads the same key (or a projected field). Duplicated copies are how cards lie after save.</p>
  <p>Optimistic UI: apply locally, send mutation, rollback on error, reconcile on 409. Never optimistic-delete a permission you have not confirmed if the cost of being wrong is high (payments, admin).</p>
  ''', "topics")

    return f'''
<section class="block" id="state" data-search="State architecture ownership URL cache" data-stype="Section" data-cat="architecture">
  <p class="kicker">Placement</p>
  <h2 class="section-title">State architecture</h2>
  <p class="lede">“We use Redux” is not a design. The map of URL / cache / local / ephemeral is.</p>
  {t1}{t2}
</section>
'''


def data() -> str:
    t1 = topic("da-keys", "Cache keys, invalidation, and races",
               "react query cache keys invalidation abort race", "Theory", f'''
  <p>A cache key is the identity of a server fact. If two screens need the same issue, they share <code>["issue", id]</code>. If the board needs a slimmer projection, either store the projection under a different key and update both on mutation, or store the issue once and select fields.</p>
  <ul>
    <li><b>staleTime</b> (client): how long you trust the memory cache before refetch.</li>
    <li><b>Cache-Control / ETag</b> (HTTP): how the browser/CDN trust the bytes.</li>
    <li>They are not the same. You can have a warm React Query cache and still hit the network if you set staleTime to 0.</li>
  </ul>
  {code("TypeScript", '''const keys = {
  board: (boardId: string, jql: string) => ["board", boardId, jql] as const,
  issue: (id: string) => ["issue", id] as const,
  comments: (id: string) => ["issue", id, "comments"] as const,
};
// After PATCH issue: invalidate issue(id) and any board that might show it.
// After rapid JQL: abort the previous fetch; ignore responses with old generation.''')}
  <p>Races: the user types JQL faster than the network. Solutions that work: abort, generation counter, or “only apply if this is still the requested key.” Solutions that do not: hope.</p>
  {diagram("""type → debounce 150–300ms → gen++ → fetch(gen)
response → if gen !== current: drop
mutation → optimistic patch → PATCH → 200: keep / 4xx: rollback / 409: refetch""")}
  ''', "topics")

    t2 = topic("da-bff", "BFF, REST, GraphQL, batching",
               "BFF GraphQL REST overfetch N+1 widgets", "Theory", f'''
  <p>The client should not take 80 round trips to open a dashboard. A <b>BFF</b> (or a batch endpoint) exists when aggregation is cheaper on a server that already has cookies and service identity.</p>
  <table>
    <tr><th>Style</th><th>Strength</th><th>Failure mode</th></tr>
    <tr><td>REST resources</td><td>Clear cache keys, HTTP caching</td><td>Overfetch; chatty lists</td></tr>
    <tr><td>GraphQL</td><td>Shape per screen</td><td>Unbounded queries; cache is harder; still need keys</td></tr>
    <tr><td>BFF view model</td><td>One payload for a screen</td><td>A new BFF per whim; versioning</td></tr>
    <tr><td>Batch GET</td><td>Widgets / cards by id</td><td>Need an id list first</td></tr>
  </table>
  <p>Errors as data: a widget failure must not 500 the page. Per-section error boundaries and <code>&#123; error, data &#125;</code> in the BFF beat a single throw.</p>
  {callout("<b>Pagination.</b> Offset is simple and breaks when the list mutates. Cursor is the default for feeds. Virtualized boards often use “window + load more per column,” not infinite offset of 10k.")}
  ''', "topics")

    t3 = topic("da-opt", "Optimistic updates without lying",
               "optimistic update rollback idempotency", "Theory", f'''
  <p>Good optimistic: drag a card to a new column, PATCH, on failure snap back and toast. Bad optimistic: mark an invoice paid before the server agrees.</p>
  <p>Every mutation you retry needs an <b>idempotency key</b> (<code>clientMutationId</code>). Double-click and flaky 200s are normal. The server must treat the same id as the same write.</p>
  {code("TypeScript", '''async function moveIssue(issueId: string, to: ColumnId, clientMutationId: string) {
  const prev = queryClient.getQueryData(keys.issue(issueId));
  queryClient.setQueryData(keys.issue(issueId), (old) => old && { ...old, columnId: to });
  try {
    await api.patch(`/issues/${issueId}`, { columnId: to, clientMutationId });
  } catch {
    queryClient.setQueryData(keys.issue(issueId), prev);
    throw new Error("Move failed — card restored");
  }
}''')}
  ''', "topics")

    return f'''
<section class="block" id="data" data-search="Data fetching cache BFF GraphQL races" data-stype="Section" data-cat="architecture">
  <p class="kicker">Server state</p>
  <h2 class="section-title">Data and caching</h2>
  <p class="lede">Keys, invalidation, abort, batching, and honest optimism. This is most of a senior FE design.</p>
  {t1}{t2}{t3}
</section>
'''
