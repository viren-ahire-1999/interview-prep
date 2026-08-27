from util import topic, diagram, callout, code, esc


def _case(
    cid,
    title,
    search,
    problem,
    fr,
    nfr,
    clarifying,
    scale,
    api,
    data_model,
    arch_diagram,
    deep_dive,
    caching,
    queues,
    database,
    consistency,
    failures,
    security,
    observability,
    scaling,
    bottlenecks,
    tradeoffs,
    followups,
    answer_structure,
):
    return topic(
        cid,
        title,
        search,
        "Case study",
        f"""
  <p class="stat-sub">Practice exercise (45 min). Not an official Atlassian interview question.</p>
  <h4>Problem</h4>
  <p>{problem}</p>
  <h4>Functional requirements</h4>
  <p>{fr}</p>
  <h4>Non-functional requirements</h4>
  <p>{nfr}</p>
  <h4>Clarifying questions</h4>
  <p>{clarifying}</p>
  <h4>Scale estimates</h4>
  <p>{scale}</p>
  <h4>API design</h4>
  <p>{api}</p>
  <h4>Data model</h4>
  <p>{data_model}</p>
  <h4>High-level architecture</h4>
  {diagram(arch_diagram)}
  <h4>Component deep dive</h4>
  <p>{deep_dive}</p>
  <h4>Caching</h4>
  <p>{caching}</p>
  <h4>Queues &amp; async</h4>
  <p>{queues}</p>
  <h4>Database</h4>
  <p>{database}</p>
  <h4>Consistency</h4>
  <p>{consistency}</p>
  <h4>Failure scenarios</h4>
  <p>{failures}</p>
  <h4>Security</h4>
  <p>{security}</p>
  <h4>Observability</h4>
  <p>{observability}</p>
  <h4>Scaling strategy</h4>
  <p>{scaling}</p>
  <h4>Bottlenecks at 10×</h4>
  <p>{bottlenecks}</p>
  <h4>Trade-offs</h4>
  <p>{tradeoffs}</p>
  <h4>Follow-ups</h4>
  <p>{followups}</p>
  <h4>Ideal 45-minute answer structure</h4>
  <p>{answer_structure}</p>
""",
        "cases",
    )


def _jira():
    return _case(
        "cs-jira",
        "Design Jira",
        "Jira issue tracker board workflow permissions multi-tenant search notifications audit",
        "Design a multi-tenant issue tracking system: projects, issues, workflows, boards, comments, attachments, search, notifications, and audit. Users collaborate in real time on boards; admins configure permissions and workflows per project.",
        "Create/read/update issues; workflow transitions with guards; Kanban/Scrum boards; JQL-style search; comments and @mentions; watchers; file attachments; project/space permissions (roles); webhooks and REST API; plugin extension points (out of hot path).",
        "p99 &lt; 300ms for issue view and transition (writer); 99.9% availability for read path; tenant isolation (no cross-tenant data leak); search index lag &lt; 30s; notifications delivered within 60s; audit log durable and queryable for 7 years; board updates visible to collaborators within 2s (eventual OK for non-editors).",
        "Multi-tenant SaaS or single org? Real-time board mandatory or poll OK? JQL full grammar or subset? Plugins in scope? Mobile offline? Compliance (SOC2, data residency)? Expected largest tenant size?",
        "Assume 500k tenants, 5M DAU, 80 req/user/day → 400M req/day → ~4,600 avg RPS, peak ~14k RPS (3×). Read/write 15:1 → ~900 WPS peak. Issues: 2B total, 50M active; avg issue row 4 KB metadata + 20 KB comments over life. New issues 500k/day. Attachments 200k/day × 2 MB avg → 400 GB/day to object store. Search: 10% of reads → 1.4k search RPS peak.",
        """REST resources: <code>POST /projects</code>, <code>POST /issues</code>, <code>GET /issues/{{id}}</code>, <code>PATCH /issues/{{id}}</code> with <code>If-Match: version</code>, <code>POST /issues/{{id}}/transitions</code> with idempotency-key header, <code>GET /boards/{{id}}/snapshot</code>, <code>GET /search?jql=...</code> cursor pagination. WebSocket <code>/live/board/{{id}}</code> for card moves. Errors: 409 on version conflict, 403 on permission, 422 on invalid transition.""",
        "Core OLTP (Postgres): <code>tenants</code>, <code>projects</code>, <code>issues</code> (tenant_id, project_id, status, version, rank), <code>transitions</code>, <code>comments</code>, <code>permissions</code> (subject, resource, action), <code>watchers</code>. Denormalize <code>issue_search_doc</code> for index pipeline. Attachments metadata in DB, blobs in S3. Audit: append-only <code>audit_events</code> (tenant_id, actor, action, entity, payload_hash, ts).",
        """Client → CDN (static) / API Gateway (auth, rate limit)
  → Issue Service (modular monolith or core domain)
  → Postgres primary (writes) + replicas (reads)
  → Redis (session, board snapshot cache, idempotency)
  → Kafka: issue.events → Search indexer, Notification worker, Audit sink, Webhook dispatcher
  → Elasticsearch (search) / OpenSearch
  → S3 (attachments)
  → WS fan-out service (board presence + moves)""",
        "<b>Transition engine.</b> Validate permission + workflow guard in one DB transaction: read issue version, check allowed transition, update status/rank, insert transition row, emit outbox event. Never call email synchronously. <b>Multi-tenancy.</b> Every table carries <code>tenant_id</code>; connection pool sets <code>SET app.tenant_id</code> or ORM scoping; cross-tenant queries impossible at API layer; largest tenants may get dedicated shard or noisy-neighbor rate limits. <b>Permissions.</b> RBAC (project roles) + issue security levels + optional object-level grants; evaluated server-side on every API — never trust UI hide alone; cache decisions per (user, project) TTL 120s, bust on role change event. <b>Search.</b> Async index of summary, description, comments; query ES then filter by permission bitmap or store allowed_principals[] in doc with periodic reconcile job. <b>Notifications.</b> Transition emits <code>issue.assigned</code> etc. to Kafka; fan-out to watchers async; respect user channel prefs and digest. <b>Audit.</b> Append-only <code>audit_events</code>: actor, IP, action, before/after hash, immutable; stream to SIEM; 7-year retention with monthly partitions.",
        "Redis: issue detail (TTL 60s, invalidate on write); board snapshot (TTL 30s, key=board_id+filter_hash); permission bitmap cache (TTL 120s). CDN: static assets immutable; attachment downloads via signed URL. Cache-aside for issue GET; stampede protection via singleflight on hot keys.",
        "Kafka topic <code>issue.events</code> partitioned by <code>issue_id</code> (ordering per issue). Consumers: search indexer (at-least-once, idempotent upsert by issue_id+version), notification (fan-out to watchers queue), audit (append), webhooks (retry + DLQ). Outbox pattern from Issue Service ensures no lost events if crash after commit.",
        "Postgres primary for OLTP; read replicas for issue GET and board load. Partition <code>audit_events</code> by month. Consider sharding by <code>tenant_id</code> when single primary exceeds ~10k WPS — cross-tenant queries (admin) go to federated layer. Connection pooling (PgBouncer) mandatory at scale.",
        "Issue transition: strong consistency + RYW for actor (return new state in PATCH). Board for other users: eventual (WS or 2s poll). Search: eventual bounded 30s. Notifications: eventual. Permissions: read from primary on write path; cache on read with invalidation on grant/revoke.",
        "Postgres primary down → fail writes, serve stale reads from replica with banner. Redis down → bypass cache, higher latency. Kafka lag → search stale, notifications delayed — alert on consumer lag. WS node loss → client reconnect + catch-up REST. Duplicate transition → idempotency key prevents double apply.",
        "Tenant_id on every query; row-level security in Postgres optional defense-in-depth. OAuth/API tokens scoped per tenant. Encrypt attachments at rest; TLS everywhere. Audit all permission changes, issue deletes, admin impersonation with actor + target. Plugin iframe sandbox + CSP. Rate limit per tenant API key. SOC2: logical separation, encryption keys per tenant tier optional.",
        "SLI: issue view p99, transition success rate, search lag, notification delivery time. Trace id from gateway through outbox to consumers. Metrics: RPS per tenant (hot tenant detection), Kafka lag, cache hit rate, WS connections. SLO dashboards per tenant tier.",
        "Horizontal stateless API pods; scale WS separately. Read replicas for GET; scale Kafka consumers with lag. ES data nodes for search. Multi-AZ; active-passive DR for Postgres with RPO 5 min. Largest tenant → dedicated shard or rate limit tier.",
        "Hot tenant on one shard; permission check N+1 on board load; WS fan-out for 500 users on one board; JQL on OLTP without index; outbox table write amplification; attachment egress costs.",
        "Modular monolith vs microservices early (monolith + async extract search). Eventual search vs synchronous index (async wins). OT vs last-write for description (version + 409). Real-time WS vs SSE vs poll (WS for board, poll for low-collab).",
        "Workflow DSL design; custom fields schema; marketplace plugin isolation; data export GDPR; cross-project boards; mobile sync.",
        "0–5 min: clarify tenant scale, real-time, search scope. 5–12 min: numbers + APIs. 12–20 min: diagram + data model. 20–35 min: deep dive transition + permissions + search/async. 35–42 min: failures + security + audit. 42–45 min: trade-offs + evolution.",
    )


