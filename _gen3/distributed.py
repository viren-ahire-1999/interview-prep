from util import code, topic, diagram, callout


def distributed() -> str:
    t1 = topic("dist-hard", "Why distributed systems are hard", "partial failure partitions latency clocks ordering duplication retries coordination", "Distributed", f'''
  <p><b>The lie of distribution.</b> On one machine, failure is binary: the process crashed or it did not. In a distributed system, failure is <i>partial</i> — some requests succeed, some time out, some return stale data, and you cannot tell which category you are in without extra protocol. That ambiguity is the root of most senior-design pain.</p>
  <p><b>Partial failure.</b> Your issue transition API returns 504. Did Postgres commit? Did the outbox row insert? Did the notification worker already fire? Without idempotency keys and durable workflow state, the user clicks again and you double-notify or leave the issue in “In Progress” forever. Partial failure means every step needs a defined “at-least” or “at-most” story.</p>
  <p><b>Network partitions.</b> A partition is not “the internet is down.” It is: group A can talk to the DB primary; group B can only see a replica or nothing. Both sides may still serve traffic. CAP (next section) is really about what you do <i>during</i> that window — not a permanent architectural tattoo.</p>
  <p><b>Latency is never zero.</b> Cross-AZ RTT is milliseconds; cross-region is tens to hundreds. Chatty synchronous graphs (issue service → permissions → audit → search → notify in one request) blow p99 budgets. At 10× traffic, tail latency dominates user experience more than average RPS.</p>
  <p><b>Clocks lie.</b> There is no global “now.” NTP skew, leap seconds, and VM pauses break “last-write-wins” unless you use version vectors, logical clocks, or the database’s transaction ordering. “UpdatedAt from the client” is not a conflict-resolution strategy.</p>
  <p><b>Ordering and duplication.</b> TCP gives ordered bytes between two sockets — not ordered events across services. Messages arrive twice (at-least-once). Retries reorder work. You design consumers to be idempotent and to tolerate gaps, or you pay for single-partition ordering (Kafka partition key) with hot-key cost.</p>
  <p><b>Retries without policy.</b> A retry storm during a brownout can turn a sick dependency into a dead one. Retries need budgets, jitter, idempotency, and circuit breaking — otherwise “make it reliable” becomes “take down the neighbor.”</p>
  <p><b>Coordination cost.</b> Leader election, distributed locks, and two-phase commit buy correctness at the price of latency, operability, and partition behavior. Senior answer: avoid coordination on the hot path; use leases, database constraints, or partition the problem so one writer owns the entity.</p>
  {diagram("""Request path (happy):
  Client → LB → Issue API → Postgres primary → 200

Same request (partial failure):
  Client → LB → Issue API → Postgres (commit OK)
                         → Search index (timeout)
                         → ??? Did user see success? Is index stale? Will retry duplicate?""")}
  {callout("Interview sentence: “I assume partial failure on every hop. Timeouts define uncertainty; idempotency and durable state define what we do after uncertainty.”", "good")}
''', "distTopics")

    t2 = topic("dist-fallacies", "Fallacies of distributed computing — taught, not listed", "fallacies network reliable latency bandwidth topology administrator secure homogeneous", "Distributed", f'''
  <p>These are not trivia. Each fallacy is a design mistake that becomes a production incident at scale.</p>
  <table>
    <tr><th>Fallacy</th><th>What people assume</th><th>What actually happens (Jira-shaped)</th><th>Design response</th></tr>
    <tr><td>Network is reliable</td><td>RPC either works or throws</td><td>Silent hangs, half-open connections, “success” after client timeout</td><td>Deadlines, bounded retries, async completion, user-visible pending state</td></tr>
    <tr><td>Latency is zero</td><td>Another internal call is free</td><td>Issue page N+1 across 6 services → p99 explodes</td><td>BFF aggregation, batch APIs, cache, push work async</td></tr>
    <tr><td>Bandwidth is infinite</td><td>Ship full issue graphs every time</td><td>Mobile clients on bad Wi‑Fi; egress bills</td><td>Pagination, field masks, delta sync, CDN for attachments</td></tr>
    <tr><td>Network is secure</td><td>Internal VPC == trusted</td><td>Compromised pod, SSRF, tenant bleed</td><td>mTLS/S2S auth, tenant_id on every query, zero-trust between services</td></tr>
    <tr><td>Topology doesn’t change</td><td>Fixed list of service IPs</td><td>Autoscaling, AZ fail-over, deploy churn</td><td>Service discovery, health checks, avoid sticky IP assumptions</td></tr>
    <tr><td>One administrator</td><td>Ops fixes the network</td><td>Partial partitions, misconfigured SG, DNS TTL</td><td>Graceful degradation, multi-AZ, runbooks for split-brain</td></tr>
    <tr><td>Transport cost is zero</td><td>Serialization is cheap</td><td>Large comment threads JSON-serialized per watcher fan-out</td><td>Event payloads by reference (issue id), compress, stream</td></tr>
    <tr><td>Homogeneous network</td><td>Everyone has same RTT</td><td>APAC user hits US-East primary</td><td>Read replicas near user, edge cache, async writes with RYW contract</td></tr>
  </table>
  <p><b>At 10×.</b> Fallacies stop being “edge cases.” A 1% packet loss × 20 chained calls ≈ meaningful user-visible error rate. Design for failure per hop, not for the demo path.</p>
  {callout("Verbal drill: pick “latency is zero” and explain how a board load would violate it — without saying “microservices bad.”")}
''', "distTopics")

    t3 = topic("dist-retries-idem", "Retries, duplication, and idempotency on the wire", "retries idempotency at-least-once duplicate delivery jitter", "Distributed", f'''
  <p><b>Duplication is the default.</b> TCP may not duplicate, but HTTP retries, message queues, and mobile clients do. Treat every write as “may arrive twice.”</p>
  {code("typescript", """// Unsafe: double transition if client retries 504
async function transition(issueId: string, to: string) {
  await db.query('UPDATE issues SET status = $1 WHERE id = $2', [to, issueId]);
}

// Safer: idempotency key + unique constraint
async function transitionIdempotent(issueId: string, to: string, key: string) {
  await db.query(
    `INSERT INTO transitions (issue_id, to_status, idempotency_key)
     VALUES ($1, $2, $3)
     ON CONFLICT (idempotency_key) DO NOTHING`,
    [issueId, to, key]
  );
  // apply from transitions table in one transaction
}""")}
  <p><b>Retry policy.</b> Max attempts, exponential backoff with jitter, retry only idempotent operations or only on known-safe errors (408, 429, 503 with Retry-After). Never retry 400-class business failures blindly.</p>
  <p><b>Cost.</b> Retries multiply load on a degraded system — the reason circuit breakers and load shedding exist. “We’ll just retry three times” without jitter is how Jira-shaped outages become company-wide.</p>
''', "distTopics")

    return f'''
<section class="block" id="distributed" data-search="Distributed Systems Partial Failure Partitions" data-stype="Section" data-cat="distributed">
  <p class="kicker">Hard truths</p>
  <h2 class="section-title">Distributed Systems Fundamentals</h2>
  <p class="lede">Phase 3 is not “draw Kafka.” It is naming what breaks when the happy path is only 95% of requests — and choosing contracts that survive the other 5%.</p>
  {t1}
  {t2}
  {t3}
</section>
'''


