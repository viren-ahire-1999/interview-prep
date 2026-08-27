from util import code, esc

Q = []

def add(level, cat, q, short, deep, miss, follow, snippet=""):
    Q.append(dict(level=level, cat=cat, q=q, short=short, deep=deep, miss=miss, follow=follow, snippet=snippet))

add("fundamentals", "react", "What exactly causes a React re-render?",
    "A state/context/store update on that Fiber (or a parent render that reaches it).",
    "Function components re-run when React renders their Fiber. That happens after setState, a context value change they consume, a store subscription fire, or a parent render unless memo bails out. Props changing is usually because the parent rendered.",
    "“Props changed” as a mystical force independent of the parent.",
    "Does a parent re-render always change the DOM?")
add("fundamentals", "react", "Does a parent re-render always mean the DOM changes?",
    "No. Render is JS. Commit patches the DOM only when host fibers differ.",
    "A child can run and return the same elements; React skips DOM work. memo can skip the child function entirely if props are equal.",
    "Re-render = DOM update.",
    "How do you see the difference in DevTools?")
add("internals", "react", "What happens when setState is called?",
    "Create an update, schedule a lane, render (interruptible), reconcile, commit DOM + effects.",
    "See Internals section. Batching may merge updates. Render can be thrown away. Effects run after paint (except layout).",
    "setState writes the DOM immediately.",
    "What can happen before commit?")
add("internals", "react", "Why can rendering be interrupted?",
    "So urgent input can run; large updates yield.",
    "Concurrent React schedules work in lanes. Transitions are interruptible. That is why render must be pure enough to retry.",
    "React 18 always paints every render attempt.",
    "What is a transition vs an urgent update?")
add("internals", "react", "Explain Fiber in one minute.",
    "A linked work unit: type, pending props, state, effects, DOM pointer, return/child/sibling.",
    "Two trees (current / WIP). Reconciliation walks Fibers. It is the scheduler’s unit of work, not a user API.",
    "Fiber is the virtual DOM array.",
    "Where is hook state stored?")
add("internals", "react", "Where does hook state live?",
    "On the Fiber, as a linked list, in call order.",
    "That is why hooks cannot be conditional. The identity of the nth hook is position, not the name useState.",
    "Hooks live in a global React map keyed by function name.",
    "What happens if you call a hook inside a condition?")
add("reconciliation", "react", "Why does React need keys?",
    "To match list children to the correct Fiber across reorder/insert/delete.",
    "Without stable keys, index matching moves state to the wrong item. Key change = remount.",
    "Keys are a performance hint only.",
    "What happens if key A becomes key B?")
add("reconciliation", "react", "What happens when key A becomes key B on the same type?",
    "Unmount A, mount B. State and effects reset.",
    "Identity includes the key. It is not a prop change.",
    "React copies state because the type is the same.",
    "When would you change a key on purpose?")
add("reconciliation", "react", "Why are index keys dangerous?",
    "Reorder/delete remaps Fibers; local state and uncontrolled inputs slide.",
    "OK only for static never-reordered lists.",
    "Index keys are recommended for performance.",
    "Give a Jira board example.")
add("hooks", "react", "useEffect vs useLayoutEffect?",
    "Layout runs after DOM mutation before paint; effect after paint.",
    "Layout for measure-and-sync-mutate. Effect for subscriptions and network. Layout blocks paint — keep it tiny.",
    "They are interchangeable.",
    "What happens if you setState in layout?")
add("hooks", "react", "When should you use useMemo?",
    "When you measured that a derived value is expensive and deps are stable.",
    "Also to stabilize referential identity for a memoized child. Not for every object literal “just in case.”",
    "useMemo is free and should wrap everything.",
    "When does it do nothing useful?")
add("hooks", "react", "When does useCallback make things worse?",
    "When deps change every render, or no child actually cares about reference equality.",
    "You pay hook + array compare + noise. Prefer colocation so the child isn’t in a hot parent.",
    "useCallback always reduces renders.",
    "Show a case where an inline function is fine.")
add("hooks", "react", "Why must hooks be unconditional?",
    "Order is identity.",
    "A conditional hook shifts the list; state attaches to the wrong hook; React throws in dev.",
    "It’s only a style rule.",
    "Custom hooks — do they have the same rule? (yes)")
add("hooks", "react", "What is a stale closure in a hook?",
    "An effect or callback captured old props/state.",
    "Fix with deps, functional updates, or a ref for latest. See Phase 1.",
    "React automatically always sees latest state in every closure.",
    "How does the compiler/React Forget change the story? (still explain the model)")
add("performance", "react", "How do you debug a slow React app in 15 minutes?",
    "Reproduce, record Profiler + Performance, find long tasks vs wide renders vs network.",
    "Check fat context, 20k rows, sync work in click handlers, huge bundles. Fix structure first (virtualize, split, colocate).",
    "Start by adding memo to every component.",
    "Which metric do you watch for a laggy click?")