def _confluence():
    return _case(
        "cs-conf",
        "Design Confluence",
        "Confluence wiki pages spaces editor permissions search macros audit multi-tenant",
        "Design a collaborative documentation platform: hierarchical spaces and pages, rich-text editor, version history, inline comments, permissions at space/page level, full-text search, macros, and audit trail.",
        "Spaces and page tree; create/edit/publish pages; version history and diff; concurrent editing with conflict detection; comments and @mentions; page-level and space-level permissions; templates; attachments; search within tenant; macro execution (tables, Jira embed); export PDF/HTML.",
        "Page read LCP &lt; 2s for 200 KB body; save p99 &lt; 500ms; 99.95% read availability; conflict surfaced within one round-trip; search lag &lt; 60s; tenant isolation; audit immutable 7 years; macro sandbox must not XSS the host.",
        "Real-time co-editing (Google Docs) or lock/merge? Max page size? Public anonymous spaces? Data residency? Confluence Cloud vs Server scale?",
        "200k tenants, 2M DAU, 60 page views/user/day → 120M views/day → ~1,400 avg RPS, peak ~4,200 RPS. Writes 5% → ~210 WPS peak. 500M pages total; avg published body 150 KB (stored compressed). Versions: 3 versions/page avg retained hot, archive cold. Search 15% of reads → ~630 search RPS peak. Attachments 50k/day × 5 MB.",
        """<code>GET /spaces/{{id}}/pages?parent=</code> paginated tree; <code>GET /pages/{{id}}?version=</code>; <code>PUT /pages/{{id}}</code> with <code>If-Match: version</code> and body format (ADF/ProseMirror JSON); <code>POST /pages/{{id}}/comments</code>; <code>GET /search?q=</code> cursor; <code>POST /pages/{{id}}/publish</code>. WebSocket optional for presence and live cursors.""",
        "<code>spaces</code>, <code>pages</code> (id, space_id, tenant_id, parent_id, title, status draft/published, current_version), <code>page_versions</code> (immutable blob storage pointer + diff metadata), <code>permissions</code> (inheritance from space), <code>comments</code> anchored to version, <code>macros</code> registry. Body in object store or compressed JSON column under 256 KB inline.",
        """Client → API Gateway → Page Service
  → Postgres (metadata, permissions, tree)
  → Object store (large page bodies, version blobs)
  → Redis (published page cache, permission cache)
  → Kafka page.events → Search indexer, Notification, Audit
  → Elasticsearch (content + titles)
  → Macro render service (isolated)""",
        "<b>Versioning.</b> Each save creates new version row; publish updates pointer. Conflict: If-Match fails → 409 with server version for merge UI. <b>Multi-tenancy.</b> Spaces belong to tenant; storage quotas per tenant; admin APIs cannot list cross-tenant even with SQL bug if middleware enforces tenant context. <b>Tree nav.</b> Materialized path or adjacency list; paginate children; never load 100k nodes at once. <b>Permissions inheritance.</b> Space ACL → page overrides; resolve effective ACL walking ancestors; cache per (user, page_id); bust on grant/revoke via Kafka event. <b>Search.</b> Index published body + titles only; strip macro noise; permission filter at query time using user's space membership set; reindex job on bulk permission change. <b>Notifications.</b> @mention in comment → async email/in-app; page publish → notify watchers. <b>Audit.</b> Log view/export/delete/permission change with page version id; compliance hold prevents purge.",
        "Published page cache key=page_id+version, TTL 5 min, purge on publish. Tree children cache per parent, short TTL. CDN for anonymous public spaces only. Editor draft never cached as published.",
        "page.events → search (upsert doc), notifications (@mention), audit, link checker async. Heavy export PDF jobs on separate queue with worker pool.",
        "Postgres for metadata and ACL; S3 for version blobs. Read replicas for page GET. Archive old versions to cold storage after N months. Full-text in ES not Postgres at scale.",
        "Published read: eventual OK via cache (seconds). Author after save: RYW via response body. Co-edit: causal or operational transform if in scope — otherwise optimistic locking with 409. Search eventual 60s.",
        "Save during partition → 409 or queue draft locally (client). ES down → search degraded, reads OK. Macro service timeout → render placeholder, not fail whole page. Blob store slow → stream body with timeout.",
        "XSS: sanitize stored HTML/ADF; macro iframe sandbox. Tenant isolation on every query. Encrypt blobs at rest. Audit page delete and permission change. CSP strict on viewer.",
        "Save latency, conflict rate, publish rate, search lag, macro error rate. Trace page_id through save and index pipeline.",
        "Scale read path with replicas + cache; ES scale independently; export workers auto-scale on queue depth. Multi-region read replicas for APAC/EU.",
        "Large page hydration; permission inheritance on deep trees; reindex storm on bulk import; hot space with 50k pages; macro CPU on render path.",
        "CRDT/OT vs lock vs last-write-wins (senior: pick by co-edit requirement). Blob vs inline body threshold. ES vs Postgres FTS for permission-heavy search.",
        "Real-time co-editing; whiteboards; analytics on page views; migration from Server; nested macro marketplace.",
        "Clarify co-edit scope first. Numbers + read-heavy ratio. Draw read vs write path. Deep dive versioning + permissions + search async. Security XSS/macros. Audit and compliance close.",
    )


def _trello():
    return _case(
        "cs-trello",
        "Design Trello",
        "Trello board cards lists drag drop realtime permissions notifications",
        "Design a lightweight kanban product: boards, lists, cards, drag-and-drop ordering, members, labels, checklists, attachments, activity feed, and real-time sync across clients.",
        "Boards with lists and ordered cards; CRUD cards; drag reorder within/between lists; members and board roles; labels, due dates, checklists; card comments and attachments; activity log; invite links; notifications on assignment and mentions; mobile + web.",
        "Drag reorder acknowledged &lt; 200ms p99; real-time update to other clients &lt; 2s; 99.9% availability; offline mobile queue replay; tenant/user isolation; activity feed consistent with card state within 5s.",
        "Personal vs team boards? Max cards per board? Guest access? Real-time mandatory? Compare to Jira complexity (no workflow engine)?",
        "50M MAU, 8M DAU, 120 actions/user/day → 960M actions/day → ~11k avg RPS, peak ~33k RPS. Writes ~30% (more mutating than Jira reads) → ~10k WPS peak. 400M boards, avg 40 cards/board. Card row ~2 KB. Activity events 960M/day → Kafka retention 7 days hot.",
        """<code>GET /boards/{{id}}</code> full snapshot or <code>?fields=minimal</code>; <code>PATCH /cards/{{id}}</code> position/list_id with idempotency-key; <code>POST /cards/{{id}}/move</code> body {{listId, beforeCardId}}; WebSocket <code>/boards/{{id}}/events</code>; <code>GET /boards/{{id}}/actions?cursor=</code>.""",
        "<code>boards</code>, <code>lists</code> (board_id, position float or lexorank string), <code>cards</code>, <code>memberships</code>, <code>labels</code>, <code>checklists</code>, <code>actions</code> (activity feed). Position: lexicographic rank keys to avoid mass renumber on insert.",
        """Clients → API + WS Gateway
  → Board Service
  → Postgres (board snapshot source of truth)
  → Redis (board snapshot cache, presence, rate limits)
  → Kafka board.events → Activity projector, Notification, Search (optional)
  → S3 attachments
  → WS fan-out cluster""",
        "<b>Card move.</b> Transaction: update card list_id + rank between neighbors; emit event with board revision. Optimistic UI with revision check; 409 if stale. <b>Multi-tenancy.</b> Workspaces (orgs) own boards; free vs paid tier quotas on board/card counts; API keys scoped to workspace. <b>Realtime.</b> WS channel per board; event = type + cardId + revision; client applies delta. On reconnect, GET snapshot with <code>sinceRevision</code>. <b>Permissions.</b> Board roles admin/member/observer; guest link tokens read-only or comment; server enforces on every PATCH. <b>Search.</b> Optional ES index of card titles/descriptions filtered by board membership. <b>Notifications.</b> Assignment, due date, mention → Kafka → email/push with user prefs. <b>Audit.</b> Activity log per board (who moved what when); enterprise export to SIEM.",
        "Board snapshot in Redis (TTL 60s, invalidate on any board write). Card detail cache optional. No CDN for private board JSON.",
        "board.events partitioned by board_id for ordering. Notification worker for mentions/assignments. Activity feed projector builds per-board timeline idempotently.",
        "Postgres sufficient for OLTP at stated scale with read replicas. board_id shard key if needed. actions table partitioned by time.",
        "Move: RYW for mover via PATCH response. Other clients: eventual via WS (~1s). Activity feed: eventual projection. No cross-board transactions.",
        "WS disconnect → poll snapshot. Split-brain rank → periodic rebalancer job for rank key exhaustion. Duplicate move → idempotency. Hot board 200 users → single partition + fan-out service scale.",
        "Board invite tokens hashed; role checks server-side; attachment signed URLs; rate limit card creation anti-abuse.",
        "Move latency p99, WS delivery lag, reconnect rate, 409 conflict rate. Dashboard per board_id event rate for hot boards.",
        "Scale WS nodes horizontally; sticky by board_id to consistent hash ring. API stateless. Read replicas for snapshot GET.",
        "Hot board WS fan-out; rank key fragmentation; large board 10k cards snapshot size; activity table write volume.",
        "Float position vs lexorank (lexorank for fewer row updates). Full snapshot vs delta sync (hybrid: snapshot + incremental events). Event sourcing vs CRUD with outbox.",
        "Power-ups/plugins; calendar view; enterprise SSO; board templates; cross-board automation.",
        "Scope simpler than Jira — emphasize realtime move + ordering algorithm. Numbers. API + WS. Deep dive move transaction + lexorank + fan-out. Failures reconnect. Trade-offs vs Jira.",
    )


