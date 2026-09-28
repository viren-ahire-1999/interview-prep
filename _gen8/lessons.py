from util import topic, diagram, callout, code


def observe() -> str:
    t1 = topic("ob-menu", "Where users actually live: the Observe menu",
               "OpenShift Observe metrics logs traces Perses incidents", "Lesson",
               """
  <p>OpenShift’s admin console is a left-nav of cluster tasks. <b>Observe</b> is the observability product inside that console. Your work is not a separate URL. It is pages, tabs, and panels under Observe (and sometimes a drawer on a workload page). If it does not show up there, it does not exist for most users.</p>
  <p>Those pages are almost never compiled into the console binary. They are <b>dynamic plugins</b> enabled on the cluster. Some come with in-cluster monitoring by default. Others appear when the Cluster Observability Operator (COO) installs them from a UIPlugin.</p>
  """ + diagram("""Console (shell: nav, chrome, PF styles, auth)
   └── Observe
         ├── Metrics / alerting / targets     (Prometheus, Alertmanager, Thanos)
         ├── Dashboards (Perses)              (dashboard + datasource CRs)
         ├── Logs                             (LokiStack)
         ├── Traces                           (Tempo + OTel collector)
         ├── Troubleshooting panel            (Korrel8r graph)
         └── Incidents                        (grouped alert timeline)""") + """
  <p>Each row is a <b>different backend</b> and often a <b>different GitHub repo</b>. Your job is one journey across them: same time range, same namespace, a jump that does not dump the user’s brain.</p>
  """, "topics")

    t2 = topic("ob-cmo-coo", "CMO vs COO — two operators, one menu",
               "Cluster Monitoring Operator Cluster Observability Operator", "Lesson",
               """
  <p>Two names will show up in every architecture discussion. They are easy to mash together and wrong to mash together.</p>
  <table>
    <tr><th></th><th>Cluster Monitoring Operator (CMO)</th><th>Cluster Observability Operator (COO)</th></tr>
    <tr><td>Job</td><td>Default in-cluster Prometheus, Alertmanager, kube-state-metrics, node exporters — “is the cluster healthy?”</td><td>Optional Observe extras: extra UI plugins, Perses, incidents, ACM wiring, logging/tracing UI install paths</td></tr>
    <tr><td>Always there?</td><td>On typical OpenShift, yes (unless someone turned monitoring off)</td><td>No. Installed when the cluster wants the extra product</td></tr>
    <tr><td>How UI appears</td><td>Monitoring plugin features that talk to the in-cluster Prometheus stack</td><td><b>UIPlugin</b> CR: COO deploys plugin + companions (e.g. Korrel8r, Perses)</td></tr>
  </table>
  """ + callout("<b>Say this out loud.</b> CMO answers ‘is cluster monitoring running?’ COO answers ‘which Observe UIs did we opt into?’ Users still only see the Observe menu.") + """
  <p>If Perses is missing, you talk to COO / UIPlugin, not to Prometheus. If in-cluster metrics are missing, you talk to CMO. If the plugin name is missing from Console <code>spec.plugins</code>, you talk to GitOps / the console Operator — not Webpack.</p>
  """, "topics")

    t3 = topic("ob-surfaces", "What each surface is for (so you pick the right first click)",
               "metrics alerting logs traces incidents Perses targets", "Lesson",
               """
  <p><b>Metrics / graph.</b> Aggregates over time: CPU, request rate, error ratio, p99. First click when the question is “how much / how often / is it getting worse?” Backing store: Prometheus (single cluster) or Thanos (long-term / many clusters).</p>
  <p><b>Alerting / targets.</b> Alertmanager silences, firing alerts, scrape targets that are down. First click when something is already paging. Incidents (below) sit <i>above</i> a flood of raw alerts.</p>
  <p><b>Dashboards (Perses).</b> Saved boards as Kubernetes objects. First click when the team already agreed “this is our SLO board,” not when you are still exploring a crash.</p>
  <p><b>Logs.</b> A specific event: stack trace, CrashLoop last lines, an auth denial. First click when you need the payload, not the average.</p>
  <p><b>Traces.</b> One request across services. First click when you know (or can search) a slow or failed call. Waterfall, not a chart of averages.</p>
  <p><b>Troubleshooting panel.</b> “This alert exists — what else is related?” Korrel8r graph. First click when the user is lost between signals.</p>
  <p><b>Incidents.</b> Group alert bursts into a timeline so a human is not staring at 4,000 firing rows. First click when “everything is on fire.”</p>
  """ + diagram("""CrashLoop          → Logs (previous container), then restart metrics
High p99           → Metrics, then trace (exemplar or TraceQL)
Auth 401s          → Logs + trace attributes (user, route)
‘Cluster is down’  → Incidents / Alertmanager, not a custom Grafana""") + """
  <p>Public code to skim later: <code>openshift/monitoring-plugin</code>, <code>logging-view-plugin</code>, <code>distributed-tracing-console-plugin</code>, <code>troubleshooting-panel-console-plugin</code>, <code>rhobs/observability-operator</code>. The tutorials on this page are enough to read those READMEs without drowning.</p>
  """, "topics")
    return f'''
<section class="block" id="observe" data-search="Observe surfaces OpenShift console CMO COO" data-stype="Section">
  <p class="kicker">Product map · tutorial</p>
  <h2 class="section-title">Observe surfaces</h2>
  <p class="lede">Learn the menu, the two operators, and which surface is the right first click. Repos come after you can teach this without notes.</p>
  {t1}{t2}{t3}
</section>
'''