add("performance", "react", "Why is memo-everywhere a bad strategy?",
    "Cost, noise, still broken if props are new objects, hides real issues.",
    "Measure; then isolate the hot subtree. Memo is a scalpel.",
    "Facebook said to memo everything.",
    "What structural fix beats memo for a fat context?")
add("performance", "react", "How do you stop context from re-rendering the world?",
    "Split providers; stable values; selector store.",
    "Don’t put tickets next to theme. Don’t value={{}}.",
    "Context is always faster than Redux.",
    "useContextSelector — when?")
add("performance", "react", "What is virtualization and when is it required?",
    "Render only visible rows (+overscan).",
    "Boards, tables, feeds, trees. A11y and jump-to need extra API (rowcount, scrollTo).",
    "CSS overflow:auto is virtualization.",
    "How do you virtualize a horizontal board column?")
add("state", "architecture", "Context vs Redux?",
    "Context = dependency injection + infrequent value. Redux = many writers, event log, selectors.",
    "Server data belongs in a cache layer either way. Toolkit vs Zustand is ceremony, not morality.",
    "Redux is required at scale.",
    "Where do you put fetched issues?")
add("state", "architecture", "What state belongs in the URL?",
    "Shareable, back-buttonable, analytical: filters, selected id, tabs, pagination.",
    "Not keystrokes in a password field. Not ephemeral hover.",
    "URLs are only for marketing.",
    "How do you type URL state safely?")
add("state", "architecture", "Why is server state not global UI state?",
    "It has freshness, identity on the server, and invalidation — not a useState lifetime.",
    "Duplicating it in Redux without a cache policy creates stale UIs.",
    "Put all API data in Redux for consistency.",
    "How do you invalidate after a transition?")
add("fetching", "architecture", "How do you prevent search race conditions?",
    "AbortController + generation token; ignore stale responses.",
    "Debounce reduces pressure but does not fix races alone.",
    "await in order guarantees order (it doesn’t if you don’t cancel).",
    "Show both abort and gen in one snippet.")
add("fetching", "architecture", "Optimistic update — when not to?",
    "Irreversible, highly contended, or hard-to-rollback side effects.",
    "Payments, unique-name deletes, transitions with validators — wait for server or preview.",
    "Always optimistic for perceived performance.",
    "How do you rollback a board move?")
add("fetching", "architecture", "What is a good cache key?",
    "The full identity of the query: resource + params the server used.",
    "Colliding keys share data by accident. Missing params show wrong pages.",
    "use the URL path only always.",
    "Board vs issue vs search keys after a move.")
add("architecture", "architecture", "How would you structure a React app for 20 engineers?",
    "Modular monolith, feature packages, enforced imports, small shared kernel, DS package, CODEOWNERS.",
    "See Fundamentals. CI affected tests. RFC for kernel changes.",
    "Micro-frontends by default.",
    "How do you enforce boundaries?")
add("architecture", "architecture", "How do you prevent a dependency mess?",
    "Allowed-import graph + lint in CI + review culture + few public barrels.",
    "Folders alone rot. Deep imports of another feature are incidents.",
    "TypeScript visibility is enough (it isn’t for runtime files).",
    "Show a forbidden import example.")
add("architecture", "architecture", "Smart vs presentational in 2026?",
    "Hooks hold policy/data; views take props. Still a useful split for testability.",
    "Not HOCs and not “container classes required.”",
    "Everything must be presentational.",
    "Where do you put permissions checks?")
add("architecture", "architecture", "Where do feature flags live?",
    "Evaluated at the feature edge from a bootstrap/service; typed map; not 40 raw ifs.",
    "Flags are not authorization. Defaults when the service is down.",
    "Hardcode flags in components.",
    "How do you avoid flicker?")
add("architecture", "architecture", "Error boundaries — where?",
    "Route + expensive widgets + plugin slots. Not around every button.",
    "They catch render errors, not events/async unless you route those in.",
    "One boundary at the root is enough for plugins.",
    "What do you show in the fallback?")
add("mfe", "architecture", "When do you refuse micro-frontends?",
    "When the problem is team process, not deploy isolation; when the domain is one issue object.",
    "Cost: duplicate runtime, UX drift, shared-dep hell. Prefer modular monolith.",
    "MFEs are the mature form of React apps.",
    "When would you accept them?")
add("mfe", "architecture", "How do MFEs share React?",
    "Singleton; two Reacts break hooks.",
    "Module federation shared or iframe isolation (two heaps then).",
    "Just npm install react in each.",
    "How do they share auth?")
add("ds", "architecture", "How do you version a design system?",
    "Semver, deprecation window, codemods, visual CI, dual-major if needed.",
    "Treat Button padding as public API.",
    "Just publish and Slack it.",
    "How do 12 teams migrate a breaking change?")
