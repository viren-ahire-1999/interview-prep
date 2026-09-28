from util import callout


def mock() -> str:
    return r'''
<section class="block" id="mock" data-search="Teach-back timed practice" data-stype="Section">
  <p class="kicker">Timed practice</p>
  <h2 class="section-title">Teach-back</h2>
  <p class="lede">Draws a random Q&amp;A or exercise (<code>data-mock</code>). Speak: plugin or query → empty/error state → what you would not build. Reveal after you have an approach. Save a debrief.</p>
  <div class="card" style="margin-bottom:16px">
    <p>Category
      <select id="mock-cat">
        <option value="all">All</option>
        <option value="console">console</option>
        <option value="ui">ui</option>
        <option value="domain">domain</option>
        <option value="promql">promql</option>
        <option value="logql">logql</option>
        <option value="traceql">traceql</option>
        <option value="dashboards">dashboards</option>
        <option value="correlation">correlation</option>
        <option value="cmo">cmo</option>
        <option value="gitops">gitops</option>
        <option value="lead">lead</option>
        <option value="upstream">upstream</option>
        <option value="review">review</option>
        <option value="plugin">plugin</option>
        <option value="ops">ops</option>
        <option value="query">query</option>
        <option value="signals">signals</option>
        <option value="patternfly">patternfly</option>
        <option value="korrel8r">korrel8r</option>
      </select>
    </p>
    <div class="status-btns">
      <button type="button" class="toggle-btn" data-start-mock="15">15-min question</button>
      <button type="button" class="toggle-btn" data-start-mock="30">30-min sketch</button>
      <button type="button" class="toggle-btn" data-start-mock="45">45-min design</button>
      <button type="button" class="toggle-btn" data-start-mock="60">60-min teach-back</button>
    </div>
    <div id="mock-panel"><p class="stat-sub">Pick a duration. Narrate before you type. Reveal only after you have a plugin/query choice and an empty-state.</p></div>
  </div>
  <div class="card">
    <h3>Debrief rubric</h3>
    <label class="task"><input type="checkbox" id="mock-q-trade" /> <span>I named a plugin boundary or query, not a new SPA</span></label>
    <label class="task"><input type="checkbox" id="mock-q-time" /> <span>I named empty, error, and partial-query states</span></label>
    <label class="task"><input type="checkbox" id="mock-q-a11y" /> <span>I named PatternFly / a11y or cardinality, not only the happy chart</span></label>
    <p>Notes<br /><textarea id="mock-notes" rows="3" style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:inherit"></textarea></p>
    <p>Confidence
      <select id="mock-confidence">
        <option value="1">1</option><option value="2">2</option>
        <option value="3" selected>3</option><option value="4">4</option><option value="5">5</option>
      </select>
    </p>
    <p><button type="button" class="toggle-btn" id="save-mock">Save teach-back</button></p>
  </div>
  <div class="card" style="margin-top:16px"><h3>History</h3><div id="mock-history"></div></div>
</section>
'''


def progress() -> str:
    return r'''
<section class="block" id="progress" data-search="Progress Tracker before we start" data-stype="Section">
  <p class="kicker">localStorage pre-start-v1</p>
  <h2 class="section-title">Progress Tracker</h2>
  <div class="grid grid-2">
    <div class="card"><h3>Daily tasks</h3><p id="track-days">0</p></div>
    <div class="card"><h3>Lessons</h3><p id="track-arch">0</p><div class="bar"><span id="bar-cat-arch"></span></div></div>
    <div class="card"><h3>Practical studies</h3><p id="track-react">0</p><div class="bar"><span id="bar-cat-react"></span></div></div>
    <div class="card"><h3>Q&amp;A</h3><p id="track-qs">0</p></div>
    <div class="card"><h3>Exercises</h3><p id="track-sd">0</p><div class="bar"><span id="bar-cat-sd"></span></div></div>
    <div class="card"><h3>Drills</h3><p id="track-ex">0</p></div>
  </div>
  <p style="margin-top:18px"><button type="button" class="danger-btn" id="reset-progress">Reset all progress on this guide</button></p>
</section>
<section class="block" id="revision" data-search="Revision spaced repetition" data-stype="Section">
  <p class="kicker">Remember on purpose</p>
  <h2 class="section-title">Revision System</h2>
  <p class="lede">Completed items review at 1 → 3 → 7 → 14 → 30 days. Attempted/failed → tomorrow. Mastered parks at 30 days.</p>
  <div class="grid grid-2">
    <div class="card"><h3>Due today</h3><ul class="tight" id="rev-today"></ul></div>
    <div class="card"><h3>Due this week</h3><ul class="tight" id="rev-week"></ul></div>
    <div class="card"><h3>Recently failed</h3><ul class="tight" id="rev-failed"></ul></div>
    <div class="card"><h3>Weak areas</h3><ul class="tight" id="rev-weak"></ul></div>
    <div class="card"><h3>Mastered</h3><ul class="tight" id="rev-mastered"></ul></div>
  </div>
</section>
'''