def plugins() -> str:
    t1 = topic("pl-fed", "Dynamic plugins: the console loads your JS at runtime",
               "Webpack 5 module federation remoteEntry console plugin", "Lesson",
               """
  <p>The OpenShift console is one React app. Teams cannot wait for a monolith release to add Observe pages. The solution is <b>Webpack 5 module federation</b>: the console (host) loads a <b>remoteEntry</b> file from your plugin at runtime and mounts the modules you exposed.</p>
  """ + diagram("""Your plugin build
  → dist/remoteEntry.js + chunks
  → HTTP server in the cluster (often a small Go binary)
Console (host) reads ConsolePlugin CR
  → fetches remoteEntry
  → executes your page inside the console chrome
You do not ship a second SPA. You do not iframe Grafana as the architecture.""") + """
  <p>That is why the template uses <b>Yarn + Webpack 5</b>, not Vite. Vite is a fine bundler for a standalone app. Here the contract is “federated remote the console already knows how to load.” Fighting it is a week of 404s on remoteEntry.</p>
  <p>Metadata the console reads from your package:</p>
  """ + code("JSON", '''{
  "name": "my-observe-plugin",
  "consolePlugin": {
    "displayName": "My Observe",
    "exposedModules": {
      "./MetricsPage": "./src/components/MetricsPage.tsx"
    }
  }
}''') + """
  <p><code>exposedModules</code> keys are what <code>console-extensions.json</code> will point at. The path is a Webpack module, not a URL route by itself.</p>
  """, "topics")

    t2 = topic("pl-ext", "console-extensions.json is your nav and routes",
               "console-extensions.json page nav tab plugin", "Lesson",
               """
  <p>The console does not import your router. You declare <b>extensions</b>: “put a nav item here,” “render this module at this path,” “add a tab on the pod page.” Shape (simplified teaching example — always match the template’s current types):</p>
  """ + code("JSON", '''[
  {
    "type": "console.navigation/href",
    "properties": {
      "id": "observe-my-metrics",
      "name": "My metrics",
      "href": "/observe/my-metrics",
      "perspective": "admin",
      "section": "observe-section"
    }
  },
  {
    "type": "console.page/route",
    "properties": {
      "path": "/observe/my-metrics",
      "component": { "$codeRef": "MetricsPage" }
    }
  }
]''') + """
  <p><code>$codeRef</code> must match an <code>exposedModules</code> key. If they disagree, the nav click is a blank page. That is the first thing to check after a “my page is empty” report.</p>
  <p>Other extension types you will see in sibling plugins: tabs on existing pages, dashboards, flags that hide a nav item unless COO or CMO is present. <b>Feature flags</b> are how one repo serves “CMO-only metrics” vs “COO Perses” without two codebases.</p>
  """ + callout("Read one real <code>console-extensions.json</code> in monitoring-plugin after this tutorial. Do not memorize every type. Memorize: nav, route, codeRef, flag."), "topics")

    t3 = topic("pl-cr", "ConsolePlugin CR: install contract, field by field",
               "ConsolePlugin CR spec.backend spec.proxy spec.plugins", "Lesson",
               """
  <p>A <b>ConsolePlugin</b> custom resource tells the console Operator: this plugin exists, here is the Service that serves its assets, here is what it may proxy to.</p>
  """ + code("YAML", '''apiVersion: console.openshift.io/v1
kind: ConsolePlugin
metadata:
  name: example-observe
spec:
  displayName: Example Observe
  backend:
    service:
      name: example-plugin
      namespace: example
      port: 9443
      basePath: /
  proxy:
    - alias: loki
      objectRef:
        name: loki
        namespace: openshift-logging
        kind: Service
        port: 8080
      authorization: UserToken
      caCertificate: default''') + """
  <ul>
    <li><code>metadata.name</code> is the name that must appear in Console <code>spec.plugins</code>.</li>
    <li><code>backend.service</code> is where <code>remoteEntry.js</code> is served (HTTPS, service CA).</li>
    <li><code>proxy</code> entries become console backend routes like <code>/api/proxy/plugin/example-observe/loki/...</code>. The browser never talks to Loki’s ClusterIP.</li>
    <li><code>authorization: UserToken</code> forwards the logged-in user’s token so RBAC applies. Impersonating cluster-admin from the plugin is a security bug.</li>
  </ul>
  """ + diagram("""Browser  →  console backend  /api/proxy/plugin/<plugin>/<alias>/...
                →  Service (Loki / Tempo / Korrel8r)
                TLS: service CA    Auth: user token
CORS hacks against ClusterIP are not the architecture.""") + """
  <p>Several Observe plugins ship a small <b>Go</b> server: static assets + sometimes extra proxy logic. You do not need to write Go on day 1. You do need to read one handler and know why HTTPS + service CA exists (the console will not fetch plaintext HTTP from a random pod).</p>
  """, "topics")

    t4 = topic("pl-enable", "Enabled on the cluster ≠ CR exists",
               "Console spec.plugins enable dynamic plugin GitOps", "Lesson",
               """
  <p>Two switches, both required:</p>
  <ol>
    <li>The <code>ConsolePlugin</code> object exists (and its Service is healthy).</li>
    <li>The cluster Console resource lists that name under <code>spec.plugins</code>.</li>
  </ol>
  <p>Admins can enable plugins in the UI. If GitOps owns Console, that click is undone on the next reconcile unless git is updated. COO’s <b>UIPlugin</b> is a third layer: it <i>deploys</i> the plugin + backends, but the Console list still has to include the name.</p>
  """ + code("YAML", '''apiVersion: observability.openshift.io/v1alpha1
kind: UIPlugin
metadata:
  name: monitoring
spec:
  type: Monitoring
  monitoring:
    perses:
      enabled: true''') + """
  <p>UIPlugin says “COO, install this Observe extra.” ConsolePlugin says “console, load this remote.” Console <code>spec.plugins</code> says “yes, actually enable it.” Mixing the three names in a standup is how you debug for a day in the wrong repo.</p>
  """, "topics")

    t5 = topic("pl-loop", "Local loop: template, Yarn, console-in-a-container",
               "console-plugin-template start-console.sh Yarn Webpack", "Lesson",
               """
  <p>The documented loop in <code>openshift/console-plugin-template</code> is:</p>
  <ol>
    <li>Clone the template. Keep Yarn + Webpack. Do not “just Vite it.”</li>
    <li>Install deps, start the plugin webpack-dev-server (it serves the federated build).</li>
    <li>Run the script that starts a <b>console container</b> pointed at your plugin URL (and usually at a real cluster API for k8s data).</li>
    <li>Open the console, enable the plugin if needed, hit your page.</li>
  </ol>
  """ + diagram("""yarn + webpack-dev-server   (your remoteEntry on localhost)
podman/docker console       (host app, loads your remote)
kubeconfig / oc             (API for lists, or a CRC cluster)
You are testing federation + PF, not a mocked iframe.""") + """
  <p>Blockers you should expect: podman vs Docker, Apple Silicon images, needing a cluster for anything beyond a static page, HTTPS mixed content. Write them down; do not stall the 30-day plan for three days on CRC. A static PF page in the template still teaches the contract.</p>
  """ + callout("Do not import PatternFly CSS in the plugin. The host already loaded PF. A second copy fights dark/light theme. Prefix any extra class with your plugin name. No element selectors on <code>body</code>."), "topics")
    return f'''
<section class="block" id="plugins" data-search="console dynamic plugins tutorial ConsolePlugin" data-stype="Section">
  <p class="kicker">Tutorial</p>
  <h2 class="section-title">Console plugins</h2>
  <p class="lede">Federation, extensions JSON, ConsolePlugin CR, proxy, enablement, local loop. After this section you should be able to walk a blank whiteboard through “how my page appears under Observe.”</p>
  {t1}{t2}{t3}{t4}{t5}
</section>
'''


