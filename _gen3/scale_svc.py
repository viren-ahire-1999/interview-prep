from util import code, topic, diagram, callout


def loadbalancing() -> str:
    t1 = topic("lb-layers", "L4 vs L7 load balancing", "L4 L7 load balancer TCP HTTP routing", "Load balancing", f'''
  <p><b>Mental model.</b> A load balancer is a traffic director with health awareness. <b>L4</b> (transport) sees IP + port — fast, protocol-agnostic, good for TCP passthrough and WebSocket stickiness at connection level. <b>L7</b> (application) sees HTTP headers, paths, cookies — you can route <code>/api/*</code> to app tier and <code>/static/*</code> to object storage, terminate TLS, inject headers, and apply WAF rules.</p>
  <table>
    <tr><th>Layer</th><th>Sees</th><th>Good for</th><th>Cost</th></tr>
    <tr><td>L4</td><td>IP, port, TCP state</td><td>DB proxy, gRPC over TLS passthrough, extreme RPS</td><td>Lower CPU per conn</td></tr>
    <tr><td>L7</td><td>HTTP method, path, Host, cookies</td><td>API gateways, canary by header, path-based routing</td><td>Parses every request</td></tr>
  </table>
  <p><b>Jira-shaped.</b> Browser hits an L7 edge that routes <code>/rest/api/*</code> to Node/Java services and static hashed assets to CDN. WebSocket upgrade for live board may terminate at L7 with longer idle timeouts than generic API routes.</p>
  {callout("Senior sentence: “I’d use L7 at the edge for routing and TLS, and L4 between internal tiers only if we need raw TCP or we’ve measured L7 as the bottleneck — not by default.”", "good")}
''', "distTopics")

    t2 = topic("lb-algos", "Algorithms: RR, least connections, consistent hashing", "round robin least connections consistent hashing", "Load balancing", f'''
  <p><b>Round robin (RR)</b> — simple, stateless, fine when requests are homogeneous and backends are equal. Breaks when one request is 200ms and another is 20s: RR ignores load.</p>
  <p><b>Least connections</b> — sends to the backend with fewest active connections. Better for long-lived requests, WebSockets, and variable latency. Needs shared state or sticky routing at the LB.</p>
  <p><b>Weighted RR / weighted least conn</b> — new smaller instances get fewer connections until warmed.</p>
  <p><b>Consistent hashing</b> — map client key (user id, tenant id, cache key) to a ring of nodes. Adding/removing a node only remaps ~1/N keys. Used for cache partitions, session stores, and some gRPC load balancers — not a substitute for health checks.</p>
  {diagram('''Client keys:  u1, u2, u3, ...
        |
   consistent hash ring
   [N1]---[N2]---[N3]---[N1]
        |
   u2 -> N2 (stable unless N2 dies)''')}
  <p><b>Practice.</b> “Why not always use consistent hashing?” Hot keys: one celebrity tenant still lands on one shard. Health: a dead node’s slice must fail over — you need redundancy on the ring or replication behind each node.</p>
''', "distTopics")

    t3 = topic("lb-ops", "Health checks, sticky sessions, horizontal scaling", "health check sticky session horizontal scale", "Load balancing", f'''
  <p><b>Health checks</b> — active (LB probes <code>/health</code>) vs passive (LB marks unhealthy after N 5xx). Deep checks (DB reachable) belong on a separate endpoint from liveness — otherwise a DB blip drains the entire fleet.</p>
  <p><b>Sticky sessions</b> — cookie or connection affinity so a user hits the same app instance. Useful for in-memory session (avoid if you can — use Redis/DB sessions). Dangerous for autoscaling: new instances get no traffic; draining is painful. Prefer stateless app + external session store.</p>
  <p><b>Horizontal scaling</b> — add identical instances behind the LB. Requires: stateless app tier, shared session/cache/DB, connection pool limits per instance, and graceful shutdown (stop accepting, drain in-flight, then SIGTERM).</p>
  {code("text", '''Scale-out checklist (say in interview):
1. Stateless app? (sessions in Redis, uploads in S3)
2. DB connection budget: 50 instances × 20 conns = 1000 — does primary allow it?
3. Cache invalidation still works with N writers?
4. Deployment: rolling update + health gate + maxUnavailable
5. Hot tenant: LB fairness ≠ shard fairness — may need tenant-aware routing''')}
  {callout("Atlassian scale: the first cliff is often connection fan-out and hot tenants, not “we need more LB algorithms.”")}
''', "distTopics")

    return f'''
<section class="block" id="loadbalancing" data-search="Load Balancing L4 L7 health checks" data-stype="Section" data-cat="reliability">
  <p class="kicker">Scale</p>
  <h2 class="section-title">Load Balancing</h2>
  <p class="lede">Direct traffic, shed unhealthy nodes, and scale horizontally — without pretending every algorithm fixes hot keys.</p>
  {t1}{t2}{t3}
</section>
'''


def proxy_cdn() -> str:
    t1 = topic("proxy-reverse", "Reverse proxy role", "reverse proxy nginx TLS termination", "Proxy / CDN", f'''
  <p>A <b>reverse proxy</b> sits in front of your app servers: terminates TLS, enforces timeouts, compresses, rate-limits, caches, and hides origin topology. Clients see one host; internally you have many pods/regions.</p>
  {diagram('''Browser --TLS--> Reverse proxy (edge)
                      |-- cache HIT --> response
                      |-- cache MISS --> origin app --> DB
                      +-- WAF / bot rules''')}
  <p><b>Forward vs reverse.</b> Forward proxy (corporate egress) represents the client. Reverse proxy represents the server. Interview questions mean reverse.</p>
  <p><b>TLS at the edge</b> — certificates rotate at the proxy; origins may use mTLS on a private network. HTTP/2 and HTTP/3 multiplexing happen at the edge; origin may stay HTTP/1.1 behind the mesh.</p>
''', "distTopics")

    t2 = topic("cdn-cache", "CDN: hashed assets vs private HTML", "CDN cache control immutable private HTML", "Proxy / CDN", f'''
  <p><b>CDN</b> caches static and cacheable API responses at PoPs close to users. Two policies dominate frontend-heavy products:</p>
  <ul class="tight">
    <li><b>Hashed immutable assets</b> — <code>app.[contenthash].js</code> with <code>Cache-Control: public, max-age=31536000, immutable</code>. Safe forever; deploy = new filename.</li>
    <li><b>Private HTML / API</b> — <code>Cache-Control: private, no-store</code> or short TTL with <code>Vary: Cookie, Authorization</code>. Never cache authenticated issue HTML as public.</li>
  </ul>
  <p><b>Stale-while-revalidate</b> for semi-static public docs. <b>Surrogate keys</b> (Fastly-style) purge all pages for project X when branding changes.</p>
  <p><b>Jira-shaped.</b> Issue REST JSON is usually origin-only with auth. Attachment downloads may be CDN-backed signed URLs. Confluence public space pages may CDN-cache anonymous HTML; logged-in view is dynamic.</p>
  {callout("Practice trade-off: “I’d CDN the static bundle and user-generated attachments via signed URLs, not the authenticated issue API — permissions change faster than TTL math allows.”", "good")}
''', "distTopics")

    return f'''
<section class="block" id="proxy" data-search="Reverse Proxy CDN TLS caching" data-stype="Section" data-cat="reliability">
  <p class="kicker">Edge</p>
  <h2 class="section-title">Reverse Proxy &amp; CDN</h2>
  <p class="lede">The edge is where TLS, caching policy, and abuse resistance meet — before your app tier pays per byte.</p>
  {t1}{t2}
</section>
'''


