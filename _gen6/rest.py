from util import callout


def mock() -> str:
    return r'''
<section class="block" id="mock" data-search="Mock Interview Mode DSA JavaScript" data-stype="Section">
  <p class="kicker">Timed practice</p>
  <h2 class="section-title">Mock Interview Mode</h2>
  <p class="lede">Draws a random practice item from the problem bank and Q&amp;A (<code>data-mock</code>). Speak: constraints → brute → intended complexity → code → trace. Reveal after you have an approach. Save a debrief.</p>
  <div class="card" style="margin-bottom:16px">
    <p>Category
      <select id="mock-cat">
        <option value="all">All</option>
        <option value="array">array</option>
        <option value="hash">hash</option>
        <option value="string">string</option>
        <option value="js">javascript</option>
        <option value="window">window</option>
        <option value="twopointer">two pointer</option>
        <option value="stack">stack</option>
        <option value="list">list</option>
        <option value="tree">tree</option>
        <option value="heap">heap</option>
        <option value="graph">graph</option>
        <option value="search">search</option>
        <option value="dp">dp</option>
        <option value="backtrack">backtrack</option>
        <option value="prefix">prefix</option>
        <option value="design">design</option>
        <option value="practical">practical</option>
        <option value="complexity">complexity</option>
      </select>
    </p>
    <div class="status-btns">
      <button type="button" class="toggle-btn" data-start-mock="15">15-min question</button>
      <button type="button" class="toggle-btn" data-start-mock="30">30-min problem</button>
      <button type="button" class="toggle-btn" data-start-mock="45">45-min problem</button>
      <button type="button" class="toggle-btn" data-start-mock="60">60-min teach-back</button>
    </div>
    <div id="mock-panel"><p class="stat-sub">Pick a duration. Narrate before you type. Reveal only after you have a complexity and an approach.</p></div>
  </div>
  <div class="card">
    <h3>Debrief rubric</h3>
    <label class="task"><input type="checkbox" id="mock-q-trade" /> <span>I named a brute force and why the chosen approach is better</span></label>
    <label class="task"><input type="checkbox" id="mock-q-time" /> <span>I stated time and extra space out loud</span></label>
    <label class="task"><input type="checkbox" id="mock-q-a11y" /> <span>I traced an example and one edge case (empty / one / duplicate)</span></label>
    <p>Notes<br /><textarea id="mock-notes" rows="3" style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:inherit"></textarea></p>
    <p>Confidence
      <select id="mock-confidence">
        <option value="1">1</option><option value="2">2</option>
        <option value="3" selected>3</option><option value="4">4</option><option value="5">5</option>
      </select>
    </p>
    <p><button type="button" class="toggle-btn" id="save-mock">Save mock</button></p>
  </div>
  <div class="card" style="margin-top:16px"><h3>History</h3><div id="mock-history"></div></div>
</section>
'''


def progress() -> str:
    return r'''
<section class="block" id="progress" data-search="Progress Tracker DSA JavaScript" data-stype="Section">
  <p class="kicker">localStorage dsa-js-v1</p>
  <h2 class="section-title">Progress Tracker</h2>
  <div class="grid grid-2">
    <div class="card"><h3>Daily tasks</h3><p id="track-days">0</p></div>
    <div class="card"><h3>Lessons</h3><p id="track-arch">0</p><div class="bar"><span id="bar-cat-arch"></span></div></div>
    <div class="card"><h3>Practical studies</h3><p id="track-react">0</p><div class="bar"><span id="bar-cat-react"></span></div></div>
    <div class="card"><h3>Interview questions</h3><p id="track-qs">0</p></div>
    <div class="card"><h3>Problems</h3><p id="track-sd">0</p><div class="bar"><span id="bar-cat-sd"></span></div></div>
    <div class="card"><h3>Implement drills</h3><p id="track-ex">0</p></div>
  </div>
  <p style="margin-top:18px"><button type="button" class="danger-btn" id="reset-progress">Reset all DSA JavaScript progress</button></p>
</section>
<section class="block" id="revision" data-search="Revision spaced repetition DSA JavaScript" data-stype="Section">
  <p class="kicker">Remember on purpose</p>
  <h2 class="section-title">Revision System</h2>
  <p class="lede">Solved items review at 1 → 3 → 7 → 14 → 30 days. Attempted/failed → tomorrow. Mastered parks at 30 days.</p>
  <div class="grid grid-2">
    <div class="card"><h3>Due today</h3><ul class="tight" id="rev-today"></ul></div>
    <div class="card"><h3>Due this week</h3><ul class="tight" id="rev-week"></ul></div>
    <div class="card"><h3>Recently failed</h3><ul class="tight" id="rev-failed"></ul></div>
    <div class="card"><h3>Weak areas</h3><ul class="tight" id="rev-weak"></ul></div>
    <div class="card"><h3>Mastered</h3><ul class="tight" id="rev-mastered"></ul></div>
  </div>
</section>
'''