def patternfly() -> str:
    t1 = topic("pf-why", "PatternFly 6 is the house look — not a suggestion",
               "PatternFly 6 OpenShift console design system", "Lesson",
               """
  <p>OpenShift 4.19 unified perspectives and moved the console to <b>PatternFly 6</b>. Console 4.22 is PF 6. New plugins target PF 6. If you ship Tailwind, Bootstrap, or a SaaS-dashboard CSS file, the page will look foreign, fight dark theme, and fail review.</p>
  <p>The <b>console already loads PF base styles and theme tokens</b> (including dark/light). Your plugin uses PF <b>React components</b> and CSS variables. If you <code>import '@patternfly/patternfly/patternfly.css'</code> (or any full PF CSS bundle) you double-load: fonts, resets, and tokens collide. That is a defect, not a shortcut.</p>
  """ + diagram("""Console host:  PF 6 CSS + theme (light/dark) + masthead
Your plugin:   @patternfly/react-core components
               optional: a few prefixed classes
Not allowed:   Tailwind CDN, Bootstrap, import PF CSS, restyle body""") + """
  <p>SDK wrappers exist for things the console already does (page headers, list pages). Prefer them when you are on a list-of-resources screen. When you are on an Observe chart page, PF <b>Toolbar</b> + <b>EmptyState</b> + <b>Alert</b> + <b>Spinner</b> are the usual skeleton.</p>
  """, "topics")

    t2 = topic("pf-build", "Build three screens the console already knows",
               "PatternFly Toolbar Table Pagination EmptyState Form", "Lesson",
               """
  <p>If you can build these without custom CSS soup, you can read monitoring-plugin:</p>
  <ol>
    <li><b>Filterable table</b> — Toolbar with SearchInput, Table, Pagination, EmptyState when rows.length === 0.</li>
    <li><b>Form</b> — Form, FormGroup, TextInput, Select, helper text, invalid state. Submit does not trap focus.</li>
    <li><b>Chart + table fallback</b> — a visual and a data table (a11y: charts are not the only representation).</li>
  </ol>
  """ + code("TSX", '''import {
  Toolbar, ToolbarContent, SearchInput,
  EmptyState, EmptyStateBody, PageSection,
} from "@patternfly/react-core";

export function AlertList({ rows, q, setQ }: Props) {
  const filtered = rows.filter((r) => r.name.includes(q));
  return (
    <PageSection>
      <Toolbar>
        <ToolbarContent>
          <SearchInput value={q} onChange={(_, v) => setQ(v)} aria-label="Filter alerts" />
        </ToolbarContent>
      </Toolbar>
      {filtered.length === 0 ? (
        <EmptyState titleText="No alerts">
          <EmptyStateBody>Firing alerts for this namespace will show up here.</EmptyStateBody>
        </EmptyState>
      ) : (
        <table className="pf-v6-c-table">{/* or PF Table composable */}</table>
      )}
    </PageSection>
  );
}''') + """
  <p>Class prefix: if you must add a class, <code>example-observe__foo</code>, never <code>.table</code> or <code>button</code>. Element selectors leak into the console chrome.</p>
  """ + callout("Senior review comment to practice: ‘This is a custom div that PF already has as Toolbar / Pagination / EmptyState. Use the component so we inherit a11y and theme.’"), "topics")

    t3 = topic("pf-a11y", "Accessibility is a ship gate, not a polish pass",
               "WCAG keyboard axe live region charts PatternFly", "Lesson",
               """
  <p>This job names accessibility. That means:</p>
  <ul>
    <li><b>Keyboard.</b> Tab order: time picker → filters → chart/table → row actions. No keyboard trap in the query bar.</li>
    <li><b>Name, role, value.</b> Icon-only buttons have <code>aria-label</code>. Custom widgets need a role. Do not reinvent a listbox.</li>
    <li><b>Charts are not color-only.</b> Pattern + label, or a table. Red vs green is insufficient.</li>
    <li><b>Failures are announced.</b> <code>aria-live="polite"</code> on “query timed out.” EmptyState title is a heading.</li>
    <li><b>Contrast</b> in both themes. PF tokens are the safe default; random hex is how you fail dark mode.</li>
  </ul>
  <p>Practice: axe DevTools on your three screens, then a keyboard-only pass with the mouse unplugged. Fix the first five issues. That is the bar, not a 100-page WCAG essay.</p>
  """, "topics")

    t4 = topic("pf-i18n", "Hard-coded English is a review block",
               "react-i18next console plugin i18n", "Lesson",
               """
  <p>Console plugins translate with <b>react-i18next</b>. Strings live in JSON locale files. A header that says <code>&lt;h1&gt;Alerts&lt;/h1&gt;</code> skips the pipeline and fails review on this team even if the English is perfect.</p>
  """ + code("TSX", '''import { useTranslation } from "react-i18next";

export function Title() {
  const { t } = useTranslation("plugin__example-observe");
  return <h1>{t("alerts.title")}</h1>;
}''') + """
  """ + code("JSON", '''{
  "alerts.title": "Alerts",
  "alerts.empty": "No alerts in this range"
}''') + """
  <p>Namespace names are plugin-specific (often <code>plugin__&lt;name&gt;</code>). Look up existing keys before adding a synonym. Interpolation for counts: <code>t("showing", { shown: 20, total: 4812 })</code> — do not concatenate sentences in code.</p>
  """, "topics")
    return f'''
<section class="block" id="patternfly" data-search="PatternFly 6 tutorial accessibility i18n" data-stype="Section">
  <p class="kicker">Tutorial</p>
  <h2 class="section-title">PatternFly 6</h2>
  <p class="lede">Why PF 6, why you must not import PF CSS, three screens to build, a11y as a gate, i18n as Done. Tailwind is a defect here, not a preference.</p>
  {t1}{t2}{t3}{t4}
</section>
'''