def consistency() -> str:
    t1 = topic("cons-models", "Consistency models — what the user actually experiences", "strong eventual read-your-writes monotonic reads causal consistency", "Consistency", f'''
  <p><b>Stop saying “strong” without a workflow.</b> Consistency is a promise between writes and reads for a <i>defined scope</i> — not a database brand. Interviewers want: who reads what, how stale is acceptable, and what you do when the promise breaks.</p>
  <table>
    <tr><th>Model</th><th>Promise</th><th>Typical mechanism</th><th>Cost</th></tr>
    <tr><td>Strong (linearizable for a key)</td><td>After ack, all reads see the write</td><td>Single leader, sync replication, or consensus</td><td>Latency, partition fragility</td></tr>
    <tr><td>Eventual</td><td>Replicas converge if writes stop</td><td>Async replication, CRDTs, cache TTL</td><td>Stale reads, conflict resolution</td></tr>
    <tr><td>Read-your-writes (RYW)</td><td>I see my own edits</td><td>Sticky session to primary, token routing, client version check</td><td>Routing complexity</td></tr>
    <tr><td>Monotonic reads</td><td>I never go “back in time” on refresh</td><td>Session stickiness to one replica, version per session</td><td>Replica load imbalance</td></tr>
    <tr><td>Causal</td><td>Cause happens before effect for related ops</td><td>Version vectors, logical timestamps</td><td>Metadata per write, merge logic</td></tr>
  </table>
  <p><b>Causal vs eventual.</b> Eventual allows comment B to appear before comment A even if A was written first globally. Causal preserves “reply to comment A” ordering relative to A — often enough for threads without paying full strong consistency on the whole issue graph.</p>
  {callout("Senior move: “For issue title we need RYW after save; for watcher count eventual ± few seconds is fine — different promises on the same page.”", "good")}
''', "distTopics")

    t2 = topic("cons-products", "Where strong vs eventual — real product examples", "payments likes comments notifications inventory profile Jira issue tracking", "Consistency", '''
  <table>
    <tr><th>Workflow</th><th>Consistency target</th><th>Why</th><th>Failure if wrong</th></tr>
    <tr><td>Payments / billing seat</td><td>Strong + idempotent</td><td>Money and entitlement are not “eventually correct”</td><td>Double charge, wrong plan</td></tr>
    <tr><td>Inventory / seat cap (hard limit)</td><td>Strong or careful reservation</td><td>Oversell is a support and legal incident</td><td>Sold 101 seats with cap 100</td></tr>
    <tr><td>Jira issue transition + permissions</td><td>Strong on authz path; RYW on status</td><td>User must not see illegal state; after click, board should reflect move</td><td>SEC-1 style wrong status; retry duplicates</td></tr>
    <tr><td>Comments on an issue</td><td>Causal / RYW for author; eventual for others</td><td>Author expects their comment; others tolerate sub-second lag</td><td>“Ghost comment” or missing reply order</td></tr>
    <tr><td>Likes / reaction counts</td><td>Eventual</td><td>Approximate count is UX-acceptable</td><td>Off by one briefly — rarely escalates</td></tr>
    <tr><td>Notifications badge</td><td>Eventual</td><td>Fan-out is async; badge is hint not ledger</td><td>Stale badge — refresh fixes</td></tr>
    <tr><td>User profile avatar / display name</td><td>RYW for editor; eventual CDN</td><td>Editor sees upload; global propagation can lag</td><td>Old avatar in one region briefly</td></tr>
    <tr><td>Search index of issues</td><td>Eventual (bounded lag SLA)</td><td>Derived view; source of truth is OLTP</td><td>Issue missing from search for 30s — document SLA</td></tr>
    <tr><td>Analytics / audit trail</td><td>Eventual ingest; durable append</td><td>Not on critical click path</td><td>Dashboard lag, not user blocker</td></tr>
  </table>
  <p><b>Jira board load.</b> Issue cards can be eventually consistent with the DB if you invalidate cache on write and accept replica lag for non-editors. The user who dragged the card needs RYW — route their reads to primary or return the new column in the PATCH response and optimistically merge client-side <i>with a version field</i> for conflict detection.</p>
  <p><b>10× traffic.</b> Strong everywhere does not scale linearly. You tighten consistency only on entities where the business pays for it (money, permissions, workflow guards) and loosen elsewhere (counts, search, notifications).</p>
''', "distTopics")

    t3 = topic("cons-implement", "Implementing promises — not just naming them", "read replica lag sticky session version vector cache invalidation", "Consistency", f'''
  <p><b>Read-your-writes patterns.</b></p>
  <ul>
    <li><b>Return written state in the response</b> — PATCH transition returns full issue; client does not need a follow-up GET.</li>
    <li><b>Session stickiness to primary</b> — simple, breaks with large pools; say the trade-off.</li>
    <li><b>Read-after-write token</b> — server returns <code>read_token=42</code>; next GET sends it; router picks replica ≥ 42.</li>
    <li><b>Client version</b> — <code>If-None-Match</code> / issue <code>version</code> field; 409 on conflict.</li>
  </ul>
  {code("text", """Issue PATCH response carries truth:
  { "id": "J-1", "status": "Done", "version": 17 }

Board GET may come from cache/replica:
  - Editor: merge version 17 locally or force primary read for 2s
  - Teammate: stale card up to TTL/replica lag — OK if SLA says so""")}
  {callout("Anti-pattern: “We use strong consistency” while reading from async replica with no routing story — that is eventual with extra steps.", "warn")}
''', "distTopics")

    return f'''
<section class="block" id="consistency" data-search="Consistency Strong Eventual Read Your Writes Causal" data-stype="Section" data-cat="distributed">
  <p class="kicker">Promises</p>
  <h2 class="section-title">Consistency Models</h2>
  <p class="lede">Consistency is per workflow. The same issue page mixes strong permissions, causal comments, and eventual search — say which is which.</p>
  {t1}
  {t2}
  {t3}
</section>
'''