def readiness() -> str:
    groups = [
        ("Plugins and install", [
            ("r-fed", "Explain Webpack federation vs a new SPA in one minute"),
            ("r-cr", "Sketch a ConsolePlugin CR including spec.proxy from memory"),
            ("r-enable", "Say how spec.plugins and GitOps Console spec interact"),
            ("r-uiplugin", "Explain UIPlugin vs ConsolePlugin and which operator watches UIPlugin"),
            ("r-go", "Say why several Observe plugins ship a small Go server"),
            ("r-template", "Describe the console-plugin-template local loop without opening the README"),
        ]),
        ("PatternFly and a11y", [
            ("r-pf6", "Name why OCP 4.19+ plugins target PatternFly 6"),
            ("r-css", "Say why importing PatternFly CSS in a plugin is a defect"),
            ("r-prefix", "Prefix custom classes with the plugin name — give one example"),
            ("r-axe", "Run a keyboard pass + axe on a PF table and name two issues you would fix"),
            ("r-i18n", "Say where English strings must not live (react-i18next)"),
            ("r-chart", "Describe a chart that is not color-only"),
        ]),
        ("Signals and queries", [
            ("r-three", "Pick first signal for CrashLoop, p99, and 401 — and the second"),
            ("r-cmo", "CMO vs COO in one minute"),
            ("r-promql", "Write a 5xx ratio PromQL without a user-id label"),
            ("r-logql", "Write a namespace LogQL and name viaq vs OTel as a risk"),
            ("r-traceql", "Find a slow service in TraceQL and open a waterfall"),
            ("r-card", "Explain why high cardinality is a UI bug as well as a backend bug"),
            ("r-abort", "Say how you abort in-flight fetches when the time picker moves"),
        ]),
        ("Perses, correlation, ops", [
            ("r-perses", "Explain Perses dashboards as namespaced CRs vs a Grafana folder"),
            ("r-import", "Say what Grafana import is for (migration, not a career)"),
            ("r-korr", "Sketch Korrel8r: alert → neighbours → console URL"),
            ("r-href", "Say why a URL-map test is more important than a pretty graph"),
            ("r-gitops", "Debug a vanished plugin starting at GitOps Console spec"),
            ("r-inc", "Say when to open Incidents vs raw Alertmanager"),
        ]),
        ("How you show up", [
            ("r-lead", "Propose a plugin boundary, proxy, flag, and PF pattern — not a new SPA"),
            ("r-up", "Describe DCO / Signed-off-by and why GitHub-first matters"),
            ("r-review", "Leave a senior review comment: a11y, i18n, unbounded fetch, or PF misuse"),
            ("r-arch", "Write a one-page architecture: plugins, COO, signals, UX, upstream"),
            ("r-teach", "Teach ConsolePlugin + three signals to a rubber duck in 5 minutes from a blank page"),
        ]),
    ]
    html = []
    for title, items in groups:
        html.append(f"<h3>{title}</h3>")
        for id_, label in items:
            html.append(
                f'<label class="task"><input type="checkbox" data-id="{id_}" data-group="readiness" /><span>{label}</span></label>'
            )
    return f'''
<section class="block" id="readiness" data-search="readiness checklist before we start" data-stype="Section">
  <p class="kicker">Gate</p>
  <h2 class="section-title">Readiness checklist</h2>
  <p class="lede">Check only if you can do it <i>today</i> without this file. Stay until ~85% and you can teach the plugin loop without notes.</p>
  <p class="stat">Score: <span id="ready-score">0%</span></p>
  <div class="bar"><span id="bar-ready-final"></span></div>
  <p id="ready-gate" class="stat-sub"></p>
  {''.join(html)}
</section>
'''


