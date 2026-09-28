from util import topic, diagram, callout, code


def ux() -> str:
    t1 = topic("ux-time", "The time picker is a product, not a date widget",
               "time range picker abort controller Observe", "Lesson",
               """
  <p>Every Observe surface shares a <b>time range</b> (last 5m, 1h, 6h, custom). That range is part of the user’s mental context. Jumps (metrics → logs → traces) that <b>drop the range</b> feel broken even if each page is “correct.”</p>
  <p>When the range changes:</p>
  <ol>
    <li>Abort in-flight fetches (<code>AbortController</code>). Late responses must not overwrite the new range.</li>
    <li>Reset “live tail / refresh” so you are not mixing a stream from the old window.</li>
    <li>Keep namespace, cluster, and severity filters. Only clear filters that are illegal in the new context.</li>
  </ol>
  """ + code("TS", '''const ac = useRef<AbortController | null>(null);

function runQuery(range: TimeRange, query: string) {
  ac.current?.abort();
  ac.current = new AbortController();
  return fetch(url, { signal: ac.current.signal, ... });
}''') + """
  <p>Absolute vs relative: “last 30 minutes” should keep sliding on refresh; a custom absolute range should not. Label which mode you are in. Keyboard: the picker is in the tab order before the chart.</p>
  """, "topics")

    t2 = topic("ux-states", "Empty, error, timeout, partial — four screens",
               "empty state error timeout partial query PatternFly", "Lesson",
               """
  <p>Happy-path charts are the easy third of the job. The other two thirds are states:</p>
  <table>
    <tr><th>State</th><th>Cause</th><th>UI</th></tr>
    <tr><td>Empty</td><td>Valid query, zero series/lines/spans</td><td>EmptyState: what was queried, one action (widen range, clear filter)</td></tr>
    <tr><td>Error</td><td>Parse, 400, 403</td><td>Alert with the message. 403 copy: permissions, not “no data.”</td></tr>
    <tr><td>Timeout</td><td>504, client abort after N seconds</td><td>Alert + “narrow the query” + retry. Live region for a11y.</td></tr>
    <tr><td>Partial</td><td>Thanos / Loki querier dropped a shard</td><td>Show data + warning: “12 of 40 series unavailable.”</td></tr>
  </table>
  """ + code("TSX", '''{status === "empty" && (
  <EmptyState titleText="No series in this range">
    <EmptyStateBody>
      Try the last 6 hours or drop the code="500" filter.
    </EmptyStateBody>
  </EmptyState>
)}
{status === "timeout" && (
  <Alert variant="danger" isInline title="Query timed out"
    role="status" aria-live="polite" />
)}''') + """
  """ + callout("If you only design the line chart, PM will still call the page ‘done’ and on-call will hate you. Put these four states in the first mock, not in QA."), "topics")

    t3 = topic("ux-card", "Cardinality and list size are UX bugs",
               "high cardinality virtualize series cap", "Lesson",
               """
  <p>A PromQL group-by on <code>user_id</code> can return 50k series. A log query without a namespace can scan the cluster. A trace waterfall can have 20k spans. The backend may survive. The <b>console tab will not</b>.</p>
  <ul>
    <li>Cap series drawn (e.g. top 20 by magnitude). Text: “Showing 20 of 4,812.”</li>
    <li>Refuse or warn on selectors that are obviously unbounded — do not silently freeze.</li>
    <li>Virtualize tables and waterfalls.</li>
    <li>Debounce the query bar; do not fire PromQL on every keystroke.</li>
  </ul>
  """ + diagram("""User types  →  debounce 300ms  →  validate  →  fetch (abortable)
Paint: at most N series / rows
If N exceeded: warning, not a frozen tab"""), "topics")
    return f'''
<section class="block" id="ux" data-search="Observe UX time picker empty error" data-stype="Section">
  <p class="kicker">Tutorial</p>
  <h2 class="section-title">Observe UX</h2>
  <p class="lede">The difference between a dashboard toy and this job: time range survives jumps, fetches abort, and empty/error/timeout/partial are designed. PatternFly already has EmptyState and Alert — use them.</p>
  {t1}{t2}{t3}
</section>
'''
