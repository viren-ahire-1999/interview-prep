from util import code, topic, diagram, callout


def _sql_practice(qid: str, n: int, prompt: str, answer: str, mistake: str) -> str:
    return f'''
<article class="topic" id="{qid}" data-search="SQL practice interview {n}" data-stype="Practice">
  <div class="meta-row"><span class="badge badge-medium">Practice {n}</span></div>
  <h3>{prompt}</h3>
  <p><button type="button" class="toggle-btn" data-toggle="{qid}-a">Reveal answer</button>
     <button type="button" class="toggle-btn" data-complete="topics" data-cid="{qid}">Mark complete</button></p>
  <div class="reveal" id="{qid}-a">
    <p><b>Answer.</b> {answer}</p>
    <p><b>Common mistake.</b> {mistake}</p>
  </div>
</article>'''


def api() -> str:
    t_rest = topic("api-rest", "REST — mental model and resource design", "REST resources HTTP verbs idempotent safe", "API", f'''
  <p><b>Mental model.</b> REST is not “JSON over HTTP.” It is a style where <i>named resources</i> (issues, comments, transitions) are manipulated with a small verb set, and the server owns authorization and invariants. URLs are bookmarks for humans and clients; they are not the security boundary.</p>
  <p><b>Technical.</b> Safe methods (GET, HEAD, OPTIONS) should not change server state. Idempotent methods (PUT, DELETE) can be retried without double effect. POST creates or triggers workflows where the client does not supply the final URL. Use nouns in paths, verbs in HTTP methods — <code>POST /issues/{{id}}/transitions</code>, not <code>POST /moveIssue</code>.</p>
  {code("typescript", '''// Jira-like issue resource (tenant-scoped)
const res = await fetch("/rest/api/3/issue/PROJ-42", {
  headers: {
    Authorization: `Bearer ${token}`,
    "X-Atlassian-Token": "no-check", // CSRF on cookie auth in real Jira
    Accept: "application/json",
  },
});
if (res.status === 404) { /* issue missing OR no permission — same shape */ }
const issue = await res.json();''')}
  {code("http", '''GET /rest/api/3/issue/PROJ-42/comments?cursor=eyJpZCI6MTIzfQ HTTP/1.1
Host: tenant.atlassian.net
Authorization: Bearer eyJ...

HTTP/1.1 200 OK
Content-Type: application/json

{
  "values": [{ "id": "124", "body": "LGTM", "author": { "accountId": "..." } }],
  "nextPage": "eyJpZCI6MTI0fQ"
}''')}
  <p><b>Production example.</b> Confluence page REST returns a stable <code>id</code> and a human <code>title</code>. Clients cache by id; search and backlinks are separate derived views. If you expose <code>GET /pages/by-slug/{{slug}}</code>, document that slug changes on rename and that slug is not globally unique across spaces without a composite key.</p>
  <p><b>Trade-offs.</b> REST’s strength is cacheability, predictable URLs, and incremental adoption. Its weakness is chatty UIs that need five round trips for one screen — that is a client/BFF problem, not an automatic reason to switch protocols.</p>
  <p><b>Interview.</b> “Design issue + comment APIs.” Start with resources, error model, pagination, and who may call what — not HTTP status trivia.</p>
  {callout("Mistake: treating 404 as ‘not found’ only. In multi-tenant products, 404 often means ‘not found OR forbidden’ to avoid leaking existence.")}
''', "topics")

    t_pagination = topic("api-pagination", "Pagination, filtering, sorting, versioning", "cursor offset pagination filter sort API version", "API", f'''
  <p><b>Mental model.</b> Pagination is a contract about stable iteration over a moving dataset. Filtering and sorting change which rows qualify; pagination must not assume the dataset is frozen while the client walks pages.</p>
  <p><b>Technical — offset vs cursor.</b></p>
  <table>
    <tr><th>Style</th><th>Good for</th><th>Breaks when</th></tr>
    <tr><td>Offset/limit</td><td>Admin exports, small tables, “page 3 of admin UI”</td><td>Deep offsets on large tables (sort + skip scans), concurrent inserts/deletes shift windows</td></tr>
    <tr><td>Keyset/cursor</td><td>Infinite scroll, issue activity feeds, comment threads</td><td>Sort key not unique — tie-breaker required; opaque cursors need versioning on schema change</td></tr>
  </table>
  {code("typescript", '''// Cursor pagination client — always follow nextPage, never invent offsets
type Page<T> = {{ values: T[]; nextPage?: string }};

async function* listComments(issueKey: string) {{
  let cursor: string | undefined;
  do {{
    const qs = cursor ? `?cursor=${{encodeURIComponent(cursor)}}` : "";
    const page: Page<Comment> = await get(`/issues/${{issueKey}}/comments${{qs}}`);
    for (const c of page.values) yield c;
    cursor = page.nextPage;
  }} while (cursor);
}}''')}
  <p><b>Filtering.</b> Prefer explicit query params with an allow-list: <code>project=PROJ&amp;status=In Progress&amp;assignee=me</code>. For complex filters (Jira JQL-shaped), a <code>POST /search</code> with a structured body beats infinitely long GET URLs — and makes caching policy explicit (usually none on search).</p>
  <p><b>Versioning.</b> Path version (<code>/v3/</code>) for breaking changes; additive JSON fields are not a version bump. Sunset headers + dual-write period beat breaking mobile clients silently.</p>
  <p><b>Production example.</b> Issue search sorted by <code>updated DESC</code>: cursor is <code>(updated_at, id)</code> encoded — never cursor on <code>updated</code> alone or two issues updated in the same millisecond swap order between pages.</p>
  <p><b>Trade-offs.</b> Cursors are harder for “jump to page 17” UX. If the product needs that, expose offset for shallow pages only and cursor for deep feeds — and say so.</p>
  <p><b>Interview.</b> “Paginate millions of rows?” Keyset on indexed sort key + tie-breaker; avoid <code>OFFSET 1000000</code>.</p>
''', "topics")

    t_reliability = topic("api-reliability", "Errors, idempotency, retries, rate limits", "idempotency retry 429 rate limit error model", "API", f'''
  <p><b>Mental model.</b> Distributed clients will retry. Your API must decide which retries are safe, which errors are actionable, and how overload presents itself.</p>
  <p><b>Technical — error model.</b> Return a stable machine code, human message, optional field errors, and a correlation id. Same shape for 4xx and 5xx.</p>
  {code("json", '''{
  "error": "transition_invalid",
  "message": "Cannot transition from Done to In Progress",
  "fields": { "status": "Issue is closed" },
  "correlationId": "9f3c2a1b-..."
}''')}
  <p><b>Idempotency.</b> POST that creates billable side effects (create issue, post comment, transition) should accept <code>Idempotency-Key</code>. Store key → response mapping with TTL; duplicate key returns original 201/409, not a second row.</p>
  {code("typescript", '''await fetch("/rest/api/3/issue/PROJ-42/transitions", {{
  method: "POST",
  headers: {{
    "Content-Type": "application/json",
    "Idempotency-Key": clientRequestId, // UUID from the UI action
  }},
  body: JSON.stringify({{ transition: {{ id: "31" }} }}),
}});''')}
  <p><b>Retries.</b> Retry GET and idempotent PUT/DELETE on 502/503/504 with exponential backoff + jitter. Do not blindly retry POST unless idempotency keys exist. Honor <code>Retry-After</code> on 429/503.</p>
  <p><b>Rate limiting.</b> Return 429 with <code>Retry-After</code> and a code like <code>rate_limit_exceeded</code>. Limit per tenant + per user + per endpoint class (search vs CRUD). Atlassian-scale integrations hit API tokens — document burst vs sustained.</p>
  <p><b>Production example.</b> Automation rule fires 500 transitions/minute during bulk import. Without per-tenant limits, one customer degrades transition latency for everyone on the shard.</p>
  <p><b>Trade-offs.</b> Strict rate limits protect the fleet but frustrate power users; offer bulk endpoints or async jobs instead of raising limits without isolation.</p>
  <p><b>Interview.</b> “What happens if the client retries transition twice?” Walk idempotency key + server-side state machine + 409 on illegal second transition.</p>
  {callout("Mistake: retrying POST without idempotency keys — that is how duplicate Jira comments get created.", "warn")}
''', "topics")

    t_auth = topic("api-auth", "Authentication and authorization on the server", "OAuth JWT RBAC ABAC tenant scope authz", "API", f'''
  <p><b>Mental model.</b> Authentication proves <i>who</i>. Authorization proves <i>what they may do on which row</i>. The UI hiding a button is not authorization.</p>
  <p><b>Technical.</b> Bearer tokens (OAuth 2.0), scoped API tokens, and session cookies each imply different CSRF and caching rules. Every handler resolves principal → tenant membership → resource ACL → action.</p>
  <p><b>Production example.</b> <code>GET /issue/PROJ-42</code>: resolve issue’s <code>tenant_id</code> and project; check <code>issue:read</code> in that project. Cross-tenant id guessing must 404/403 consistently. Comment create requires <code>comment:add</code> and issue not in archived state — enforce in the service, not only in JQL.</p>
  <p><b>Trade-offs.</b> RBAC is operable; ABAC (field-level, issue security levels) is expressive but expensive to evaluate per row. Cache permission snapshots with short TTL and invalidate on role change — never cache “allowed forever.”</p>
  <p><b>Interview.</b> “User A shares a link; user B opens it.” Explain org boundary, issue security scheme, and why the API must re-check on every request.</p>
  {callout("Mistake: putting tenant_id only in the JWT claim without verifying it matches the resource row on every query.")}
''', "topics")

    t_graphql = topic("api-graphql", "GraphQL — when it earns the complexity", "GraphQL N+1 BFF resolver federation", "API", f'''
  <p><b>Mental model.</b> GraphQL is a <i>query language for a graph of resolvers</i>, usually one HTTP endpoint. It solves over-fetching and under-fetching for product-shaped reads — not every API.</p>
  <p><b>Technical.</b> Client specifies the tree; server resolves fields. Danger: N+1 queries if each issue’s assignee triggers a separate DB round trip. Mitigate with batch loaders (DataLoader), JOINs at the service layer, or persisted queries.</p>
  {code("graphql", '''query IssueBoard($project: ID!) {{
  project(id: $project) {{
    issues(first: 50, after: $cursor) {{
      nodes {{
        key
        summary
        assignee {{ displayName avatarUrl }}
        commentCount
      }}
      pageInfo {{ endCursor hasNextPage }}
    }}
  }}
}}''')}
  <p><b>Production example.</b> Jira issue view first paint: GraphQL can fetch issue + fields + permissions + three comments in one round trip. But search, bulk export, and webhooks remain REST/event-shaped — GraphQL rarely replaces the whole surface.</p>
  <p><b>Trade-offs — GraphQL is not automatically better.</b></p>
  <ul>
    <li>Caching at CDN edge is harder than GET-with-URL REST.</li>
    <li>Complexity moves to resolvers, rate limiting per field, and query cost analysis.</li>
    <li>Public third-party integrations often prefer stable REST OpenAPI docs.</li>
    <li>A thin BFF aggregating 3 REST calls may be simpler than GraphQL for one frontend team.</li>
  </ul>
  <p><b>Interview.</b> “REST + BFF vs GraphQL for issue page?” Compare team count, client diversity, cache needs, and operability — pick one and name what you would not do.</p>
  {callout("Mistake: adopting GraphQL because ‘the frontend wants one request’ without a query cost budget — a single anonymous query can still take the database down.")}
''', "topics")

    t_grpc = topic("api-grpc", "gRPC and internal service contracts", "gRPC protobuf streaming internal microservices", "API", f'''
  <p><b>Mental model.</b> gRPC is a binary, contract-first RPC framework (Protobuf on HTTP/2). It shines <i>inside</i> the datacenter: low latency, strong schemas, streaming.</p>
  <p><b>Technical.</b> .proto files version fields with numbered tags; never reuse field numbers. Unary for request/response; server streaming for large result sets; client/bidi streaming for real-time ingestion.</p>
  <p><b>Production example.</b> Issue indexing pipeline: <code>IssueService.StreamChanges</code> pushes change events to search workers. Browser clients still use JSON REST — gRPC-web is optional and adds operational weight.</p>
  <p><b>Trade-offs.</b> Excellent for service-to-service; poor default for public browser APIs without a gateway. Debugging with curl is harder — invest in grpcurl, reflection, and good status details.</p>
  <p><b>Interview.</b> “When gRPC over REST internally?” Schema evolution, streaming, and typed codegen — not ‘because Google uses it.’</p>
''', "topics")

    t_realtime = topic("api-realtime", "WebSockets vs SSE", "WebSocket SSE realtime presence live updates", "API", f'''
  <p><b>Mental model.</b> Both push server → client. WebSockets are bidirectional full-duplex; SSE is unidirectional text/event-stream over HTTP.</p>
  {diagram("""Browser                    Edge/API
   |  SSE: GET /events (long-lived HTTP)
   |<-------------------- text/event-stream
   |
   |  WS: Upgrade: websocket
   |<=======================> bidirectional frames""")}
  <p><b>Technical.</b> SSE: auto reconnect, works through many corporate proxies, one-way fan-out (issue updated, comment added). WebSockets: typing presence, collaborative cursors, binary frames — but sticky sessions, connection limits, and custom heartbeat.</p>
  <p><b>Production example.</b> Confluence live edit cursors → WebSocket or CRDT channel. “Issue PROJ-42 status changed” toast on a board → SSE or polling with ETag is often enough. Jira does not need a persistent socket on every tab for read-mostly boards.</p>
  <p><b>Trade-offs — WebSockets are not automatically better than SSE.</b></p>
  <ul>
    <li>SSE is simpler to operate (standard HTTP load balancing, retry built in).</li>
    <li>WebSockets cost one connection per tab — 50k concurrent users is a capacity line item.</li>
    <li>If the client only listens, SSE + POST for commands keeps auth and idempotency familiar.</li>
  </ul>
  <p><b>Interview.</b> “Realtime board updates?” Ask freshness SLA (seconds vs ms), bidirectional need, and mobile background behavior — then pick SSE, WS, or short polling.</p>
  {callout("Mistake: opening a WebSocket per micro-widget on the issue page — connection storms dominate.")}
''', "topics")

    return f'''
<section class="block" id="api" data-search="API Design REST GraphQL gRPC WebSocket SSE" data-stype="Section" data-cat="design">
  <p class="kicker">Contracts</p>
  <h2 class="section-title">API Design</h2>
  <p class="lede">Frontends are clients of contracts. Senior design names resources, failure modes, and the protocol that matches the access pattern — not the trendiest transport.</p>
  {t_rest}
  {t_pagination}
  {t_reliability}
  {t_auth}
  {t_graphql}
  {t_grpc}
  {t_realtime}
</section>
'''