def resources() -> str:
    rows = [
        ("OpenShift console dynamic plugins", "https://github.com/openshift/enhancements/blob/master/enhancements/console/dynamic-plugins.md",
         "How the console loads remote plugins.", "Read once so ConsolePlugin is not magic.", "Plugins", False),
        ("console-plugin-template", "https://github.com/openshift/console-plugin-template",
         "Yarn, Webpack, start-console, extensions JSON.", "This is the loop. Clone it in week 1.", "Plugins", False),
        ("Dynamic plugin SDK", "https://github.com/openshift/console/tree/master/frontend/packages/console-dynamic-plugin-sdk",
         "APIs plugins are allowed to use.", "Prefer SDK wrappers over reinventing list pages.", "Plugins", False),
        ("PatternFly 6", "https://www.patternfly.org/get-started/design/",
         "House design system for the console.", "Build three screens. Do not import PF CSS in the plugin.", "PatternFly", False),
        ("PatternFly accessibility", "https://www.patternfly.org/accessibility/about-accessibility/",
         "Keyboard, contrast, components that already have a11y.", "Job-level bar, not a polish pass.", "PatternFly", False),
        ("Prometheus querying", "https://prometheus.io/docs/prometheus/latest/querying/basics/",
         "PromQL: rate, instant vs range, aggregations.", "Ten queries on a real Prometheus beat twenty blog posts.", "Queries", False),
        ("LogQL", "https://grafana.com/docs/loki/latest/query/",
         "Loki query language.", "Selector first, then line filter, then unpack.", "Queries", False),
        ("TraceQL", "https://grafana.com/docs/tempo/latest/traceql/",
         "Tempo trace search.", "Current tracing UI direction with OTel — not Jaeger-as-product.", "Queries", False),
        ("OpenTelemetry semantic conventions", "https://opentelemetry.io/docs/specs/semconv/",
         "service.name, k8s, http join keys.", "The glue between metrics, logs, and traces.", "Signals", False),
        ("Perses", "https://github.com/perses/perses",
         "Dashboards as code.", "Create one YAML dashboard; try one Grafana import.", "Perses", False),
        ("Korrel8r", "https://github.com/korrel8r/korrel8r",
         "Correlation engine.", "Read the rule idea, then the troubleshooting panel.", "Correlation", False),
        ("troubleshooting-panel-console-plugin", "https://github.com/openshift/troubleshooting-panel-console-plugin",
         "Graph + URL maps + tests.", "AGENTS.md in the repo is worth a pass.", "Correlation", False),
        ("monitoring-plugin", "https://github.com/openshift/monitoring-plugin",
         "Metrics, alerting, Perses theming, incidents, ACM.", "Largest Observe UI. Skim README and feature flags.", "Observe", False),
        ("logging-view-plugin", "https://github.com/openshift/logging-view-plugin",
         "Log list, Loki proxy, schema switch.", "Pairs with LogQL practice.", "Observe", False),
        ("distributed-tracing-console-plugin", "https://github.com/openshift/distributed-tracing-console-plugin",
         "React + Go, Tempo proxy.", "See a hybrid plugin.", "Observe", False),
        ("observability-operator", "https://github.com/rhobs/observability-operator",
         "UIPlugin and how COO installs UI.", "The CR that actually puts pages on a cluster.", "Ops", False),
        ("OpenShift Cluster Observability Operator", "https://docs.openshift.com/container-platform/latest/observability/cluster_observability_operator/coo-overview.html",
         "Product docs for COO / Observe extras.", "Use after you understand UIPlugin. Optional official docs.", "Ops", True),
        ("OpenShift console plugins docs", "https://docs.openshift.com/container-platform/latest/web_console/dynamic-plugin/overview-dynamic-plugin.html",
         "Supported plugin model on OpenShift.", "Pairs with the template README.", "Plugins", True),
        ("DCO", "https://developercertificate.org/",
         "Signed-off-by for upstream commits.", "One tiny docs PR teaches the machine.", "Upstream", False),
        ("Frontend system design on this hub", "frontend-system-design.html",
         "Product design discipline you reuse for Observe pages.", "Empty states and scoped v1 still apply.", "Design", True),
    ]
    cards = []
    for name, url, what, why, topic, opt in rows:
        badge = '<span class="badge badge-opt">Optional</span>' if opt else '<span class="badge badge-pattern">Primary</span>'
        cards.append(f'''
<article class="card" data-search="{name}" data-stype="Resource">
  <div class="meta-row">{badge}</div>
  <h3><a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a></h3>
  <p><b>Teaches.</b> {what}</p>
  <p><b>Why open it.</b> {why}</p>
  <p><b>Guide topic.</b> {topic}</p>
</article>''')
    return f'''
<section class="block" id="resources" data-search="Resource library Observe UI" data-stype="Section">
  <p class="kicker">Public first</p>
  <h2 class="section-title">Resource Library</h2>
  <p class="lede">This HTML already contains the teaching. Links are public docs and GitHub. Practice items here are original teaching, not claimed company questions. Internal CI and downstream branches wait until you have accounts.</p>
  {callout("Vendor product docs are labeled optional. You do not need a subscription to finish the 30-day plan.")}
  <div class="grid grid-2">{''.join(cards)}</div>
</section>
'''


