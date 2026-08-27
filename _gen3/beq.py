from util import code, esc

Q = []

def add(level, cat, q, short, deep, miss, follow, snippet=""):
    Q.append(dict(level=level, cat=cat, q=q, short=short, deep=deep, miss=miss, follow=follow, snippet=snippet))

add("medium", "node", "What blocks the Node.js event loop in production?",    "CPU-bound sync work, large JSON.parse/stringify, sync bcrypt, unbounded loops, native addons doing sync I/O.",    "The event loop runs one JS thread. Any synchronous CPU or blocking libuv call delays timers, sockets, and health checks. At scale, one hot handler stalls all requests on that worker. Fix: worker threads, offload to queue, bounded work, streaming.",    "Only database calls block Node.",    "How do you detect event-loop lag in production?")

add("easy", "node", "Why use a connection pool for Postgres in Node?",    "Opening a TCP+TLS+auth connection per request is expensive; pools reuse connections with bounded concurrency.",    "Pool size ≈ (cores × 2) is a starting heuristic, but real limit is Postgres max_connections and query latency. Too large a pool → DB contention; too small → queueing in app. Monitor wait time on pool.acquire().",    "Unlimited connections scale linearly.",    "What happens when pool is exhausted under load?")

add("medium", "node", "How does cluster module help — and what does it not fix?",    "Forks workers per CPU to use multiple cores; each worker has its own event loop and memory.",    "It does not share in-memory state — sessions in RAM need Redis/sticky LB. It does not help one worker blocked by CPU. Graceful shutdown must drain connections before exit.",    "cluster makes Node multi-threaded for JS.",    "When would you prefer containers over cluster?")

add("hard", "node", "Design graceful shutdown for a Node API.",    "Stop accepting, drain in-flight requests, close pool/queue connections, then exit; respect K8s terminationGracePeriodSeconds.",    "SIGTERM → set draining flag → server.close() → wait for active count with timeout → close DB pool → flush metrics → exit 0. In-flight jobs: stop dequeuing new work, finish or checkpoint current batch.",    "Kill process immediately on deploy.",    "What if shutdown exceeds the grace period?")

add("medium", "node", "Streams vs loading entire file into memory?",    "Streams process chunks — constant memory for large uploads/downloads.",    "pipe() from request to S3/GCS avoids buffering 4GB in heap. Backpressure: pause source when sink is slow. Error handling must destroy both sides on failure.",    "Node handles big files automatically without streams.",    "How do you resume a multipart upload?")

add("easy", "node", "Why is JSON.parse on a 50MB body dangerous?",    "Single allocation and sync parse blocks the event loop and can OOM the process.",    "Set body size limits at reverse proxy and framework. For huge payloads use streaming parser or direct-to-object-store upload via pre-signed URL.",    "V8 handles any JSON size.",    "Where should size limits live — nginx or app?")

add("hard", "node", "How do worker_threads fit a CPU-heavy image thumbnail job?",    "Offload CPU work to worker pool so HTTP handlers stay responsive.",    "Main thread posts job + buffer path; worker runs sharp/libvips; reply with result or error. Pool size bounded by CPU. Alternative: separate microservice/queue if jobs are minutes long.",    "Just use async/await for image processing.",    "When is a queue better than worker_threads?")

add("medium", "node", "Explain libuv thread pool vs event loop.",    "Event loop runs JS and non-blocking callbacks; libuv pool runs some blocking fs/crypto/dns ops off the main thread.",    "Pool default size 4 — heavy fs can queue. Not a substitute for proper async drivers. DNS lookup blocking behavior has bitten many deploys.",    "All I/O is non-blocking on the event loop.",    "What symptom shows thread pool starvation?")

add("medium", "database", "When does a composite index (a, b, c) not help query WHERE b = ?",    "Left-prefix rule: index helps (a), (a,b), (a,b,c) — not bare b or c alone.",    "Planner may seq scan if selectivity is low or stats stale. EXPLAIN ANALYZE is the truth. Covering index includes SELECT columns to avoid heap fetch.",    "Any column in the index helps any query.",    "How do partial indexes change the story?")

