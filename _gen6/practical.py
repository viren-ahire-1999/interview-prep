from util import topic, callout, code, diagram


def _study(cid, title, search, problem, structure, code_js, product, trap):
    return topic(cid, title, search, "Practical study", f'''
  <p><b>Problem.</b> {problem}</p>
  <p><b>Structure / algorithm.</b> {structure}</p>
  {code("JavaScript", code_js)}
  <p><b>Where this shows up at work.</b> {product}</p>
  <p><b>Trap.</b> {trap}</p>
  ''', "reactTopics")


def practical() -> str:
    items = [
        _study("ps-lru", "LRU cache", "LRU cache practical JavaScript",
               "Keep the K most recently used keys. get/put in O(1).",
               "Map (insertion order in JS is specified) or Map + doubly linked list. JS Map: delete + set moves a key to the end.",
               '''class LRUCache {
  constructor(capacity) { this.cap = capacity; this.map = new Map(); }
  get(key) {
    if (!this.map.has(key)) return -1;
    const v = this.map.get(key);
    this.map.delete(key);
    this.map.set(key, v);
    return v;
  }
  put(key, value) {
    if (this.map.has(key)) this.map.delete(key);
    this.map.set(key, value);
    if (this.map.size > this.cap) {
      const oldest = this.map.keys().next().value;
      this.map.delete(oldest);
    }
  }
}
''',
               "Image/cache of API responses, tab keep-alive (cap 3–5), parsed module cache.",
               "Using an array + indexOf is O(n). Forgetting to refresh on get."),
        _study("ps-undo", "Undo / redo", "undo redo stack practical",
               "Editor undo. Undo moves the last op to a redo stack. A new edit clears redo.",
               "Two stacks.",
               '''class History {
  constructor() { this.undo = []; this.redo = []; }
  do(op) { this.undo.push(op); this.redo.length = 0; }
  undoOp() {
    if (!this.undo.length) return null;
    const op = this.undo.pop();
    this.redo.push(op);
    return op;
  }
  redoOp() {
    if (!this.redo.length) return null;
    const op = this.redo.pop();
    this.undo.push(op);
    return op;
  }
}
''',
               "Rich text, form wizards, whiteboard tools. Persist undo only if you also persist the document.",
               "Storing full document snapshots every keystroke — store ops or diffs."),
        _study("ps-auto", "Autocomplete", "autocomplete trie practical",
               "Type a prefix, return up to 10 words.",
               "Trie + DFS/BFS collect, or a sorted array + binary search on prefix (simpler, O(n) collect).",
               '''function suggest(trie, prefix, limit = 10) {
  let n = trie.root;
  for (const ch of prefix) {
    if (!n.next.has(ch)) return [];
    n = n.next.get(ch);
  }
  const out = [];
  function dfs(node, path) {
    if (out.length >= limit) return;
    if (node.end) out.push(path);
    for (const [ch, nxt] of node.next) dfs(nxt, path + ch);
  }
  dfs(n, prefix);
  return out;
}
''',
               "Command palette, mention lists, Jira key search. Production still needs server authz so private titles never leak.",
               "Walking the whole dictionary on each keystroke without a prefix index."),
        _study("ps-deps", "Dependency / import graph", "module dependency cycle topological",
               "Given package.json-style deps, detect a cycle and produce an install order.",
               "Directed graph + Kahn topological sort (see Graphs).",
               '''function installOrder(packages) {
  // packages: { name: string, deps: string[] }[]
  const names = packages.map((p) => p.name);
  const prereqs = [];
  for (const p of packages) for (const d of p.deps) prereqs.push([p.name, d]);
  const idx = new Map(names.map((n, i) => [n, i]));
  const edges = prereqs.map(([a, b]) => [idx.get(a), idx.get(b)]);
  // canFinish + collect order — if false, cycle
  return edges;
}
''',
               "Bundlers, monorepo build order, CI jobs, spreadsheet formulas.",
               "Treating npm’s graph as a tree — it is a DAG if legal, a cycle if broken."),
        _study("ps-rate", "Rate limiter (sliding window)", "rate limit sliding window practical",
               "Allow at most N requests per user per W milliseconds.",
               "Queue of timestamps per key; drop those older than now-W.",
               '''function allow(buckets, key, now, n, windowMs) {
  const q = buckets.get(key) || [];
  const cut = now - windowMs;
  while (q.length && q[0] <= cut) q.shift();
  if (q.length >= n) { buckets.set(key, q); return false; }
  q.push(now);
  buckets.set(key, q);
  return true;
}
''',
               "Login attempts, search-as-you-type on the client (debounce is different — it delays; a limiter rejects).",
               "A fixed counter that never expires. Using shift in a huge queue — for interviews n is small; at scale use a deque or Redis."),
        _study("ps-feed", "Feed dedup + cursor", "feed pagination cursor set",
               "Infinite scroll must not show the same post twice when the server overlaps pages.",
               "Set of seen ids + cursor string from the last item.",
               '''function mergePage(seen, items, cursorFrom) {
  const out = [];
  for (const it of items) {
    if (seen.has(it.id)) continue;
    seen.add(it.id);
    out.push(it);
  }
  const next = items.length ? items[items.length - 1].cursor : cursorFrom;
  return { out, next };
}
''',
               "Any infinite list: notifications, Jira search, chat history.",
               "Using offset pagination while the list mutates — items shift and you skip/dup."),
        _study("ps-virt", "Visible window (virtual list)", "virtual list window indexes",
               "Render only rows [start, end] for a 10k list.",
               "Arithmetic, not a fancy structure: start = floor(scrollTop / rowHeight).",
               '''function visibleRange(scrollTop, viewH, rowH, n) {
  const start = Math.max(0, Math.floor(scrollTop / rowH) - 2);
  const count = Math.ceil(viewH / rowH) + 4;
  const end = Math.min(n, start + count);
  return { start, end };
}
''',
               "Boards, admin grids, file trees. This is why O(n) DOM is a product bug.",
               "Variable row height needs a prefix-sum of heights or a probe — say so."),
        _study("ps-sched", "Job scheduler (min-heap)", "scheduler heap practical",
               "Run the next due job. Jobs have a timestamp.",
               "Min-heap of [time, job].",
               '''function nextDue(heap, now) {
  const due = [];
  while (heap.peek() !== undefined && heap.peek()[0] <= now) due.push(heap.pop());
  return due;
}
''',
               "Retry queues, reminder toasts, animation timelines, Node timers (conceptually).",
               "Scanning an unsorted array every tick — O(n) vs O(log n) pop."),
        _study("ps-merge", "Accounts / identity merge", "union find accounts merge",
               "Emails that overlap belong to the same person.",
               "Union-find on email nodes, or graph BFS.",
               '''function mergeAccounts(accounts) {
  const uf = new UnionFind(accounts.length);
  const emailTo = new Map();
  accounts.forEach((acc, i) => {
    for (const e of acc.slice(1)) {
      if (emailTo.has(e)) uf.union(i, emailTo.get(e));
      else emailTo.set(e, i);
    }
  });
  return uf;
}
''',
               "CRM merge, SSO identity, “same user, two tickets.”",
               "Union on names (collisions) instead of unique emails."),
        _study("ps-ser", "Serialize a tree", "serialize deserialize tree JSON",
               "Save/load a comment thread or org chart.",
               "Preorder with null sentinels, or JSON of nested objects (the practical one).",
               '''function toJSON(root) {
  if (!root) return null;
  return { val: root.val, left: toJSON(root.left), right: toJSON(root.right) };
}
function fromJSON(j) {
  if (!j) return null;
  return new TreeNode(j.val, fromJSON(j.left), fromJSON(j.right));
}
''',
               "Persisting UI trees, exporting a page outline, cloning a node.",
               "Forgetting nulls so the shape is lost; cycles if it is a graph — then you need ids."),
        _study("ps-diff", "List reconciliation (keys)", "react keys list diff practical DSA",
               "Old list A, new list B. Reuse nodes with the same key.",
               "Map key → node from A; walk B; leftovers unmount. This is the DSA behind React lists — not Fiber.",
               '''function reconcile(prev, next) {
  const map = new Map(prev.map((n) => [n.key, n]));
  const reused = [];
  for (const n of next) {
    if (map.has(n.key)) { reused.push(map.get(n.key)); map.delete(n.key); }
    else reused.push({ ...n, born: true });
  }
  const dead = [...map.values()];
  return { reused, dead };
}
''',
               "Any keyed list UI. Index keys remap state — that is this map going wrong.",
               "Using index as key when the list reorders."),
        _study("ps-path", "Shortest path in a warehouse grid",
               "grid BFS shortest path practical",
               "Robot from start to end, 4-way, walls.",
               "BFS + parent pointers to reconstruct.",
               '''function shortest(grid, start, end) {
  const q = [start];
  const prev = new Map();
  const key = (r, c) => r + "," + c;
  prev.set(key(start[0], start[1]), null);
  const dirs = [[1,0],[-1,0],[0,1],[0,-1]];
  while (q.length) {
    const [r, c] = q.shift();
    if (r === end[0] && c === end[1]) break;
    for (const [dr, dc] of dirs) {
      const nr = r + dr, nc = c + dc;
      const k = key(nr, nc);
      if (grid[nr]?.[nc] === 0 && !prev.has(k)) {
        prev.set(k, [r, c]);
        q.push([nr, nc]);
      }
    }
  }
  return prev.has(key(end[0], end[1]));
}
''',
               "Games, warehouse bots, “is this Jira workflow reachable,” maze tutorials.",
               "DFS for shortest path in an unweighted grid — it is not shortest."),
    ]
    return f'''
<section class="block" id="practical" data-search="Practical DSA studies JavaScript products" data-stype="Section">
  <p class="kicker">{len(items)} studies</p>
  <h2 class="section-title">Practical studies</h2>
  <p class="lede">Same structures, in product clothing. Type the code. Then name a feature from <i>your</i> work that matches — do not invent metrics.</p>
  {callout("These are teaching shapes, not claimed official interview questions.")}
  {diagram("Structure → tiny implementation → product sentence → trap")}
  {''.join(items)}
</section>
'''
