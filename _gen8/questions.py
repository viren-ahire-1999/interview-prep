from util import esc, code

Q = []


def add(level, cat, q, short, deep, miss, follow, snippet=""):
    Q.append(dict(level=level, cat=cat, q=q, short=short, deep=deep, miss=miss, follow=follow, snippet=snippet))


add("plugin", "console", "What is an OpenShift console dynamic plugin?",
    "A Webpack 5 federated bundle the console loads at runtime, registered with a ConsolePlugin CR.",
    "You are not shipping a second SPA. Nav, pages, and tabs are console-extensions. Admins enable the plugin on the console Operator spec.plugins list.",
    "It is an iframe of Grafana.",
    "Where do proxy routes for Loki live?")
add("plugin", "console", "Why does a plugin declare spec.proxy?",
    "So the console backend can reach in-cluster services (Loki, Tempo, Korrel8r) with TLS and optional user token.",
    "The browser must not CORS-hack cluster IPs. Default is HTTPS plus the service CA. Several plugins add a small Go server to serve assets and proxy.",
    "proxy is only for external CDNs.",
    "What URL prefix does the console expose for plugin proxies?")
add("plugin", "console", "What is a UIPlugin CR for?",
    "Cluster Observability Operator watches it and deploys the matching Observe UI (and backends) for you.",
    "Example: type Monitoring with perses.enabled installs Perses wiring. You still need the plugin name on the Console spec if GitOps owns it.",
    "UIPlugin replaces ConsolePlugin.",
    "What happens if GitOps Console spec omits the plugin name?")
add("plugin", "console", "Why Webpack 5 and Yarn, not Vite, for these plugins?",
    "The console’s module federation contract is Webpack 5. The template and sibling plugins are Yarn.",
    "Vite can be a fine app bundler elsewhere. Here, mismatch means the remote entry never loads. Follow the template until you have a reason and a reviewer.",
    "Any bundler is fine if the JS is valid.",
    "What file lists exposed modules for federation?")
add("plugin", "console", "Why must plugins not import PatternFly CSS?",
    "The console already loads PF. A second copy fights theme (including dark/light) and future PF upgrades.",
    "Prefix custom classes with the plugin name. Avoid element selectors that leak. Use PF React components and CSS variables.",
    "Importing @patternfly/patternfly makes it look more ‘official’.",
    "What OpenShift version moved the console to PatternFly 6?")
add("patternfly", "ui", "What does PatternFly 6 change for a plugin author?",
    "OCP 4.19+ console is PF 6. New plugins should target PF 6, not PF 4/5 or Tailwind.",
    "Use PF components the console already uses (Toolbar, Pagination, EmptyState). Accessibility and theme come with them.",
    "PF is optional if your charts look modern.",
    "Name a review comment you would leave on a custom div that is already a PF component.")
add("patternfly", "ui", "What is an accessibility miss that will fail a senior review?",
    "Color-only charts, no keyboard path through the toolbar, unlabeled icon buttons, missing live region on query failure.",
    "WCAG is in the job. axe plus a keyboard pass. Name/role/value on custom widgets. i18n keys — hard-coded English in a header is a block.",
    "a11y is a nice-to-have after GA.",
    "How would you announce ‘query timed out’ to a screen reader?")
add("signals", "domain", "When do you start with logs vs metrics vs traces?",
    "Logs: a specific event (crash, 401). Metrics: aggregates (error rate, p99). Traces: one request across services.",
    "CrashLoop → logs, then restart metrics. High p99 → metrics then trace. Auth failures → logs plus trace attributes.",
    "Always open traces first because they are richest.",
    "What do you open if ‘everything is on fire’?")
add("signals", "domain", "Why is a high-cardinality label a UI bug as well as a backend bug?",
    "The chart invites unbounded series; Prometheus and the browser both melt.",
    "Do not offer user-id as a PromQL group-by. Cap series. Warn. Prefer recording rules for expensive queries.",
    "The UI should run whatever query the user typed.",
    "How do you abort work when the time picker moves?")
add("query", "promql", "rate() vs irate() — when is rate() the default?",
    "rate() averages over the range; use it for graphs and SLOs. irate() uses the last two points — spiky, for instant troubleshooting.",
    "Counters need increase/rate, not a raw gauge plot. histogram_quantile needs a histogram. by/without must match the question.",
    "irate is always more accurate.",
    "Write PromQL for 5xx ratio without grouping by user.")
add("query", "logql", "What is a LogQL stream selector vs a line filter?",
    "Selector picks streams (labels). Line filter then greps the payload. JSON unpack is after that.",
    "The logging plugin schema switch (viaq vs OTel) changes field names. Inventing {app=} on the wrong schema returns empty, not an error you can see.",
    "LogQL is grep on every node disk.",
    "Why might a filter that worked last year return nothing after OTel migration?")
add("query", "traceql", "What is TraceQL for?",
    "Find traces in Tempo by service, duration, status, attributes — then open a waterfall.",
    "OTel semantic conventions (service.name, k8s, http) are the join keys with metrics and logs. Exemplars can jump metric → trace.",
    "Jaeger is the current OpenShift tracing UI.",
    "When is a trace the wrong first click?")
add("perses", "dashboards", "Why Perses instead of ‘just Grafana’ on this stack?",
    "Dashboards and datasources are namespace-scoped CRs — RBAC and GitOps. COO wires Observe → Dashboards (Perses).",
    "Grafana import exists as a migration. Visualization direction is Perses + PatternFly theming in monitoring-plugin, not a new Grafana plugin career.",
    "Perses is a Grafana fork you must re-skin by hand.",
    "Where does a Perses dashboard live as an object?")