add("hard", "database", "Explain MVCC in Postgres in an interview.",    "Readers don't block writers; each transaction sees a snapshot; dead tuples need vacuum.",    "UPDATE creates new row version; old visible until xmin/xmax rules say otherwise. Long transactions block vacuum → bloat → slower scans. Repeatable read prevents phantom reads for indexed scans but not all anomalies without careful SQL.",    "MVCC means no locks ever.",    "What causes 'could not serialize access' errors?")

add("medium", "database", "Offset pagination vs cursor — when does OFFSET fail?",    "OFFSET N skips N rows — cost grows with page depth; cursor uses indexed key (updated_at, id).",    "Page 10000 with OFFSET 200000 scans/discards rows. Cursor stable if tie-breaker column unique. Offset OK for admin pages with small max page.",    "OFFSET is always fine with an index.",    "How do you paginate with non-unique sort keys?")

add("easy", "database", "What is a lost update and how do you prevent it?",    "Two transactions read same row, both write — last writer wins silently.",    "Optimistic: version column / if-match; pessimistic: SELECT FOR UPDATE; or atomic UPDATE ... WHERE status = expected. Idempotency keys for retries.",    "Transactions automatically merge writes.",    "Read committed vs repeatable read for a board move?")

add("hard", "database", "Design multi-tenant schema: shared table vs DB per tenant.",    "Shared tables with tenant_id + RLS is default; dedicated DB/shard for whale tenants or compliance.",    "Every query must filter tenant_id — enforce in ORM middleware and DB RLS. Indexes start with tenant_id. Cross-tenant reporting needs warehouse, not app DB scan.",    "Separate DB per tenant always scales best.",    "How do you prevent tenant_id injection in raw SQL?")

add("medium", "database", "When denormalize issue list for board view?",    "When read QPS dominates and join cost hurts p99 — store assignee_name, status on issue row.",    "Trade: write amplification on assignee rename. Use events or triggers to propagate. Denormalize with explicit invalidation story, not 'because NoSQL.'",    "Normalization is always correct.",    "How do you detect denormalization drift?")

add("medium", "database", "What is write skew?",    "Two transactions read overlapping rows, write disjoint rows, both commit — invariant broken.",    "Classic: two doctors on call both see count≥1 and both take leave. Fix: serializable isolation, advisory lock, or constraint on count. Not visible under read committed alone.",    "Foreign keys prevent write skew.",    "Give an issue-tracker example of write skew.")

add("easy", "database", "Why unique constraint on idempotency key?",    "Duplicate POST with same key returns same result without double effect.",    "Store key + response hash with TTL or forever for money. INSERT ... ON CONFLICT DO NOTHING then fetch. Race: two threads — DB serializes.",    "Application check-then-insert is enough.",    "What if idempotency store is down?")

add("hard", "distributed", "Why is there no exactly-once delivery without cooperation?",    "Network retries duplicate; consumer crash after process-before-ack duplicates.",    "Exactly-once effect = idempotent consumer + dedupe store or transactional outbox/inbox. Kafka EOS needs idempotent producer + transactions — still not magic across external systems.",    "Kafka gives exactly-once end-to-end always.",    "Map at-least-once email send to safe UX.")

add("medium", "distributed", "What is the CAP trade-off during a partition?",    "Must choose: remain available with possibly stale reads (AP) or reject writes/reads to preserve consistency (CP) — for the partitioned window.",    "Not a pick-once logo — per operation. Payment ledger CP; notification badge AP. Real systems tune per feature with explicit lag contracts.",    "CAP means pick C or A forever.",    "Draw CAP for search index vs issue title.")

add("medium", "distributed", "How does consistent hashing help sharding?",    "Maps keys and nodes to a ring; add/remove node moves only adjacent key ranges.",    "Virtual nodes spread load evenly. Hot key still hot — need application-level split or cache. Contrast with hash mod N where rescale reshuffles everything.",    "Consistent hashing eliminates hot keys.",    "When is hash mod N acceptable?")