def _slack():
    return _case(
        "cs-slack",
        "Design Slack",
        "Slack chat channels messages threads search realtime presence notifications",
        "Design a team messaging platform: workspaces, channels (public/private/DM), threaded messages, file sharing, search, presence, and push notifications.",
        "Send/receive messages in channels and DMs; threads; edit/delete with retention policy; file uploads; emoji reactions; @mentions and @channel; full-text search; unread counts; presence (active/away); mobile push; bots/webhooks.",
        "Message send ack &lt; 200ms p99; delivery to online clients &lt; 1s; 99.99% message durability once acked; search lag &lt; 2 min; support 500k concurrent WS per region; E2E optional enterprise tier.",
        "Max message size? Retention forever or configurable? Federation across companies? End-to-end encryption in scope?",
        "100M DAU, 50 msgs/user/day → 5B msgs/day → ~58k avg ingest RPS, peak ~175k RPS. Avg message 500 bytes text + 10% with 1 MB file. Storage 2.5 TB/day text + 500 TB/day files (dedupe reduces). WS: 10M concurrent connections globally.",
        """<code>POST /channels/{{id}}/messages</code> returns message id immediately; <code>GET /channels/{{id}}/history?cursor=</code>; <code>GET /search?q=</code>; WebSocket events: message, reaction, presence. Upload: <code>POST /files/uploadUrl</code> then PUT to object store.""",
        "<code>workspaces</code>, <code>channels</code>, <code>messages</code> (channel_id, ts as sort key, thread_ts), <code>memberships</code>, <code>reactions</code>, <code>files</code>. Messages sharded by (workspace_id, channel_id); ts = unique per channel (snowflake or ULID).",
        """Clients → WS Gateway (long-lived) + REST API
  → Message Service (accept → persist → fan-out)
  → Cassandra/Dynamo (messages by channel+ts)
  → Redis (presence, unread counters, recent cache)
  → Kafka message.events → Search indexer, Push, Analytics
  → Elasticsearch search
  → S3 files
  → Notification/Push service""",
        "<b>Write path.</b> Assign ts, write to channel partition, ack client, async fan-out to WS subscribers and push for offline users. <b>Read path.</b> History paginated backwards by cursor (ts). <b>Search.</b> Async index; permission filter by channel membership inverted index. <b>Presence.</b> Heartbeat to Redis set with TTL; pub/sub for friend graph optional.",
        "Recent 100 messages per channel in Redis. User unread counts in Redis HASH. No cache of full history.",
        "Kafka for fan-out to search, push, bots, compliance export. Partition by channel_id for ordering within channel.",
        "Wide-column store for messages (write-heavy, time-range queries). Postgres for workspace metadata. ES for search. Hot channels may need dedicated partition.",
        "Per-channel ordering guaranteed. Cross-channel eventual. User sees own message on ack (RYW). Search eventual.",
        "WS node crash → client reconnect other node, backfill via REST. Kafka consumer lag → search stale. Push provider down → queue retries, in-app still works.",
        "Workspace isolation; private channel ACL on every read; signed file URLs; audit enterprise; rate limit @channel; token scopes for bots.",
        "Message ingest p99, WS fan-out lag, push success rate, search lag, connection count per WS pod.",
        "Shard messages by workspace; WS horizontal scale with connection draining; regional clusters; cross-region async replication for DR.",
        "Celebrity channel hot partition; @channel fan-out to 100k users; search index size; WS memory per connection.",
        "Cassandra vs Dynamo vs sharded Postgres. Pull vs push fan-out (push for active, poll for catch-up). Store messages vs event log retention.",
        "Huddles/video; workflow automation; Slack Connect shared channels; compliance eDiscovery.",
        "Clarify retention and E2E. Numbers on messages/sec. Draw write→persist→fan-out. Deep dive sharding + WS. Search async. Failures and hot channel.",
    )


def _url():
    return _case(
        "cs-url",
        "URL shortener",
        "URL shortener redirect hash collision analytics rate limit",
        "Design a service that maps short URLs to long URLs with high read volume, optional custom aliases, analytics, and expiration.",
        "Shorten URL; redirect HTTP 301/302; custom slug optional; expiration TTL; click analytics (count, geo, referrer); admin delete; API for bulk create.",
        "Redirect p99 &lt; 50ms; 99.99% redirect availability; no broken links if target was valid at create time; slug collision handled; 100:1 read/write ratio.",
        "Custom domains? Private vs public short links? Edit long URL after create? Analytics real-time or batch?",
        "100M shortened URLs total; 10M DAU creators; 1B redirects/day → ~11.6k avg RPS, peak ~50k RPS (reads spike). Writes 10M/day → ~115 WPS. Slug 7 chars base62 ≈ 3.5T space. Metadata 500 bytes/URL.",
        """<code>POST /urls</code> body {{longUrl, customSlug?, ttl?}} → {{shortUrl, id}}; <code>GET /{{slug}}</code> → 302 Location; <code>GET /urls/{{id}}/stats</code>; idempotency on create with same longUrl+user.""",
        "<code>urls</code> (id, slug UNIQUE, long_url_hash, long_url, user_id, expires_at, created_at). Analytics: <code>clicks</code> aggregate rollups per hour or stream to warehouse.",
        """Client → CDN edge (cache 302?) → Redirect Service
  → Redis (slug → long_url hot cache)
  → Postgres/Dynamo (slug PK lookup)
  → Kafka click.events → Analytics aggregator
  → Optional separate read replicas""",
        "<b>Slug generation.</b> Base62 counter (Snowflake) or hash long URL + truncate with collision retry. Custom slug: transactional UNIQUE check. <b>Redirect.</b> Cache-aside Redis; on miss DB lookup; if expired return 410. <b>Analytics.</b> Async fire-and-forget click event — never block redirect.",
        "Redis slug→target, TTL min(expires, 24h). 301 vs 302: 302 allows analytics hit each time; 301 browsers cache — pick consciously.",
        "click.events to Kafka → Flink/Spark rollups or Redis INCR per url_id hourly.",
        "DynamoDB slug as PK ideal for point reads at scale. Postgres OK until ~10k RPS with cache. Separate analytics store.",
        "Redirect read: eventual cache OK. Create: strong unique on slug. Analytics: eventual.",
        "Cache stampede on viral link → singleflight + prewarm. DB miss on expired slug → 410 not 500. Kafka down → drop analytics sample, redirect still works.",
        "Rate limit create per IP; block malicious targets (phishing scan); don't expose internal URLs; slug enumeration hard with random slugs.",
        "Redirect p99, cache hit rate, create error rate, click pipeline lag.",
        "Scale redirect tier horizontally stateless; Redis cluster; multi-region read replicas; CDN cache 302 only if acceptable.",
        "Viral hot key in Redis; custom slug squatting; analytics volume >> redirect if logging too much per click.",
        "Hash vs counter slug (counter predictable but simple). 301 vs 302. Sync analytics vs async (async always on redirect path).",
        "QR codes; A/B link rotation; branded domains per tenant; link preview scraping.",
        "Classic intro problem: 5 min clarify, 5 min math (100:1 reads), 10 min API+DB+redirect path, 10 min cache+analytics queue, 5 min hot key + trade-offs.",
    )


