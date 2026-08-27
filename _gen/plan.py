DAYS = [
  {
    "n": 1, "title": "Arrays + HashMap foundations",
    "dsa": "Arrays, HashMap mental model, O(1) average lookup",
    "problems": "Two Sum · Contains Duplicate",
    "js": "Execution model: execution context, call stack, heap",
    "learn": "What gets allocated where; why recursion needs a stack; GEC vs function EC",
    "ex": "Implement a frequency counter with Map<string, number>",
    "verbal": "Explain the JavaScript execution model to a peer in 3 minutes.",
    "rev": "Big O notation: O(1), O(n), O(n²) with one example each"
  },
  {
    "n": 2, "title": "HashMap grouping",
    "dsa": "Anagram grouping, canonical keys",
    "problems": "Valid Anagram · Group Anagrams",
    "js": "Scope + lexical environment + variable environment",
    "learn": "Lexical scope vs dynamic scope; inner function looking outward",
    "ex": "Write groupBy(arr, fn) using Map",
    "verbal": "What is lexical scope, and where is it determined?",
    "rev": "Walk through Two Sum out loud: brute force then HashMap"
  },
  {
    "n": 3, "title": "Frequency + prefix products",
    "dsa": "Top-K via count map; prefix/suffix products",
    "problems": "Top K Frequent Elements · Product of Array Except Self",
    "js": "var / let / const and the Temporal Dead Zone",
    "learn": "Hoisting of bindings vs initialization; why TDZ exists",
    "ex": "Predict 8 short hoisting snippets (write answers before running)",
    "verbal": "Difference between var, let, and const — including scope and TDZ.",
    "rev": "HashMap average vs worst-case lookup"
  },
  {
    "n": 4, "title": "Set + sequence problems",
    "dsa": "Set for O(1) membership; longest consecutive run",
    "problems": "Longest Consecutive Sequence · Valid Sudoku",
    "js": "Function declarations vs function expressions vs hoisting",
    "learn": "Why function declarations are callable above their line; why const fn = () => is not",
    "ex": "Write a 6-question hoist quiz and answer it cold",
    "verbal": "What is the Temporal Dead Zone? When does it start and end?",
    "rev": "Anagram key strategies: sort vs count signature"
  },
  {
    "n": 5, "title": "Two pointers — linear scans",
    "dsa": "Opposite pointers on sorted data; palindrome scan",
    "problems": "Valid Palindrome · Two Sum II (sorted)",
    "js": "Closures: lexical scoping and closure creation",
    "learn": "A closure is a function plus the lexical environment it was created in",
    "ex": "Implement makeCounter() and makeAdder(x)",
    "verbal": "What is a closure? Give a production example (React hooks / private state).",
    "rev": "When HashMap beats two pointers and vice versa"
  },
  {
    "n": 6, "title": "Two pointers — 3Sum and water",
    "dsa": "Sorted two-pointer + skip duplicates; max-area invariant",
    "problems": "3Sum · Container With Most Water",
    "js": "Closure traps: loops, stale bindings, memory retention",
    "learn": "var in for-loop vs let; why a closure can keep a large object alive",
    "ex": "Fix a classic var-in-loop bug; then recreate it with let",
    "verbal": "How can closures cause memory leaks?",
    "rev": "Two-pointer recognition clues from yesterday"
  },
  {
    "n": 7, "title": "Week 1 review + first mock",
    "dsa": "Mixed: Two Sum, Anagrams, 3Sum, Container",
    "problems": "Re-solve any two you marked Attempted. Timed 25-min mock from Problem Bank.",
    "js": "this binding overview (preview of week 2)",
    "learn": "Default / implicit / explicit / new / arrow — names only today",
    "ex": "Predict this in 5 one-liners",
    "verbal": "3-minute recap: HashMap vs two pointers vs Set",
    "rev": "All Week 1 problems: mark Review or Mastered"
  },
  {
    "n": 8, "title": "Sliding window — first invariant",
    "dsa": "Fixed vs variable window; buy/sell as one-pass extrema",
    "problems": "Best Time to Buy and Sell Stock · Longest Substring Without Repeating Characters",
    "js": "this: implicit and explicit binding; call / apply / bind",
    "learn": "How the call-site decides this; bound functions",
    "ex": "Write demos for obj.fn(), fn.call(obj), fn.bind(obj)",
    "verbal": "Difference between call, apply, and bind.",
    "rev": "Two pointers vs sliding window: contiguous vs pair from ends"
  },
  {
    "n": 9, "title": "Sliding window — constraint windows",
    "dsa": "At most K replacements; permutation as anagram window",
    "problems": "Longest Repeating Character Replacement · Permutation in String",
    "js": "Arrow functions and lexical this",
    "learn": "Arrows do not have their own this, arguments, or prototype",
    "ex": "Convert a method that breaks as a callback into an arrow or bound fn",
    "verbal": "Why are arrow functions different from regular functions?",
    "rev": "State the sliding-window invariant in one sentence"
  },
  {
    "n": 10, "title": "Minimum windows",
    "dsa": "Shrink-while-valid; need-count maps",
    "problems": "Minimum Size Subarray Sum · Minimum Window Substring",
    "js": "new binding, constructors, and what new actually does",
    "learn": "Create object, set [[Prototype]], bind this, return object if any",
    "ex": "Implement a tiny constructor and an equivalent factory",
    "verbal": "What does the new keyword do, step by step?",
    "rev": "Re-derive min-window shrink condition without looking"
  },
  {
    "n": 11, "title": "Prefix sums",
    "dsa": "Range sums in O(1); complement prefix for subarray sum K",
    "problems": "Range Sum Query (immutable) · Subarray Sum Equals K",
    "js": "Prototype chain and [[Prototype]]",
    "learn": "Lookup walks the chain; own vs inherited properties",
    "ex": "Draw the prototype chain for a literal {}, an array, and a class instance",
    "verbal": "Explain the prototype chain as if drawing on a whiteboard.",
    "rev": "Prefix sum vs sliding window: when the window cannot move monotonically"
  },
  {
    "n": 12, "title": "Stack basics",
    "dsa": "Matching, monotonic candidates, min-on-stack",
    "problems": "Valid Parentheses · Min Stack",
    "js": "Constructor functions vs class syntax",
    "learn": "class is mostly sugar; methods live on .prototype",
    "ex": "Implement the same type as function + as class",
    "verbal": "How does instanceof work?",
    "rev": "Stack recognition: nested matching, next greater, undo"
  },
  {
    "n": 13, "title": "Monotonic stack",
    "dsa": "Next greater; histogram as next-smaller-on-both-sides",
    "problems": "Daily Temperatures · Evaluate Reverse Polish Notation",
    "js": "Object.create and prototype inheritance",
    "learn": "Delegation vs copying; why mutating a prototype is dangerous",
    "ex": "Build a small inherit(Child, Parent) helper",
    "verbal": "Prototype vs class: what is actually different at runtime?",
    "rev": "Monotonic stack invariant (decreasing / increasing)"
  },
  {
    "n": 14, "title": "Week 2 review + mock",
    "dsa": "Window + stack mixed set",
    "problems": "Timed mock: one Medium window + one stack. Re-solve Min Window if shaky.",
    "js": "Event loop introduction (preview of the deep section)",
    "learn": "Call stack, host APIs, task queue, microtask queue",
    "ex": "Predict: console A / setTimeout 0 / Promise.then / console D",
    "verbal": "Explain the event loop without using the word 'async' as a magic wand.",
    "rev": "Week 2 problems: status update + notes on first stuck point"
  },
  {
    "n": 15, "title": "Queue + BFS intro",
    "dsa": "Level-order thinking; multi-source BFS",
    "problems": "Rotting Oranges · Binary Tree Level Order Traversal",
    "js": "Microtasks vs macrotasks",
    "learn": "Promise jobs drain completely before the next task; rendering sits between tasks",
    "ex": "Do event-loop questions 1–5 in the Event Loop section",
    "verbal": "Why do promises use the microtask queue?",
    "rev": "BFS vs DFS: when shortest path / layers matter"
  },
  {
    "n": 16, "title": "Binary search — classic",
    "dsa": "Predicate binary search; insert position",
    "problems": "Binary Search · Search Insert Position",
    "js": "Promise.then chaining and error bubbling",
    "learn": "A then callback enqueues a microtask; thrown errors reject the next promise",
    "ex": "Predict two nested-then traces from the Event Loop section",
    "verbal": "What happens internally when await is encountered?",
    "rev": "Binary search invariant: lo/hi meaning after each step"
  },
  {
    "n": 17, "title": "Binary search on matrices and rotation",
    "dsa": "2D as virtual 1D; rotated min via unsorted half",
    "problems": "Search a 2D Matrix · Find Minimum in Rotated Sorted Array",
    "js": "async/await desugaring",
    "learn": "await value is Promise.resolve(value).then(rest-of-function)",
    "ex": "Rewrite a then-chain as async/await and vice versa",
    "verbal": "Does await block the JavaScript thread? Be precise.",
    "rev": "Why rotated search still works: one half is always sorted"
  },
  {
    "n": 18, "title": "Binary search on answer",
    "dsa": "Search the solution space (Koko); rotated target search",
    "problems": "Search in Rotated Sorted Array · Koko Eating Bananas",
    "js": "Promise.all / allSettled / race / any",
    "learn": "Fail-fast vs settle-all; empty arrays; rejection reasons",
    "ex": "Implement a simplified Promise.all in the Exercises section",
    "verbal": "Difference between Promise.all and Promise.allSettled.",
    "rev": "Recognize 'binary search on answer' from a word problem"
  },
  {
    "n": 19, "title": "Linked list — rewires",
    "dsa": "Dummy nodes; iterative reverse; merge",
    "problems": "Reverse Linked List · Merge Two Sorted Lists",
    "js": "Iterators and generators",
    "learn": "Iterable protocol; yield pauses and returns { value, done }",
    "ex": "Write a range(start, end) generator",
    "verbal": "What is an iterator in JavaScript?",
    "rev": "Dummy-head pattern: why it deletes edge-case branches"
  },
  {
    "n": 20, "title": "Linked list — two pointers",
    "dsa": "Fast/slow cycle; n-from-end with gap",
    "problems": "Linked List Cycle · Remove Nth Node From End",
    "js": "WeakMap, WeakSet, and GC-friendly caches",
    "learn": "Weak keys do not prevent collection; cannot enumerate",
    "ex": "Cache derived data on a DOM/object key via WeakMap",
    "verbal": "Why would you use WeakMap instead of Map?",
    "rev": "Floyd cycle: why they meet if a cycle exists"
  },
  {
    "n": 21, "title": "Week 3 review + mock",
    "dsa": "BS + linked list mixed",
    "problems": "Timed mock: one BS-on-answer + one list. Reorder List if extra time.",
    "js": "Garbage collection and leak patterns",
    "learn": "Mark-sweep idea; detached DOM; forgotten listeners; closure retention",
    "ex": "List 4 leak patterns you have seen in React/Node apps",
    "verbal": "How can JavaScript applications leak memory?",
    "rev": "Linked list + binary search: mark weak problems Review"
  },
  {
    "n": 22, "title": "Trees — recursion core",
    "dsa": "Height, invert, diameter (height + extra state)",
    "problems": "Maximum Depth · Invert Binary Tree · Diameter of Binary Tree",
    "js": "Browser rendering pipeline",
    "learn": "Style → layout → paint → composite; what forces reflow",
    "ex": "Name 5 operations that flush layout (offsetHeight, getBoundingClientRect, ...)",
    "verbal": "Explain layout vs paint vs composite.",
    "rev": "Tree recursion: what you compute on the way down vs up"
  },
  {
    "n": 23, "title": "Trees — balance and views",
    "dsa": "Height-balanced check; BFS right-side view",
    "problems": "Balanced Binary Tree · Binary Tree Right Side View",
    "js": "requestAnimationFrame and long tasks",
    "learn": "rAF aligns with frames; long tasks block input and rendering",
    "ex": "Explain why scroll handlers should be throttled / rAF-batched",
    "verbal": "Why is requestAnimationFrame preferred for visual work?",
    "rev": "Level-order template from memory"
  },
  {
    "n": 24, "title": "BST contracts",
    "dsa": "Inorder sorted property; bounds for validate; LCA in BST",
    "problems": "Validate BST · Lowest Common Ancestor of a BST · Kth Smallest in a BST",
    "js": "Debounce and throttle (implement today)",
    "learn": "Trailing vs leading debounce; throttle guarantees a max rate",
    "ex": "Implement debounce and throttle from the Exercises section",
    "verbal": "Debounce vs throttle — when does each match a product requirement?",
    "rev": "BST vs binary tree: which algorithms need the BST invariant?"
  },
  {
    "n": 25, "title": "Tree construction + more DFS",
    "dsa": "Preorder+inorder rebuild; another DFS grid/tree",
    "problems": "Construct Binary Tree from Preorder and Inorder · Add Two Numbers (list warmup if needed)",
    "js": "memoize and once",
    "learn": "Cache key design; once is a single-fire wrapper",
    "ex": "Implement memoize and once",
    "verbal": "When does memoization become incorrect?",
    "rev": "Index-map trick for inorder positions"
  },
  {
    "n": 26, "title": "Heaps and Top-K",
    "dsa": "Size-K heap; count then heap; distance",
    "problems": "Kth Largest Element · K Closest Points to Origin",
    "js": "Deep clone and flatten",
    "learn": "JSON limits; cycles; structuredClone; Map/Date/undefined",
    "ex": "Implement deepClone (acyclic) and flatten",
    "verbal": "JSON.parse(JSON.stringify) — what does it silently drop?",
    "rev": "When a heap is overkill vs sort vs Quickselect"
  },
  {
    "n": 27, "title": "Grid DFS/BFS",
    "dsa": "Flood fill; graph clone with a visited map",
    "problems": "Number of Islands · Clone Graph",
    "js": "Event emitter",
    "learn": "on/off/emit; snapshot listeners before emit",
    "ex": "Implement a tiny EventEmitter",
    "verbal": "Pub/sub vs passing callbacks — trade-offs in a UI app.",
    "rev": "Grid DFS template: bounds, visited, 4-directions"
  },
  {
    "n": 28, "title": "Graphs — dependencies and multi-source",
    "dsa": "Cycle detection / topo; reverse multi-source DFS",
    "problems": "Course Schedule · Pacific Atlantic Water Flow",
    "js": "Simplified Promise + retry with backoff",
    "learn": "pending/fulfilled/rejected; thenables; microtask settle",
    "ex": "Start Mini Promise or retryWithBackoff from Exercises",
    "verbal": "What are the three Promise states and which transitions are legal?",
    "rev": "Kahn vs DFS cycle detection"
  },
  {
    "n": 29, "title": "Mixed interview set",
    "dsa": "Hard-lite classics used in senior screens",
    "problems": "Trapping Rain Water · Largest Rectangle in Histogram (or Reorder List + Find Median if those are weaker)",
    "js": "LRU cache + concurrency limiter",
    "learn": "Map insertion order; permit pool / queue",
    "ex": "Implement LRU; sketch limiter",
    "verbal": "Why is LRU a favorite frontend-adjacent interview problem?",
    "rev": "Pattern quiz: 10 prompts → name the pattern in 15 seconds each"
  },
  {
    "n": 30, "title": "Full mock + Phase 1 gate",
    "dsa": "One Easy + one Medium, timed, spoken",
    "problems": "Random mock from Mock Interview Mode. Then one weak Medium from Review.",
    "js": "Event loop questions 11–20 + 5 JS bank answers out loud",
    "learn": "Close gaps from the Readiness Checklist",
    "ex": "Record yourself (phone) explaining Two Sum and the event loop",
    "verbal": "Full communication dry-run using the 10-step framework",
    "rev": "Complete the Final Readiness Checklist honestly. Schedule Phase 2 only if ≥ 85%."
  },
]