def readiness() -> str:
    groups = [
        ("From scratch", [
            ("r-arr", "Implement rotate-in-place and compact-remove without notes"),
            ("r-map", "Explain Map vs object vs Set and when each is wrong"),
            ("r-list", "Implement reverse, merge, and cycle detect on a list"),
            ("r-stq", "Implement a min stack and a queue that is not O(n) shift"),
            ("r-heap", "Implement a binary heap (push/pop/peek) with 2i+1 indexes"),
            ("r-trie", "Implement trie insert / search / startsWith"),
            ("r-uf", "Implement union-find with path compression"),
        ]),
        ("Patterns", [
            ("r-tp", "Solve a two-pointer problem and say why the array must be sorted (or not)"),
            ("r-win", "Solve a variable window and a case where negatives break it"),
            ("r-bfs", "BFS an islands / maze grid and mark on enqueue"),
            ("r-topo", "Kahn-sort a DAG and detect a cycle"),
            ("r-bt", "Write subsets or permutations with a reused path array"),
            ("r-dp", "Write coin change and name the state / transition"),
            ("r-bs", "Binary search and one rotated-array or lower-bound variant"),
        ]),
        ("Explain out loud", [
            ("r-big", "Define Big O, amortized push, and extra vs output space"),
            ("r-js", "Explain unshift, string +=, and sort-without-comparator costs"),
            ("r-bst", "Validate a BST with bounds, not parent-only"),
            ("r-short", "Say when BFS is shortest path and when you need a heap"),
            ("r-lru", "Teach LRU two ways: Map order and DLL + Map"),
            ("r-rec", "Name base case, subproblem, and combination on a tree problem"),
        ]),
        ("Practical", [
            ("r-undo", "Map undo/redo to two stacks"),
            ("r-auto", "Map autocomplete to a trie (and say when a filter is enough)"),
            ("r-dep", "Map package deps to a graph + topo sort"),
            ("r-rate", "Explain a sliding-window rate limiter"),
            ("r-virt", "Explain a virtual list as window + prefix heights"),
            ("r-key", "Explain list reconcile / React keys as a Map join"),
        ]),
        ("Senior behavior", [
            ("r-brute", "Start every mock with brute + target complexity"),
            ("r-edge", "Trace empty / one / duplicate without being asked"),
            ("r-stuck", "Narrate a pattern family when stuck instead of going silent"),
            ("r-phase1", "Know when to leave this file and grind Phase 1 for volume"),
            ("r-teach", "Teach one structure to a rubber duck in 5 minutes from a blank file"),
        ]),
    ]
    html = []
    for title, items in groups:
        html.append(f"<h3>{title}</h3>")
        for id_, label in items:
            html.append(
                f'<label class="task"><input type="checkbox" data-id="{id_}" data-group="readiness" /><span>{label}</span></label>'
            )
    return f'''
<section class="block" id="readiness" data-search="DSA JavaScript readiness checklist" data-stype="Section">
  <p class="kicker">Gate</p>
  <h2 class="section-title">Readiness checklist</h2>
  <p class="lede">Check only if you can do it <i>today</i> without this file. Stay until ~85% and 8+ mocks. Then use Phase 1 on this hub for more problem volume.</p>
  <p class="stat">Score: <span id="ready-score">0%</span></p>
  <div class="bar"><span id="bar-ready-final"></span></div>
  <p id="ready-gate" class="stat-sub"></p>
  {''.join(html)}
</section>
'''