def _twitter():
    return _case(
        "cs-twitter",
        "Twitter / X feed",
        "Twitter feed timeline fan-out celebrity problem home timeline",
        "Design a social feed: post tweets, follow users, home timeline, likes/retweets, trending, and media attachments.",
        "Post tweet (text/media); follow/unfollow; home timeline (followees' tweets reverse chrono); user profile timeline; like/retweet; reply threads; @mentions; search users/tweets; notifications.",
        "Timeline load p99 &lt; 500ms; post ack &lt; 300ms; 99.9% availability; celebrity users with 50M followers must not break write path; media served via CDN.",
        "Strict chronological or ranked feed? Retweet semantics? Delete propagation? Verified-only features?",
        "300M DAU, 500M tweets/day → ~5.8k tweet WPS avg, peak ~20k WPS. Timeline reads 10× writes → 200k read RPS peak. Avg tweet 300 bytes; media 20% × 2 MB. Fan-out: avg 200 followers, 1% celebs with 1M+.",
        """<code>POST /tweets</code>; <code>GET /home_timeline?cursor=</code>; <code>GET /users/{{id}}/tweets</code>; <code>POST /follow/{{userId}}</code>; <code>POST /tweets/{{id}}/like</code>. Cursor by (timestamp, id).""",
        "<code>users</code>, <code>tweets</code>, <code>follows</code> (follower, followee), <code>likes</code>. Timeline cache: Redis sorted set tweet_ids per user OR fan-out-on-read from follow list.",
        """Post → Tweet Service → tweets DB shard by user_id
  → Fan-out Service (async for normal, hybrid for celebs)
  → Redis timeline caches (per user ZSET)
  → Kafka tweet.events → Counter, Search, Notification
  → CDN media
  → Timeline read from Redis with fallback fan-out-on-read""",
        "<b>Fan-out.</b> Normal user (&lt;10k followers): on post, push tweet_id to each follower's timeline cache (async queue). Celebrity: skip push; merge on read from followees' tweet lists. <b>Hybrid threshold</b> e.g. 10k followers. <b>Ranked feed</b> (follow-up): ML scorer async updates candidate set.",
        "Home timeline Redis ZSET top 800 tweet ids per user. Tweet object cache by id. CDN immutable media.",
        "tweet.events for fan-out workers, search index, notification (@mention), analytics. Separate fan-out queue per priority tier.",
        "Tweets sharded by author user_id. Follow graph in Postgres or graph store. Timeline purely cache — rebuild from fan-out-on-read if cold.",
        "Post ack after durable write; timeline eventual (seconds). Like counts eventual. Delete: tombstone propagate async.",
        "Fan-out worker backlog → timelines stale briefly. Redis eviction → cold timeline slower (fan-out-on-read). Celebrity post → read path heavy — rate limit visibility.",
        "Block/hide; spam detection on post; rate limit tweets; media virus scan; private accounts filter on fan-out.",
        "Timeline p99, fan-out lag, fan-out queue depth, cold cache miss rate, post success.",
        "Scale fan-out workers horizontally; Redis cluster shards timeline keys; read replicas for user/tweet DB; celeb tier separate pipeline.",
        "Celebrity fan-out write storm; hot tweet object; follow graph size for fan-out-on-read; Redis memory for 300M users × timeline.",
        "Fan-out on write vs read vs hybrid (hybrid standard answer). Ranked vs chronological. Push vs pull notification for new tweets.",
        "Spaces/audio; communities; ads injection; quote tweets graph; federated ActivityPub.",
        "Always discuss celebrity problem with numbers (1% of 500M tweets). Draw hybrid fan-out. Timeline read path. Cache sizing rough estimate.",
    )


def _instagram():
    return _case(
        "cs-instagram",
        "Instagram feed",
        "Instagram feed stories photos ranking CDN social graph",
        "Design a photo-sharing social network: upload photos/videos, follow graph, home feed, stories, likes, comments, and explore/discovery.",
        "Upload image/video with filters; follow users; home feed (ranked); stories 24h TTL; like/comment; user profile grid; explore recommendations; notifications; direct messages (optional scope).",
        "Feed load p99 &lt; 800ms; upload ack &lt; 2s (async processing); 99.9% availability; media global CDN p99 &lt; 100ms; stories expire precisely within 1 min of 24h.",
        "Feed ranking ML in scope or chronological fallback? Video transcode pipeline? Public vs private accounts?",
        "2B MAU, 500M DAU, 100M posts/day, 5 feed loads/user/day → 2.5B feed reads/day → ~29k avg RPS peak ~90k. Posts 100 MB avg raw → transcode to multiple renditions. Stories 500M/day 15s video.",
        """<code>POST /media</code> multipart → processing job id; <code>GET /feed?cursor=</code>; <code>GET /stories/tray</code>; <code>POST /media/{{id}}/like</code>; webhook when processing complete.""",
        "<code>users</code>, <code>media</code> (owner, type, status, renditions URLs), <code>follows</code>, <code>feed_candidates</code> (precomputed), <code>stories</code> (expires_at TTL index), <code>likes</code>, <code>comments</code>.",
        """Upload → Object store → Transcode workers → CDN
  → Media metadata DB
  → Feed Service (ranking + candidate generation)
  → Redis feed cache per user
  → Kafka media.events → Feed ranker, Notification, Explore indexer
  → Graph store for follows""",
        "<b>Media pipeline.</b> Accept upload to S3, enqueue transcode (multiple resolutions), update status, CDN purge/warm. <b>Feed ranking.</b> Offline + nearline: generate candidate pool from follow graph + explore; online lightweight ranker scores top 50. <b>Stories.</b> Separate low-latency store with TTL; tray = active stories from followees.",
        "Feed page cache (user, cursor) TTL 60s. Media URLs CDN immutable. Story tray Redis with TTL aligned to expiry.",
        "media.events → feed fan-out (lighter than Twitter — ranked batch), notification, explore features, delete cascade.",
        "Media metadata Postgres/Cassandra; blob S3; stories Redis or Cassandra TTL; graph DB or sharded follows table.",
        "Feed ranked eventual (minutes for rank features). Like count eventual. Story view immediate RYW for viewer.",
        "Transcode backlog → post stays 'processing'. CDN miss → origin load spike. Ranking model stale → fallback chronological.",
        "Private account media ACL on CDN signed URLs; report/block; EXIF strip; child safety scanning async.",
        "Feed p99, transcode queue depth, CDN hit ratio, story expiry job lag, upload failure rate.",
        "Transcode worker pool auto-scale; CDN multi-PoP; feed service horizontal; shard by user_id.",
        "Transcode CPU; feed ranking compute; hot influencer; storage egress costs; story expiry sweep at scale.",
        "Precompute candidates vs full online rank. Store originals vs derived only. Pull CDN vs push to edge.",
        "Reels; shopping tags; ads; DMs E2E; AR filters client vs server.",
        "Emphasize media pipeline + ranked feed. Numbers on read:write. CDN architecture. Story TTL mechanism. Ranking as async follow-up.",
    )


def _youtube():
    return _case(
        "cs-youtube",
        "Design YouTube",
        "YouTube video upload transcode streaming CDN recommendations",
        "Design a video platform: upload, transcode, store, stream to global audience, metadata, comments, subscriptions, and recommendations.",
        "Upload video; processing to multiple bitrates (ABR); playback with seeking; thumbnails; channels and subscriptions; comments/likes; search; home recommendations; view counts; live streaming (optional).",
        "Playback start p99 &lt; 2s; upload accept &lt; 5s (processing async); 99.99% playback availability via CDN; transcode SLA &lt; 30 min for 1080p hour video; view count accuracy ±5% OK.",
        "Live vs VOD focus? DRM? Monetization/ads? Global or single region upload?",
        "2B logged-in, 500M DAU watch 5 videos/day avg 10 min → massive CDN egress not origin RPS. 500k hours uploaded/day. Transcode farm CPU-bound. Metadata 1M video queries/sec peak globally at CDN.",
        """<code>POST /videos/upload/init</code> multipart presigned; <code>POST /videos/{{id}}/complete</code>; <code>GET /videos/{{id}}/manifest.m3u8</code>; <code>GET /feed/home</code>; <code>GET /search?q=</code>.""",
        "<code>videos</code> (owner, status processing/ready, renditions manifest pointer), <code>channels</code>, <code>subscriptions</code>, <code>comments</code>, <code>view_events</code> aggregated.",
        """Upload → S3 raw → Transcode cluster → CDN origin (segments)
  → Video metadata service
  → Kafka upload.events → Transcode, Thumbnail, Search index, Reco features
  → CDN edge (95%+ traffic)
  → Recommendation offline (Spark) + online ranker
  → ES search""",
        "<b>Transcoding.</b> DAG: ingest → probe → encode 360p-4K → package HLS/DASH → store segments → update manifest. Priority queue by uploader tier. <b>Playback.</b> Client adaptive bitrate from manifest; CDN cache segments immutable. <b>View count.</b> Sampled heartbeat events aggregated — not sync per view on OLTP.",
        "CDN caches video segments (long TTL, content-addressed). Manifest short TTL. Metadata video page cache 5 min.",
        "upload.events → transcode workers (GPU), search, reco pipeline, notification to subscribers.",
        "Metadata Postgres sharded; blobs never in DB; view aggregates in Cassandra or warehouse.",
        "Video ready: eventual after transcode. View counts eventual. Subscriptions strong on write.",
        "Transcode failure → retry with DLQ; partial renditions serve best available. CDN origin overload → multi-origin failover.",
        "Content ID scan; age restrictions geo-block; signed URLs for premium; comment moderation queue.",
        "Playback start time, transcode queue lag, CDN hit ratio, rebuffer rate (client telemetry).",
        "CDN is the scale story; transcode auto-scale on queue; metadata DB read replicas; reco precompute.",
        "Transcode cost and time; storage of long-tail videos; reco freshness vs compute; live chat fan-out.",
        "Self-hosted CDN vs third party. Sync view count vs approximate. Central upload region vs edge ingest.",
        "Live streaming; Shorts; monetization; copyright Content ID ML.",
        "Split upload/transcode/playback paths. CDN carries scale. View count async. Reco as offline+online two-tier.",
    )


