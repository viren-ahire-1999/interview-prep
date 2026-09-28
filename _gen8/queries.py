from util import topic, diagram, callout, code


def promql() -> str:
    t1 = topic("pq-types", "Instant vs range: what the chart actually asks for",
               "PromQL instant range vector step", "Lesson",
               """
  <p>Prometheus stores <b>time series</b>: a metric name + labels (the identity) and samples (timestamp, value). The language is <b>PromQL</b>. The UI almost always sends a <b>range query</b>: start, end, and step. The backend returns one series per matching identity, with a point at each step.</p>
  <table>
    <tr><th>Kind</th><th>What you get</th><th>UI use</th></tr>
    <tr><td>Instant query</td><td>One value “now” (or at a timestamp) per series</td><td>Single-stat, table of current values</td></tr>
    <tr><td>Range query</td><td>A matrix: series × timestamps</td><td>Line/area charts, heatmaps</td></tr>
  </table>
  """ + diagram("""Browser time picker  →  start, end, step
GET /api/v1/query_range?query=...&start=&end=&step=
  →  { metric: {code:"500"}, values: [[t, v], ...] }
Empty: no matching series. Error: parse / timeout. Partial: some series dropped.""") + """
  <p>A <b>selector</b> picks series. Labels are equality, regex, or not-equal:</p>
  """ + code("PromQL", '''http_requests_total{job="checkout", code="200"}
http_requests_total{code=~"5.."}      # regex
http_requests_total{code!="200"}''') + """
  <p><b>Counters</b> only go up (except on process restart). Graphing a raw counter looks like a staircase and lies on restarts. You almost always wrap counters in <code>rate()</code> or <code>increase()</code>. <b>Gauges</b> (CPU, memory, queue depth) you can plot raw or with <code>avg_over_time</code>.</p>
  """ + callout("If a backend engineer says ‘just graph http_requests_total,’ ask: is it a counter? If yes, the UI should offer rate, not the raw series, as the default."), "topics")

    t2 = topic("pq-rate", "rate, irate, histograms — the three you will type",
               "PromQL rate irate histogram_quantile by without", "Lesson",
               """
  <p><code>rate(x[5m])</code> is “per-second average increase of counter x over the last 5 minutes,” computed at each step of a range query. Use it for graphs and SLOs. The window <code>[5m]</code> must be several scrapes long (if you scrape every 30s, 5m is fine; 10s is not).</p>
  <p><code>irate(x[5m])</code> uses only the last two samples. It is spiky — useful for “what is happening in this instant,” misleading as a 6-hour SLO chart.</p>
  """ + code("PromQL", '''# Requests per second, by status class
sum(rate(http_requests_total[5m])) by (code)

# Error ratio — same grouping in numerator and denominator
sum(rate(http_requests_total{code=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))

# p99 latency if you have a histogram
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))''') + """
  <p><code>by (label)</code> keeps those labels and sums away the rest. <code>without (label)</code> is the inverse. The #1 PromQL bug in a UI is <b>numerator and denominator grouped differently</b>, so the ratio is nonsense. The #2 bug is <b>grouping by a high-cardinality label</b> (user id, pod uid, request id) — thousands of series, melted Prometheus, melted browser.</p>
  <p><b>histogram_quantile</b> needs the <code>_bucket</code> series and the <code>le</code> label. It is an estimate, not a true percentile of raw events. Recording rules exist so the UI does not recompute expensive queries on every zoom.</p>
  """ + diagram("""Good group-by:  code, route, job, namespace
Bad group-by:   user_id, email, trace_id, pod_uid
UI job: do not offer the bad ones as a chip. Warn if series count explodes.""") + """
  <p>When the time picker moves, <b>abort</b> the in-flight fetch (AbortController). Otherwise you paint a stale range on top of a new one. Cap the number of series you draw (for example 20) and say “12 more not shown.”</p>
  """, "topics")

    t3 = topic("pq-ui", "What a metrics page must show besides the line",
               "Prometheus empty error timeout no data UI", "Lesson",
               """
  <p>PromQL can return:</p>
  <ul>
    <li><b>No data</b> — query is valid, nothing matched (wrong label, empty namespace).</li>
    <li><b>Parse error</b> — show the backend message; do not swallow it into “No data.”</li>
    <li><b>Timeout / 502</b> — the query is too expensive or the proxy died.</li>
    <li><b>Partial</b> — some shards failed (common with Thanos). Show the series you have and a warning.</li>
  </ul>
  <p>Each of those is a different PatternFly EmptyState or Alert. Color-only “red chart” is not enough. A screen reader needs a live region: “Query failed: timeout.”</p>
  """ + callout("Multi-cluster (ACM + Thanos) adds a cluster picker. ‘cluster’ is a first-class filter, not a footnote. A query that worked on one cluster can be empty on another because scrape configs differ."), "topics")
    return f'''
<section class="block" id="promql" data-search="PromQL tutorial rate histogram" data-stype="Section">
  <p class="kicker">Tutorial</p>
  <h2 class="section-title">PromQL</h2>
  <p class="lede">You will not memorize every function. You will know counters vs gauges, rate vs irate, how a range query is parameterized, and which empty state you are in. That is enough to argue with a backend query in a design review.</p>
  {t1}{t2}{t3}
</section>
'''


