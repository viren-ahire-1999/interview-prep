from util import code, topic, diagram, callout


def fundamentals() -> str:
    t = topic("sd-what", "What system design actually is", "system design fundamentals FR NFR scalability reliability", "Fundamentals", f'''
  <p><b>Mental model.</b> System design is the craft of choosing <i>boundaries, contracts, and failure policies</i> under constraints of people, money, and physics. It is not a catalog of logos. A senior answer names the user, the critical path, the number, the thing that breaks first, and the option you rejected.</p>
  <table>
    <tr><th>Word</th><th>Means in an interview</th><th>How you measure it</th></tr>
    <tr><td>Functional</td><td>What the product does</td><td>APIs, entities, user stories</td></tr>
    <tr><td>Non-functional</td><td>How well it must do it</td><td>p99 latency, availability, RPO/RTO</td></tr>
    <tr><td>Scalability</td><td>Cost of 10× load is roughly linear, not a rewrite</td><td>RPS headroom, shard plan</td></tr>
    <tr><td>Reliability</td><td>Correct enough under failure</td><td>Error budget, retries, degradation</td></tr>
    <tr><td>Availability</td><td>Can a useful request succeed now?</td><td>nines, but define the <i>user</i> action</td></tr>
    <tr><td>Latency</td><td>Time for one request</td><td>p50/p95/p99, not the average</td></tr>
    <tr><td>Throughput</td><td>Work per second</td><td>RPS, MB/s</td></tr>
    <tr><td>Consistency</td><td>Which reads see which writes</td><td>Say the workflow, not “strong”</td></tr>
    <tr><td>Durability</td><td>A write that was acked is not lost</td><td>Replicas, fsync, backups</td></tr>
    <tr><td>Maintainability</td><td>A team can change this in a year</td><td>Boundaries, operability</td></tr>
    <tr><td>Cost</td><td>Money and engineer time</td><td>Over-provision vs on-call load</td></tr>
  </table>
  <p><b>Jira-shaped example.</b> “Transition issue” is functional. “p99 &lt; 300ms for the writer, watchers notified within 30s, never show a status the user is not allowed to see” are NFRs. If you optimize notification latency by writing the email in the request path, you have traded availability of the click for a Slack-outage-shaped failure.</p>
  {callout("Senior trade-off sentence: “I’d rather the transition succeed and the email be late than the transition fail because SES is down. That is an explicit consistency and availability choice, not a missing queue.\"", "good")}
  <p><b>Interview.</b> Start with users and the one workflow that must not be wrong. Do not start with Kubernetes.</p>
''', "topics")
    return f'''
<section class="block" id="fundamentals" data-search="System Design Fundamentals" data-stype="Section" data-cat="design">
  <p class="kicker">Foundations</p>
  <h2 class="section-title">System Design Fundamentals</h2>
  <p class="lede">You already design frontends. Phase 3 is the same judgment applied to data, networks, and other people’s failures.</p>
  {t}
</section>
'''