def _netflix():
    return _case(
        "cs-netflix",
        "Design Netflix",
        "Netflix streaming CDN Open Connect encoding recommendations",
        "Design a subscription streaming service: catalog, encoding, personalized rows, playback, continue watching, and multi-device DRM.",
        "Browse catalog by genre/row; personalized homepage; stream with ABR; resume position; profiles per account; watchlist; search; download offline (mobile); billing integration (high level).",
        "Playback start &lt; 3s p99; rebuffer &lt; 0.5%; 99.99% streaming; encode new titles within SLA; personalization refresh daily or faster for trending.",
        "Live content? Ad tier? Regional licensing? Studio upload workflow?",
        "200M subscribers, 100M concurrent peak evening → CDN serves terabits; origin RPS low. Catalog 15k titles × bitrates. Personalization: batch + real-time signals.",
        """<code>GET /browse/home</code>; <code>GET /titles/{{id}}</code>; <code>GET /play/{{id}}/manifest</code>; <code>PUT /progress/{{id}}</code> heartbeat; <code>GET /search</code>.""",
        "<code>titles</code>, <code>licenses</code> (region, window), <code>profiles</code>, <code>viewing_progress</code>, <code>recommendation_rows</code> precomputed per profile cohort.",
        """Studio ingest → Encode → Origin → Open Connect CDN (ISP appliances + cloud)
  → Catalog API
  → Personalization (offline Spark + online feature store)
  → Progress service (Cassandra)
  → Client ABR player""",
        "<b>Open Connect.</b> Push popular content to ISP boxes; origin only on cache miss. <b>Personalization.</b> Precompute row candidates nightly; online re-rank top N with recent events from Kafka. <b>Progress.</b> Heartbeat every 30s async; RYW on 'continue watching' row.",
        "Catalog title metadata CDN+app cache. Manifest per CDN edge. Personalization row cache per profile_id 15 min.",
        "view.events → reco feature store, popularity counters, 'because you watched' pipelines.",
        "Progress in wide-column store; catalog relational; analytics warehouse separate.",
        "Progress RYW after heartbeat flush (~30s). Catalog eventual across regions. Recommendations eventual hours unless trending boost.",
        "CDN miss storm on new release → pre-position content. License expiry → purge CDN keys. Reco pipeline delay → fallback popularity rows.",
        "DRM Widevine/FairPlay; geo-fencing licenses; device limits; no plaintext stream URLs long-lived.",
        "Rebuffer rate, startup time, CDN fill ratio, encode backlog, signup-to-first-play funnel.",
        "Scale CDN not API; regional catalog shards; personalization compute offline; progress writes batched.",
        "Evening peak bandwidth; cold title launch; personalization for new users (cold start); cross-device progress sync.",
        "Push CDN vs pull only. Heavy offline reco vs online only. Central vs regional catalog.",
        "Live sports; ad insertion; social watch party; gaming cloud.",
        "Netflix interview = CDN + personalization + progress, not CRUD. Draw Open Connect concept. ABR. Personalization two-phase.",
    )


def _dropbox():
    return _case(
        "cs-dropbox",
        "Design Dropbox",
        "Dropbox file sync block storage deduplication conflict",
        "Design a cloud file sync product: desktop/mobile clients sync folders, handle conflicts, share links, and block-level deduplication.",
        "Upload/sync files and folders; delta sync (blocks); conflict copies; share links with permissions; version history; selective sync; desktop watch folder; quota per user.",
        "Sync delta ack &lt; 1s for small changes; 99.9% durability; eventual consistency across devices within 30s; large file resume; dedupe saves storage.",
        "E2E encryption? Team vs personal? Max file size? Real-time co-edit?",
        "700M users, 50M DAU active sync, avg 50 MB/day delta sync → write bandwidth focus. 500 PB total storage with 2× dedupe factor. Metadata 10B files.",
        """<code>POST /files/upload_block</code> hash addressed; <code>POST /files/commit</code> manifest of block hashes; <code>GET /files/{{path}}/metadata</code>; <code>GET /delta?cursor=</code> long poll or WS; <code>POST /shares</code>.""",
        "<code>namespaces</code> (user/team), <code>file_entries</code> (path, revision, block_list[]), <code>blocks</code> (hash, size, ref_count), <code>share_links</code>. Content-addressed blocks.",
        """Client → Sync API → Metadata DB (Postgres)
  → Block store S3
  → Dedupe index by hash
  → Notification long-poll/WS for changes
  → Kafka sync.events → Search index, Audit""",
        "<b>Block sync.</b> Client computes rolling hash chunks (4 MB); upload only missing blocks; commit new file revision atomically. <b>Conflict.</b> If revision mismatch on commit → create conflicted copy file. <b>Delta API.</b> Cursor of namespace revision; clients pull changes since cursor.",
        "Metadata hot paths cached per namespace revision. Blocks immutable — CDN for popular shared blocks optional.",
        "sync.events for cross-device notify, search indexing, virus scan on new block hash.",
        "Metadata Postgres with namespace sharding; blocks S3; ref_count garbage collect unreferenced blocks async.",
        "Per-namespace linearizable revision increments. Cross-device eventual seconds. Share link read strong on permission check.",
        "Split brain two clients offline → conflict copies both kept. Block upload partial → resume by hash. GC deletes block still referenced → ref_count prevents.",
        "Share link tokens; team ACL; encrypt at rest; client-side E2E optional enterprise; scan blocks for malware.",
        "Sync latency, block upload failures, storage per user, GC lag, conflict rate.",
        "Shard metadata by namespace; block store unlimited horizontal; notify service scale with connections.",
        "Hot namespace sync storm; ref_count GC at PB scale; list_dir huge folders; mobile battery vs sync frequency.",
        "Block vs file level dedupe. Central metadata vs peer (Dropbox is central). Conflict copy vs merge for text.",
        "Paper co-edit; team admin DLP; smart sync partial hydration.",
        "Explain content-addressed blocks + delta sync. Revision cursor. Conflict policy. Dedupe storage math.",
    )


def _gdrive():
    return _case(
        "cs-gdrive",
        "Design Google Drive",
        "Google Drive docs collaboration permissions search realtime",
        "Design a cloud document and file storage system like Google Drive: files, folders, Google Docs-style collaboration, sharing, and search.",
        "Store files/folders; real-time collaborative editing for docs/sheets; sharing with link or user; permissions view/comment/edit; search by name/content; version history; offline sync (mobile).",
        "Doc typing latency &lt; 100ms p99; file list &lt; 500ms; 99.9% availability; collaboration without lost edits; search lag &lt; 5 min for content.",
        "Docs OT/CRDT in scope or file-only? Max collaborators? Google-scale or startup scale?",
        "1B users, 100M concurrent docs sessions peak hypothetical → OT traffic dominates. 5B files metadata. Docs 50 KB/s typing aggregate per active doc session via OT service.",
        """Drive API: <code>files.list</code>, <code>files.create</code>, <code>permissions.create</code>; Docs: WebSocket OT operations; <code>GET /files/{{id}}/export</code>.""",
        "<code>files</code> (parent_id, mime, owners), <code>permissions</code>, <code>revisions</code>, <code>doc_snapshots</code> + <code>op_log</code> for OT.",
        """Client → API Gateway → File metadata service
  → Object store (binary files)
  → Docs OT service (WS, in-memory + persist op log)
  → Kafka → Search indexer, Virus scan
  → ES content search""",
        "<b>OT pipeline.</b> Operations transformed against concurrent ops; periodic snapshot + compact op log. Single doc session routed to one OT server (shard by doc_id). <b>Files.</b> Standard metadata + blob like Dropbox without block dedupe requirement unless asked.",
        "File metadata cache; doc snapshot cache for load; CDN for binary downloads.",
        "file.events → search, audit, thumbnail generation, quota accounting.",
        "Metadata Postgres; op log Cassandra; blobs GCS/S3.",
        "OT session: strong ordering within doc. File ACL eventual seconds. Search eventual.",
        "OT server crash → replay op log on new server. Partition → client queue ops offline. Permission revoke → next op rejected.",
        "Sharing link leak prevention; domain-wide policies; encrypt blobs; audit downloads.",
        "OT lag, op log size, snapshot frequency, search index lag, share permission denials.",
        "Shard OT by doc_id; scale file metadata read replicas; search independent cluster.",
        "Hot collaborative doc single shard; op log unbounded → snapshot; search index size.",
        "CRDT vs OT vs lock. Central OT vs peer-to-peer. Dedupe optional for Drive binary.",
        "Sheets formula engine; Shared drives team model; Vault retention.",
        "Split binary Drive vs Docs OT if time short. OT deep dive if collaborative scope confirmed.",
    )


