from util import topic, diagram, callout, code


def observe() -> str:
    t = topic("ob-menu", "The Observe menu is the product",
              "OpenShift Observe metrics logs traces Perses incidents", "Lesson",
              """
  <p>Users live under <b>Observe</b> in the OpenShift console. Your work shows up as pages, tabs, and panels there — installed as dynamic plugins, often by the Cluster Observability Operator (COO).</p>
  <table>
    <tr><th>Surface</th><th>Job</th><th>Typical backend</th></tr>
    <tr><td>Metrics / Alerting / Targets</td><td>In-cluster Prometheus; multi-cluster alerts</td><td>Cluster Monitoring Operator, Thanos, Alertmanager</td></tr>
    <tr><td>Dashboards (Perses)</td><td>Kubernetes-native dashboards; Grafana import path</td><td>Perses Operator, Prometheus, Loki, Tempo</td></tr>
    <tr><td>Logs</td><td>Query, filter, expand lines; schema viaq vs OTel</td><td>LokiStack</td></tr>
    <tr><td>Traces</td><td>Search traces, open a waterfall</td><td>Tempo + OpenTelemetry collector</td></tr>
    <tr><td>Troubleshooting panel</td><td>Graph of related signals and resources</td><td>Korrel8r</td></tr>
    <tr><td>Incidents</td><td>Group alert bursts into a timeline</td><td>Cluster health analyzer in COO</td></tr>
  </table>
  """ + callout("<b>CMO vs COO.</b> Cluster Monitoring Operator is the default in-cluster Prometheus stack on most OpenShift installs. COO is the meta-operator that adds optional UI plugins, Perses, incidents, ACM wiring, logging and tracing UIs.") + """
  <p>Public repos to skim: <code>openshift/monitoring-plugin</code>, <code>logging-view-plugin</code>, <code>distributed-tracing-console-plugin</code>, <code>troubleshooting-panel-console-plugin</code>, <code>rhobs/observability-operator</code>.</p>
  """, "topics")
    return f'''
<section class="block" id="observe" data-search="Observe surfaces OpenShift console" data-stype="Section">
  <p class="kicker">Product map</p>
  <h2 class="section-title">Observe surfaces</h2>
  {t}
</section>
'''


