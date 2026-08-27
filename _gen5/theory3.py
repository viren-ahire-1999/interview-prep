from util import topic, diagram, callout, code


def auth() -> str:
    t1 = topic("au-model", "The client never grants power",
               "auth session JWT cookie CSRF tenant permissions", "Theory", f'''
  <p>The browser shows buttons. The server decides. A hidden “Delete project” is UX, not security. Design both: hide what you know is forbidden, still handle 403 as a first-class state.</p>
  <table>
    <tr><th>Topic</th><th>Senior default</th></tr>
    <tr><td>Session</td><td>HttpOnly Secure SameSite cookie + CSRF strategy for cookie mutations</td></tr>
    <tr><td>SPA token in localStorage</td><td>Avoid — XSS reads it. Memory + refresh cookie is the usual adult story</td></tr>
    <tr><td>JWT in the client</td><td>Fine as a format on the wire; not a reason to skip revocation and tenant checks</td></tr>
    <tr><td>Tenant</td><td>Tenant id from the session, never from a query param the user can edit to see another cloud</td></tr>
  </table>
  {code("TypeScript", '''// UI may skip rendering, but every mutation still carries server authz
function IssueActions({ canTransition }: { canTransition: boolean }) {
  return canTransition ? <TransitionMenu /> : null;
}
// Server: 403 if the role cannot transition, even if someone forged the POST.''')}
  {callout("Export, search, and plugins are classic leak surfaces. “Can view issue” is not “can run JQL that returns the description in a plugin iframe.”")}
  ''', "topics")

    return f'''
<section class="block" id="auth" data-search="Auth permissions session tenant CSRF" data-stype="Section" data-cat="security">
  <p class="kicker">Trust boundary</p>
  <h2 class="section-title">Auth and permissions</h2>
  <p class="lede">Pretty 403s. Ugly if you trust the client.</p>
  {t1}
</section>
'''


def security() -> str:
    t1 = topic("sec-xss", "XSS is the frontend security interview",
               "XSS CSRF CSP dangerouslySetInnerHTML plugins", "Theory", f'''
  <p>React encodes text children. You still lose if you: <code>dangerouslySetInnerHTML</code>, markdown→HTML without a sanitizer, CSS <code>url()</code>, <code>javascript:</code> hrefs, open redirects, or <b>plugin HTML</b>.</p>
  <ul>
    <li><b>Encode</b> by default (text).</li>
    <li><b>Sanitize</b> if you must store HTML (allowlist).</li>
    <li><b>CSP</b> as depth (script-src, no unsafe-inline if you can, frame-ancestors).</li>
    <li><b>Sandbox iframes</b> for third-party apps (capability tokens, not the user’s session cookie if you can avoid it).</li>
  </ul>
  <p>CSRF: cookie-authenticated mutations need a token, custom header, or SameSite strategy you can explain. CORS is not CSRF protection. Clickjacking: <code>frame-ancestors</code>.</p>
  {code("TypeScript", '''// Never: title as HTML because a PM wanted bold
<h1>{issue.title}</h1>
// If you render stored markup:
<div dangerouslySetInnerHTML={{ __html: sanitize(storedHtml) }} />''')}
  {callout("Supply chain: lockfiles, least privilege in CI, don’t execute arbitrary package postinstall in prod builds. Mention it once; don’t spend the hour there unless they ask.")}
  ''', "topics")

    return f'''
<section class="block" id="security" data-search="Security XSS CSRF CSP plugins" data-stype="Section" data-cat="security">
  <p class="kicker">Defense</p>
  <h2 class="section-title">Security architecture</h2>
  <p class="lede">Encode, sanitize, CSP, sandbox. Unprompted in every design.</p>
  {t1}
</section>
'''


def a11y() -> str:
    t1 = topic("a11y-arch", "Accessibility is a keyboard and semantics design",
               "accessibility ARIA combobox grid focus POUR", "Theory", f'''
  <p>POUR: perceivable, operable, understandable, robust. In a design interview you specify:</p>
  <ul>
    <li>Semantic HTML first. ARIA when you invent a widget (combobox, grid, tabs).</li>
    <li>Focus: trap in modal, restore on close, skip link, don’t steal on every rerender.</li>
    <li>Keyboard model for the money path (board move, mention list, command palette).</li>
    <li>Live regions: polite for “issue moved,” assertive only for errors that block.</li>
    <li>Don’t use color alone for status. Don’t rely on drag without a keyboard alternative.</li>
  </ul>
  <p>Use the WAI-ARIA APG patterns by name: <b>combobox</b> for typeahead, <b>dialog</b> for modal, <b>grid</b> or a well-explained list for boards. “I’ll add aria-label later” is how seniors fail.</p>
  {diagram("""Board keyboard
  Tab → column
  Arrows → cards (roving tabindex)
  Space/Enter → open
  Cmd+arrows or menu → move
  Live region → “ISSUE-18 moved to Done”""")}
  ''', "topics")

    return f'''
<section class="block" id="a11y" data-search="Accessibility keyboard ARIA combobox" data-stype="Section" data-cat="architecture">
  <p class="kicker">Operable</p>
  <h2 class="section-title">Accessibility as architecture</h2>
  <p class="lede">Name the pattern. Own focus. Don’t leave drag as the only move.</p>
  {t1}
</section>
'''


def observability() -> str:
    t1 = topic("ob-rum", "If you cannot measure it you did not ship it",
               "RUM observability feature flags correlation id", "Theory", f'''
  <p>Week-one metrics for a surface: LCP of the money view, INP of the money click, error rate of the money mutation, plugin crash rate if you have plugins. Add a <b>correlation id</b> from click → API → log.</p>
  <p>Feature flags: boot the ones that affect chrome <b>before first paint</b> or reserve space. Experiments that swap layouts after hydrate cause CLS and broken a11y trees. Flags are architecture: they create versions of the product in the wild.</p>
  {callout("Session replay is optional and legal-sensitive. Never say “we record everything at 100%.” Sample, mask inputs, have a reason.")}
  {code("TypeScript", '''type BoardSli = {
  lcpIssueBoardMs: number;
  inpDragMs: number;
  transitionErrorRate: number;
  pluginInitFailures: number;
};''')}
  ''', "topics")

    return f'''
<section class="block" id="obs" data-search="Observability RUM flags metrics" data-stype="Section" data-cat="architecture">
  <p class="kicker">Signals</p>
  <h2 class="section-title">Observability and flags</h2>
  <p class="lede">Four numbers and a correlation id beat a vanity dashboard.</p>
  {t1}
</section>
'''


def mfe() -> str:
    t1 = topic("mfe-when", "Micro-frontends are a people-scale tool",
               "microfrontends module federation iframe plugins", "Theory", f'''
  <p>A modular monolith (packages, import rules, CI ownership) is the default. Runtime MFEs exist when <b>independent deploy</b> is worth the tax: duplicate React, CSS fights, shared nothing, performance.</p>
  <table>
    <tr><th>Integration</th><th>When</th><th>Tax</th></tr>
    <tr><td>Build-time packages</td><td>Same org, same release train OK</td><td>Lowest runtime cost</td></tr>
    <tr><td>iframe plugin host</td><td>Untrusted / other vendors</td><td>UX seams, postMessage, resize</td></tr>
    <tr><td>Module federation</td><td>You truly need independent deploy of JS</td><td>Version skew, shared deps, debugging</td></tr>
  </table>
  {diagram("""Need isolation from untrusted JS? → iframe + sandbox + cap
Need independent deploy of trusted teams? → maybe federation, measure
Need clearer folders? → packages, not MFE""")}
  <p>If someone says “we should federate everything,” answer with the tax and ask which team cannot share a release train. Often the answer is “none.”</p>
  ''', "topics")

    return f'''
<section class="block" id="mfe" data-search="Micro-frontends federation iframe plugins" data-stype="Section" data-cat="architecture">
  <p class="kicker">Integration</p>
  <h2 class="section-title">Micro-frontends</h2>
  <p class="lede">Default to packages. Iframe untrusted apps. Federation is a last resort you can defend.</p>
  {t1}
</section>
'''


def media() -> str:
    t1 = topic("md-up", "Upload, images, and not freezing the tab",
               "file upload worker image LCP media", "Theory", f'''
  <p>Multi-GB upload: chunk, resume, worker for hash, progress via rAF, don’t put the file in Redux. Direct-to-storage with a signed URL is normal; the browser must not stream 2GB through your Node BFF unless you have a reason.</p>
  <p>Images: width/height or aspect-ratio (CLS), srcset, priority on LCP image only, lazy the rest. Don’t decode 40 hero-sized images offscreen.</p>
  {code("TypeScript", '''async function hashInWorker(file: File): Promise<string> {
  const worker = new Worker(new URL("./hash.worker.ts", import.meta.url));
  return new Promise((resolve, reject) => {
    worker.onmessage = (e) => resolve(e.data.hash);
    worker.onerror = reject;
    worker.postMessage(file);
  });
}''')}
  ''', "topics")

    t2 = topic("md-search", "Search, feeds, and command palettes",
               "search feed command palette autocomplete", "Theory", f'''
  <p>Typeahead: debounce, min chars, abort, recents, <b>combobox</b> APG, authz on the server so private titles never leak. Command palette is typeahead plus actions (navigation, create). Same a11y pattern.</p>
  <p>Feeds: cursor pagination, virtualize, stable keys, restore scroll, skeleton that matches layout (CLS). Prefetch next page near the end. Don’t mount 2k cards.</p>
  ''', "topics")

    return f'''
<section class="block" id="media" data-search="Upload media search feed command palette" data-stype="Section" data-cat="performance">
  <p class="kicker">Heavy I/O</p>
  <h2 class="section-title">Media, upload, search</h2>
  <p class="lede">Workers for CPU. Cursors for feeds. Combobox for typeahead.</p>
  {t1}{t2}
</section>
'''
