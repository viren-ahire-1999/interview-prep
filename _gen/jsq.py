import html as _html

def code(lang: str, src: str) -> str:
    return (
        f'<div class="code-block"><div class="code-head"><span>{lang}</span>'
        f'<button type="button" class="copy-btn">Copy</button></div>'
        f"<pre><code>{_html.escape(src)}</code></pre></div>"
    )


# Each: id, level, topic, q, short, long, code?, miss, follow
Q = []

def add(level, topic, q, short, long, miss, follow, snippet=""):
    Q.append({
        "level": level, "topic": topic, "q": q, "short": short,
        "long": long, "miss": miss, "follow": follow, "snippet": snippet,
    })

# --- Closures / scope / hoist (1-20)
add("beginner", "closures", "What is a closure?",
    "A function bundled with the lexical environment in which it was created.",
    "Every function has an [[Environment]] pointer. When that function is invoked later, free variables resolve through that chain — even if the outer stack frame is gone. Closures are how JS implements private state, partial application, and React hooks' remembered callbacks.",
    "Thinking closures only exist if you nest functions on purpose, or that they copy values instead of binding live locations (let vs a copied snapshot).",
    "Where have you leaked memory with a closure in production?")
add("beginner", "scope", "What is lexical scope?",
    "Where a name resolves is determined by where the function is written, not where it is called.",
    "The engine walks the scope chain outward from the inner function to module/global. Dynamic scope (this) is the exception people confuse with lexical scope.",
    "Confusing this with lexical scope for regular functions.",
    "How do modules change the global picture?")
add("beginner", "hoisting", "Difference between var, let, and const?",
    "var is function-scoped and initialized undefined; let/const are block-scoped and TDZ; const cannot be rebound.",
    "const objects can have mutated properties. var attaches to the global object at top-level in scripts (not modules). Prefer const, then let; avoid var in new TS.",
    "const means immutable deep values.",
    "What does const mean for an array?")
add("beginner", "hoisting", "What is the Temporal Dead Zone?",
    "The time from block start until a let/const is initialized, during which access throws ReferenceError.",
    "The binding exists (so it can shadow outer names) but is uninitialized. typeof on a TDZ binding throws, unlike typeof undeclared.",
    "TDZ is the same as undefined.",
    "Why did the language add TDZ instead of initializing let to undefined?")
add("intermediate", "closures", "Why does var in a for-loop share one i across callbacks?",
    "var creates a single function-scoped binding; all closures see the final value.",
    "let creates a fresh binding per iteration (the spec's per-iteration environment). Fix with let, or an IIFE capturing the current i, or forEach.",
    "The loop is 'too fast' for the callbacks.",
    "How does this show up in React event handlers in a list without keys? (related stale identity)")
add("intermediate", "closures", "How can closures cause memory leaks?",
    "A long-lived function keeps its lexical environment (and everything it references) alive.",
    "An event handler on document that closes over a large React fiber, a detached DOM node, or a unused big array will pin that memory. Fix by unsubscribing, closing over primitives, or WeakMap.",
    "Closures always leak.",
    "How would you prove it in DevTools?")
add("beginner", "scope", "What is the difference between function scope and block scope?",
    "var ignores blocks except functions; let/const honor { }.",
    "switch cases share a block unless you wrap case bodies. for (let) is a special per-iteration block.",
    "if (true) { var x } is block scoped.",
    "Predict a switch + let collision.")
add("beginner", "hoisting", "Are function declarations hoisted differently from expressions?",
    "Declarations are initialized as functions; expressions follow var/let/const rules of their binding.",
    "const f = function(){} cannot be called above its line. Named function expressions have a local name inside the function.",
    "All functions can be called anywhere in the file.",
    "What about export function in a module?")
add("intermediate", "scope", "What is a lexical environment in the spec sense?",
    "A pair: an environment record (bindings) plus an outer pointer.",
    "This is the real chain: inner LE → outer LE → module → global. VariableEnvironment historically held var bindings.",
    "It is the same as the call stack.",
    "Does a block { let x } create a new LE? (yes)")
