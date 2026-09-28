from util import topic, code, callout, diagram


def _study(cid, title, search, problem, approach, lang, snippet, product, trap):
    return topic(cid, title, search, "Practical study", f'''
  <p><b>Problem.</b> {problem}</p>
  <p><b>Approach.</b> {approach}</p>
  {code(lang, snippet)}
  <p><b>Where this shows up.</b> {product}</p>
  <p><b>Trap.</b> {trap}</p>
  ''', "reactTopics")


def practical() -> str:
    items = [
        _study("ps-plugin-loop", "Ship a Hello Observe plugin",
               "console plugin template local loop",
               "You need a page under Observe that is not a new SPA.",
               "Clone console-plugin-template. Keep Webpack + Yarn. Register consolePlugin in package.json, a console-extensions.json nav item, a ConsolePlugin CR. Enable spec.plugins. Do not import PatternFly CSS.",
               "JSON",
               '''{
  "consolePlugin": {
    "exposedModules": { "./ObservePage": "./src/components/ObservePage" }
  }
}''',
               "Every Observe UI that is not baked into the console binary.",
               "Starting a Vite app and iframe-ing it into the console."),
        _study("ps-proxy", "Logs page without CORS hacks",
               "ConsolePlugin spec.proxy Loki",
               "The browser cannot talk to Loki directly. Copy-paste fetch to an internal URL fails CORS and RBAC.",
               "Declare spec.proxy to the Loki service. Call /api/proxy/plugin/<name>/…. Go (or the template server) terminates TLS with the service CA. Send the user token if the CR says so.",
               "YAML",
               '''spec:
  proxy:
    - objectRef:
        name: loki
        namespace: openshift-logging
        kind: Service
      authorization: UserToken''',
               "logging-view-plugin, tracing plugin, Korrel8r panel.",
               "Hard-coding a cluster IP in frontend code."),
        _study("ps-pf-table", "Filterable list that looks like the console",
               "PatternFly 6 table toolbar empty state",
               "PM wants a ‘nice dashboard table’ of firing alerts.",
               "Toolbar + filter + pagination + EmptyState from PatternFly 6. Keyboard through the toolbar. Prefix any extra class with the plugin name.",
               "TSX",
               '''<Toolbar>
  <ToolbarContent>
    <SearchInput value={q} onChange={(_, v) => setQ(v)} />
  </ToolbarContent>
</Toolbar>
{rows.length ? <Table rows={rows} /> : <EmptyState titleText="No alerts" />}''',
               "Alerting, log lines, trace search hits.",
               "Tailwind table + custom pagination that skips PF a11y."),
        _study("ps-signals", "CrashLoop: pick the first click",
               "CrashLoop logs then metrics then events",
               "A deployment is CrashLooping. The user is already in the console.",
               "Logs first (why did the process die). Then metrics (restart count). Then events / Korrel8r for related objects. Do not open a 40-panel Grafana board as v1.",
               "text",
               '''CrashLoop
  1. Observe → Logs  (last lines, previous container)
  2. Metrics         (restarts, CPU OOM?)
  3. Troubleshooting (related pods, alerts)''',
               "Workload debugging from Observe.",
               "Starting with a custom dashboard because it looks senior."),
        _study("ps-promql", "Error-rate chart that will not melt Prometheus",
               "PromQL rate by code cardinality",
               "Show request error ratio for a service. Someone wants a label for every user id.",
               "rate() on a counter, then divide 5xx by total. Aggregate by code or route — never by user. Cap series in the UI. Abort the fetch when the time picker moves.",
               "PromQL",
               '''sum(rate(http_requests_total{code=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))''',
               "Metrics pages, Perses panels, ACM aggregated views.",
               "histogram_quantile on a high-cardinality label without a recording rule."),
        _study("ps-logql", "Find checkout errors without grepping a node",
               "LogQL stream selector JSON unpack",
               "Checkout is failing for one namespace. Logs are in Loki.",
               "Stream selector first (namespace, container), then a line filter, then JSON unpack if the schema is structured. Know viaq vs OTel field names before you invent a filter.",
               "LogQL",
               '''{kubernetes_namespace_name="shop", app="checkout"}
  |= "error"
  | json''',
               "logging-view-plugin query bar.",
               "A regex across all tenants because ‘it worked in grep’."),
        _study("ps-perses", "Dashboard as a namespaced CR",
               "Perses dashboard YAML GitOps",
               "Platform team wants the same SLO board in every shop namespace, reviewable in git.",
               "Perses dashboard + datasource CRs, not a Grafana folder nobody owns. Import Grafana JSON once as a migration, then treat YAML as source of truth.",
               "YAML",
               '''apiVersion: perses.dev/v1alpha1
kind: PersesDashboard
metadata:
  name: checkout-slo
  namespace: shop
spec:
  display:
    name: Checkout SLO''',
               "Observe → Dashboards (Perses).",
               "Editing production Grafana by hand forever."),
        _study("ps-korrel8r", "Alert click that must not 404",
               "Korrel8r URL map troubleshooting panel",
               "The graph shows a log node. Click should open Observe → Logs with the right query.",
               "Keep the domain → console URL map in lockstep with plugin routes. Add a unit test for the href. If Logging is not installed, the node should say so — not fail silently.",
               "text",
               '''alert node
  → korrel8r neighbours
  → console URL (plugin route + query)
  → tests: snapshot the href''',
               "troubleshooting-panel-console-plugin.",
               "Pretty graph, wrong href. Looks like a backend bug."),
        _study("ps-gitops-plugin", "Plugin vanished after a sync",
               "GitOps Console spec.plugins wipe",
               "You enabled a plugin in the UI. Next morning it is gone. GitOps owns the Console CR.",
               "The plugin name must be in the git Console spec. A live toggle without git is a race the reconcilers will win.",
               "YAML",
               '''apiVersion: operator.openshift.io/v1
kind: Console
spec:
  plugins:
    - monitoring-plugin
    - logging-view-plugin''',
               "Any cluster with Argo/ACM policy on console.",
               "Debugging Webpack for a day when git overwrote spec.plugins."),
        _study("ps-a11y-chart", "A chart a keyboard user can use",
               "accessibility charts not color only",
               "Error vs OK is red vs green. Color-blind and screen-reader users get nothing.",
               "Pattern + label + not color-only. Summary in text. Live region for ‘query failed’. Focus order through the time picker, then the chart, then the table.",
               "text",
               '''OK:  pattern + "2xx" label
ERR: pattern + "5xx" label
SR:  "Query failed: timeout" in a live region''',
               "Every Observe chart.",
               "Custom canvas with no name/role/value."),
    ]
    return f'''
<section class="block" id="practical" data-search="Practical studies Observe UI" data-stype="Section">
  <p class="kicker">{len(items)} studies</p>
  <h2 class="section-title">Practical studies</h2>
  <p class="lede">Sketches, not production PRs. Speak the approach before you open the snippet. Mark complete when you can redo it on a whiteboard.</p>
  {callout("These are original teaching scenarios. They are not claimed interview questions from any employer.")}
  {diagram("""read the problem
  → name the plugin / CR / query
  → say the empty and error states
  → then look at the snippet""")}
  {''.join(items)}
</section>
'''