def glossary() -> str:
    terms = [
        ("ACM", "Advanced Cluster Management. Multi-cluster; often Thanos for metrics and a different alerting path."),
        ("Alertmanager", "Routes and groups Prometheus alerts. Incidents sit above raw alert floods."),
        ("CMO", "Cluster Monitoring Operator — default in-cluster Prometheus stack on OpenShift."),
        ("ConsolePlugin", "CR that registers a dynamic plugin: assets service, optional proxy, display name."),
        ("COO", "Cluster Observability Operator — installs optional Observe UIs, Perses, incidents, related backends."),
        ("CRC / OpenShift Local", "A laptop-sized OpenShift cluster for plugin loops."),
        ("DCO", "Developer Certificate of Origin. Commits need Signed-off-by for many OpenShift repos."),
        ("Dynamic plugin", "Webpack 5 module federation: the console loads your JS at runtime."),
        ("Exemplar", "A trace id attached to a metric sample so the UI can jump metric → trace."),
        ("GitOps Console spec", "If git owns the Console CR, plugin names must live there or a sync disables them."),
        ("Korrel8r", "Correlation engine: rules that link alerts, metrics, logs, pods, netflows."),
        ("LogQL", "Loki query language. Stream selector, then line filters, then unpack."),
        ("Loki / LokiStack", "Log store. Observe → Logs talks to it through a plugin proxy."),
        ("OTel", "OpenTelemetry: collector pipeline + semantic conventions. Not a React library."),
        ("OWNERS", "File that lists who can approve a repo area. Read it before you ping randomly."),
        ("PatternFly 6", "OpenShift console design system from 4.19+. Do not import its CSS in a plugin."),
        ("Perses", "Cloud-native dashboards as Kubernetes CRs. Observe → Dashboards (Perses)."),
        ("PromQL", "Prometheus query language. Instant vs range; rate on counters."),
        ("spec.plugins", "Console Operator list of enabled dynamic plugins."),
        ("spec.proxy", "ConsolePlugin field: console backend proxies to an in-cluster Service."),
        ("Tempo", "Trace store used with the current tracing UI. Jaeger is legacy conversation."),
        ("Thanos", "Long-term / multi-cluster metrics path (often with ACM)."),
        ("TraceQL", "Tempo’s language to find traces by service, duration, attributes."),
        ("Troubleshooting panel", "Console graph UI over Korrel8r results; clicks must map to real routes."),
        ("UIPlugin", "COO CR that selects which Observe UI extras to install."),
        ("viaq", "Legacy OpenShift logging schema. OTel schema is the other switch in the logs UI."),
        ("WCAG", "Accessibility standard. Keyboard, contrast, name/role/value — in the job, not polish."),
    ]
    items = []
    for name, defn in terms:
        items.append(f'<article class="card glossary-item" data-search="{name}"><h3>{name}</h3><p>{defn}</p></article>')
    return f'''
<section class="block" id="glossary" data-search="Glossary Observe UI" data-stype="Section">
  <p class="kicker">Language</p>
  <h2 class="section-title">Glossary</h2>
  <p><input id="glossary-filter" type="search" placeholder="Filter terms..." style="width:100%;max-width:360px;padding:8px 10px;border-radius:8px;border:1px solid var(--border);background:var(--bg);color:inherit" /></p>
  <div class="grid grid-2" style="margin-top:16px">{''.join(items)}</div>
</section>
'''
