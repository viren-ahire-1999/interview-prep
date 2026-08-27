from util import esc, code

Q = []

def add(level, cat, q, short, deep, miss, follow, snippet=""):
    Q.append(dict(level=level, cat=cat, q=q, short=short, deep=deep, miss=miss, follow=follow, snippet=snippet))

add("fundamentals", "architecture", "What is frontend system design, in one minute?",
    "Owning a product surface in the browser: users, critical path, client architecture, data, budgets, and degrade — not a Kubernetes diagram.",
    "You design how the page is rendered, how state is placed, how data is fetched and cached, how the money interaction stays fast, and what the user sees when the network or a plugin lies. Backend scale is in scope only when it changes the client.",
    "Drawing 12 microservices and saying React.",
    "What do you refuse to draw in 45 minutes?")
add("fundamentals", "architecture", "What do you clarify first?",
    "Questions that fork the design: SEO/login, realtime SLA, plugins, items on screen, offline, mobile.",
    "“What’s your QPS?” rarely forks a board UI. “Are plugins iframes or in-process JS?” does.",
    "Asking for the company’s total MAU and then stalling.",
    "Give three clarifying questions for “design Instagram.”")
add("fundamentals", "architecture", "Why is “10 million users” a weak FE scale statement?",
    "It does not tell you DOM size, payload, or collaborators on one screen.",
    "Say p95 visible cards, filter hits, JS kb, concurrent editors. Those force virtualize, pagination, and split.",
    "Always starting with DAU math from backend primers.",
    "What numbers would you guess for a Jira-like board?")
add("fundamentals", "architecture", "What is the critical path?",
    "First useful pixel, first interaction that must feel instant, first failure the user will see.",
    "If you cannot name those three, you are decorating boxes. Everything else is supporting cast.",
    "Equating critical path with the longest backend hop only.",
    "Name them for checkout vs a kanban board.")
add("framework", "architecture", "How do you spend a 45-minute FE design?",
    "8 min clarify/NFR/numbers, 25 min architecture+data, 10 min fail/a11y/security/metrics, 2 min close.",
    "Cut component inventories before you cut failure and a11y. 30-minute loops collapse the middle, not the ends.",
    "Spending 35 minutes on folder names.",
    "What do you cut first at 30 minutes?")
add("framework", "architecture", "What is a good “I decide” default?",
    "Pick the stricter interesting constraint and write it down so they can correct you.",
    "Example: logged-in, 400 cards, poll OK, iframe plugins, no CRDT. Silence is worse than a labeled guess.",
    "Inventing a fantasy company and 14 must-haves.",
    "When should you ask instead of deciding?")
add("rendering", "architecture", "CSR vs SSR vs SSG — how do you choose?",
    "SEO + public + stable → SSG/ISR. Personalized first paint → SSR/stream. Logged-in tool → CSR is often honest.",
    "Hydration cost can make SSR win LCP and lose INP. Read views should not hydrate editors.",
    "“We SSR everything because it’s modern.”",
    "What would you pick for a Confluence read view vs editor?")
add("rendering", "architecture", "What is hydration and why does it fail?",
    "Attaching client runtime to server HTML. It fails when that HTML ≠ first client render.",
    "Date.now, window, random ids, late flags. useId for stable ids. Boot chrome flags with the HTML.",
    "Hydration is just SSR with extra steps and no cost.",
    "How can SSR hurt INP?")
add("rendering", "architecture", "When is CSR the adult answer?",
    "Behind login, highly interactive, bundle already large, SEO does not matter.",
    "A skeleton + HTTP-cached APIs can beat fake-SSR of a 2MB board. Say it.",
    "CSR is always slower so never choose it.",
    "How do you still get a good LCP on a CSR tool?")
add("rendering", "architecture", "What are islands?",
    "Static HTML with small interactive widgets, not a full SPA hydrate.",
    "Great for docs/marketing. Awkward as the only model for a Jira-like app.",
    "Islands means micro-frontends.",
    "Where would you place an island on a PDP?")
add("routing", "architecture", "What belongs in the app shell?",
    "Boring chrome: nav, search trigger, user menu, auth boot — small and cached.",
    "Editors, admin, maps, and chart kits must not ride in main.js.",
    "Putting the editor in the shell “because we use it a lot.”",
    "How do you prefetch without wrecking TTI?")