def ratelimit() -> str:
    t1 = topic("rl-algos", "Token bucket, leaky bucket, fixed & sliding windows", "token bucket leaky bucket sliding window rate limit", "Rate limiting", f'''
  <table>
    <tr><th>Algorithm</th><th>Behavior</th><th>Pros</th><th>Cons</th></tr>
    <tr><td>Token bucket</td><td>Refill tokens at rate R; burst up to capacity B</td><td>Allows controlled bursts; smooth average</td><td>Per-key state (tokens + last refill)</td></tr>
    <tr><td>Leaky bucket</td><td>Queue drains at fixed rate</td><td>Perfectly smooth output</td><td>Queues can grow; bad for hard reject</td></tr>
    <tr><td>Fixed window</td><td>Count per calendar minute</td><td>Simple counters in Redis</td><td>2× burst at window edges</td></tr>
    <tr><td>Sliding window</td><td>Count in last N seconds</td><td>Fairer than fixed</td><td>More memory or approximations</td></tr>
  </table>
  <p><b>When to use which.</b> Public APIs and login endpoints: token bucket or sliding window with clear 429 + <code>Retry-After</code>. Background workers: leaky bucket to protect downstream SMTP/push vendors.</p>
  {code("TypeScript", '''/** In-memory token bucket — interview reference implementation */
export class TokenBucket {
  private tokens: number;
  private lastRefillMs: number;

  constructor(
    private readonly capacity: number,
    private readonly refillPerSec: number,
  ) {
    this.tokens = capacity;
    this.lastRefillMs = Date.now();
  }

  tryTake(count = 1): boolean {
    this.refill();
    if (this.tokens < count) return false;
    this.tokens -= count;
    return true;
  }

  private refill(): void {
    const now = Date.now();
    const elapsedSec = (now - this.lastRefillMs) / 1000;
    if (elapsedSec <= 0) return;
    this.tokens = Math.min(
      this.capacity,
      this.tokens + elapsedSec * this.refillPerSec,
    );
    this.lastRefillMs = now;
  }
}''')}
  {code("TypeScript", '''/** Sliding window log — accurate, Redis-friendly pattern */
export async function slidingWindowAllow(
  redis: { zremrangebyscore(k: string, min: number, max: number): Promise<void>;
           zcard(k: string): Promise<number>;
           zadd(k: string, score: number, member: string): Promise<void>;
           expire(k: string, sec: number): Promise<void>; },
  key: string,
  limit: number,
  windowMs: number,
): Promise<boolean> {
  const now = Date.now();
  const windowStart = now - windowMs;
  await redis.zremrangebyscore(key, 0, windowStart);
  const count = await redis.zcard(key);
  if (count >= limit) return false;
  await redis.zadd(key, now, `${now}:${Math.random()}`);
  await redis.expire(key, Math.ceil(windowMs / 1000));
  return true;
}''')}
''', "distTopics")

    t2 = topic("rl-distributed", "Distributed rate limiting at 1M users", "Redis rate limit distributed API design", "Rate limiting", f'''
  <p><b>Problem.</b> Each app instance with an in-memory bucket is wrong: users hop instances; attackers rotate IPs. Centralize counters in <b>Redis</b> (or a dedicated rate-limit service) with atomic INCR + EXPIRE or Lua scripts for token bucket.</p>
  {diagram('''Client --> API gateway --> rate-limit check (Redis)
                              | allowed --> app
                              | 429 + Retry-After''')}
  <p><b>Design API for 1M users</b> (practice):</p>
  <ul class="tight">
    <li><b>Dimensions:</b> per API key, per user id, per tenant, per IP (unauthenticated), per route class (read vs write).</li>
    <li><b>Headers:</b> <code>X-RateLimit-Limit</code>, <code>Remaining</code>, <code>Reset</code> on every response; 429 when exceeded.</li>
    <li><b>Sharding Redis:</b> hash key by tenant to avoid single hot key; local approximate counters (Redis Cell / GCRA) for high-cardinality keys.</li>
    <li><b>Fail open vs closed:</b> product choice — billing API fails closed; read-heavy search may fail open with logging if Redis is down.</li>
    <li><b>Sync vs async:</b> check synchronously at gateway; heavy abuse analysis async via events.</li>
  </ul>
  <p><b>Numbers.</b> 1M DAU, 100 req/user/day → ~1.2k avg RPS, ~3–5k peak. Redis handles millions of ops/s on a small cluster — the design problem is key cardinality and fairness, not raw throughput.</p>
  {callout("Senior line: “Rate limits protect the system and set expectations. They are not a substitute for auth, input validation, or queue-based absorption for fan-out work.”", "good")}
''', "distTopics")

    return f'''
<section class="block" id="ratelimit" data-search="Rate Limiting token bucket Redis 429" data-stype="Section" data-cat="reliability">
  <p class="kicker">Protection</p>
  <h2 class="section-title">Rate Limiting</h2>
  <p class="lede">Shape traffic before it shapes your outage. Know the algorithms, implement two in TypeScript, and centralize at scale.</p>
  {t1}{t2}
</section>
'''