def cap() -> str:
    t1 = topic("cap-defined", "CAP — what it actually says", "CAP consistency availability partition tolerance theorem", "CAP", f'''
  <p><b>Not a slogan.</b> CAP (Brewer, formalized by Gilbert–Lynch) says: during a <i>network partition</i>, a distributed data store cannot simultaneously provide both linearizable consistency (C) and total availability (A) for every request. You must choose to sacrifice one for the duration of the partition.</p>
  <p><b>C — Consistency (linearizability).</b> All clients see a single ordered timeline of operations. Not “ACID in one Postgres” alone — CAP is about replicated/shared data across nodes when messages are lost or delayed.</p>
  <p><b>A — Availability.</b> Every request to a non-failing node gets a response (not an error) in finite time. Note: a timeout from the client’s view is unavailability even if the server eventually answers.</p>
  <p><b>P — Partition tolerance.</b> The system continues despite arbitrary message loss or delay between nodes. In real clouds, partitions happen — switch misconfig, AZ isolation, cable cut, GC pause causing heartbeat miss. <i>You do not opt out of P in production.</i></p>
  {diagram("""Normal operation (no partition):
  [App] --write--> [Leader DB] --sync replicate--> [Follower]
  [App] --read-->  [Follower OK if linearizable policy allows]

Partition (Leader reachable from AZ-a, not AZ-b):
  AZ-a apps: still talk to Leader
  AZ-b apps: see Follower only — stale? elect new leader? refuse writes?

CAP question: during partition, do AZ-b clients get
  CP: error / read-only until quorum (forfeit A)
  AP: accept writes/reads on both sides (forfeit C — merge later)""")}
  <p><b>Why partitions happen.</b> Not only “region down.” Common causes: asymmetric routing, overloaded link, deployment blip, DNS stale, firewall rule, replica lag mistaken for health. Any distributed store with multiple nodes will hit split-brain risk without quorum rules.</p>
''', "distTopics")

    t2 = topic("cap-cp-ap", "CP vs AP — examples and misconceptions", "CP AP etcd zookeeper cassandra dynamo redis cluster split brain", "CAP", f'''
  <table>
    <tr><th>Lean</th><th>Behavior under partition</th><th>Example systems / patterns</th><th>Product fit</th></tr>
    <tr><td>CP</td><td>Refuse or degrade writes/reads without quorum</td><td>ZooKeeper/etcd, Consul, traditional sync-replicated SQL primary</td><td>Leader election, payment ledger, strict workflow lock</td></tr>
    <tr><td>AP</td><td>Stay available on both sides; resolve conflicts later</td><td>Dynamo-style stores, Cassandra tunable, multi-master with LWW</td><td>Shopping cart, likes, session prefs, badge counts</td></tr>
  </table>
  <p><b>Jira-shaped classification.</b></p>
  <ul>
    <li><b>Issue permission check</b> — CP bias: better fail closed (“cannot verify role”) than allow unauthorized transition.</li>
    <li><b>Notification fan-out queue depth</b> — AP bias: deliver later; don’t block the transition click.</li>
    <li><b>Global issue key uniqueness</b> — CP on allocate (DB primary or consensus); not “two regions invent PROJ-123.”</li>
  </ul>
  <p><b>Misconception 1: “Pick 2 of 3 forever.”</b> CAP applies <i>during a partition event</i>. Normal operation can be both consistent and available. Design is: what is your partition mode?</p>
  <p><b>Misconception 2: “CA systems exist.”</b> Without P, it is a single node — not distributed. RDBMS on one server is CA until you replicate.</p>
  <p><b>Misconception 3: “AP means no consistency ever.”</b> AP means availability during partition; you still add RYW, causal merges, and CRDTs after.</p>
  <p><b>Misconception 4: “CP means always down in partition.”</b> CP often means minority partition read-only/unavailable for writes; majority continues with quorum.</p>
  {callout("Interview line: “We’re not CAP-tagging the whole company AP. This workflow is CP on entitlement, AP on notifications, with explicit merge and idempotency rules.”", "good")}
''', "distTopics")

    t3 = topic("cap-practice", "Partition drills — what you would do", "quorum split brain merge conflict resolution", "CAP", '''
  <p><b>Drill.</b> Two AZs lose connectivity for 90s. Primary in AZ-a; replica promoted in AZ-b by automation mistake. Both accept writes.</p>
  <p><b>CP response.</b> Require quorum for writes (odd number of nodes); AZ-b without quorum rejects writes; ops fix routing; no split-brain writes.</p>
  <p><b>AP response.</b> Both accept; issue versions diverge; merge with version vectors or last-write-wins + audit; user may see conflict UI.</p>
  <p><b>Cost.</b> CP → short write unavailability, simpler mental model for money/perms. AP → no hard stop, expensive conflict tooling and support.</p>
  <p><b>10×.</b> More nodes ≠ safer. More nodes = more partition scenarios. Prefer odd quorum, fencing tokens, and “source of truth is primary” over clever multi-master unless product demands it.</p>
''', "distTopics")

    return f'''
<section class="block" id="cap" data-search="CAP Theorem Consistency Availability Partition CP AP" data-stype="Section" data-cat="distributed">
  <p class="kicker">During a split</p>
  <h2 class="section-title">CAP — Not a Slogan</h2>
  <p class="lede">Partitions are guaranteed. The question is what your system does for the 60 seconds the network lies — not which triangle letter you tattoo on the architecture poster.</p>
  {t1}
  {t2}
  {t3}
</section>
'''