def signals() -> str:
    t1 = topic("sg-def", "Metric, log, trace — definitions you can teach",
               "metrics logs traces observability definitions", "Lesson",
               """
  <p>These words get used as synonyms in slides. They are not synonyms in the product.</p>
  <table>
    <tr><th>Signal</th><th>What one point means</th><th>Question it answers</th><th>Store (typical here)</th></tr>
    <tr><td>Metric</td><td>A number aggregated over a window (rate, gauge, histogram bucket)</td><td>How much / how often / is it worse?</td><td>Prometheus / Thanos</td></tr>
    <tr><td>Log</td><td>An event with a payload (string or JSON) at a timestamp</td><td>What exactly happened in this process?</td><td>Loki</td></tr>
    <tr><td>Trace</td><td>A tree of spans for one request or job</td><td>Where did this call spend time / fail?</td><td>Tempo</td></tr>
  </table>
  <p>A trace is <b>not</b> a better metric. You cannot graph SLO error ratio from one waterfall. A log is <b>not</b> a better trace — you will not reconstruct a 30-service call graph from grep. A metric will not give you the stack trace.</p>
  """ + diagram("""RED:  Rate  Error  Duration     →  metrics first
USE:  Utilization Saturation Errors →  metrics first
Crash / exception / message     →  logs first
This checkout is slow           →  traces first
Related to this alert?          →  Korrel8r / troubleshooting"""), "topics")

    t2 = topic("sg-journey", "One journey, not three dump pages",
               "observability jump time range filters correlation", "Lesson",
               """
  <p>Excellent Observe UI keeps <b>time range + namespace + cluster</b> while the user jumps. The join keys are boring on purpose:</p>
  <ul>
    <li>Metrics ↔ traces: <code>service.name</code>, exemplar trace id, HTTP route.</li>
    <li>Traces ↔ logs: <code>trace_id</code> / <code>traceId</code> on the log line (if the collector injected it), plus namespace + pod.</li>
    <li>Logs ↔ workload: pod name, namespace, container (previous container for CrashLoop).</li>
    <li>Alert → everything: alert labels (namespace, alertname, pod) into Korrel8r.</li>
  </ul>
  <p>If those labels were never written (bad instrumentation), the UI cannot invent them. Your collaboration with backend is “we need this attribute on the span / this label on the metric,” not a new SPA.</p>
  """ + callout("Cardinality: a metric label with unbounded values (user id) will melt Prometheus <i>and</i> the chart. The UI must not present ‘group by user’ as a friendly chip."), "topics")

    t3 = topic("sg-incidents", "When the cluster is on fire, do not open 4000 alerts",
               "incidents Alertmanager grouping Observe", "Lesson",
               """
  <p><b>Alertmanager</b> still fires alerts. The <b>incidents</b> surface (COO cluster-health analyzer) groups bursts into a timeline: fewer rows, a start/end, a component. It does not replace alerting rules. It replaces the human failure mode of staring at a wall of firing.</p>
  <p>What you must not hide when you group: the underlying alerts still exist; severity; “this incident is 3 alerts, not 1 outage.” Empty state: “no incidents in range” vs “analyzer not installed.”</p>
  """, "topics")
    return f'''
<section class="block" id="signals" data-search="metrics logs traces three signals tutorial" data-stype="Section">
  <p class="kicker">Tutorial</p>
  <h2 class="section-title">Three signals</h2>
  <p class="lede">Definitions, first-click rules, join keys, incidents vs raw alerts. Query languages in the next sections are how you implement this picture.</p>
  {t1}{t2}{t3}
</section>
'''