add("hard", "distributed", "Why avoid distributed locks on the hot path?",    "Lock service partition or lease expiry → double execution or deadlock; adds latency.",    "Prefer DB unique constraint, single-partition Kafka consumer, or assign ownership in DB. Redis lock needs fencing token so stale holder cannot commit.",    "Redlock is always safe.",    "Redesign job processing without a lock.")

add("medium", "distributed", "What is a hot partition in Kafka?",    "One partition gets disproportionate traffic because partition key skew (celebrity issue).",    "That partition's consumer lags while others idle. Mitigate: salt key + merge downstream, dedicated fan-out service, or accept disorder for that entity.",    "More partitions always fixes hot keys.",    "Partition key for issue events — what ordering do you get?")

add("easy", "distributed", "Clock skew breaks last-write-wins — what instead?",    "Use server-generated version, logical clock, or DB transaction ordering — not client timestamp.",    "NTP skew and user clock wrong → silent data loss. CRDT/vector clock for collaborative; serializable TX for issue fields.",    "updated_at from client is fine.",    "How does Postgres tie-break concurrent updates?")

add("hard", "distributed", "Explain two-phase commit cost.",    "Prepare phase locks resources; coordinator failure leaves participants blocked until timeout.",    "2PC across microservices kills availability and adds latency. Sagas + outbox for cross-service; 2PC inside one DB is fine (Postgres transaction).",    "2PC is the standard for microservices.",    "How does saga compensate a failed notify step?")

add("medium", "distributed", "What is quorum read/write (Dynamo-style)?",    "R + W > N replicas → overlap guarantees you read latest write (with version vectors for conflicts).",    "Tunable: W=1 R=N fast write slow read vs W=N R=1 opposite. Conflicts need application merge or LWW with known loss.",    "Quorum means strong SQL consistency.",    "When is sloppy quorum acceptable?")

add("easy", "caching", "Cache-aside vs read-through?",    "Cache-aside: app reads cache, on miss loads DB and sets cache. Read-through: cache library loads DB on miss.",    "Write-aside invalidates or updates on write. Read-through simplifies app but cache must know loader. Stampede: many misses on hot key — use singleflight or probabilistic early expiry.",    "Cache always stays in sync automatically.",    "What happens when cache dies at 10× traffic?")

add("medium", "caching", "Cache penetration, avalanche, stampede — define and fix.",    "Penetration: queries for non-existent keys — bloom filter or cache null with short TTL. Avalanche: many keys expire together — jitter TTL. Stampede: thundering herd on one hot key — lock/singleflight.",    "At 10× launch, synchronized TTL expiry can DDOS your DB. Monitor miss rate spike correlated with expiry.",    "Longer TTL fixes everything.",    "Design invalidation for issue detail + board snapshot.")

add("medium", "caching", "Write-through vs write-back cache?",    "Write-through: write cache and DB together — consistent but slower writes. Write-back: write cache first, async flush — fast but data loss risk on crash.",    "Write-back rare for authoritative data. Redis as write-back buffer needs AOF/fsync policy understood. Issue transitions should not use write-back to Redis as SoT.",    "Write-back is always faster and safe.",    "When is write-through worth the latency?")

add("hard", "caching", "How do you cache permission checks safely?",    "Short TTL + tenant-scoped keys + invalidate on role change event; never cache 'deny' forever without TTL.",    "Key: perm:{tenant}:{user}:{resource_hash}. Wrong cache → privilege escalation or false deny. Server always re-check on mutation even if cache hit on read.",    "Cache allow results for a day.",    "What event invalidates permission cache?")

add("easy", "caching", "ETag vs Last-Modified?",    "Both enable conditional GET (304). ETag is opaque hash of representation; Last-Modified is time — weaker for dynamic content.",    "Strong ETag changes if any byte changes. Useful for issue JSON bandwidth on mobile. Combine with Cache-Control: private, must-revalidate.",    "304 means browser can skip auth.",    "Does ETag help collaborative editing?")