add("ds", "architecture", "Headless vs styled components?",
    "Headless for hard a11y widgets; styled composites for brand.",
    "Buy Radix/Aria; own tokens and product patterns.",
    "Always write your own combobox.",
    "What belongs in the DS vs the product?")
add("browser", "browser", "Explain the critical rendering path.",
    "HTML/CSS → DOM/CSSOM → render tree → layout → paint → composite; JS may block.",
    "See Browser section. Preload LCP; defer non-critical JS.",
    "The browser paints after all JS.",
    "What blocks LCP on a Confluence page?")
add("browser", "browser", "Layout vs paint vs composite?",
    "Geometry vs pixels vs layer stitch.",
    "Width changes layout; some transforms composite. Forced reflow if you interleave read/write.",
    "They are synonyms.",
    "Name APIs that force layout.")
add("browser", "browser", "preload vs prefetch vs preconnect?",
    "preload: this page, high. prefetch: future nav. preconnect: early TLS.",
    "Mis-preload fights the LCP image for bandwidth.",
    "They are the same hint.",
    "When does preload hurt?")
add("webperf", "performance", "LCP vs INP vs CLS?",
    "Largest content / interaction delay / layout shift.",
    "Connect each to a decision (image, long task, reserved space).",
    "Lighthouse score is the product goal.",
    "Why INP can be bad when LCP is good.")
add("webperf", "performance", "What is a long task and why does it hurt INP?",
    ">50ms on the main thread blocks input.",
    "Break work, workers, debounce, virtualize, defer analytics.",
    "Long task means a large file on disk.",
    "How do you find them?")
add("network", "browser", "Cache-Control vs ETag?",
    "Freshness policy vs validator for 304.",
    "Hashed assets: immutable long max-age. HTML/API: short or private + ETag.",
    "ETag replaces Cache-Control.",
    "What is stale-while-revalidate?")
add("network", "browser", "Why doesn’t HTTP/2 make a 5MB bundle fine?",
    "You still parse/compile/execute on the main thread.",
    "Multiplex helps many small files; it does not erase JS cost.",
    "H2 removes the need to code-split.",
    "H3 difference in one sentence.")
add("security", "security", "How does XSS show up in React apps?",
    "dangerouslySetInnerHTML, unsanitized markdown/HTML, javascript: href, plugin HTML.",
    "Encode by default; sanitize if you must render HTML; CSP depth.",
    "React makes XSS impossible.",
    "ADF/macros in Confluence-like apps.")
add("security", "security", "Why is localStorage a bad home for refresh tokens?",
    "Any XSS can read it.",
    "Prefer HttpOnly cookie / BFF session. localStorage is not ‘safer than cookies.’",
    "localStorage is XSS-proof because of origin isolation.",
    "What about memory-only access tokens?")
add("security", "security", "CORS vs CSRF?",
    "CORS is a browser read restriction. CSRF is cookie-auth mutation from another site.",
    "SameSite + CSRF token or custom header. CORS does not stop curl.",
    "Enabling CORS fixes CSRF.",
    "Does JWT in header get CSRF? (less; XSS still matters)")
add("security", "security", "CSP in one minute?",
    "Restrict script/frame/connect sources; nonce/hash over unsafe-inline.",
    "Defense in depth, not a substitute for encoding.",
    "CSP is only for images.",
    "How do plugins affect CSP?")
add("security", "security", "AuthN vs AuthZ on the frontend?",
    "Who you are vs what you can do. UI hides; server enforces.",
    "Capability cache is UX. Hidden route is not security.",
    "If the button is hidden, the API is safe.",
    "How do you batch capabilities?")
add("a11y", "architecture", "Why is a div-onClick not a button?",
    "No keyboard, no role, no form semantics, SR issues.",
    "Use button. If you fake it you must add role, tabindex, key handlers — worse.",
    "It’s fine if we add a click handler.",
    "Modal focus restore steps.")
add("a11y", "architecture", "How do you make a modal accessible?",
    "role=dialog, aria-modal, label, focus trap, escape, restore, inert background.",
    "One Modal primitive so features cannot forget.",
    "aria-modal alone is enough.",
    "What about nested dialogs?")
add("a11y", "architecture", "When is ARIA the wrong first move?",
    "When native HTML works (button, a, label, nav).",
    "Wrong ARIA lies to AT. First semantics, then names, then ARIA.",
    "Sprinkle aria-label on every div.",
    "Give a combobox example where ARIA is required.")
add("testing", "testing", "What should you not unit-test in React?",
    "React internals, third-party widgets, snapshots of everything, CSS pixels.",
    "Test user flows, invalidation, permissions, a11y labels, error fallbacks.",
    "100% coverage is the goal.",
    "Where does Playwright pay for itself?")