add("advanced", "closures", "Do arrows close over this and arguments?",
    "They lexically capture this (and arguments, super, new.target) from the enclosing non-arrow.",
    "They do not have their own this. bind on an arrow cannot rebind this. They have no prototype and cannot be new'd.",
    "Arrows are just shorter functions with the same this rules.",
    "When is an arrow the wrong choice for a method?")
add("beginner", "scope", "What is shadowing?",
    "An inner binding with the same name hides the outer one.",
    "TDZ still applies to the inner name for the whole inner block, so you cannot read the outer let through the inner name even before the inner declaration.",
    "Shadowing is a runtime error always.",
    "How does this interact with catch (e) bindings?")
add("intermediate", "hoisting", "What happens with typeof x when x is a let in TDZ?",
    "ReferenceError, not 'undefined'.",
    "typeof only swallows undeclared globals, not TDZ.",
    "typeof never throws.",
    "Why is that exception for undeclared historical?")
add("beginner", "closures", "Give a practical production closure example.",
    "A factory that returns methods closing over private state; or a memoize cache Map closed over by the wrapper.",
    "Redux listeners, addEventListener callbacks, setTimeout in a custom hook that must clear on unmount — all closures.",
    "Only academic nested functions count.",
    "How do React hooks rely on closures?")
add("intermediate", "closures", "What is a stale closure in React?",
    "A callback created in render N that still reads N's props/state after N+1 committed.",
    "Fix: include deps, use functional setState, useRef for latest values, or an effect that updates a ref.",
    "React is broken; rewrite in classes.",
    "How does useEffect's dependency array relate?")
add("advanced", "scope", "What is the difference between the script goal and module goal?",
    "Modules are strict, have their own scope, and this at top level is undefined.",
    "Scripts in browsers can create global var bindings on window. Modules do not. Live bindings on exports.",
    "type=module is only a bundler flag.",
    "Why does this === undefined in a module's top-level function default call?")
add("beginner", "hoisting", "Can you access a const before its line in the same block?",
    "No — TDZ ReferenceError.",
    "The binding exists and shadows, but is uninitialized.",
    "It is undefined like var.",
    "Does import hoisting differ? (imports are hoisted and live)")
add("intermediate", "closures", "What does IIFE mean and why did we use them?",
    "Immediately Invoked Function Expression — create a private scope in var-world / avoid globals.",
    "Modules and let/const reduced the need. Still useful for isolated one-time setup.",
    "IIFE is required for async.",
    "Show an async IIFE vs top-level await.")
add("beginner", "scope", "What is the global object in the browser vs Node?",
    "window / globalThis in browsers (also self). global / globalThis in Node.",
    "globalThis is the portable name. In modules, global var does not become a property the same way.",
    "global and window are always the same object everywhere.",
    "What is globalThis on a Web Worker?")
add("advanced", "closures", "How do you clone a function and not its closure?",
    "You cannot extract the closed-over environment. You rewrite or pass dependencies explicitly.",
    "This is why DI and explicit args beat hidden closures in large systems.",
    "JSON.stringify the function.",
    "How does this affect testing?")
add("intermediate", "hoisting", "Predict: function vs var same name.",
    "Function declarations and var share the function-scope slot; the winner depends on order of instantiation vs assignment — do not do this.",
    "It is a footgun. Interviewer wants you to refuse the pattern and explain it is confusing.",
    "It is a syntax error always.",
    "Would TypeScript allow it?")

# this / proto (21-35)
add("beginner", "this", "How is this determined for a regular function?",
    "By the call-site: default, implicit (obj.fn), explicit (call/apply/bind), or new.",
    "In strict mode, default is undefined. Losing the receiver when passing obj.fn as a callback is the classic bug.",
    "this is always the object that lexically contains the function.",
    "What happens with obj.fn.bind(other).call(third)?")
