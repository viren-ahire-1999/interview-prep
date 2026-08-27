def mock() -> str:
    return r'''
<section class="block" id="mock" data-search="Mock System Design Interview" data-stype="Section">
  <p class="kicker">Timed practice</p>
  <h2 class="section-title">System Design Mock Interview Mode</h2>
  <p class="lede">Draws a random practice item (<code>data-mock</code>) from the system-design bank and backend questions. Speak the 16-step framework. Reveal answers only after you have a plan.</p>
  <div class="card" style="margin-bottom:16px">
    <p>Category
      <select id="mock-cat">
        <option value="all">All</option>
        <option value="easy">Easy</option>
        <option value="medium">Medium</option>
        <option value="hard">Hard</option>
        <option value="node">Node</option>
        <option value="distributed">Distributed</option>
        <option value="database">Database</option>
      </select>
    </p>
    <div class="status-btns">
      <button type="button" class="toggle-btn" data-start-mock="15">15-min clarify + estimate</button>
      <button type="button" class="toggle-btn" data-start-mock="30">30-min architecture</button>
      <button type="button" class="toggle-btn" data-start-mock="45">45-min system design</button>
      <button type="button" class="toggle-btn" data-start-mock="60">60-min full round</button>
    </div>
    <div id="mock-panel"><p class="stat-sub">Pick a duration. Timer starts when you click Start timer.</p></div>
  </div>
  <div class="card">
    <h3>Rubric (self-score 1–5)</h3>
    <table>
      <tr><th>Dimension</th><th>Score</th></tr>
      <tr><td>Requirements</td><td><select id="mock-r-req"><option>1</option><option>2</option><option selected>3</option><option>4</option><option>5</option></select></td></tr>
      <tr><td>Estimation</td><td><select id="mock-r-est"><option>1</option><option>2</option><option selected>3</option><option>4</option><option>5</option></select></td></tr>
      <tr><td>Architecture</td><td><select id="mock-r-arch"><option>1</option><option>2</option><option selected>3</option><option>4</option><option>5</option></select></td></tr>
      <tr><td>Data model</td><td><select id="mock-r-data"><option>1</option><option>2</option><option selected>3</option><option>4</option><option>5</option></select></td></tr>
      <tr><td>Scaling</td><td><select id="mock-r-scale"><option>1</option><option>2</option><option selected>3</option><option>4</option><option>5</option></select></td></tr>
      <tr><td>Reliability</td><td><select id="mock-r-rel"><option>1</option><option>2</option><option selected>3</option><option>4</option><option>5</option></select></td></tr>
      <tr><td>Trade-offs</td><td><select id="mock-r-trade"><option>1</option><option>2</option><option selected>3</option><option>4</option><option>5</option></select></td></tr>
      <tr><td>Communication</td><td><select id="mock-r-comms"><option>1</option><option>2</option><option selected>3</option><option>4</option><option>5</option></select></td></tr>
    </table>
    <p>Notes<br /><textarea id="mock-notes" rows="3" style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:inherit"></textarea></p>
    <p>Confidence
      <select id="mock-confidence">
        <option value="1">1</option><option value="2">2</option>
        <option value="3" selected>3</option><option value="4">4</option><option value="5">5</option>
      </select>
    </p>
    <p><button type="button" class="toggle-btn" id="save-mock">Save mock</button></p>
  </div>
  <div class="card" style="margin-top:16px"><h3>History</h3><div id="mock-history"></div></div>
</section>
'''


