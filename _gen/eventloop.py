import html as _html

def code(lang: str, src: str) -> str:
    return (
        f'<div class="code-block"><div class="code-head"><span>{lang}</span>'
        f'<button type="button" class="copy-btn">Copy</button></div>'
        f"<pre><code>{_html.escape(src)}</code></pre></div>"
    )


QS = [
    {
        "n": 1, "title": "Classic timeout vs promise",
        "code": '''console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve().then(() => console.log("C"));
console.log("D");''',
        "ans": "A D C B",
        "steps": "Sync: A, schedule timer task, schedule microtask C, D. Stack empty → drain microtasks (C) → next task (B).",
        "why": "Promise.then is a microtask. setTimeout(0) is a task (macrotask). Microtasks run before the next task.",
        "miss": "Thinking setTimeout(0) runs before promises because 0 means now.",
    },
    {
        "n": 2, "title": "Nested then vs timeout",
        "code": '''setTimeout(() => console.log("T"), 0);
Promise.resolve()
  .then(() => console.log("P1"))
  .then(() => console.log("P2"));
console.log("S");''',
        "ans": "S P1 P2 T",
        "steps": "S sync. Microtask P1 runs, its then queues P2 still as a microtask. Drain P2. Then T.",
        "why": "A then callback that returns a non-thenable fulfills the next promise and queues that next then in the same drain.",
        "miss": "Putting T between P1 and P2.",
    },
    {
        "n": 3, "title": "queueMicrotask vs then",
        "code": '''queueMicrotask(() => console.log("M"));
Promise.resolve().then(() => console.log("P"));
queueMicrotask(() => console.log("M2"));
console.log("S");''',
        "ans": "S M P M2",
        "steps": "Three microtasks queued in that order during sync, then S, then FIFO drain.",
        "why": "queueMicrotask and Promise jobs share the microtask queue (HTML: perform a microtask checkpoint).",
        "miss": "Assuming promises always jump ahead of queueMicrotask.",
    },
    {
        "n": 4, "title": "Timeout inside then",
        "code": '''Promise.resolve().then(() => {
  console.log("P");
  setTimeout(() => console.log("T"), 0);
});
setTimeout(() => console.log("T0"), 0);
console.log("S");''',
        "ans": "S P T0 T",
        "steps": "S. Microtask P schedules T. Existing task T0 was already queued. T0 then T.",
        "why": "The timer inside then is a new task after the ones already queued.",
        "miss": "T before T0 because it was scheduled 'sooner' in source order.",
    },
    {
        "n": 5, "title": "async function start is sync until await",
        "code": '''async function f() {
  console.log("1");
  await null;
  console.log("2");
}
console.log("A");
f();
console.log("B");''',
        "ans": "A 1 B 2",
        "steps": "A. f runs until await (logs 1), schedules resume. B. Microtask resume logs 2.",
        "why": "The prefix of an async function before the first await is synchronous. await Promise.resolve(null) queues the remainder.",
        "miss": "Thinking the whole async function is deferred.",
    },
    {
        "n": 6, "title": "await Promise.resolve vs then",
        "code": '''async function f() {
  console.log("f1");
  await Promise.resolve();
  console.log("f2");
}
f();
Promise.resolve().then(() => console.log("then"));
console.log("S");''',
        "ans": "f1 S then f2   (or f1 S f2 then — engine-dependent on extra tick)",
        "steps": "Practical modern engines: await often takes an extra microtask hop vs a bare then. In interviews, say: both are microtasks; await may schedule one more Promise.resolve wrapper.",
        "why": "Spec: await uses PromiseResolveThenable then performPromiseThen. You may see f2 after then. Do not fight the interviewer — explain the extra tick.",
        "miss": "Guaranteeing f2 before then on every engine.",
    },
    {
        "n": 7, "title": "finally is a microtask too",
        "code": '''Promise.resolve("ok")
  .finally(() => console.log("F"))
  .then(() => console.log("T"));
console.log("S");''',
        "ans": "S F T",
        "steps": "S. finally job, then the following then.",
        "why": "finally schedules a microtask, then rethrows or passes through the value.",
        "miss": "finally runs synchronously when the promise is already resolved.",
    },
    {
        "n": 8, "title": "Rejected promise and catch",
        "code": '''Promise.reject("e")
  .catch((e) => { console.log("C", e); return 1; })
  .then((v) => console.log("T", v));
console.log("S");''',
        "ans": "S  then  C e  then  T 1",
        "steps": "Rejection queues catch. catch returns 1 so the next then fulfills with 1.",
        "why": "Unhandled rejection would fire later; here it is handled. Returning from catch un-rejects the chain.",
        "miss": "Thinking the chain stays rejected after catch.",
    },
    {
        "n": 9, "title": "Promise.all success",
        "code": '''Promise.all([
  Promise.resolve(1),
  Promise.resolve(2),
]).then((v) => console.log("all", v));
Promise.resolve().then(() => console.log("p"));
console.log("S");''',
        "ans": "S p all [1,2]   (all may land after a few microtasks)",
        "steps": "S. Independent then (p). all waits until both input promises are fulfilled, then its then runs.",
        "why": "all itself resolves in a microtask after the last child fulfills.",
        "miss": "all before p always — not guaranteed vs already-resolved children; still after S.",
    },
    {
        "n": 10, "title": "Promise.all fail-fast",
        "code": '''Promise.all([
  Promise.reject("x"),
  new Promise((r) => setTimeout(() => r("late"), 0)),
]).then(
  () => console.log("ok"),
  (e) => console.log("err", e)
);
console.log("S");''',
        "ans": "S  err x   (timeout still runs later but all already rejected)",
        "steps": "Reject is a microtask. all rejects immediately. The timer task still fires but nobody cares.",
        "why": "all is fail-fast. allSettled would wait for the timer.",
        "miss": "Waiting for the timeout before err.",
    },
    {
        "n": 11, "title": "Nested setTimeout vs promise",
        "code": '''setTimeout(() => {
  console.log("T1");
  Promise.resolve().then(() => console.log("P"));
  setTimeout(() => console.log("T2"), 0);
}, 0);
console.log("S");''',
        "ans": "S T1 P T2",
        "steps": "S. Task T1 runs, queues microtask P and task T2. After T1 returns, drain P, then T2.",
        "why": "Every task is followed by a microtask checkpoint.",
        "miss": "T1 T2 P — forgetting the checkpoint after T1.",
    },
    {
        "n": 12, "title": "Two timeouts and a then in the first",
        "code": '''setTimeout(() => {
  console.log("A");
  Promise.resolve().then(() => console.log("B"));
}, 0);
setTimeout(() => console.log("C"), 0);''',
        "ans": "A B C",
        "steps": "Task A, then microtask B, then task C. Not A C B.",
        "why": "Same as 11. This is the most common senior-level trick question.",
        "miss": "A C B because both timeouts were scheduled together.",
    },
    {
        "n": 13, "title": "async IIFE and then",
        "code": '''(async () => {
  console.log("1");
  await 0;
  console.log("2");
})();
Promise.resolve().then(() => console.log("3"));
console.log("4");''',
        "ans": "1 4 3 2  or  1 4 2 3  (await extra hop)",
        "steps": "1 sync. 4 sync. Then microtasks 3 and the resume 2 — order can flip with the extra await tick.",
        "why": "Know that 1 and 4 are definitely first; 2 and 3 are both microtasks.",
        "miss": "2 before 4.",
    },
    {
        "n": 14, "title": "throw in then",
        "code": '''Promise.resolve()
  .then(() => { console.log("A"); throw new Error("x"); })
  .then(() => console.log("B"))
  .catch(() => console.log("C"))
  .then(() => console.log("D"));''',
        "ans": "A C D",
        "steps": "A runs, throws, skips B, catch C, chain fulfilled, D.",
        "why": "Throw in a then rejects the next promise. catch recovers.",
        "miss": "A B C D or stopping at C.",
    },
    {
        "n": 15, "title": "resolved thenable",
        "code": '''const thenable = { then(res) { console.log("th"); res(1); } };
Promise.resolve(thenable).then((v) => console.log("v", v));
console.log("S");''',
        "ans": "S th v 1",
        "steps": "Promise.resolve on a thenable adopts it via a microtask/job; thenable.then runs, then the wrapper fulfills.",
        "why": "thenables are not Promises; resolve assimilates them (sometimes an extra job).",
        "miss": "S v 1 th — thenable.then is how resolve happens.",
    },
    {
        "n": 16, "title": "Promise.race",
        "code": '''const slow = new Promise((r) => setTimeout(() => r("s"), 0));
const fast = Promise.resolve("f");
Promise.race([slow, fast]).then(console.log);
console.log("S");''',
        "ans": "S f   (then later the timeout still resolves unused)",
        "steps": "fast is already fulfilled so race fulfills with f on a microtask. S first.",
        "why": "race uses the first settlement. An already-resolved promise beats a 0ms timer.",
        "miss": "s because the timeout is 0.",
    },
    {
        "n": 17, "title": "Promise.any vs all reject",
        "code": '''Promise.any([
  Promise.reject(1),
  Promise.resolve(2),
]).then(console.log, (e) => console.log("agg", e));''',
        "ans": "2",
        "steps": "First fulfill wins. Rejected sibling is ignored.",
        "why": "any is succeed-fast. All reject → AggregateError.",
        "miss": "agg because one rejected.",
    },
    {
        "n": 18, "title": "MutationObserver / queueMicrotask nest",
        "code": '''queueMicrotask(() => {
  console.log("M1");
  queueMicrotask(() => console.log("M2"));
});
queueMicrotask(() => console.log("M3"));
console.log("S");''',
        "ans": "S M1 M3 M2",
        "steps": "Queue is FIFO. M1 runs, appends M2 at the end, then M3 (already queued), then M2.",
        "why": "Newly queued microtasks run in the same checkpoint, after what was already in line.",
        "miss": "S M1 M2 M3 (depth-first).",
    },
    {
        "n": 19, "title": "requestAnimationFrame conceptually",
        "code": '''// In a browser tab (not this file's JS)
console.log("S");
requestAnimationFrame(() => console.log("R"));
Promise.resolve().then(() => console.log("P"));
setTimeout(() => console.log("T"), 0);''',
        "ans": "S P  then typically T and R depending on frame timing — R is before paint, not a microtask",
        "steps": "S sync. P microtask. T is a task. rAF callbacks run before the next repaint, after the current task/microtasks, aligned to the frame.",
        "why": "rAF is neither then nor setTimeout. Do not put it in the microtask queue in your answer.",
        "miss": "R always before T or always after — frame phase is host-specific.",
    },
    {
        "n": 20, "title": "async await in a for loop (sequential)",
        "code": '''async function run() {
  for (const x of [1, 2]) {
    await Promise.resolve(x).then((v) => console.log("a", v));
    console.log("b", x);
  }
}
run();
console.log("S");''',
        "ans": "S  a 1  b 1  a 2  b 2",
        "steps": "S. First await completes, logs a1, then b1, then next iteration.",
        "why": "await in a for-loop is sequential. forEach(async) would overlap — a common bug.",
        "miss": "S a1 a2 b1 b2.",
    },
    {
        "n": 21, "title": "forEach async pitfall",
        "code": '''console.log("S");
[1, 2].forEach(async (x) => {
  await 0;
  console.log("x", x);
});
console.log("E");''',
        "ans": "S E x 1 x 2",
        "steps": "forEach does not await the async callbacks. Both start, both hit await, E runs, then both resumes (order 1 then 2 typically).",
        "why": "This is why we use for...of with await or Promise.all(map).",
        "miss": "S x1 x2 E.",
    },
    {
        "n": 22, "title": "setTimeout 0 vs 0 vs Promise in Node vs browser",
        "code": '''setTimeout(() => console.log("T"), 0);
setImmediate?.(() => console.log("I")); // Node
Promise.resolve().then(() => console.log("P"));''',
        "ans": "P first. Then T vs I is Node-phase specific (check/timers). In the browser there is no setImmediate.",
        "steps": "Always: microtasks before the next task. Do not claim setImmediate vs timeout order in a browser interview.",
        "why": "Host queues differ. Atlassian browser/Node full-stack: say 'I will not pretend they are the same.'",
        "miss": "Memorizing one Node version's order as universal.",
    },
    {
        "n": 23, "title": "new Promise executor is sync",
        "code": '''console.log("A");
new Promise((resolve) => {
  console.log("B");
  resolve();
  console.log("C");
}).then(() => console.log("D"));
console.log("E");''',
        "ans": "A B C E D",
        "steps": "Executor runs immediately. resolve only queues then. C still sync. E. Then D.",
        "why": "resolve is not a yield point.",
        "miss": "A B D C E.",
    },
    {
        "n": 24, "title": "Double resolve ignored",
        "code": '''new Promise((resolve) => {
  resolve("first");
  resolve("second");
}).then(console.log);''',
        "ans": "first",
        "steps": "Second resolve is a no-op. Promise is already fulfilled.",
        "why": "Settled promises are immutable.",
        "miss": "second or both.",
    },
]