add("medium", "caching", "When is Redis the wrong primary store?",    "When you need durable complex queries, large values, or authoritative financial/issue history without another SoT.",    "Redis memory cost, persistence lag (AOF/RDB), no ad-hoc joins. OK for sessions, rate limits, locks, ephemeral presence — not issue graph.",    "Redis with AOF is a database replacement.",    "Pick Redis types for session vs leaderboard vs idempotency.")

add("medium", "caching", "CDN caching authenticated content — pitfalls?",    "Shared cache key without Vary/Auth leaks data across users; wrong Cache-Control on JSON is a SEV.",    "Use private, no-store for API. Attachments via short-lived signed URL to CDN. Never cache Set-Cookie responses.",    "CDN always speeds up API.",    "Separate cache policy for hashed JS vs issue API.")

add("medium", "messaging", "At-least-once vs at-most-once vs effectively-once?",    "At-least-once: retry until ack — duplicates possible. At-most-once: fire and forget — loss possible. Effectively-once: at-least-once + idempotent consumer.",    "Queues ack after process → crash redelivers. Kafka offset commit timing matters. DLQ for poison messages after N tries.",    "Exactly-once is the default in SQS.",    "Design comment-notification with DLQ.")

add("hard", "messaging", "Transactional outbox pattern — why?",    "DB commit and message publish are two systems — crash between them loses or duplicates events.",    "Write business row + outbox row in same TX; relay process polls outbox → publishes → marks sent. Inbox on consumer for dedupe. Dual-write without outbox is a bug.",    "Publish to Kafka after commit is always safe.",    "What if relay publishes but fails to mark sent?")

add("medium", "messaging", "Kafka consumer group rebalancing pain?",    "Partition reassignment stops consumption briefly; slow consumer extends rebalance.",    "Static membership, cooperative sticky assignor, reduce max.poll.interval, scale consumers ≤ partitions. Rebalance storm during deploy if many consumers bounce.",    "More consumers always speeds up.",    "Consumer lag growing — first three checks?")

add("easy", "messaging", "What is a dead letter queue for?",    "Messages that fail processing after retries — isolate poison pill without blocking main queue.",    "Alert on DLQ depth. Replay after fix with idempotency. Include original headers + error reason for debug.",    "DLQ deletes bad messages.",    "How do you safely replay DLQ at 2am?")

add("medium", "messaging", "Ordering guarantees in Kafka?",    "Order preserved within one partition; not across partitions.",    "Partition key = issue_id → all events for issue ordered. Global order impossible at scale without single partition. Trade hot key vs ordering scope.",    "Kafka orders all messages globally.",    "What if you need order across issue and comment?")

add("hard", "messaging", "Saga orchestration vs choreography?",    "Orchestrator: central state machine sends commands. Choreography: services react to events without central coordinator.",    "Orchestration easier to debug and enforce timeouts; choreography looser coupling but hard to trace. Both need compensating transactions for failure.",    "Events mean no central failure point automatically.",    "Compensate failed payment capture in issue upgrade saga.")

add("medium", "messaging", "Backpressure in message consumers?",    "Slow consumer must not unbounded-buffer memory — pause fetch, scale workers, or drop to DLQ with policy.",    "Prefetch count, max.in.flight, rate limit dequeue. Producer faster than consumer → lag → SLA miss. Monitor age of oldest unprocessed message.",    "Queue absorbs infinite backlog free.",    "When do you reject publish vs queue deeply?")

add("medium", "reliability", "Retry with exponential backoff and jitter — why jitter?",    "Synchronized retries create retry storms that amplify outages.",    "Full jitter: random(0, min(cap, base×2^attempt)). Cap max attempts and total deadline. Only retry idempotent or safe methods.",    "Retry immediately forever.",    "How do retries make a brownout a blackout?")

add("easy", "reliability", "Circuit breaker states?",    "Closed: normal. Open: fail fast after threshold. Half-open: probe if recovered.",    "Prevents hammering sick dependency. Half-open allows one trial request. Metrics: open count, failure rate. Not a substitute for fixing root cause.",    "Circuit breaker retries internally forever.",    "CB open — what should API return to user?")