def caching() -> str:
    t1 = topic("cache-layers", "Cache layers — browser to database", "browser CDN application Redis database cache", "Caching", '''
  <table>
    <tr><th>Layer</th><th>What it caches</th><th>Invalidation</th><th>Jira-shaped example</th></tr>
    <tr><td>Browser</td><td>Static assets, ETag on GET</td><td>Cache-Control, hash in filename</td><td>Frontend bundle, icons</td></tr>
    <tr><td>CDN</td><td>Static + cacheable API GETs at edge</td><td>Short TTL, purge on deploy, private data never shared</td><td>Public attachment thumbs; not issue JSON with PII</td></tr>
    <tr><td>Application (in-process)</td><td>Hot config, permission bitmaps</td><td>TTL + pub/sub invalidation</td><td>Project role map — watch memory per pod</td></tr>
    <tr><td>Redis (shared)</td><td>Issue snapshots, board columns, rate limits</td><td>Explicit delete on write, TTL backup</td><td>Issue PROJ-42 JSON, board sprint view</td></tr>
    <tr><td>Database buffer pool</td><td>Pages / rows</td><td>Automatic</td><td>You still need app cache for cross-request hot keys</td></tr>
  </table>
  <p><b>Why layer.</b> Each layer buys different TTL and hit ratio. Issue detail might be Redis 60s + CDN none (auth). Static field config might be CDN 1h. Caching the wrong layer (PII in CDN) is a security incident, not a performance win.</p>
''', "distTopics")

    t2 = topic("cache-patterns", "Patterns — aside, read-through, write-through, write-back, refresh-ahead", "cache aside read through write through write back refresh ahead", "Caching", f'''
  <table>
    <tr><th>Pattern</th><th>Flow</th><th>Pros</th><th>Cons</th></tr>
    <tr><td>Cache-aside</td><td>App reads cache; on miss, read DB, populate cache</td><td>Simple; app controls keys</td><td>Stampede on miss; app must invalidate on write</td></tr>
    <tr><td>Read-through</td><td>Cache library loads from DB on miss</td><td>Centralized load logic</td><td>Same stampede risk without locking</td></tr>
    <tr><td>Write-through</td><td>Write goes to cache + DB together</td><td>Cache always warm for writes</td><td>Write latency; cache stores cold keys too</td></tr>
    <tr><td>Write-back</td><td>Write to cache; async flush to DB</td><td>Fast writes</td><td>Data loss window; complexity — rare for issue source of truth</td></tr>
    <tr><td>Refresh-ahead</td><td>Proactively refresh before TTL expiry</td><td>Smoother p99 for hot keys</td><td>Wasted refresh if key goes cold</td></tr>
  </table>
  <p><b>Jira issue + board.</b> Cache-aside for issue detail: GET Redis → miss → Postgres → set Redis with TTL 120s. On PATCH transition: update Postgres, <code>DEL issue:{{id}}</code>, <code>DEL board:{{projectId}}:sprint:{{sid}}</code> (or version bump). Board snapshot is read-heavy; invalidate on any issue move in that board — narrow invalidation beats flushing entire project.</p>
  {code("text", """Write path (cache-aside):
  PATCH /issues/J-1  →  TX on primary  →  DEL cache keys  →  200 + body

Read path:
  GET /issues/J-1  →  Redis GET  →  hit: return
                              →  miss: SELECT, SET EX 120, return""")}
''', "distTopics")

    t3 = topic("cache-failures", "TTL, invalidation, stampede, penetration, avalanche, hot keys", "cache stampede penetration avalanche hot key TTL invalidation", "Caching", f'''
  <ul>
    <li><b>TTL</b> — safety net when invalidation misses a path; not a substitute for delete-on-write on hot entities.</li>
    <li><b>Invalidation</b> — hard part is fan-out: one issue change may touch issue, board, search facet, permission cache. Document key naming up front.</li>
    <li><b>Cache stampede</b> — hot key expires; 500 pods miss together. Fix: single-flight lock, jittered TTL, refresh-ahead, stale-while-revalidate.</li>
    <li><b>Cache penetration</b> — requests for non-existent ids (scrapers). Fix: short TTL null cache, bloom filter, validate id format.</li>
    <li><b>Cache avalanche</b> — many keys expire same second (deploy reset TTL). Fix: jitter per key, stagger warmup.</li>
    <li><b>Hot keys</b> — viral issue, CEO’s project. Fix: local L1, read replicas, split key read-only copies, request coalescing.</li>
  </ul>
  <p><b>When cache dies at 10×.</b> Every request hits Postgres. Connection pool exhausts, p99 → seconds, retries amplify. Mitigations: circuit breaker to partial JSON, shed non-critical fields, pre-warm after Redis fail-over, rate limit anonymous reads.</p>
  {callout("Say out loud: “TTL is backup; invalidation on write is the contract. Stale board for 2s is OK; stale permissions is not — don’t cache authz without tight TTL + invalidation.”", "good")}
''', "distTopics")

    return f'''
<section class="block" id="caching" data-search="Caching CDN Redis Cache Aside Stampede Invalidation" data-stype="Section" data-cat="caching">
  <p class="kicker">Layers & patterns</p>
  <h2 class="section-title">Caching Patterns</h2>
  <p class="lede">Caching is a consistency decision with a hit ratio. Name what stale means before you name Redis.</p>
  {t1}
  {t2}
  {t3}
</section>
'''


