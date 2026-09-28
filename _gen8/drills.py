from util import practice_problem, callout


def drills() -> str:
    rows = [
        ("ex-consoleplugin", 1, "Sketch a ConsolePlugin CR",
         "easy", "plugin", "CR + proxy",
         "Write YAML: plugin name, backend service, one Loki proxy with UserToken. Then say how an admin enables it.",
         "ConsolePlugin is console.openshift.io/v1. Enable via console Operator spec.plugins. Proxy is how the browser reaches Loki.",
         """apiVersion: console.openshift.io/v1
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
      authorization: UserToken
# enable: Console spec.plugins += example-observe""",
         "Wrong API group or skipping spec.plugins.",
         "Hard-coding the Loki URL in fetch()."),
        ("ex-uiplugin", 2, "Sketch a UIPlugin that turns Perses on",
         "easy", "ops", "COO CR",
         "Write the smallest UIPlugin that enables Perses under Monitoring. Say which operator consumes it.",
         "observability.openshift.io UIPlugin, type Monitoring, monitoring.perses.enabled. COO deploys the bits.",
         """apiVersion: observability.openshift.io/v1alpha1
kind: UIPlugin
metadata:
  name: monitoring
spec:
  type: Monitoring
  monitoring:
    perses:
      enabled: true""",
         "Putting this on the Console CR instead of COO.",
         "Assuming Grafana appears automatically."),
        ("ex-promql", 3, "5xx ratio PromQL",
         "medium", "query", "rate + ratio",
         "Write PromQL for 5xx / all requests over 5m, summed across instances. No user-id label.",
         "rate() on a counter. Filter 5xx in the numerator. Same grouping in num and den.",
         """sum(rate(http_requests_total{code=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))""",
         "Plotting the raw counter. Grouping by user.",
         "irate() on an SLO graph."),
        ("ex-logql", 4, "Namespace error LogQL",
         "medium", "query", "selector then filter",
         "Logs for namespace shop, container checkout, lines containing error. Mention viaq vs OTel as a risk.",
         "Stream selector first, then |=. Field names depend on schema.",
         """{kubernetes_namespace_name="shop", app="checkout"} |= "error"
# if empty: check viaq vs OTel label names""",
         "Regex over every tenant.",
         "Assuming {app=} exists on both schemas."),
        ("ex-pf-empty", 5, "Empty and error states",
         "easy", "patternfly", "EmptyState + live region",
         "List the PF pieces and a11y for: no rows, query timeout, partial series.",
         "EmptyState for zero. Inline alert + live region for timeout. Partial: show what you have and say what dropped.",
         """no rows     → EmptyState (title, body, optional action)
timeout     → Alert + aria-live polite
partial     → table + ‘12 series dropped’""",
         "A spinner forever.",
         "Color-only red banner."),
        ("ex-journey", 6, "One request, three signals",
         "medium", "signals", "join keys",
         "A checkout request is slow. Write the click path: metric → trace → logs. Name the join keys.",
         "p99 or error ratio → Tempo by service.name / trace id (exemplar) → Loki by namespace + trace id if present.",
         """Metrics:  histogram_quantile or error ratio (service=checkout)
Traces:   TraceQL resource.service.name + duration
Logs:     namespace shop + trace_id if the collector injects it""",
         "Three unlinked dump pages.",
         "Starting in Jaeger because of a 2021 blog."),
        ("ex-korrel8r", 7, "URL map test",
         "medium", "korrel8r", "href contract",
         "Write in words the test you would add when Observe log route changes.",
         "Given an alert neighbour of type log, expect href host + path + query. Fail CI if the plugin route renamed.",
         """given: korrel8r node {domain: log, query: ...}
expect: /observe/logs?q=...   (or current plugin path)
assert: logging plugin missing → explicit empty copy, not 404""",
         "Screenshot tests of the graph only.",
         "Assuming sibling plugins are always installed."),
        ("ex-gitops", 8, "Plugin disappeared",
         "easy", "ops", "Console spec",
         "Checklist: three places to look before blaming Webpack.",
         "Console CR spec.plugins (git). UIPlugin / COO. Plugin Deployment / Route. Then webpack.",
         """1. Console spec.plugins in git (GitOps won)
2. UIPlugin + COO status
3. Plugin pod / service
4. Then browser: remote entry 404""",
         "Only Chrome DevTools network tab.",
         "Re-enabling in UI without committing."),
    ]
    blocks = [practice_problem(*row, lang="text") for row in rows]
    return f'''
<section class="block" id="drills" data-search="Exercises Observe UI sketches" data-stype="Section">
  <p class="kicker">{len(rows)} sketches</p>
  <h2 class="section-title">Exercises</h2>
  <p class="lede">Write on paper first. Reveal after you have YAML or PromQL, not before. Mark complete when you can redo it from a blank page.</p>
  {callout("Original teaching drills — not claimed employer questions.")}
  {''.join(blocks)}
</section>
'''