add("routing", "architecture", "Why is the URL a public API?",
    "Share, back, refresh, and support all depend on it.",
    "Filters, selected entity, view mode, date range — URL. Drag ghost — not URL.",
    "Storing the selected issue only in Redux.",
    "What breaks if the selected issue is not in the URL?")
add("routing", "architecture", "Route split vs component split?",
    "Route first. Component-split when a route still contains a heavy island (editor, map).",
    "Prefetch on intent. Don’t prefetch admin from the board.",
    "One bundle because “HTTP/2 is fine.”",
    "Name a waterfall you would collapse with a bootstrap payload.")
add("state", "architecture", "What are the four state buckets?",
    "URL, server cache, local UI, ephemeral.",
    "Shareable → URL. From server and reused → cache. Session widget → local. Pointer/gesture → refs.",
    "“Everything in Redux” as an architecture.",
    "Place: JQL, issue body, draft comment, drag overlay.")
add("state", "architecture", "Why is fat context a design bug?",
    "Any value change rerenders all consumers. Heartbeats will rerender the board.",
    "Split providers or use a selector store. Theme can be CSS variables.",
    "Memoizing the world to save a fat context.",
    "How do you prove it in Profiler?")
add("state", "architecture", "Who is allowed to write a fact?",
    "One writer per fact. Board cards and the overlay must share the issue key.",
    "Duplicated copies are how the card lies after save. Optimistic updates patch the same key.",
    "Each screen keeps its own copy of the issue “for simplicity.”",
    "What happens on 409 after an optimistic move?")
add("data", "architecture", "What is a cache key?",
    "The identity of a server fact, e.g. [\"issue\", id].",
    "Shared keys prevent drift. Projections need an update story. staleTime ≠ HTTP Cache-Control.",
    "Using the component name as the cache key.",
    "What do you invalidate after PATCH issue on a board?")
add("data", "architecture", "How do you kill a JQL race?",
    "Abort the previous fetch and/or ignore responses with an old generation.",
    "Debounce input; only the latest gen may write the cache. Hope is not a strategy.",
    "Disabling the input while a request is in flight as the only fix.",
    "Show TypeScript-sized pseudocode for gen++.")
add("data", "architecture", "When do you want a BFF?",
    "When the screen would take too many round trips or leak service-to-service secrets.",
    "A view-model or batch endpoint for 100 widgets. A new BFF per whim is ceremony.",
    "BFF because GraphQL is scary.",
    "How do you isolate a widget 500 so the page survives?")
add("data", "architecture", "Optimistic UI — when not to?",
    "When being wrong is expensive: payments, irreversible admin, legal.",
    "Good: drag a card, rollback on error. Always idempotency keys on retries.",
    "Optimistic everything to feel “snappy.”",
    "What is a clientMutationId for?")
add("data", "architecture", "Offset vs cursor pagination?",
    "Cursor for feeds and mutating lists. Offset is simple and breaks when rows move.",
    "Boards often window per column rather than infinite-offset 10k.",
    "page=1000 as a badge of scale.",
    "How do you restore scroll on a back-navigation to a feed?")
add("realtime", "architecture", "Poll vs SSE vs WebSocket?",
    "Pick a freshness SLA. Poll is valid. SSE one-way. WS bidirectional.",
    "Keep REST as source of truth. Socket is a hint. Dedupe by id. Reconnect with since-cursor.",
    "“Just use WebSockets” in minute one.",
    "What do you show when the socket dies?")
add("realtime", "architecture", "Presence vs document state?",
    "Heartbeats must not setState on the document body.",
    "Colocate presence. Throttle UI. Caret is ephemeral; a comment is not.",
    "Putting viewers[] on the same context as issue.description.",
    "How fast would you tick avatar updates?")
add("realtime", "architecture", "Why isn’t the socket lossless?",
    "Disconnects, at-least-once delivery, proxy idle timeouts, dropped frames.",
    "After reconnect, snapshot or since-seq. Dedupe. Never assume the stream was complete.",
    "Trusting WS as the inbox.",
    "Design gap-fill for chat.")
add("performance", "performance", "LCP vs INP vs CLS in one line each?",
    "LCP: when the main content appears. INP: how laggy interactions feel. CLS: how much the layout jumps.",
    "LCP → HTML/image/JS before paint. INP → main thread + React work. CLS → reserved space and early flags.",
    "Treating Lighthouse as the product.",
    "Why can INP be bad when LCP looks fine?")