add("hard", "reliability", "Define SLO, SLI, SLA — interview clarity.",    "SLI: measured metric (p99 latency). SLO: internal target (99% requests <300ms). SLA: contractual consequence with customer.",    "Error budget = 1 - SLO — spend on releases vs freeze. Alert on burn rate, not every blip. Product chooses SLO, not only ops.",    "SLA and SLO are the same.",    "Issue transition SLO — what SLI do you pick?")

add("medium", "reliability", "Bulkhead pattern?",    "Isolate resource pools so one dependency's failure doesn't exhaust all threads.",    "Separate connection pools per downstream; thread caps per call type. Issue API still serves reads if search pool exhausted.",    "One big pool is efficient.",    "Timeout per downstream vs global request timeout?")

add("medium", "reliability", "Health check: liveness vs readiness?",    "Liveness: process up — fail → restart. Readiness: can serve traffic — fail → remove from LB.",    "Readiness should check DB connectivity; liveness should not flap on slow DB. Startup probe for slow init.",    "Same endpoint for both.",    "What if DB down — kill pod or drain?")

add("hard", "reliability", "Design idempotent POST /transitions in Node.",    "Client sends Idempotency-Key; server stores key→response; unique constraint prevents double transition.",    "Same key + same body → replay stored 200. Same key + different body → 409. TTL keys 24h except financial forever.",    "GET is the only idempotent method.",    "Webhook at-least-once with idempotency — walk through.")

add("easy", "reliability", "Why timeouts on every outbound call?",    "Without deadline, thread/socket waits forever; cascading queue buildup.",    "Set timeout < client timeout. Propagate context deadline (OpenTelemetry/gRPC). Partial results better than hang if BFF design allows.",    "TCP will eventually timeout anyway.",    "504 to client but DB committed — what now?")

add("medium", "security", "JWT in localStorage vs httpOnly cookie?",    "httpOnly Secure SameSite cookie for session — XSS cannot exfiltrate token easily.",    "JWT in localStorage readable by any XSS script. BFF + cookie common for SPAs. Short-lived access + refresh rotation if JWT. mTLS for S2S.",    "JWT is stateless so storage doesn't matter.",    "How do you invalidate JWT before expiry?")

add("hard", "security", "Multi-tenant isolation — defense in depth?",    "tenant_id on every row + RLS + middleware guard + audit; never trust client tenant header alone.",    "Integration tests that attempt cross-tenant IDOR. Logs include tenant. Cache keys include tenant. S2S tokens scoped per tenant.",    "UUID obscurity is enough.",    "Bug: missing tenant filter in one endpoint — impact?")

add("medium", "security", "Rate limiting: token bucket vs sliding window?",    "Token bucket allows bursts with steady refill; sliding window smooths count over rolling interval.",    "Distributed: Redis INCR + TTL or dedicated limiter service. Layer at gateway + sensitive endpoints. Return 429 + Retry-After.",    "Rate limit only at CDN.",    "Race on Redis INCR without atomic script?")

add("easy", "security", "AuthN vs AuthZ — server responsibility?",    "AuthN: who. AuthZ: what they can do — always enforced server-side on every mutation.",    "UI hiding button is UX not security. Capability cache with short TTL OK; source of truth is permission service or DB join.",    "Frontend RBAC is sufficient.",    "How audit issue delete and permission change?")

add("medium", "security", "SSRF when fetching user-supplied URL?",    "Server-side fetch of webhook URL can hit internal metadata (169.254.169.254).",    "Block private IP ranges, require allowlist, no redirects to internal, separate network segment for fetcher.",    "Only HTTPS URLs are safe.",    "Preview unfurl for issue links — threat model?")

add("hard", "security", "Secrets management in Node deploy?",    "Secrets in env from vault/K8s secrets at runtime — not in git, not baked in image layers.",    "Rotate without redeploy if possible. Least privilege IAM for S3/DB. Audit secret access.",    ".env in repo is fine if private.",    "How rotate DB password with connection pool?")

add("medium", "security", "TLS termination — where and what trust?",    "Terminate at LB or service mesh; re-encrypt east-west with mTLS optional.",    "Cert rotation automation. HSTS on public edge. Internal plaintext only inside trusted mesh with network policy — document threat model.",    "TLS once at edge means internal is trusted forever.",    "What headers must not pass through from client to origin?")