def reliability() -> str:
    t1 = topic("rel-patterns", "Redundancy, failover, timeouts, retries", "redundancy failover timeout retry exponential backoff", "Reliability", f'''
  <p><b>Redundancy</b> — no single instance of anything on the critical path. Multi-AZ as a baseline; multi-region when RTO/RPO demand it.</p>
  <p><b>Failover</b> — automated (health-based DNS/LB) vs manual (runbook). Practice stating RTO: “DNS TTL 60s + warm standby ≈ 2 min user-visible blip.”</p>
  <p><b>Timeouts</b> — every outbound call gets one, shorter than the client’s timeout. Cascading slowness is a timeout budget problem: if A waits 30s for B and B waits 30s for C, one slow leaf stalls the fleet.</p>
  <p><b>Retries</b> — only on idempotent operations or with idempotency keys; cap max attempts; use <b>exponential backoff + jitter</b> so retries don’t align into a retry storm.</p>
  {code("TypeScript", '''function backoffMs(attempt: number, base = 100, cap = 10_000): number {
  const exp = Math.min(cap, base * 2 ** attempt);
  const jitter = Math.floor(Math.random() * exp * 0.3);
  return exp + jitter;
}''')}
  {callout("Retry storm: SES blips → every app retries email at t=1s → you DDoS yourself. Jitter + queue + circuit breaker.", "warn")}
''', "distTopics")

    t2 = topic("rel-isolation", "Circuit breakers, bulkheads, graceful degradation", "circuit breaker bulkhead graceful degradation", "Reliability", f'''
  <p><b>Circuit breaker</b> — closed (normal) → open (fail fast after error threshold) → half-open (probe). Stops hammering a sick dependency. Pair with fallbacks that are honest (“notifications delayed”) not silent wrong data.</p>
  <p><b>Bulkheads</b> — separate thread pools / connection limits per dependency so one slow search cannot exhaust all DB connections for issue writes.</p>
  <p><b>Graceful degradation</b> — issue transition succeeds; activity stream omits avatar URLs if avatar service is down. Define which features are tier-1 vs tier-2.</p>
  {diagram('''Issue PATCH (tier-1) ------> primary DB (reserved pool)
              |--> audit log queue
              +--> search indexer (breaker OPEN -> skip, catch up later)
              +--> email worker (bulkhead: max 50 concurrent)''')}
  <p><b>Practice.</b> “What fails first at 10×?” Usually connection pools, not CPU. Name bulkheads before you name Kubernetes.</p>
''', "distTopics")

    return f'''
<section class="block" id="reliability" data-search="Reliability retries circuit breaker bulkhead" data-stype="Section" data-cat="reliability">
  <p class="kicker">Failure</p>
  <h2 class="section-title">Reliability Patterns</h2>
  <p class="lede">Systems fail partially. Seniors design for that: timeouts, bounded retries, isolation, and honest degradation.</p>
  {t1}{t2}
</section>
'''


def idempotency() -> str:
    t1 = topic("idem-why", "Why idempotency matters", "idempotency key duplicate request at-least-once", "Idempotency", f'''
  <p>Networks retry. Browsers double-submit. Webhooks redeliver. Message queues are <b>at-least-once</b>. Without idempotency, “create charge” twice means angry customers and finance tickets.</p>
  <p><b>Definition.</b> Performing the same operation multiple times with the same logical intent produces the same outcome as once — no duplicate side effects.</p>
  <p><b>HTTP.</b> GET/PUT/DELETE are idempotent by spec; POST is not — so payments and creates need an <b>Idempotency-Key</b> header (Stripe-style) or a natural unique key (order id).</p>
''', "distTopics")

    t2 = topic("idem-patterns", "Payments, orders, uploads, webhooks, jobs", "idempotency payment webhook upload dedupe", "Idempotency", f'''
  <table>
    <tr><th>Workflow</th><th>Key</th><th>Store pattern</th></tr>
    <tr><td>Payment charge</td><td>Idempotency-Key per client attempt</td><td>UNIQUE(idempotency_key); store response snapshot</td></tr>
    <tr><td>Order create</td><td>Client order uuid</td><td>INSERT … ON CONFLICT return existing</td></tr>
    <tr><td>Multipart upload</td><td>uploadId from initiate</td><td>Complete once; list parts idempotently</td></tr>
    <tr><td>Webhook handler</td><td>vendor event id</td><td>processed_events table UNIQUE(event_id)</td></tr>
    <tr><td>Background job</td><td>job id / dedupe key in queue</td><td>visibility timeout + idempotent consumer</td></tr>
  </table>
  {code("TypeScript", '''// Express-style idempotent POST with Postgres
app.post("/charges", async (req, res) => {
  const key = req.header("Idempotency-Key");
  if (!key) return res.status(400).json({ error: "missing idempotency key" });

  const existing = await db.query(
    "SELECT status, body FROM idempotent_requests WHERE key = $1",
    [key],
  );
  if (existing.rows[0]?.status === "completed") {
    return res.status(200).json(existing.rows[0].body);
  }

  try {
    await db.query(
      "INSERT INTO idempotent_requests (key, status) VALUES ($1, 'pending')",
      [key],
    );
  } catch (e: unknown) {
    // unique violation — another worker won the race; poll or return stored result
    if (!isUniqueViolation(e)) throw e;
  }

  const charge = await paymentProvider.charge({ amount: req.body.amount });
  await db.query(
    "UPDATE idempotent_requests SET status = 'completed', body = $2 WHERE key = $1",
    [key, charge],
  );
  return res.status(201).json(charge);
});''')}
  {code("TypeScript", '''// Webhook dedupe — consumer must be safe under redelivery
export async function handleWebhook(event: { id: string; type: string; payload: unknown }) {
  const inserted = await db.query(
    `INSERT INTO inbox_events (event_id, payload)
     VALUES ($1, $2)
     ON CONFLICT (event_id) DO NOTHING
     RETURNING event_id`,
    [event.id, event.payload],
  );
  if (inserted.rowCount === 0) return; // already processed

  await processBusinessLogic(event);
}''')}
  <p><b>Jira transition.</b> Client sends <code>Idempotency-Key</code> or If-Match etag; server uses UNIQUE(issue_id, transition_id, client_token) so double-click doesn’t double-audit.</p>
  {callout("Dedupe + unique constraint beats distributed locks for most idempotency. The database is the referee.", "good")}
''', "distTopics")

    return f'''
<section class="block" id="idempotency" data-search="Idempotency key dedupe webhook payment" data-stype="Section" data-cat="reliability">
  <p class="kicker">Exactly-once intent</p>
  <h2 class="section-title">Idempotency</h2>
  <p class="lede">At-least-once delivery is reality. Idempotency keys, dedupe tables, and unique constraints make that safe.</p>
  {t1}{t2}
</section>
'''