def perses() -> str:
    t1 = topic("pe-what", "Dashboards as Kubernetes objects, not a Grafana folder",
               "Perses dashboard CRD GitOps Observe", "Lesson",
               """
  <p><b>Perses</b> is an open-source dashboard app designed for cloud-native: dashboards and datasources are <b>namespace-scoped custom resources</b>. That matches RBAC (you can only see boards in namespaces you can get) and GitOps (the board is YAML in git, reviewable in a PR).</p>
  <p>On OpenShift, COO wires <b>Observe → Dashboards (Perses)</b> when the UIPlugin enables it. The monitoring plugin does PatternFly theming so Perses does not look like a foreign iframe theme.</p>
  """ + code("YAML", '''apiVersion: perses.dev/v1alpha1
kind: PersesDashboard
metadata:
  name: checkout-slo
  namespace: shop
spec:
  display:
    name: Checkout SLO
  duration: 6h
  # panels + queries live under spec (shape evolves — read the CRD)
---
apiVersion: perses.dev/v1alpha1
kind: PersesDatasource
metadata:
  name: prometheus
  namespace: shop
spec:
  plugin:
    kind: PrometheusDatasource
    spec:
      proxy:
        url: https://thanos-querier.openshift-monitoring.svc:9091''') + """
  <p>You do not need to memorize every panel JSON field. You need: <b>namespaced</b>, <b>RBAC-aware list</b>, empty state when CRD/COO is missing, and “this is the visualization direction.”</p>
  """, "topics")

    t2 = topic("pe-grafana", "Grafana import is a bridge, not a career",
               "Perses Grafana import migration", "Lesson",
               """
  <p>Teams have years of Grafana JSON. Perses can <b>import</b> that as a migration. Know the conversation: “we can bring board X across.” Do not become a Grafana plugin author as the 30-day plan — visualization energy is Perses + PF theming in monitoring-plugin.</p>
  <p>The editor in the console: create, rename, duplicate, edit panels. Datasources: Prometheus/Thanos, Loki, Tempo as documented for the version you target. If a datasource CR is missing, the board shows a configuration empty state, not a mysterious blank chart.</p>
  """ + callout("If you do one extra clone in week 3: <code>perses/perses</code> (or perses-dev). Create a dashboard as YAML. Import one Grafana JSON. That talk comes up constantly."), "topics")
    return f'''
<section class="block" id="perses" data-search="Perses tutorial dashboards as code" data-stype="Section">
  <p class="kicker">Tutorial</p>
  <h2 class="section-title">Perses</h2>
  <p class="lede">Why dashboards are CRs, how COO puts them under Observe, and how to talk about Grafana without making it the plan.</p>
  {t1}{t2}
</section>
'''