add("performance", "performance", "When do you virtualize?",
    "When p95 list size makes the DOM or render expensive — after you have a number.",
    "Cost: measurement, scroll jump, a11y. Paginate when users think in pages.",
    "Virtualize everything including a 12-item menu.",
    "What a11y must you still provide?")
add("performance", "performance", "How do you debug a laggy React app in 15 minutes?",
    "Reproduce, Performance panel for long tasks, Profiler for who rerenders, then Network.",
    "Hypotheses: fat context, unbounded list, sync plugin init, huge handler. Fix the largest slice.",
    "Sprinkling memo before measuring.",
    "What is the first DevTools click for a sticky search box?")
add("performance", "performance", "What is a performance budget?",
    "A CI number that fails the build: JS kb, LCP, INP.",
    "Without it the bundle only grows. Product and eng own it together.",
    "Budgets are for native games only.",
    "What budget would you set for an issue view route?")
add("performance", "performance", "Why move work to a worker?",
    "Hashing, encoding, big parse — keep the main thread free for INP.",
    "Don’t setState every byte. rAF-throttle progress. Don’t put File in Redux.",
    "Workers for every click handler.",
    "Design a 2GB upload without freezing the tab.")
add("offline", "architecture", "What should work offline in v1?",
    "Usually drafts, not the entire mutation graph.",
    "IDB persist. Queue with idempotency. Conflict UX. SW caches shell + immutable assets, not personalized HTML as public.",
    "“PWA” as a substitute for a product decision.",
    "Two tabs both flush the same queued comment — what happens?")
add("offline", "architecture", "How do you show eventual consistency without lying?",
    "Label pending, failed, and conflicted. Don’t paint a 200 that hasn’t happened.",
    "Optimistic is a maybe. Banners beat silent clobber. History link on conflict.",
    "Spinner forever or fake success.",
    "409 on a published page — what does the user see?")
add("ds", "architecture", "What is a design-system token?",
    "A named design decision (color, space, type) that themes swap.",
    "Features consume tokens, not hex. Breaking token meaning is semver.",
    "A token is a Sass variable dumped in a feature.",
    "How do you theme dark mode without rerendering the board?")
add("ds", "architecture", "How do you stop a DS junk drawer?",
    "Tight variant APIs, RFC, a11y review, versioning, no “just this once” props.",
    "Slots and variants beat 40 booleans. Escaped one-offs become the system.",
    "Accepting every product request into Button.",
    "When is a one-off in the product allowed?")
add("collab", "architecture", "OT vs CRDT vs If-Match — what do you say?",
    "Most work software needs versions and a conflict UI, not a CRDT lecture.",
    "If they want Google Docs, you integrate a known engine and spend the hour on awareness, undo, offline, permissions.",
    "Implementing CRDT on the whiteboard to look senior.",
    "What is a soft lock good for?")
add("collab", "architecture", "Why split read and edit?",
    "Read should not download or hydrate the editor.",
    "LCP and INP both win. Macros on read still need isolation.",
    "One rich surface “to share code.”",
    "Where does the draft live while offline?")
add("auth", "security", "Why must the client never grant power?",
    "UI hide is UX. Server deny is security. Design 403.",
    "Tenant id from the session, not a writable query param. Export and search leak.",
    "Trusting a canDelete flag in localStorage.",
    "How do you still show a disabled Delete that explains why?")
add("auth", "security", "Why not access tokens in localStorage?",
    "Any XSS can exfiltrate them. Prefer HttpOnly cookies + CSRF strategy, or memory + refresh cookie.",
    "JWT as a format is fine; skipping revocation and tenant checks is not.",
    "localStorage is “simpler for SPAs.”",
    "What does SameSite actually buy you?")
add("security", "security", "Name XSS paths that are not dangerouslySetInnerHTML.",
    "Markdown→HTML, plugin HTML, javascript: hrefs, CSS url(), open redirects, SVG.",
    "Encode default, sanitize if you must store HTML, CSP as depth, sandbox iframes.",
    "“React is safe so we are safe.”",
    "What does a useful CSP look like for a plugin host?")
add("security", "security", "CSRF vs CORS?",
    "CSRF is the browser attaching cookies to a foreign-initiated request. CORS is which origins may read a response via XHR.",
    "CORS is not CSRF protection. Cookie mutations need a token, custom header, or a SameSite story you can defend.",
    "“We have CORS so CSRF is done.”",
    "How do you CSRF-protect a cookie-session PATCH?")
