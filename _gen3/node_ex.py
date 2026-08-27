from util import code, topic, diagram, callout, esc


def _ex(
    eid: str,
    title: str,
    search: str,
    req: str,
    starter: str,
    hints: str,
    solution: str,
    explanation: str,
    failures: str,
    performance: str,
    followups: str,
    constraints: str = "",
) -> str:
    cons_block = f"<p><b>Constraints.</b> {constraints}</p>" if constraints else ""
    return f'''
<article class="ex" id="{eid}" data-search="{esc(search)}" data-stype="Exercise" data-cat="backend">
  <h3>{title}</h3>
  <p><b>Requirements.</b> {req}</p>
  {cons_block}
  <p><b>Starter.</b></p>{code("TypeScript", starter)}
  <p><b>Hints.</b> {hints}</p>
  <p><button type="button" class="toggle-btn" data-toggle="{eid}-sol">Reveal solution</button>
     <button type="button" class="toggle-btn" data-complete="exercises" data-cid="{eid}">Mark complete</button></p>
  <div class="reveal" id="{eid}-sol">
    {code("TypeScript", solution)}
    <p><b>Explanation.</b> {explanation}</p>
    <p><b>Failure cases.</b> {failures}</p>
    <p><b>Performance.</b> {performance}</p>
    <p><b>Interview follow-ups.</b> {followups}</p>
  </div>
</article>'''