def _notif():
    return _case(
        "cs-notif",
        "Notification system",
        "notification system email push in-app fan-out preferences dedupe",
        "Design a multi-channel notification platform: in-app, email, push, SMS — triggered by product events with user preferences, deduplication, and delivery guarantees.",
        "Send notification on events (issue assigned, comment, etc.); channels in-app/email/push/SMS; user preferences per channel and event type; digest batching; read/unread in-app; template rendering; unsubscribe; rate limits per user.",
        "API accept &lt; 100ms (async delivery); 99% email within 5 min; push within 30s; at-least-once delivery with dedupe; no duplicate emails for same event; preference honored before send.",
        "Exactly-once required? Global or single region? Template who owns? Priority tiers?",
        "500M users; 2B events/day → ~23k events/s avg, peak ~70k/s. Fan-out avg 3 channels × 30% eligible → ~60k delivery jobs/s peak. Email provider limit 100/s per domain — need many IPs/pools.",
        """<code>POST /notifications/emit</code> internal {{eventType, actor, targetUsers[], payload, idempotencyKey}}; <code>GET /notifications?cursor=</code>; <code>PUT /preferences</code>; <code>POST /notifications/{{id}}/read</code>.""",
        "<code>notification_events</code> (idempotency_key UNIQUE), <code>deliveries</code> (user, channel, status), <code>preferences</code>, <code>in_app_inbox</code>, <code>templates</code>, <code>digest_buckets</code>.",
        """Product services → Notification API (validate, dedupe)
  → Kafka notification.events
  → Router (prefs, quiet hours, channel select)
  → Per-channel workers (email, push, SMS, in-app)
  → Provider adapters (SES, FCM, Twilio)
  → Postgres + Redis dedupe cache
  → In-app store (Cassandra)""",
        "<b>Dedupe.</b> idempotency_key + user + channel UNIQUE; Redis SET 24h TTL for hot path. <b>Fan-out.</b> One event → N users → M channels; expand in router worker, not in API thread. <b>Digest.</b> Accumulate in Redis sorted set until window closes or cap reached.",
        "Preference cache per user TTL 5 min. Template compile cache. Dedupe Redis.",
        "Kafka primary; per-channel topics for isolation; DLQ per provider; retry with exponential backoff.",
        "Postgres for prefs and audit; Cassandra for in-app inbox high write; Redis dedupe.",
        "In-app inbox RYW after write worker ack. Email/push eventual minutes. Preferences read strong on routing decision.",
        "SES throttled → backoff queue, alternate pool. Provider down → DLQ alert. Duplicate emit → dedupe drops. Hot user 10k notifications → rate cap digest.",
        "Unsubscribe tokens signed; no PII in push payload; internal API mTLS; tenant isolation on templates.",
        "Delivery success per channel, lag p99, DLQ depth, dedupe hit rate, provider error codes.",
        "Scale channel workers independently; Kafka partitions by user_id hash; email shard by domain reputation.",
        "Email provider limits; fan-out explosion on @channel; template rendering CPU; digest timer accuracy.",
        "Sync send vs queue always (queue). Multi-provider failover vs single. In-app pull vs push WS.",
        "Priority/on-call paging; A/B template test; localization; compliance quiet hours GDPR.",
        "Classic Phase 3 mock (Day 21). Emit async. Draw router + channel workers. Dedupe story. Preference before fan-out.",
    )


def _chat():
    return _case(
        "cs-chat",
        "Chat system",
        "chat system websocket message ordering group channel WhatsApp Messenger",
        "Design a 1:1 and group chat system: message delivery, ordering, read receipts, presence, media, and push for offline users.",
        "1:1 and group chats; send text/media; delivery and read receipts; typing indicators; presence online/last seen; message history pagination; push notification offline; block users; end-to-end optional.",
        "Message ack &lt; 200ms; delivery to online recipient &lt; 1s; durability once acked; order preserved per chat; support groups up to 256 members; presence update &lt; 5s.",
        "E2E encryption? Message retention? Maximum group size? Multi-device sync?",
        "500M DAU, 40 msgs/user/day → 20B msgs/day → ~231k msg/s avg, peak ~700k/s. Groups 20% of msgs, avg 50 members → fan-out 10M delivery events/s peak subset.",
        """<code>POST /chats/{{id}}/messages</code>; <code>GET /chats/{{id}}/messages?before=</code>; <code>WS /connect</code> for realtime; <code>PUT /messages/{{id}}/read</code>; <code>POST /presence</code> heartbeat.""",
        "<code>chats</code>, <code>chat_members</code>, <code>messages</code> (chat_id, seq monotonic), <code>read_receipts</code>, <code>devices</code> for push tokens.",
        """Mobile/Web → WS Gateway + REST
  → Chat Service (assign seq, persist)
  → Message store (Cassandra: chat_id + seq)
  → Redis presence + typing pub/sub
  → Kafka → Push, Search (optional), Media virus scan
  → S3 media""",
        "<b>Sequencing.</b> Per-chat sequence counter (Redis INCR or DB) for total order. Client displays by seq. <b>Group fan-out.</b> Write once; push WS to online members via connection registry; FCM for offline. <b>Multi-device.</b> Sync same chat_id across devices via seq cursor.",
        "Recent messages per chat in Redis. User→connection mapping in Redis for WS routing.",
        "message.events for push, audit, moderation ML, backup.",
        "Cassandra partition chat_id; metadata Postgres; seq hot chat sharded carefully.",
        "Per-chat strong order. Read receipts eventual. Presence eventual few seconds.",
        "WS loss → REST catch-up from last_seq. Counter gap → repair job. Split brain rare with single seq writer per chat.",
        "Block list check on send; rate limit; media scan; E2E optional client-side keys out of scope server.",
        "Send p99, WS delivery lag, push latency, seq gap alerts, online connection count.",
        "Horizontal WS; message store scale with partitions; separate push tier.",
        "Hot group fan-out; seq counter single point per chat; presence thundering herd on reconnect.",
        "Pull history vs push all (push deltas). Central seq vs Lamport clocks. Store vs derive receipts.",
        "Voice/video SFU; bots; message reactions; export legal hold.",
        "Similar Slack but emphasize 1:1 + seq ordering + receipts. Draw seq assignment. Offline push path.",
    )


def _search():
    return _case(
        "cs-search",
        "Search engine",
        "search engine inverted index crawling ranking Elasticsearch web search",
        "Design a web search engine: crawl the web, build inverted index, rank results, serve queries with autocomplete and spell correction.",
        "Crawl URLs; index documents; query with keywords; ranked results; snippets; autocomplete; spell correct; freshness for news; safe search; pagination.",
        "Query p99 &lt; 500ms; index update within hours for crawl; 99.9% query availability; billions of documents indexed.",
        "Whole web or vertical (product search)? Personalized ranking? Real-time index or batch?",
        "10B pages indexed; 100k QPS peak; avg query 3 terms; index size ~100 TB inverted + stored fields. Crawl 1B pages/day refreshed.",
        """Internal: <code>POST /crawl/seed</code>; <code>GET /search?q=</code> page token; <code>GET /suggest?q=</code>. Crawler politeness delay per domain.""",
        "<code>documents</code> (url, content_hash, pagerank, terms[]), inverted index shards term→doc_ids, <code>link_graph</code> for PageRank offline.",
        """Query → Search API → Query parser (spell, expand)
  → Index servers (sharded by term hash)
  → Ranker (PageRank + BM25 + boosts)
  → Snippet generator
  Crawl pipeline: Frontier queue → Fetcher → Parser → Index builder
  Kafka crawl.events → Index updates""",
        "<b>Crawl.</b> Priority frontier; respect robots.txt; dedupe URL hash; politeness 1 req/s/domain. <b>Index.</b> MapReduce/Spark build inverted lists; sharded by term. <b>Query.</b> Scatter-gather posting lists, merge heap top K, rank, snippet from stored field.",
        "Query result cache common queries 60s. Autocomplete trie in memory per shard. CDN for static.",
        "crawl.frontier Kafka; index build batch jobs; incremental index segments merge.",
        "Index in dedicated search cluster (ES/Lucene custom); crawl metadata Postgres; graph store for links.",
        "Index eventual hours behind web. Query read from near-real-time segments + committed segments.",
        "Index shard down → partial results flag. Crawler banned → domain stale. Hot query overload → cache + shed long queries.",
        "Safe search filter; no SQL injection in query parser; rate limit queries; block scraper abuse.",
        "Query latency histogram, crawl lag per domain, index size growth, zero-result rate.",
        "Horizontal index shards; replicate hot shards; crawl workers per domain partition; query tier auto-scale.",
        "Posting list merge for common terms ('the'); index rebuild time; crawler trap infinite URLs.",
        "Batch vs incremental index. Centralized rank vs federated. ES vs custom Lucene.",
        "Ads auction; personal search history; image search; federated vertical tabs.",
        "Separate crawl/index/query. Explain inverted index verbally. Ranking two-phase retrieve+rank. Scale via sharding.",
    )