add("beginner", "this", "Difference between call, apply, and bind?",
    "call/apply invoke now (apply takes an array of args); bind returns a new function with this (and optional partial args) fixed.",
    "Bound functions ignore later call/apply this (except construct quirks). Spread made apply less necessary.",
    "bind invokes immediately.",
    "How do you unbind? (you don't; wrap)")
add("beginner", "this", "Why are arrow functions different?",
    "Lexical this, no arguments object, no prototype, not constructible.",
    "They are the right default for callbacks. They are the wrong default when you need a method that should use the receiver.",
    "Arrows are faster therefore always better.",
    "Can you new an arrow? (TypeError)")
add("intermediate", "this", "What does new do, step by step?",
    "Create object, set prototype, bind this, run ctor, return object unless ctor returned an object.",
    "If you return a primitive from a constructor it is ignored; an object return replaces this.",
    "new only allocates memory.",
    "What is new.target?")
add("intermediate", "prototypes", "Explain the prototype chain.",
    "Lookup walks [[Prototype]] until null after own properties miss.",
    "Assignment typically creates an own property (does not walk), except with setters on the chain. Object.create(null) has no chain.",
    "The chain is a copy of parent fields.",
    "How does hasOwn vs in differ?")
add("intermediate", "prototypes", "How does instanceof work?",
    "Walk object's proto chain looking for Ctor.prototype.",
    "Breaks across iframes (different Object). Can be customized with Symbol.hasInstance.",
    "It checks constructor.name.",
    "Why is instanceof Array sometimes wrong vs Array.isArray?")
add("intermediate", "prototypes", "class vs constructor function?",
    "class is strict, not callable without new, prototype methods non-enumerable, super works.",
    "Runtime is still prototypes. extends sets both instance proto chain and constructor proto chain (static inheritance).",
    "class is a new object model unrelated to prototypes.",
    "Where do static methods live?")
add("advanced", "prototypes", "What is the difference between __proto__ and prototype?",
    "prototype is a property on functions (the object that new instances will point to). [[Prototype]]/__proto__ is on instances.",
    "You should use Object.getPrototypeOf. __proto__ is a legacy getter.",
    "They are synonyms.",
    "What is Object.setPrototypeOf and why is it slow?")
add("beginner", "this", "What is implicit binding?",
    "obj.method() sets this to obj.",
    "Only the last property access before the call matters: a.b.c() has this === c's owner b? Wait: this is a.b (the object before the last dot).",
    "The this is always the class instance.",
    "Predict: const { method } = obj; method();")
add("advanced", "this", "this in an event handler: DOM vs React?",
    "DOM addEventListener with a regular function: this is the element. React 17+ delegates; class handlers need bind; function components have no this.",
    "Arrow handlers on DOM do not get the element as this (use event.currentTarget).",
    "this is always the component.",
    "Why did React drop implicit this in function components?")
add("intermediate", "prototypes", "What does Object.create do?",
    "Creates an object with a chosen [[Prototype]] and optional property descriptors.",
    "Object.create(null) is a pure dictionary. Object.create(obj) delegates to obj.",
    "It deep clones obj.",
    "How do you copy own enumerable properties? (assign / spread — shallow)")
add("beginner", "prototypes", "Where do array methods live?",
    "Array.prototype. Map/Set similarly. for-in on arrays is a mistake because it can see extra enumerable keys.",
    "You can monkey-patch Array.prototype — do not, except in well-known polyfill cases.",
    "Methods are copied onto each array.",
    "Why is for-of preferred?")
add("advanced", "prototypes", "Explain super in a class method.",
    "super.method() looks up the method on the prototype of the current class's prototype (the parent), and calls it with the current this.",
    "super in constructor calls the parent constructor. In derived classes you must call super before using this.",
    "super is just Parent.method().",
    "What happens if you destructure a method that uses super?")