add("medium", "node", "How do you structure a Fastify/Express service for testability?",    "Separate route registration, handlers, and data layer; inject config and db pool; health at /healthz.",    "App factory pattern: buildApp(deps) for tests with mocks. Graceful shutdown hook. Correlation id middleware first.",    "Controllers must be singletons.",    "Where put validation — schema at boundary.")

add("hard", "database", "Read replica lag vs read-your-writes?",    "User writes primary, reads replica — may not see own write until replication catches up.",    "Route user's session reads to primary after write (sticky session flag), or sync replication for critical reads, or client passes read-after-write token.",    "Replicas are always consistent.",    "Board load after creating issue — which read path?")

add("medium", "distributed", "What is a fencing token?",    "Monotonic token from lock service included with write — storage rejects stale holder's write after lease expiry.",    "Without fencing, delayed old worker can overwrite new data after lock lost. Zookeeper/etcd sequential nodes common source.",    "TTL lock alone prevents double write.",    "When lease expires mid-transaction?")

add("medium", "messaging", "Event schema evolution — compatibility rules?",    "Additive changes forward compatible; breaking changes need new topic/version or dual-write period.",    "Consumers ignore unknown fields. Never rename in place. Schema registry enforces. Document deprecation timeline.",    "JSON needs no schema.",    "Remove field from IssueCreated event — safe how?")

add("easy", "caching", "What is TTL and when is it not a strategy?",    "Time-to-live expires cache entry — good for bounded staleness.",    "If writes frequent and TTL short → low hit rate. If TTL long → stale reads. Event invalidation + TTL backup is typical.",    "Infinite TTL with nightly flush.",    "Issue assignee changes every minute — cache TTL?")
def beq() -> str:
    blocks = []
    cats = ["node", "database", "distributed", "caching", "messaging", "reliability", "security"]
    cat_counts = {c: sum(1 for x in Q if x["cat"] == c) for c in cats}
    for i, item in enumerate(Q, 1):
        snip = code("typescript", item["snippet"]) if item.get("snippet") else ""
        hid = f"beq-{i}"
        blocks.append(f'''
<article class="q" id="{hid}" data-level="{item["level"]}" data-cat="{item["cat"]}" data-search="{esc(item["q"])}" data-stype="Interview question" data-mock="1">
  <div class="meta-row"><span class="badge badge-js">{item["level"]}</span><span class="chip">{item["cat"]}</span><span class="chip">Q{i}</span></div>
  <h3>{i}. {esc(item["q"])}</h3>
  <p><button type="button" class="toggle-btn" data-toggle="{hid}-a">Reveal answer</button>
     <button type="button" class="toggle-btn" data-complete="questions" data-cid="{hid}">Mark complete</button></p>
  <div class="reveal" id="{hid}-a">
    <p><b>Short answer.</b> {item["short"]}</p>
    <p><b>Deep explanation.</b> {item["deep"]}</p>
    {snip}
    <p><b>Common misconception.</b> {item["miss"]}</p>
    <p><b>Senior follow-up.</b> {item["follow"]}</p>
  </div>
</article>''')
    tab_btns = "".join(
        f'<button type="button" class="tab" data-tab="{c}">{c} ({cat_counts[c]})</button>'
        for c in cats
    )
    n = len(Q)
    return f'''
<section class="block" id="beq" data-search="Backend Node Distributed Interview Question Bank" data-stype="Section">
  <p class="kicker">{n} questions</p>
  <h2 class="section-title">Backend / Node / Distributed Question Bank</h2>
  <p class="lede">Practice questions for senior backend interviews — Node.js, databases, distributed systems, caching, messaging, reliability, and security. Answer aloud, then reveal. Not claimed as official interview questions from any company.</p>
  <div class="tabs" data-tabs="beq">
    <button type="button" class="tab active" data-tab="all">All ({n})</button>
    {tab_btns}
  </div>
  {''.join(blocks)}
</section>
'''