add("a11y", "architecture", "When is ARIA required vs a smell?",
    "Required when you invent a widget (combobox, dialog, grid). Smell when you ARIA a native button.",
    "Semantics first. APG by name. Focus trap and restore.",
    "aria-label on everything “for a11y.”",
    "Specify the keyboard model for a board.")
add("a11y", "architecture", "Why isn’t drag-and-drop enough?",
    "It excludes keyboard and many AT users. Provide a menu or shortcuts and announce the result.",
    "Roving tabindex on cards. Live region: “ISSUE-18 moved to Done.”",
    "“We’ll add keyboard later.”",
    "What role/pattern do you use for typeahead?")
add("obs", "architecture", "What four metrics would you watch in week one of a board?",
    "LCP of the board, INP of drag, transition error rate, plugin crash rate — plus a correlation id.",
    "SLIs vs vanity. Flags that move chrome must not cause CLS.",
    "A 40-graph dashboard and no correlation id.",
    "How do you boot a flag that adds a top banner?")
add("obs", "architecture", "Why are feature flags architecture?",
    "They create versions of the product in the wild and can break hydrate/CLS.",
    "Inline chrome flags with HTML. Reserve space. Don’t fetch-then-push the board.",
    "Flags as a few ifs in random components.",
    "What is an experiment flicker?")
add("mfe", "architecture", "When are micro-frontends justified?",
    "When independent deploy is worth duplicate runtime, CSS fights, and debug tax.",
    "Default: packages. Untrusted: iframe. Federation last. People-scale ≠ runtime split.",
    "Federate everything for “ownership.”",
    "How do you answer “we should federate the design system”?")
add("mfe", "architecture", "Why iframe untrusted plugins?",
    "Process isolation, CSP, capability tokens, crash containment.",
    "postMessage and resize are the tax. In-process vendor JS shares the user’s session and the main thread.",
    "eval of plugin JS because iframes feel old.",
    "What budget do you set per plugin slot?")
add("media", "performance", "How do you upload 2GB without jank?",
    "Chunk, resume in IDB, hash in a worker, signed URLs, rAF progress, cap concurrency.",
    "Don’t stream through the BFF without a reason. Don’t put File in the global store.",
    "FileReader on the main thread for the whole blob.",
    "What happens when a signed URL expires mid-upload?")
add("media", "performance", "How do you treat the LCP image?",
    "One priority image with dimensions. Lazy the rest. srcset.",
    "Don’t decode 40 heroes. Reserve aspect-ratio to kill CLS.",
    "loading=lazy on the LCP image.",
    "PDP vs feed — which image is LCP?")
add("search", "architecture", "What is the a11y name for typeahead?",
    "Combobox (APG). aria-activedescendant or the modern pattern you can defend. Announce count.",
    "Same pattern for command palette. Abort and debounce are part of the design.",
    "A div list with onClick only.",
    "How do you prevent leaking private issue titles in suggest?")
add("search", "architecture", "Why is the search URL the query?",
    "Shareable, back-button, supportable. Filters and q belong there.",
    "Cache key is the full query. Abort on change. Cursor not deep offset.",
    "q only in component state.",
    "Zero results — what do you design?")
add("commerce", "architecture", "Why split PDP and checkout bundles?",
    "PDP is SEO and LCP. Checkout is reliability and tiny JS.",
    "ISR/SSR the PDP. Don’t ship the CMS or the dashboard on either.",
    "One storefront SPA for everything including admin.",
    "Would you optimistic-update a payment?")
add("canvas", "architecture", "How do you scope “design Figma”?",
    "v1: camera, selection, move, inspector. Scene in a ref. Honest no-CRDT.",
    "React for panels only. If they want multiplayer, name a known engine.",
    "Implementing OT in 20 minutes.",
    "SVG vs canvas/WebGL — how do you choose in v1?")
add("platform", "architecture", "How do you boot i18n without CLS?",
    "Locale known before paint (URL/cookie). Catalogs split by route. dir on html.",
    "Don’t block the board on admin strings. Stable hydrate. Format dates with locale APIs.",
    "One 2MB mega-catalog in main.js.",
    "Where do you put RTL?")
add("platform", "architecture", "What is a bootstrap payload?",
    "One first response with user, critical flags, and shell config to kill waterfalls.",
    "Then feature routes fetch their own data. Don’t hide a 200-field god object forever.",
    "12 sequential GETs: user, flags, layout, theme, …",
    "What must still stream/SSR for LCP?")