add("intermediate", "this", "What is explicit binding?",
    "call/apply/bind set this regardless of the call-site's implicit owner.",
    "null/undefined thisArg become the global object in sloppy non-arrow functions — another reason for strict/modules.",
    "Explicit always wins over new. (new actually has its own rule; bound + new is messy)",
    "When would you still use apply?")
add("beginner", "this", "What is default binding?",
    "A bare fn() call. this is undefined in strict, global in sloppy.",
    "TS/JS modules are strict. Your interview code is strict.",
    "Default this is always window.",
    "How do you opt into sloppy? (don't)")

# promises / event loop (36-55)
add("beginner", "promises", "What are the three Promise states?",
    "pending, fulfilled, rejected. Settled means either of the last two. Transitions are one-way.",
    "Then callbacks run in microtasks. You cannot observe a synchronously flipping internal state from outside except via then.",
    "resolved is a fourth public state. (resolved means 'adopted another thenable' in spec jargon)",
    "What does Promise.resolve(thenable) do?")
add("beginner", "async/await", "What happens internally when await is encountered?",
    "The current async function returns a pending promise to its caller; the remainder is scheduled to resume when the awaited value settles (via Promise.resolve).",
    "The thread is not blocked. Sync code after the async call still runs. Resume is a microtask (sometimes an extra hop).",
    "await sleeps the browser.",
    "Does await on a non-promise wrap it?")
add("intermediate", "event-loop", "Why do promises use the microtask queue?",
    "So promise reactions run soon, predictably, after the current stack, before rendering and timer tasks — keeping async invariants tight.",
    "If then were a macrotask, already-resolved promises would yield to timers and paints, making composition racy.",
    "Because they are faster hardware.",
    "How can microtasks starve the UI?")
add("intermediate", "microtasks", "Difference between microtask and task?",
    "Tasks: one per turn (timers, I/O, events). Microtasks: drain all after each task/stack-empty (promises, queueMicrotask).",
    "Rendering is between tasks, not between microtasks.",
    "Microtask means small CPU work.",
    "Where does rAF sit?")
add("beginner", "promises", "Difference between Promise.all and allSettled?",
    "all fail-fast rejects; allSettled waits for every child and never rejects for a child reject.",
    "all([]) fulfills []. allSettled is what you want for 'run these side effects and report'.",
    "allSettled is slower therefore worse.",
    "When is race the right tool?")
add("intermediate", "promises", "Why can long then chains become problematic?",
    "Hard to read, easy to miss errors, accidental sequential waterfalls, extra microtask hops, stack traces less clear than async/await.",
    "Prefer async/await, named helpers, and Promise.all for independent work. Still use then for one-off adaptation.",
    "then is deprecated.",
    "How do you convert a callback API without pyramid of doom?")
add("beginner", "promises", "What does a catch return value do to the chain?",
    "Returning a value fulfills the next promise; throwing or returning reject keeps it rejected.",
    "catch is then(undefined, handler). It recovers by default if it returns normally.",
    "catch swallows and ends the chain always.",
    "Show a catch that rethrows.")
add("advanced", "async/await", "Is await Promise.all concurrent?",
    "The promises start when constructed. await all waits for all. That is concurrency, not parallelism of JS CPU.",
    "If you await in a loop you did not start the work first, you are sequential. Start then await all.",
    "await always parallelizes.",
    "How would you limit concurrency to 4? (see exercises)")
add("intermediate", "event-loop", "Is setTimeout(fn, 0) the next thing that runs?",
    "No. It is a task, after the current stack and all microtasks, and subject to nesting clamps (minimum delay).",
    "Browsers clamp nested timeouts. Node has different phases.",
    "0 means insert at the front of the stack.",
    "What is the 4ms clamp story?")
add("advanced", "event-loop", "What is a microtask checkpoint?",
    "The HTML algorithm that runs all queued microtasks (and those they queue) until empty.",
    "It happens whenever the stack empties at well-defined points, including after each task.",
    "It runs exactly one microtask.",
    "What happens if a microtask queues another infinitely?")