def redis() -> str:
    t1 = topic("redis-types", "Data types and primitives", "Redis string hash set sorted set list TTL pub sub", "Redis", f'''
  <table>
    <tr><th>Type</th><th>Operations</th><th>Use when</th></tr>
    <tr><td>String</td><td>GET/SET/INCR/SETNX</td><td>Simple cache value, counters, idempotency flag</td></tr>
    <tr><td>Hash</td><td>HGET/HSET on fields</td><td>Session fields, object with partial updates</td></tr>
    <tr><td>Set</td><td>SADD/SMEMBERS</td><td>Unique online users on board, tag sets</td></tr>
    <tr><td>Sorted Set (ZSet)</td><td>ZADD/ZRANGE by score</td><td>Leaderboards, time-ordered activity (score=timestamp)</td></tr>
    <tr><td>List</td><td>LPUSH/BRPOP</td><td>Simple queues (prefer dedicated queue at scale)</td></tr>
    <tr><td>TTL / EXPIRE</td><td>Automatic eviction</td><td>Sessions, rate windows, lock leases</td></tr>
    <tr><td>Pub/Sub</td><td>Fan-out messages (fire-and-forget)</td><td>Cache invalidation signals — not durable event log</td></tr>
  </table>
  {code("text", """Session (Hash):
  HSET session:abc user_id 42 tenant_id acme ttl refreshed_at ...

Rate limit (String INCR + EXPIRE):
  INCR rl:{tenant}:{user}:202608261430
  EXPIRE ... 60

Leaderboard (ZSet):
  ZADD sprint:42:points 150 user:7  120 user:3

Idempotency (String SETNX):
  SET idem:{key} 1 NX EX 86400""")}
''', "distTopics")

    t2 = topic("redis-usecases", "Use cases — cache, sessions, rate limit, locks, leaderboards", "Redis session rate limit distributed lock leaderboard counter", "Redis", '''
  <ul>
    <li><b>Cache</b> — issue JSON, permission bitmap; always have DB fallback; never cache secrets without encryption.</li>
    <li><b>Sessions</b> — fast, TTL, revocable; pair with httpOnly cookie; consider sticky-less pods.</li>
    <li><b>Rate limiting</b> — fixed window INCR or sliding with ZSet; cluster-wide; fail-open vs fail-closed is a product call.</li>
    <li><b>Distributed locks</b> — Redlock-style with lease + fencing token if you must; prefer DB row lock or partition-by-issue-id worker.</li>
    <li><b>Leaderboards / counters</b> — INCR and ZADD are O(1)/log N; good for gamification, sprint points.</li>
    <li><b>Pub/Sub invalidation</b> — “drop issue:J-1 on all app nodes” — subscribers can miss messages; not a job queue.</li>
  </ul>
  <p><b>10×.</b> Memory cost dominates. 50 KB × 10M warm keys ≈ 500 GB — you shard Redis Cluster or trim payloads. Hot keys still exist in cluster; use hashtags or local merge.</p>
''', "distTopics")

    t3 = topic("redis-not", "When Redis is NOT appropriate", "Redis source of truth complex queries huge dataset persistence", "Redis", f'''
  <ul>
    <li><b>Source of truth for issues</b> — durability, complex queries, joins, audit — Postgres (or your OLTP) owns this. Redis is a derived cache or ephemeral state.</li>
    <li><b>Huge datasets that don’t fit memory</b> — full issue history search belongs in OLTP + search index, not Redis strings.</li>
    <li><b>Complex queries</b> — “all issues where custom field X > Y across tenant” — SQL/ES, not SCAN keys.</li>
    <li><b>Durable job processing</b> — use SQS/Rabbit/Kafka; Redis lists lose messages on crash unless Streams with care — ops cost still higher than purpose-built queue.</li>
    <li><b>Multi-key ACID across entities</b> — Redis transactions are limited; cross-issue saga belongs in DB or outbox.</li>
  </ul>
  {callout("Senior refusal: “I would not store issue bodies only in Redis because restart + eviction + no ad-hoc query is an ops and compliance risk. Redis accelerates reads; Postgres remains truth.”", "good")}
''', "distTopics")

    return f'''
<section class="block" id="redis" data-search="Redis Hash Set ZSet TTL Pub Sub Sessions Rate Limit" data-stype="Section" data-cat="caching">
  <p class="kicker">In-memory, on purpose</p>
  <h2 class="section-title">Redis</h2>
  <p class="lede">Redis is a fast data structure server — not a smaller Postgres. Pick the type to match access pattern and accept memory + durability limits.</p>
  {t1}
  {t2}
  {t3}
</section>
'''