add("testing", "testing", "RTL philosophy in one sentence?",
    "Test the component the way a user uses it.",
    "Queries by role/label. Avoid getByClassName.",
    "RTL is a shallow renderer.",
    "How do you test a hook-only module?")
add("obs", "architecture", "How do you investigate random slowness?",
    "Define the metric, slice RUM, pull a trace, reproduce, fix the dominant bucket, verify.",
    "See Observability playbook. Plugins and issue size are common correlates on Jira-like pages.",
    "Add console.time everywhere in prod.",
    "What is a correlation ID good for?")
add("obs", "architecture", "Logs vs metrics vs traces?",
    "Events vs aggregates vs request stories.",
    "You need all three plus RUM for frontend. Sample logs; budget metrics; stitch traces with IDs.",
    "Metrics replace traces.",
    "Where does session replay fit (privacy)?")
add("offline", "architecture", "How does the frontend handle eventual consistency?",
    "Show source-of-truth, last-updated, retries, conflict UI.",
    "Optimistic overlay with rollback. Two tabs: version if-match + BroadcastChannel.",
    "The cache is always the truth.",
    "Design comment drafts offline.")
add("ssr", "react", "CSR vs SSR vs streaming — pick from constraints.",
    "CSR: simple, slower first HTML. SSR: HTML/LCP/SEO, hydrate cost. Stream: earlier bytes.",
    "Logged-in Jira-like often CSR+skeleton is fine. Marketing/docs may SSR.",
    "SSR is always faster.",
    "What is hydration mismatch?")
add("ssr", "react", "What is hydration?",
    "Attach listeners/state to server HTML.",
    "Mismatch if server/client markup differs (time, random, theme). Cost is JS on the main thread.",
    "Hydration is SSR.",
    "Why can hydration hurt INP?")
add("react", "react", "What is Suspense conceptually?",
    "A boundary that shows fallback while a child is not ready (throw thenable / lazy).",
    "Data Suspense needs a cache integration. Don’t invent it casually.",
    "Suspense is a spinner component.",
    "How does it interact with transitions?")
add("react", "react", "useTransition vs useDeferredValue?",
    "Transition marks a setState non-urgent. Deferred lags a value.",
    "Filter input: keep input urgent, list in a transition or deferred.",
    "They disable rendering.",
    "When is debounce still better?")
add("react", "react", "Why Strict Mode double-invokes render/effects in dev?",
    "To surface impure render and missing effect cleanup.",
    "Not a prod behavior. Fix purity and cleanup, don’t disable Strict Mode to hide bugs.",
    "React is broken in dev.",
    "What must an effect cleanup do?")
add("architecture", "architecture", "How do you design for independent team ownership without MFEs?",
    "Packages, CODEOWNERS, public APIs, release trains for kernel only, DS versioning.",
    "Deploy can stay one artifact. Ownership is social + module, not iframe.",
    "Ownership requires separate deploys.",
    "What belongs in the shared kernel?")
add("architecture", "architecture", "What is a port/adapter on the frontend?",
    "A TypeScript interface the feature depends on; infra implements it.",
    "issuesApi, analytics, flags. Tests fake ports. Hexagonal-lite, not 12 layers.",
    "It’s a Java thing only.",
    "Show a tiny port.")
add("performance", "performance", "Bundle 5MB — first three moves?",
    "Analyze composition; route/widget split; kill moment/unused icons; defer plugins.",
    "Coverage tab. Don’t guess. Set a budget in CI.",
    "Switch to a different bundler first.",
    "How do plugins inflate this at Atlassian-like scale?")
add("performance", "performance", "Search box lag — first three moves?",
    "Colocate input; debounce query; transition/virtualize list.",
    "Profiler: is the board in the same parent?",
    "useMemo the input value.",
    "Worker — when?")
add("security", "security", "Supply-chain risk in a SPA?",
    "Lockfile, audit, pin, review postinstall, least deps, verify DS/internal registry.",
    "Famous packages still get hijacked. Treat install as production.",
    "npm audit zero is sufficient forever.",
    "What about import maps / CDN React?")
add("testing", "testing", "Contract tests — why for frontends?",
    "API shape shared across teams; catch breaks before E2E.",
    "OpenAPI/Pact. Cheaper than full E2E for field renames.",
    "E2E replaces contracts.",
    "Who owns the contract?")
add("a11y", "architecture", "Live regions — when?",
    "Async status the user didn’t focus: search count, save failed, new chat message if viewing.",
    "polite vs assertive. Don’t announce every keystroke.",
    "Use assertive for everything so they hear it.",
    "Board card move announcement.")