add("beginner", "promises", "What is Promise.race vs any?",
    "race: first settle (fulfill or reject). any: first fulfill; if all reject, AggregateError.",
    "race with a timeout promise is a common pattern (and a leak if you do not cancel the other).",
    "They are aliases.",
    "How do you cancel the loser? (AbortController)")
add("intermediate", "async/await", "How do you handle errors with async/await?",
    "try/catch around await, or .catch on the returned promise. Unhandled rejection if you forget.",
    "Don't mix then and await randomly. For multiple, allSettled or map + try inside.",
    "try/catch around the async function declaration itself without calling it.",
    "What is an unhandledRejection in Node?")
add("beginner", "promises", "Does the Promise constructor executor run async?",
    "No — it runs synchronously. resolve/reject queue reactions.",
    "new Promise((res) => { console.log(1); res(); }) logs 1 before later then.",
    "The whole constructor is deferred.",
    "When would you wrap a callback API with new Promise?")
add("advanced", "promises", "What is a thenable?",
    "An object with a then method. Promise.resolve assimilates it.",
    "This is how libraries interop. It is also an attack/footgun if user data has a then (JSON from API) — do not Promise.resolve(userObject) blindly.",
    "thenable means it is an instance of Promise.",
    "CVE-ish: prototype pollution + then.")
add("intermediate", "microtasks", "queueMicrotask vs Promise.resolve().then?",
    "Same queue conceptually. queueMicrotask is the direct API without creating a Promise.",
    "Exceptions: then creates extra Promise objects. Prefer queueMicrotask for 'after this stack' scheduling without promise semantics.",
    "queueMicrotask is a macrotask.",
    "When is setTimeout(0) more appropriate? (yield to rendering)")
add("beginner", "async/await", "What does an async function return?",
    "Always a Promise. Non-promise returns are wrapped. Throws become rejections.",
    "async function foo(){ return 1 } → Promise that fulfills with 1.",
    "It returns the awaited value directly.",
    "What if you return an already rejected promise?")
add("advanced", "event-loop", "Where does rendering sit relative to promises?",
    "After a task and its microtask drain, the browser may render. Promises can delay paint if you keep queueing microtasks.",
    "rAF runs before paint in the rendering steps, not as a promise job.",
    "Every then triggers a paint.",
    "How do you yield to the browser? (setTimeout/rAF/scheduler.yield)")
add("intermediate", "promises", "Explain Promise chaining value pass-through.",
    "then that returns a value fulfills the next with that value. Returning a promise makes the next wait. Returning nothing fulfills with undefined.",
    "Forgetting to return inside then is a classic bug.",
    "The original promise value is always forwarded.",
    "How does finally differ in value pass-through?")
add("beginner", "event-loop", "Is JavaScript multi-threaded?",
    "The language runtime for your page JS is single-threaded. Workers, I/O threads, compositor threads exist in the host.",
    "SharedArrayBuffer + Atomics is the exception for true shared memory. Don't use it unless you know the model.",
    "Promises run on other threads.",
    "What is the same-origin worker model?")
add("advanced", "async/await", "Top-level await — implications?",
    "ES modules can await at top level, delaying module evaluation and dependents.",
    "Good for init. Bad if it creates import waterfalls or cycles. Bundlers have rules.",
    "It blocks the OS.",
    "How does it affect circular imports?")
add("intermediate", "promises", "What is the difference between resolve and fulfill?",
    "Fulfill: settle with a non-thenable value. Resolve: may adopt a thenable (which might reject).",
    "Spec language. In interviews: resolve(x) is not always 'success with x' if x is a thenable.",
    "They are identical English.",
    "Show Promise.resolve(Promise.reject(1)).")