EX = [
    (
        "ex-token-bucket",
        "Token-bucket rate limiter",
        "token bucket rate limiter TypeScript Node",
        "Implement an in-memory <code>TokenBucket</code> with configurable capacity and refill rate. Expose <code>tryTake(n?: number): boolean</code> that refills based on elapsed time, allows controlled bursts, and is safe to call from a single Node process. Add a Fastify-style hook sketch that returns 429 with <code>Retry-After</code> when denied.",
        '''export class TokenBucket {
  constructor(private capacity: number, private refillPerSec: number) {}
  tryTake(count = 1): boolean { return false; }
}

export function rateLimitHook(bucket: TokenBucket) {
  return async (_req: unknown, reply: { status(n: number): { header(k: string, v: string): unknown } }) => {
    // return 429 or continue
  };
}''',
        "Refill on every <code>tryTake</code>, not on a timer — fewer moving parts. Store <code>lastRefillMs</code>. Cap tokens at capacity. For 429, compute seconds until one token arrives for <code>Retry-After</code>.",
        '''export class TokenBucket {
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

  secondsUntilAvailable(count = 1): number {
    this.refill();
    const deficit = count - this.tokens;
    if (deficit <= 0) return 0;
    return Math.ceil(deficit / this.refillPerSec);
  }

  private refill(): void {
    const now = Date.now();
    const elapsedSec = (now - this.lastRefillMs) / 1000;
    if (elapsedSec <= 0) return;
    this.tokens = Math.min(this.capacity, this.tokens + elapsedSec * this.refillPerSec);
    this.lastRefillMs = now;
  }
}

type Reply = { status(n: number): { header(k: string, v: string): unknown } };

export function rateLimitHook(bucket: TokenBucket) {
  return async (_req: unknown, reply: Reply): Promise<void> => {
    if (bucket.tryTake()) return;
    const wait = bucket.secondsUntilAvailable();
    reply.status(429).header("Retry-After", String(wait));
    throw new Error("rate_limit_exceeded");
  };
}''',
        "Token bucket models sustained rate plus burst — the interview-friendly choice for public APIs. Refill-on-use avoids <code>setInterval</code> drift and keeps the class testable without fake timers.",
        "Per-process buckets diverge behind a load balancer — two instances double effective quota. Clock skew across machines matters only after you centralize in Redis. Returning 429 without <code>Retry-After</code> causes thundering herds.",
        "O(1) per request. Memory is O(keys) — one bucket per tenant/user if you map keys to instances. At scale, move token state to Redis with Lua for atomic refill+decrement.",
        "How do you rate-limit 1M users across 50 pods? Where do you fail open vs closed if Redis is down?",
    ),
    (
        "ex-retry-jitter",
        "Retry with exponential backoff + jitter",
        "retry exponential backoff jitter TypeScript fetch",
        "Implement <code>withRetry(fn, opts)</code> that retries on configurable status codes or thrown network errors. Use exponential backoff capped at <code>maxDelayMs</code>, full jitter (<code>random(0, delay)</code>), honor <code>Retry-After</code> on 429/503, and respect <code>maxAttempts</code>. Never retry non-idempotent POST unless caller opts in.",
        '''type RetryOpts = {
  maxAttempts?: number;
  baseDelayMs?: number;
  maxDelayMs?: number;
  retryOn?: (err: unknown, res?: Response) => boolean;
};

export async function withRetry<T>(
  fn: (attempt: number) => Promise<T>,
  opts: RetryOpts = {},
): Promise<T> {
  throw new Error("not implemented");
}''',
        "Attempt 0 is the first try; backoff after failure n uses <code>min(maxDelay, base * 2**n)</code> then jitter. Parse <code>Retry-After</code> as seconds or HTTP-date. AbortSignal should cancel the sleep.",
        '''type RetryOpts = {
  maxAttempts?: number;
  baseDelayMs?: number;
  maxDelayMs?: number;
  retryOn?: (err: unknown, res?: Response) => boolean;
  signal?: AbortSignal;
};

const sleep = (ms: number, signal?: AbortSignal) =>
  new Promise<void>((resolve, reject) => {
    if (signal?.aborted) return reject(signal.reason);
    const t = setTimeout(resolve, ms);
    signal?.addEventListener("abort", () => { clearTimeout(t); reject(signal.reason); }, { once: true });
  });

function parseRetryAfter(res: Response): number | undefined {
  const h = res.headers.get("Retry-After");
  if (!h) return undefined;
  const sec = Number(h);
  if (!Number.isNaN(sec)) return sec * 1000;
  const when = Date.parse(h);
  return Number.isNaN(when) ? undefined : Math.max(0, when - Date.now());
}

const defaultRetryOn = (err: unknown, res?: Response) => {
  if (res) return res.status === 429 || res.status >= 500;
  return err instanceof TypeError; // fetch network failure
};

export async function withRetry<T>(
  fn: (attempt: number) => Promise<T>,
  opts: RetryOpts = {},
): Promise<T> {
  const maxAttempts = opts.maxAttempts ?? 4;
  const baseDelayMs = opts.baseDelayMs ?? 200;
  const maxDelayMs = opts.maxDelayMs ?? 8_000;
  const retryOn = opts.retryOn ?? defaultRetryOn;
  let lastErr: unknown;

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      return await fn(attempt);
    } catch (err) {
      lastErr = err;
      const res = (err as { response?: Response }).response;
      if (attempt === maxAttempts - 1 || !retryOn(err, res)) throw err;
      const retryAfter = res ? parseRetryAfter(res) : undefined;
      const exp = Math.min(maxDelayMs, baseDelayMs * 2 ** attempt);
      const delay = retryAfter ?? Math.floor(Math.random() * exp);
      await sleep(delay, opts.signal);
    }
  }
  throw lastErr;
}''',
        "Full jitter spreads retry times so a fleet of clients does not realign after an outage — the classic fix for retry storms. Honoring <code>Retry-After</code> is part of being a good API citizen.",
        "Retrying POST without idempotency keys creates duplicates. Infinite retries on 400-class errors waste resources. Ignoring <code>AbortSignal</code> leaves hung shutdown during deploy.",
        "Worst case latency ≈ sum of delays — cap attempts and max delay explicitly. For high fan-out workers, use per-destination circuit breakers alongside retries.",
        "How do retries make a partial outage worse? When would you retry only at the gateway vs in the SDK?",
    ),
    (
        "ex-circuit-breaker",
        "Circuit breaker for downstream calls",
        "circuit breaker closed open half-open TypeScript",
        "Implement a three-state circuit breaker (<code>closed</code>, <code>open</code>, <code>half-open</code>) wrapping async calls. Track consecutive failures; open after threshold; after cooldown allow one probe in half-open; close on success, re-open on probe failure. Expose <code>exec(fn)</code> that fails fast while open.",
        '''type CBState = "closed" | "open" | "half-open";

export class CircuitBreaker {
  constructor(private failureThreshold = 5, private cooldownMs = 30_000) {}
  async exec<T>(fn: () => Promise<T>): Promise<T> {
    throw new Error("not implemented");
  }
  get state(): CBState { return "closed"; }
}''',
        "Only count failures you classify as downstream (5xx, timeout) — not 404. Store <code>openedAt</code>. In half-open, serialize probes (one in flight). Emit metrics on state transitions.",
        '''type CBState = "closed" | "open" | "half-open";

export class CircuitOpenError extends Error {
  constructor() { super("circuit_open"); this.name = "CircuitOpenError"; }
}

export class CircuitBreaker {
  private state: CBState = "closed";
  private failures = 0;
  private openedAt = 0;
  private halfOpenInFlight = false;

  constructor(
    private readonly failureThreshold = 5,
    private readonly cooldownMs = 30_000,
    private readonly isFailure: (err: unknown) => boolean = () => true,
  ) {}

  getState(): CBState { return this.state; }

  async exec<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === "open") {
      if (Date.now() - this.openedAt < this.cooldownMs) throw new CircuitOpenError();
      this.state = "half-open";
      this.halfOpenInFlight = false;
    }
    if (this.state === "half-open") {
      if (this.halfOpenInFlight) throw new CircuitOpenError();
      this.halfOpenInFlight = true;
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (err) {
      if (this.isFailure(err)) this.onFailure();
      throw err;
    } finally {
      if (this.state === "half-open") this.halfOpenInFlight = false;
    }
  }

  private onSuccess(): void {
    this.failures = 0;
    this.state = "closed";
  }

  private onFailure(): void {
    this.failures += 1;
    if (this.state === "half-open" || this.failures >= this.failureThreshold) {
      this.state = "open";
      this.openedAt = Date.now();
      this.failures = 0;
    }
  }
}''',
        "The breaker protects the caller and gives the downstream time to recover. Half-open is the subtle state — allow exactly one trial request, not a full traffic slice.",
        "Counting 4xx as failures opens the circuit on client bugs. Shared breaker state per process means each pod learns independently — acceptable for interview; production may need a shared sliding window.",
        "Fail-fast while open is O(1) — saves thread pool and sockets during outages. Pair with bulkheads so one dependency cannot trip every breaker.",
        "Draw the state machine. How does a breaker interact with retries? Why not use a breaker on every internal call?",
    ),
    (
        "ex-redis-cache",
        "Redis-style cache wrapper (cache-aside)",
        "cache aside Redis wrapper TTL stampede TypeScript",
        "Build a <code>CacheAside&lt;T&gt;</code> with <code>get(key, loader)</code> using an injected KV store (get/set/del with TTL). Implement singleflight so concurrent misses for the same key call the loader once. Support JSON serialization and optional stale-on-error fallback.",
        '''type KV = {
  get(k: string): Promise<string | null>;
  set(k: string, v: string, ttlSec: number): Promise<void>;
  del(k: string): Promise<void>;
};

export class CacheAside<T> {
  constructor(private kv: KV, private ttlSec: number, private prefix = "c:") {}
  async get(key: string, loader: () => Promise<T>): Promise<T> {
    throw new Error("not implemented");
  }
  async invalidate(key: string): Promise<void> {}
}''',
        "Map of in-flight promises keyed by cache key — delete entry in <code>finally</code>. Version keys or wrap JSON. On loader failure after cache miss, do not negative-cache 500s unless intentional.",
        '''type KV = {
  get(k: string): Promise<string | null>;
  set(k: string, v: string, ttlSec: number): Promise<void>;
  del(k: string): Promise<void>;
};

export class CacheAside<T> {
  private inflight = new Map<string, Promise<T>>();

  constructor(
    private readonly kv: KV,
    private readonly ttlSec: number,
    private readonly prefix = "c:",
    private readonly serialize: (v: T) => string = JSON.stringify,
    private readonly deserialize: (s: string) => T = JSON.parse,
  ) {}

  private k(key: string) { return this.prefix + key; }

  async get(key: string, loader: () => Promise<T>): Promise<T> {
    const cached = await this.kv.get(this.k(key));
    if (cached != null) return this.deserialize(cached);

    const existing = this.inflight.get(key);
    if (existing) return existing;

    const p = (async () => {
      const value = await loader();
      await this.kv.set(this.k(key), this.serialize(value), this.ttlSec);
      return value;
    })();

    this.inflight.set(key, p);
    try {
      return await p;
    } finally {
      this.inflight.delete(key);
    }
  }

  async invalidate(key: string): Promise<void> {
    await this.kv.del(this.k(key));
  }
}''',
        "Cache-aside keeps the DB authoritative: app reads cache, on miss loads DB and writes cache. Singleflight prevents stampedes when a hot key expires.",
        "Stale cache after write if you forget invalidation — classic bug for issue detail pages. Serializing <code>undefined</code> or Dates without a reviver breaks reads. Redis down: decide fail-open (loader every time) vs fail-closed.",
        "Hit ratio drives win — monitor evictions and p99 loader latency. TTL jitter (<code>ttl ± 10%</code>) reduces synchronized expiry. Hot keys may need local L1 in-process LRU.",
        "How do you invalidate issue + board cache together? What is dog-pile / cache stampede at 10× traffic?",
    ),
    (
        "ex-job-queue",
        "In-memory job queue with ack and DLQ",
        "job queue in-memory ack dead letter retry TypeScript",
        "Implement an in-memory queue: enqueue jobs with id and payload; workers poll with visibility timeout; ack removes job; nack or timeout returns job for retry until <code>maxAttempts</code>, then move to DLQ. Expose events for metrics.",
        '''type Job<T> = { id: string; payload: T; attempts: number; visibleAt: number };

export class MemoryQueue<T> {
  enqueue(id: string, payload: T): void {}
  poll(): Job<T> | undefined { return undefined; }
  ack(id: string): void {}
  nack(id: string): void {}
  dlq: Job<T>[] = [];
}''',
        "Use a min-heap or sorted structure by <code>visibleAt</code> for efficient poll — for interview, scanning a Map is fine. Visibility timeout simulates SQS. Idempotent handlers still required.",
        '''type Job<T> = { id: string; payload: T; attempts: number; visibleAt: number; maxAttempts: number };

export class MemoryQueue<T> {
  private jobs = new Map<string, Job<T>>();
  dlq: Job<T>[] = [];

  constructor(
    private readonly visibilityMs = 30_000,
    private readonly maxAttempts = 5,
  ) {}

  enqueue(id: string, payload: T): void {
    if (this.jobs.has(id)) return; // dedupe by id
    this.jobs.set(id, {
      id, payload, attempts: 0, visibleAt: Date.now(), maxAttempts: this.maxAttempts,
    });
  }

  poll(now = Date.now()): Job<T> | undefined {
    for (const job of this.jobs.values()) {
      if (job.visibleAt <= now) {
        job.visibleAt = now + this.visibilityMs;
        return { ...job };
      }
    }
    return undefined;
  }

  ack(id: string): void {
    this.jobs.delete(id);
  }

  nack(id: string): void {
    const job = this.jobs.get(id);
    if (!job) return;
    job.attempts += 1;
    if (job.attempts >= job.maxAttempts) {
      this.jobs.delete(id);
      this.dlq.push(job);
      return;
    }
    job.visibleAt = Date.now() + this.visibilityMs;
  }
}''',
        "Visibility timeout gives at-least-once semantics: if the worker dies mid-handle, the job reappears. DLQ preserves poison messages for inspection instead of infinite spin.",
        "Process crash after handle but before ack → duplicate processing. In-memory queue vanishes on restart — fine for sketch, not production. No ordering guarantee across workers unless single partition.",
        "Poll scan is O(n) — production queues partition by key. Back-pressure: cap queue depth and reject enqueue with 503 when full.",
        "Compare to Kafka vs SQS for comment notifications. How do you replay DLQ safely?",
    ),
    (
        "ex-worker-pool",
        "Worker pool for CPU-bound tasks",
        "worker pool worker threads Piscina TypeScript Node",
        "Create a fixed-size worker pool that accepts tasks, queues when saturated, and runs work off the main thread via <code>worker_threads</code>. Support graceful drain on shutdown — finish in-flight, reject new tasks.",
        '''import { Worker } from "node:worker_threads";

type Task<T, R> = { payload: T; resolve(v: R): void; reject(e: unknown): void };

export class WorkerPool<T, R> {
  constructor(private size: number, private workerScript: string) {}
  run(payload: T): Promise<R> { return Promise.reject(new Error("not implemented")); }
  async shutdown(): Promise<void> {}
}''',
        "Each worker loads the script once; postMessage serializes payload. Maintain a task queue and idle worker list. On shutdown, set a flag, wait for active count → 0, then terminate workers.",
        '''import { Worker } from "node:worker_threads";

type Task<T, R> = { payload: T; resolve(v: R): void; reject(e: unknown): void };

export class WorkerPool<T, R> {
  private workers: Worker[] = [];
  private idle: Worker[] = [];
  private queue: Task<T, R>[] = [];
  private active = 0;
  private closed = false;

  constructor(private readonly size: number, private readonly workerScript: string) {
    for (let i = 0; i < size; i++) this.spawn();
  }

  private spawn(): void {
    const w = new Worker(this.workerScript);
    w.on("message", (msg: { ok: boolean; result?: R; error?: string }) => {
      this.active -= 1;
      const task = (w as Worker & { current?: Task<T, R> }).current;
      if (!task) return;
      (w as Worker & { current?: Task<T, R> }).current = undefined;
      if (msg.ok) task.resolve(msg.result as R);
      else task.reject(new Error(msg.error ?? "worker_error"));
      this.idle.push(w);
      this.pump();
    });
    this.idle.push(w);
  }

  run(payload: T): Promise<R> {
    if (this.closed) return Promise.reject(new Error("pool_closed"));
    return new Promise((resolve, reject) => {
      this.queue.push({ payload, resolve, reject });
      this.pump();
    });
  }

  private pump(): void {
    while (this.idle.length && this.queue.length) {
      const w = this.idle.pop()!;
      const task = this.queue.shift()!;
      (w as Worker & { current?: Task<T, R> }).current = task;
      this.active += 1;
      w.postMessage(task.payload);
    }
  }

  async shutdown(): Promise<void> {
    this.closed = true;
    while (this.active > 0) await new Promise((r) => setTimeout(r, 10));
    await Promise.all(this.workers.map((w) => w.terminate()));
    this.workers = [];
    this.idle = [];
  }
}''',
        "Worker pools isolate CPU-heavy work (PDF render, markdown parse, image resize) from the event loop. Pool size ≈ CPU cores — more threads add context-switch cost without throughput gain.",
        "Large postMessage payloads copy memory — prefer SharedArrayBuffer or file paths. Uncaught worker exceptions must reject the in-flight task and respawn worker. Shutdown race: reject queued tasks explicitly if you need stricter semantics.",
        "Throughput bounded by cores; queue depth adds latency under burst — expose queue length metric. For very small tasks, thread overhead may exceed benefit — batch in worker.",
        "When worker_threads vs cluster vs running a separate service? What blocks the event loop in Node?",
    ),
    (
        "ex-idempotent-api",
        "Idempotent POST handler",
        "idempotent API Idempotency-Key POST TypeScript Fastify",
        "Implement middleware + store for <code>Idempotency-Key</code> on POST. First request runs handler and caches status+body with TTL; duplicate key returns cached response without re-running side effects. Return 409 if same key arrives with different body hash.",
        '''type Stored = { statusCode: number; body: string; requestHash: string };

export interface IdempotencyStore {
  get(key: string): Promise<Stored | null>;
  put(key: string, value: Stored, ttlSec: number): Promise<boolean>;
}

export function idempotencyMiddleware(store: IdempotencyStore) {
  return async (req: { method: string; headers: Record<string, string | undefined>; body: unknown },
                reply: { status(n: number): { send(b: unknown): unknown } },
                handler: () => Promise<{ statusCode: number; body: unknown }>) => {
    return handler();
  };
}''',
        "Hash stable JSON body. Use <code>put</code> only if absent (SET NX) to win races. TTL 24h typical. Only apply to POST/PATCH that create billable side effects.",
        '''import { createHash } from "node:crypto";

type Stored = { statusCode: number; body: string; requestHash: string };

export interface IdempotencyStore {
  get(key: string): Promise<Stored | null>;
  putIfAbsent(key: string, value: Stored, ttlSec: number): Promise<boolean>;
}

function hashBody(body: unknown): string {
  return createHash("sha256").update(JSON.stringify(body ?? null)).digest("hex");
}

export function idempotencyMiddleware(store: IdempotencyStore, ttlSec = 86_400) {
  return async (
    req: { method: string; headers: Record<string, string | undefined>; body: unknown },
    handler: () => Promise<{ statusCode: number; body: unknown }>,
  ): Promise<{ statusCode: number; body: unknown; replayed: boolean }> => {
    const method = req.method.toUpperCase();
    if (method !== "POST" && method !== "PATCH") return { ...(await handler()), replayed: false };

    const key = req.headers["idempotency-key"] ?? req.headers["Idempotency-Key"];
    if (!key) return { ...(await handler()), replayed: false };

    const requestHash = hashBody(req.body);
    const existing = await store.get(key);
    if (existing) {
      if (existing.requestHash !== requestHash) {
        return { statusCode: 409, body: { error: "idempotency_key_reuse" }, replayed: true };
      }
      return { statusCode: existing.statusCode, body: JSON.parse(existing.body), replayed: true };
    }

    const result = await handler();
    const stored: Stored = {
      statusCode: result.statusCode,
      body: JSON.stringify(result.body),
      requestHash,
    };
    const won = await store.putIfAbsent(key, stored, ttlSec);
    if (!won) {
      const again = await store.get(key);
      if (again && again.requestHash === requestHash) {
        return { statusCode: again.statusCode, body: JSON.parse(again.body), replayed: true };
      }
      return { statusCode: 409, body: { error: "idempotency_conflict" }, replayed: true };
    }
    return { ...result, replayed: false };
  };
}''',
        "Idempotency keys turn at-least-once networks into exactly-once effect from the client’s perspective. Store response, not just a lock — clients retry to get the original 201 body.",
        "Store down on first attempt → client retries may double-create unless DB has unique constraint backup. Key scoped per tenant/user — global keys collide across customers. Caching 500 responses traps clients in failure.",
        "One Redis GET/SET per POST — negligible vs DB write. Prune keys by TTL; monitor cardinality per tenant for abuse.",
        "How is this different from a dedupe table in Postgres? What happens if handler succeeds but cache write fails?",
    ),
    (
        "ex-offset-pagination",
        "Offset/limit pagination API",
        "offset limit pagination SQL API TypeScript",
        "Build a handler for <code>GET /issues?project=PROJ&amp;offset=0&amp;limit=50&amp;sort=updated&amp;dir=desc</code> that validates params, caps limit at 100, returns <code>{ values, total, offset, limit, hasMore }</code>, and uses parameterized SQL with ORDER BY — no string-concatenated sort columns.",
        '''type Issue = { id: string; key: string; summary: string; updatedAt: string };

export async function listIssuesOffset(
  db: { query<T>(sql: string, params: unknown[]): Promise<{ rows: T[] }> },
  q: { project: string; offset: number; limit: number; sort: string; dir: "asc" | "desc" },
): Promise<{ values: Issue[]; total: number; offset: number; limit: number; hasMore: boolean }> {
  throw new Error("not implemented");
}''',
        "Allow-list sort columns map to SQL identifiers. Run COUNT(*) for total (or estimate for huge tables — mention trade-off). Clamp offset ≥ 0.",
        '''type Issue = { id: string; key: string; summary: string; updatedAt: string };

const SORT_COLS: Record<string, string> = {
  updated: "updated_at",
  created: "created_at",
  key: "issue_key",
};

export async function listIssuesOffset(
  db: { query<T>(sql: string, params: unknown[]): Promise<{ rows: T[] }> },
  q: { project: string; offset: number; limit: number; sort: string; dir: "asc" | "desc" },
): Promise<{ values: Issue[]; total: number; offset: number; limit: number; hasMore: boolean }> {
  const limit = Math.min(Math.max(q.limit, 1), 100);
  const offset = Math.max(q.offset, 0);
  const sortCol = SORT_COLS[q.sort] ?? SORT_COLS.updated;
  const dir = q.dir === "asc" ? "ASC" : "DESC";

  const countRes = await db.query<{ count: string }>(
    "SELECT COUNT(*)::text AS count FROM issues WHERE project_key = $1",
    [q.project],
  );
  const total = Number(countRes.rows[0]?.count ?? 0);

  const dataRes = await db.query<Issue>(
    `SELECT id, issue_key AS key, summary, updated_at AS "updatedAt"
     FROM issues WHERE project_key = $1
     ORDER BY ${sortCol} ${dir}, id ${dir}
     LIMIT $2 OFFSET $3`,
    [q.project, limit, offset],
  );

  return {
    values: dataRes.rows,
    total,
    offset,
    limit,
    hasMore: offset + dataRes.rows.length < total,
  };
}''',
        "Offset pagination is simple for admin UIs and shallow pages. Always tie-break sort with primary key so order is stable when timestamps collide.",
        "Deep offset scans get slow — OFFSET 1M is O(n). Concurrent inserts shift windows (duplicates/skips). Unvalidated sort allows SQL injection via column name.",
        "Index on <code>(project_key, updated_at DESC, id)</code> for the common case. COUNT(*) can be expensive — cache totals or cap max offset in public API.",
        "When does offset fail for Jira issue lists? How would you expose page numbers anyway?",
    ),
    (
        "ex-cursor-pagination",
        "Cursor (keyset) pagination API",
        "cursor keyset pagination encode decode TypeScript",
        "Implement cursor pagination for issues sorted by <code>(updated_at, id)</code> descending. Cursor encodes last-seen pair; query fetches rows strictly “before” cursor. Return opaque base64url cursor in <code>nextPage</code>. Reject tampered cursors.",
        '''type Issue = { id: string; updatedAt: string; summary: string };
type Page = { values: Issue[]; nextPage?: string };

export async function listIssuesCursor(
  db: { query<T>(sql: string, params: unknown[]): Promise<{ rows: T[] }> },
  project: string,
  limit: number,
  cursor?: string,
): Promise<Page> {
  throw new Error("not implemented");
}''',
        "Predicate: <code>(updated_at, id) &lt; ($cursorUpdated, $cursorId)</code> for DESC. Encode JSON cursor with HMAC or sign — interview: base64 JSON + validate shape. Limit default 50, max 100.",
        '''import { createHmac, timingSafeEqual } from "node:crypto";

type Issue = { id: string; updatedAt: string; summary: string };
type Page = { values: Issue[]; nextPage?: string };
type CursorPayload = { u: string; i: string };

const SECRET = process.env.CURSOR_SECRET ?? "dev-secret";

function sign(payload: CursorPayload): string {
  const body = Buffer.from(JSON.stringify(payload)).toString("base64url");
  const sig = createHmac("sha256", SECRET).update(body).digest("base64url");
  return `${body}.${sig}`;
}

function verify(token: string): CursorPayload | null {
  const [body, sig] = token.split(".");
  if (!body || !sig) return null;
  const expected = createHmac("sha256", SECRET).update(body).digest("base64url");
  const a = Buffer.from(sig);
  const b = Buffer.from(expected);
  if (a.length !== b.length || !timingSafeEqual(a, b)) return null;
  try {
    return JSON.parse(Buffer.from(body, "base64url").toString("utf8")) as CursorPayload;
  } catch {
    return null;
  }
}

export async function listIssuesCursor(
  db: { query<T>(sql: string, params: unknown[]): Promise<{ rows: T[] }> },
  project: string,
  limit: number,
  cursor?: string,
): Promise<Page> {
  const take = Math.min(Math.max(limit, 1), 100);
  const params: unknown[] = [project];
  let where = "WHERE project_key = $1";

  if (cursor) {
    const c = verify(cursor);
    if (!c) throw new Error("invalid_cursor");
    params.push(c.u, c.i);
    where += ` AND (updated_at, id) < ($${params.length - 1}::timestamptz, $${params.length}::uuid)`;
  }

  params.push(take + 1);
  const res = await db.query<Issue>(
    `SELECT id, updated_at AS "updatedAt", summary FROM issues
     ${where}
     ORDER BY updated_at DESC, id DESC
     LIMIT $${params.length}`,
    params,
  );

  const rows = res.rows;
  const hasMore = rows.length > take;
  const values = hasMore ? rows.slice(0, take) : rows;
  const last = values[values.length - 1];
  const nextPage = hasMore && last
    ? sign({ u: last.updatedAt, i: last.id })
    : undefined;

  return { values, nextPage };
}''',
        "Keyset pagination walks indexed sort keys — stable under concurrent writes unlike offset. Opaque signed cursors stop tampering and hide internal ids if needed.",
        "Sort key must be unique — always tie-break with id. Changing sort schema invalidates old cursors — version the cursor format. ASC vs DESC flips comparator — easy bug.",
        "Each page is an index range scan — constant time regardless of depth. Fetch <code>limit+1</code> to detect hasMore without COUNT.",
        "Why Atlassian APIs expose cursor for comments but admin export might use offset? How do you paginate in Elasticsearch?",
    ),
    (
        "ex-webhook-processor",
        "Webhook processor with signature verify",
        "webhook HMAC signature verify idempotent processor TypeScript",
        "Build a webhook ingress: verify HMAC-SHA256 signature header, persist event id for dedupe, enqueue async processing, return 200 quickly. Reject bad signature with 401; duplicate delivery id returns 200 without re-enqueue.",
        '''type EventStore = {
  seen(id: string): Promise<boolean>;
  mark(id: string, ttlSec: number): Promise<void>;
};
type Queue = { enqueue(id: string, payload: unknown): void };

export async function handleWebhook(
  rawBody: Buffer,
  headers: Record<string, string | undefined>,
  store: EventStore,
  queue: Queue,
  secret: string,
): Promise<{ status: number; body: unknown }> {
  throw new Error("not implemented");
}''',
        "Use timing-safe compare for signatures. Parse event id from JSON after verify. TTL on seen ids ≥ provider retry window (e.g. 72h). Never do heavy work before ack.",
        '''import { createHmac, timingSafeEqual } from "node:crypto";

type EventStore = {
  seen(id: string): Promise<boolean>;
  mark(id: string, ttlSec: number): Promise<void>;
};
type Queue = { enqueue(id: string, payload: unknown): void };

function verifySig(raw: Buffer, header: string | undefined, secret: string): boolean {
  if (!header?.startsWith("sha256=")) return false;
  const expected = createHmac("sha256", secret).update(raw).digest("hex");
  const got = header.slice("sha256=".length);
  const a = Buffer.from(got, "hex");
  const b = Buffer.from(expected, "hex");
  return a.length === b.length && timingSafeEqual(a, b);
}

export async function handleWebhook(
  rawBody: Buffer,
  headers: Record<string, string | undefined>,
  store: EventStore,
  queue: Queue,
  secret: string,
): Promise<{ status: number; body: unknown }> {
  const sig = headers["x-signature-256"] ?? headers["X-Signature-256"];
  if (!verifySig(rawBody, sig, secret)) {
    return { status: 401, body: { error: "invalid_signature" } };
  }

  const event = JSON.parse(rawBody.toString("utf8")) as { id: string; type: string; data: unknown };
  if (!event.id) return { status: 400, body: { error: "missing_event_id" } };

  if (await store.seen(event.id)) {
    return { status: 200, body: { ok: true, duplicate: true } };
  }

  await store.mark(event.id, 72 * 3600);
  queue.enqueue(event.id, event);
  return { status: 200, body: { ok: true } };
}''',
        "Webhooks are at-least-once — signature proves authenticity, id store proves dedupe. Fast 200 + async worker is the production pattern for payment and integration providers.",
        "Marking seen before enqueue loses event if queue write fails — production uses outbox or mark-after-enqueue with reconciler. Raw body must be preserved — re-parsing JSON changes whitespace and breaks HMAC.",
        "Verify + dedupe is O(1). Worker concurrency scales independently. Rate-limit ingress per sender IP.",
        "How do you rotate webhook secrets? What if processing fails after 200 — how does provider retry interact with your dedupe?",
    ),
    (
        "ex-notification-worker",
        "Notification worker with preferences and dedupe",
        "notification worker email in-app dedupe preferences TypeScript",
        "Implement a worker consuming <code>NotificationJob</code> events: check user prefs (email/in-app off), dedupe by <code>(userId, dedupeKey)</code> within 24h, fan out to channel senders, record metrics. Must be safe under duplicate jobs.",
        '''type NotificationJob = {
  userId: string;
  dedupeKey: string;
  template: string;
  data: Record<string, unknown>;
  channels: ("email" | "in-app")[];
};

export type Prefs = { email: boolean; "in-app": boolean };
export type Sender = (channel: "email" | "in-app", job: NotificationJob) => Promise<void>;

export async function processNotification(
  job: NotificationJob,
  getPrefs: (userId: string) => Promise<Prefs>,
  dedupeSeen: (key: string) => Promise<boolean>,
  markDedupe: (key: string, ttlSec: number) => Promise<boolean>,
  send: Sender,
): Promise<{ sent: string[]; skipped: string[] }> {
  throw new Error("not implemented");
}''',
        "<code>markDedupe</code> returns false if already seen — only then skip. Filter channels by prefs before send. Parallelize channel sends with <code>Promise.allSettled</code> and report partial failure.",
        '''type NotificationJob = {
  userId: string;
  dedupeKey: string;
  template: string;
  data: Record<string, unknown>;
  channels: ("email" | "in-app")[];
};

export type Prefs = { email: boolean; "in-app": boolean };
export type Sender = (channel: "email" | "in-app", job: NotificationJob) => Promise<void>;

export async function processNotification(
  job: NotificationJob,
  getPrefs: (userId: string) => Promise<Prefs>,
  dedupeSeen: (key: string) => Promise<boolean>,
  markDedupe: (key: string, ttlSec: number) => Promise<boolean>,
  send: Sender,
): Promise<{ sent: string[]; skipped: string[] }> {
  const dedupeId = `${job.userId}:${job.dedupeKey}`;
  if (await dedupeSeen(dedupeId)) {
    return { sent: [], skipped: job.channels.slice() };
  }
  const first = await markDedupe(dedupeId, 86_400);
  if (!first) return { sent: [], skipped: job.channels.slice() };

  const prefs = await getPrefs(job.userId);
  const sent: string[] = [];
  const skipped: string[] = [];

  await Promise.all(job.channels.map(async (ch) => {
    if (!prefs[ch]) { skipped.push(ch); return; }
    await send(ch, job);
    sent.push(ch);
  }));

  return { sent, skipped };
}''',
        "Assignment notifications fan out to thousands of watchers — async worker + prefs + dedupe prevents email storms when an issue churns status rapidly.",
        "Dedupe before prefs check blocks legitimate cross-channel first sends if key is too coarse. Email sender succeeds but in-app fails — job ack policy determines retry duplication. Prefs cache stale after user disables email.",
        "Batch SMTP or push vendor calls where possible. Dedupe store in Redis with SET NX — O(channels) per job.",
        "Design the full pipeline: event → queue → worker → SendGrid. How do you rate-limit outbound email per tenant?",
    ),
    (
        "ex-presign-upload",
        "File upload backend (pre-signed URL flow)",
        "presigned URL multipart upload S3 TypeScript Node",
        "Implement initiate/complete handlers: validate auth + size, create upload record, return pre-signed PUT URL(s) for direct client→object-store upload, complete multipart with ETags, enqueue virus-scan job. API never proxies file bytes.",
        '''type UploadRecord = {
  uploadId: string;
  tenantId: string;
  objectKey: string;
  status: "pending" | "complete" | "scanning";
  parts: { partNumber: number; etag: string }[];
};

export async function initiateUpload(
  input: { tenantId: string; filename: string; size: number; contentType: string },
  signer: (objectKey: string, contentType: string, ttlSec: number) => Promise<string>,
): Promise<{ uploadId: string; putUrl: string; objectKey: string }> {
  throw new Error("not implemented");
}

export async function completeUpload(
  uploadId: string,
  parts: { partNumber: number; etag: string }[],
  repo: { get(id: string): Promise<UploadRecord | null>; save(r: UploadRecord): Promise<void> },
  scanQueue: { enqueue(id: string): void },
): Promise<{ status: string }> {
  throw new Error("not implemented");
}''',
        "Object key = opaque uuid, not user filename. Max size check at initiate. TTL 15 min on presign. Status machine: pending → complete → scanning → ready.",
        '''import { randomUUID } from "node:crypto";

type UploadRecord = {
  uploadId: string;
  tenantId: string;
  objectKey: string;
  status: "pending" | "complete" | "scanning";
  parts: { partNumber: number; etag: string }[];
  contentType: string;
  size: number;
};

const MAX_BYTES = 5 * 1024 * 1024 * 1024; // 5 GiB sketch

export async function initiateUpload(
  input: { tenantId: string; filename: string; size: number; contentType: string },
  repo: { save(r: UploadRecord): Promise<void> },
  signer: (objectKey: string, contentType: string, ttlSec: number) => Promise<string>,
): Promise<{ uploadId: string; putUrl: string; objectKey: string }> {
  if (input.size <= 0 || input.size > MAX_BYTES) throw new Error("invalid_size");
  const uploadId = randomUUID();
  const objectKey = `tenants/${input.tenantId}/uploads/${uploadId}`;
  const record: UploadRecord = {
    uploadId, tenantId: input.tenantId, objectKey,
    status: "pending", parts: [], contentType: input.contentType, size: input.size,
  };
  await repo.save(record);
  const putUrl = await signer(objectKey, input.contentType, 900);
  return { uploadId, putUrl, objectKey };
}

export async function completeUpload(
  uploadId: string,
  parts: { partNumber: number; etag: string }[],
  repo: { get(id: string): Promise<UploadRecord | null>; save(r: UploadRecord): Promise<void> },
  scanQueue: { enqueue(id: string): void },
): Promise<{ status: string }> {
  const rec = await repo.get(uploadId);
  if (!rec || rec.status !== "pending") throw new Error("upload_not_found");
  if (!parts.length) throw new Error("missing_parts");
  rec.parts = parts.sort((a, b) => a.partNumber - b.partNumber);
  rec.status = "scanning";
  await repo.save(rec);
  scanQueue.enqueue(uploadId);
  return { status: rec.status };
}''',
        "Pre-signed URLs move bytes off the app tier — Node handles metadata and policy only. Multipart enables parallel client uploads and resume. Virus scan async before linking attachment to issue.",
        "Client completes without all parts → orphan objects — lifecycle rule cleans bucket. Presign TTL expiry mid-upload frustrates users — refresh part URLs endpoint. Trusting client-reported size without head-object check allows abuse.",
        "S3 scales horizontally; API stays O(1) per initiate/complete. Multipart threshold ~8–64 MiB per part balances parallelism and request count.",
        "Why not stream through Node? How does React uploader resume after network drop?",
    ),
    (
        "ex-distributed-counter",
        "Distributed counter (Redis-style INCR)",
        "distributed counter Redis INCR rate view count TypeScript",
        "Implement a counter service: <code>increment(key, delta)</code> and <code>get(key)</code> via injected store supporting atomic incr. Add optional flush-to-DB every N seconds for analytics. Handle hot keys by sharding counter across suffix keys.",
        '''type CounterStore = {
  incrBy(key: string, delta: number): Promise<number>;
  get(key: string): Promise<number>;
};

export class DistributedCounter {
  constructor(private store: CounterStore, private shards = 8) {}
  async increment(key: string, delta = 1): Promise<number> {
    throw new Error("not implemented");
  }
  async get(key: string): Promise<number> {
    throw new Error("not implemented");
  }
}''',
        "Pick shard with <code>hash(key) % shards</code>. Sum shards on read. For flush, periodic job reads and writes to Postgres — mention eventual consistency.",
        '''type CounterStore = {
  incrBy(key: string, delta: number): Promise<number>;
  get(key: string): Promise<number>;
};

function shardIndex(key: string, shards: number): number {
  let h = 0;
  for (let i = 0; i < key.length; i++) h = (h * 31 + key.charCodeAt(i)) >>> 0;
  return h % shards;
}

export class DistributedCounter {
  constructor(
    private readonly store: CounterStore,
    private readonly shards = 8,
  ) {}

  private shardKey(key: string, i: number) { return `${key}:s${i}`; }

  async increment(key: string, delta = 1): Promise<number> {
    const i = shardIndex(key, this.shards);
    return this.store.incrBy(this.shardKey(key, i), delta);
  }

  async get(key: string): Promise<number> {
    const parts = await Promise.all(
      Array.from({ length: this.shards }, (_, i) => this.store.get(this.shardKey(key, i))),
    );
    return parts.reduce((a, b) => a + b, 0);
  }
}''',
        "Redis INCR is atomic per key — sharding spreads hot-key write load (view counts on viral issue). Reads sum shards — slight race gives approximate total, acceptable for display metrics.",
        "Non-atomic multi-shard increment during read can drift — fine for views, wrong for billing. Flush job double-counts if not reset keys atomically — use GETSET or dedicated flush script.",
        "Write O(1) to one shard; read O(shards) — keep shard count modest (8–64). HyperLogLog alternative when exact count unnecessary.",
        "How is this different from a CRDT? When would you use Kafka aggregation instead of Redis counters?",
    ),
]