def progress() -> str:
    return r'''
<section class="block" id="progress" data-search="Progress Tracker Phase 3" data-stype="Section">
  <p class="kicker">localStorage atl-phase3-v1</p>
  <h2 class="section-title">Progress Tracker</h2>
  <div class="grid grid-2">
    <div class="card"><h3>Daily tasks</h3><p id="track-days">0</p></div>
    <div class="card"><h3>System design topics</h3><p id="track-sd">0</p><div class="bar"><span id="bar-cat-sd"></span></div></div>
    <div class="card"><h3>Distributed systems</h3><p id="track-dist">0</p><div class="bar"><span id="bar-cat-dist"></span></div></div>
    <div class="card"><h3>Backend / Node</h3><p id="track-backend">0</p></div>
    <div class="card"><h3>Case studies</h3><p id="track-cases">0</p></div>
    <div class="card"><h3>System-design bank</h3><p id="track-designs">0</p></div>
    <div class="card"><h3>Interview questions</h3><p id="track-qs">0</p></div>
    <div class="card"><h3>Exercises</h3><p id="track-ex">0</p></div>
    <div class="card"><h3>Mocks</h3><p id="track-mocks">0</p></div>
    <div class="card"><h3>Databases</h3><div class="bar"><span id="bar-cat-db"></span></div></div>
    <div class="card"><h3>Caching</h3><div class="bar"><span id="bar-cat-cache"></span></div></div>
    <div class="card"><h3>Messaging</h3><div class="bar"><span id="bar-cat-msg"></span></div></div>
    <div class="card"><h3>Reliability</h3><div class="bar"><span id="bar-cat-rel"></span></div></div>
  </div>
  <p style="margin-top:18px"><button type="button" class="danger-btn" id="reset-progress">Reset all Phase 3 progress</button></p>
</section>
<section class="block" id="revision" data-search="Revision spaced repetition" data-stype="Section">
  <p class="kicker">Remember on purpose</p>
  <h2 class="section-title">Revision System</h2>
  <p class="lede">Solved items review at 1 → 3 → 7 → 14 → 30 days. Attempted/failed → tomorrow. Mastered parks at 30 days.</p>
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
        ("Interview craft", [
            ("r-start", "Start a system-design interview without jumping to a library"),
            ("r-clarify", "Clarify FR/NFR and park out-of-scope"),
            ("r-est", "Estimate scale and calculate RPS with units"),
            ("r-talk", "Speak the 16-step framework from memory"),
        ]),
        ("Data", [
            ("r-api", "Design REST APIs with cursor pagination and errors"),
            ("r-sql", "Design a SQL schema with tenant_id and sensible indexes"),
            ("r-idx", "Explain why an index might not be used"),
            ("r-repl", "Explain primary/replica and replica lag"),
            ("r-shard", "Explain when sharding is premature and how you would shard"),
        ]),
        ("Distributed", [
            ("r-hard", "Explain why distributed systems are hard (partial failure, clocks)"),
            ("r-cons", "Pick consistency per workflow (payment vs like vs Jira transition)"),
            ("r-cap", "Explain CAP without the slogan"),
            ("r-cache", "Design cache-aside + invalidation + stampede control"),
            ("r-redis", "Say when Redis is the wrong store"),
            ("r-q", "Design a queue with ack, retry, DLQ"),
            ("r-kaf", "Explain what Kafka adds over a queue (replay, groups)"),
        ]),
        ("Reliability", [
            ("r-retry", "Explain retries + jitter and retry storms"),
            ("r-idem", "Design idempotency keys for a webhook"),
            ("r-cb", "Explain a circuit breaker state machine"),
            ("r-rl", "Design distributed rate limiting"),
            ("r-lock", "Refuse a distributed lock and offer an alternative"),
        ]),
        ("Product systems", [
            ("r-rt", "Design a real-time board or chat and name the fan-out"),
            ("r-up", "Design multi-GB upload with pre-signed URLs"),
            ("r-se", "Design issue search (index derived, authz in source of truth)"),
            ("r-no", "Design notifications with prefs + DLQ"),
            ("r-an", "Design analytics without querying the OLTP issue DB"),
            ("r-jira", "Design a Jira-like system for 45 minutes"),
        ]),
        ("Operate", [
            ("r-obs", "Discuss SLI/SLO and a slow-transition playbook"),
            ("r-sec", "Discuss tenant isolation, audit, token storage"),
            ("r-cost", "Name cost/scaling implications of your design"),
            ("r-fail", "Walk failure of a dependency mid-request"),
            ("r-45", "Complete a 45-minute design coherently"),
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
<section class="block" id="readiness" data-search="Phase 3 Readiness Checklist" data-stype="Section">
  <p class="kicker">Gate</p>
  <h2 class="section-title">Final Phase 3 Readiness Checklist</h2>
  <p class="lede">Check only if you can do it <i>today</i> without this file. Stay until ~85%.</p>
  <p class="stat">Score: <span id="ready-score">0%</span></p>
  <div class="bar"><span id="bar-ready-final"></span></div>
  <p id="ready-gate" class="stat-sub"></p>
  {''.join(html)}
</section>
'''