# browser / memory / perf / react-js (56-80)
add("beginner", "browser", "What is the DOM?",
    "A tree of objects representing the document. JS mutates it; the browser renders it.",
    "It is not the pixels. Frequent mutation without batching causes style/layout work.",
    "DOM is CSS.",
    "What is the difference between DOM and virtual DOM?")
add("intermediate", "browser", "Explain reflow vs repaint.",
    "Reflow/layout: geometry. Repaint: pixels without geometric change. Composite: layers.",
    "Changing width triggers layout; changing a composited transform may skip layout/paint of siblings.",
    "They are the same word.",
    "Name APIs that force layout.")
add("intermediate", "performance", "What is layout thrashing?",
    "Interleaving reads of layout-dependent properties with writes, forcing repeated synchronous layout.",
    "Batch writes, then read. Or use rAF. Libraries like fastdom exist for this.",
    "Too many CSS files.",
    "Show a for-loop of offsetHeight after style changes.")
add("beginner", "memory", "How does garbage collection work at a high level?",
    "Tracing GC marks objects reachable from roots (stack, globals, registered callbacks) and sweeps the rest.",
    "Generational: young objects die fast. You cannot force a reliable collect. WeakRefs exist but are not deterministic.",
    "Reference counting only (cycles would leak forever — engines are tracing).",
    "What are roots in a browser tab?")
add("intermediate", "memory", "How can JS apps leak memory?",
    "Listeners, intervals, detached DOM, unbounded caches, closures, growing arrays, detached fibers.",
    "SPAs are long-lived. Always pair subscribe with unsubscribe in effects.",
    "JS cannot leak because of GC.",
    "How do you take a heap snapshot comparison?")
add("advanced", "memory", "What is a detached DOM node leak?",
    "A node removed from the document but still referenced from JS, so it and its subtree stay in memory.",
    "A Map of elements, a closure in a listener, or a jQuery cache. WeakMap keyed by element avoids owning the node.",
    "innerHTML = '' always frees everything.",
    "How does React's unmount help?")
add("beginner", "browser", "What is requestAnimationFrame for?",
    "Schedule work before the next paint, vsync-aligned.",
    "Use for animation and visual batching. Not for non-visual deferral (use idle/timeout).",
    "It is setTimeout(16).",
    "What happens to rAF in a background tab?")
add("intermediate", "performance", "What is a long task?",
    "A task occupying the main thread for >50ms, blocking input and rendering.",
    "Split work, workers, debounce, virtualize lists, avoid sync layout in hot paths. Atlassian UIs are plugin-heavy — this matters.",
    "Long task means a large JS file on disk.",
    "How do you find them in Performance panel?")
add("intermediate", "react-js", "Why must hook calls be unconditional?",
    "React associates hook state with call order in that component.",
    "This is a JS closure + array-of-hooks model, not magic. Conditional hooks desync state.",
    "It is a style lint only.",
    "What happens if you return early before a useState?")
add("intermediate", "react-js", "Why can a useEffect closure be stale?",
    "The effect function closed over props/state from the render that scheduled it.",
    "Deps tell React when to re-subscribe. Missing deps is a JS problem, not a React bug.",
    "React should autotrack everything always (it might in compiler world — still explain the model).",
    "When is an empty dep array correct?")
add("advanced", "react-js", "What does React batching have to do with the event loop?",
    "Updates inside React-controlled event handlers and, in 18, many async paths, are batched before paint.",
    "You still flush a render as a JS task; effects run after paint. Promises in 17 were not batched — 18 is.",
    "setState is a microtask.",
    "What is flushSync and why is it dangerous?")
add("beginner", "react-js", "Why are keys needed in lists?",
    "Identity so React can map previous instances to the next array, preserving state.",
    "Index keys remount incorrectly on reorder — a JS identity problem.",
    "Keys improve CSS.",
    "Why is Math.random() a bad key?")