def locks() -> str:
    t1 = topic("locks-hard", "Why locks are hard across machines", "distributed lock partition clock TTL", "Distributed locks", f'''
  <p>On one machine, a mutex is cheap and well-defined. Across machines you inherit: <b>partial failure</b> (holder dies mid-critical-section), <b>clock skew</b>, <b>network partitions</b>, and <b>GC pauses</b> (your process stops while still “holding” the lock).</p>
  <p>A “lock” in Redis is really a <b>lease</b>: SET key token NX PX ttl. If TTL expires before work finishes, another worker can enter — you may run two writers unless you validate the token on unlock and use fencing.</p>
  {callout("Martin Kleppmann’s critique stands: a naive Redis lock is not a safe distributed lock without careful token checks, TTL tuning, and often fencing tokens on the storage layer.", "warn")}
''', "distTopics")

    t2 = topic("locks-redis", "Redis locks, lease, TTL, fencing", "Redis lock lease fencing token", "Distributed locks", f'''
  <p><b>Correct-ish pattern:</b></p>
  <ol>
    <li>Acquire with random token: <code>SET lock:issue:42 &lt;token&gt; NX PX 30000</code></li>
    <li>Do work; refresh lease if long (extend only if token matches — Lua script)</li>
    <li>Release with compare-and-del Lua: delete only if value == token</li>
    <li><b>Fencing token</b> — monotonic counter passed to DB/storage so stale lock holders cannot commit (e.g. issue version must be &gt; last seen fence)</li>
  </ol>
  {code("TypeScript", '''// Release only if we still own the lock (Redis Lua sketch as TS logic)
async function releaseLock(redis: Redis, key: string, token: string): Promise<boolean> {
  const script = `
    if redis.call("get", KEYS[1]) == ARGV[1] then
      return redis.call("del", KEYS[1])
    else
      return 0
    end`;
  const result = await redis.eval(script, 1, key, token);
  return result === 1;
}''')}
''', "distTopics")

    t3 = topic("locks-avoid", "When to AVOID distributed locks", "avoid distributed lock alternative idempotency", "Distributed locks", f'''
  <p>Prefer, in order:</p>
  <ul class="tight">
    <li><b>Unique constraints + idempotent upsert</b> — one row wins; others get conflict or no-op</li>
    <li><b>Single writer per partition</b> — Kafka partition key = issue id; ordering without locks</li>
    <li><b>Optimistic concurrency</b> — UPDATE … WHERE version = $expected</li>
    <li><b>DB advisory locks</b> — if all writers hit same Postgres, <code>pg_advisory_xact_lock</code> is simpler than Redis + fencing</li>
  </ul>
  <p><b>Use a distributed lock when</b> you truly need mutual exclusion across heterogeneous workers on a resource Redis doesn’t own — and you accept ops complexity. Scheduled cron “only one leader” is a common acceptable case (with lease + watchdog).</p>
  {callout("Interview: “I’d try optimistic locking on the issue row before I’d introduce Redlock for Jira transitions.”", "good")}
''', "distTopics")

    return f'''
<section class="block" id="locks" data-search="Distributed Locks Redis lease fencing" data-stype="Section" data-cat="reliability">
  <p class="kicker">Coordination</p>
  <h2 class="section-title">Distributed Locks</h2>
  <p class="lede">Locks across machines are leases with failure modes. Know Redis patterns — and when to refuse them.</p>
  {t1}{t2}{t3}
</section>
'''


def replication() -> str:
    t1 = topic("repl-basics", "Primary-replica and read replicas", "primary replica read replica replication lag", "Replication / sharding", f'''
  <p><b>Primary-replica</b> — one writer (primary), N read replicas streaming WAL/binlog. Reads scale; writes don’t. <b>Replication lag</b> means a user may not see their own write on a replica — need read-your-writes routing (sticky to primary after write, or session token).</p>
  <p><b>Multi-primary</b> — writes on multiple nodes; conflict resolution required. Useful geo-write latency; painful for relational invariants. Most Jira-shaped OLTP stays single-primary per shard.</p>
  {diagram('''Writes ----> Primary ---- WAL ----> Replica 1 (reads)
                      |-------------> Replica 2 (reads)
                      +-------------> Replica 3 (reports)''')}
''', "distTopics")

    t2 = topic("repl-partition", "Vertical vs horizontal partitioning, sharding", "sharding partition vertical horizontal hot shard", "Replication / sharding", f'''
  <p><b>Vertical partitioning</b> — split by table/service (issues DB, attachments metadata, audit). Good first split.</p>
  <p><b>Horizontal partitioning (sharding)</b> — split rows by key (tenant_id, project_id). Each shard is a full DB with its own primary.</p>
  <p><b>Hot shards</b> — one mega-tenant dominates a shard. Mitigations: sub-shard by project, dedicated shard for whale tenant, rate limits, async denormalization.</p>
  <p><b>Rebalancing</b> — move ranges with dual-write or copy + catch-up + cutover. Plan years before you need it; consistent hashing reduces remapping on add/remove.</p>
  {diagram('''tenant_id hash --> shard A (tenants 0-999)
              |--> shard B (tenants 1000-1999)
              |--> shard C (whale tenant isolated)''')}
  {callout("When sharding is premature: &lt; few TB, &lt; ~10k sustained write RPS on well-indexed Postgres, team can’t operate cross-shard queries. Vertical split + replicas + cache first.", "good")}
''', "distTopics")

    t3 = topic("repl-practice", "Practice: shard or not?", "consistent hashing rebalancing premature sharding", "Replication / sharding", f'''
  <p><b>Consistent hashing</b> — route <code>shard = ring(tenant_id)</code>. Adding a node moves only adjacent keys. Often implemented at app router or Vitess/Citus layer.</p>
  <p><b>Cross-shard queries</b> — avoid. Design access patterns per shard key. Global search/analytics → separate derived store.</p>
  <p><b>Practice question.</b> “10M issues, 50k writes/s peak?” Probably sharded by <code>project_id</code> or <code>tenant_id</code>. “500 writes/s?” Replicas + partitioning large audit table maybe; not 16 shards day one.</p>
''', "distTopics")

    return f'''
<section class="block" id="replication" data-search="Replication Sharding read replica consistent hashing" data-stype="Section" data-cat="distributed">
  <p class="kicker">Data scale</p>
  <h2 class="section-title">Replication &amp; Sharding</h2>
  <p class="lede">Replicas for read scale; shards for write scale — each with lag, hot spots, and rebalance tax.</p>
  {t1}{t2}{t3}
</section>
'''