add("react", "react", "Controlled vs uncontrolled inputs?",
    "Controlled: value + onChange from React. Uncontrolled: defaultValue + ref.",
    "Mixing causes the “can’t type” bug. Keys remount uncontrolled state.",
    "Always controlled everything including 20k cells.",
    "When is uncontrolled better?")
add("react", "react", "Why keys on a form stepper remount?",
    "You want fresh state per step; key={step} is intentional remount.",
    "Don’t do that if you want to preserve field values — lift state.",
    "Keys never remount.",
    "How do you preserve vs reset deliberately?")
add("architecture", "architecture", "REST vs GraphQL on the issue page?",
    "REST+BFF for partial compose is enough; GraphQL if clients need many shapes and you will staff the graph.",
    "GraphQL cache complexity vs overfetch. Neither is morally better.",
    "GraphQL is required for senior apps.",
    "How do you avoid a 2s GraphQL on first paint?")
add("architecture", "architecture", "WebSocket vs polling vs SSE?",
    "WS bidirectional; SSE server→client; poll simple and good enough for many UIs.",
    "Pick from frequency, infra, and degrade story. Always have a catch-up REST.",
    "Realtime means WebSocket or you’re junior.",
    "How do you catch up after a disconnect?")
add("architecture", "architecture", "Pagination vs infinite scroll?",
    "Pagination: shareable, a11y-simple. Infinite: engagement, memory and a11y cost.",
    "Virtualize either. Prefer page for admin tables; infinite for feeds with a load-more fallback.",
    "Infinite is always better UX.",
    "SEO implications?")
add("react", "react", "What does batching mean in React 18?",
    "Multiple setStates in the same event (and many async paths) share one render.",
    "You cannot assume an intermediate render. Use functional updates when depending on previous state.",
    "Each setState always paints.",
    "How do you force a flush? (flushSync — rare, dangerous)")
add("react", "react", "refs vs state?",
    "Ref changes do not render. State does.",
    "Timers, latest callbacks, DOM nodes → ref. Anything on screen → state.",
    "Refs are faster state.",
    "Is mutating ref.current during render safe? (no)")
add("performance", "performance", "Derived state — when is it a bug?",
    "Copying props into state and forgetting to sync.",
    "Prefer derive during render or key-remount. Don’t mirror server lists into useState.",
    "Always copy props to state for performance.",
    "Show the anti-pattern.")
add("browser", "browser", "What is INP measuring end-to-end?",
    "Input → event handlers → rendering → next paint.",
    "Not just your onClick. Includes React render and style/layout.",
    "INP is server time.",
    "How do you attribute INP to a component?")
add("security", "security", "Clickjacking mitigation?",
    "frame-ancestors / X-Frame-Options; not only JS frame-busting.",
    "Plugin platforms must allow some framing — allowlist.",
    "HTTPS prevents clickjacking.",
    "When must you allow framing?")
add("ds", "architecture", "What is a breaking change in a DS?",
    "Anything that forces product code or visual contract to change unexpectedly.",
    "Rename prop, drop variant, contrast fail, DOM structure Screen Readers depend on.",
    "Only TypeScript type breaks count.",
    "How do you ship one safely?")
add("obs", "architecture", "Why put correlation IDs on API calls?",
    "Stitch RUM session → BFF → services for one user action.",
    "Show the id in a “copy debug info” affordance for support.",
    "They’re only for backend.",
    "Who generates the id?")
add("architecture", "architecture", "How do you keep a 400-card board interactive?",
    "Virtualize, cheap cards, optimistic move, isolate drag overlay, don’t rerender body on presence.",
    "See Jira case study.",
    "Memo every card and you’re done.",
    "How do plugins interact with this budget?")
add("architecture", "architecture", "Design a kill switch for a bad frontend release.",
    "Flag default off; version.json; prompt reload; don’t wipe drafts.",
    "See kill-switch system-design card.",
    "Users will hard-refresh on their own.",
    "Service worker + old HTML?")
add("react", "react", "Explain concurrent rendering without saying ‘async React’.",
    "React may start a render, pause, discard, and commit a more urgent one.",
    "UI stays responsive. Your render must tolerate running twice.",
    "Concurrent means web workers render React.",
    "What is a lane?")
add("fetching", "architecture", "How do you paginate a 10k issue search?",
    "Cursor on the server; URL page/cursor; virtualize the window; don’t GET 10k.",
    "Offset pagination breaks when the set moves.",
    "Load all and filter client-side.",
    "Infinite vs numbered pages for JQL?")
add("a11y", "architecture", "Roving tabindex on a board?",
    "One tab stop per column/board; arrows move; tab leaves the widget.",
    "Don’t make 400 tab stops.",
    "tabIndex=0 on every card.",
    "How do you announce a move?")
add("testing", "testing", "Visual regression — where does it belong?",
    "DS primitives and a few product money screens, not every page every PR.",
    "Flaky screenshots are worse than none. Stabilize fonts/dates.",
    "Screenshot the whole app nightly as the main suite.",
    "Who reviews the diffs?")
