from util import callout, esc


ADRS = [
    (
        "Postgres vs NoSQL",
        "Multi-tenant issue tracker: rich queries (project + status + assignee + text), ACID transitions, tenant isolation, 50M issues growing 20%/year. Some teams want flexible custom fields.",
        "Postgres as system of record for issues, comments, permissions, and transitions. Document/KV store only where access pattern is truly key-value (e.g. per-issue activity blob, session, idempotency keys) — not as the primary issue graph.",
        "Mongo for everything; Dynamo for issues; Postgres only; polyglot with event sync.",
        "Postgres wins when you need joins, constraints, and ad-hoc admin queries. NoSQL wins when access pattern is fixed, write volume per key is huge, and you can denormalize aggressively. Custom fields push toward JSONB columns or EAV — not automatic NoSQL.",
        "Search still needs Elasticsearch/OpenSearch — Postgres is not your inverted index. Migrations and connection pooling become the ops focus. Revisit NoSQL for a hot shard only after measuring a specific key skew.",
    ),
    (
        "Redis vs DB cache",
        "Issue detail p99 is 180ms at 2k RPS; 70% reads are repeat views of the same 5k popular issues. Postgres CPU is climbing. Team proposes 'Redis in front of everything.'",
        "Cache-aside Redis for issue detail + board snapshot with explicit TTL (60–120s) and event-driven invalidation on write. Do not cache permission matrices without tenant-scoped keys and short TTL. Postgres remains source of truth.",
        "Postgres query cache; CDN for JSON; materialized views only; Redis as primary store.",
        "Redis is fast but adds invalidation complexity and another failure domain. DB read replicas help read scaling without stampede risk if queries are bounded. Write-through to Redis on every comment is usually wrong — write volume + invalidation fan-out.",
        "Document cache key schema and invalidation events in the ADR. Alert on Redis memory and hit rate. Cold start: stagger TTL + singleflight on hot keys.",
    ),
    (
        "REST vs events",
        "Issue transition must update DB, audit log, search index, and notify watchers. Today: synchronous REST chain from API → 4 downstream HTTP calls; p99 spikes when search is slow.",
        "REST for command/query from clients. After successful DB commit, publish domain events (outbox → Kafka/SQS) for search, notifications, analytics. Clients get 202/200 with issue state; side effects are async with idempotent consumers.",
        "Keep sync REST fan-out; GraphQL subscriptions for everything; event sourcing for issues.",
        "Events decouple latency and failure domains but add eventual consistency UX. REST stays simpler for CRUD and debugging. Event-first without outbox risks lost messages on crash between commit and publish.",
        "Define user-visible consistency: 'search lags ≤30s' is acceptable; 'transition must be atomic in DB' is not negotiable. Consumers must be idempotent; DLQ + replay runbook required.",
    ),
    (
        "Kafka vs message queue",
        "Notification pipeline: 500 events/sec average, 5k/sec peak on release day. Need retry, DLQ, and multiple independent consumers (email, in-app, push, analytics). Ordering per issue preferred but not global.",
        "Kafka (or Kafka-like log) when you need replay, multiple consumer groups, and retention for reprocessing. SQS/Rabbit when workload is task queue with competing consumers and no replay requirement. Here: Kafka with partition key = issue_id for per-issue ordering; email worker is separate consumer group.",
        "Kafka because scalable; single SQS queue; Rabbit with one queue per channel.",
        "Kafka is not free: ops, partition planning, consumer lag monitoring. A queue is simpler for fire-and-forget tasks. Kafka wins when analytics and notifications both need the same stream without duplicating publish.",
        "Monitor consumer lag per group. Hot partition if one celebrity issue gets 10k watchers — mitigation: sub-partition by batch id or fan-out worker before Kafka.",
    ),
    (
        "Monolith vs microservices",
        "40 engineers, one product (Jira-like), shared release train, heavy cross-feature transactions (issue + comment + permission). Search team wants independent deploy cadence.",
        "Modular monolith for issue/comment/permission core with strict module boundaries and CI import lint. Extract search and notification delivery as services only where deploy independence and different scaling profile justify network + transaction cost.",
        "Full microservices day one; never split; serverless everything.",
        "Microservices do not fix org problems by themselves — they add distributed failure modes. Monolith avoids 2PC on issue transition. Split when team is blocked on release or resource profile diverges (search CPU vs OLTP).",
        "Core monolith keeps ACID transitions simple. Search service accepts eventual consistency contract. Document S2S auth and correlation IDs before second service ships.",
    ),
    (
        "Sync vs async",
        "User clicks 'Assign to me' — must see updated assignee immediately. Same action triggers email to 200 watchers and search index update.",
        "Sync path: validate permission, update Postgres, return new issue JSON (read-your-writes). Async path: enqueue notification + search index jobs via outbox. Never block the HTTP response on email SMTP or Elasticsearch.",
        "Async everything including the DB write; sync fan-out to all downstreams; websocket-only updates.",
        "Sync minimizes user confusion but limits tail latency budget. Async maximizes throughput but needs status UX for long operations. Senior rule: sync what the user waits for; async what they tolerate lag on.",
        "API returns consistent issue entity; badge/email may lag. Idempotent workers; user sees 'Notifications sending' only if SLA requires it.",
    ),
    (
        "SQL vs NoSQL (access-pattern lens)",
        "Analytics dashboard: 'issues closed per team per week' plus operational queries by issue id. Write pattern: append-only events; read pattern: aggregate by team/time and point lookup by id.",
        "SQL warehouse (BigQuery/Snowflake/Postgres replica) for aggregates. OLTP stays Postgres. If point lookups at billions of rows/day with fixed key-only access, add KV (Dynamo/Redis) — not replace SQL for reporting.",
        "NoSQL for analytics because scale; one Mongo cluster for all; CSV exports.",
        "The question is access pattern, not religion. SQL handles ad-hoc aggregates with known cost if indexed/partitioned. NoSQL handles predictable key access at extreme QPS. Mixing without boundaries creates dual-write hell.",
        "ETL from OLTP to warehouse with lag SLA. Operational APIs never hit the warehouse.",
    ),
    (
        "WebSocket vs polling",
        "Live board: 30 users, remote card moves, presence avatars. Infra team prefers no persistent connections at edge. Mobile clients on flaky networks.",
        "WebSocket (or SSE) for board room when product commits to sub-second remote updates; fallback to poll every 15–30s on disconnect. REST remains source for full board snapshot on reconnect. Do not WS the entire issue graph.",
        "WS always; poll every 1s; long poll forever; Firestore.",
        "WS saves bandwidth at steady state but costs connection memory and complicates load balancers. Polling is correct when freshness of 30s is fine. Senior answer states reconnect, auth, and backpressure — not protocol zeal.",
        "Auth on connect (cookie/session upgrade). Heartbeat + idle timeout. On reconnect: GET snapshot + apply missed events by version vector or since cursor.",
    ),
    (
        "Strong vs eventual consistency",
        "Payment for premium tier (strong), like count on comment (eventual), issue title after edit (read-your-writes), global search index (eventual).",
        "Classify per entity/action. Money: serializable/strong in ledger DB. Issue transition: transactional in OLTP + async index. Likes: counter with periodic reconcile or CRDT if high write contention. Document each UX contract.",
        "Eventual everywhere for simplicity; strong everywhere via 2PC; ignore consistency labels.",
        "Strong consistency costs latency and availability under partition. Eventual is fine when users expect lag or when approximate counts are OK. Wrong: eventual for inventory deduction without reservation pattern.",
        "Product sign-off on lag numbers. Tests assert RYW after mutation. Search shows 'index updating' if lag > SLA.",
    ),
    (
        "Single DB vs sharding",
        "Postgres at 2TB, 8k write TPS peak on transitions, one tenant (enterprise) generates 40% of writes. Vertical scale exhausted.",
        "Shard by tenant_id (or tenant group) when cross-tenant queries are rare or can be federated. Keep global metadata (users, billing) on a catalog DB. Avoid shard until replica + partitioning + archive prove insufficient — sharding hurts ad-hoc queries and migrations.",
        "Shard by issue_id immediately; one DB forever; NewSQL automatically.",
        "Single DB simplifies transactions and joins. Sharding buys write headroom at cost of cross-shard queries, rebalancing, and operational pain. Hot tenant may need isolation to dedicated shard, not whole-system shard.",
        "Router layer maps tenant → shard. Background jobs for cross-shard admin. Rebalance playbook before production shard.",
    ),
    (
        "CDN vs origin",
        "Global users fetch attachments (PDFs, images) and static API docs. Authenticated issue JSON must not leak via shared cache.",
        "CDN for public/immutable assets (hashed JS, public docs, signed attachment URLs with short TTL). Origin handles authenticated API with Cache-Control: private/no-store. Pre-signed S3 URLs so bytes bypass app server.",
        "CDN cache all API responses; no CDN; origin serves everything.",
        "CDN reduces latency and origin load for cacheable bytes. Wrong cache headers on private JSON is a SEV. Signed URLs shift auth to token scope and expiry — not 'security through obscurity.'",
        "Separate cache policies per path. Pen-test shared cache keys. Monitor CDN 403/404 on expired signatures.",
    ),
    (
        "Server cache vs client cache",
        "Issue list refetched on every navigation; mobile app also caches locally. Stale assignee after colleague's change causes wrong triage.",
        "Server: Redis/cache-aside for hot lists with invalidation on write. Client: short staleTime + background revalidate; optimistic only for user's own actions. ETag/If-None-Match on GET issue for bandwidth. Never client-only cache for shared collaborative fields without version checks.",
        "Client cache only to reduce server load; server cache only; no cache.",
        "Client cache improves perceived speed offline-ish; server cache protects DB. Both without coordination → stale UI. Version column or updatedAt in response lets client merge intelligently.",
        "Document staleTime per resource. 409 on stale write. Server invalidates list cache keys on issue update pattern.",
    ),
]