def distxact() -> str:
    t1 = topic("dx-2pc", "Two-phase commit and its costs", "2PC two phase commit distributed transaction", "Distributed transactions", f'''
  <p><b>2PC</b> — coordinator prepares all participants (hold locks), then commits or aborts. Blocks on coordinator failure; participants hold locks during uncertainty → throughput collapse under latency.</p>
  <p>Seniors rarely propose 2PC across microservices in interviews. It’s CP, slow, and operationally scary. Use when a single datastore can own the transaction boundary.</p>
''', "distTopics")

    t2 = topic("dx-saga", "Sagas: orchestration vs choreography", "saga compensating transaction orchestration", "Distributed transactions", f'''
  <p><b>Saga</b> — sequence of local transactions with <b>compensating actions</b>. Issue transition saga: (1) update issue (2) emit event (3) index search. If (3) fails, retry (3); don’t undo (1) if business says transition stands.</p>
  <p><b>Orchestration</b> — central workflow engine decides next step. <b>Choreography</b> — services react to events. Orchestration easier to debug; choreography fewer coupling points but harder tracing.</p>
  {diagram('''Transition API --> update DB (local tx)
              --> outbox row (same local tx)
              --> relay --> search worker --> index
                              | fail --> retry / DLQ (no 2PC)''')}
''', "distTopics")

    t3 = topic("dx-outbox", "Transactional outbox, inbox, dual-write", "transactional outbox inbox dual write problem", "Distributed transactions", f'''
  <p><b>Dual-write problem</b> — write DB then publish to Kafka: crash between them → inconsistency. Fix: <b>transactional outbox</b> — insert event row in same DB transaction as business write; separate relay publishes and marks sent.</p>
  <p><b>Inbox pattern</b> — consumer stores incoming event id uniquely before processing (pairs with idempotency).</p>
  {code("TypeScript", '''await db.transaction(async (tx) => {
  await tx.query("UPDATE issues SET status = $1 WHERE id = $2", [next, issueId]);
  await tx.query(
    "INSERT INTO outbox (aggregate_id, type, payload) VALUES ($1, $2, $3)",
    [issueId, "IssueTransitioned", payload],
  );
});
// relay process polls outbox -> message bus -> marks published''')}
  {callout("Practice: “Search index is eventually consistent; the issue row is source of truth. Outbox makes that eventual path reliable.”", "good")}
''', "distTopics")

    return f'''
<section class="block" id="distxact" data-search="Distributed Transactions saga outbox 2PC" data-stype="Section" data-cat="distributed">
  <p class="kicker">Cross-service writes</p>
  <h2 class="section-title">Distributed Transactions</h2>
  <p class="lede">You don’t get ACID across services. Sagas, outbox, and idempotent consumers are the senior toolkit.</p>
  {t1}{t2}{t3}
</section>
'''


def microservices() -> str:
    t1 = topic("ms-shapes", "Monolith vs modular monolith vs microservices", "monolith modular monolith microservices trade-off", "Microservices", f'''
  <table>
    <tr><th>Shape</th><th>Deploy</th><th>When it wins</th><th>Tax</th></tr>
    <tr><td>Monolith</td><td>One unit</td><td>Small team, one domain, fast iteration</td><td>Compile/test blast radius grows</td></tr>
    <tr><td>Modular monolith</td><td>One unit, hard module boundaries</td><td>Most Atlassian-shaped products at senior interviews</td><td>Boundaries need enforcement (lint, reviews)</td></tr>
    <tr><td>Microservices</td><td>Many independent deploys</td><td>Clear ownership, different SLOs, scale one hot service</td><td>Network, observability, distributed tx, ops headcount</td></tr>
  </table>
  <p><b>Microservices are NOT automatically better.</b> They trade compile-time coupling for runtime coupling. You gain team autonomy only if org structure matches service boundaries and you invest in platform (CI, tracing, contract tests).</p>
''', "topics")

    t2 = topic("ms-dimensions", "Deployment, scaling, ownership, latency", "microservices deployment scaling ownership latency", "Microservices", f'''
  <ul class="tight">
    <li><b>Deployment</b> — independent release cadence vs coordinated schema migrations across services</li>
    <li><b>Scaling</b> — scale search workers without scaling billing — if they’re actually separate services with separate bottlenecks</li>
    <li><b>Ownership</b> — team owns API + data + on-call; avoid “shared ownership” services nobody maintains</li>
    <li><b>Latency</b> — user request crossing 6 sync HTTP hops adds tail latency; prefer async for non-critical path</li>
    <li><b>Observability</b> — distributed traces mandatory; otherwise debugging is archaeology</li>
    <li><b>Transactions</b> — sagas/outbox replace JOINs across DBs you used to have in one monolith</li>
    <li><b>Testing</b> — contract tests + staging env complexity; local dev needs good mocks or devcontainers</li>
    <li><b>Failure</b> — partial failure is default; need bulkheads per dependency</li>
    <li><b>Ops cost</b> — N services × (deploy pipeline, dashboards, runbooks, CVE patches)</li>
  </ul>
  {callout("Practice sentence: “I’d extract search when its SLO, team, and data volume diverge — not because the diagram looks modern.”", "good")}
''', "topics")

    return f'''
<section class="block" id="microservices" data-search="Microservices monolith modular monolith trade-offs" data-stype="Section" data-cat="design">
  <p class="kicker">Architecture</p>
  <h2 class="section-title">Microservices &amp; Monoliths</h2>
  <p class="lede">Service boundaries are org and reliability decisions — not a maturity ladder.</p>
  {t1}{t2}
</section>
'''


def communication() -> str:
    t1 = topic("comm-protocols", "REST, gRPC, events, queues, pub/sub", "REST gRPC events queue pub sub sync async", "Communication", f'''
  <table>
    <tr><th>Style</th><th>Best for</th><th>Watch out</th></tr>
    <tr><td>REST/HTTP JSON</td><td>Public APIs, browser clients, CRUD</td><td>Over-fetch, chatty N+1 without BFF</td></tr>
    <tr><td>gRPC</td><td>Internal S2S, strong contracts, streaming</td><td>Browser needs grpc-web or gateway</td></tr>
    <tr><td>Message queue</td><td>Work distribution, backpressure, retries</td><td>Ordering only per partition; poison messages</td></tr>
    <tr><td>Pub/sub</td><td>Fan-out notifications, decoupled consumers</td><td>Consumer lag, schema evolution</td></tr>
    <tr><td>Event log (Kafka)</td><td>Replay, multiple independent consumers</td><td>Ops complexity; not a task queue alone</td></tr>
  </table>
  <p><b>Sync vs async.</b> Sync when user waits for result (issue GET, permission check). Async when user tolerates delay (email, search index, analytics). Atlassian transitions: sync for DB write; async for watchers.</p>
  {diagram('''Client --sync REST--> Issue API --> DB
Issue API --async event--> queue --> notification worker
                              --> search indexer''')}
''', "topics")

    return f'''
<section class="block" id="communication" data-search="Communication REST gRPC events sync async" data-stype="Section" data-cat="design">
  <p class="kicker">Contracts</p>
  <h2 class="section-title">Service Communication</h2>
  <p class="lede">Pick the transport for coupling, latency budget, and failure mode — not resume keywords.</p>
  {t1}
</section>
'''


def gateway() -> str:
    t1 = topic("gw-role", "Design an API gateway", "API gateway routing auth rate limit aggregation", "API Gateway", f'''
  <p><b>Gateway responsibilities:</b></p>
  <ul class="tight">
    <li><b>Routing</b> — path/host to service cluster; canary by header or percentage</li>
    <li><b>AuthN/Z</b> — validate JWT/session, attach user/tenant context headers (signed internal)</li>
    <li><b>Rate limiting</b> — global and per-tenant quotas</li>
    <li><b>Aggregation</b> — BFF-style compose issue + permissions + flags (careful: don’t become a god object)</li>
    <li><b>Logging/metrics</b> — request id, latency, 4xx/5xx by route</li>
    <li><b>TLS termination</b>, WAF, request size limits</li>
  </ul>
  {diagram('''Browser --> API Gateway --> issue-svc
                         |--> search-svc
                         |--> user-svc
                         +--> rate-limit (Redis)''')}
  <p><b>What must NOT live only on the gateway:</b></p>
  <ul class="tight">
    <li><b>Authorization business rules</b> — “can transition this issue?” must be enforced in issue-svc with DB truth</li>
    <li><b>Transactional invariants</b> — gateway cannot be sole owner of consistency</li>
    <li><b>PII access policy</b> — downstream services must re-check tenant scope</li>
    <li><b>Idempotency storage</b> — belongs with the domain write</li>
  </ul>
  {callout("Gateway is a front door, not a second monolith with all the business logic.", "warn")}
''', "topics")

    return f'''
<section class="block" id="gateway" data-search="API Gateway routing auth aggregation BFF" data-stype="Section" data-cat="design">
  <p class="kicker">Edge API</p>
  <h2 class="section-title">API Gateway</h2>
  <p class="lede">Centralize cross-cutting ingress concerns — without smuggling domain logic into the edge.</p>
  {t1}
</section>
'''


def auth() -> str:
    t1 = topic("auth-models", "Sessions, OAuth, JWT, S2S", "session OAuth JWT service to service auth", "Auth", f'''
  <p><b>Session cookies</b> — server-side session store (Redis/DB), HttpOnly Secure SameSite cookie. Good for browser apps; CSRF protection required. Atlassian cloud sessions are long-lived with refresh and device binding patterns.</p>
  <p><b>OAuth 2 / OIDC</b> — delegate identity to IdP; your app gets tokens. Use authorization code + PKCE for SPAs. Scopes express delegated permission, not your internal RBAC entire matrix.</p>
  <p><b>JWT</b> — signed claims, stateless verification. Watch expiry, rotation, revocation (short TTL + refresh, or introspection). Don’t put secrets in JWT payload — it’s base64, not encrypted.</p>
  <p><b>S2S (service-to-service)</b> — mTLS, signed service JWTs, or workload identity (IAM). Never share a user cookie between services.</p>
''', "backendTopics")

    t2 = topic("authz-tenant", "RBAC/ABAC, token storage, tenant isolation", "RBAC ABAC tenant isolation token storage", "Auth", f'''
  <p><b>RBAC</b> — role → permissions. <b>ABAC</b> — attributes (tenant, project, issue security level). Jira mixes both: project role + issue-level security.</p>
  <p><b>Token storage (browser).</b> Access token in memory; refresh in HttpOnly cookie or secure rotation endpoint. Avoid localStorage for bearer tokens (XSS exfiltration).</p>
  <p><b>Tenant isolation.</b> Every query includes <code>tenant_id</code> from auth context — never from client body alone. Row-level security in Postgres is a defense-in-depth layer, not a substitute for app checks.</p>
  {callout("Defensive only: assume tokens leak and XSS happens — minimize blast radius with short TTL, scoped permissions, and server-side enforcement on every mutation.", "good")}
''', "backendTopics")

    return f'''
<section class="block" id="auth" data-search="Authentication Authorization OAuth JWT RBAC tenant" data-stype="Section" data-cat="security">
  <p class="kicker">Identity</p>
  <h2 class="section-title">AuthN &amp; AuthZ</h2>
  <p class="lede">Sessions and tokens get users in; RBAC/ABAC and tenant scoping keep data in the right place.</p>
  {t1}{t2}
</section>
'''


def realtime() -> str:
    t1 = topic("rt-transports", "WebSocket, SSE, long poll, poll", "WebSocket SSE long polling realtime", "Real-time", f'''
  <table>
    <tr><th>Transport</th><th>Direction</th><th>Use when</th></tr>
    <tr><td>WebSocket</td><td>Bi-directional</td><td>Chat, collaborative board cursors, typing indicators</td></tr>
    <tr><td>SSE</td><td>Server → client</td><td>Notifications feed, live metrics dashboard</td></tr>
    <tr><td>Long poll</td><td>Emulated push</td><td>Legacy proxies; higher latency/overhead</td></tr>
    <tr><td>Short poll</td><td>Client pull</td><td>Low freshness OK; simplest ops</td></tr>
  </table>
  <p><b>Practice scenarios.</b> Chat → WS with presence. Notification bell → SSE or WS fan-in. Live Jira board → WS for issue moves + optimistic UI + reconcile on reconnect. Dashboard → SSE metrics or poll every 30s if good enough.</p>
''', "topics")

    t2 = topic("rt-ops", "Connections, fan-out, presence, ordering, backpressure", "WebSocket fan-out presence ordering reconnect", "Real-time", f'''
  <ul class="tight">
    <li><b>Connections</b> — 50k concurrent WS ≈ memory + file descriptors + LB sticky config. Scale connection tier horizontally; separate from REST API tier.</li>
    <li><b>Fan-out</b> — issue update → N room subscribers; use pub/sub backbone (Redis/Kafka) between API and WS nodes.</li>
    <li><b>Presence</b> — who’s online; heartbeats; TTL keys in Redis; gossip is hard — central store is fine at moderate scale.</li>
    <li><b>Ordering</b> — per-channel sequence numbers; client drops stale events; CRDTs for collaborative text (hard).</li>
    <li><b>Reconnect</b> — resume token + replay missed events since last seq; idempotent server-side event ids.</li>
    <li><b>Backpressure</b> — slow client buffers fill → drop/coalesce (board moves) or disconnect with reason.</li>
  </ul>
  {diagram('''Issue API --publish--> Redis pub/sub --subscribe--> WS node --push--> browsers
                                                      |
                                               presence in Redis''')}
''', "topics")

    return f'''
<section class="block" id="realtime" data-search="Real-Time WebSocket SSE fan-out presence" data-stype="Section" data-cat="design">
  <p class="kicker">Live UX</p>
  <h2 class="section-title">Real-Time Systems</h2>
  <p class="lede">Connections are a resource. Design fan-out, ordering, and reconnect like you design APIs.</p>
  {t1}{t2}
</section>
'''


def files() -> str:
    t1 = topic("files-storage", "Object storage, multipart, pre-signed URLs", "S3 object storage multipart presigned upload", "File storage", f'''
  <p><b>Object storage</b> (S3/GCS) for attachments, exports, avatars. Metadata in Postgres: <code>file_id, tenant_id, owner_id, sha256, size, status</code>. Bytes in bucket keyed by opaque id — not original filename in path (path traversal, guessability).</p>
  <p><b>Multipart upload</b> — split large files into parts; parallel upload; complete with part ETags. Required for multi-GB Confluence exports or video attachments.</p>
  <p><b>Pre-signed URLs</b> — browser uploads/downloads directly to storage; app never proxies gigabytes. Short TTL, content-type constraint, max size policy.</p>
  <p><b>CDN</b> — public avatars/thumbnails via CDN; private attachments via signed URLs after auth check.</p>
''', "topics")

    t2 = topic("files-react", "React frontend: multi-GB resumable upload", "React upload multipart presigned resumable", "File storage", f'''
  <p><b>Flow.</b> React app requests <code>POST /uploads/initiate</code> → gets <code>uploadId</code> + pre-signed part URLs → uploads parts with progress → <code>POST /uploads/complete</code> → virus scan job (async) → mark <code>ready</code>.</p>
  {code("TypeScript", '''// React: parallel part upload with progress (simplified)
async function uploadLargeFile(file: File, issueId: string) {
  const init = await api.post("/uploads/initiate", {
    issueId,
    filename: file.name,
    size: file.size,
    contentType: file.type,
  });
  const partSize = 8 * 1024 * 1024;
  const parts: { partNumber: number; etag: string }[] = [];
  for (let partNumber = 1, offset = 0; offset < file.size; partNumber++, offset += partSize) {
    const chunk = file.slice(offset, offset + partSize);
    const url = init.partUrls[partNumber - 1];
    const etag = await putWithProgress(url, chunk, (pct) =>
      reportProgress(partNumber, pct),
    );
    parts.push({ partNumber, etag });
  }
  return api.post(`/uploads/${init.uploadId}/complete`, { parts });
}''')}
  <p><b>Resumable.</b> Persist <code>uploadId</code> + completed parts in IndexedDB; on reconnect, list parts from server and skip finished chunks. Show virus-scan pending state in UI — don’t attach to issue until clean.</p>
  {callout("Never stream untrusted uploads through your Node tier at scale — cost, timeout, and memory will hurt before malware scanning does.", "good")}
''', "topics")

    return f'''
<section class="block" id="files" data-search="File Storage S3 multipart presigned upload" data-stype="Section" data-cat="design">
  <p class="kicker">Attachments</p>
  <h2 class="section-title">File Storage</h2>
  <p class="lede">Metadata in your DB; bytes in object storage; browser talks to storage via signed URLs.</p>
  {t1}{t2}
</section>
'''


def search() -> str:
    t1 = topic("search-internals", "Inverted index, tokenization, ranking, shards", "inverted index Elasticsearch ranking sharding", "Search", f'''
  <p><b>Inverted index</b> — term → list of doc ids with positions/frequencies. Tokenization: lowercase, stemming, stop words, language analyzers. <b>Ranking</b> — TF-IDF/BM25 + boosts (title &gt; body, recency, project match).</p>
  <p><b>Shards/replicas</b> — shard = horizontal split of index; replica = copy for read scale and failover. Routing key often <code>tenant_id</code> or <code>project_id</code> to localize queries.</p>
  <p><b>Search is derived.</b> Issue row in Postgres is source of truth; indexer consumes outbox/events. Stale search OK for seconds; wrong permissions is never OK.</p>
''', "topics")

    t2 = topic("search-jira", "Practice: Search Jira issues", "design search Jira issues permissions", "Search", f'''
  <p><b>Requirements.</b> Full-text on summary/description/comments; filters (project, assignee, status); permission-filtered results; p95 &lt; 300ms; index within ~30s of write.</p>
  {diagram('''Issue write --> outbox --> indexer --> OpenSearch shard
Query API --> OpenSearch (candidate ids + text rank)
           --> permission filter (source of truth OR denormalized ACL snapshot)
           --> hydrate snippets from index''')}
  <p><b>Permissions.</b> Options: (1) filter ids post-query against permission service — safe, extra latency; (2) denormalize allowed viewer/principal sets into index — fast, complex invalidation on permission change. Senior answer: start with post-filter + cache hot ACL; denormalize when profiling demands.</p>
  <p><b>Reindex.</b> Blue/green index alias swap; version mapping changes without downtime if you plan alias cutover.</p>
  {callout("If search returns an issue the user cannot open, you failed authorization — not search ranking.", "warn")}
''', "topics")

    return f'''
<section class="block" id="search" data-search="Search inverted index Jira issues OpenSearch" data-stype="Section" data-cat="design">
  <p class="kicker">Derived read model</p>
  <h2 class="section-title">Search</h2>
  <p class="lede">Fast text retrieval is a separate store fed by events — permissions still come from truth.</p>
  {t1}{t2}
</section>
'''


def notifications() -> str:
    t1 = topic("notif-pipeline", "Event → queue → workers", "notification email push in-app queue worker", "Notifications", f'''
  {diagram('''IssueTransitioned event --> notification queue
                                      --> worker: load prefs
                                      --> dedupe (user, event, channel)
                                      --> render template
                                      --> email / push / in-app store
                                      | fail --> retry --> DLQ''')}
  <p><b>Channels.</b> Email (SES), mobile push (APNs/FCM), in-app feed (DB + WS/SSE). User prefs per project/event type/channel.</p>
  <p><b>Ops concerns.</b> Dedupe keys, exponential backoff retry, DLQ for poison templates, rate limit per provider, fan-out math (1 transition × 50 watchers).</p>
  <p><b>Idempotency.</b> UNIQUE(user_id, event_id, channel) prevents duplicate emails on consumer retry.</p>
''', "topics")

    return f'''
<section class="block" id="notifications" data-search="Notifications email push in-app queue DLQ" data-stype="Section" data-cat="design">
  <p class="kicker">Async UX</p>
  <h2 class="section-title">Notifications</h2>
  <p class="lede">Never send email in the request path. Queue, dedupe, retry, and respect prefs.</p>
  {t1}
</section>
'''


def pipelines() -> str:
    t1 = topic("pipe-modes", "Stream vs batch, ETL/ELT, warehouse", "ETL ELT stream batch data warehouse", "Data pipelines", f'''
  <p><b>Batch</b> — hourly/daily aggregates; cheap, high latency. <b>Stream</b> — Kafka/Kinesis → Flink/Spark streaming; seconds latency, higher ops.</p>
  <p><b>ETL</b> — transform before load into warehouse. <b>ELT</b> — load raw, transform in warehouse (dbt). Modern default for analytics teams.</p>
  <p><b>Warehouse</b> — Snowflake/BigQuery/Redshift for BI; not OLTP. Issue DB stays OLTP; product analytics reads derived tables.</p>
''', "topics")

    t2 = topic("pipe-dashboard", "Practice: real-time analytics dashboard", "real-time analytics dashboard pipeline design", "Data pipelines", f'''
  <p><b>Goal.</b> Exec dashboard: issues created/transitions per minute, p99 API latency, error rate — near real-time.</p>
  {diagram('''App logs/metrics --> OTel collector --> time-series DB (metrics)
Issue events --> stream --> aggregate windows --> dashboard API
Historical --> nightly batch --> warehouse (trends)''')}
  <p><b>Design.</b> Metrics path (Prometheus/Datadog) for latency/errors; event stream for business counters; 10–30s refresh in UI via SSE or poll. Separate hot path from expensive joins.</p>
  {callout("Practice: “Real-time enough” beats perfectly real-time if it saves operating a Flink cluster for v1.”", "good")}
''', "topics")

    return f'''
<section class="block" id="pipelines" data-search="Data Pipelines ETL stream batch warehouse" data-stype="Section" data-cat="design">
  <p class="kicker">Analytics path</p>
  <h2 class="section-title">Data Pipelines</h2>
  <p class="lede">OLTP serves users; pipelines serve questions. Know stream vs batch trade-offs.</p>
  {t1}{t2}
</section>
'''


def observability() -> str:
    t1 = topic("obs-pillars", "Logs, metrics, traces, correlation IDs", "logs metrics traces correlation id SLI SLO", "Observability", f'''
  <p><b>Logs</b> — structured JSON, searchable fields (tenant_id, issue_id, trace_id). <b>Metrics</b> — counters/histograms for RPS, error rate, queue lag. <b>Traces</b> — span per outbound call; find which hop blew the p99 budget.</p>
  <p><b>Correlation ID</b> — generated at edge, propagated through headers, included in every log line and async message.</p>
  <p><b>SLI/SLO/SLA.</b> SLI = measured signal (transition success rate). SLO = internal target (99.9%/30d). SLA = contractual consequence. Error budget drives release policy.</p>
''', "distTopics")

    t2 = topic("obs-debug", "Debug: issue transition randomly slow", "debug slow transition trace observability", "Observability", f'''
  <p><b>Practice scenario.</b> Users report Jira transitions “randomly” take 5s. p50 is fine; p99 spiked.</p>
  <ol>
    <li>Check metrics: p99 by route, region, tenant — is it one whale tenant or global?</li>
    <li>Traces: compare fast vs slow — DB wait? permission service? audit queue backlog?</li>
    <li>Logs: filter <code>trace_id</code> from a slow request — lock waits, retry loops, missing index?</li>
    <li>Infra: connection pool saturation, replica lag causing read-after-write retries?</li>
    <li>Recent deploy/feature flag — canary correlation?</li>
  </ol>
  {callout("Random slowness is usually tail amplification: one dependency without timeout, N+1 queries, or GC pause — traces prove which.", "good")}
''', "distTopics")

    return f'''
<section class="block" id="observability" data-search="Observability logs metrics traces SLO debugging" data-stype="Section" data-cat="reliability">
  <p class="kicker">Operate</p>
  <h2 class="section-title">Observability</h2>
  <p class="lede">You cannot fix what you cannot see. Instrument the critical path before the incident.</p>
  {t1}{t2}
</section>
'''


def security() -> str:
    t1 = topic("sec-defensive", "TLS, secrets, encryption, audit, S2S", "TLS secrets encryption audit log defensive security", "Security", f'''
  <ul class="tight">
    <li><b>TLS everywhere</b> — public and internal where feasible; mTLS for high-trust S2S</li>
    <li><b>Secrets</b> — vault/KMS; rotate; never in repo or client bundles; inject at runtime</li>
    <li><b>Encryption at rest</b> — DB and object storage default provider encryption; field-level for highly sensitive columns</li>
    <li><b>Audit logs</b> — who changed permission, exported data, admin actions — append-only, tamper-evident storage</li>
    <li><b>S2S auth</b> — workload identity; no shared DB password across 12 services</li>
    <li><b>Input validation</b> — size limits, content-type checks on uploads; parameterized SQL</li>
    <li><b>Least privilege</b> — IAM roles scoped per service; break-glass documented</li>
  </ul>
  {callout("Defensive posture only: design to reduce blast radius and prove access in audits — not to discuss exploit chains.", "good")}
''', "backendTopics")

    return f'''
<section class="block" id="security" data-search="Security TLS secrets encryption audit defensive" data-stype="Section" data-cat="security">
  <p class="kicker">Hardening</p>
  <h2 class="section-title">Security</h2>
  <p class="lede">Assume breach. Encrypt, isolate tenants, audit admin paths, and keep secrets out of git.</p>
  {t1}
</section>
'''
