def rest() -> str:
    return r'''
<section class="block" id="comms" data-search="Interview communication Atlassian speak aloud" data-stype="Section">
  <p class="kicker">How you talk</p>
  <h2 class="section-title">Interview Communication Practice</h2>
  <p class="lede">Atlassian senior interviews grade how you think, not only the final code. Silence looks like stuck. Narration looks like leadership. Use this 10-step script until it is muscle memory.</p>

  <div class="comm-step"><div class="comm-num">1</div><div>
    <h3>Clarify requirements</h3>
    <p class="say">“I’ll first clarify the constraints. Is the array sorted? Can values be negative? Should I return indices or values? What should I do if there is no answer — throw, null, or empty?”</p>
    <p>Ask about duplicates, stability, mutation, integer overflow, and whether they want a function signature in TypeScript.</p>
  </div></div>
  <div class="comm-step"><div class="comm-num">2</div><div>
    <h3>State assumptions</h3>
    <p class="say">“I’ll assume inputs fit in memory, n can be 10⁵ so I need linear or n log n, and I may allocate O(n) extra unless you want in-place.”</p>
    <p>Write assumptions at the top of the editor. If they are wrong, the interviewer will correct you now, not after 20 minutes.</p>
  </div></div>
  <div class="comm-step"><div class="comm-num">3</div><div>
    <h3>Describe brute force</h3>
    <p class="say">“The brute-force approach would be to try every pair. That is O(n²) time and O(1) extra. It’s correct, and I’d ship it if n were 20.”</p>
    <p>Brute force proves you understand the problem. Seniors do not skip it; they dismiss it with a reason.</p>
  </div></div>
  <div class="comm-step"><div class="comm-num">4</div><div>
    <h3>Identify the bottleneck</h3>
    <p class="say">“The bottleneck is repeated lookup — for each i I rescan the rest of the array for the complement.”</p>
    <p>Name the wasted work: repeated scans, repeated sorts, repeated height computations, single-source BFS that should have been multi-source.</p>
  </div></div>
  <div class="comm-step"><div class="comm-num">5</div><div>
    <h3>Derive the optimal approach</h3>
    <p class="say">“To reduce this from O(n²) to O(n), I’ll use a HashMap from value to index. As I scan, I ask whether target − x is already stored.”</p>
    <p>Name the pattern. State the invariant in one sentence. If you cannot, you are not ready to code.</p>
  </div></div>
  <div class="comm-step"><div class="comm-num">6</div><div>
    <h3>Explain the data structure</h3>
    <p class="say">“Map gives expected O(1) get/set. I’ll mention worst-case O(n) if they care; in practice V8’s Map is fine. Space is O(n).”</p>
    <p>If you choose a heap in JS, say you will sort if n is small, or implement a 30-line heap, or use a PriorityQueue API.</p>
  </div></div>
  <div class="comm-step"><div class="comm-num">7</div><div>
    <h3>Code while communicating</h3>
    <p class="say">“I’m creating the map. I’m looking up the complement before I insert so I don’t use the same index twice. I’ll name variables so you can read this without me.”</p>
    <p>Do not go silent for five minutes. If you need quiet, say “I need 60 seconds to write the loop, then I’ll narrate.” Use TypeScript types as documentation.</p>
  </div></div>
  <div class="comm-step"><div class="comm-num">8</div><div>
    <h3>Test edge cases</h3>
    <p class="say">“Empty input — I’ll guard. Single element. Duplicates: [3,3] target 6. Negatives. Already-sorted. I’ll walk the example line by line.”</p>
    <p>Dry-run the example they gave you. Then one mean case. Fix bugs before they point them out.</p>
  </div></div>
  <div class="comm-step"><div class="comm-num">9</div><div>
    <h3>Explain complexity</h3>
    <p class="say">“Time O(n) expected, space O(n). If memory were tight I would sort and two-pointer in O(n log n) time and O(1) extra, but I’d lose original indices unless I store pairs.”</p>
  </div></div>
  <div class="comm-step"><div class="comm-num">10</div><div>
    <h3>Discuss alternatives</h3>
    <p class="say">“I could binary-search each complement after sorting — worse. I could use two pointers if you allowed me to sort. In production I would extract the map into a well-named helper and add a test for the duplicate-index case.”</p>
    <p>This is the senior beat: trade-offs, testability, what you would not do.</p>
  </div></div>

  <div class="card">
    <h3>Two Sum — full spoken script (practice this verbatim once)</h3>
    <p class="say">“I’ll first clarify: return any valid pair of indices? Are there negatives? Exactly one solution — good. I won’t mutate the input.
      Brute force is nested loops, O(n²). The bottleneck is scanning for the complement. I’ll keep a Map from value to index. For each x, if target−x is in the map, return those indices; otherwise store x.
      That is O(n) time and O(n) space. Edge case [3,3], 6 works because I look up before insert. I’ll type it in TypeScript and walk the sample [2,7,11,15], 9: store 2 at 0, then 7 finds 2.”</p>
  </div>
  <div class="callout">Atlassian values: be the teammate who makes the problem smaller, states risks, and writes readable code. Arrogance and silent genius score worse than a correct brute force you then improve.</div>
</section>

<section class="block" id="mock" data-search="Mock interview mode timer" data-stype="Section">
  <p class="kicker">Simulate the room</p>
  <h2 class="section-title">Mock Interview Mode</h2>
  <p class="lede">Random problem from the bank. Timer on. Speak the 10-step framework. Reveal hint/solution only after you have a plan. Save a debrief so the Revision board can see patterns.</p>
  <div class="card" style="margin-bottom:16px">
    <div class="status-btns">
      <button type="button" class="toggle-btn" id="start-mock">Start Mock Interview</button>
    </div>
    <div id="mock-panel"><p class="stat-sub">Click Start to draw a random problem. Suggested time: Easy 15 min · Medium 30 min · Hard 40 min.</p></div>
  </div>
  <div class="card">
    <h3>Debrief (after you stop)</h3>
    <label class="task"><input type="checkbox" id="mock-q-pattern" /> <span>I identified the pattern in the first 4 minutes</span></label>
    <label class="task"><input type="checkbox" id="mock-q-time" /> <span>I solved (or had a correct plan + mostly-correct code) within time</span></label>
    <label class="task"><input type="checkbox" id="mock-q-complex" /> <span>I stated time and space complexity out loud</span></label>
    <label class="task"><input type="checkbox" id="mock-q-edges" /> <span>I tested edge cases on the microphone</span></label>
    <p>Confidence
      <select id="mock-confidence">
        <option value="1">1 — lost</option>
        <option value="2">2 — shaky</option>
        <option value="3" selected>3 — ok</option>
        <option value="4">4 — solid</option>
        <option value="5">5 — teach it</option>
      </select>
    </p>
    <p><button type="button" class="toggle-btn" id="save-mock">Save mock to history</button></p>
  </div>
  <div class="card" style="margin-top:16px">
    <h3>History</h3>
    <div id="mock-history"></div>
  </div>
</section>

<section class="block" id="revision" data-search="Revision dashboard spaced repetition" data-stype="Section">
  <p class="kicker">Remember on purpose</p>
  <h2 class="section-title">Revision System</h2>
  <p class="lede">Lightweight spaced repetition. When you mark a problem <b>Solved</b>, the next review is in 1 day, then 3, 7, 14, 30. <b>Attempted</b> or a failed review → tomorrow. <b>Mastered</b> parks it at a 30-day horizon. This page reads those dates from localStorage.</p>
  <div class="grid grid-2">
    <div class="card"><h3>Due today</h3><ul class="tight" id="rev-today"></ul></div>
    <div class="card"><h3>Due this week</h3><ul class="tight" id="rev-week"></ul></div>
    <div class="card"><h3>Recently / frequently failed</h3><ul class="tight" id="rev-failed"></ul></div>
    <div class="card"><h3>Weak topics</h3><ul class="tight" id="rev-topics"></ul></div>
    <div class="card"><h3>Frequently failed patterns</h3><ul class="tight" id="rev-patterns"></ul></div>
    <div class="card"><h3>Mastered</h3><ul class="tight" id="rev-mastered"></ul></div>
  </div>
</section>

<section class="block" id="progress" data-search="Progress tracker reset" data-stype="Section">
  <p class="kicker">Local only</p>
  <h2 class="section-title">Progress Tracker</h2>
  <p class="lede">Stored in <code>localStorage</code> key <code>atl-phase1-v1</code> on this browser. Clearing site data wipes it. Export is: you keep the file; the file does not phone home.</p>
  <div class="grid grid-2">
    <div class="card">
      <h3>Daily plan tasks</h3>
      <p id="track-days">0 / 0</p>
      <div class="bar"><span id="bar-days"></span></div>
    </div>
    <div class="card">
      <h3>DSA topics marked complete</h3>
      <p id="track-topics">0</p>
    </div>
    <div class="card">
      <h3>JavaScript topics + exercises</h3>
      <p id="track-js">0</p>
    </div>
    <div class="card">
      <h3>JS questions completed</h3>
      <p id="track-qs">0</p>
    </div>
  </div>
  <p style="margin-top:18px"><button type="button" class="danger-btn" id="reset-progress">Reset all progress</button></p>
  <p class="stat-sub">Asks for confirmation. Keeps your theme preference.</p>
</section>

<section class="block" id="readiness" data-search="Phase 1 readiness checklist" data-stype="Section">
  <p class="kicker">Gate to Phase 2</p>
  <h2 class="section-title">Final Phase 1 Readiness Checklist</h2>
  <p class="lede">Check a box only if you can do it <i>today</i>, out loud, without this document. Score is the percent checked. Do not start system design / Atlassian-specific Phase 2 until this is honestly around 85%+.</p>
  <p class="stat">Score: <span id="ready-score">0%</span></p>
  <div class="bar"><span id="bar-ready-final"></span></div>
  <p id="ready-gate" class="stat-sub"></p>
  <h3>DSA</h3>
''' + _checks([
        ("Explain Big O including average vs worst case and amortized", "r-bigo"),
        ("Solve Two Sum in under 10 minutes with a spoken HashMap explanation", "r-twosum"),
        ("Identify the HashMap / complement pattern from a new prompt", "r-hashpat"),
        ("Identify Sliding Window from contiguous + constraint language", "r-swpat"),
        ("Identify Two Pointers on sorted / palindrome / area prompts", "r-tppat"),
        ("Write a bug-free binary search and a binary search on the answer", "r-bs"),
        ("Implement BFS with a queue and level-size minutes", "r-bfs"),
        ("Implement DFS flood fill / 3-color cycle detection", "r-dfs"),
        ("Traverse trees: depth, invert, diameter, level order", "r-trees"),
        ("Explain when to use a heap / top-K vs sort", "r-heap"),
        ("Solve common Easy problems in 10–15 minutes", "r-easy"),
        ("Solve common Medium problems in ~25–35 minutes", "r-med"),
    ]) + '''
  <h3>JavaScript</h3>
''' + _checks([
        ("Explain execution context, call stack, and heap", "r-ec"),
        ("Explain closures and a stale-closure React example", "r-cl"),
        ("Explain this: default, implicit, explicit, new, arrows", "r-this"),
        ("Explain the prototype chain and instanceof", "r-proto"),
        ("Explain promises, states, and all vs allSettled vs race vs any", "r-prom"),
        ("Explain what await does to the function and the thread", "r-await"),
        ("Explain the event loop with a drawn diagram", "r-el"),
        ("Distinguish microtasks vs tasks and place rAF", "r-micro"),
        ("Explain 4 JS leak patterns and how you would debug one", "r-leak"),
        ("Explain style / layout / paint / composite and forced reflow", "r-rend"),
    ]) + '''
  <h3>Interview behavior</h3>
''' + _checks([
        ("Think aloud without going silent for more than a minute", "r-talk"),
        ("Clarify requirements and state assumptions first", "r-clar"),
        ("Explain trade-offs (time vs space, sort vs hash, DFS vs BFS)", "r-trade"),
        ("Analyze complexity after coding without being prompted", "r-cx"),
        ("Test edge cases on an example before saying done", "r-edge"),
    ]) + '''
</section>

<section class="block" id="resources" data-search="Resource library LeetCode MDN NeetCode Atlassian" data-stype="Section">
  <p class="kicker">Optional outside this file</p>
  <h2 class="section-title">Resource Library</h2>
  <p class="lede">This HTML already contains Phase 1 explanations, problems, and solutions. Use the links below only when you want a second explanation, official docs, or extra practice volume. Official and high-quality sources only.</p>
''' + _res() + '''
</section>
'''