def framework() -> str:
    steps = [
        ("Clarify requirements", "What is in / out? Realtime? Multi-tenant? Mobile? Offline?",
         "I’ll first clarify whether consistency or availability matters more for this workflow."),
        ("Define scope", "One happy path + 2–3 must-have adjacent flows. Park the rest.",
         "I’ll treat plugins / AI / mobile as follow-ups unless you want them in scope."),
        ("Identify users", "Actors, tenants, admin vs end user, abuse cases.",
         "Who can see an issue — that constraint will shape the data model more than the cache."),
        ("Estimate scale", "DAU, RPS, peak, read/write, storage, payload size.",
         "I’ll assume peak and say if that changes the architecture. Challenge me if the number is wrong."),
        ("Define APIs", "Resources, errors, pagination, idempotency.",
         "The URL and the error model are part of the design, not decoration."),
        ("High-level architecture", "Clients → edge → app → data stores → async.",
         "I’ll draw the request path first, then the async path."),
        ("Data model", "Entities, keys, what is source of truth.",
         "Search and cache are derived. Permissions live in the source of truth."),
        ("Deep dive", "The one or two components that make this problem hard.",
         "At this scale, this component is the likely bottleneck."),
        ("Caching", "What, where, TTL, invalidation, stampede.",
         "I’d cache the read-heavy snapshot and invalidate on write — and say what stale means."),
        ("Scaling", "Vertical first, then replica, then partition if numbers demand it.",
         "I would not shard on day one unless the estimate forces it."),
        ("Reliability", "Timeouts, retries, idempotency, degradation.",
         "Retries without idempotency and jitter are how we take the site down."),
        ("Security", "AuthN/Z, tenant isolation, audit, secrets.",
         "UI hide is UX. The API enforces."),
        ("Observability", "SLI for the critical path, traces, correlation ids.",
         "I’d know how we’d debug ‘randomly slow’ next quarter."),
        ("Trade-offs", "Named alternative you rejected.",
         "I considered Kafka here; a queue is enough because we don’t need replay by multiple independent teams yet."),
        ("Bottlenecks", "What dies at 10×.",
         "The next cliff is hot partitions / connection fan-out / lock contention — pick one."),
        ("Evolution", "What you would split later.",
         "I’d start as a modular monolith and extract search when its SLO and ownership diverge."),
    ]
    html = []
    for i, (title, detail, phrase) in enumerate(steps, 1):
        html.append(f'''
<div class="comm-step">
  <div class="comm-num">{i}</div>
  <div>
    <h3 style="margin:0 0 4px;font-size:16px">{title}</h3>
    <p style="margin:0 0 8px">{detail}</p>
    <div class="say">“{phrase}”</div>
  </div>
</div>''')
    return f'''
<section class="block" id="framework" data-search="System Design Interview Framework 45 60 minute" data-stype="Section">
  <p class="kicker">How you talk</p>
  <h2 class="section-title">System Design Interview Framework</h2>
  <p class="lede">45–60 minutes is a conversation with a clock, not a textbook. Spend ~8 min clarify+estimate, ~12 min high-level, ~20 min deep dive, ~10 min failures/trade-offs. Practice questions in this file use this spine.</p>
  {''.join(html)}
  {callout("Timeboxed honesty: if you are 25 minutes in and still listing every microservice, you are failing communication — the same skill Atlassian senior loops reward.")}
</section>
'''


