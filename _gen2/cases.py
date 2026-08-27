from util import topic, diagram, callout


def _case(cid, title, search, req, nfr, scale, arch, state, api, cache, perf, sec, a11y, obs, trade):
    return topic(cid, title, search, "Case study", f'''
  <p class="stat-sub">Practice exercise (45–60 min). Not a claimed official Atlassian question.</p>
  <p><b>Requirements.</b> {req}</p>
  <p><b>Non-functional.</b> {nfr}</p>
  <p><b>Scale assumptions.</b> {scale}</p>
  <p><b>Frontend architecture.</b> {arch}</p>
  <p><b>State.</b> {state}</p>
  <p><b>API / data flow.</b> {api}</p>
  <p><b>Caching.</b> {cache}</p>
  <p><b>Performance.</b> {perf}</p>
  <p><b>Security.</b> {sec}</p>
  <p><b>Accessibility.</b> {a11y}</p>
  <p><b>Observability.</b> {obs}</p>
  <p><b>Major trade-offs.</b> {trade}</p>
  ''', "designs")


def cases() -> str:
    items = [
        _case("cs-jira", "Jira-like issue tracker / board", "Jira board case study",
              "Kanban/scrum board, issue create/view, transitions, filters, comments, permissions, plugins.",
              "INP on drag &lt; 200ms p75; 99.9% issue view availability; a11y keyboard board; tenant isolation.",
              "10k issues in a filter; 400 visible cards; 50 collaborators; plugin iframes.",
              "Modular monolith: features/board, issue-view, search. Virtualized columns. Issue view as route overlay. Plugin host iframe.",
              "URL: board, jql, selected issue. Server cache: issues, board layout. Local: drag overlay. Presence: ephemeral store.",
              "GET board snapshot; PATCH issue (optimistic); websocket or poll for remote moves. Bulk fetch issue cards, lazy extra fields.",
              "SWR on board snapshot 10–30s; mutation invalidates issue + column keys; CDN for static; no-store on HTML.",
              "Virtualize; memo card; transition for filter; code-split editor; don’t render offscreen columns fully.",
              "Server-enforced perms; encode ADF/HTML; CSRF on cookie mutations; sandbox plugins; CSP.",
              "Grid semantics or list-with-instructions; roving tabindex; live region on move; don’t rely on color for status.",
              "INP on drag; API p95 transition; plugin error rate; correlation id on issue id.",
              "Realtime vs poll; MFE plugins vs iframe; one board query vs per-column."),
        _case("cs-conf", "Confluence-like document app", "Confluence document case study",
              "Spaces, pages, tree nav, editor, comments, permissions, search, macros.",
              "LCP of page body; editor INP; conflict-safe saves; offline draft.",
              "100k pages/space tree (virtualize); 200KB–2MB docs; concurrent editors rare but painful.",
              "features/page-view (read), editor (lazy), tree, search. Macros as isolated components with error boundaries.",
              "URL: space/page/anchor. Draft in IDB. Server: page document cache. Presence optional.",
              "GET page by id/version; PUT with if-match version; tree as paginated children; search separate index.",
              "Immutable page versions; stale-while-revalidate read view; never cache draft as the published page.",
              "Don’t hydrate a 2MB editor on read view. Split read vs edit. Virtualize tree. Image lazy.",
              "XSS in stored HTML/macros; sanitize; CSP; permission on every write; version if-match.",
              "Landmarks; skip link; editor uses platform a11y (contenteditable is hard — budget for it).",
              "Save latency, conflict rate, macro crash rate, LCP body.",
              "OT/CRDT vs lock vs last-write+diff. Read/edit split vs one rich surface."),
        _case("cs-trello", "Trello-like board", "Trello board case study",
              "Lists, cards, drag-drop, members, labels, realtime.",
              "Optimistic drag; reconnect; mobile touch.",
              "Hundreds of cards; dozens of live users.",
              "Simpler than Jira: fewer plugins, flatter model. Still virtualize tall lists.",
              "Board document in cache; drag local; URL card overlay.",
              "Snapshot + event stream (websocket). Replay on reconnect.",
              "Optimistic positions; reconcile with server order ids.",
              "Keep card component cheap; images deferred.",
              "Same XSS/CSRF as any card description HTML.",
              "Keyboard move alternatives to drag.",
              "WS disconnects, drop rate.",
              "Event stream vs poll; client-authoritative drag vs server."),
        _case("cs-dash", "Analytics dashboard (100 widgets)", "dashboard 100 widgets",
              "User-configurable widgets, date range, export, share.",
              "First widgets paint &lt; 2s; no 100-request waterfalls; CLS stable grid.",
              "100 widgets; some 1M-row queries (pre-aggregated).",
              "Widget registry + layout grid; each widget lazy + error boundary; shared time-range context (split!).",
              "Layout in URL/user prefs. Time range URL. Per-widget server cache keys include range + id.",
              "Batch widget data endpoint or BFF. Prefetch visible; idle-load below fold.",
              "CDN for aggregates with short TTL; ETag per widget query.",
              "Virtualize dashboard rows; request idle; web worker for client charts if needed.",
              "Tenant data; export ACL; no token in widget URLs.",
              "Text alternatives for charts; keyboard to widget chrome.",
              "Widget error vs page error; slow-widget isolation.",
              "One mega query vs N; custom widget JS (plugins) vs catalog only."),
        _case("cs-ecom", "Ecommerce storefront", "ecommerce frontend architecture",
              "Catalog, PDP, cart, checkout, search, personalized rails.",
              "LCP on PDP; checkout reliability; inventory freshness.",
              "SEO + millions of PDPs; flash sales.",
              "SSR/ISR for PDP/catalog; CSR cart/checkout. Edge cache public pages.",
              "Cart: server + optimistic. Price: never only-client. Personalization: late, don’t block LCP.",
              "BFF for compose; inventory poll on PDP; checkout idempotent POST.",
              "CDN HTML for public; private cart no-store.",
              "Image CDN; priority LCP image; split reviews.",
              "PCI: don’t touch raw PAN if possible (hosted fields). XSS on reviews.",
              "Form labels; error announcement on checkout.",
              "Conversion funnels; checkout error rate.",
              "SSR vs CSR hybrid; personalize vs cache hit."),
        _case("cs-feed", "Social / activity feed", "infinite social feed",
              "Infinite feed, likes, composer, media, notifications badge.",
              "INP on scroll; memory after 20 screens; unread freshness.",
              "Unbound scroll; media heavy.",
              "Virtualized feed; cursor pages; unmount offscreen media.",
              "Pages in infinite query; composer local; badge poll/push.",
              "Cursor API; mutation like optimistic; rank on server.",
              "Short TTL; don’t cache personalized first page too long.",
              "Windowing; recycle players; image size.",
              "XSS in posts; report/abuse; authz on delete.",
              "Live region for new posts (polite, not every like).",
              "Scroll jank RUM; memory.",
              "Virtualize vs ‘load more’; client rank vs server."),
        _case("cs-chat", "Real-time chat", "realtime chat frontend",
              "Channels, messages, typing, receipts, attachments, search.",
              "Message INP; ordering; reconnect catch-up; a11y live.",
              "High event rate; 10k messages history.",
              "Virtualized list; WS manager singleton; catch-up REST.",
              "Messages in store keyed by channel; optimistic send; ack replace.",
              "WS for events; REST history; upload separate.",
              "Don’t cache WS; history pages cacheable per channel.",
              "Window list; debounce typing; worker for search index optional.",
              "E2E optional; ACL on channel; XSS markdown.",
              "aria-live for new messages when at bottom; don’t steal focus.",
              "WS drop, send failure, dup detection.",
              "WS vs SSE vs poll; at-least-once vs exactly-once (you won’t have exactly-once)."),
        _case("cs-admin", "Admin portal", "admin portal frontend",
              "CRUD tables, roles, audit log, bulk actions, impersonation.",
              "Correctness &gt; flash; auditability; dangerous-action UX.",
              "Tens of thousands of rows; rare usage.",
              "Feature-based admin package, lazy from main app. Table + filters in URL.",
              "Server tables; don’t dump all rows. Draft forms local.",
              "Paginated REST; bulk async job + poll.",
              "no-store on admin HTML; short cache lists.",
              "Virtualize; don’t prefetch admin into main bundle.",
              "Step-up auth; CSRF; impersonation breadcrumbs; least privilege UI.",
              "Confirm dialogs accessible; don’t use color-only for destructive.",
              "Audit every mutation from UI correlation id.",
              "In-app admin vs separate origin (security isolation)."),
        _case("cs-files", "File management", "file management uploader",
              "Browse, preview, multi-GB upload, share links, virus scan states.",
              "Resume upload; progress durable; preview sandbox.",
              "4GB files; flaky networks; 100k files in a folder (virtualize).",
              "features/browser + uploader queue (IDB). Preview in sandboxed iframe.",
              "Folder listing server cache; upload queue local durable.",
              "Multipart upload, etag parts, complete. Signed PUT to object store via BFF.",
              "Listings short TTL; never cache signed URLs long.",
              "Chunk, parallel cap, hash in worker; don’t block UI.",
              "Signed URLs, ACL, XSS via SVG/HTML preview — sandbox.",
              "Progress announced; keyboard file list.",
              "Fail/resume rates; part error.",
              "BFF vs direct-to-store; virus scan UX vs wait."),
        _case("cs-lowcode", "Low-code / app builder", "low-code builder frontend",
              "Palette, canvas, property panel, preview, publish, versioning.",
              "Canvas INP with 500 nodes; undo; preview isolation.",
              "Power users; large schemas.",
              "Editor shell; schema as data; preview iframe (separate runtime). Don’t run user JS on the builder origin unsandboxed.",
              "Document schema local + autosave; published version server.",
              "GET/PUT document; preview render uses published snapshot.",
              "Autosave debounce; conflict if two builders.",
              "Virtualize palette and layers; canvas windowing; isolate preview CSS.",
              "Sandbox user code; CSP; XSS in custom HTML widgets.",
              "Keyboard canvas is hard — plan it; don’t trap without escape.",
              "Publish failures; schema validation errors.",
              "One-tree editor vs iframe preview; CRDT vs lock."),
    ]
    return f'''
<section class="block" id="cases" data-search="Large-Scale Frontend Architecture case studies" data-stype="Section" data-cat="architecture">
  <p class="kicker">45–60 min drills</p>
  <h2 class="section-title">Large-Scale Case Studies</h2>
  <p class="lede">Timebox, speak the 15-step framework, then compare. Jira/Confluence/Trello shapes are used because they match Atlassian product gravity — still practice questions.</p>
  {''.join(items)}
</section>
'''
