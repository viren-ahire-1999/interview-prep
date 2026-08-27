import html as _html

def code(lang: str, src: str) -> str:
    return (
        f'<div class="code-block"><div class="code-head"><span>{lang}</span>'
        f'<button type="button" class="copy-btn">Copy</button></div>'
        f"<pre><code>{_html.escape(src)}</code></pre></div>"
    )


EX = [
    {
        "id": "ex-debounce", "name": "Implement debounce",
        "req": "debounce(fn, wait) returns a function that delays fn until wait ms have passed without another call. Include cancel() if you can.",
        "start": "function debounce<T extends (...a: any[]) => void>(fn: T, wait: number): T & { cancel(): void } {\n  // TODO\n}",
        "expect": "Rapid calls at t=0,10,20 with wait=50 → fn runs once around t=70 with the last args.",
        "hints": "Store a timer id. On each call, clearTimeout and setTimeout. Preserve this and args.",
        "cx": "O(1) per call besides the scheduled fn.",
        "follow": "Leading vs trailing. maxWait (lodash). React: cancel on unmount.",
        "sol": """function debounce<T extends (...a: any[]) => void>(fn: T, wait: number) {
  let t: ReturnType<typeof setTimeout> | undefined;
  const wrapped = function (this: unknown, ...args: Parameters<T>) {
    clearTimeout(t);
    t = setTimeout(() => fn.apply(this, args), wait);
  };
  wrapped.cancel = () => clearTimeout(t);
  return wrapped as T & { cancel(): void };
}""",
        "why": "Trailing debounce is a closure over timer + last this/args. Leading fires immediately then ignores until quiet.",
    },
    {
        "id": "ex-throttle", "name": "Implement throttle",
        "req": "throttle(fn, wait) ensures fn runs at most once per wait ms. Trailing call with last args is a nice extra.",
        "start": "function throttle<T extends (...a: any[]) => void>(fn: T, wait: number): T {\n  // TODO\n}",
        "expect": "Calls every 10ms for 300ms with wait=100 → about 3–4 invocations, not 30.",
        "hints": "Record lastRan. If now-lastRan >= wait, run. Else schedule a trailing timeout.",
        "cx": "O(1) per call.",
        "follow": "leading:false. Difference vs debounce for scroll.",
        "sol": """function throttle<T extends (...a: any[]) => void>(fn: T, wait: number) {
  let last = 0, t: ReturnType<typeof setTimeout> | undefined;
  return function (this: unknown, ...args: Parameters<T>) {
    const now = Date.now();
    const remaining = wait - (now - last);
    if (remaining <= 0) {
      clearTimeout(t); t = undefined;
      last = now; fn.apply(this, args);
    } else if (!t) {
      t = setTimeout(() => {
        last = Date.now(); t = undefined; fn.apply(this, args);
      }, remaining);
    }
  } as T;
}""",
        "why": "Throttle guarantees a maximum rate. Scroll/mousemove. Debounce waits for silence (search).",
    },
    {
        "id": "ex-once", "name": "Implement once()",
        "req": "once(fn) runs fn at most once and caches its return value for later calls.",
        "start": "function once<T extends (...a: any[]) => any>(fn: T): T {\n  // TODO\n}",
        "expect": "Second call does not re-run side effects; returns the first result.",
        "hints": "closed-over called flag + result. Decide whether later args are ignored (yes).",
        "cx": "O(1).",
        "follow": "once that resets. once per unique args (that's memoize).",
        "sol": """function once<T extends (...a: any[]) => any>(fn: T): T {
  let called = false, res: ReturnType<T>;
  return function (this: unknown, ...args: Parameters<T>) {
    if (!called) { called = true; res = fn.apply(this, args); }
    return res;
  } as T;
}""",
        "why": "Initialization guards. Be careful if fn throws — decide whether retry is allowed.",
    },
    {
        "id": "ex-memo", "name": "Implement memoize",
        "req": "memoize(fn) caches by a key derived from args. Default key = JSON.stringify(args).",
        "start": "function memoize<T extends (...a: any[]) => any>(fn: T, key = (...a: any[]) => JSON.stringify(a)): T {\n  // TODO\n}",
        "expect": "fib(40) with memoized recursion returns quickly. Same args hit the cache.",
        "hints": "Map<string, result>. Cache only successful returns unless you want to cache throws.",
        "cx": "O(1) extra per call after the first, plus key cost.",
        "follow": "When is JSON key wrong (object identity, undefined, order)? LRU bound. WeakMap for single object arg.",
        "sol": """function memoize<T extends (...a: any[]) => any>(
  fn: T,
  key = (...a: any[]) => JSON.stringify(a)
): T {
  const cache = new Map<string, ReturnType<T>>();
  return function (this: unknown, ...args: Parameters<T>) {
    const k = key(...args);
    if (cache.has(k)) return cache.get(k)!;
    const v = fn.apply(this, args);
    cache.set(k, v);
    return v;
  } as T;
}""",
        "why": "Memoization is incorrect when fn is not referentially transparent (Date.now, I/O, this-dependent without including this).",
    },
    {
        "id": "ex-curry", "name": "Implement curry",
        "req": "curry(fn) lets you call fn(a)(b)(c) or fn(a,b,c) until arity is met (fn.length).",
        "start": "function curry<T extends (...a: any[]) => any>(fn: T) {\n  // TODO\n}",
        "expect": "const add = (a,b,c)=>a+b+c; curry(add)(1)(2)(3)===6; curry(add)(1,2)(3)===6.",
        "hints": "Return a function that accumulates args until args.length >= fn.length.",
        "cx": "O(arity) allocations.",
        "follow": "Default params break fn.length. Rest params. Placeholders (_).",
        "sol": """function curry(fn: Function) {
  const go = (...acc: unknown[]) =>
    acc.length >= fn.length
      ? fn(...acc)
      : (...more: unknown[]) => go(...acc, ...more);
  return go;
}""",
        "why": "Partial application for React event handlers (id) => () => remove(id) is often clearer than a generic curry.",
    },
    {
        "id": "ex-clone", "name": "Deep clone (acyclic)",
        "req": "deepClone a plain JSON-like value: objects, arrays, primitives. Document what you skip (functions, Date, cycles).",
        "start": "function deepClone<T>(v: T): T {\n  // TODO\n}",
        "expect": "Mutating clone.nested does not change original. Arrays stay arrays.",
        "hints": "Array.isArray first, then object. Recurse. structuredClone is the platform answer.",
        "cx": "O(n) nodes.",
        "follow": "Cycles (WeakMap). Date, Map, Set. Why JSON fails.",
        "sol": """function deepClone<T>(v: T): T {
  if (v === null || typeof v !== "object") return v;
  if (Array.isArray(v)) return v.map((x) => deepClone(x)) as T;
  const out: Record<string, unknown> = {};
  for (const [k, val] of Object.entries(v as object)) out[k] = deepClone(val);
  return out as T;
}""",
        "why": "Interviewers want you to name structuredClone and JSON limits, then write a simple recursive clone.",
    },
    {
        "id": "ex-flatten", "name": "Flatten an array",
        "req": "flatten(arr, depth = Infinity) like Array.prototype.flat.",
        "start": "function flatten(arr: unknown[], depth = Infinity): unknown[] {\n  // TODO\n}",
        "expect": "[1,[2,[3]],4] → [1,2,3,4] at Infinity; depth 1 → [1,2,[3],4].",
        "hints": "Reduce + concat recurse. Or iterative stack.",
        "cx": "O(n) output size.",
        "follow": "flatten object values. Don't flatten typed arrays unless asked.",
        "sol": """function flatten(arr: unknown[], depth = Infinity): unknown[] {
  if (depth < 1) return arr.slice();
  const out: unknown[] = [];
  for (const x of arr) {
    if (Array.isArray(x)) out.push(...flatten(x, depth - 1));
    else out.push(x);
  }
  return out;
}""",
        "why": "Iterative vs recursive is a good complexity/stack discussion.",
    },
    {
        "id": "ex-promise-all", "name": "Implement Promise.all",
        "req": "promiseAll(iterable) fulfills with an array in input order, rejects on first reject. Empty → [].",
        "start": "function promiseAll<T>(items: (T | Promise<T>)[]): Promise<T[]> {\n  // TODO\n}",
        "expect": "Order preserved even if the last promise settles first. Empty array fulfills immediately.",
        "hints": "Counter of remaining. Wrap each with Promise.resolve. Do not use the real Promise.all.",
        "cx": "O(n) space for the result array.",
        "follow": "allSettled. Concurrency limiter.",
        "sol": """function promiseAll<T>(items: (T | Promise<T>)[]): Promise<T[]> {
  return new Promise((resolve, reject) => {
    const list = [...items];
    if (!list.length) { resolve([]); return; }
    const out: T[] = Array(list.length);
    let left = list.length;
    list.forEach((item, i) => {
      Promise.resolve(item).then((v) => {
        out[i] = v;
        if (--left === 0) resolve(out);
      }, reject);
    });
  });
}""",
        "why": "The index write is the whole trick. forEach + leftover count.",
    },
    {
        "id": "ex-mini-promise", "name": "Simplified Promise",
        "req": "MiniPromise with then and a constructor (executor). Support resolve with a value (not thenable chaining if you need to cut scope).",
        "start": "class MiniPromise {\n  constructor(exec: (res: (v: unknown) => void, rej: (e: unknown) => void) => void) {}\n  then(onF?: (v: unknown) => unknown, onR?: (e: unknown) => unknown): MiniPromise { throw 0; }\n}",
        "expect": "new MiniPromise((r)=>r(1)).then(console.log) logs 1 as a microtask. Then is chainable at a basic level.",
        "hints": "State pending|fulfilled|rejected. Queue reactions. Flush via queueMicrotask. then always returns a new MiniPromise.",
        "cx": "Each then is O(1) enqueue.",
        "follow": "Thenables. catch. finally. Unhandled rejection.",
        "sol": """type Handler = { onF?: (v: unknown) => unknown; onR?: (e: unknown) => unknown; resolve: (v: unknown) => void; reject: (e: unknown) => void };
class MiniPromise {
  private state: "pending" | "fulfilled" | "rejected" = "pending";
  private value: unknown;
  private q: Handler[] = [];
  constructor(exec: (res: (v: unknown) => void, rej: (e: unknown) => void) => void) {
    const settle = (st: "fulfilled" | "rejected", v: unknown) => {
      if (this.state !== "pending") return;
      this.state = st; this.value = v;
      queueMicrotask(() => this.flush());
    };
    try { exec((v) => settle("fulfilled", v), (e) => settle("rejected", e)); }
    catch (e) { settle("rejected", e); }
  }
  then(onF?: (v: unknown) => unknown, onR?: (e: unknown) => unknown) {
    return new MiniPromise((resolve, reject) => {
      this.q.push({ onF, onR, resolve, reject });
      if (this.state !== "pending") queueMicrotask(() => this.flush());
    });
  }
  private flush() {
    if (this.state === "pending") return;
    const jobs = this.q.splice(0);
    for (const h of jobs) {
      const fn = this.state === "fulfilled" ? h.onF : h.onR;
      try {
        if (!fn) (this.state === "fulfilled" ? h.resolve : h.reject)(this.value);
        else h.resolve(fn(this.value));
      } catch (e) { h.reject(e); }
    }
  }
}""",
        "why": "You are proving you understand jobs, immutability after settle, and that then always returns a new promise.",
    },
    {
        "id": "ex-emitter", "name": "Event emitter",
        "req": "on, off, emit, once. emit should snapshot listeners so off during emit is safe.",
        "start": "class Emitter {\n  on(ev: string, fn: Function) {}\n  off(ev: string, fn: Function) {}\n  emit(ev: string, ...args: unknown[]) {}\n}",
        "expect": "on('x', fn); emit('x', 1) calls fn(1). off removes. once fires a single time.",
        "hints": "Map<string, Function[]>. slice() before iterate.",
        "cx": "emit O(listeners).",
        "follow": "Wildcard events. Error in one listener (should others run?).",
        "sol": """class Emitter {
  private m = new Map<string, Function[]>();
  on(ev: string, fn: Function) {
    const a = this.m.get(ev) ?? [];
    a.push(fn); this.m.set(ev, a);
    return () => this.off(ev, fn);
  }
  off(ev: string, fn: Function) {
    const a = this.m.get(ev); if (!a) return;
    this.m.set(ev, a.filter((f) => f !== fn));
  }
  once(ev: string, fn: Function) {
    const wrap = (...a: unknown[]) => { this.off(ev, wrap); fn(...a); };
    this.on(ev, wrap);
  }
  emit(ev: string, ...args: unknown[]) {
    for (const fn of (this.m.get(ev) ?? []).slice()) fn(...args);
  }
}""",
        "why": "Pub/sub vs callbacks: many subscribers, lifecycle off, avoid tight coupling. Snapshot prevents skip/double bugs.",
    },
    {
        "id": "ex-lru", "name": "LRU cache",
        "req": "capacity n. get(key) and put(key,val) O(1). Evict least recently used on overflow.",
        "start": "class LRU {\n  constructor(private cap: number) {}\n  get(k: string): number | undefined { return; }\n  put(k: string, v: number) {}\n}",
        "expect": "cap 2: put a,b,c evicts a. get(b) then put d evicts c if b was refreshed.",
        "hints": "Map insertion order in JS is LRU-friendly: delete+set moves to end. Evict map.keys().next().",
        "cx": "O(1) average get/put.",
        "follow": "TTL. Persistence. Why Map not object (order + any keys).",
        "sol": """class LRU {
  private map = new Map<string, number>();
  constructor(private cap: number) {}
  get(k: string) {
    if (!this.map.has(k)) return undefined;
    const v = this.map.get(k)!;
    this.map.delete(k); this.map.set(k, v);
    return v;
  }
  put(k: string, v: number) {
    if (this.map.has(k)) this.map.delete(k);
    this.map.set(k, v);
    if (this.map.size > this.cap) this.map.delete(this.map.keys().next().value!);
  }
}""",
        "why": "Frontend-adjacent: image caches, parsed module caches, in-memory API caches. Interviewers love Map order.",
    },
    {
        "id": "ex-retry", "name": "Retry with exponential backoff",
        "req": "retry(fn, { retries, baseMs }) calls async fn, waits base*2^attempt on fail, throws last error.",
        "start": "async function retry<T>(fn: () => Promise<T>, opts = { retries: 3, baseMs: 100 }): Promise<T> {\n  // TODO\n}",
        "expect": "fn fails twice then succeeds → three calls, delays ~100 and ~200ms.",
        "hints": "for loop try/catch. await sleep. jitter is a follow-up (avoid thundering herd).",
        "cx": "O(retries) attempts.",
        "follow": "AbortSignal. Retry only 429/5xx. Full jitter.",
        "sol": """const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
async function retry<T>(fn: () => Promise<T>, opts = { retries: 3, baseMs: 100 }): Promise<T> {
  let last: unknown;
  for (let i = 0; i <= opts.retries; i++) {
    try { return await fn(); }
    catch (e) {
      last = e;
      if (i === opts.retries) break;
      await sleep(opts.baseMs * 2 ** i);
    }
  }
  throw last;
}""",
        "why": "Production fetch to Jira/Confluence-style APIs. Seniors mention jitter and idempotency.",
    },
    {
        "id": "ex-limiter", "name": "Concurrency limiter",
        "req": "limit(n) returns a function wrap(task) that runs at most n tasks at once; the rest queue.",
        "start": "function limit(n: number) {\n  return function <T>(task: () => Promise<T>): Promise<T> {\n    // TODO\n  };\n}",
        "expect": "n=2, five tasks of 50ms → ~150ms total, never 3 running.",
        "hints": "active count + queue of resolve starters. After each finish, dequeue.",
        "cx": "O(1) extra per task besides the queue.",
        "follow": "Fairness. Priority. Abort queued work.",
        "sol": """function limit(n: number) {
  let active = 0;
  const q: (() => void)[] = [];
  const next = () => { active--; q.shift()?.(); };
  return function <T>(task: () => Promise<T>): Promise<T> {
    return new Promise<T>((resolve, reject) => {
      const run = () => {
        active++;
        task().then(resolve, reject).finally(next);
      };
      if (active < n) run();
      else q.push(run);
    });
  };
}""",
        "why": "Browsers limit HTTP/2 streams; you still want app-level limits for fan-out fetches. Pair with Promise.all on the wrapped tasks.",
    },
]