def eventloop() -> str:
    items = []
    for q in QS:
        items.append(f'''
<article class="elq" id="elq-{q["n"]}" data-search="event loop question {q["n"]} {q["title"]}" data-stype="Event loop">
  <div class="meta-row"><span class="badge badge-js">Q{q["n"]}</span></div>
  <h3>{q["n"]}. {q["title"]}</h3>
  {code("JavaScript", q["code"])}
  <p><button type="button" class="toggle-btn" data-toggle="elq-a-{q["n"]}">Reveal answer</button></p>
  <div class="reveal" id="elq-a-{q["n"]}">
    <p><b>Answer.</b> {q["ans"]}</p>
    <p><b>Queue execution.</b> {q["steps"]}</p>
    <p><b>Why.</b> {q["why"]}</p>
    <p><b>Common misconception.</b> {q["miss"]}</p>
  </div>
</article>''')
    return f'''
<section class="block" id="eventloop" data-search="Event loop microtasks macrotasks" data-stype="Section">
  <p class="kicker">The strongest JS section</p>
  <h2 class="section-title">Event Loop — Beginner to Advanced</h2>
  <p class="lede">If you can narrate the queues, you will beat most senior frontend candidates who only have a slogan (“JS is async”). Draw this on a whiteboard in every mock.</p>

  <article class="topic">
    <h3>The pieces</h3>
    <ul class="tight">
      <li><b>Call stack</b> — currently running JS. Nothing else in your JS runs until this is empty (except workers).</li>
      <li><b>Heap</b> — objects. Not a queue.</li>
      <li><b>Web APIs / host</b> — <code>setTimeout</code>, fetch, DOM events, Node I/O. They complete off-stack, then enqueue a callback.</li>
      <li><b>Task queue</b> (macrotasks): timer callbacks, message events, I/O, rendering-related tasks. One task per turn.</li>
      <li><b>Microtask queue</b>: Promise jobs, <code>queueMicrotask</code>, MutationObserver. <b>Drain the entire queue</b> whenever the stack is empty, before the next task, and after every task.</li>
      <li><b>Rendering</b> — opportunity between tasks (not between microtasks). Infinite microtasks starve rendering and input (the “microtask death loop”).</li>
    </ul>
    <div class="diagram">while (eventLoopAlive) {{
  const task = taskQueue.takeNext();   // one macrotask
  run(task);
  while (microtaskQueue.nonEmpty()) {{  // ALL of them
    run(microtaskQueue.takeNext());
  }}
  if (needsRendering && frameDue) {{
    runRAFCallbacks();
    style / layout / paint / composite
  }}
}}</div>
    <h3>Exact ordering you should recite</h3>
    <ol>
      <li>Run synchronous script / current function to completion.</li>
      <li>If the stack is empty, run <i>all</i> microtasks (including ones those microtasks enqueue).</li>
      <li>Take the oldest task. Run it. Go to 2.</li>
      <li>The browser may render if a frame is due and you are not starving it with microtasks.</li>
    </ol>
    <div class="callout good">Promise callbacks are not “async magic.” They are jobs on a queue with a higher priority than timer tasks. <code>await</code> is syntax for “return to the caller and resume this function as a job when the thenable settles.”</div>
    <p>Do all 24 traces below. Cover the answer. Speak the queues. Then uncover.</p>
  </article>
  {''.join(items)}
</section>
'''