def _adr_card(i: int, title: str, ctx: str, dec: str, alt: str, trade: str, cons: str) -> str:
    aid = f"adr-{i}"
    return f'''
<article class="topic adr" id="{aid}" data-search="ADR {esc(title)}" data-stype="ADR">
  <h3>ADR: {esc(title)}</h3>
  <p><b>Context.</b> {ctx}</p>
  <p><b>Decision.</b> {dec}</p>
  <p><b>Alternatives.</b> {alt}</p>
  <p><b>Trade-offs.</b> {trade}</p>
  <p><b>Consequences.</b> {cons}</p>
  <p><button type="button" class="toggle-btn" data-complete="topics" data-cid="{aid}">Mark complete</button></p>
</article>'''


def adrs() -> str:
    cards = [_adr_card(i, *row) for i, row in enumerate(ADRS, 1)]
    n = len(ADRS)
    return f'''
<section class="block" id="adrs" data-search="Architecture Decision Records backend system design" data-stype="Section" data-cat="architecture">
  <p class="kicker">{n} decision records</p>
  <h2 class="section-title">Architecture Decision Records</h2>
  <p class="lede">Practice explaining <b>why</b>, not buzzwords. Each ADR follows Context → Decision → Alternatives → Trade-offs → Consequences. Kafka, microservices, and NoSQL are not automatically correct — constraints decide.</p>
  {callout("Senior move: name the constraint first ('we need replay for analytics' → Kafka; 'user waits on screen' → sync OLTP). Then reject one alternative with a concrete failure mode.")}
  {''.join(cards)}
</section>
'''