def nodejs() -> str:
    t_event = topic("node-event", "Event loop, async I/O, and what blocks", "Node event loop libuv async blocking worker threads", "Node.js", f'''
  <p><b>Mental model.</b> Node is single-threaded JavaScript on a multi-threaded libuv runtime. Your code runs on the <i>event loop</i>; libuv handles thread-pool I/O (fs, dns, some crypto) and OS async notifications (sockets). Throughput comes from non-blocking I/O, not from parallel JS.</p>
  {diagram("""Phases (simplified): timers → pending callbacks → idle/prepare → poll (I/O) → check → close
Request ──► epoll/kqueue ──► callback queued ──► event loop tick ──► your .then / handler""")}
  <p><b>What blocks the event loop (say in interview).</b></p>
  <ul class="tight">
    <li>CPU-heavy sync JS: JSON.parse of 50MB, regex catastrophic backtracking, tight loops</li>
    <li>Sync native calls: <code>bcrypt.hashSync</code>, large <code>fs.readFileSync</code>, <code>child_process.execSync</code></li>
    <li>Massive microtask chains starving the loop</li>
    <li>Not blocking: awaited network I/O, Postgres pool query, Redis — threads/pool work elsewhere</li>
  </ul>
  {code("typescript", '''// BAD — blocks every request on this pod
app.get("/report", (_req, res) => {
  const rows = db.querySync("SELECT * FROM issues"); // fictional sync driver
  res.send(JSON.stringify(rows));
});

// GOOD — yield during I/O
app.get("/report", async (_req, res) => {
  const rows = await pool.query("SELECT id, summary FROM issues LIMIT 500");
  res.send({ rows: rows.rows });
});''')}
  {callout("Senior line: “I’d profile with async_hooks / clinic.js before adding workers — most ‘Node is slow’ issues are sync CPU or N+1 I/O, not the event loop model itself.”", "good")}
''', "backendTopics")

    t_http = topic("node-http", "HTTP server — Express/Fastify patterns", "Express Fastify middleware routing TypeScript Node HTTP", "Node.js", f'''
  <p><b>Structure.</b> Thin controllers, domain services, repositories. Register routes once; inject dependencies (pool, redis, config) via factory or lightweight container — avoid global singletons in tests.</p>
  {code("typescript", '''import Fastify from "fastify";
import { healthRoutes } from "./routes/health";
import { issueRoutes } from "./routes/issues";
import { buildContainer } from "./di";

export async function buildApp() {
  const app = Fastify({ logger: true, requestIdHeader: "x-request-id" });
  const deps = await buildContainer();

  app.decorate("deps", deps);
  app.addHook("onRequest", async (req) => {
    req.log = req.log.child({ tenantId: req.headers["x-tenant-id"] });
  });

  await app.register(healthRoutes);
  await app.register(issueRoutes, { prefix: "/api/v1" });

  app.setErrorHandler((err, req, reply) => {
    const status = err.statusCode ?? 500;
    reply.status(status).send({
      error: err.code ?? "internal_error",
      message: status < 500 ? err.message : "Internal error",
      correlationId: req.id,
    });
  });

  return app;
}''')}
  <p><b>Connection pooling.</b> One <code>pg.Pool</code> per process — size ≈ <code>(DB_max_connections / pod_count) - margin</code>. Exhausting the pool looks like app deadlock; monitor <code>waitingCount</code>.</p>
  {code("typescript", '''import pg from "pg";

export const pool = new pg.Pool({
  connectionString: process.env.DATABASE_URL,
  max: Number(process.env.PG_POOL_SIZE ?? 10),
  idleTimeoutMillis: 30_000,
  connectionTimeoutMillis: 5_000,
});''')}
  {callout("Mistake: creating a new Pool per request — exhausts Postgres in minutes under load.", "warn")}
''', "backendTopics")

    t_streams = topic("node-streams", "Streams, backpressure, and large payloads", "Node streams backpressure pipeline transform", "Node.js", f'''
  <p><b>Streams</b> move data in chunks with backpressure — essential for exports, log tail, proxying attachments. Prefer piping to res; do not buffer entire 2GB export in RAM.</p>
  {code("typescript", '''import { pipeline } from "node:stream/promises";
import { createReadStream } from "node:fs";
import { gzip } from "node:zlib";

app.get("/export/:id", async (req, res) => {
  res.setHeader("Content-Type", "application/gzip");
  await pipeline(
    createReadStream(exportPath(req.params.id)),
    gzip(),
    res,
  );
});''')}
  <p><b>Async iteration</b> (<code>for await</code>) fits paginated DB reads into a CSV stream without loading all rows.</p>
''', "backendTopics")

    t_scale = topic("node-scale", "Worker threads, clustering, and multi-core", "worker threads cluster Node PM2 multi-core", "Node.js", f'''
  <p><b>cluster / PM2</b> — fork one process per CPU for HTTP accept throughput; shared nothing; sticky sessions rarely needed if JWT + Redis sessions. Each worker has its own pool — divide DB connections accordingly.</p>
  <p><b>worker_threads</b> — CPU-bound JS in isolation; not for every request. Pool size ≈ cores.</p>
  {diagram("""                    ┌─ worker 1 (event loop + pool)
  LB ──► Node host ───┼─ worker 2
                    └─ worker N
        CPU job ──► worker_threads pool (shared on host)""")}
  {code("typescript", '''import cluster from "node:cluster";
import os from "node:os";

if (cluster.isPrimary) {
  for (let i = 0; i < os.cpus().length; i++) cluster.fork();
  cluster.on("exit", (worker) => {
    console.warn("worker died", worker.process.pid);
    cluster.fork();
  });
} else {
  const app = await buildApp();
  await app.listen({ port: 3000, host: "0.0.0.0" });
}''')}
''', "backendTopics")

    t_shutdown = topic("node-shutdown", "Graceful shutdown and health checks", "graceful shutdown SIGTERM health liveness readiness Node", "Node.js", f'''
  <p><b>Health endpoints.</b></p>
  <ul class="tight">
    <li><code>/health/live</code> — process up (K8s liveness)</li>
    <li><code>/health/ready</code> — can serve traffic (DB ping, redis ping) — fail during shutdown</li>
  </ul>
  <p><b>Shutdown order (memorize).</b></p>
  <ol class="tight">
    <li>Receive SIGTERM → mark not-ready (fail readiness probe)</li>
    <li>Stop accepting new HTTP connections (<code>server.close()</code>)</li>
    <li>Drain in-flight requests (with timeout budget)</li>
    <li>Stop background job consumers / cron</li>
    <li>Flush metrics/logs</li>
    <li>Close pools (pg, redis) and exit</li>
  </ol>
  {code("typescript", '''export function wireGracefulShutdown(app: { close(): Promise<void> }, deps: {
  pool: { end(): Promise<void> };
  jobWorker: { stop(): Promise<void> };
}) {
  let shuttingDown = false;
  app.addHook("onRequest", async (_req, reply) => {
    if (shuttingDown) reply.code(503).send({ error: "shutting_down" });
  });

  const shutdown = async (signal: string) => {
    if (shuttingDown) return;
    shuttingDown = true;
    app.log.info({ signal }, "shutdown start");
    await app.close();
    await deps.jobWorker.stop();
    await deps.pool.end();
    process.exit(0);
  };

  process.on("SIGTERM", () => void shutdown("SIGTERM"));
  process.on("SIGINT", () => void shutdown("SIGINT"));
}''')}
  {callout("If you close the DB pool before HTTP drain, in-flight handlers throw — order matters.", "warn")}
''', "backendTopics")

    t_ops = topic("node-ops", "Config, DI, errors, logging, metrics, jobs", "config DI pino prometheus bullmq background jobs Node", "Node.js", f'''
  <p><b>Config.</b> Validate env at boot (zod/envalid) — fail fast. No <code>process.env</code> scattered in handlers.</p>
  <p><b>DI.</b> Factory builds pool, redis, repos, services. Tests swap fakes without mocking modules.</p>
  <p><b>Logging.</b> Structured JSON (pino) with <code>correlationId</code>, <code>tenantId</code>, <code>durationMs</code>. Log levels: error for action needed, warn for degraded, info for request lifecycle.</p>
  <p><b>Metrics.</b> Prometheus counters/histograms: <code>http_request_duration_seconds</code>, pool wait, queue lag, breaker state. RED method: rate, errors, duration.</p>
  <p><b>Background jobs.</b> BullMQ / SQS worker in same repo or separate deployable — never <code>setInterval</code> for critical work without leader election. Jobs idempotent; visibility timeout; DLQ.</p>
  {code("typescript", '''// Minimal DI container sketch
export async function buildContainer() {
  const config = loadConfig();
  const pool = new pg.Pool({ connectionString: config.databaseUrl, max: config.pgPoolSize });
  const redis = new Redis(config.redisUrl);
  const issueRepo = new IssueRepo(pool);
  const issueService = new IssueService(issueRepo, redis);
  return { config, pool, redis, issueService };
}''')}
  <p><b>Interview.</b> Sketch a Fastify service on a whiteboard: routes, health, config validation, pool, graceful shutdown, one async job consumer — that alone signals senior backend hygiene.</p>
''', "backendTopics")

    return f'''
<section class="block" id="nodejs" data-search="Node.js architecture event loop Fastify graceful shutdown" data-stype="Section" data-cat="backend">
  <p class="kicker">Backend</p>
  <h2 class="section-title">Node.js Architecture</h2>
  <p class="lede">Senior Node is not “JavaScript on a server” — it is event-driven I/O, explicit pooling, failure-aware shutdown, and knowing exactly what blocks the loop.</p>
  {t_event}{t_http}{t_streams}{t_scale}{t_shutdown}{t_ops}
</section>
'''


def exercises() -> str:
    cards = [
        _ex(eid, title, search, req, starter, hints, solution, explanation, failures, performance, followups)
        for eid, title, search, req, starter, hints, solution, explanation, failures, performance, followups in EX
    ]
    return f'''
<section class="block" id="exercises" data-search="Backend Node.js coding exercises token bucket circuit breaker" data-stype="Section" data-cat="backend">
  <p class="kicker">Implementation</p>
  <h2 class="section-title">Backend Exercises</h2>
  <p class="lede">Thirteen TypeScript/Node sketches aligned with Phase 3 days 23–25 and 41–42. Implement first, then reveal. No empty stubs in solutions — copy into a scratch file and test with node --experimental-strip-types or tsx.</p>
  {''.join(cards)}
</section>
'''