def queues() -> str:
    t1 = topic("queue-basics", "Producer, consumer, ack, retry, DLQ, visibility", "message queue producer consumer ack retry DLQ visibility timeout", "Queues", f'''
  <p><b>Core loop.</b> Producer enqueues work; consumer processes; broker tracks in-flight state. Decouples peak (transition clicks) from slow side effects (email, webhooks, index updates).</p>
  <table>
    <tr><th>Concept</th><th>Meaning</th><th>Failure without it</th></tr>
    <tr><td>Ack</td><td>Consumer confirms success; message deleted</td><td>Duplicate or lost work depending on broker</td></tr>
    <tr><td>Visibility timeout</td><td>Message hidden while processing; reappears if worker dies</td><td>Stuck messages or double process — tune vs p99 job time</td></tr>
    <tr><td>Retry</td><td>Requeue with backoff on transient error</td><td>Poison message loops — cap attempts</td></tr>
    <tr><td>DLQ (dead letter queue)</td><td>Park failed messages for inspection</td><td>Silent drop or infinite retry storm</td></tr>
  </table>
  {diagram("""Comment notification pipeline:
  Transition API → enqueue {issueId, watcherIds, eventId}
  Worker → send email → ack
  Worker crash mid-send → visibility expires → retry
  Bad payload / permanent 4xx → DLQ + alert""")}
  <p><b>Ordering.</b> Single consumer preserves order; multiple consumers generally do not unless partitioned (partition key = issue id).</p>
''', "distTopics")

    t2 = topic("queue-semantics", "At-least-once, at-most-once, exactly-once — what you actually build", "at least once at most once exactly once delivery semantics idempotent", "Queues", f'''
  <table>
    <tr><th>Semantics</th><th>Real meaning</th><th>How</th></tr>
    <tr><td>At-most-once</td><td>May lose message; never duplicate</td><td>Fire-and-forget, no retry — rare for important work</td></tr>
    <tr><td>At-least-once</td><td>Default for queues with ack + retry</td><td>Idempotent consumer + dedupe key</td></tr>
    <tr><td>Exactly-once</td><td>Effect once end-to-end</td><td>Not a wire property — idempotent writes + transactional outbox + dedupe store, or Kafka transactions with cost</td></tr>
  </table>
  <p><b>Interview honesty.</b> “We implement at-least-once delivery with idempotent handlers keyed by eventId.” That is senior. “Exactly-once Kafka” without consumer design is not.</p>
  {code("typescript", """async function handleNotification(evt: { eventId: string; issueId: string }) {
  const inserted = await db.query(
    'INSERT INTO processed_events (event_id) VALUES ($1) ON CONFLICT DO NOTHING RETURNING 1',
    [evt.eventId]
  );
  if (!inserted.rowCount) return; // duplicate delivery — safe no-op
  await sendEmail(evt);
}""")}
''', "distTopics")

    t3 = topic("queue-compare", "Kafka vs RabbitMQ vs SQS-like vs pub/sub", "Kafka RabbitMQ SQS compare message broker trade-offs", "Queues", '''
  <table>
    <tr><th>System</th><th>Shape</th><th>Strengths</th><th>Weaknesses / cost</th></tr>
    <tr><td>SQS-like</td><td>Managed queue, visibility timeout</td><td>Ops-simple, scales, DLQ built-in</td><td>No replay log; ordering only FIFO shards; cross-consumer replay hard</td></tr>
    <tr><td>RabbitMQ</td><td>Broker routes to queues, ack, DLX</td><td>Flexible routing, classic task queues</td><td>Broker can be bottleneck; clustering ops; not a long retention log</td></tr>
    <tr><td>Kafka</td><td>Distributed commit log + consumer groups</td><td>Replay, multiple independent consumers, high throughput</td><td>Ops heavy, partition design, not a job queue with per-message ack semantics alone</td></tr>
    <tr><td>Pub/Sub (Redis/NATS)</td><td>Fan-out, no persistence default</td><td>Low latency signals</td><td>Missed messages if offline — not work queue</td></tr>
  </table>
  <p><b>Choose queue when</b> task disappears after success, workers compete, job volume spiky (send 10k emails). <b>Choose log when</b> audit, analytics, search indexer, and billing each need same event stream at different speeds.</p>
  <p><b>Jira comment notify.</b> Start SQS/Rabbit — one consumer group, idempotent send. Add Kafka when compliance wants 7-day replay for new “slack integration” consumer without touching the producer.</p>
''', "distTopics")

    return f'''
<section class="block" id="queues" data-search="Message Queue Ack Retry DLQ At Least Once" data-stype="Section" data-cat="messaging">
  <p class="kicker">Async work</p>
  <h2 class="section-title">Message Queues</h2>
  <p class="lede">Queues move work off the click path. Delivery guarantees are implemented in consumers — brokers only give you primitives.</p>
  {t1}
  {t2}
  {t3}
</section>
'''