def resources() -> str:
    rows = [
        ("MDN — Array", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array",
         "push, pop, shift, splice, sort, iteration.", "Pairs with the Arrays lesson. Read complexity as 'what the engine must do,' not magic.", "Arrays", False),
        ("MDN — Map", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map",
         "Keys, insertion order, size.", "Official reason LRU can be a Map in JS.", "Hash", False),
        ("MDN — Set", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set",
         "Presence, iteration.", "containsDuplicate and visited sets.", "Hash", False),
        ("MDN — String", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String",
         "Immutability, code units vs for...of.", "After the Strings lesson.", "Strings", False),
        ("MDN — Equality comparisons", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Equality_comparisons_and_sameness",
         "=== vs Object.is vs ==.", "Floyd compares node identity, not val.", "JS model", False),
        ("ECMAScript spec — Map", "https://tc39.es/ecma262/#sec-map-objects",
         "Insertion order is specified.", "Cite this if someone says Map order is undefined.", "Spec", True),
        ("Phase 1 on this hub", "phase1-atlassian-prep.html",
         "TypeScript pattern gym, larger problem bank.", "After you can implement structures from scratch.", "Volume", False),
        ("Visualgo", "https://visualgo.net/en",
         "Animations of list/heap/graph/sort.", "Watch once, then implement without it.", "Visual", True),
        ("Big-O cheat sheet (plain reference)", "https://www.bigocheatsheet.com/",
         "Common structure costs.", "Do not memorize instead of deriving from your own code.", "Complexity", True),
    ]
    cards = []
    for name, url, what, why, topic, opt in rows:
        badge = '<span class="badge badge-opt">Optional</span>' if opt else '<span class="badge badge-pattern">Primary</span>'
        cards.append(f'''
<article class="card" data-search="{name}" data-stype="Resource">
  <div class="meta-row">{badge}</div>
  <h3><a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a></h3>
  <p><b>Teaches.</b> {what}</p>
  <p><b>Why open it.</b> {why}</p>
  <p><b>Course topic.</b> {topic}</p>
</article>''')
    return f'''
<section class="block" id="resources" data-search="Resource library DSA JavaScript" data-stype="Section">
  <p class="kicker">Official first</p>
  <h2 class="section-title">Resource Library</h2>
  <p class="lede">This HTML already contains the teaching. Links are for signatures and specs. Phase 1 is the volume gym after you can build the structures.</p>
  {callout("Practice problems in this course are original teaching items. They are not claimed official interview questions from any company.")}
  <div class="grid grid-2">{''.join(cards)}</div>
</section>
'''


def glossary() -> str:
    terms = [
        ("Adjacency list", "Graph as node → list of neighbors. Default for sparse graphs."),
        ("Amortized O(1)", "Average cost per op if expensive resizes are rare (e.g. push)."),
        ("BFS", "Queue. Level by level. Shortest hops on unweighted graphs."),
        ("Binary search", "Halve a sorted range. Watch lo/hi and mid overflow."),
        ("BST", "Left < node < right (consistent with equals policy). Height is not automatically log n."),
        ("Backtracking", "Choose, recurse, unchoose. Copy the path when you store a result."),
        ("Big O", "Growth of worst-case work (or space) as n grows."),
        ("Cycle (Floyd)", "Two pointers at different speeds meet if a list loops."),
        ("DFS", "Stack or recursion. Paths, components, topo via postorder."),
        ("Dummy node", "Fake list head so insert/merge never special-cases the first real node."),
        ("Heap (binary)", "Array-backed complete tree. Children at 2i+1 and 2i+2."),
        ("Indegree", "Count of incoming edges. Kahn starts at indegree 0."),
        ("Kadane", "Best subarray ending here = max(x, prevEnding + x)."),
        ("Kahn", "Topo sort by peeling indegree-0 nodes. leftover nodes ⇒ cycle."),
        ("LRU", "Evict least recently used. Map insertion order, or Map + doubly linked list."),
        ("Memoization", "Top-down DP: cache answers to a named state."),
        ("Monotonic stack", "Indexes whose values stay increasing or decreasing. Next-greater family."),
        ("Prefix sum", "pref[i] = sum of first i. Range = pref[r] − pref[l]."),
        ("Sliding window", "Two indexes that only move forward. Fixed k or shrink while invalid."),
        ("Tabulation", "Bottom-up DP. Loops from base cases, often rollable."),
        ("Topological order", "A before B if A must happen first. DAG only."),
        ("Trie", "Prefix tree. Each edge is a character. startsWith is O(length)."),
        ("Two pointers", "Lo/hi or slow/fast. Needs an invariant (sorted, or partition)."),
        ("Union-find", "Disjoint sets. find(root) + union. Path compression + rank ≈ O(1)."),
        ("Visited", "Mark when first seen (usually enqueue) so BFS/DFS do not explode."),
    ]
    items = []
    for name, defn in terms:
        items.append(f'<article class="card glossary-item" data-search="{name}"><h3>{name}</h3><p>{defn}</p></article>')
    return f'''
<section class="block" id="glossary" data-search="Glossary DSA JavaScript" data-stype="Section">
  <p class="kicker">Language</p>
  <h2 class="section-title">Glossary</h2>
  <p><input id="glossary-filter" type="search" placeholder="Filter terms..." style="width:100%;max-width:360px;padding:8px 10px;border-radius:8px;border:1px solid var(--border);background:var(--bg);color:inherit" /></p>
  <div class="grid grid-2" style="margin-top:16px">{''.join(items)}</div>
</section>
'''