def _checks(items):
    out = []
    for label, id_ in items:
        out.append(
            f'<label class="task"><input type="checkbox" data-id="{id_}" data-group="readiness" />'
            f"<span>{label}</span></label>"
        )
    return "".join(out)


def _res():
    rows = [
        ("LeetCode", "https://leetcode.com/",
         "The standard judge for typed practice.",
         "Paste a problem from this bank into LeetCode when you want hidden tests. Optional if you dry-run here.",
         "DSA problem bank", True),
        ("NeetCode", "https://neetcode.io/",
         "Pattern-organized video explanations and a well-known 150 list.",
         "Use if a visual walk-through helps after you attempted the problem here. Optional.",
         "Pattern recognition", True),
        ("MDN JavaScript", "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
         "Canonical language and Web API reference.",
         "Look up exact semantics (Promise, TDZ, event loop in HTML spec links). Primary docs; this file teaches the mental model.",
         "JS deep dive", False),
        ("javascript.info", "https://javascript.info/",
         "Long-form tutorials with excellent diagrams (closures, prototypes, event loop).",
         "Optional second pass if you want more prose after this file’s JS sections.",
         "JS runtime, event loop", True),
        ("HTML Living Standard — event loop", "https://html.spec.whatwg.org/multipage/webappapis.html#event-loop-processing-model",
         "The actual processing model browsers implement.",
         "Advanced. Read after you can predict the 20 traces. Optional for Phase 1, impressive if cited accurately.",
         "Event loop", True),
        ("ECMA-262", "https://tc39.es/ecma262/",
         "The JavaScript language spec (jobs, promises, environments).",
         "Optional. Use for ‘what does await really do’ after the deep dive.",
         "Promises, execution contexts", True),
        ("Atlassian Engineering blog", "https://www.atlassian.com/blog/atlassian-engineering",
         "How Atlassian teams write about production systems, frontend scale, and reliability.",
         "Culture and taste — not DSA. Skim a few posts so your conversation sounds like you researched the company. Optional for Phase 1 mechanics.",
         "Company context", True),
        ("Atlassian careers / interview info", "https://www.atlassian.com/company/careers",
         "Official careers surface; role descriptions for India SWE / frontend.",
         "Confirm the role family you are targeting. Process details change — treat blog posts and recruiter mail as source of truth for loops.",
         "Positioning", False),
        ("Atlassian Design System", "https://atlassian.design/",
         "Design tokens, components, accessibility guidance used in Atlassian products.",
         "Optional in Phase 1. Useful later for frontend-system and UI-quality conversations.",
         "Frontend taste", True),
        ("React docs (beta/learn)", "https://react.dev/learn",
         "Official React mental model: rendering, effects, hooks.",
         "Phase 1 only needs the JS-under-React pieces (closures, identity, batching). Optional deeper React is Phase 2+.",
         "React-related JS", True),
        ("web.dev performance", "https://web.dev/explore/performance",
         "INP, rendering, long tasks — Google’s web performance curriculum.",
         "Optional backup to the rendering/memory sections here.",
         "Browser / performance", True),
        ("TypeScript handbook", "https://www.typescriptlang.org/docs/handbook/intro.html",
         "Official TS language handbook.",
         "You already write TS; use this if a type puzzle blocks you. Optional.",
         "TS fluency", True),
        ("Frontend Interview Handbook", "https://www.frontendinterviewhandbook.com/",
         "Community handbook: JS, UI, algorithms for frontend interviews.",
         "Optional extra prompts. Prefer this file’s banks first so you do not dilute focus.",
         "Frontend interviews", True),
        ("System Design Primer", "https://github.com/donnemartin/system-design-primer",
         "Classic system-design outline.",
         "Phase 2+. Labeled so you do not disappear into design during Phase 1.",
         "Later phases", True),
        ("ByteByteGo (system design)", "https://bytebytego.com/",
         "Visual system-design explanations.",
         "Optional, Phase 2+. Do not substitute for DSA/JS this month.",
         "Later phases", True),
    ]
    cards = []
    for name, url, what, why, helps, optional in rows:
        badge = '<span class="badge badge-opt">Optional</span>' if optional else '<span class="badge badge-pattern">Use when needed</span>'
        cards.append(f'''
<article class="card" data-search="{name}" data-stype="Resource">
  <div class="meta-row">{badge}</div>
  <h3><a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a></h3>
  <p><b>What it is.</b> {what}</p>
  <p><b>Why you would open it.</b> {why}</p>
  <p><b>Phase 1 topic.</b> {helps}</p>
</article>''')
    return '<div class="grid grid-2">' + "".join(cards) + "</div>"
