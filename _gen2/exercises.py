from util import code


EX = [
    ("ex-ac", "Debounced autocomplete",
     "Input + listbox. Debounce 150ms. Abort in-flight. Keyboard. a11y combobox.",
     "function Autocomplete({ search }: { search: (q: string, s: AbortSignal) => Promise<string[]> }) { return null; }",
     "n/a network in this file — inject search.",
     "Type, wait, see options; arrow/enter; abort on change.",
     "AbortController + generation; debounce timer cleanup.",
     '''function Autocomplete({ search }: { search: (q: string, s: AbortSignal) => Promise<string[]> }) {
  const [q, setQ] = useState("");
  const [items, setItems] = useState<string[]>([]);
  const [open, setOpen] = useState(false);
  useEffect(() => {
    const ac = new AbortController();
    const t = setTimeout(async () => {
      if (!q) { setItems([]); return; }
      try { setItems(await search(q, ac.signal)); setOpen(true); } catch (e) { if ((e as any).name !== "AbortError") throw e; }
    }, 150);
    return () => { clearTimeout(t); ac.abort(); };
  }, [q, search]);
  return (
    <div>
      <input role="combobox" aria-expanded={open} aria-controls="ac-list" value={q} onChange={(e) => setQ(e.target.value)} />
      <ul id="ac-list" role="listbox">{items.map((it) => <li key={it} role="option">{it}</li>)}</ul>
    </div>
  );
}''',
     "Debounce the network, not the painted input. Announce result count.",
     "activedescendant, highlight, recents."),
    ("ex-inf", "Infinite scroll list",
     "Cursor pages, sentinel IntersectionObserver, loading/error, no dup keys.",
     "function Infinite({ fetchPage }: { fetchPage: (c: string | null) => Promise<{ items: {id:string}[]; next: string | null }> }) { return null; }",
     "Page size 20.",
     "Scroll loads next; stop at null cursor.",
     "Guard inFlight; observe last element.",
     '''function Infinite({ fetchPage }: any) {
  const [items, setItems] = useState<any[]>([]);
  const [cursor, setCursor] = useState<string | null>(null);
  const [done, setDone] = useState(false);
  const load = useRef(false);
  const more = async () => {
    if (load.current || done) return;
    load.current = true;
    const res = await fetchPage(cursor);
    setItems((x) => [...x, ...res.items]);
    setCursor(res.next); setDone(!res.next); load.current = false;
  };
  useEffect(() => { more(); }, []);
  return <ul>{items.map((i) => <li key={i.id}>{i.id}</li>)}{!done && <li ref={(el) => { /* IO on el -> more */ }} />}</ul>;
}''',
     "Virtualize if items stay mounted forever. Memory after 20 screens.",
     "Load more button for a11y."),
    ("ex-virt", "Virtualized list",
     "Fixed row height. Render visible + overscan. aria-rowcount.",
     "function VList({ n, row }: { n: number; row: (i: number) => React.ReactNode }) { return null; }",
     "Row height 32, overscan 5.",
     "Only ~viewport/32 + 10 nodes in DOM for n=20000.",
     "scrollTop / h = start index.",
     '''function VList({ n, row }: { n: number; row: (i: number) => React.ReactNode }) {
  const h = 32, oh = 5, [st, setSt] = useState(0);
  const vh = 400;
  const start = Math.max(0, Math.floor(st / h) - oh);
  const end = Math.min(n, Math.ceil((st + vh) / h) + oh);
  return (
    <div style={{ height: vh, overflow: "auto" }} onScroll={(e) => setSt(e.currentTarget.scrollTop)} role="grid" aria-rowcount={n}>
      <div style={{ height: n * h, position: "relative" }}>
        {Array.from({ length: end - start }, (_, k) => (
          <div key={start + k} style={{ position: "absolute", top: (start + k) * h, height: h }}>{row(start + k)}</div>
        ))}
      </div>
    </div>
  );
}''',
     "Variable height is a different algorithm (measured cache).",
     "scrollToIndex, a11y, dynamic height."),
    ("ex-modal", "Reusable accessible modal",
     "Focus trap, restore, escape, backdrop, labelled title.",
     "function Modal({ open, onClose, title, children }: any) { return null; }",
     "Must work without a library.",
     "Tab cycles; escape closes; focus returns.",
     "Save activeElement on open.",
     '''function Modal({ open, onClose, title, children }: any) {
  const ref = useRef<HTMLDivElement>(null);
  const prev = useRef<HTMLElement | null>(null);
  useEffect(() => {
    if (!open) return;
    prev.current = document.activeElement as HTMLElement;
    const el = ref.current; el?.querySelector<HTMLElement>("button, [href], input")?.focus();
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", onKey);
    return () => { document.removeEventListener("keydown", onKey); prev.current?.focus(); };
  }, [open, onClose]);
  if (!open) return null;
  return (
    <div className="backdrop" onClick={onClose}>
      <div role="dialog" aria-modal="true" aria-label={title} ref={ref} onClick={(e) => e.stopPropagation()}>
        <h2>{title}</h2>{children}<button type="button" onClick={onClose}>Close</button>
      </div>
    </div>
  );
}''',
     "One primitive for the whole app. Full trap needs tab wrap.",
     "Nested dialogs, scroll lock."),
    ("ex-table", "Sortable data table (URL sort)",
     "Columns, sort in search params, server fetch key includes sort.",
     "function Table({ rows, onSort }: any) { return null; }",
     "Don’t sort 20k on client unless asked.",
     "Click header toggles sort; URL updates.",
     "Keep sort in URL as source of truth.",
     '''function useSort() {
  const [sp, setSp] = useSearchParams();
  const sort = sp.get("sort") ?? "name";
  const dir = sp.get("dir") ?? "asc";
  const toggle = (col: string) => {
    const next = sort === col && dir === "asc" ? "desc" : "asc";
    setSp({ sort: col, dir: next });
  };
  return { sort, dir, toggle };
}''',
     "Virtualize body separately. Don’t lose sort on refresh.",
     "Multi-sort, column picker."),
    ("ex-upload", "Chunked uploader (sketch)",
     "Split file, PUT parts with concurrency 3, persist progress, resume.",
     "async function upload(file: File, api: any) {}",
     "Part 5MB.",
     "Refresh mid-upload resumes remaining parts.",
     "IDB map part->etag; complete at end.",
     '''async function upload(file: File, api: any) {
  const size = 5 * 1024 * 1024;
  const id = await api.init(file.name, file.size);
  const parts = Math.ceil(file.size / size);
  const limit = 3; let active = 0; const q: (() => void)[] = [];
  const run = (fn: () => Promise<void>) => new Promise<void>((res, rej) => {
    const start = () => { active++; fn().then(res, rej).finally(() => { active--; q.shift()?.(); }); };
    if (active < limit) start(); else q.push(start);
  });
  await Promise.all(Array.from({ length: parts }, (_, i) => run(async () => {
    const blob = file.slice(i * size, (i + 1) * size);
    const etag = await api.putPart(id, i, blob);
    await idb.set(`${id}:${i}`, etag);
  })));
  await api.complete(id);
}''',
     "Hash in a worker; don’t block UI. Preview SVG sandboxed.",
     "Pause, checksum, virus scan UX."),
    ("ex-retry", "Retryable API client",
     "GET retries with jitter. POST only if idempotencyKey provided.",
     "function createClient(base: string) { return { get(p: string) {}, post(p: string, b: unknown, key?: string) {} }; }",
     "Max 3 retries on 502/503/429.",
     "GET /x fails twice then works; POST without key does not retry.",
     "Respect Retry-After. Abort signal through.",
     '''async function withRetry(fn: () => Promise<Response>, tries = 3) {
  let last: unknown;
  for (let i = 0; i < tries; i++) {
    const res = await fn();
    if (res.ok || (res.status < 500 && res.status !== 429)) return res;
    last = res; await new Promise((r) => setTimeout(r, 200 * 2 ** i + Math.random() * 100));
  }
  throw last;
}''',
     "POST without idempotency must not auto-retry.",
     "401 refresh queue."),
    ("ex-cache", "In-memory request cache + dedupe",
     "get(key, fetcher): share in-flight; TTL stale.",
     "class QueryCache { get<T>(key: string, fetcher: () => Promise<T>): Promise<T> { throw 0; } }",
     "TTL 10s.",
     "Two parallel get('issue:1') → one fetch.",
     "Map key → { data, exp, inflight }.",
     '''class QueryCache {
  private m = new Map<string, { data?: unknown; exp: number; inflight?: Promise<unknown> }>();
  get<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
    const now = Date.now(); const hit = this.m.get(key);
    if (hit?.data !== undefined && hit.exp > now) return Promise.resolve(hit.data as T);
    if (hit?.inflight) return hit.inflight as Promise<T>;
    const inflight = fetcher().then((data) => { this.m.set(key, { data, exp: now + 10_000 }); return data; });
    this.m.set(key, { exp: 0, inflight });
    return inflight;
  }
}''',
     "This is TanStack Query in a napkin. Add abort and invalidation next.",
     "gc, stale-while-revalidate."),
    ("ex-emitter", "Typed event emitter",
     "on/off/emit; snapshot listeners; once.",
     "class Emitter<T extends Record<string, unknown[]>> {}",
     "Safe off during emit.",
     "on + emit + off works; once fires once.",
     "slice() before iterate.",
     '''class Emitter {
  private m = new Map<string, Function[]>();
  on(e: string, f: Function) { const a = this.m.get(e) ?? []; a.push(f); this.m.set(e, a); return () => this.off(e, f); }
  off(e: string, f: Function) { this.m.set(e, (this.m.get(e) ?? []).filter((x) => x !== f)); }
  emit(e: string, ...args: unknown[]) { for (const f of (this.m.get(e) ?? []).slice()) f(...args); }
}''',
     "Used for plugin bridges and telemetry. Don’t share a god-bus across features.",
     "Wildcard, error isolation."),
    ("ex-toast", "Notification / toast system",
     "Queue, max 3 visible, a11y polite, dismiss, no steal focus.",
     "const toast = { success(m: string) {} };",
     "Stack from a module store.",
     "Three toasts then a fourth waits.",
     "IDs; timers; portal.",
     '''type T = { id: string; msg: string };
let items: T[] = []; const subs = new Set<() => void>();
export const toast = {
  success(msg: string) { items = [...items, { id: crypto.randomUUID(), msg }].slice(-3); subs.forEach((s) => s()); },
  subscribe(s: () => void) { subs.add(s); return () => subs.delete(s); },
  get() { return items; },
};''',
     "useSyncExternalStore in the viewport. aria-live=polite on the region.",
     "Action toasts, persist errors."),
    ("ex-flag", "useFlag hook",
     "Typed flags from a bootstrap map; default if missing; no world rerender.",
     "function useFlag(name: 'ai-issue' | 'new-board'): boolean { return false; }",
     "Flags from FlagContext that is a stable map.",
     "Gate a button; missing key → default false.",
     "Context holds Record; hook selects one key — still rerenders all useFlag unless selector store.",
     '''const FlagCtx = createContext<Record<string, boolean>>({});
export function useFlag(name: string, fallback = false) {
  return useContext(FlagCtx)[name] ?? fallback;
}
// Better: zustand flags.select(name) to avoid broadcast.''',
     "Flags ≠ permissions. Avoid flicker with bootstrap-before-paint.",
     "Experiments, exposure events."),
    ("ex-perm", "Permission gate",
     "useCan(resource, action); disable + reason; server still enforces.",
     "function Gate({ can, children, reason }: any) { return null; }",
     "Batch caps from API.",
     "Unauthorized submit hidden/disabled with name.",
     "Don’t only hide — announce why if focused.",
     '''function Gate({ allowed, reason, children }: { allowed: boolean; reason?: string; children: React.ReactElement }) {
  if (allowed) return children;
  return React.cloneElement(children, { disabled: true, "aria-disabled": true, title: reason });
}''',
     "403 UX if they still call the API. Batch /caps.",
     "Field-level vs view-level."),
    ("ex-form", "Form architecture (RHF-like sketch)",
     "Uncontrolled defaults, submit once, field errors, a11y describedby.",
     "function useForm<T>(opts: { defaultValues: T; onSubmit: (v: T) => Promise<void> }) { return {}; }",
     "Don’t rerender the app per keystroke.",
     "Submit shows field errors; focus first error.",
     "Refs or tiny field store; not one setState per key.",
     '''function useForm<T extends Record<string, string>>(opts: { defaultValues: T; onSubmit: (v: T) => Promise<void> }) {
  const refs = useRef(opts.defaultValues);
  const [errors, setErrors] = useState<Partial<T>>({});
  return {
    register: (name: keyof T) => ({ name, defaultValue: opts.defaultValues[name], "aria-invalid": !!errors[name],
      "aria-describedby": errors[name] ? `${String(name)}-err` : undefined, onChange: (e: any) => { refs.current[name] = e.target.value; } }),
    errors,
    handleSubmit: async (e: React.FormEvent) => { e.preventDefault(); await opts.onSubmit(refs.current); },
  };
}''',
     "Uncontrolled scales. Zod at submit. Announce errors.",
     "Wizard, dirty tracking."),
    ("ex-dsbtn", "Design-system Button",
     "Variants via tokens, asChild composition, disabled, loading, a11y name.",
     "function Button(props: React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'subtle' }) { return null; }",
     "No boolean soup.",
     "Keyboard, name, loading disables.",
     "Never render a div. Compose with Slot if asChild.",
     '''function Button({ variant = "primary", loading, children, disabled, ...rest }: any) {
  return (
    <button type="button" className={`btn btn-${variant}`} disabled={disabled || loading} aria-busy={loading} {...rest}>
      {loading ? <span className="sr-only">Loading</span> : null}{children}
    </button>
  );
}''',
     "Tokens for color/space. Visual tests. Breaking a variant is a major.",
     "Icon-only needs aria-label."),
    ("ex-rt", "Realtime notification UI",
     "Subscribe, dedupe by id, badge, center list virtualized.",
     "function useInbox() { return { items: [], badge: 0 }; }",
     "WS + REST catch-up.",
     "Dup events don’t double badge.",
     "Set of ids; reconnect catch-up since timestamp.",
     '''function useInbox(ws: { on: Function; off: Function }) {
  const [items, setItems] = useState<{ id: string }[]>([]);
  useEffect(() => {
    const seen = new Set<string>();
    const on = (n: { id: string }) => {
      if (seen.has(n.id)) return; seen.add(n.id);
      setItems((x) => [n, ...x].slice(0, 50));
    };
    ws.on("n", on); return () => ws.off("n", on);
  }, [ws]);
  return { items, badge: items.length };
}''',
     "Don’t put toasts in Redux forever. polite live region. Catch-up REST.",
     "Read/unread, mute."),
]