add("korrel8r", "correlation", "What does Korrel8r do for the troubleshooting panel?",
    "Rules connect alerts, metrics, logs, pods, netflows. The panel draws a graph and maps clicks to console URLs.",
    "If Logging is missing, log nodes will not be useful. URL maps need unit tests — a pretty graph with a 404 is a silent product bug.",
    "Korrel8r is a replacement for Prometheus.",
    "What repo owns the OpenShift URL mapping?")
add("ops", "cmo", "CMO vs COO in one minute.",
    "CMO is the default in-cluster Prometheus stack. COO is the meta-operator that adds optional Observe UIs, Perses, incidents, ACM wiring.",
    "Users still live under Observe. COO installs plugins from UIPlugin. CMO still answers ‘is cluster monitoring on?’",
    "COO replaced Prometheus.",
    "Which operator do you talk to if Perses is missing?")
add("ops", "gitops", "A plugin was enabled yesterday and is gone today. First question?",
    "Does GitOps own the Console CR? If yes, the name must be in git spec.plugins.",
    "A UI toggle without git is a race. Looks like a frontend regression. Check operators and Console spec before Webpack.",
    "Always a bad webpack build.",
    "Where do you look besides the plugin Deployment?")
add("senior", "lead", "What does ‘lead the UI’ mean here if you are not rewriting the console?",
    "Propose plugin boundaries, proxies, feature flags, and PF patterns — then land them upstream.",
    "You sit between signal teams, PM, and UX. Empty states and RBAC-aware lists are the product. A new SPA is usually the wrong architecture.",
    "Lead means pick the chart library.",
    "What artifact would you write before week 6?")
add("senior", "upstream", "What does ‘own it through upstream’ imply for a PR?",
    "The feature lands on GitHub first (DCO sign-off, OWNERS), then in the operator that installs it.",
    "Downstream-only patches surprise the next rebase. Know backport norms. Tiny docs/test PRs teach the machine before a large UI change.",
    "Ship only on the internal fork.",
    "What is Signed-off-by for?")
add("senior", "review", "Name three review comments that are senior, not style nits.",
    "PF misuse, unbounded fetch/cardinality, missing i18n or a11y, proxy vs hardcoded service, GitOps Console spec.",
    "Lint is table stakes. You catch silent no-ops: URL maps, feature flags, empty/error/partial query states.",
    "Rename a variable and approve.",
    "What would you block a merge for on a chart PR?")
add("plugin", "i18n", "Why are hard-coded English strings a review block?",
    "Console plugins are translated with react-i18next. English in a header skips that pipeline.",
    "Keys live with the plugin. You will see this on every sibling repo. Treat it as part of Done.",
    "English-only is fine for an internal plugin.",
    "Where do you look for existing keys before adding a new one?")
add("signals", "incidents", "What is the incidents surface for?",
    "Group alert bursts into a timeline so humans are not staring at 4000 raw alerts.",
    "It is a COO cluster-health feature, not a replacement for Alertmanager. Start here when ‘everything is on fire.’",
    "Incidents replace Prometheus rules.",
    "When do you still open Alertmanager / metrics?")
add("query", "otel", "What OpenTelemetry pieces should a UI engineer actually know?",
    "Semantic conventions, collector as the pipeline, Tempo as the store, exemplars as metric→trace jumps.",
    "You do not need to write the collector config on day 1. You do need to know why service.name is the join key and why Jaeger is legacy talk.",
    "OTel is a React library.",
    "Name one attribute you would show on a trace search row.")
add("perses", "grafana", "How should you talk about Grafana in this codebase?",
    "Import path and migration story. Do not become a Grafana plugin author as the plan.",
    "Perses is the Kubernetes-native board. Grafana JSON in is a bridge. Know that the conversation exists.",
    "Grafana is the Observe dashboards page.",
    "What object type would you GitOps instead of a Grafana folder?")
add("korrel8r", "ux", "Why can a Korrel8r graph look ‘done’ and still be a P1?",
    "Clicks must land on the right Observe page with the right query. Wrong href is silent.",
    "Extensive URL-map tests exist for a reason. Missing sibling plugins (logging) need honest empty copy.",
    "If the graph renders, the product works.",
    "What would you test besides snapshotting SVG positions?")


def feq() -> str:
    blocks = []
    for i, item in enumerate(Q, 1):
        snip = code("text", item["snippet"]) if item["snippet"] else ""
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
    <p><b>Follow-up.</b> {item["follow"]}</p>
  </div>
</article>''')
    return f'''
<section class="block" id="feq" data-search="Observe UI interview questions" data-stype="Section">
  <p class="kicker">{len(Q)} questions</p>
  <h2 class="section-title">Q&amp;A</h2>
  <p class="lede">Answer standing up. Mark complete only if you can teach the short answer. Practice items — not official company lists.</p>
  <div class="tabs" data-tabs="feq">
    <button type="button" class="tab active" data-tab="all">All ({len(Q)})</button>
    <button type="button" class="tab" data-tab="plugin">plugin</button>
    <button type="button" class="tab" data-tab="patternfly">patternfly</button>
    <button type="button" class="tab" data-tab="signals">signals</button>
    <button type="button" class="tab" data-tab="query">query</button>
    <button type="button" class="tab" data-tab="perses">perses</button>
    <button type="button" class="tab" data-tab="korrel8r">korrel8r</button>
    <button type="button" class="tab" data-tab="ops">ops</button>
    <button type="button" class="tab" data-tab="senior">senior</button>
  </div>
  {''.join(blocks)}
</section>
'''
