from util import code, topic, diagram, callout


def internals() -> str:
    t = topic("ri-fiber", "Elements, Fiber, render, commit, scheduling", "React internals Fiber render commit concurrent", "React internals", f'''
  <p><b>Simple model.</b> <code>createElement</code> / JSX produces a plain object (an <b>element</b>): <code>{{ type, props, key }}</code>. React’s runtime walks that description and maintains a parallel tree of <b>Fibers</b> — work-in-progress units that remember state, effects, and the real DOM node. “Virtual DOM” as a full-tree-diff myth is outdated; reconciliation is Fiber-vs-Fiber, guided by type and key.</p>
  <p><b>Deeper model.</b> There are typically two Fiber trees: current (what’s on screen) and work-in-progress (the render being built). Render can be <b>interrupted</b> and thrown away. Commit is <b>synchronous</b> and applies DOM + refs + layout effects.</p>
  {diagram('''JSX -> Element (immutable description)
        |
        v
  scheduleUpdate (lane / priority)
        |
        v
  RENDER (interruptible)     -- reconcile, call function components
  work-in-progress Fiber tree
        |
        |  (may restart if a higher-priority update arrives)
        v
  COMMIT (sync)
    mutation (DOM)
    layout effects (useLayoutEffect)
    paint
    passive effects (useEffect)''')}
  <h4>What happens when setState() is called</h4>
  <ol>
    <li><b>Update creation.</b> React stores an update (and a lane) on the Fiber. In 18, multiple updates in the same event are batched. In 18+, many async updates batch too.</li>
    <li><b>Scheduling.</b> The scheduler decides when to start a render. Urgent (click) vs transition (list filter). This is why typing can stay responsive while a large list updates.</li>
    <li><b>Render.</b> Function components run. Hooks read the WIP Fiber. This must be <i>pure enough to retry</i>. Do not put DOM writes or subscriptions here.</li>
    <li><b>Reconciliation.</b> Child elements are matched to existing Fibers by position, type, and key. Same type+key: update. Different type or key: unmount old, mount new (state reset).</li>
    <li><b>Before commit.</b> The WIP tree may be discarded. Effects have not run. The DOM is still the previous commit.</li>
    <li><b>Commit.</b> DOM mutations. <code>useLayoutEffect</code> (read layout, sync). Browser paints. Then <code>useEffect</code> (subscriptions, network, logging).</li>
  </ol>
  <p><b>Why render is interruptible.</b> A 30ms component tree on the main thread would wreck INP. Concurrent rendering yields to input. If you treat render as “this definitely happened,” your side effects in the function body will double-fire in Strict Mode and tear in concurrent features.</p>
  <p><b>Suspense (conceptual).</b> A component throws a thenable; React shows a fallback Fiber and continues siblings it can. Data libraries integrate by throwing promises. Do not invent a custom Suspense cache in an interview unless you can discuss tearing and cache identity.</p>
  <p><b>Refs</b> are the escape hatch that does not schedule a render. <b>useLayoutEffect</b> vs <b>useEffect</b>: layout is for “measure then mutate before paint” (tooltip position). Passive is for “talk to the world after paint.”</p>
  {callout("Senior sentence: “I treat render as a calculation that can run extra times. I put world-changing work in effects or event handlers, and I pick priority with transitions when the update is large and non-urgent.\"", "good")}
''', "reactTopics")

    t2 = topic("ri-lanes", "Batching, lanes, transitions, Suspense", "React batching lanes useTransition Suspense concurrent", "React internals", f'''
  <p><b>Batching.</b> React 18+ flushes many <code>setState</code> calls in the same event, timeout, promise, and native handler as <i>one</i> render. You almost never need <code>flushSync</code>. Use it only when the next line must read the DOM (measure a node you just forced). Overusing <code>flushSync</code> destroys INP.</p>
  <p><b>Lanes / priorities (mental model, not source names).</b> Updates are not a FIFO queue of “the next render.” They have urgency. A click that opens a menu is urgent. Filtering 10k issues is usually a <b>transition</b>: keep the typed characters instant, mark the list update as interruptible. If a higher-priority update arrives, the WIP list render can be thrown away and restarted.</p>
  {code("TypeScript", '''const [isPending, startTransition] = useTransition();
function onJqlChange(next: string) {
  setDraft(next);                 // urgent: the input
  startTransition(() => {
    setAppliedJql(next);          // interruptible: the board
  });
}
// useDeferredValue(appliedJql) is the “one value, two speeds” variant
// when you do not control the setter (e.g. a library prop).''')}
  <p><b>useTransition vs useDeferredValue.</b> Transition wraps <i>your</i> setState. Deferred wraps a <i>value you already have</i> so a child can lag. Do not wrap everything. If the list is 20 rows, a transition is ceremony.</p>
  <p><b>Suspense (conceptual).</b> A child is not ready. It “suspends” (throws a thenable). React keeps showing the nearest fallback and can continue siblings. Data libraries integrate by throwing a promise tied to a cache key. Pitfalls seniors mention: cache identity (two caches = two waterfalls), tearing if you read a mutable store during render, and using Suspense as a substitute for an error boundary (errors need <code>ErrorBoundary</code>).</p>
  <p><b>Effects model.</b> Render calculates the next screen. <code>useLayoutEffect</code> runs after DOM mutation, before paint — measure, then sync-set. <code>useEffect</code> runs after paint — subscribe, fetch, log. Strict Mode in development mounts → unmounts → remounts to prove your cleanup is real. If you “fetch in useEffect” without abort, you will double-fetch in dev and race in prod.</p>
  {callout("Interview: “What can happen before commit?” Answer: another render can start; the WIP tree can be discarded; no DOM writes; no effects. That is why you do not put side effects in the function body.")}
  ''', "reactTopics")

    return f'''
<section class="block" id="internals" data-search="React Internals Fiber setState" data-stype="Section" data-cat="react">
  <p class="kicker">Runtime</p>
  <h2 class="section-title">React Internals</h2>
  <p class="lede">You do not need to recite source file names. You do need a model that explains Strict Mode double-invoke, transitions, and why “setState in render” is a footgun.</p>
  {t}{t2}
</section>
'''


def reconciliation() -> str:
    examples = [
        ("key-swap", "Same type, key A → key B",
         '''function Box({ id }: { id: string }) {
  const [n, setN] = useState(0);
  return <button onClick={() => setN(n + 1)}>{id}:{n}</button>;
}
// first render:
<Box key="A" id="A" />
// next:
<Box key="B" id="B" />''',
         "The Fiber is thrown away. State n resets to 0. DOM node is remounted. Effects clean up and re-run.",
         "Key is part of identity. Changing it is an unmount + mount, not a prop change."),
        ("index-keys", "Index keys on a reorderable list",
         '''items.map((item, i) => <Row key={i} item={item} />)
// User deletes index 0. Every later row keeps key i but gets a new item.''',
         "React reuses Fibers by index. Uncontrolled inputs and local state slide to the wrong row. You will ship a bug that looks like “React is broken.”",
         "Stable IDs as keys. Index keys only for static lists that never reorder or prepend."),
        ("unstable-key", "Unstable key (Math.random or new UUID each render)",
         '''<Row key={Math.random()} />''',
         "Every render remounts the row. State lost. Effects thrash. Focus lost. CPU waste.",
         "Keys must be stable across renders for the same logical entity."),
        ("conditional-type", "Conditional changes component type at the same position",
         '''{isEdit ? <Textarea value={v} /> : <Preview value={v} />}''',
         "Different type → remount. That’s usually what you want (don’t leak textarea state into preview). If you need to keep a draft, lift state.",
         "Type is identity. To preserve state, keep the same type and toggle props, or lift state."),
        ("position-swap", "Two siblings swap without keys",
         '''// Before: <Input /><Checkbox />
// After:  <Checkbox /><Input />''',
         "Without keys, React matches by index + type. Types differ at each index → remount both. With keys, it can move Fibers.",
         "Keys are not only for arrays; they disambiguate siblings of mixed types when order changes."),
        ("list-reorder", "Board cards reorder with stable keys",
         '''cards.map(c => <Card key={c.id} card={c} />)''',
         "Fibers move. Local collapse/expand state stays on the correct card. DOM nodes can be moved instead of rebuilt.",
         "This is why Jira-like boards must key by issue id, never by column index."),
    ]
    blocks = []
    for i, (eid, title, src, expect, take) in enumerate(examples, 1):
        blocks.append(f'''
<article class="topic" id="rec-{eid}" data-search="{title} reconciliation" data-stype="Reconciliation example">
  <div class="meta-row"><span class="badge badge-js">Practice</span></div>
  <h3>{i}. {title}</h3>
  {code("TypeScript", src)}
  <p><button type="button" class="toggle-btn" data-toggle="rec-a-{eid}">Reveal behavior</button></p>
  <div class="reveal" id="rec-a-{eid}">
    <p><b>Expected behavior.</b> {expect}</p>
    <p><b>Interview takeaway.</b> {take}</p>
  </div>
</article>''')

    body = topic("rec-model", "Reconciliation rules", "reconciliation keys identity mount update unmount", "React internals", f'''
  <p>React does not “diff the whole page.” It walks the tree and, at each Fiber, asks: is this the same component instance as last time?</p>
  <ul class="tight">
    <li><b>Same type + same key</b> (default key = position): <b>update</b>. Props change, state stays, DOM is patched.</li>
    <li><b>Different type or different key:</b> <b>unmount</b> old (effects cleanup, state gone), <b>mount</b> new.</li>
    <li><b>Lists:</b> keys let React match across reorder. Missing keys → index matching → state bugs.</li>
  </ul>
  <p>Parent re-render does <i>not</i> mean the DOM changes. If child props are referentially equal and the child is memoized, even the function may not run. If it runs and returns the same host elements, commit may still skip DOM work.</p>
  ''', "reactTopics")

    return f'''
<section class="block" id="reconciliation" data-search="React Reconciliation keys identity" data-stype="Section" data-cat="react">
  <p class="kicker">Identity</p>
  <h2 class="section-title">React Reconciliation</h2>
  <p class="lede">If you can teach keys with a board-card example, you are at the senior bar for this topic.</p>
  {body}
  {''.join(blocks)}
</section>
'''