def logql() -> str:
    t1 = topic("lq-stream", "Selector first, then grep — that order is the product",
               "LogQL stream selector line filter json unpack", "Lesson",
               """
  <p>Loki stores logs as <b>streams</b>: a set of labels (like Prometheus) plus lines. <b>LogQL</b> starts with a <b>stream selector</b> in curly braces. That is the cheap index. Everything after it is a filter or parser on the line payload — more CPU, more scan.</p>
  """ + code("LogQL", '''# 1. Pick streams (labels). Cheap if labels are the index.
{kubernetes_namespace_name="shop", app="checkout"}

# 2. Then filter lines. |= is substring. |~ is regex. != / !~ negate.
{kubernetes_namespace_name="shop", app="checkout"} |= "error"

# 3. Then parse structured lines so you can filter on fields.
{kubernetes_namespace_name="shop", app="checkout"}
  |= "error"
  | json
  | status >= 500''') + """
  <p>If you skip the selector and regex across every tenant, you can take down Loki the same way unbounded PromQL takes down Prometheus. The query bar should <b>require or strongly suggest</b> namespace / application labels before a free-text grep.</p>
  """ + diagram("""Good:  {namespace, app, container}  then  |= "error"
Bad:   {job=~".+"} |~ "error"     across the whole cluster
UI:    namespace picker first, not a blank grep box as the hero.""") + """
  <p><b>Line filters:</b> <code>|= "error"</code> substring, <code>|~ "err(or|s)"</code> regex, <code>!=</code> / <code>!~</code> negate. After a parser (<code>| json</code>, <code>| logfmt</code>, <code>| regexp</code>), you can filter on extracted fields.</p>
  <p>LogQL can also become a <b>metric query</b> (count of matching lines over time) with <code>rate({...} |= "error" [5m])</code>. That is how “errors/sec from logs” charts work — still a Loki query, not Prometheus.</p>
  """, "topics")

    t2 = topic("lq-schema", "viaq vs OTel: the same UI, different field names",
               "viaq OpenTelemetry logging schema OpenShift", "Lesson",
               """
  <p>OpenShift logging has lived through more than one <b>schema</b>. Older stacks emit <b>viaq</b> labels (you will see names like <code>kubernetes_namespace_name</code>, <code>kubernetes_pod_name</code>). Newer paths emit <b>OpenTelemetry</b> conventions (<code>k8s.namespace.name</code>, <code>k8s.pod.name</code>, <code>service.name</code> — dotted, semantic-conv style).</p>
  <p>The logging plugin exposes a schema switch because a query written for viaq returns <b>empty, not an error</b>, on OTel streams. Empty is the worst failure mode: users think there are no logs.</p>
  """ + code("text", '''viaq-ish:  {kubernetes_namespace_name="shop"} |= "error"
OTel-ish:  {k8s_namespace_name="shop"} |= "error"
           (exact label keys depend on the collector config)

UI job: remember the schema next to the query, or rewrite labels
when the user toggles the switch.''') + """
  <p>When you expand a line, show <b>parsed JSON</b> if present, not only the raw string. Link pod name → workload page. If a <code>trace_id</code> / <code>traceId</code> is on the line, that is the jump to traces — do not make the user copy-paste if the collector already injected it.</p>
  """ + callout("A 403 from Loki and ‘no matching streams’ must not share the same EmptyState. One is permissions. One is filters. Mixing them trains people to open tickets on the wrong team."), "topics")

    t3 = topic("lq-list", "The log list is a virtualized product, not a &lt;pre&gt;",
               "log list virtualize previous container CrashLoop", "Lesson",
               """
  <p>CrashLoop debugging is the flagship log journey: current container <b>and</b> previous container (the one that just died). If the UI only tails the new empty container, you hid the crash.</p>
  <p>Lists are huge. <b>Virtualize</b> rows (render what is on screen). Do not dump 50k <code>&lt;div&gt;</code>s. Wrap long lines; keep a monospace option. Filter chips (severity, container) should compose with the LogQL bar, not fight it.</p>
  <p>Live tail is a separate mode: a websocket or poll with pause. Pause must be obvious — otherwise the user’s scroll position is a lie.</p>
  """, "topics")
    return f'''
<section class="block" id="logql" data-search="LogQL tutorial Loki viaq OTel" data-stype="Section">
  <p class="kicker">Tutorial</p>
  <h2 class="section-title">LogQL</h2>
  <p class="lede">Selector, then line filter, then parser. Schema names differ. Empty vs 403 vs timeout are three products. That is the logging UI job in one paragraph — the rest of this section unpacks it.</p>
  {t1}{t2}{t3}
</section>
'''