def plugins() -> str:
    t1 = topic("pl-fed", "Dynamic plugins: Webpack federation, not a new app",
               "OpenShift console dynamic plugin ConsolePlugin", "Lesson",
               """
  <p>The console loads remote JavaScript at runtime (Webpack 5 module federation). You register a <b>ConsolePlugin</b> custom resource. A cluster admin enables it on the console Operator: <code>spec.plugins</code>.</p>
  """ + diagram("""plugin webpack build → HTTP server on cluster
ConsolePlugin CR  →  console Operator spec.plugins
browser loads chunks  →  Observe nav + pages""") + """
  <p>If the UI must call an in-cluster service, declare <code>spec.proxy</code>. The console backend exposes <code>/api/proxy/plugin/…</code>. Default is HTTPS with the service CA. This is why several plugins ship a small <b>Go</b> server: serve assets + proxy Loki/Tempo/Korrel8r.</p>
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
  proxy:
    - objectRef:
        name: loki
        namespace: openshift-logging
        kind: Service
      authorization: UserToken''') + """
  <p>Start from <code>openshift/console-plugin-template</code>. Metadata lives in <code>package.json</code> → <code>consolePlugin</code>. Routes and nav live in <code>console-extensions.json</code>. Use Yarn and Webpack as the READMEs do — Vite is not the console contract.</p>
  """ + callout("Do not import PatternFly CSS in the plugin. Prefix any custom class with the plugin name. Avoid element selectors that leak outside your tree."), "topics")

    t2 = topic("pl-uiplugin", "COO installs your UI with a UIPlugin CR",
               "UIPlugin Cluster Observability Operator", "Lesson",
               """
  <p>For Observe extras, COO watches a <b>UIPlugin</b> and deploys the matching plugin + backends (for example Korrel8r next to the troubleshooting panel, or Perses when monitoring.perses is enabled).</p>
  """ + code("YAML", '''apiVersion: observability.openshift.io/v1alpha1
kind: UIPlugin
metadata:
  name: monitoring
spec:
  type: Monitoring
  monitoring:
    perses:
      enabled: true''') + """
  <p>If Console is GitOps-managed, the plugin name must be in the git <code>Console</code> spec or a sync will disable it. That is an operations bug that looks like a frontend regression.</p>
  """, "topics")
    return f'''
<section class="block" id="plugins" data-search="console dynamic plugins UIPlugin" data-stype="Section">
  <p class="kicker">How code reaches the cluster</p>
  <h2 class="section-title">Console plugins</h2>
  {t1}{t2}
</section>
'''


def patternfly() -> str:
    t = topic("pf-6", "PatternFly 6 is the house look. Tailwind is a defect.",
              "PatternFly 6 OpenShift console accessibility", "Lesson",
              """
  <p>OpenShift 4.19 unified admin/developer perspectives and moved the console to <b>PatternFly 6</b>. Console 4.22 is PF 6. New plugins should target PF 6. The console loads PF base styles. If you import <code>@patternfly/patternfly</code> or PF CSS files, you fight theming (including dark/light) and future upgrades.</p>
  <ul>
    <li>Use PF React components and CSS variables from the SDK / PF packages as the plugin docs allow.</li>
    <li>SDK wrappers exist (for example list page headers). Prefer those when the console already has a pattern.</li>
    <li>No Bootstrap, no Tailwind, no random chart CSS that restyles <code>body</code>.</li>
    <li><b>Accessibility is in the job description.</b> Keyboard, focus order, contrast, name/role/value, charts that are not color-only. Use axe plus a keyboard pass. PF accessibility docs are the standard.</li>
    <li><b>i18n:</b> react-i18next. Hard-coded English in a header is a review block on this team.</li>
  </ul>
  """ + callout("A senior review comment you should be ready to leave: ‘This is a custom div that PF already has as Toolbar / Pagination / EmptyState. Use the component so we inherit a11y and theme.’"), "topics")
    return f'''
<section class="block" id="patternfly" data-search="PatternFly 6 accessibility i18n" data-stype="Section">
  <p class="kicker">Design system</p>
  <h2 class="section-title">PatternFly 6</h2>
  {t}
</section>
'''


def signals() -> str:
    t = topic("sg-three", "Three signals, one journey",
              "metrics logs traces observability mental model", "Lesson",
              """
  <p>A <b>metric</b> is an aggregate over time (CPU, error rate). A <b>log</b> is an event with a payload. A <b>trace</b> is one request across services (spans). Excellent Observe UI does not dump all three on one page. It starts in the right place and <b>jumps</b> with time range and filters intact.</p>
  """ + diagram("""CrashLoop → logs first, then metrics (restarts), then events
High p99   → metrics + trace (who is slow)
Auth 401s  → logs + trace attributes (user, route)
‘Everything is on fire’ → incidents / Alertmanager, not raw 4000 alerts""") + """
  <p>Cardinality: high-cardinality labels in Prometheus will melt the backend <i>and</i> the chart. The UI should not invite unbounded label selectors without a warning.</p>
  """, "topics")
    return f'''
<section class="block" id="signals" data-search="metrics logs traces three signals" data-stype="Section">
  <p class="kicker">Domain</p>
  <h2 class="section-title">Three signals</h2>
  {t}
</section>
'''


def queries() -> str:
    t = topic("qy-langs", "PromQL, LogQL, TraceQL — minimum fluency",
              "PromQL LogQL TraceQL OpenTelemetry", "Lesson",
              """
  <p>You will sit in design reviews where a backend engineer says “just use this query.” You need to know if the UI can show empty, error, timeout, and partial results.</p>
  <ul>
    <li><b>PromQL:</b> instant vs range, <code>rate()</code> vs <code>irate()</code>, <code>histogram_quantile</code>, <code>by</code>/<code>without</code>, recording vs alerting rules. Write ten queries on a real Prometheus.</li>
    <li><b>LogQL:</b> stream selectors, line filters, JSON unpack, then metric queries over logs. The logging plugin has a schema switch: legacy <b>viaq</b> vs <b>OTel</b> logs.</li>
    <li><b>TraceQL:</b> find traces by service, duration, status, attributes. Waterfall, span links, exemplars from metrics into traces. OTel semantic conventions (<code>service.name</code>, k8s, http).</li>
  </ul>
  """ + code("text", '''# PromQL — request rate
sum(rate(http_requests_total[5m])) by (code)

# LogQL — errors in a namespace
{kubernetes_namespace_name="shop"} |= "error"

# TraceQL — slow checkouts
{ resource.service.name = "checkout" && duration > 2s }''') + """
  <p>Jaeger still appears in older talks. Current tracing UI on OpenShift is <b>Tempo</b> plus the OpenTelemetry collector. Learn Tempo; do not become a Jaeger maintainer.</p>
  """ + callout("Performance: abort in-flight fetches when the time picker moves. Cap series. Virtualize huge log/trace tables. A pretty chart that freezes the console is a P1."), "topics")
    return f'''
<section class="block" id="queries" data-search="PromQL LogQL TraceQL" data-stype="Section">
  <p class="kicker">Languages</p>
  <h2 class="section-title">Query languages</h2>
  {t}
</section>
'''


def perses() -> str:
    t = topic("pe-k8s", "Perses is dashboards as cluster resources",
              "Perses dashboards Grafana import OpenShift", "Lesson",
              """
  <p>Perses is an open-source, cloud-native dashboard tool. On OpenShift it is wired through COO: <b>Observe → Dashboards (Perses)</b>. Dashboards and datasources are namespace-scoped CRDs, which matches Kubernetes RBAC and GitOps (dashboard as YAML).</p>
  <ul>
    <li>Graphical editor in the console (create, rename, duplicate).</li>
    <li>Grafana import for the migration story — you should know it exists, not become a Grafana plugin author.</li>
    <li>Datasources: Prometheus / Thanos, Loki, Tempo (as documented for the build you target).</li>
    <li>PatternFly theming work already exists in monitoring-plugin so Perses does not look like a foreign app.</li>
  </ul>
  """ + callout("If you can run one thing extra in week 3: clone <code>perses-dev/perses</code>, create a dashboard as YAML, import one Grafana JSON. That conversation comes up constantly."), "topics")
    return f'''
<section class="block" id="perses" data-search="Perses dashboards as code" data-stype="Section">
  <p class="kicker">Visualization future</p>
  <h2 class="section-title">Perses</h2>
  {t}
</section>
'''


def korrel8r() -> str:
    t = topic("kr-panel", "Correlation is the unified workflow",
              "Korrel8r troubleshooting panel signal correlation", "Lesson",
              """
  <p>Korrel8r is an open-source correlation engine (rules that connect alerts, metrics, logs, pods, netflows). The <b>troubleshooting panel</b> turns results into an interactive graph. Click a node → the matching Observe or workload page with the right query.</p>
  """ + diagram("""Alert firing
  → Korrel8r query
  → nodes: metrics, logs, pod, netflow
  → click → console URL with filters
If Logging plugin is missing, log nodes will not render usefully.""") + """
  <p>The panel plugin maps Korrel8r domains to OpenShift URLs. Those mappings <b>must stay accurate</b> — the repo calls out extensive unit tests. Breaking a URL map is a silent product bug: the graph looks fine, the click goes to the wrong page.</p>
  <p>Clone <code>korrel8r/korrel8r</code> and <code>openshift/troubleshooting-panel-console-plugin</code>. Read AGENTS.md in the panel repo.</p>
  """, "topics")
    return f'''
<section class="block" id="korrel8r" data-search="Korrel8r troubleshooting correlation" data-stype="Section">
  <p class="kicker">The JD’s ‘unified UI workflows’</p>
  <h2 class="section-title">Correlation</h2>
  {t}
</section>
'''


def tools() -> str:
    t = topic("tl-install", "Install this week, not after you join",
              "oc kubectl podman yarn CRC PatternFly axe", "Lesson",
              """
  <table>
    <tr><th>Tool</th><th>Why</th><th>How far in 30 days</th></tr>
    <tr><td><code>oc</code> + kubectl + podman</td><td>Every plugin README assumes them</td><td>Daily muscle memory</td></tr>
    <tr><td>OpenShift Local (CRC) or a sandbox cluster</td><td>Console + plugins against a real API</td><td>One cluster you can break</td></tr>
    <tr><td>Yarn (classic, as plugin repos use it)</td><td>Template and console still yarn</td><td>Install + start-console.sh</td></tr>
    <tr><td>PatternFly 6 React docs</td><td>House design system</td><td>Three screens, no custom CSS soup</td></tr>
    <tr><td>Prometheus + Grafana (kind/minikube)</td><td>PromQL muscle</td><td>Ten useful queries</td></tr>
    <tr><td>Loki + Tempo or the OTel demo</td><td>Logs + traces</td><td>One request across three signals</td></tr>
    <tr><td>Perses (clone and run UI if you can)</td><td>Dashboarding direction</td><td>One YAML dashboard + one Grafana import</td></tr>
    <tr><td>axe DevTools + keyboard-only</td><td>Accessible at the bar they ship</td><td>Audit one PF page</td></tr>
    <tr><td>GitHub CLI + DCO sign-off</td><td>Upstream PRs need Signed-off-by</td><td>One tiny docs or test PR</td></tr>
  </table>
  """, "topics")
    return f'''
<section class="block" id="tools" data-search="tools oc patternfly prometheus" data-stype="Section">
  <p class="kicker">Laptop</p>
  <h2 class="section-title">Tools</h2>
  {t}
</section>
'''


def repos() -> str:
    t = topic("rp-clone", "Read before you write",
              "github console-plugin-template monitoring-plugin", "Lesson",
              """
  <table>
    <tr><th>Repository</th><th>Extract in a weekend</th></tr>
    <tr><td>openshift/console-plugin-template</td><td>Local console-in-container loop, consolePlugin, extensions JSON</td></tr>
    <tr><td>openshift/monitoring-plugin</td><td>Feature flags (CMO vs COO), Perses theming, ACM alerting, incidents</td></tr>
    <tr><td>openshift/logging-view-plugin</td><td>Log list UX, Loki proxy, viaq vs OTel schema</td></tr>
    <tr><td>openshift/distributed-tracing-console-plugin</td><td>React + Go hybrid, Perses for traces, Tempo proxy</td></tr>
    <tr><td>openshift/troubleshooting-panel-console-plugin</td><td>Korrel8r URL mapping, topology graph, tests you must not break</td></tr>
    <tr><td>rhobs/observability-operator</td><td>UIPlugin CR is how UI actually gets onto a cluster</td></tr>
    <tr><td>korrel8r/korrel8r</td><td>Rules that turn an alert into related logs/metrics/pods</td></tr>
    <tr><td>perses-dev/perses</td><td>Dashboard-as-code, query plugins</td></tr>
  </table>
  <p>You will not finish every repo. The template loop + monitoring-plugin README + one tracing or logging plugin is a strong start.</p>
  """, "topics")
    return f'''
<section class="block" id="repos" data-search="repos to clone OpenShift plugins" data-stype="Section">
  <p class="kicker">Source</p>
  <h2 class="section-title">Repos to clone</h2>
  {t}
</section>
'''


def skip() -> str:
    t = topic("sk-no", "Do not over-invest",
              "skip grafana plugins eBPF operator-sdk", "Lesson",
              """
  <p><b>Skip or keep light:</b> training a custom ML model for incidents; replacing PatternFly; deep Grafana plugin authoring (visualization is moving to Perses); full operator-SDK mastery; eBPF internals; becoming a Jaeger maintainer.</p>
  <p><b>Worth four hours each:</b> network observability (netflows in Korrel8r); incident grouping UX; Thanos query path for ACM; OpenShift 4.19 unified perspective. Internal Konflux/CI after you have a laptop and internal docs.</p>
  """, "topics")
    return f'''
<section class="block" id="skip" data-search="what not to study" data-stype="Section">
  <p class="kicker">Focus</p>
  <h2 class="section-title">Do not over-invest</h2>
  {t}
</section>
'''


def senior() -> str:
    t = topic("sr-jd", "Map the job bullets to artifacts",
              "lead architect mentor upstream community", "Lesson",
              """
  <table>
    <tr><th>Line</th><th>What excellence looks like by week 6 on the team</th></tr>
    <tr><td>Lead &amp; architect</td><td>You propose a plugin boundary, a proxy, a feature flag, and a PF pattern — not a new SPA</td></tr>
    <tr><td>Catalyze collaboration</td><td>You translate Loki tenant limits and Tempo retention into UI copy, empty states, and UX with PM</td></tr>
    <tr><td>Own &amp; deliver upstream</td><td>Feature lands on GitHub first, then COO/CMO. You know DCO, OWNERS, backport</td></tr>
    <tr><td>Mentor &amp; influence</td><td>Reviews catch a11y, i18n keys, PF misuse, unbounded fetches — not only lint</td></tr>
    <tr><td>Community</td><td>You can talk Perses, Korrel8r, or console plugins without reading slides first</td></tr>
  </table>
  <p>Write a one-page architecture before day 30: plugins, COO, signals, UX, upstream. You will reuse it in 1:1s.</p>
  """, "topics")
    return f'''
<section class="block" id="senior" data-search="senior behaviors lead mentor upstream" data-stype="Section">
  <p class="kicker">How you show up</p>
  <h2 class="section-title">Senior behaviors</h2>
  {t}
</section>
'''