def korrel8r() -> str:
    t1 = topic("kr-engine", "Korrel8r is rules, not magic AI",
               "Korrel8r correlation engine domains rules", "Lesson",
               """
  <p><b>Korrel8r</b> is an open-source engine: given a starting object (an alert, a metric selector, a pod), <b>rules</b> produce related objects in other <b>domains</b> (metrics, logs, pods, netflows, alerts, traces — depending on what is installed). It is deterministic. It is not an LLM summarizing your cluster.</p>
  """ + diagram("""Start: Alert  {alertname=CrashLoop, namespace=shop, pod=checkout-7d}
  rules →  Log query for that pod
        →  Metric selector (restarts)
        →  Pod / ReplicaSet / Deployment
        →  maybe netflow, maybe trace
Each neighbour is a domain + a query string.""") + """
  <p>If Logging is not installed, log neighbours cannot be realized in the UI. The graph must not pretend they work. Missing plugin = honest copy, not a 404 on click.</p>
  """, "topics")

    t2 = topic("kr-panel", "The troubleshooting panel is a URL mapper with a graph",
               "troubleshooting panel console plugin URL map", "Lesson",
               """
  <p>The <b>troubleshooting panel</b> plugin calls Korrel8r, draws a graph, and on click opens the <b>right console URL</b> with the query filled in. That mapping (Korrel8r domain → Observe path + query string) is the product. If the logs plugin route changes and the map does not, the graph still looks pretty and the click is wrong. Silent P1.</p>
  """ + code("text", '''given:  node { domain: "log", query: "{namespace=shop,pod=checkout}" }
expect: /monitoring/logs?...   or whatever the current logging-view path is
test:   snapshot the href; fail CI if it drifts
missing logging plugin:  node shows “Logs UI not installed”, no 404''') + """
  <p>The panel repo calls out <b>unit tests</b> on those maps. Read them. When you change an Observe route, you are a consumer of this map even if you did not touch Korrel8r.</p>
  <p>Clone later: <code>korrel8r/korrel8r</code> (rules) and <code>openshift/troubleshooting-panel-console-plugin</code> (graph + hrefs). AGENTS.md in the panel repo is a short, useful read.</p>
  """ + callout("Unified UI workflows in the job description means this: alert → related signals without the user inventing three queries. The graph is the UX; the tests are the quality bar."), "topics")
    return f'''
<section class="block" id="korrel8r" data-search="Korrel8r tutorial troubleshooting panel" data-stype="Section">
  <p class="kicker">Tutorial</p>
  <h2 class="section-title">Correlation</h2>
  <p class="lede">Rules that connect signals, a panel that must not 404, tests on hrefs. This is the ‘unified workflow’ in concrete form.</p>
  {t1}{t2}
</section>
'''