def database() -> str:
    t_model = topic("db-model", "Relational mental model — tables, keys, tenants", "PostgreSQL schema PK FK normalization tenant_id", "Database", f'''
  <p><b>Mental model.</b> Postgres is row storage with ACID transactions and declarative constraints. The schema is the contract that outlives any single service deploy.</p>
  <p><b>Technical.</b> Primary keys identify rows. Foreign keys enforce referential integrity (or deliberate ON DELETE rules). Every multi-tenant table carries <code>tenant_id</code> and queries filter on it — composite keys and indexes lead with <code>tenant_id</code>.</p>
  {code("sql", '''CREATE TABLE tenants (
  id         UUID PRIMARY KEY,
  slug       TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE projects (
  id         UUID PRIMARY KEY,
  tenant_id  UUID NOT NULL REFERENCES tenants(id),
  key        TEXT NOT NULL,              -- e.g. 'PROJ'
  name       TEXT NOT NULL,
  UNIQUE (tenant_id, key)
);

CREATE TABLE issues (
  id           UUID PRIMARY KEY,
  tenant_id    UUID NOT NULL REFERENCES tenants(id),
  project_id   UUID NOT NULL REFERENCES projects(id),
  issue_number INT NOT NULL,             -- per-project sequence
  summary      TEXT NOT NULL,
  status       TEXT NOT NULL,
  assignee_id  UUID,
  updated_at   TIMESTAMPTZ NOT NULL,
  UNIQUE (tenant_id, project_id, issue_number)
);

CREATE TABLE comments (
  id         UUID PRIMARY KEY,
  tenant_id  UUID NOT NULL REFERENCES tenants(id),
  issue_id   UUID NOT NULL REFERENCES issues(id) ON DELETE CASCADE,
  author_id  UUID NOT NULL,
  body       TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE watchers (
  tenant_id  UUID NOT NULL REFERENCES tenants(id),
  issue_id   UUID NOT NULL REFERENCES issues(id) ON DELETE CASCADE,
  user_id    UUID NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, issue_id, user_id)
);''')}
  <p><b>Production example.</b> Issue key <code>PROJ-42</code> is <code>(tenant_id, project.key, issue_number)</code> — never a global serial. Comments cascade-delete with issue; watchers use composite PK to prevent duplicates without a surrogate id explosion.</p>
  <p><b>Trade-offs.</b> UUID PKs: no hot insert on a global sequence, but wider indexes. <code>BIGSERIAL</code> per tenant/project is an alternative if keys stay internal.</p>
  <p><b>Interview.</b> “Add soft delete.” Column + partial unique indexes (<code>WHERE deleted_at IS NULL</code>) — and say how JQL/search excludes tombstones.</p>
  {callout("Mistake: unique constraint on issue_number alone — collisions across projects on day one.")}
''', "topics")

    t_norm = topic("db-norm", "Normalization vs denormalization", "3NF denormalize read model cache", "Database", f'''
  <p><b>Mental model.</b> Normalization reduces update anomalies; denormalization trades write simplicity for read speed. 3NF is a default for OLTP source of truth — not a religion.</p>
  <p><b>Technical.</b> Normalize: comments in <code>comments</code>, not JSON blob on <code>issues</code>, so pagination and permissions stay row-level. Denormalize deliberately: <code>comment_count</code> on <code>issues</code> maintained by trigger or async counter to avoid <code>COUNT(*)</code> on hot board queries.</p>
  <p><b>Production example.</b> Board column shows assignee avatar + name. Option A: JOIN users on every board row. Option B: denormalized <code>assignee_display</code> snapshot updated when user renames — acceptable if stale name for 30s is OK. Option C: read model table rebuilt from events — when search/board SLO diverges from OLTP.</p>
  <p><b>Trade-offs.</b> Denormalization without an invalidation story becomes silent drift. Say who wins on conflict (source of truth is still <code>users</code>).</p>
  <p><b>Interview.</b> “When is denormalization senior?” When you can name the read path, staleness budget, and reconciliation — not “because JOINs are slow.”</p>
''', "topics")

    t_index = topic("db-index", "Indexes and why the planner ignores them", "B-tree composite index EXPLAIN covering index", "Database", f'''
  <p><b>Mental model.</b> Indexes are sorted shortcuts maintained on write. The planner picks seq scan vs index scan based on selectivity, statistics, and query shape — not your hope.</p>
  <p><b>Technical.</b> B-tree default. Composite index <code>(tenant_id, project_id, updated_at DESC)</code> supports board queries filtered by tenant+project sorted by recency. Left-prefix rule: index <code>(a,b,c)</code> helps <code>WHERE a</code> and <code>WHERE a,b</code>, not bare <code>WHERE b</code>.</p>
  {code("sql", '''-- Board: issues in project, newest first
CREATE INDEX idx_issues_project_updated
  ON issues (tenant_id, project_id, updated_at DESC, id);

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, summary, status, updated_at
FROM issues
WHERE tenant_id = $1 AND project_id = $2
ORDER BY updated_at DESC, id DESC
LIMIT 50;''')}
  <p><b>Why an index might not be used.</b></p>
  <ul>
    <li>Function on column: <code>WHERE lower(summary) = 'bug'</code> skips plain index — need expression index or trigram.</li>
    <li>Low selectivity: “30% of rows match” → seq scan cheaper.</li>
    <li>Stale stats after bulk import — run <code>ANALYZE</code>.</li>
    <li>Type coercion: comparing UUID column to text without cast.</li>
    <li><code>OR</code> across incompatible predicates — planner gives up or bitmaps multiple indexes.</li>
    <li>Leading column missing: filter only <code>project_id</code> without <code>tenant_id</code> on composite index.</li>
  </ul>
  <p><b>Production example.</b> Search by summary substring needs <code>pg_trgm</code> GIN index — a btree on <code>summary</code> will not help <code>LIKE '%foo%'</code>.</p>
  <p><b>Trade-offs.</b> More indexes → slower writes and bulk migration time. Index what you measure, not every column in the ER diagram.</p>
  <p><b>Interview.</b> “Query has an index but is slow?” Walk EXPLAIN, selectivity, leading column, and hidden seq scan on sort.</p>
''', "topics")

    t_tx = topic("db-tx", "Transactions, isolation, locks, MVCC", "ACID isolation MVCC deadlock row lock", "Database", f'''
  <p><b>Mental model.</b> A transaction groups writes into one atomic unit. Isolation level defines which anomalies you accept. Postgres uses MVCC: readers don’t block writers; writers don’t block readers — but conflicts still happen.</p>
  <p><b>Technical.</b> Read committed (default): each statement sees committed snapshots. Repeatable read: transaction sees consistent snapshot — phantoms still possible on range unless serializable. Row locks: <code>SELECT ... FOR UPDATE</code> for transition workflows.</p>
  {code("sql", '''BEGIN;
SELECT status FROM issues
  WHERE tenant_id = $1 AND id = $2
  FOR UPDATE;
-- validate transition allowed
UPDATE issues SET status = 'In Progress', updated_at = now()
  WHERE tenant_id = $1 AND id = $2;
INSERT INTO issue_history (issue_id, from_status, to_status, actor_id)
  VALUES ($2, 'To Do', 'In Progress', $3);
COMMIT;''')}
  <p><b>MVCC.</b> Updates create new row versions; old versions vacuum away. Long transactions hold back vacuum → bloat and frozen-id pressure. Keep transactions short.</p>
  <p><b>Production example.</b> Two automations transition the same issue: second transaction blocks on <code>FOR UPDATE</code> or fails with serialization error — better than lost update. Idempotency key unique index is another lock story.</p>
  <p><b>Trade-offs.</b> Serializable is safest, hottest under contention. Most Jira-shaped OLTP runs read committed + explicit row locks on contested rows.</p>
  <p><b>Interview.</b> “Board drag-and-drop reorder?” Transaction scope, lock ordering to avoid deadlocks, optimistic versioning with <code>version</code> column.</p>
  {callout("Mistake: holding a transaction open while calling Slack — connection pool exhaustion, not ‘distributed transactions.’")}
''', "topics")

    t_scale = topic("db-scale", "Replication, partitioning, sharding intro", "read replica lag partition shard tenant", "Database", f'''
  <p><b>Mental model.</b> Scale reads with replicas; scale writes with partitioning/sharding or architectural split. Replication is not backup — it is redundancy with lag.</p>
  <p><b>Technical.</b> Primary handles writes; read replicas apply WAL asynchronously. Read-your-writes: route session to primary after mutation, or tolerate lag on board refresh. Partition large tables by <code>tenant_id</code> hash or time (comments by month) for maintenance windows.</p>
  <p><b>Sharding intro.</b> Split tenants across Postgres clusters when single-primary write ceiling or storage cap hits. Router maps <code>tenant_id</code> → shard. Cross-shard joins are avoided — global search becomes a separate system.</p>
  <p><b>Production example.</b> Atlassian-scale: hot tenant on one shard dominates IOPS — isolate noisy neighbor to dedicated shard. Comment history partitioned by <code>created_at</code> makes archival detach cheap.</p>
  <p><b>Trade-offs.</b> Replicas fix read-heavy issue GETs; they do not fix write-heavy comment storms. Sharding is operability tax — don’t shard at 3k RPS.</p>
  <p><b>Interview.</b> “User posts comment, refresh doesn’t show it?” Replica lag vs cache vs read-after-write routing.</p>
''', "topics")

    return f'''
<section class="block" id="database" data-search="Database PostgreSQL schema indexes transactions MVCC" data-stype="Section" data-cat="database">
  <p class="kicker">Source of truth</p>
  <h2 class="section-title">Database Design</h2>
  <p class="lede">Postgres-shaped OLTP is the default backbone for issue trackers. Design for tenant isolation, measured indexes, and honest write paths before reaching for shards.</p>
  {t_model}
  {t_norm}
  {t_index}
  {t_tx}
  {t_scale}
</section>
'''


def sql() -> str:
    t_basics = topic("sql-basics", "SELECT, JOIN, aggregation", "SQL JOIN GROUP BY HAVING WHERE", "SQL", f'''
  <p><b>Mental model.</b> SQL is declarative: you describe the relation you want; the optimizer chooses how. Think in sets, not loops.</p>
  {code("sql", '''-- Issues with project key and comment count
SELECT p.key,
       i.issue_number,
       i.summary,
       i.status,
       COUNT(c.id) AS comment_count
FROM issues i
JOIN projects p
  ON p.id = i.project_id AND p.tenant_id = i.tenant_id
LEFT JOIN comments c
  ON c.issue_id = i.id AND c.tenant_id = i.tenant_id
WHERE i.tenant_id = $1
  AND p.key = 'PROJ'
GROUP BY p.key, i.issue_number, i.summary, i.status, i.id
HAVING COUNT(c.id) >= 5
ORDER BY comment_count DESC
LIMIT 20;''')}
  <p><b>Production example.</b> Always join on <code>tenant_id</code> as well as fk id — defense in depth against cross-tenant bugs if a stray UUID appears.</p>
  <p><b>Trade-offs.</b> <code>HAVING</code> filters after aggregation; put row filters in <code>WHERE</code> when possible so less data aggregates.</p>
  <p><b>Interview.</b> “Explain this query plan verbally.” Start from driving table, join order, aggregation, sort.</p>
''', "topics")

    t_advanced = topic("sql-advanced", "Subqueries, CTEs, window functions", "CTE window function ROW_NUMBER LATERAL", "SQL", f'''
  <p><b>Mental model.</b> CTEs clarify steps; window functions compute per-row analytics without collapsing rows like GROUP BY.</p>
  {code("sql", '''-- Latest comment per issue (Postgres DISTINCT ON)
SELECT DISTINCT ON (c.issue_id)
       c.issue_id, c.id, c.body, c.created_at
FROM comments c
WHERE c.tenant_id = $1
ORDER BY c.issue_id, c.created_at DESC, c.id DESC;

-- Same with window function
SELECT issue_id, id, body, created_at
FROM (
  SELECT c.*,
         ROW_NUMBER() OVER (
           PARTITION BY c.issue_id
           ORDER BY c.created_at DESC, c.id DESC
         ) AS rn
  FROM comments c
  WHERE c.tenant_id = $1
) t
WHERE rn = 1;''')}
  {code("sql", '''-- Running count of open issues per project by week
SELECT date_trunc('week', i.created_at) AS week,
       p.key,
       COUNT(*) FILTER (WHERE i.status != 'Done') AS open_issues
FROM issues i
JOIN projects p ON p.id = i.project_id AND p.tenant_id = i.tenant_id
WHERE i.tenant_id = $1
GROUP BY 1, 2
ORDER BY 1, 2;''')}
  <p><b>Production example.</b> Activity feed “last actor per issue” for 10k issues: window + index on <code>(tenant_id, issue_id, created_at DESC)</code> — not correlated subquery per row in app code.</p>
  <p><b>Trade-offs.</b> CTEs before Postgres 12 were optimization fences; modern planner can inline — still prefer readability when complex.</p>
''', "topics")

    t_explain = topic("sql-explain", "EXPLAIN and transactions in practice", "EXPLAIN ANALYZE transaction isolation", "SQL", f'''
  <p><b>Mental model.</b> EXPLAIN is the interview whiteboard for Postgres. Read top-to-bottom cost, actual rows vs estimated, and buffer hits.</p>
  {code("sql", '''EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT i.id, i.summary
FROM issues i
WHERE i.tenant_id = $1
  AND i.project_id = $2
  AND i.status = 'In Progress'
ORDER BY i.updated_at DESC
LIMIT 50;''')}
  <p>Look for: seq scan on large table, sort spilling to disk, nested loop with huge inner loops, bitmap heap scan with bad row estimates.</p>
  <p><b>Transactions.</b> Wrap multi-statement invariants (transition + history + watcher side effect queue row) in one transaction. Use savepoints only when you understand partial rollback semantics.</p>
  <p><b>Interview.</b> “How do you debug slow query in prod?” pg_stat_statements → EXPLAIN on representative params → index or rewrite → verify row counts.</p>
''', "topics")

    practices = [
        ("sql-p1", 1,
         "Why might a query be slow despite having an index?",
         "The index may not match the predicate (function wrap, wrong leading column, implicit cast), the planner may prefer seq scan due to high selectivity or stale statistics, the query may sort/limit in a way the index cannot satisfy, or the slowness is lock wait / IO bloat — not missing index. Always EXPLAIN (ANALYZE) with production-like parameters.",
         "Adding another index without reading EXPLAIN — you accumulate write overhead and still seq scan."),
        ("sql-p2", 2,
         "Latest record per user (e.g. most recent comment each author made)",
         "Use <code>DISTINCT ON (author_id) ... ORDER BY author_id, created_at DESC</code> in Postgres, or <code>ROW_NUMBER() OVER (PARTITION BY author_id ORDER BY created_at DESC)</code> in a subquery filtered to rn=1. Index <code>(tenant_id, author_id, created_at DESC)</code>. Avoid correlated subqueries per author in application loops.",
         "Grouping without tie-breaker id — two comments same timestamp return arbitrary row."),
        ("sql-p3", 3,
         "Paginate millions of rows without OFFSET death",
         "Keyset pagination: <code>WHERE (updated_at, id) &lt; ($cursor_updated, $cursor_id) ORDER BY updated_at DESC, id DESC LIMIT 50</code>. Index must match sort order. O(page size) per page; OFFSET is O(offset).",
         "Using OFFSET 500000 for ‘infinite scroll’ — each page scans half a million rows."),
        ("sql-p4", 4,
         "N+1 and join fan-out in SQL",
         "N+1 is an app pattern: loop issues, query assignee each time — fix with JOIN or batch IN query. Join fanout is SQL: joining issues → comments duplicates issue columns per comment; use aggregation, subquery, or lateral join for comment counts instead of joining all comments when you only need counts.",
         "LEFT JOIN comments then DISTINCT issue id — dedup after explosion instead of preventing explosion."),
        ("sql-p5", 5,
         "Find issues with no comments (anti-join)",
         "<code>SELECT i.* FROM issues i LEFT JOIN comments c ON c.issue_id = i.id AND c.tenant_id = i.tenant_id WHERE i.tenant_id = $1 AND c.id IS NULL</code>. Or <code>NOT EXISTS (SELECT 1 FROM comments c WHERE ...)</code> — often clearer to humans and planner alike.",
         "COUNT(c.id) = 0 with LEFT JOIN without GROUP BY — wrong semantics on multiple joins."),
        ("sql-p6", 6,
         "Detect duplicate watchers inserted under race",
         "Primary key on <code>(tenant_id, issue_id, user_id)</code> makes second insert fail with unique violation — catch and treat as success for idempotent watch. In interview, mention INSERT ... ON CONFLICT DO NOTHING.",
         "SELECT then INSERT in app without unique constraint — race creates duplicates."),
        ("sql-p7", 7,
         "Top 3 projects by open issue count per tenant",
         "Window rank: <code>RANK() OVER (PARTITION BY tenant_id ORDER BY open_count DESC)</code> in a CTE, filter rank &lt;= 3. Or aggregate first then join — avoid counting in window over raw issues twice if expensive.",
         "LIMIT 3 globally instead of per tenant — answers wrong question."),
        ("sql-p8", 8,
         "Issue transition audit: show status duration",
         "Lead/lag window on history table: <code>LEAD(changed_at) OVER (PARTITION BY issue_id ORDER BY changed_at) - changed_at AS duration</code>. Requires immutable history rows, not overwriting status.",
         "Storing only current status — cannot answer ‘how long in QA’ without event log."),
        ("sql-p9", 9,
         "When would you refuse to solve this in SQL?",
         "Full-text relevance ranking across shards, graph traversal (‘all downstream linked issues’), or ML scoring — push to search/graph service. SQL for set operations on owned data; not every hammer is JOIN.",
         "Recursive CTE ten levels deep on production OLTP without index support — kills primary."),
    ]

    practice_html = "".join(_sql_practice(qid, n, prompt, ans, mis) for qid, n, prompt, ans, mis in practices)

    return f'''
<section class="block" id="sql" data-search="SQL JOIN CTE window functions EXPLAIN interview" data-stype="Section" data-cat="database">
  <p class="kicker">Queries</p>
  <h2 class="section-title">SQL Deep Dive</h2>
  <p class="lede">Senior SQL is reading plans, choosing set operations, and knowing when to stop pushing logic into one query. Work the practice items before revealing.</p>
  {t_basics}
  {t_advanced}
  {t_explain}
  <h3 class="subsection-title">Interview practice — SQL</h3>
  {practice_html}
</section>
'''


def nosql() -> str:
    t_types = topic("nosql-types", "Four NoSQL families — when each fits", "KV document column graph NoSQL", "NoSQL", f'''
  <p><b>Mental model.</b> NoSQL is not “SQL but faster.” It is a bet that you know your access patterns upfront and can trade relational flexibility for scale or shape.</p>
  <table>
    <tr><th>Store</th><th>Shape</th><th>Good fit</th><th>Weak fit</th></tr>
    <tr><td>Key-value</td><td>opaque blob by key</td><td>Sessions, rate counters, feature flags</td><td>Ad hoc joins across entities</td></tr>
    <tr><td>Document</td><td>JSON docs</td><td>Content pages, flexible metadata, nested configs</td><td>Multi-doc ACID across aggregates (unless explicitly supported)</td></tr>
    <tr><td>Column-family</td><td>wide rows, sorted columns</td><td>Time-series, write-heavy feeds, TTL’d events</td><td>Complex relational reporting in one query</td></tr>
    <tr><td>Graph</td><td>nodes + edges</td><td>Permission inheritance, linked issues, org hierarchy</td><td>Bulk analytics on entire graph nightly</td></tr>
  </table>
  <p><b>Production example.</b> Confluence page body + metadata in document store; permissions edges in graph or relational ACL tables; issue search in OpenSearch — one product, multiple stores by access pattern.</p>
  <p><b>Trade-offs.</b> Pick the store after listing read/write paths and consistency needs — not the logo on a blog post.</p>
  <p><b>Interview.</b> “SQL vs Mongo for issues?” If you need cross-issue transactions and arbitrary reporting, Postgres unless you can name the document boundary.</p>
''', "topics")

    t_dynamo = topic("nosql-dynamo", "DynamoDB-style — partition key, sort key, GSI", "DynamoDB partition sort GSI hot partition", "NoSQL", f'''
  <p><b>Mental model.</b> Single-table design: one item collection, multiple access patterns via primary key + GSIs. Throughput is provisioned per partition — hot keys are a physical limit.</p>
  {code("json", '''// Primary: all comments on an issue (thread read)
{
  "PK": "TENANT#acme#ISSUE#PROJ-42",
  "SK": "COMMENT#2025-08-26T10:00:00Z#124",
  "body": "Ship it",
  "authorId": "user-9"
}

// GSI1: comments by author (activity feed)
{
  "GSI1PK": "TENANT#acme#AUTHOR#user-9",
  "GSI1SK": "2025-08-26T10:00:00Z#124",
  ...
}''')}
  <p><b>Technical.</b> Partition key spreads load; sort key orders within partition. GSI is eventually consistent replica of alternate key — duplicate write amplification. Conditional writes for optimistic locking.</p>
  <p><b>Hot partitions.</b> All tenants’ global counters on PK <code>COUNTER#global</code> → throttling. Mitigate: shuffle suffixes, per-tenant counters, or accept approximate counts.</p>
  <p><b>Production example.</b> Trello card moves: PK = board id, SK = list position — high write rate on one popular board still one partition; split boards or use transact writes sparingly.</p>
  <p><b>Trade-offs.</b> Excellent for known key lookups at scale; painful for ad hoc analytics — export to warehouse instead of pretending GSIs are SQL.</p>
  <p><b>Interview.</b> “Design comment thread + author feed.” Draw PK/SK and one GSI; say what query is impossible without another index.</p>
  {callout("Mistake: scanning partitions — Dynamo bills rage and latency spikes; it means wrong key design.")}
''', "topics")

    t_mongo = topic("nosql-mongo", "MongoDB-style — documents and boundaries", "MongoDB document embed reference schema", "NoSQL", f'''
  <p><b>Mental model.</b> Documents group data that is read and written together. Embed when 1:few and bounded; reference when unbounded or shared (users, labels).</p>
  {code("json", '''{
  "_id": "PROJ-42",
  "tenantId": "acme",
  "summary": "Login fails on Safari",
  "status": "In Progress",
  "watchers": ["user-1", "user-2"],
  "recentComments": [
    { "id": "124", "authorId": "user-9", "body": "Repro steps added" }
  ]
}''')}
  <p><b>Production example.</b> Embed last 5 comments for issue detail fast path; full history in separate collection for pagination. Unbounded embed → document size limit and write contention on single doc.</p>
  <p><b>Trade-offs.</b> Multi-document transactions exist but are not free — default happy path is single-document atomicity.</p>
  <p><b>Interview.</b> “Where would Mongo hurt for Jira?” Cross-project reporting, strict FK integrity, complex permission joins — relational or search wins.</p>
''', "topics")

    t_cassandra = topic("nosql-cassandra", "Cassandra-style — write-optimized wide rows", "Cassandra column family tunable consistency", "NoSQL", f'''
  <p><b>Mental model.</b> Partition key determines node; clustering columns sort within partition. Query patterns must include partition key — there is no free secondary filter.</p>
  {code("sql", '''-- CQL-ish: issue activity timeline (write-heavy)
CREATE TABLE issue_activity (
  tenant_id text,
  issue_id text,
  event_time timestamp,
  event_id uuid,
  event_type text,
  payload text,
  PRIMARY KEY ((tenant_id, issue_id), event_time, event_id)
) WITH CLUSTERING ORDER BY (event_time DESC);''')}
  <p><b>Production example.</b> Audit/event log append, notification outbox per tenant, metrics — not primary issue OLTP unless team accepts query rigidity.</p>
  <p><b>Eventual consistency.</b> Tunable per read (<code>QUORUM</code>, <code>LOCAL_QUORUM</code>). Say what stale read means for the UX (“activity feed may lag 1s”).</p>
  <p><b>Trade-offs.</b> Massive write throughput and multi-region; you design tables per query upfront — altering access pattern ≈ new table + backfill.</p>
''', "topics")

    t_when = topic("nosql-refuse", "Access-pattern modeling and when to refuse NoSQL", "eventual consistency refuse NoSQL access pattern", "NoSQL", f'''
  <p><b>Mental model.</b> Start from workflows: list issues by project, get issue by key, add comment, search full text. Each gets a primary store; caches and indexes are derived.</p>
  <p><b>When to refuse NoSQL in an interview.</b></p>
  <ul>
    <li>Core money/issue state needs cross-row ACID and you cannot articulate aggregate boundaries.</li>
    <li>Reporting is ad hoc and drives the business — warehouse + SQL, not document scans.</li>
    <li>Team lacks operability for eventual consistency debugging (ghost reads, dual writes).</li>
    <li>You chose NoSQL to avoid schema design — that schema still exists, just implicit in keys.</li>
  </ul>
  <p><b>Production example.</b> Issue transition with watchers + automation webhooks: relational transaction on issue + outbox row; search index updates async — eventual search is OK, wrong status is not.</p>
  <p><b>Trade-offs.</b> Polyglot persistence adds sync jobs and drift. One Postgres plus Redis plus search is already three systems — add Dynamo only for a proven hot path.</p>
  <p><b>Interview.</b> “Everything in Dynamo?” Push back: name the transaction, the report, and the query you cannot express — senior candidates defend relational source of truth.</p>
  {callout("Mistake: ‘use Kafka because scalable’ without a consumer story — same as ‘use NoSQL because web scale’ without access patterns.", "warn")}
''', "topics")

    return f'''
<section class="block" id="nosql" data-search="NoSQL DynamoDB MongoDB Cassandra graph KV" data-stype="Section" data-cat="database">
  <p class="kicker">Access patterns first</p>
  <h2 class="section-title">NoSQL</h2>
  <p class="lede">NoSQL stores are specialized tools. Model keys from queries, measure hot partitions, and keep issue-shaped source of truth where transactions matter.</p>
  {t_types}
  {t_dynamo}
  {t_mongo}
  {t_cassandra}
  {t_when}
</section>
'''
