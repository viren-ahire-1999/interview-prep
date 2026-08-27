import html as _html

def code(lang: str, src: str) -> str:
    return (
        f'<div class="code-block"><div class="code-head"><span>{lang}</span>'
        f'<button type="button" class="copy-btn">Copy</button></div>'
        f"<pre><code>{_html.escape(src)}</code></pre></div>"
    )


def topic(tid, title, search, body):
    return f'''
<article class="topic" id="{tid}" data-search="{search}" data-stype="JavaScript topic">
  <h3>{title}</h3>
  {body}
  <p><button type="button" class="toggle-btn" data-complete="jsTopics" data-cid="{tid}">Mark complete</button></p>
</article>
'''


def js_dive() -> str:
    runtime = topic("js-runtime", "Runtime fundamentals", "JavaScript execution model call stack heap", f'''
  <p>JavaScript is single-threaded at the language level: one call stack runs one piece of your code at a time. Concurrency comes from the <b>host</b> (browser or Node) which owns Web APIs / libuv, queues, and the event loop.</p>
  <h4>Execution context</h4>
  <p>Every time you enter a function (or the script), the engine creates an execution context: a box that holds a lexical environment (scope), a <code>this</code> binding (for non-arrows), and a pointer to the current instruction. The <b>global execution context</b> (GEC) is created first and lives until the page / process dies.</p>
  <h4>Call stack</h4>
  <p>Contexts are stacked. <code>A</code> calls <code>B</code> calls <code>C</code>: C is on top, then B, then A, then GEC. <code>return</code> or a throw pops. Stack overflow is this structure growing without bound (unbounded recursion).</p>
  <h4>Heap</h4>
  <p>Objects, closures, and most arrays live on the heap. The stack stores primitives and <i>references</i> to heap objects. When no reference remains, GC may reclaim the object — not instantly, and not if a closure or detached listener still points at it.</p>
  <div class="diagram">Event loop (browser)
  Call stack          Heap
  +--------+          +----------+
  |  C()   |          | objects  |
  |  B()   |          | closures |
  |  A()   |          | DOM ...  |
  |  GEC   |          +----------+
  +--------+
  Host: timers, fetch, DOM, rAF
  Microtask queue | Task queue</div>
  <p><b>Lexical environment vs variable environment.</b> ES spec: a function has a lexical environment (let/const/functions, and the outer pointer) and historically a variable environment for <code>var</code>. Mentally: <code>var</code> is function-scoped and hoisted as <code>undefined</code>; <code>let</code>/<code>const</code> are block-scoped and hoisted into the TDZ.</p>
  {code("JavaScript", '''function outer(x) {
  const y = 2;          // in outer's lexical environment
  return function inner() {
    return x + y;       // inner's [[Environment]] points at outer's LE
  };
}
const f = outer(1);     // outer's frame is gone from the stack
f();                    // 3 — heap still holds {x:1, y:2} because f closed over it''')}
''')

    hoist = topic("js-hoist", "Hoisting and the Temporal Dead Zone", "hoisting var let const TDZ", f'''
  <p>Hoisting means the engine <b>creates bindings</b> before running the body. It does <i>not</i> mean values are available.</p>
  <ul class="tight">
    <li><code>var x</code>: binding exists in the function, initialized to <code>undefined</code> at instantiate time. Assignments stay in place.</li>
    <li><code>let</code>/<code>const</code>: binding exists in the block but is uninitialized until the declaration line. Access before that is a <code>ReferenceError</code> (TDZ).</li>
    <li>Function declarations: fully initialized (the function object) in the scope. Callable above their line in the same scope (not inside a block in sloppy ways — prefer not to rely on block-level function hoisting).</li>
    <li>Function expressions / arrows assigned to <code>const</code>: the name is in TDZ until the line runs.</li>
  </ul>
  {code("JavaScript", '''console.log(a); // undefined
var a = 1;
console.log(b); // ReferenceError
let b = 2;
foo();          // works
function foo() {}
bar();          // TypeError: bar is not a function (bar is undefined)
var bar = function () {};''')}
  <p>TDZ starts at the beginning of the block and ends when the initializer runs. <code>const</code> must have an initializer; <code>let</code> may not (then it becomes <code>undefined</code> after the line).</p>
  <div class="callout warn">Interview trap: <code>typeof undeclared</code> is <code>"undefined"</code>, but <code>typeof</code> of a <code>let</code> in TDZ throws. <code>typeof</code> is not always safe.</div>
''')

    clos = topic("js-closures", "Closures", "closures lexical scoping memory", f'''
  <p>A closure is a function plus the lexical environment it was created in. It is not a special type — every function has an <code>[[Environment]]</code> slot. You <i>observe</i> a closure when the inner function outlives the stack frame that created it.</p>
  <p><b>Why it matters in production.</b> React function components close over props/state from the render that created them (stale closures). Module-level caches close over maps. Event handlers close over elements. Private state in factories is a closure, not a keyword.</p>
  {code("JavaScript", '''function makeBank() {
  let balance = 0; // not reachable except via the returned methods
  return {
    deposit: (n) => { balance += n; },
    get: () => balance,
  };
}
const acct = makeBank();
acct.deposit(10);
acct.get(); // 10 — balance is heap-retained by the two methods''')}
  <p><b>Loop trap.</b> <code>var i</code> in a loop is one binding. All closures see the final i. <code>let i</code> creates a new binding per iteration.</p>
  {code("JavaScript", '''const fns = [];
for (var i = 0; i < 3; i++) fns.push(() => i);
fns.map((f) => f()); // [3,3,3]
const fns2 = [];
for (let j = 0; j < 3; j++) fns2.push(() => j);
fns2.map((f) => f()); // [0,1,2]''')}
  <p><b>Memory.</b> If a long-lived function closes over a large object you no longer need, that object cannot be collected. Fix: null the reference, close over a smaller field, or unregister the handler. This is a real leak pattern in SPAs.</p>
''')

    thisb = topic("js-this", "this, call, apply, bind, new", "this binding call apply bind arrow", f'''
  <p><code>this</code> is decided at <b>call time</b> for ordinary functions, and at <b>creation time</b> (lexically) for arrows. It is not “the object above the function” unless the call-site makes it so.</p>
  <table>
    <tr><th>Rule</th><th>Call site</th><th>this</th></tr>
    <tr><td>Default</td><td><code>fn()</code></td><td><code>undefined</code> in strict / modules; global object in sloppy</td></tr>
    <tr><td>Implicit</td><td><code>obj.fn()</code></td><td><code>obj</code></td></tr>
    <tr><td>Explicit</td><td><code>fn.call(obj)</code> / <code>apply</code></td><td><code>obj</code> (unless fn is bound or an arrow)</td></tr>
    <tr><td>Bound</td><td><code>fn.bind(obj)</code> then later call</td><td>fixed <code>obj</code></td></tr>
    <tr><td>new</td><td><code>new Fn()</code></td><td>the created instance</td></tr>
    <tr><td>Arrow</td><td>any</td><td>this of the enclosing non-arrow (lexical)</td></tr>
  </table>
  <p><code>call(thisArg, ...args)</code> invokes immediately. <code>apply(thisArg, argsArray)</code> same with an array. <code>bind(thisArg, ...partial)</code> returns a new function. <code>new</code> ignores a bound this in the sense that constructor binding wins for the constructed object — bound functions as constructors are a footgun; do not do it.</p>
  {code("JavaScript", '''const obj = {
  n: 1,
  regular() { return this.n; },
  arrow: () => this.n, // this is outer (module/global), not obj
};
obj.regular();          // 1
const r = obj.regular;
r();                    // undefined.n → throw in strict
r.call({ n: 7 });       // 7
obj.arrow();            // not 1
const bound = obj.regular.bind({ n: 9 });
bound();                // 9
bound.call({ n: 1 });   // still 9 — bind wins over later call''')}
  <p><b>What <code>new Fn()</code> does.</b> Create <code>{{}}</code>, set its <code>[[Prototype]]</code> to <code>Fn.prototype</code>, run <code>Fn</code> with <code>this</code> bound to that object, return the object (unless the constructor returns another object).</p>
  <div class="callout">React class methods lose <code>this</code> when passed as callbacks — bind in the constructor, use a class field arrow, or wrap. Function components avoid the issue.</div>
''')

    proto = topic("js-proto", "Prototype system", "prototype chain class inheritance instanceof", f'''
  <p>Every ordinary object has an internal <code>[[Prototype]]</code> (exposed as <code>Object.getPrototypeOf</code> / <code>__proto__</code>). Property lookup: own properties first, then walk the chain until <code>null</code>.</p>
  {code("JavaScript", '''const proto = { greet() { return "hi " + this.name; } };
const user = Object.create(proto);
user.name = "Vi";
user.greet(); // "hi Vi" — greet found on proto, this is user
Object.getPrototypeOf(user) === proto; // true
user instanceof Object; // true — walks the chain to Object.prototype''')}
  <p><code>instanceof</code> checks whether <code>Ctor.prototype</code> is on the object's prototype chain. It can be fooled by realms (iframes) and by mutated <code>.prototype</code>.</p>
  <p><b>Constructor functions vs <code>class</code>.</b> <code>class</code> is mostly syntax: methods land on <code>.prototype</code>, <code>constructor</code> is the function, <code>extends</code> wires <code>[[Prototype]]</code> of both the constructor and the prototype object. Classes are strict and not callable without <code>new</code>.</p>
  {code("JavaScript", '''class Animal {
  constructor(name) { this.name = name; }
  speak() { return this.name; }
}
class Dog extends Animal {
  speak() { return super.speak() + " woof"; }
}
const d = new Dog("Rex");
d.speak();
Object.getPrototypeOf(d) === Dog.prototype;
Object.getPrototypeOf(Dog.prototype) === Animal.prototype;
Object.getPrototypeOf(Dog) === Animal; // constructor inheritance''')}
  <p><code>Object.create(null)</code> is a dictionary with no prototype — useful to avoid <code>toString</code> key collisions. Prefer <code>Map</code> in modern TS.</p>
''')

    asyncj = topic("js-async", "Async JavaScript: promises and await", "promises async await Promise.all", f'''
  <p>A Promise is a thenable state machine: pending → fulfilled or rejected, then frozen. <code>then</code>/<code>catch</code>/<code>finally</code> schedule <b>microtasks</b>. The host (timers, I/O) schedules <b>tasks</b>.</p>
  <p><b>What <code>await</code> does.</b> <code>await x</code> wraps <code>x</code> in <code>Promise.resolve</code>, suspends the async function (returns a pending promise to the caller), and resumes the rest of the function as a microtask when x settles. It does <i>not</i> block the thread. Other tasks and microtasks can run while you are awaiting.</p>
  {code("JavaScript", '''async function sample() {
  const a = await 1;          // microtask resume, a === 1
  const b = await Promise.resolve(2);
  return a + b;
}
sample().then(console.log);   // schedules more microtasks
console.log("sync");          // runs first''')}
  <table>
    <tr><th>Helper</th><th>Behavior</th></tr>
    <tr><td>Promise.all</td><td>Fulfill when all fulfill; reject on first reject; [] → [] immediately</td></tr>
    <tr><td>allSettled</td><td>Wait for all; never rejects for child rejects</td></tr>
    <tr><td>race</td><td>First settle wins (fulfill or reject)</td></tr>
    <tr><td>any</td><td>First fulfill wins; reject AggregateError if all reject</td></tr>
  </table>
  <p>Long <code>then</code> chains are hard to debug and can hide sequential waterfalls that should have been <code>Promise.all</code>. Prefer async/await plus explicit concurrency.</p>
''')

    browse = topic("js-browser", "Browser rendering pipeline", "rendering reflow paint composite rAF", f'''
  <p>A frame is approximately: process input → JS → style → layout (reflow) → paint → composite. The compositor can move already-painted layers on the GPU (transform/opacity) without layout.</p>
  <ul class="tight">
    <li><b>Style:</b> compute computed styles (CSSOM + DOM).</li>
    <li><b>Layout:</b> geometry. Reading <code>offsetHeight</code>, <code>getBoundingClientRect</code>, <code>scrollTop</code> can flush pending layout (layout thrashing if you interleave writes and reads).</li>
    <li><b>Paint:</b> fill pixels for layers.</li>
    <li><b>Composite:</b> stitch layers.</li>
  </ul>
  <p><code>requestAnimationFrame(cb)</code> runs <code>cb</code> before the next paint, so visual updates stay vsynced. It is not a timer. Long tasks (&gt;50ms) block input and rendering — split work, use workers, debounce handlers.</p>
  <div class="callout warn">Forced reflow example: in a loop, set <code>el.style.width</code> then read <code>el.offsetWidth</code>. Batch writes, then read once.</div>
''')

    mem = topic("js-memory", "Memory and leaks", "garbage collection memory leaks closures DOM", f'''
  <p>JS engines use generational mark-and-sweep / tracing GC. You do not free objects. You drop references.</p>
  <p><b>Leak patterns that show up in React/Node interviews:</b></p>
  <ul class="tight">
    <li>Forgotten <code>addEventListener</code> / <code>setInterval</code> after unmount.</li>
    <li>Detached DOM nodes still referenced from a JS cache or closure.</li>
    <li>Global caches that grow without eviction (unbounded Map).</li>
    <li>Closures holding the entire props object when they needed one field.</li>
    <li>Console logging large objects in DevTools (retains them).</li>
    <li>Unbounded Promise chains or queues in a worker.</li>
  </ul>
  <p>Debug: Memory panel heap snapshots, comparison after a suspected interaction, look for Detached HTMLElement and growing retainer paths. <code>WeakMap</code>/<code>WeakRef</code> when the cache should not own the key.</p>
''')

    adv = topic("js-advanced", "Advanced language features", "iterators generators symbols WeakMap Proxy Reflect", f'''
  <p><b>Iterators.</b> An object with <code>next() → {{ value, done }}</code>. Iterables have <code>[Symbol.iterator]()</code>. <code>for...of</code>, spread, and destructuring use this protocol. Arrays are iterable; objects are not unless you define it.</p>
  <p><b>Generators.</b> <code>function*</code> returns a generator. <code>yield</code> pauses. Useful for lazy sequences and cooperative cancellation. <code>async function*</code> yields promises.</p>
  <p><b>Symbols.</b> Unique keys. Well-known symbols (<code>Symbol.iterator</code>, <code>toStringTag</code>) hook the language. They are not copied by <code>JSON.stringify</code>.</p>
  <p><b>WeakMap / WeakSet.</b> Keys (WM) / values (WS objects) are weakly held. Not enumerable. Use for private metadata on objects you do not own, or caches that should die with the key.</p>
  <p><b>Proxy / Reflect.</b> Intercept get/set/apply/etc. <code>Reflect</code> is the default-behavior twin so you can forward traps correctly. Use cases: observable state, validation, negative-index arrays. Cost: they are slower and debugging is harder — do not sprinkle them everywhere.</p>
  {code("JavaScript", '''const wm = new WeakMap();
function tag(el, meta) { wm.set(el, meta); }
function getTag(el) { return wm.get(el); } // dies with el

const handler = {
  get(t, p, r) { return Reflect.get(t, p, r); },
  set(t, p, v, r) { return Reflect.set(t, p, v, r); },
};
const proxied = new Proxy({ x: 1 }, handler);''')}
''')

    return f'''
<section class="block" id="js" data-search="JavaScript Deep Dive runtime" data-stype="Section">
  <p class="kicker">Language</p>
  <h2 class="section-title">JavaScript Deep Dive</h2>
  <p class="lede">Written for a 7-year React/TypeScript engineer. The goal is a senior mental model, not a beginner tour. Pair each topic with the Event Loop section and the question bank. Mark complete only after you can teach it without notes.</p>
  {runtime}{hoist}{clos}{thisb}{proto}{asyncj}{browse}{mem}{adv}
</section>
'''