def tools() -> str:
    t1 = topic("tl-core", "Install the daily loop, not a lab full of toys",
               "oc kubectl podman yarn CRC PatternFly axe DCO", "Lesson",
               """
  <p>You can finish the tutorials on this page without a cluster. You cannot finish the <i>job</i> without muscle memory on a few tools. Install this week:</p>
  <table>
    <tr><th>Tool</th><th>What you use it for</th><th>Done when</th></tr>
    <tr><td><code>oc</code> + kubectl</td><td>Plugins, CRs, logs, Console spec</td><td>You can <code>oc get consoleplugins</code> without looking it up</td></tr>
    <tr><td>podman or Docker</td><td>Template’s console container</td><td>The README loop starts or you wrote the blocker</td></tr>
    <tr><td>Yarn (classic, as repos use)</td><td>Plugin builds</td><td><code>yarn install</code> in the template works</td></tr>
    <tr><td>A cluster (CRC / sandbox / kind+Prometheus)</td><td>Real API, real PromQL</td><td>One cluster you are allowed to break</td></tr>
    <tr><td>PatternFly 6 React</td><td>House UI</td><td>Three screens, keyboard-only</td></tr>
    <tr><td>axe + keyboard</td><td>a11y bar</td><td>One audit with five fixes</td></tr>
    <tr><td>gh + DCO</td><td>Upstream PRs</td><td>You can produce Signed-off-by</td></tr>
  </table>
  """ + code("Bash", '''# DCO sign-off on every commit in many OpenShift repos
git commit -s -m "Fix typo in plugin README"

# oc daily
oc get consoleplugins
oc get console cluster -o jsonpath='{.spec.plugins[*]}'
oc logs -n example deploy/example-plugin --tail=50''') + """
  <p>Prometheus on kind (kube-prometheus-stack) is enough for PromQL practice if CRC is heavy. Loki + Tempo or the OpenTelemetry demo is enough for one three-signal journey. You do not need a production-like OpenShift on day 4.</p>
  """, "topics")

    t2 = topic("tl-dco", "Signed-off-by is a legal checkbox, not etiquette",
               "DCO Developer Certificate of Origin Signed-off-by", "Lesson",
               """
  <p>Many OpenShift / CNCF repos require the <b>Developer Certificate of Origin</b>. Your commit message includes <code>Signed-off-by: Your Name &lt;email&gt;</code>, usually via <code>git commit -s</code>. CI will NAK a PR without it. Set the email to the one GitHub knows.</p>
  <p><b>OWNERS</b> files list who can approve a directory. Read them before pinging random maintainers. A tiny docs or test PR is how you learn the machine before a 400-line UI change.</p>
  """, "topics")
    return f'''
<section class="block" id="tools" data-search="tools tutorial oc yarn DCO" data-stype="Section">
  <p class="kicker">Tutorial</p>
  <h2 class="section-title">Tools</h2>
  <p class="lede">What to install, what ‘done’ means, and why <code>git commit -s</code> matters before you open a real PR.</p>
  {t1}{t2}
</section>
'''


def repos() -> str:
    t1 = topic("rp-how", "How to read a plugin repo in one afternoon",
               "how to read console plugin repository", "Lesson",
               """
  <p>Do not clone eight repos and ‘read everything.’ For each repo, in order:</p>
  <ol>
    <li>README: how to run, what operator it needs, feature flags.</li>
    <li><code>package.json</code> → <code>consolePlugin.exposedModules</code>.</li>
    <li><code>console-extensions.json</code> (or generated equivalent): nav + routes.</li>
    <li>One page component: how it fetches (proxy URL? SDK?).</li>
    <li>If Go exists: one handler, one proxy target.</li>
    <li>Tests next to URL maps / feature flags.</li>
  </ol>
  <p>Write five lines in your notes: flags, proxy aliases, one PF pattern they use, one a11y or i18n detail, one thing you would ask in review.</p>
  """, "topics")

    t2 = topic("rp-list", "What each repo is for (so you pick one)",
               "monitoring-plugin logging-view-plugin tracing korrel8r perses", "Lesson",
               """
  <table>
    <tr><th>Repository</th><th>Learn from it</th></tr>
    <tr><td>openshift/console-plugin-template</td><td>The loop. Start here. Do not skip it for a ‘real’ plugin.</td></tr>
    <tr><td>openshift/monitoring-plugin</td><td>Biggest Observe UI: CMO vs COO flags, Perses theming, ACM alerts, incidents</td></tr>
    <tr><td>openshift/logging-view-plugin</td><td>Log list, Loki proxy, schema switch</td></tr>
    <tr><td>openshift/distributed-tracing-console-plugin</td><td>React + Go hybrid, Tempo proxy, trace UX</td></tr>
    <tr><td>openshift/troubleshooting-panel-console-plugin</td><td>Korrel8r graph, URL maps, tests you must not break</td></tr>
    <tr><td>rhobs/observability-operator</td><td>UIPlugin — how UI actually gets onto a cluster</td></tr>
    <tr><td>korrel8r/korrel8r</td><td>Rules, domains, queries</td></tr>
    <tr><td>perses/perses</td><td>Dashboard-as-code, query plugins</td></tr>
  </table>
  <p>Strong start: template loop + monitoring-plugin README + either logging or tracing. That is enough for week 2–3. You will not finish every repo and you should not try.</p>
  """, "topics")
    return f'''
<section class="block" id="repos" data-search="repos to clone tutorial OpenShift plugins" data-stype="Section">
  <p class="kicker">Tutorial</p>
  <h2 class="section-title">Repos to clone</h2>
  <p class="lede">A reading order, then a map of repos. The tutorials above are the prerequisite so the READMEs are not a wall of nouns.</p>
  {t1}{t2}
</section>
'''