def _upload():
    return _case(
        "cs-upload",
        "File upload system",
        "file upload multipart presigned resume virus scan large files",
        "Design a file upload service for multi-GB files: resumable uploads, virus scanning, metadata, and integration with a product (e.g. Jira attachments).",
        "Init upload; multipart/chunk upload; resume after failure; complete and attach to entity; progress polling; virus/malware scan; quota; delete and GC.",
        "Init &lt; 200ms; part upload &lt; 5s p99 per 5 MB chunk; 99.9% durability after complete; scan complete within 5 min for 100 MB file; support 5 GB max.",
        "Direct client-to-storage or via API? Public vs authenticated only? Deduplication?",
        "10M uploads/day; avg 20 MB; 1% files 1 GB → bandwidth to object store not API. 500 upload init RPS peak.",
        """<code>POST /uploads</code> → {{uploadId, partSize, presignedUrls[]}}; <code>PUT</code> to presigned part; <code>POST /uploads/{{id}}/complete</code> {{parts:[{{etag,partNumber}}]}}; <code>GET /uploads/{{id}}/status</code>.""",
        "<code>uploads</code> (id, user, status, parts_completed bitmap), <code>files</code> (storage_key, scan_status), link table to parent entity.",
        """Client → Upload API (auth, quota)
  → Object store multipart (S3)
  → Postgres upload session state
  → Kafka upload.completed → Virus scan worker → Metadata finalize
  → CDN optional after clean""",
        "<b>Multipart.</b> Client splits file; parallel PUT parts (limit 4 concurrent); complete composes object server-side. <b>Resume.</b> List parts API returns done part numbers. <b>Scan.</b> Async on complete; entity shows 'scanning' until pass.",
        "Presigned URL TTL 1 hour. Don't cache incomplete uploads.",
        "upload.completed → scan queue (priority by size); DLQ infected files; notify parent service.",
        "Session state Postgres; blobs S3; scan results Postgres.",
        "Complete: strong on compose. Download allowed only after scan_status=clean (strong gate).",
        "Part upload fail → retry same part number. Complete with missing part → 400. Scan timeout → quarantine state.",
        "Auth on init; presigned short TTL; content-type allowlist; block executable MIME; tenant quota.",
        "Upload success rate, time-to-complete, scan backlog, infected file count, part retry rate.",
        "API stateless; S3 scales; scan workers auto-scale on queue depth.",
        "Scan CPU bottleneck; many small files vs few huge; stale incomplete uploads storage leak — lifecycle rule.",
        "Presigned direct-to-S3 vs proxy through API (presigned wins). Sync scan vs async (async).",
        "Image transcoding; client-side encryption; cross-region replication.",
        "Tied to Phase 3 Day 28 mock. Presigned multipart diagram. Resume story. Scan async gate.",
    )


def _analytics():
    return _case(
        "cs-analytics",
        "Analytics system",
        "analytics pipeline real-time batch warehouse metrics dashboard",
        "Design a product analytics system: ingest high-volume events, real-time and batch aggregation, dashboards, and funnel queries.",
        "Track client/server events (page view, click, purchase); real-time counters (DAU, active now); batch warehouse for historical analysis; funnel and retention queries; dashboard API; data export; privacy opt-out.",
        "Ingest 1M events/s peak; real-time dashboard lag &lt; 1 min; batch queries complete overnight; 99.9% ingest availability; GDPR delete propagation within 30 days.",
        "Real-time strict or near-real-time OK? Raw event retention? Self-serve SQL or fixed dashboards?",
        "500M events/day → ~5.8k/s avg, peak 1M/s during flash sale if stated. 1 KB avg event → 500 GB/day raw. 3 year retention compressed ~200 TB warehouse.",
        """<code>POST /collect</code> batch events (API key); internal <code>GET /metrics/active_users</code>; <code>POST /queries/funnel</code> async job id; <code>GET /reports/{{id}}</code>.""",
        "Raw: Kafka topics by event_type. OLAP: Star schema <code>fact_events</code>, dims user/product/time. Rollups: <code>hourly_counts</code> materialized.",
        """SDK → Collect API → Kafka (partition by user_id)
  → Stream processor (Flink) → Real-time Redis/ClickHouse
  → Batch (Spark) → S3 data lake → Snowflake/BigQuery
  → Query service → Dashboard UI
  → Schema registry for event contracts""",
        "<b>Ingest.</b> Validate schema version; drop malformed; partition for parallel consumers. <b>Real-time.</b> Tumbling window counts in Flink → Redis for dashboard tiles. <b>Batch.</b> Daily partition Parquet; merge small files; preaggregate funnels nightly.",
        "Dashboard tile cache 30s. Query result cache keyed by query hash 5 min.",
        "Kafka central; separate topics per priority; dead letter for bad schema.",
        "Kafka retention 7 days hot; S3 lake cold; ClickHouse for interactive OLAP; never query OLTP product DB.",
        "Real-time metrics eventual 30–60s. Batch reports strong for completed job snapshot. Raw ingest ack after Kafka write.",
        "Kafka lag → dashboards stale alert. Schema break → quarantine topic. Hot key user_id skew → salt partition key.",
        "PII hashing at ingest; opt-out flag filter in stream; API keys per tenant; row-level security in warehouse.",
        "Ingest rate, consumer lag, Flink checkpoint failures, query queue time, event schema reject rate.",
        "Scale Kafka partitions; Flink parallelism; separate batch cluster; read replicas on OLAP.",
        "Cardinality explosion on high-cardinality dims; late-arriving events; backfill replay overload.",
        "Lambda vs Kappa architecture. Real-time approx vs exact. ClickHouse vs Druid vs warehouse only.",
        "ML feature store export; session replay; experimentation A/B integration.",
        "Never OLTP for analytics — say early. Draw Kafka → stream + batch fork. Schema registry mention. GDPR delete pipeline.",
    )


def _ratelimit():
    return _case(
        "cs-ratelimit",
        "Rate limiter",
        "rate limiter token bucket sliding window Redis distributed",
        "Design a distributed rate limiter for API protection: per-user, per-IP, and per-tenant limits with configurable rules.",
        "Limit requests per window (e.g. 1000/hour/user); burst allowance; different rules per endpoint tier; return 429 with Retry-After; distributed across many API nodes; dynamic rule updates.",
        "Check adds &lt; 1ms p99; accurate within 1% at scale; 99.99% limiter availability (fail open vs closed policy explicit); support 1M distinct keys.",
        "Hard enforce or soft warn? Global vs regional? Fail open if Redis down?",
        "100k API RPS peak; 10M active limit keys (users+IPs); 100 rules evaluated per request worst case → optimize hot path to 1 Redis round-trip.",
        """Middleware: <code>X-RateLimit-Remaining</code> headers; <code>429</code> + Retry-After. Admin: <code>PUT /rules/{{id}}</code> propagated to edge within 60s.""",
        "<code>rules</code> (scope, limit, window, burst), counter storage in Redis keys <code>rl:{{scope}}:{{id}}:{{window}}</code>.",
        """API Gateway / Sidecar → Rate Limit Service
  → Redis Cluster (counters)
  → Optional local token cache (80% hit) → reduce Redis
  → Rules config from etcd/Consul watch""",
        "<b>Token bucket.</b> Redis LUA script atomic refill+decrement. <b>Sliding window.</b> Sorted set of timestamps or approximate sliding window log. <b>Local cache.</b> Brief over-admission acceptable for global limit — document trade-off.",
        "Local LRU 100ms TTL mirror of Redis counter for hot keys. Rules cache in memory on each node.",
        "Optional audit queue for blocked requests analytics — not on hot path.",
        "Redis cluster only; no Postgres on request path.",
        "Counter strong per key single-threaded LUA. Rule update eventual 60s.",
        "Redis down → fail open with alert vs fail closed (product choice). Clock skew → use Redis TIME. Race without LUA → over-count.",
        "Prevent limit bypass headers; protect admin rule API; DDoS at L7 before limiter.",
        "429 rate, Redis latency, local cache hit, rule propagation lag, false positive blocks.",
        "Redis cluster horizontal; many gateway nodes stateless; shard keys.",
        "Hot key celebrity user; Redis single key throughput; thundering herd after window reset.",
        "Token bucket vs sliding window vs fixed window (mention boundary burst). Central Redis vs gossip (Redis wins simplicity). Fail open vs closed.",
        "Geo-specific limits; cost-based limiting; GraphQL query complexity limit.",
        "Day 23 topic — implement token bucket then design distributed. LUA atomicity. Fail-open policy sentence.",
    )