def resources() -> str:
    rows = [
        ("AWS Architecture Center", "https://aws.amazon.com/architecture/", "Reference architectures and trade-off writeups.", "Compare to your drawings; do not copy as gospel.", "Case studies", True),
        ("Google Cloud Architecture Framework", "https://cloud.google.com/architecture/framework", "Reliability, security, cost pillars.", "Same ideas as this file’s NFR table, vendor-flavored.", "Fundamentals", True),
        ("Azure Architecture Center", "https://learn.microsoft.com/azure/architecture/", "Cloud design patterns (retry, CB, queue-based load leveling).", "Pattern names you can say in interviews.", "Reliability", True),
        ("Designing Data-Intensive Applications (Kleppmann)", "https://dataintensive.net/", "Replication, partitioning, transactions, streams — the book seniors actually mean.", "Read after this file’s distributed + consistency sections. Optional depth.", "Distributed", True),
        ("High Scalability", "http://highscalability.com/", "How real companies scaled (dated but useful war stories).", "Extract constraints, not cargo-cult stacks.", "Case studies", True),
        ("PostgreSQL docs — indexes", "https://www.postgresql.org/docs/current/indexes.html", "Official index types and behavior.", "After SQL / indexing sections.", "Database", False),
        ("PostgreSQL docs — MVCC", "https://www.postgresql.org/docs/current/mvcc.html", "Isolation and vacuum at the source.", "After transactions.", "Database", True),
        ("Redis docs", "https://redis.io/docs/latest/", "Types, persistence, eviction.", "Look up commands after the Redis section.", "Caching", False),
        ("Apache Kafka docs", "https://kafka.apache.org/documentation/", "Topics, consumers, guarantees.", "After the Kafka section; don’t start here.", "Messaging", True),
        ("Node.js docs", "https://nodejs.org/docs/latest/api/", "Streams, cluster, worker_threads.", "Signatures after Node architecture.", "Backend", False),
        ("MDN HTTP caching", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching", "Cache-Control, validators.", "Connects Phase 2 frontend cache to this file’s CDN layer.", "Caching", False),
        ("OWASP Cheat Sheet Series", "https://cheatsheetseries.owasp.org/", "Auth, session, XSS — defensive.", "Optional depth beside Security.", "Security", True),
        ("Atlassian Engineering blog", "https://www.atlassian.com/blog/atlassian-engineering", "How they write about scale and reliability.", "Culture, not a question dump.", "Company", True),
        ("Atlassian Design System", "https://atlassian.design/", "Product taste.", "Optional; Phase 2 already covers frontend DS.", "Company", True),
        ("web.dev / Chrome performance", "https://web.dev/explore/performance", "INP/LCP — how backends show up in the browser.", "Connects Phase 2 vitals to TTFB and APIs.", "Frontend↔backend", True),
        ("Maria Kleppmann talks / papers index", "https://martin.kleppmann.com/", "Author site for DDIA extras.", "Optional.", "Distributed", True),
        ("AWS Well-Architected", "https://aws.amazon.com/architecture/well-architected/", "Operational excellence, reliability, cost.", "Checklist language for trade-offs.", "Operate", True),
        ("OpenTelemetry", "https://opentelemetry.io/docs/", "Traces/metrics/logs vendor-neutral.", "After Observability.", "Observability", True),
        ("Fastify docs", "https://fastify.dev/docs/latest/", "One Node framework.", "Optional implementation.", "Node", True),
        ("TanStack Query (client cache)", "https://tanstack.com/query/latest", "Frontend server-state — pair with this file’s HTTP cache.", "Phase 2 leftover. Optional.", "Frontend↔backend", True),
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
  <p><b>Phase 3 topic.</b> {topic}</p>
</article>''')
    return f'''
<section class="block" id="resources" data-search="Resource Library AWS Kafka Postgres" data-stype="Section">
  <p class="kicker">Official first</p>
  <h2 class="section-title">Resource Library</h2>
  <p class="lede">This HTML already contains the teaching. Links are for specs and vendor depth. Optional when you do not need them to finish Phase 3.</p>
  <div class="grid grid-2">{''.join(cards)}</div>
</section>
'''
