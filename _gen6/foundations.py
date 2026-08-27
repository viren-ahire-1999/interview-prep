from util import topic, diagram, callout, code


def howto() -> str:
    t = topic("ht-loop", "The only loop that works",
              "how to learn DSA JavaScript", "Lesson", f'''
  <p>DSA is not a spectator sport. For every lesson: <b>predict</b> on paper → <b>type</b> in JS → <b>break</b> it with an edge case → <b>say</b> time and space. Reading this HTML without a keyboard will not make you expert.</p>
  <ol>
    <li>Draw the data (boxes and arrows). JS references are arrows.</li>
    <li>Write the function without looking at the solution.</li>
    <li>Run 3 cases: empty, one element, the ugly case (duplicates, cycles, negatives).</li>
    <li>Only then reveal. Diff your code. Steal one idea, rewrite from blank.</li>
  </ol>
  {callout("<b>From scratch vs built-in.</b> You implement a linked list so you understand pointers. In production you use <code>Array</code> and <code>Map</code> unless you need the pointer structure (LRU, explicit nodes). Interviews want both: you can write it, and you know when not to.")}
  <p>Phase 1 on this hub is extra volume in TypeScript after you can teach these structures. Do not skip typing JS here.</p>
  ''', "topics")
    return f'''
<section class="block" id="howto" data-search="How to learn DSA from scratch" data-stype="Section">
  <p class="kicker">Method</p>
  <h2 class="section-title">How to learn</h2>
  {t}
</section>
'''


def jsmodel() -> str:
    t1 = topic("js-ref", "Values, references, and why mutations surprise you",
               "JavaScript references primitives objects heap", "Lesson", f'''
  <p>JavaScript values are either <b>primitives</b> (number, string, boolean, null, undefined, symbol, bigint) or <b>objects</b> (arrays, functions, maps, your nodes). Assignment of a primitive copies the value. Assignment of an object copies the <b>reference</b> — another arrow to the same box.</p>
  {code("JavaScript", '''let a = 1;
let b = a;
b = 2;
// a is still 1

const x = { n: 1 };
const y = x;
y.n = 2;
// x.n is 2 — same object

function bump(obj) {
  obj.n += 1;          // mutates caller
  obj = { n: 0 };      // rebinds local only
}
''')}
  <p>This is why linked-list and tree code is “pointer” code even though JS has no <code>*</code>. A node is an object. <code>curr.next = prev</code> redirects an arrow.</p>
  {diagram("""stack (names)          heap (objects)
head  ──────────────►  { val: 1, next: ──► { val: 2, next: null } }
curr  ──────────────┘""")}
  {callout("Arrays are objects. <code>const a = b</code> does not copy elements. <code>[...b]</code> or <code>b.slice()</code> is a shallow copy — nested objects are still shared.")}
  ''', "topics")

    t2 = topic("js-cost", "What JS actually makes cheap",
               "JavaScript array Map cost V8", "Lesson", f'''
  <p>You do not need V8 internals. You need the costs interviewers expect:</p>
  <table>
    <tr><th>Operation</th><th>Typical cost</th><th>Note</th></tr>
    <tr><td><code>arr[i]</code></td><td>O(1)</td><td>Dense packed arrays</td></tr>
    <tr><td><code>push</code> / <code>pop</code></td><td>amortized O(1)</td><td>End of array</td></tr>
    <tr><td><code>unshift</code> / <code>shift</code></td><td>O(n)</td><td>Rewrites indices</td></tr>
    <tr><td><code>splice</code> in the middle</td><td>O(n)</td><td>Moves the tail</td></tr>
    <tr><td><code>Map.get/set</code></td><td>average O(1)</td><td>Quote average</td></tr>
    <tr><td><code>obj[key]</code></td><td>average O(1)</td><td>Keys are strings/symbols</td></tr>
    <tr><td>string <code>+</code> in a loop</td><td>often O(n²)</td><td>Strings are immutable — push to array, <code>join</code></td></tr>
  </table>
  {code("JavaScript", '''// Bad
let s = "";
for (const ch of chars) s += ch; // new string each time

// Good
const parts = [];
for (const ch of chars) parts.push(ch);
const s = parts.join("");
''')}
  ''', "topics")

    return f'''
<section class="block" id="jsmodel" data-search="JavaScript memory references arrays" data-stype="Section">
  <p class="kicker">The language</p>
  <h2 class="section-title">JS as a machine</h2>
  <p class="lede">DSA in JS is pointer-and-array thinking with a garbage collector. Learn the costs, then forget micro-optimizing V8.</p>
  {t1}{t2}
</section>
'''


def bigo() -> str:
    t1 = topic("bo-feel", "If n doubles, what happens?",
               "Big O JavaScript complexity", "Lesson", f'''
  <p>Big O is how work <b>grows</b>, ignoring constants. Interviewers want you to read <i>your</i> loops.</p>
  <table>
    <tr><th>Class</th><th>Feel when n doubles</th><th>JS shape</th></tr>
    <tr><td>O(1)</td><td>same</td><td>index, Map get</td></tr>
    <tr><td>O(log n)</td><td>one extra step</td><td>binary search, balanced tree height</td></tr>
    <tr><td>O(n)</td><td>twice the work</td><td>one <code>for</code> over n</td></tr>
    <tr><td>O(n log n)</td><td>~ sort-shaped</td><td><code>array.sort</code>, many heap ops</td></tr>
    <tr><td>O(n²)</td><td>four times</td><td>nested loops both to n</td></tr>
    <tr><td>O(2<sup>n</sup>)</td><td>explodes</td><td>unmemoized branching recursion</td></tr>
  </table>
  {code("JavaScript", '''function sum(a) {           // O(n) time, O(1) extra space
  let s = 0;
  for (const x of a) s += x;
  return s;
}
function hasDupNaive(a) {   // O(n²)
  for (let i = 0; i < a.length; i++)
    for (let j = i + 1; j < a.length; j++)
      if (a[i] === a[j]) return true;
  return false;
}
function hasDup(a) {        // O(n) time, O(n) space
  const seen = new Set();
  for (const x of a) {
    if (seen.has(x)) return true;
    seen.add(x);
  }
  return false;
}
''')}
  <p>Space: extra arrays, maps, and recursion depth count. The input itself is usually not “extra.” Recursion depth of n is O(n) stack space.</p>
  {callout("<b>n = 10<sup>6</sup>.</b> O(n) is fine. O(n log n) is usually fine. O(n²) is not. Say this out loud when you pick an approach.")}
  ''', "topics")

    return f'''
<section class="block" id="bigo" data-search="Big O from scratch JavaScript" data-stype="Section">
  <p class="kicker">Language of growth</p>
  <h2 class="section-title">Big O</h2>
  {t1}
</section>
'''