add("architecture", "architecture", "Monorepo vs polyrepo for 20 teams?",
    "Monorepo helps atomic DS changes and affected CI; needs tooling. Polyrepo helps hard isolation; costs versioning.",
    "Not a moral choice. Atlassian-scale often monorepo + packages.",
    "Monorepo does not need CI discipline.",
    "How do you keep CI fast?")
add("react", "react", "Why not fetch in useEffect as the default architecture?",
    "Races, no cache, waterfall, Strict double-fetch in dev — use a cache library or framework fetch.",
    "Effects are for syncing with the world, not a query layer.",
    "useEffect fetch is the official pattern forever.",
    "What does a query library add?")
add("security", "security", "iframe sandbox for plugins — what do you still fear?",
    "postMessage to the wrong origin, resize loops, UX redress, escaped sandbox if misconfigured.",
    "Allowlist origins; tight API; CSP; budgets.",
    "sandbox attribute means zero risk.",
    "How do you theme a sandboxed plugin?")
add("performance", "performance", "Why timeupdate on a video should not setState 10Hz on a parent?",
    "It re-renders the tree 10 times a second.",
    "Keep time in a ref; rAF the scrubber only.",
    "React is fast enough.",
    "Same pattern: presence heartbeats, websocket ticks.")
add("architecture", "architecture", "What is an ADR and why say it in an interview?",
    "Context, decision, alternatives, consequences.",
    "Trains you to answer why, not we used Redux.",
    "ADRs are bureaucracy.",
    "Walk REST vs GraphQL as an ADR.")
add("react", "react", "Element vs Fiber vs DOM node?",
    "Description vs work unit vs pixel host.",
    "Elements are cheap and immutable. Fibers persist state. DOM is commit output.",
    "They are three names for the same thing.",
    "What is a host fiber vs a composite fiber?")
add("fetching", "architecture", "staleTime vs cacheTime/gcTime?",
    "staleTime: when data is fresh enough not to refetch. gcTime: when unused data leaves memory.",
    "Product vs memory. Don’t confuse them.",
    "They’re the same number.",
    "What would you pick for issue detail vs presence?")
add("browser", "browser", "Why can reading offsetHeight in a loop be disastrous?",
    "Forces layout each iteration (thrash).",
    "Batch writes, then read once.",
    "offsetHeight is a paint call.",
    "Name two other forcing APIs.")
add("architecture", "architecture", "How do you roll out a DS breaking change to 12 teams?",
    "Dual package or compat shim, lint, codemod, scheduled majors, office hours.",
    "Measure adoption. Don’t Friday-dump.",
    "Just bump major; they’ll deal.",
    "What if one team cannot move?")
add("react", "react", "What is useSyncExternalStore for?",
    "Subscribe to non-React stores without tearing.",
    "Must return immutable snapshots. Used by many store libraries.",
    "It’s a Redux hook.",
    "What is tearing?")
add("obs", "architecture", "How would you prove a plugin caused INP regressions?",
    "RUM slice by plugin set/version; disable flag; lab profile with/without; budget per slot.",
    "Don’t argue from one HAR.",
    "Ask the plugin vendor first and wait.",
    "What telemetry does the host need?")
add("architecture", "architecture", "BFF vs client N+1?",
    "BFF aggregates with timeouts and partial success; client N+1 is simple and slow.",
    "BFF can become a monolith — cache and team ownership required.",
    "Always add a BFF on day one of a todo app.",
    "How do you trace a BFF fanout?")
add("security", "security", "SameSite cookie attribute — what it does not do?",
    "Does not replace XSS protection or server authz; Lax still sends cookies on top-level GET.",
    "Know Strict/Lax/None+Secure. CSRF story still needs mutations protected.",
    "SameSite=Lax means no CSRF ever.",
    "Third-party cookies dying — impact on embeds?")
add("a11y", "architecture", "How do you treat a11y as architecture?",
    "Primitives own focus/semantics; lint; review; no custom widgets without DS.",
    "Not a QA ticket after feature-complete.",
    "Axe at the end is a strategy.",
    "What’s your Modal invariant?")
add("testing", "testing", "Why MSW over mocking fetch in each test?",
    "One network contract; tests look like the app; fewer brittle spies.",
    "Still not a replacement for a real E2E on money paths.",
    "Mock the hook, never the network.",
    "How do you test error states?")
add("react", "react", "Why fragments and no key on <> vs <Fragment key>?",
    "Short <> cannot take a key; use <Fragment key> in lists of groups.",
    "Common interview gotcha.",
    "Fragments don’t participate in reconciliation.",
    "When do you need a key on a fragment?")
