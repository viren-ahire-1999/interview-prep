from util import code, topic, diagram, callout


def browser_and_web() -> str:
    return f'''
<section class="block" id="browser" data-search="Browser Architecture critical rendering path" data-stype="Section" data-cat="browser">
  <p class="kicker">Host</p>
  <h2 class="section-title">Browser Architecture</h2>
  {topic("br-crp", "From URL to pixels", "DNS TCP TLS HTML DOM CSSOM layout paint", "Browser", f'''
  {diagram('''URL
 -> DNS
 -> TCP + TLS
 -> HTTP request / response
 -> HTML bytes
 -> tokenizer / parser  --> DOM
 -> CSS (blocking)      --> CSSOM
 -> DOM + CSSOM         --> render tree
 -> layout (reflow)
 -> paint
 -> composite (GPU layers)
 JS can block parse (sync scripts) or run after (defer/module)
 rAF / input sit between tasks, not between microtasks''')}
  <p><b>Critical rendering path:</b> anything that delays first paint or LCP: TTFB, render-blocking CSS, sync JS, late hero image, font-display:block. <b>preload</b> the LCP image and critical font. <b>prefetch</b> the next route. <b>lazy</b> below-the-fold and non-critical JS. Resource hints are not magic if the main thread is busy.</p>
  <p>Priorities: browsers now have Fetch Priority. Mark the LCP image high; mark analytics low. HTTP/2 multiplexing does not save you from 400KB of unused JS.</p>
  ''', "topics")}
</section>
<section class="block" id="webperf" data-search="Web Performance Core Web Vitals LCP INP CLS" data-stype="Section" data-cat="performance">
  <p class="kicker">Vitals</p>
  <h2 class="section-title">Web Performance</h2>
  {topic("wp-vitals", "Core Web Vitals as decisions", "LCP INP CLS TTFB long tasks", "Performance", f'''
  <table>
    <tr><th>Metric</th><th>What the user felt</th><th>Engineering lever</th></tr>
    <tr><td>LCP</td><td>Main content appeared</td><td>TTFB, hero image/CSS, don’t hide text, SSR/stream if it helps</td></tr>
    <tr><td>INP</td><td>Click/key felt delayed</td><td>Short event handlers, break long tasks, virtualize, transitions</td></tr>
    <tr><td>CLS</td><td>Layout jumped</td><td>Size attributes, reserve space, no late webfonts, no ads shoving content</td></tr>
    <tr><td>TTFB</td><td>Server/edge slowness</td><td>CDN, cache, SSR budget, avoid mega GraphQL on first byte</td></tr>
    <tr><td>FCP</td><td>Something painted</td><td>Critical CSS, don’t block on fat JS</td></tr>
  </table>
  <p>TTI is less official now; treat “time until the primary control works” as INP + hydration story. Long tasks &gt; 50ms on the main thread are the usual INP villain in React SPAs.</p>
  ''', "topics")}
</section>
<section class="block" id="network" data-search="Networking Caching HTTP CDN ETag" data-stype="Section" data-cat="browser">
  <p class="kicker">Wire</p>
  <h2 class="section-title">Networking &amp; Caching</h2>
  {topic("net-cache", "HTTP versions and cache layers", "HTTP/2 Cache-Control ETag stale-while-revalidate", "Networking", f'''
  <p>HTTP/1.1: few connections, head-of-line blocking. HTTP/2: multiplex on one TLS connection (still HOL at TCP). HTTP/3/QUIC: better loss recovery. You still pay TLS and TTFB. CDNs terminate TLS close to the user and cache GET/HEAD at the edge.</p>
  <p>Compression: Brotli for static text; Gzip fallback. Don’t compress already-compressed images.</p>
  <table>
    <tr><th>Layer</th><th>Good for</th><th>Invalidation</th></tr>
    <tr><td>Browser cache (Cache-Control, ETag)</td><td>Hashed assets: immutable, 1y</td><td>Change the filename/hash</td></tr>
    <tr><td>CDN</td><td>Public GETs, images</td><td>Purge by tag or hash</td></tr>
    <tr><td>Service worker</td><td>Offline, app-shell</td><td>Precache revision; careful with HTML</td></tr>
    <tr><td>App / TanStack cache</td><td>User-specific JSON</td><td>Mutation invalidation</td></tr>
    <tr><td>Server Redis (concept)</td><td>Shared computed payloads</td><td>TTL + explicit bust</td></tr>
  </table>
  <p><code>Cache-Control: public, max-age=60, stale-while-revalidate=600</code> — serve stale, refresh in background. <code>ETag</code> + <code>If-None-Match</code> → 304. Private, cookie-varying HTML should be <code>private, no-store</code> or very short TTL.</p>
  <p>Invalidation is the hard part: time-based (simple, stale), event-based (precise, racy), versioned URLs (best for assets). You cannot have “instant global consistency” and “99% cache hit” without a story.</p>
  ''', "topics")}
</section>
<section class="block" id="offline" data-search="Offline first service workers retry optimistic" data-stype="Section" data-cat="architecture">
  <p class="kicker">Resilience</p>
  <h2 class="section-title">Offline / Resilience</h2>
  {topic("off-1", "Degraded and offline-first", "service worker backoff conflict resolution", "Resilience", f'''
  <p>Offline-first means the UI works on a cache and a queue, not that every Atlassian product must work on a plane. Confluence drafts: yes. Jira board realtime: degrade to “last known + reconnect.”</p>
  <ul class="tight">
    <li>Service worker: cache app shell; never blindly cache authenticated HTML.</li>
    <li>Retry GET with exponential backoff + jitter. Mutations: idempotency key, finite retries, dead-letter UI.</li>
    <li>Request dedupe (in-flight map) plus optimistic UI when rollback is cheap.</li>
    <li>Eventual consistency: show “saved locally” vs “on server.” Two tabs: last-write-wins or merge (CRDT/OT only if you must).</li>
    <li>Graceful degradation: hide presence avatars; keep typing; disable drag if sync is down.</li>
  </ul>
  ''', "topics")}
</section>
'''