def estimation() -> str:
    drills = [
        ("10M users, 1M DAU, 100 req/user/day, peak = 10% of daily in 1 hour",
         "Daily req = 1e6 × 100 = 1e8. Avg RPS = 1e8 / 86400 ≈ 1,160. Peak hour req = 0.10 × 1e8 = 1e7. Peak RPS ≈ 1e7/3600 ≈ 2,780.",
         "Always state the seconds approximation: 86400 ≈ 10^5 if you need a back-of-envelope (then you get ~1,000 RPS — say you rounded)."),
        ("Jira-like: 200k DAU, 40 pages/user/day, 8 API calls/page, peak 3×",
         "Daily API = 2e5 × 40 × 8 = 6.4e7. Avg RPS ≈ 740. Peak ≈ 2,200.",
         "Pages ≠ API calls. Frontends amplify."),
        ("Comments: 5% of API writes, 2 KB each, keep 5 years, 3 replicas",
         "Writes/day = 0.05 × 6.4e7 ≈ 3.2e6. Bytes/day ≈ 6.4 GB. Year ≈ 2.3 TB. 5y ≈ 12 TB. ×3 replicas ≈ 36 TB plus indexes (~1.5–2×).",
         "Indexes and history matter. Say the multiplier."),
        ("Cache: 20% of issue reads are unique/day, 50 KB payload, 80% hit target",
         "If 50M issue reads/day and 20% unique → 10M keys × 50KB = 500 GB working set. You will not hold it all; cache the hot 5–10% (25–50 GB) and accept misses.",
         "Working set ≠ cardinality. Hot keys dominate."),
        ("Upload: 10k attachments/day, average 8 MB, 1% are 1 GB",
         "Typical bytes/day ≈ 80 GB. Tail: 100 files × 1 GB = 100 GB. Bandwidth out of origin is not the same as user upload (they hit object storage).",
         "Design the API server out of the byte path. Pre-signed PUT to object storage."),
        ("Chat: 50k concurrent WS, 1 msg/user/min, 200 byte messages, fan-out 10",
         "Ingress 50k/60 ≈ 833 msg/s. Egress 8,330 msg/s. Connections are the scarce resource, not bytes.",
         "Quote connection count and fan-out before you quote Kafka."),
        ("Search: 10% of reads, 200ms p95 budget, 2M docs",
         "Search RPS ≈ 0.1 × 740 ≈ 74 average. You still isolate it so a reindex cannot take the issue API down.",
         "Low RPS can still be a reliability island."),
        ("Multi-tenant: 5k tenants, one tenant is 30% of traffic",
         "Hot tenant is a shard/key design problem. Average RPS is a lie for that tenant.",
         "Always ask: is traffic uniform? Atlassian-like products are not."),
        ("Notifications: 1 event → 20 watchers, 10% email",
         "If 50 transitions/s → 1,000 watcher fan-out/s → 100 emails/s. That is a queue + rate limit, not a for-loop in the request.",
         "Fan-out is the number that surprises people."),
        ("Read/write 20:1 on issue GET vs PATCH",
         "Replicas help GETs. PATCHes still hit primary. Cache helps the 20, invalidation is the write cost.",
         "Read-heavy is not 'easy' if every write must wake 20 cached copies."),
    ]
    cards = []
    for i, (prompt, ans, note) in enumerate(drills, 1):
        cards.append(f'''
<article class="topic" id="est-{i}" data-search="estimation exercise {i}" data-stype="Estimation">
  <div class="meta-row"><span class="badge badge-medium">Exercise {i}</span></div>
  <h3>Estimate {i}</h3>
  <p>{prompt}</p>
  <p><button type="button" class="toggle-btn" data-toggle="est-a-{i}">Reveal answer</button>
     <button type="button" class="toggle-btn" data-complete="topics" data-cid="est-{i}">Mark complete</button></p>
  <div class="reveal" id="est-a-{i}">
    <p><b>Worked answer.</b> {ans}</p>
    <p><b>Interview note.</b> {note}</p>
  </div>
</article>''')

    body = topic("est-formulas", "Formulas and a worked 10M-user example", "capacity estimation RPS DAU storage cache", "Estimation", f'''
  <p>Write units every line. Interviewers forgive arithmetic if the method is visible.</p>
  <table>
    <tr><th>Quantity</th><th>Formula</th><th>Typical assumption to say out loud</th></tr>
    <tr><td>Daily requests</td><td>DAU × req/user/day</td><td>Req includes API, not just page views</td></tr>
    <tr><td>Average RPS</td><td>daily / 86,400</td><td>“~10^5 seconds/day”</td></tr>
    <tr><td>Peak RPS</td><td>avg × peak factor, or peak-window / seconds</td><td>2–5× if unknown; or 10% of daily in one hour</td></tr>
    <tr><td>Storage/day</td><td>writes/day × avg bytes × overhead</td><td>Overhead 1.5–3× for indexes/replicas later</td></tr>
    <tr><td>Bandwidth</td><td>RPS × response size</td><td>Separate ingress/egress and CDN offload</td></tr>
    <tr><td>Cache</td><td>hot working set, not full DB</td><td>80/20: cache the hot 20%</td></tr>
  </table>
  <p><b>Worked example.</b> 10 million registered, 1 million DAU, 100 requests/user/day, 10% of daily traffic in the peak hour, 20:1 reads, 2 KB average JSON.</p>
  {code("text", '''Daily requests     = 1e6 * 100 = 1e8
Avg RPS            = 1e8 / 86400 ≈ 1,160
Peak-hour requests = 0.10 * 1e8 = 1e7
Peak RPS           ≈ 1e7 / 3600 ≈ 2,780
Writes             ≈ 2,780 / 21 ≈ 130 WPS (if 20:1)
Read RPS           ≈ 2,650
Egress at peak     ≈ 2650 * 2KB ≈ 5.3 MB/s (tiny — payload was small)
If issue page is 80KB HTML+JSON: 2650 * 80KB ≈ 212 MB/s — now CDN matters''')}
  <p>At ~3k peak RPS a <b>modular monolith + Postgres primary + read replicas + Redis</b> is a default. You do <i>not</i> need Kafka to survive 3k RPS. You need Kafka (or a log) when multiple independent consumers, replay, or huge fan-out appear.</p>
  {callout("What happens at 10× (30k peak RPS)? Connection pools, lock contention, and a hot tenant matter before “we didn’t have Kubernetes.”")}
  ''', "topics")

    return f'''
<section class="block" id="estimation" data-search="Capacity Estimation RPS DAU storage" data-stype="Section" data-cat="design">
  <p class="kicker">Numbers</p>
  <h2 class="section-title">Capacity Estimation</h2>
  <p class="lede">A wrong number with a clear method beats a precise number with no units. Do the ten drills.</p>
  {body}
  {''.join(cards)}
</section>
'''