add("intermediate", "performance", "debounce vs throttle?",
    "Debounce: wait until quiet. Throttle: max rate. Leading/trailing variants.",
    "Search boxes debounce. Scroll/resize often throttle or rAF-batch. Implement both in exercises.",
    "They are the same.",
    "How do you cancel a debounce on unmount?")
add("advanced", "browser", "Critical rendering path in one minute?",
    "HTML → DOM, CSS → CSSOM, combine to render tree, layout, paint, composite. JS can block parsing if parser-blocking scripts.",
    "defer/async, prefetch, avoid huge sync JS. Senior frontend topic at Atlassian.",
    "The path is only CSS.",
    "What does defer vs async change?")
add("intermediate", "memory", "WeakMap vs Map for caching?",
    "WeakMap keys are objects and do not prevent GC. Map keys pin the key.",
    "WeakMap is not iterable — you cannot dump size. Use Map when you need enumeration or primitive keys.",
    "WeakMap is always better.",
    "Can WeakMap use a string key? (no)")
add("beginner", "browser", "event.preventDefault vs stopPropagation vs stopImmediatePropagation?",
    "preventDefault: cancel default action. stopPropagation: no other nodes. stopImmediate: no other listeners on this node either.",
    "React's synthetic system wraps this; still know the DOM meaning.",
    "They all cancel the event identically.",
    "Does preventDefault stop bubbling? (no)")
add("advanced", "performance", "What is INP / why do long handlers matter?",
    "Interaction to Next Paint: how quickly the UI responds after a click/key. Long JS on the main thread hurts INP.",
    "Atlassian cloud apps feel 'heavy' when plugins do sync work in click handlers. Yield, defer, workers.",
    "INP is a Lighthouse-only vanity metric.",
    "How would you split a click handler?")
add("intermediate", "react-js", "Why is mutating state directly a bug even if it 'works' sometimes?",
    "React's reconciliation and memo compare by reference. Mutating hides the change.",
    "This is a JS object-identity issue. Immutability is a contract, not a religion — but the contract is real.",
    "Mutation is faster therefore preferred.",
    "What does structuredClone vs spread miss?")
add("beginner", "memory", "Do primitives live on the stack?",
    "Engine-dependent. Mentally: primitives are copied by value; objects by reference. Closures capture bindings, not copies of objects (the binding holds a reference).",
    "Do not overfit stack vs heap in an interview; be precise about values vs references.",
    "All numbers are on the heap always / never.",
    "What about boxed Number objects?")
add("advanced", "browser", "What is the compositor thread vs main thread?",
    "Main: JS, style, layout, paint setup. Compositor: stitch layers, often GPU, can scroll some content without main.",
    "Heavy JS still blocks hit-testing and many inputs. Not a silver bullet.",
    "GPU means JS is parallel.",
    "Which CSS properties are typically compositor-only?")
add("intermediate", "react-js", "What is the JS meaning of a custom hook?",
    "A function that calls hooks — shared closure/stateful logic, not a new runtime feature.",
    "Rules of hooks still apply. It is composition of functions.",
    "Custom hooks run on a worker.",
    "When should it be a component instead?")
add("beginner", "promises", "What is async about fetch?",
    "fetch returns a Promise. The network completes in the host; the callback/then is queued as a task (and then body.json() another promise).",
    "You must handle HTTP errors yourself — fetch only rejects on network failure, not 404.",
    "fetch rejects on 404.",
    "How do you abort fetch?")
add("advanced", "microtasks", "MutationObserver callbacks — which queue?",
    "Microtasks. DOM mutations observed are delivered as microtasks.",
    "That is why observing and mutating in a loop can livelock the microtask queue.",
    "They are animation frames.",
    "When would you use IntersectionObserver instead (tasks / rAF-ish batching)?")
add("intermediate", "this", "How does this work in a class field arrow vs a method?",
    "Class field arrows are created per instance and close over the instance this. Prototype methods are shared and depend on call-site.",
    "Arrows cost memory per instance; methods need bind for callbacks.",
    "They are identical after transpile always.",
    "What does the Babel transform look like?")