def kafka() -> str:
    t1 = topic("kafka-core", "Topics, partitions, producers, consumer groups, offsets", "Kafka topic partition producer consumer group offset replication", "Kafka", f'''
  <table>
    <tr><th>Term</th><th>What it is</th><th>Design lever</th></tr>
    <tr><td>Topic</td><td>Named log category</td><td><code>issue-events</code>, <code>audit</code></td></tr>
    <tr><td>Partition</td><td>Ordered append-only shard of topic</td><td>Parallelism unit; ordering only per partition</td></tr>
    <tr><td>Producer</td><td>Appends records with key optional</td><td>Key → hash → partition (issue id keeps issue events ordered)</td></tr>
    <tr><td>Consumer group</td><td>Cooperative consumers share partitions</td><td>Each partition → one consumer in group at a time</td></tr>
    <tr><td>Offset</td><td>Position in partition log</td><td>Commit after process → at-least-once if crash before commit</td></tr>
    <tr><td>Retention</td><td>Time/size bound keep log</td><td>Replay window vs disk cost</td></tr>
    <tr><td>Replication</td><td>Leader + followers per partition</td><td>ISR, acks=all for durability</td></tr>
  </table>
  {diagram("""Topic issue-events (3 partitions):
  P0: [e1, e4, e7]   key hash issue-1, issue-4...
  P1: [e2, e5]
  P2: [e3, e6]

Consumer group search-indexers: each partition read by one worker
Consumer group analytics: independent offsets — replay same log""")}
''', "distTopics")

    t2 = topic("kafka-behavior", "Ordering, scaling, replay, lag, delivery semantics", "Kafka ordering replay consumer lag exactly once issue events", "Kafka", f'''
  <ul>
    <li><b>Ordering</b> — guaranteed per partition, not global topic. All events for <code>issue-42</code> need key=<code>issue-42</code>; cross-issue order undefined — usually fine.</li>
    <li><b>Scaling</b> — more partitions → more parallel consumers up to partition count. Too many small partitions → overhead. Hot partition if one mega-project dominates keys.</li>
    <li><b>Replay</b> — reset offset or new consumer group reads history — killer feature vs classic queue.</li>
    <li><b>Consumer lag</b> — records behind real time; alert on lag SLA. Fix: scale consumers (≤ partitions), optimize handler, reject oversized messages.</li>
    <li><b>Delivery</b> — at-least-once default (commit after process). Exactly-once needs idempotent producer + transactions + cooperating sink — expensive; often idempotent consumer is enough.</li>
  </ul>
  <p><b>Design example — issue events.</b> Event envelope: <code>{{ eventId, issueId, type, version, payload, occurredAt }}</code>. Partition key = <code>issueId</code>. Search indexer updates doc; notification service filters watchers; audit appends immutable record. New consumer “ML summarizer” joins months later — reads from retention without producer change.</p>
  <p><b>What Kafka solves vs a queue.</b> Multiple independent readers, ordered shard, durable replay, backpressure via log retention. <b>Operational cost.</b> Cluster tuning, rebalances, schema governance, monitoring lag — don’t pay it for 200 notifications/sec.</p>
''', "distTopics")

    t3 = topic("kafka-when", "When to adopt and when to refuse", "Kafka operational cost when not to use Kafka", "Kafka", f'''
  <p><b>Adopt when</b> several teams consume same event stream, replay is a requirement, throughput &gt; single broker queue comfortably, event sourcing/audit trail is first-class.</p>
  <p><b>Refuse (for now) when</b> one background worker drains tasks, no replay, &lt; few k msgs/sec, team lacks ops — SQS/Rabbit + outbox is simpler.</p>
  <p><b>Failure modes.</b> Rebalance storm during deploy, poison message blocking partition if handler throws without skip, disk full on retention misconfig, producer without idempotency duplicates on retry.</p>
  {callout("Trade-off sentence: “Kafka earns its keep when the second and third consumer appear. For comment email only, I’d use a queue and transactional outbox first.”", "good")}
''', "distTopics")

    return f'''
<section class="block" id="kafka" data-search="Kafka Partition Consumer Group Offset Retention Replay" data-stype="Section" data-cat="messaging">
  <p class="kicker">Commit log</p>
  <h2 class="section-title">Kafka / Event Streaming</h2>
  <p class="lede">Kafka is a distributed log with consumer groups — not a drop-in replacement for every queue. Partition keys and offset policy <i>are</i> your design.</p>
  {t1}
  {t2}
  {t3}
</section>
'''