add("performance", "performance", "Prefetch next route — risks?",
    "Wasted bandwidth, contention with LCP, stale prefetch.",
    "Intent-based (hover), idle, respect data saver.",
    "Prefetch everything on load.",
    "How do you prefetch data vs JS?")
add("architecture", "architecture", "How do you handle 20 open issue tabs in an SPA?",
    "Cap keep-alive, unmount hidden bodies, abort queries, bound caches.",
    "Memory is a feature requirement.",
    "Users should not open 20 tabs.",
    "Heap snapshot: what do you look for?")
add("react", "react", "Explain batching + functional updates together.",
    "If two setStates in one event depend on previous, use fn form because they share a render.",
    "setN(n+1); setN(n+1) → +1. setN(x=>x+1) twice → +2.",
    "Functional updates are only for async.",
    "Show the bug.")
add("network", "browser", "Private HTML vs hashed JS — cache headers?",
    "HTML: private, no-store or very short. JS/CSS hashed: public, max-age=31536000, immutable.",
    "Mixing these up either leaks or ships stale apps.",
    "Cache-Control: public on the app HTML is fine.",
    "How does a service worker complicate this?")
add("architecture", "architecture", "When is a modular monolith the wrong answer?",
    "True isolation (untrusted plugins), independent SLO/deploy that a module cannot give, or org constraints you cannot lint away.",
    "Then MFE/iframe with eyes open.",
    "Never — always monolith.",
    "How do you migrate incrementally?")
add("react", "react", "What is the purpose of keys besides lists?",
    "Force remount to reset state (key=id on a form), or disambiguate siblings.",
    "Use deliberately; don’t randomize.",
    "Only map() needs keys.",
    "Give a reset-form example.")
add("fetching", "architecture", "How do you design retries for POST /transition?",
    "Idempotency key; finite retries; don’t double-transition.",
    "GET retry is easier. POST needs a story.",
    "Retry all 500s blindly three times.",
    "What status codes are retryable?")
add("webperf", "performance", "CLS on a Jira-like page — typical causes?",
    "Late webfonts, banners, plugin resize, images without size, late ads/macros.",
    "Reserve space; tokens for banner height; plugin min-height.",
    "CLS is only ads.",
    "How do you debug a shift in Performance?")
add("architecture", "architecture", "How would you explain trade-offs like a senior?",
    "Constraint → options → rejected options → cost you accepted → how you’ll revisit.",
    "ADR spoken. No library-name answers.",
    "List 6 libraries you like.",
    "Do it for Redux vs Context now.")
add("react", "react", "Does memo compare deeply?",
    "Default shallow compare props.",
    "Custom compare is easy to get wrong and expensive. Prefer stable props.",
    "memo deep-equals automatically.",
    "What about children prop?")
add("security", "security", "OAuth token in the SPA — preferred pattern in 2026?",
    "BFF / confidential session cookie; short-lived access if any in memory.",
    "Implicit flow in the SPA is dated. PKCE with a BFF is common.",
    "Store the refresh token in localStorage and hope.",
    "What does the BFF add?")
add("obs", "architecture", "What frontend metric would you add for a board drag?",
    "Custom INP-like mark around drop-to-stable; plus API time; plus rollback rate.",
    "Vitals alone may miss the interaction.",
    "FPS forever in prod for everyone.",
    "How do you sample?")
add("architecture", "architecture", "Feature folder vs layer folder — one sentence each?",
    "Feature: change lives in one place, hard to share atoms. Layer: easy to find all hooks, every change touches five dirs.",
    "Default feature + small shared for 20 engineers.",
    "There is one correct folder structure.",
    "When do you extract an entity package?")
add("react", "react", "What breaks if you update state during render incorrectly?",
    "Infinite loops or discarded updates; allowed pattern is setState during render only to adjust state from props with a condition (rare).",
    "Prefer key remount or derive.",
    "setState in render is always illegal.",
    "Show the rare legal pattern vs the loop.")
add("browser", "browser", "Service worker caching HTML — danger?",
    "Users stuck on an old shell; hard to kill-switch.",
    "Versioned precache; skipWaiting strategy; never cache authenticated HTML casually.",
    "SW is just a faster CDN.",
    "How do you ship an emergency SW update?")
add("testing", "testing", "How do you test a virtualized list?",
    "Drive scroll in RTL/Playwright; assert visible rows; don’t expect all 20k nodes.",
    "Unit-test the window math if you wrote it.",
    "snapshot the whole list.",
    "A11y tests for rowcount?")
add("architecture", "architecture", "How do you share types between 12 frontend packages?",
    "A small entities/types package or generated OpenAPI types; no god types package that imports UI.",
    "Generate from the API to avoid drift.",
    "Copy-paste interfaces for independence.",
    "Who owns a breaking type change?")