def design_mfe() -> str:
    return f'''
<section class="block" id="design-systems" data-search="Design Systems tokens theming versioning" data-stype="Section" data-cat="architecture">
  <p class="kicker">Multi-team UI</p>
  <h2 class="section-title">Design Systems</h2>
  {topic("ds-1", "Tokens, APIs, versioning, adoption", "design tokens breaking changes headless", "Design systems", f'''
  {diagram('''Foundations: color / space / type tokens
    -> primitives (Pressable, Text, FocusRing)
    -> composites (Button, Modal, Menu)
    -> product patterns (IssueLozenge)
Docs + a11y contract + visual regression
Package: @acme/ds  semver  + codemods for breaks''')}
  <p>Tokens are the language (not hex in 40 repos). Component APIs prefer composition. Theming via tokens + CSS variables, not a React context that re-renders the world. Accessibility is in the primitive (keyboard, roles), not a “phase 2” add-on.</p>
  <p>Versioning: treat the DS like a public API. Breaking a Button padding is a major. Provide a second major and a migration lint. Visual regression (Chromatic/Playwright screenshots) on primitives. Documentation is how 12 teams adopt without Slack archaeology.</p>
  <p>MUI vs custom vs headless (Radix/React Aria): buy primitives when a11y is hard (listbox, combobox); own tokens and product composites. A full custom DS is justified when brand + density + plugin theming (Atlassian-like) is the product.</p>
  <p>CSS architecture: CSS variables for tokens; avoid deep descendant selectors that leak across plugins. Shadow DOM only if you truly isolate third-party CSS.</p>
  <h4>Multi-team adoption (the hard part)</h4>
  <ul class="tight">
    <li><b>Package architecture:</b> tokens package (no React), primitives, composites, icons. Apps depend downward. Features do not import another feature’s CSS.</li>
    <li><b>Documentation:</b> do / don’t, a11y notes, token mapping. A DS without docs is a Sketch file in npm form.</li>
    <li><b>Testing:</b> unit on logic, RTL on keyboard, visual regression on primitives, axe in CI for the kitchen-sink page.</li>
    <li><b>Breaking changes:</b> major + codemod + dual-run. “Just change Button” is how you stall 12 teams.</li>
    <li><b>Theming:</b> CSS variables on <code>:root</code> / <code>[data-theme]</code>, not a React theme object that re-renders Jira.</li>
  </ul>
  <p>MUI / Chakra: fast start, theming escape hatches, you inherit their a11y and their bundle. Custom DS: justified when density, plugins, and brand <i>are</i> the product (Atlassian-shaped). Headless (React Aria / Radix) + your tokens is the usual senior compromise.</p>
  {callout("Practice: “Design a design system for 8 product teams.” Lead with tokens, versioning, a11y in primitives, and an RFC for kernel changes — not a component gallery screenshot.")}
  ''', "topics")}
</section>
<section class="block" id="mfe" data-search="Micro-frontends module federation" data-stype="Section" data-cat="architecture">
  <p class="kicker">Independence vs cost</p>
  <h2 class="section-title">Micro-frontends</h2>
  {topic("mfe-1", "When MFEs earn their complexity", "micro-frontends module federation shared dependencies", "Micro-frontends", f'''
  <p>MFEs exist to buy <b>independent deploy and team autonomy</b>. They cost duplicate runtime, shared-dep hell, inconsistent UX, and debugging across bundles. Atlassian-like plugin iframes are a form of isolation — not the same as “five webpack Module Federations on one issue page.”</p>
  <table>
    <tr><th></th><th>Monolith</th><th>Modular monolith</th><th>MFE</th></tr>
    <tr><td>Deploy</td><td>One</td><td>One</td><td>Many</td></tr>
    <tr><td>Consistency</td><td>Easy</td><td>Enforceable</td><td>Hard (DS + contracts)</td></tr>
    <tr><td>Perf</td><td>One optimize pass</td><td>Same</td><td>Duplicate React risk</td></tr>
    <tr><td>Failure isolation</td><td>Weak</td><td>Weak (one JS heap)</td><td>Better if iframe/separate origin</td></tr>
  </table>
  <p>Integration: build-time compose (simple, coupled releases) vs runtime (Module Federation, iframes, web components). Shared React must be a singleton or you break hooks. Auth: one session cookie at the parent; never N copies of JWT in localStorage. Routing: a parent router or path convention. State: pass IDs and events, do not share a Redux store across deployables.</p>
  {callout("Decision: start modular monolith. Split a deployable when a team is blocked on release cadence <i>and</i> the runtime contract is small (admin settings ≠ issue field). Refuse MFE as a resume-driven rewrite.")}
  <h4>Runtime details seniors get asked</h4>
  <ul class="tight">
    <li><b>Module Federation (concept):</b> a host loads remotes at runtime. You must singleton React (and usually the router / DS). Version skew of React = hook crashes. Treat shared deps as a compatibility contract, not “npm will work it out.”</li>
    <li><b>Build-time compose:</b> packages imported into one bundle. Independent <i>code</i>, one deploy. Cheaper than federation; not independent release.</li>
    <li><b>iframe plugins:</b> strongest isolation, worst integration (resize, a11y, theme, auth via postMessage). Correct for untrusted apps. Wrong for your own issue header.</li>
    <li><b>Communication:</b> custom events or a tiny typed bus of IDs. Do not share a Redux store across deployables — you have created a distributed monolith with extra latency.</li>
    <li><b>Auth:</b> parent session cookie; remotes call APIs with the same origin or a BFF. N copies of JWT in localStorage is an XSS farm.</li>
    <li><b>Performance cost:</b> duplicate copies of React/lodash, waterfalls of remoteEntry, layout shift when a remote loads late. Budget remotes like third-party scripts.</li>
  </ul>
  <p><b>When NOT to use MFEs:</b> one product, one domain object (Issue), one design language, teams that already share a weekly release. Split packages, not deploys.</p>
  ''', "topics")}
</section>
'''