add("judgment", "architecture", "What does “two rejected options” sound like?",
    "“I rejected in-process plugins because XSS and INP; iframes cost UX seams.”",
    "Interviewers hire the person who can say no. Library names are not rejects.",
    "“We could also use Vue.”",
    "Give rejects for notifications and for a document editor.")
add("judgment", "architecture", "How do you handle an unknown requirement?",
    "Label an assumption, pick v1, say what you would measure.",
    "Don’t freeze. Don’t invent a platform. Timebox and move.",
    "Silence, or a 10-minute tangent on Kafka.",
    "They say “make it like Figma” at minute 40 — what do you do?")
add("judgment", "architecture", "What is an ADR sentence in an interview?",
    "Context → options → decision → why → consequence.",
    "“Given untrusted apps, iframe sandbox over in-process JS, because containment; consequence: postMessage tax.”",
    "“We’ll use the industry standard.”",
    "Speak an ADR for read vs edit on a wiki page.")
add("fundamentals", "architecture", "Shell vs feature — who owns permissions UI?",
    "A shared authz helper/service. Features must not each parse JWT.",
    "Chrome may hide links; each mutation still hits the server. Plugin host has its own cap tokens.",
    "Copy-pasting canEdit into every folder.",
    "Where do you put “export disabled because of plan” copy?")
add("data", "architecture", "GraphQL vs REST on the client?",
    "GraphQL helps shape; you still need cache keys and cost control. REST + BFF is valid.",
    "Unbounded GraphQL is an N+1 in costume. HTTP caching is easier on REST GETs.",
    "GraphQL because it is what seniors use.",
    "How do you cache a GraphQL issue query next to a REST board?")
add("data", "architecture", "What does stale-while-revalidate mean on the client?",
    "Show last cache immediately, refetch in background, swap when fresh.",
    "Great for boards. Bad if you must not show stale money (balances) — then wait or mark stale.",
    "SWR as a reason to ignore authz.",
    "When is showing stale dangerous?")
add("realtime", "architecture", "How do you design mark-as-read without a stampede?",
    "Debounce, batch ids, idempotent POST, don’t fire on every pixel of scroll unless you mean to.",
    "Email clients die here. Track last-visible id, flush on idle or blur.",
    "A POST per row on render.",
    "How do unread badges stay honest after batching?")
add("performance", "performance", "What causes CLS on a “simple” tool app?",
    "Late banners from flags, web fonts, images without size, plugin slots that grow.",
    "Reserve chrome. Boot flags early. Aspect-ratio. Cap plugin height.",
    "CLS is only a marketing-site problem.",
    "How do you reserve a plugin slot you have not loaded?")
add("performance", "performance", "Why can useCallback make things worse?",
    "It is extra work and still changes when deps are fat/unstable, busting memo children.",
    "Colocate and shrink props first. Stabilize only what you measured.",
    "Wrap every function for “performance.”",
    "When is useCallback correct?")
add("security", "security", "What is clickjacking in a FE design?",
    "Your UI framed by an attacker; user clicks a hidden dangerous control.",
    "frame-ancestors / X-Frame-Options. Careful if you need to be embedded as a plugin yourself.",
    "CSRF token solves clickjacking.",
    "Can a Jira-like app be embedded? What’s the policy?")
add("security", "security", "How do you preview a user-uploaded HTML file?",
    "You probably don’t, on your origin. Sandboxed iframe + different origin + CSP, or convert to safe PDF.",
    "Never innerHTML the upload in the app origin.",
    "Opening the blob: URL in the same origin is “fine.”",
    "What about SVG uploads?")
add("a11y", "architecture", "What is focus restore?",
    "When a modal/palette closes, return focus to the invoker.",
    "Without it, keyboard and SR users fall to the document start. Part of dialog APG.",
    "Focus the first field of the page on every route change “for a11y.”",
    "What do you focus when the invoker was a deleted row?")
add("obs", "architecture", "What is a correlation id from a click?",
    "An id born in the client (or taken from the server) that you send on the mutation and show in support UI.",
    "Ties RUM span → API log → user report. More useful than “it was slow.”",
    "Logging the whole Redux store.",
    "Where do you display it to the user?")