def _payment():
    return _case(
        "cs-payment",
        "Payment system",
        "payment system stripe ledger idempotency double charge saga PCI",
        "Design a payment processing system: charge cards, idempotent payments, ledger, refunds, webhooks from PSP, and reconciliation.",
        "Create payment for order; authorize/capture; refund full/partial; store payment methods tokenized; webhook from Stripe-like PSP; idempotent retries; ledger double-entry; daily reconciliation.",
        "Payment API p99 &lt; 500ms (excluding PSP); exactly-once monetary effect (idempotent); 99.99% ledger durability; PCI scope minimized (no raw PAN storage); audit every state change.",
        "Which PSP? Multi-currency? Hold/capture vs immediate charge? Strong consistency globally?",
        "50M users; 5M transactions/day → ~58 TPS avg, peak 500 TPS. Avg $40 → ledger accuracy critical not volume RPS.",
        """<code>POST /payments</code> Idempotency-Key, {{orderId, amount, currency, paymentMethodId}}; <code>POST /payments/{{id}}/capture</code>; <code>POST /refunds</code>; webhook <code>POST /webhooks/psp</code> with signature verify.""",
        "<code>payments</code> (state machine pending/authorized/captured/failed), <code>ledger_entries</code> (debit/credit accounts), <code>idempotency_keys</code> UNIQUE, <code>webhook_events</code> processed id.",
        """Client → Payment API → Postgres (transaction + ledger)
  → PSP adapter (Stripe API)
  → Webhook handler (verify HMAC, idempotent process)
  → Kafka payment.events → Notification, Analytics, Fulfillment
  → Reconciliation batch job nightly""",
        "<b>Idempotency.</b> Key stored with response snapshot; duplicate POST returns same result. <b>State machine.</b> Legal transitions only; webhook and API race resolved by version+state check. <b>Ledger.</b> Double-entry each capture: debit customer liability credit revenue.",
        "Do not cache payment state reads in interview design except idempotency response cache 24h.",
        "payment.events async for email receipt, order fulfillment — never block capture on email.",
        "Postgres ACID primary; ledger append-only; reconciliation compares PSP CSV to ledger.",
        "Strong consistency on ledger and payment row. PSP eventual webhook may arrive before API response — reconcile by payment id.",
        "PSP timeout → leave pending; poll job reconciles. Duplicate webhook → idempotent event id. Partial failure capture → compensating refund saga.",
        "PCI: tokenized PM only; webhook signature; least privilege API keys; encrypt ledger at rest; audit admin refunds.",
        "Capture success rate, PSP latency, webhook lag, reconciliation mismatch count, idempotent replay rate.",
        "Vertical scale DB for TPS stated; PSP handles card network scale; stateless API horizontal.",
        "Ledger contention if undersharded; webhook ordering; currency conversion rounding disputes.",
        "Saga vs 2PC (saga/outbox). Sync PSP call vs async (sync authorize common). Ledger in same DB vs separate service.",
        "Subscriptions recurring; chargebacks dispute flow; multi-PSP failover; crypto (usually out of scope).",
        "Day 25 idempotency tie-in. State machine diagram verbal. Webhook idempotency. Never double charge story.",
    )


def _scheduler():
    return _case(
        "cs-scheduler",
        "Job scheduler",
        "job scheduler cron distributed leader worker at-least-once",
        "Design a distributed job scheduler: cron-like schedules, one-off delayed jobs, at-least-once execution, retries, and visibility for millions of jobs.",
        "Schedule recurring (cron) and one-time jobs; execute HTTP/worker callbacks; retry with backoff; job history; pause/resume; timezone aware; priority queues; dedupe same schedule fire.",
        "Schedule accuracy ±1s for high tier; 99.9% job eventually runs; no lost jobs after ack schedule; support 10M active schedules; worker scale independent.",
        "Exactly-once execution or at-least-once with idempotent workers? Multi-region active-active?",
        "10M schedules; 100k fires/min peak (top of hour spike); avg job 2s; 500 worker concurrency needed peak.",
        """<code>POST /schedules</code> {{cron, callbackUrl, payload}}; <code>POST /jobs</code> runAt; <code>GET /jobs/{{id}}</code> status; worker poll or push from queue.""",
        "<code>schedules</code>, <code>job_runs</code> (schedule_id, fire_time, status, attempt), <code>next_run_at</code> index for due jobs.",
        """API → Schedule DB
  → Leader elector (etcd) runs due scanner OR shard time wheel
  → Kafka/SQS job.ready queue
  → Worker pool (execute callback)
  → DLQ + retry scheduler""",
        "<b>Time wheel / scanner.</b> Leader scans <code>next_run_at &lt; now</code> batch insert job_runs enqueue — not one thread per cron. <b>Execution.</b> Worker POST callback with timeout; record result; retry schedule if fail. <b>Shard.</b> Partition schedules by id for scanner parallelism.",
        "Optional next_run cache in Redis for hot schedules — DB source of truth.",
        "job.ready queue with visibility timeout; retry topic with delay queue (SQS DLQ or Kafka retry topic).",
        "Postgres with index on next_run_at; at 10M scale Cassandra or sharded Postgres.",
        "Schedule definition strong on create. Fire at-least-once; workers idempotent. next_run update transactional with enqueue.",
        "Leader crash → new leader rescans missed window. Duplicate enqueue → idempotent job_run UNIQUE(schedule_id, fire_time). Worker timeout → retry visible again.",
        "Callback URL SSRF block; auth HMAC on worker invoke; tenant isolation on schedules.",
        "Missed fire count, queue lag, job success rate, retry depth, scanner duration.",
        "Multiple scanner shards; worker auto-scale on queue depth; leader election only for coordination not all work.",
        "Top-of-hour thundering herd; DB scan slow without index; callback slow blocks worker — separate thread pool.",
        "Pull vs push workers. DB polling vs Kafka delay topics. Exactly-once illusion via idempotent job_run key.",
        "Workflow DAG (Airflow style); human approval step; global clock skew handling.",
        "At-least-once + idempotent workers standard answer. Due job scan index critical. Draw leader scanner → queue → workers.",
    )


def _flags():
    return _case(
        "cs-flags",
        "Feature flag system",
        "feature flags LaunchDarkly rollout targeting consistent evaluation",
        "Design a feature flag service: boolean and multivariate flags, percentage rollouts, user targeting, consistent evaluation across services, and fast config updates.",
        "Create/update flags; evaluate for user/context; percentage rollout; targeting rules (tenant, email hash); audit changes; SDK caching; kill switch; optional experiment metrics tie-in.",
        "Evaluation &lt; 5ms p99 local SDK; config propagation &lt; 30s globally; 99.99% eval availability (SDK defaults); consistent same user same flag value across requests (sticky bucketing).",
        "Edge eval vs server only? How many flags (100 vs 100k)? Multi-variate JSON payloads?",
        "10k flags; 1B evaluations/day → ~11.6k eval/s (SDK local so this is config fetch RPS ~1k/s). Config updates 100/day.",
        """Admin: <code>PUT /flags/{{key}}</code> rules JSON; SDK: <code>GET /sdk/config?env=prod&version=</code> streaming or poll; server eval <code>POST /evaluate</code> optional.""",
        "<code>flags</code>, <code>rules</code> (priority, conditions, rollout %), <code>segments</code>, <code>audit_log</code>. Evaluation engine deterministic hash(userId+flagKey) → bucket 0-99.",
        """Admin UI → Flag API → Postgres
  → Config CDN / streaming bus (SSE) to SDKs
  → SDK in-process cache + event source
  → Optional eval API for backend services""",
        "<b>Sticky bucketing.</b> <code>hash(userId + flagKey) % 100 &lt; rollout</code> ensures stable assignment. <b>Rule chain.</b> First match wins by priority. <b>Propagation.</b> Version counter bump → SDKs poll or SSE push invalidate cache.",
        "SDK in-memory full config snapshot; ETag on config endpoint; CDN edge for config blob read-heavy.",
        "Config change events Kafka for audit analytics and cache bust fan-out.",
        "Postgres flags; config snapshots to S3/CDN versioned.",
        "Eval deterministic read-your-rules after SDK refresh eventual 30s. Admin write strong.",
        "SDK stale → old flag until refresh — acceptable with version display in debug. CDN stale config → short TTL + SSE override.",
        "Admin RBAC; no PII in flag keys; prevent flag injection in SDK payload schema validate.",
        "Config fetch rate, eval latency client-side, rule eval errors, propagation delay, kill switch activation time.",
        "CDN for config; SDK scales with app instances; flag API low QPS admin.",
        "Rule complexity CPU on edge; too many flags bloating SDK init; inconsistent hash if algorithm changes — version algorithm.",
        "Server-side vs client-side eval (hybrid common). Real-time SSE vs poll (SSE nicer). Store rules vs precomputed segments.",
        "Experimentation stats; guarded rollout auto-rollback; per-tenant flag packs.",
        "Hash bucketing explanation is core. Config propagation architecture. Kill switch story for incidents.",
    )


def cases() -> str:
    items = [
        _jira(),
        _confluence(),
        _trello(),
        _slack(),
        _url(),
        _twitter(),
        _instagram(),
        _youtube(),
        _netflix(),
        _dropbox(),
        _gdrive(),
        _notif(),
        _chat(),
        _search(),
        _upload(),
        _analytics(),
        _ratelimit(),
        _payment(),
        _scheduler(),
        _flags(),
    ]
    return f"""
<section class="block" id="cases" data-search="System Design Case Studies Jira Confluence URL shortener notifications" data-stype="Section" data-cat="design">
  <p class="kicker">45-min drills</p>
  <h2 class="section-title">System Design Case Studies</h2>
  <p class="lede">Twenty full-stack backend designs using the Phase 3 framework. Jira, Confluence, and Trello are Atlassian-shaped practice — not claimed official questions. Timebox: clarify → estimate → APIs → architecture → deep dive → failures → trade-offs.</p>
  {''.join(items)}
</section>
"""