add("beginner", "scope", "What is strict mode and why do modules use it?",
    "Fewer silent errors: assign to undeclared throws, this default undefined, no with, etc.",
    "Modules and classes are strict automatically.",
    "strict mode makes the engine faster only.",
    "Name two silent sloppy bugs strict fixes.")
add("advanced", "prototypes", "What is a realm and why do instanceof checks fail?",
    "Each iframe / worker / vm has its own intrinsics (its own Array, Object).",
    "An array from an iframe is not instanceof parent.Array. Use Array.isArray, duck typing, or structuredClone across the boundary.",
    "instanceof is realm-safe.",
    "How does this show up with multiple copies of a library in a monorepo bundle?")
add("intermediate", "performance", "Why is JSON.parse(JSON.stringify) a bad deep clone?",
    "Drops undefined, functions, symbols; turns Date into string; fails on cycles, Map, Set, BigInt, undefined in arrays → null.",
    "structuredClone handles more (still not functions). Write a recursive clone when you need custom types.",
    "It is specified to clone everything.",
    "When is it still OK?")
add("beginner", "react-js", "What is reconciliation in JS terms?",
    "Diff previous element tree vs next (by type and key), then commit DOM mutations.",
    "You produce a description; React decides updates. Keys and types steer identity.",
    "Reconciliation is CSS.",
    "Why does changing a component type remount state?")


def jsq() -> str:
    blocks = []
    for i, item in enumerate(Q, 1):
        snip = code("JavaScript", item["snippet"]) if item["snippet"] else ""
        blocks.append(f'''
<article class="q" id="jsq-{i}" data-level="{item["level"]}" data-search="{item["q"]}" data-stype="JS question">
  <div class="meta-row">
    <span class="badge badge-js">{item["level"]}</span>
    <span class="chip">{item["topic"]}</span>
    <span class="chip">Q{i}</span>
  </div>
  <h3>{i}. {item["q"]}</h3>
  <p><button type="button" class="toggle-btn" data-toggle="jsq-a-{i}">Reveal answer</button>
     <button type="button" class="toggle-btn" data-complete="questions" data-cid="jsq-{i}">Mark complete</button></p>
  <div class="reveal" id="jsq-a-{i}">
    <p><b>Short answer.</b> {item["short"]}</p>
    <p><b>Detailed explanation.</b> {item["long"]}</p>
    {snip}
    <p><b>Common misconception.</b> {item["miss"]}</p>
    <p><b>Follow-up.</b> {item["follow"]}</p>
  </div>
</article>''')
    return f'''
<section class="block" id="jsq" data-search="JavaScript interview question bank" data-stype="Section">
  <p class="kicker">80 questions</p>
  <h2 class="section-title">JavaScript Interview Question Bank</h2>
  <p class="lede">Answer out loud. Then reveal. Mark complete only if you could teach the short answer without peeking. Levels are Beginner / Intermediate / Advanced — a senior is expected to handle all three, with more depth on event loop, this, and memory.</p>
  <div class="tabs" data-tabs="jsq">
    <button type="button" class="tab active" data-tab="all">All ({len(Q)})</button>
    <button type="button" class="tab" data-tab="beginner">Beginner</button>
    <button type="button" class="tab" data-tab="intermediate">Intermediate</button>
    <button type="button" class="tab" data-tab="advanced">Advanced</button>
  </div>
  <div data-tabpanel="jsq" data-tab="all">{''.join(blocks)}</div>
  <div class="hidden" data-tabpanel="jsq" data-tab="beginner"></div>
  <div class="hidden" data-tabpanel="jsq" data-tab="intermediate"></div>
  <div class="hidden" data-tabpanel="jsq" data-tab="advanced"></div>
  <p class="stat-sub">Use the badges on each card to filter mentally, or use page search. Count: {len(Q)} questions.</p>
</section>
'''