def sec_a11y_test_obs() -> str:
    return f'''
<section class="block" id="security" data-search="Frontend Security XSS CSRF CORS CSP" data-stype="Section" data-cat="security">
  <p class="kicker">Defensive</p>
  <h2 class="section-title">Security</h2>
  <p class="lede">Examples stay at the level of attack <i>class</i> and mitigation. No exploit recipes.</p>
  {topic("sec-web", "Browser threat model for seniors", "XSS CSRF CORS CSP JWT cookies", "Security", f'''
  <table>
    <tr><th>Topic</th><th>What goes wrong</th><th>Mitigation</th><th>Misconception</th></tr>
    <tr><td>XSS</td><td>Untrusted HTML/JS runs as the user</td><td>Encode/text content; sanitize if HTML required; CSP as depth</td><td>“React prevents all XSS” (dangerouslySetInnerHTML, href, plugin HTML)</td></tr>
    <tr><td>CSRF</td><td>Browser sends cookies to your API from another origin</td><td>SameSite cookies; CSRF token on cookie-auth mutations; prefer custom header + SameSite</td><td>“JWT in localStorage means no CSRF” (and you bought XSS-theft instead)</td></tr>
    <tr><td>CORS</td><td>A browser restriction, not an access-control system</td><td>Least origins; no * with credentials</td><td>“CORS protects the server from curl”</td></tr>
    <tr><td>CSP</td><td>Limits script sources, frames, etc.</td><td>nonce/hash; forbid unsafe-inline over time</td><td>CSP replaces encoding</td></tr>
    <tr><td>Clickjacking</td><td>UI framed and overlaid</td><td>frame-ancestors; X-Frame-Options</td><td>Only banks care</td></tr>
    <tr><td>Cookies</td><td>Theft or CSRF</td><td>HttpOnly, Secure, SameSite=Lax/Strict as product allows</td><td>localStorage is “more secure”</td></tr>
    <tr><td>localStorage</td><td>Any XSS reads it</td><td>Don’t put refresh tokens there</td><td>“It’s origin-isolated so nobody can steal it”</td></tr>
    <tr><td>Session / OAuth / JWT</td><td>Confused deputy, long-lived tokens</td><td>BFF/session cookie; short access tokens; rotate refresh</td><td>JWT must live in the SPA forever</td></tr>
    <tr><td>AuthN vs AuthZ</td><td>UI hides a button</td><td>Server enforces; UI is UX</td><td>Hidden route is secure</td></tr>
    <tr><td>Supply chain</td><td>Compromised npm / lockfile</td><td>lockfile, audit, pin, least install, review postinstall</td><td>“We only use famous packages”</td></tr>
  </table>
  <p>Plugin platforms (Jira-like) add iframe sandboxing, tight postMessage origins, and CSP frame-src allowlists. Treat third-party JS as hostile.</p>
  ''', "topics")}
</section>
<section class="block" id="a11y" data-search="Accessibility WCAG focus ARIA" data-stype="Section" data-cat="architecture">
  <p class="kicker">Built-in, not bolted-on</p>
  <h2 class="section-title">Accessibility</h2>
  {topic("a11y-1", "Architecture of inclusive UI", "semantic HTML keyboard ARIA live regions", "Accessibility", f'''
  <p>WCAG is the bar (perceivable, operable, understandable, robust). Architecture means: primitives handle focus and semantics; features cannot ship a custom div-button; modals go through one Modal that traps focus and restores it.</p>
  {code("TypeScript", '''// BAD
<div onClick={onClose}>Close</div>
<div className="modal">...

// GOOD
<button type="button" onClick={onClose}>Close</button>
<div role="dialog" aria-modal="true" aria-labelledby="t" ref={dialogRef}>
  <h2 id="t">Edit issue</h2>
  ...
</div>
// On open: remember document.activeElement, focus first focusable.
// On close: restore. Trap Tab. Escape closes. Background inert.''')}
  <p>ARIA is a supplement when HTML cannot express the widget (combobox). Wrong ARIA is worse than none. Live regions announce async results (<code>aria-live="polite"</code> on search status). Forms: label, error tied with <code>aria-describedby</code>, do not rely on color alone.</p>
  ''', "topics")}
</section>
<section class="block" id="testing" data-search="Frontend Testing RTL Playwright pyramid" data-stype="Section" data-cat="testing">
  <p class="kicker">Risk vs cost</p>
  <h2 class="section-title">Testing</h2>
  {topic("test-1", "Strategy, not trophy coverage", "unit integration E2E visual contract", "Testing", f'''
  {diagram('''Many: unit (pure functions, mappers, flags)
   Some: component/RTL (user flows in a feature)
   Fewer: integration (MSW + page)
   Few: E2E Playwright (money paths: create issue, comment, transition)
   Targeted: visual regression on DS primitives
   Contract: OpenAPI/Pact for API shapes teams share''')}
  <p>React Testing Library: assert what the user sees / can do. Avoid snapshot-everything and enzyme-style internals. Jest/Vitest are runners. Playwright is for real browser paths; Cypress is the same job with a different runner — pick one. Do not E2E every tooltip.</p>
  <p><b>Do not test:</b> React itself, third-party Modal internals, pixel-perfect CSS (except DS visual tests), implementation details of useState. <b>Do test:</b> invalidation after mutation, permission-disabled submit, focus restore, error fallback, URL filter parse.</p>
  ''', "topics")}
</section>
<section class="block" id="observability" data-search="Observability RUM traces correlation" data-stype="Section" data-cat="architecture">
  <p class="kicker">See production</p>
  <h2 class="section-title">Observability</h2>
  {topic("obs-1", "Logs, metrics, traces, RUM", "error tracking session replay correlation IDs", "Observability", f'''
  <p>Frontend observability is how you debug “works on my machine” at 10M users. <b>Logs</b> (structured, sampled). <b>Metrics</b> (INP, API error rate, cache hit). <b>Traces</b> (click → fetch → downstream). <b>Error tracking</b> (stack + release). <b>Session replay</b> (privacy-reviewed). Correlation IDs: generate on the client or take from the edge; send on every API call; show in the support dialog.</p>
  <h4>Practice: “Users say the Jira issue page is randomly slow.”</h4>
  <ol>
    <li>Define slow (INP? LCP? a specific click? a tenant?).</li>
    <li>Slice RUM by browser, release, plugin count, issue size, region.</li>
    <li>Find a trace for a slow session; look at long tasks vs API p95 vs render.</li>
    <li>Check if a plugin iframe or a large ADF document correlates.</li>
    <li>Reproduce with Performance + React Profiler on a large fixture.</li>
    <li>Fix the dominant bucket (often: no virtualization, sync parse, waterfall).</li>
    <li>Ship a mark/measure around the interaction; verify the metric moves.</li>
  </ol>
  ''', "topics")}
</section>
'''