add("mfe", "architecture", "Build-time packages vs module federation?",
    "Packages share a release train and one React. Federation independently deploys JS at the cost of skew.",
    "Most orgs need folders and CI owners, not federation.",
    "Federation as the default “modern” architecture.",
    "What shared deps problem does federation create?")
add("media", "performance", "Why isolate a &lt;video&gt; from comment state?",
    "So likes and polling cannot rerender the media element and drop frames.",
    "Player island / ref. Comments are a sibling tree.",
    "One big WatchPage state.",
    "What else belongs in the island?")
add("work", "architecture", "What does select-all mean in a 50k-row grid?",
    "You must say: this page vs the whole query. The latter is a server job.",
    "Silent page-only select-all is how ops people nuke the wrong set — or think they did.",
    "A checked box in the header, unspecified.",
    "How do you show “50,000 selected” without loading 50,000 rows?")
add("work", "architecture", "Where do recurring calendar events expand?",
    "On the server for the visible range. The client layouts chips.",
    "Expanding years of rrules in the browser is a lock-up.",
    "Store every instance in React state for the year.",
    "How do you edit “this event” vs “the series”?")
add("realtime", "architecture", "When is SSE better than WS?",
    "One-way server push, simpler reconnect (EventSource), no client→server frames needed.",
    "Still keep REST. Still dedupe. Proxies and HTTP/2 matter — know they exist.",
    "SSE is obsolete because WS exists.",
    "Can you send mark-read over SSE?")
add("fundamentals", "architecture", "What is degrade in one sentence?",
    "The product still completes the job when the fancy channel dies.",
    "Poll if WS dies. Read-only if save conflicts. Hide the plugin if it throws. Say it before they ask.",
    "A spinner that never ends.",
    "Write the degrade sentence for notifications.")
add("judgment", "architecture", "How do you use Phase 2 vs this course in an interview?",
    "This course is the 45-minute product design. Phase 2 is why React rerendered and how Fiber works if they drill.",
    "Don’t reciting Fiber when they asked for a feed. Don’t skip INP when they asked for React performance.",
    "Mixing both into an unfocused dump.",
    "They ask “what happens on setState” mid-design — 90 seconds, then return to the board.")
add("fundamentals", "architecture", "What belongs in v1 vs v2 in every design?",
    "v1: money path, degrade, a11y of that path, security of that path. v2: polish, extra realtime, plugins.",
    "Say the cut. Interviewers listen for it.",
    "Listing 20 features as all v1.",
    "Cut a feed design to v1 in 20 seconds.")
add("data", "architecture", "How do you cache user + flags + layout without a waterfall?",
    "Bootstrap GET or SSR-embedded JSON for the critical trio; then parallel feature fetches.",
    "Don’t serialize the entire app into bootstrap. Don’t 4 sequential hops before first paint.",
    "Await user, then flags, then layout, then board.",
    "Which of those three can be in the HTML?")
add("performance", "performance", "What is the LCP element on a board vs a PDP vs a feed?",
    "Board: first cards/chrome text. PDP: product image. Feed: first post media.",
    "If you don’t name it, you cannot prioritize it. Don’t lazy the LCP image.",
    "“The hero” without pointing.",
    "How do you mark it in code (fetchpriority / preload)?")
add("security", "security", "What is a capability token for a plugin?",
    "A short-lived, scoped credential for one slot, not the user’s full session cookie.",
    "The iframe asks the host; the host mints; the API checks the cap. Limits blast radius.",
    "Passing the session cookie into the iframe “temporarily.”",
    "What scopes would an issue-glance plugin get?")
add("a11y", "architecture", "Live region polite vs assertive?",
    "Polite: “issue moved.” Assertive: blocking error. Don’t assertive-spam.",
    "Toasts and presence are usually polite or not live at all.",
    "Assertive on every badge increment.",
    "Does a like on a feed need a live region?")
add("collab", "architecture", "What is If-Match doing on PUT page?",
    "Optimistic concurrency: you save only if the version you loaded is still current.",
    "409 means someone else wrote. Show diff or reload. Pair with clientMutationId for retries.",
    "Last write silently wins always.",
    "How does this interact with drafts in IDB?")
add("platform", "architecture", "Why hashed immutable JS + no-store HTML?",
    "Assets can live on a CDN forever. HTML is the pointer that must update.",
    "Personalized HTML must not be cached as public. Board JSON often private, short TTL or ETag.",
    "Cache-Control: public on the HTML of a logged-in board.",
    "What do you set on /api/issues/:id?")