def pubsub() -> str:
    t1 = topic("pubsub-models", "Pub/sub vs queue vs log", "pub sub fan out queue log notifications work distribution", "Pub/Sub", f'''
  <table>
    <tr><th>Pattern</th><th>Delivery</th><th>Consumer relationship</th><th>Best for</th></tr>
    <tr><td>Queue (point-to-point)</td><td>One consumer gets each message (competing workers)</td><td>Workers share load</td><td>Email send, thumbnail generate, webhook deliver</td></tr>
    <tr><td>Pub/Sub (fan-out)</td><td>Each subscriber gets copy</td><td>Independent channels</td><td>Live UI updates, cache bust broadcast, metrics tap</td></tr>
    <tr><td>Log (Kafka)</td><td>Retained stream; many groups read at own pace</td><td>Independent offset per group</td><td>Audit + search + analytics on same issue events</td></tr>
  </table>
  {diagram("""One issue transitioned:

Queue: one email worker picks job from shared queue

Pub/Sub: event published → websocket service, mobile push, metrics — all subscribers

Log: event appended; search group at offset 9001, audit group at 8998 — replay OK""")}
''', "distTopics")

    t2 = topic("pubsub-fit", "When each fits — notifications vs work distribution", "notifications fan out websocket SSE work distribution", "Pub/Sub", '''
  <p><b>Notifications (fan-out).</b> One transition → N watchers. Pub/sub or topic fan-out (SNS → many SQS, Kafka with multiple consumer groups, Redis pub/sub for ephemeral). User-visible latency target is seconds; duplicates handled with idempotent notify id.</p>
  <p><b>Work distribution.</b> Heavy jobs (PDF export, import 10k issues) — queue with competing consumers, visibility timeout, DLQ. You want <i>one</i> worker to own the job until done, not every subscriber.</p>
  <p><b>Live board updates.</b> Websocket/SSE layer often uses pub/sub backbone (Redis, NATS) to reach all app servers; client still needs version on issue to ignore stale. Not the same as durable notification email queue.</p>
  <p><b>Hybrid (common).</b> Transactional outbox → Kafka log (durability + replay) → fan-out adapters push to pub/sub for realtime and queue for email — each path matches semantics.</p>
''', "distTopics")

    t3 = topic("pubsub-pitfalls", "Fan-out cost, ordering, and failure", "fan out backpressure missed messages pub sub pitfalls", "Pub/Sub", f'''
  <ul>
    <li><b>Fan-out math</b> — 50 watchers × 500 transitions/min = 25k downstream deliveries/min — rate limit and batch.</li>
    <li><b>Ephemeral pub/sub</b> — subscriber offline = message gone; use queue or log for must-deliver.</li>
    <li><b>Ordering</b> — pub/sub usually unordered across subscribers; per-user mailbox may need partition key.</li>
    <li><b>Backpressure</b> — slow email provider must not block transition; decouple with queue depth metrics and shed.</li>
    <li><b>10×</b> — naive “publish to 10 services sync” recreates distributed monolith; log once, consume independently.</li>
  </ul>
  {callout("Jira-shaped answer: “Transition writes DB + outbox. Log consumer fans to realtime pub/sub for board and email queue for SMTP. Badge counter is eventual AP — separate path.”", "good")}
''', "distTopics")

    return f'''
<section class="block" id="pubsub" data-search="Pub Sub Fan Out Queue Log Notifications" data-stype="Section" data-cat="messaging">
  <p class="kicker">Fan-out</p>
  <h2 class="section-title">Pub/Sub vs Queues vs Logs</h2>
  <p class="lede">Pub/sub is for “tell everyone who is listening now.” Queues are for “one worker completes this job.” Logs are for “never lose the story.” Most real notification systems use all three deliberately.</p>
  {t1}
  {t2}
  {t3}
</section>
'''