def exercises() -> str:
    cards = []
    for e in EX:
        cards.append(f'''
<article class="ex" id="{e["id"]}" data-search="{e["name"]}" data-stype="JS exercise">
  <h3>{e["name"]}</h3>
  <p><b>Requirements.</b> {e["req"]}</p>
  <p><b>Starter.</b></p>
  {code("TypeScript", e["start"])}
  <p><b>Expected behavior.</b> {e["expect"]}</p>
  <p><b>Hints.</b> {e["hints"]}</p>
  <p><button type="button" class="toggle-btn" data-toggle="{e["id"]}-sol">Solution</button>
     <button type="button" class="toggle-btn" data-complete="jsTopics" data-cid="{e["id"]}">Mark complete</button></p>
  <div class="reveal" id="{e["id"]}-sol">
    {code("TypeScript", e["sol"])}
    <p><b>Explanation.</b> {e["why"]}</p>
    <p><b>Complexity.</b> {e["cx"]}</p>
    <p><b>Follow-up interview questions.</b> {e["follow"]}</p>
  </div>
</article>''')
    return f'''
<section class="block" id="exercises" data-search="JavaScript coding exercises debounce throttle" data-stype="Section">
  <p class="kicker">Hands-on</p>
  <h2 class="section-title">JavaScript Coding Exercises</h2>
  <p class="lede">These show up in senior frontend / full-stack screens as often as Two Sum. Implement from the starter without peeking. Then compare. Complexity is usually secondary to API design and edge cases — say both.</p>
  {''.join(cards)}
</section>
'''