add("judgment", "architecture", "How do you end the interview?",
    "Restate v1, two rejects, metrics, ask what they want to go deeper on.",
    "Don’t introduce a new subsystem at 0:45. Don’t apologize for not drawing Kafka.",
    "Talking until they cut you.",
    "They say “anything else?” — what 20-second add-on is high value?")
add("fundamentals", "architecture", "Name the 16 steps in order.",
    "Restate, clarify, FR, NFR, assumptions, architecture, components, flow, API, state, cache, perf, fail, security+a11y, observe, trade-offs.",
    "If you freeze, jump to the next unused step. Failure and a11y are not optional epilogues.",
    "Starting at API because you memorized CRUD.",
    "Time yourself saying only the step names.")
add("data", "architecture", "What is N+1 on the client?",
    "A list render that fires a request per row (or per widget) instead of a batch/BFF.",
    "100 widgets × GET is the classic dashboard fail. Prefetch-visible still needs a batch.",
    "N+1 is only a backend ORM problem.",
    "How do you batch issue cards after a board id list?")
add("realtime", "architecture", "Push notifications vs in-app inbox?",
    "Push reaches a closed tab (with permission). Inbox is still required when they open the app.",
    "Don’t treat SW push as the source of truth. Same dedupe ids.",
    "Push replaces the bell.",
    "What if the user denied notification permission?")
add("performance", "performance", "Why reserve min-height for chrome?",
    "Late flags and banners are a top CLS source in tools.",
    "Know the banner height at paint, or don’t insert it above the board after hydrate.",
    "Animating height from 0 is “fine if it’s pretty.”",
    "How do plugins interact with this rule?")
add("work", "architecture", "Issue overlay vs full route — how do you choose?",
    "Overlay keeps board context and back-stack; full route is shareable and simpler for deep work.",
    "Many products do both: /board?selected= and /issue/:id. Same cache key for the issue.",
    "Modals for everything because they look modern.",
    "What happens to the board subscription while the overlay is open?")
add("judgment", "architecture", "What must you never claim in this course’s examples?",
    "That you shipped a specific Atlassian feature, or that a prompt is an official question.",
    "Use “Jira-like.” Official process/values stay labeled official on the Phase 4 file. Practice is practice.",
    "Inventing metrics from a company you did not work at.",
    "How do you cite atlassian.design in an interview?")


def feq() -> str:
    blocks = []
    for i, item in enumerate(Q, 1):
        snip = code("TypeScript", item["snippet"]) if item["snippet"] else ""
        blocks.append(f'''
<article class="q" id="feq-{i}" data-level="{item["level"]}" data-cat="{item["cat"]}" data-search="{esc(item["q"])}" data-stype="Interview question" data-mock="1">
  <div class="meta-row"><span class="badge badge-js">{item["level"]}</span><span class="chip">{item["cat"]}</span><span class="chip">Q{i}</span></div>
  <h3>{i}. {esc(item["q"])}</h3>
  <p><button type="button" class="toggle-btn" data-toggle="feq-a-{i}">Reveal answer</button>
     <button type="button" class="toggle-btn" data-complete="questions" data-cid="feq-{i}">Mark complete</button></p>
  <div class="reveal" id="feq-a-{i}">
    <p><b>Short answer.</b> {item["short"]}</p>
    <p><b>Deep explanation.</b> {item["deep"]}</p>
    {snip}
    <p><b>Common misconception.</b> {item["miss"]}</p>
    <p><b>Senior follow-up.</b> {item["follow"]}</p>
  </div>
</article>''')
    return f'''
<section class="block" id="feq" data-search="Frontend system design interview questions" data-stype="Section">
  <p class="kicker">{len(Q)} questions</p>
  <h2 class="section-title">Interview Q&amp;A</h2>
  <p class="lede">Answer standing up. Then reveal. Mark complete only if you can teach the short answer without this file. All items are practice questions.</p>
  <div class="tabs" data-tabs="feq">
    <button type="button" class="tab active" data-tab="all">All ({len(Q)})</button>
    <button type="button" class="tab" data-tab="architecture">architecture</button>
    <button type="button" class="tab" data-tab="performance">performance</button>
    <button type="button" class="tab" data-tab="security">security</button>
    <button type="button" class="tab" data-tab="fundamentals">fundamentals</button>
    <button type="button" class="tab" data-tab="judgment">judgment</button>
  </div>
  {''.join(blocks)}
</section>
'''