def skip() -> str:
    t = topic("sk-no", "Do not over-invest — explicit skip list",
              "skip grafana plugins eBPF operator-sdk Jaeger", "Lesson",
              """
  <p>Time is the scarce resource. These look productive and are the wrong 30-day bets:</p>
  <ul>
    <li>Training a custom ML model for incidents.</li>
    <li>Replacing PatternFly or introducing Tailwind.</li>
    <li>Deep Grafana plugin authoring (visualization is moving to Perses).</li>
    <li>Full operator-SDK / writing CMO yourself.</li>
    <li>eBPF internals / becoming a kernel tracer.</li>
    <li>Becoming a Jaeger maintainer (Tempo + OTel is the UI path).</li>
  </ul>
  <p><b>Worth about four hours each, not a week:</b> network observability (netflows as a Korrel8r domain), incident grouping UX, Thanos query path for ACM, OpenShift 4.19 unified perspective. Internal CI/Konflux after you have a laptop and internal docs — not from this public file.</p>
  """, "topics")
    return f'''
<section class="block" id="skip" data-search="what not to study skip list" data-stype="Section">
  <p class="kicker">Focus</p>
  <h2 class="section-title">Do not over-invest</h2>
  {t}
</section>
'''


def senior() -> str:
    t1 = topic("sr-jd", "Map the job bullets to artifacts you can point at",
               "lead architect mentor upstream community Observe UI", "Lesson",
               """
  <table>
    <tr><th>Line</th><th>What excellence looks like by week 6</th></tr>
    <tr><td>Lead &amp; architect</td><td>You propose a plugin boundary, a proxy, a feature flag, and a PF pattern — not a new SPA</td></tr>
    <tr><td>Catalyze collaboration</td><td>You translate Loki tenant limits, Tempo retention, and PromQL cost into UI copy and empty states with PM/UX</td></tr>
    <tr><td>Own &amp; deliver upstream</td><td>Feature lands on GitHub first (DCO, OWNERS), then the operator that installs it</td></tr>
    <tr><td>Mentor &amp; influence</td><td>Reviews catch a11y, i18n, PF misuse, unbounded fetches, wrong href maps — not only lint</td></tr>
    <tr><td>Community</td><td>You can talk Perses, Korrel8r, or console plugins without opening slides</td></tr>
  </table>
  """, "topics")

    t2 = topic("sr-onepager", "Write the one-pager before day 30",
               "architecture one-pager plugins COO signals", "Lesson",
               """
  <p>One page, no branding, reuse in 1:1s:</p>
  <ol>
    <li>How a page gets to Observe (federation, ConsolePlugin, spec.plugins, UIPlugin/COO).</li>
    <li>CMO vs COO in five lines.</li>
    <li>Three signals + first-click rules + join keys.</li>
    <li>UX non-negotiables: time range, abort, four query states, PF + a11y + i18n.</li>
    <li>Upstream: DCO, GitHub first, GitOps Console spec.</li>
  </ol>
  <p>If you cannot write it without this file, you are not done — that is the gate, not a percent on a dashboard.</p>
  """, "topics")
    return f'''
<section class="block" id="senior" data-search="senior behaviors lead mentor upstream tutorial" data-stype="Section">
  <p class="kicker">How you show up</p>
  <h2 class="section-title">Senior behaviors</h2>
  {t1}{t2}
</section>
'''