def plan() -> str:
    cards = []
    for d in DAYS:
        n = d["n"]
        tasks = [
            ("DSA topic", d["dsa"]),
            ("Problems", d["problems"]),
            ("JavaScript", d["js"]),
            ("Learn", d["learn"]),
            ("Practical exercise", d["ex"]),
            ("Verbal interview question", d["verbal"]),
            ("Revision", d["rev"]),
        ]
        body = []
        for i, (label, text) in enumerate(tasks):
            tid = f"day{n}-t{i}"
            body.append(
                f'<label class="task"><input type="checkbox" data-id="{tid}" data-group="checks" />'
                f"<span><b>{label}</b>{text}</span></label>"
            )
        cards.append(
            f'''<article class="day" id="day-{n}">
  <button type="button" class="day-head">
    <div>
      <h3>Day {n} — {d["title"]}</h3>
      <div class="day-meta">~2 hours · 10 min revision · 50–60 min DSA · 40–45 min JS · 10–15 min speaking</div>
    </div>
    <span class="badge badge-pattern">Day {n}</span>
  </button>
  <div class="day-body">
    {''.join(body)}
  </div>
</article>'''
        )
    return f'''
<section class="block" id="plan" data-search="30-Day Study Plan" data-stype="Section">
  <p class="kicker">Schedule</p>
  <h2 class="section-title">30-Day Study Plan</h2>
  <p class="lede">Six days a week of focused work. Days 7, 14, 21, 28, and 30 are review + mock days — treat them as interviews, not rest. Expand a day, check every task. Checkboxes persist in this browser.</p>
  <div class="card" style="margin-bottom:16px">
    <h3>Daily cadence (≈ 2 hours)</h3>
    <table>
      <tr><th>Time</th><th>Block</th><th>Rule</th></tr>
      <tr><td>10 min</td><td>Revision</td><td>Yesterday’s notes + one weak problem. No new topics.</td></tr>
      <tr><td>50–60 min</td><td>DSA</td><td>Read the pattern, then solve the named problems from the Problem Bank. Speak out loud.</td></tr>
      <tr><td>40–45 min</td><td>JavaScript</td><td>Study the named topic in JS Deep Dive. Write the exercise. Do not only read.</td></tr>
      <tr><td>10–15 min</td><td>Speaking</td><td>Answer the verbal question as if a bar-raiser is in the room.</td></tr>
    </table>
    <p class="stat-sub">If you miss a day, do not double DSA volume the next day. Finish the missed day’s verbal + one problem, then continue. Coverage beats exhaustion.</p>
  </div>
  {''.join(cards)}
</section>
'''