def exercises() -> str:
    cards = []
    for eid, name, req, start, cons, expect, hints, sol, expl, follow in EX:
        cards.append(f'''
<article class="ex" id="{eid}" data-search="{name}" data-stype="Exercise" data-cat="architecture">
  <h3>{name}</h3>
  <p><b>Requirements.</b> {req}</p>
  <p><b>Starter.</b></p>{code("TypeScript", start)}
  <p><b>Constraints.</b> {cons}</p>
  <p><b>Expected.</b> {expect}</p>
  <p><b>Hints.</b> {hints}</p>
  <p><button type="button" class="toggle-btn" data-toggle="{eid}-sol">Solution</button>
     <button type="button" class="toggle-btn" data-complete="exercises" data-cid="{eid}">Mark complete</button></p>
  <div class="reveal" id="{eid}-sol">
    {code("TypeScript", sol)}
    <p><b>Explanation / performance / a11y / testing.</b> {expl} Test with RTL by role. Don’t snapshot the DOM of a virtualizer.</p>
    <p><b>Senior follow-up.</b> {follow}</p>
  </div>
</article>''')
    return f'''
<section class="block" id="exercises" data-search="Hands-on Coding Exercises" data-stype="Section">
  <p class="kicker">Implementation</p>
  <h2 class="section-title">Hands-on Coding Exercises</h2>
  <p class="lede">Fifteen production-shaped sketches. Implement first, then uncover. TypeScript is illustrative (JSX assumed under React 18 types).</p>
  {''.join(cards)}
</section>
'''