def traceql() -> str:
    t1 = topic("tq-otel", "OpenTelemetry is the join key, Tempo is the store",
               "OpenTelemetry Tempo TraceQL semantic conventions", "Lesson",
               """
  <p>A <b>trace</b> is one request (or job) as a tree of <b>spans</b>: each span is work in one service (or library) with a start, duration, status, and attributes. <b>OpenTelemetry (OTel)</b> is the instrumentation + collector pipeline that produces those spans (and can also emit metrics and logs). <b>Tempo</b> is the store the OpenShift tracing UI queries. Jaeger appears in old slides; you learn Tempo.</p>
  """ + diagram("""App SDKs / auto-instr  →  OTel Collector  →  Tempo
                              (tail sample, attributes)
Metrics scrape  →  Prometheus     Logs  →  Loki
Join keys:  service.name,  k8s.*,  http.*,  trace_id""") + """
  <p><b>Semantic conventions</b> are the agreed attribute names: <code>service.name</code>, <code>k8s.namespace.name</code>, <code>http.route</code>, <code>http.status_code</code>. If two teams name the service “checkout” vs “Checkout-API,” correlation dies. The UI should show <code>service.name</code> as the primary identity, not a random process name.</p>
  <p>An <b>exemplar</b> is a trace id stuck onto a metric sample. That is how a p99 spike on a chart becomes “open this trace.” If exemplars are missing, the jump is a TraceQL search with time window + service — harder, still doable.</p>
  """ + callout("OTel is not a React library. You will not import it in the plugin. You will display the fields the collector already wrote."), "topics")

    t2 = topic("tq-lang", "TraceQL: find the slow tree, then open the waterfall",
               "TraceQL duration status resource.service.name", "Lesson",
               """
  <p>TraceQL (Tempo) picks <b>spansets</b>. The curly-brace query is “spans that match these conditions.” Duration, status, resource attributes, and span attributes are the usual knobs.</p>
  """ + code("TraceQL", '''# Slow checkouts
{ resource.service.name = "checkout" && duration > 2s }

# Failed spans on a route
{ resource.service.name = "checkout" && status = error && span.http.route = "/pay" }

# Find by attribute the logs also have
{ span.k8s.namespace.name = "shop" && duration > 1s }''') + """
  <p>Search results are a <b>table</b> (trace id, service, duration, start). Click → <b>waterfall</b>: parent/child spans on a time axis. The waterfall is UI, not another query language. You need: collapse/expand, span attributes panel, links to logs (by trace id) and to metrics (by service).</p>
  <p>Status <code>error</code> on a span is not the same as HTTP 500 on a child. Show both. Span events (exceptions) belong in the attributes drawer.</p>
  """ + diagram("""Metrics (p99) --exemplar-->  one TraceQL hit
                         -->  waterfall
                         -->  logs where trace_id = ...
Time range and namespace should survive every jump.""") + """
  <p>When is a trace the <b>wrong</b> first click? Aggregates (error <i>rate</i>, saturation) — start in metrics. A CrashLoop with no incoming request — start in logs. Traces shine when you already know “this request / this job” or “this service is slow.”</p>
  """, "topics")

    t3 = topic("tq-ui", "Waterfall performance and missing tracing",
               "trace waterfall virtualize Tempo not installed", "Lesson",
               """
  <p>A busy trace can have thousands of spans. Virtualize the waterfall. Do not layout 8k absolutely-positioned DOM nodes on first paint. Truncate with “show 500 more.”</p>
  <p>If Tempo or the tracing plugin is not installed, the Observe → Traces item should say so (or not appear). A Korrel8r trace node that 404s is a worse experience than hiding the node with copy: “Tracing UI is not installed.”</p>
  <p>Retention: Tempo may keep 24h. A jump from a 7-day metrics chart to traces must say “trace expired” instead of an empty table that looks like “no errors.”</p>
  """, "topics")
    return f'''
<section class="block" id="traceql" data-search="TraceQL OpenTelemetry Tempo waterfall" data-stype="Section">
  <p class="kicker">Tutorial</p>
  <h2 class="section-title">Traces and OpenTelemetry</h2>
  <p class="lede">Collector in the middle, Tempo as the store, TraceQL to search, waterfall to read. Semantic conventions are how metrics, logs, and traces agree on names. Jaeger is history in this UI.</p>
  {t1}{t2}{t3}
</section>
'''