add("react", "react", "Explain startTransition with a Jira filter example.",
    "Input stays urgent; filtering 10k issues is a transition so typing isn’t blocked.",
    "Pair with virtualization. Still debounce the network.",
    "startTransition makes the filter faster CPU-wise (it doesn’t; it deprioritizes).",
    "What does isPending buy you?")
add("performance", "performance", "When do Web Workers help a React app?",
    "CPU off main thread: parse, highlight, hash, huge JSON. Not for React render itself.",
    "Copy cost of postMessage matters. Don’t worker a 10-item sort.",
    "Put React DOM in a worker first thing.",
    "COMLink vs raw?")
add("a11y", "architecture", "Color-only status lozenges — what’s wrong?",
    "Fails contrast and fails non-color meaning.",
    "Icon + text + token. DS owns the pattern.",
    "We’re not a bank so it doesn’t matter.",
    "How do you test contrast in CI?")
add("architecture", "architecture", "How do you design an API client?",
    "One client: timeout, corr-id, 401 refresh, error mapping, abort. Features call resource methods.",
    "No fetch in components. Test the mapper.",
    "axios in every file.",
    "Where does retry live?")
add("react", "react", "Why is rendering treated as a calculation?",
    "So it can rerun, discard, and stay consistent with concurrent features.",
    "Side effects in the function body will lie under Strict Mode and transitions.",
    "Render is the same as commit.",
    "Where do you put the side effect instead?")
add("sysdesign", "architecture", "First four questions you’d ask for ‘design Jira’?",
    "Users and jobs-to-be-done; scale (cards, plugins); realtime need; mobile/a11y bar.",
    "Then URL, cache, virtualize, failures. Don’t draw k8s.",
    "Start with database schema.",
    "What’s the first diagram you draw?")
add("sysdesign", "architecture", "How do you timebox a 45-minute frontend design?",
    "5 clarify, 10 high-level, 15 deep (perf/state), 10 failures/sec/a11y, 5 trade-offs.",
    "Use the 15-step list as a checklist, not a script you rush.",
    "Spend 40 minutes on the component tree.",
    "What do you cut if you’re behind?")
add("react", "react", "Children as a prop and memo — what happens?",
    "inline <Child><span/></Child> creates new children each parent render; memo on Child often fails.",
    "Lift the static child or accept the rerender.",
    "memo always skips when children are JSX.",
    "How do you stabilize children?")
add("security", "security", "Why encode rather than ‘sanitize sometimes’ as default?",
    "Encoding is complete for text context; sanitizers are policies that rot.",
    "If you need HTML, sanitize with a maintained library and CSP.",
    "innerHTML is fine if we trust the API.",
    "What is the context (HTML vs attr vs JS)?")
add("architecture", "architecture", "What does ‘dependency direction’ mean in a React repo?",
    "UI may depend on domain; domain may not import React components. Features don’t import features.",
    "Cycles are the smell. Lint them.",
    "All imports are fine if types check.",
    "How do two features communicate?")
add("obs", "architecture", "Session replay — what do you worry about?",
    "PII, secrets in DOM, performance of the recorder, consent.",
    "Mask inputs; sample; legal review. Still not a substitute for traces.",
    "Record everything at 100%.",
    "When is replay the wrong tool?")
add("react", "react", "Explain useId and why it matters for a11y/SSR.",
    "Stable unique ids for label/input across server and client.",
    "Don’t Math.random() ids if you hydrate.",
    "useId is a CSS hook.",
    "Multiple components needing several ids?")
add("performance", "performance", "What is a performance budget?",
    "A number in CI (JS kb, LCP, INP) that fails the build.",
    "Without a budget, the bundle only grows. Product + eng own it.",
    "Budgets are for mobile games.",
    "What would you set for an issue view?")
add("architecture", "architecture", "How do you handle environment config for many realms?",
    "Runtime config endpoint or per-realm inject; don’t bake unchangeable URLs into a single immutable hash you cannot retarget.",
    "Public env vs secrets (secrets never in the SPA).",
    "One .env for all clouds.",
    "How do you rotate an API host?")


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
<section class="block" id="feq" data-search="React Frontend Interview Question Bank" data-stype="Section">
  <p class="kicker">{len(Q)} questions</p>
  <h2 class="section-title">React / Frontend Interview Question Bank</h2>
  <p class="lede">Answer standing up. Then reveal. Mark complete only if you could teach the short answer. All items are practice questions.</p>
  <div class="tabs" data-tabs="feq">
    <button type="button" class="tab active" data-tab="all">All ({len(Q)})</button>
    <button type="button" class="tab" data-tab="react">react-ish</button>
    <button type="button" class="tab" data-tab="architecture">architecture</button>
    <button type="button" class="tab" data-tab="performance">performance</button>
    <button type="button" class="tab" data-tab="security">security</button>
  </div>
  {''.join(blocks)}
</section>
'''
