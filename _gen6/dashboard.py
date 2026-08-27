def dashboard() -> str:
    return r'''
<section class="block" id="dashboard" data-search="DSA JavaScript from scratch dashboard" data-stype="Section">
  <p class="kicker">From scratch → expert · JavaScript only</p>
  <h2 class="section-title">DSA using JavaScript</h2>
  <p class="lede">This course teaches data structures and algorithms by <b>building them in JavaScript</b>, then using them in interview problems and in real frontend/fullstack work. Phase 1 on this hub is the Atlassian pattern gym (TypeScript problem bank). Use this file first if you want the foundations; use Phase 1 when you are already fluent and need volume.</p>

  <div class="card" style="margin-bottom:16px">
    <h3>How this is different</h3>
    <div class="profile-row">
      <span class="chip">Language: JavaScript</span>
      <span class="chip">You implement the structure</span>
      <span class="chip">Then you solve</span>
      <span class="chip">Then you apply it at work</span>
    </div>
    <p class="stat-sub" style="margin-top:12px">Every structure is explained as: what it is, how JS stores it (references, arrays vs objects vs <code>Map</code>), how you would write it from scratch, complexity, when a built-in is enough, and a practical study. Practice problems are labeled practice — not claimed official company questions.</p>
  </div>

  <div class="grid grid-2" style="margin-bottom:16px">
    <div class="card">
      <h3>You will be able to</h3>
      <ul class="tight">
        <li>Explain Big O using your own JS loops and allocations</li>
        <li>Implement list, stack, queue, tree, heap, graph, trie, union-find</li>
        <li>Choose array vs <code>Map</code> vs object vs set for a reason</li>
        <li>Trace recursion, BFS/DFS, and DP on paper and in the debugger</li>
        <li>Solve easy → hard problems without memorizing a recipe only</li>
        <li>Map structures onto product work: LRU, undo, autocomplete, deps</li>
      </ul>
    </div>
    <div class="card">
      <h3>How to use this file</h3>
      <ol class="tight">
        <li>Open the <b>35-Day Plan</b>. Check every box.</li>
        <li>Read the named lesson. Type the implementation — do not only read.</li>
        <li>Do the named problem standing up. Reveal after you have code.</li>
        <li>Do the practical study (where this shows up in a real app).</li>
        <li>Weekly: Mock Interview Mode. Save a debrief.</li>
        <li>Then grind Phase 1’s problem bank if you want Atlassian volume.</li>
      </ol>
    </div>
  </div>

  <div class="grid grid-3">
    <div class="card"><div class="stat-sub">Days / daily tasks</div><div class="stat" id="stat-days">0%</div><div class="bar"><span id="bar-days"></span></div></div>
    <div class="card"><div class="stat-sub">Lessons</div><div class="stat" id="stat-arch">0%</div><div class="bar"><span id="bar-arch"></span></div></div>
    <div class="card"><div class="stat-sub">Practical studies</div><div class="stat" id="stat-react">0%</div><div class="bar"><span id="bar-react"></span></div></div>
    <div class="card"><div class="stat-sub">Q&amp;A</div><div class="stat" id="stat-qs">0 / 0</div><div class="bar"><span id="bar-qs"></span></div></div>
    <div class="card"><div class="stat-sub">Problems</div><div class="stat" id="stat-sd">0 / 0</div><div class="bar"><span id="bar-sd"></span></div></div>
    <div class="card"><div class="stat-sub">Mock interviews</div><div class="stat" id="stat-mocks">0</div><p class="stat-sub">Target 8–10</p></div>
    <div class="card"><div class="stat-sub">Overall readiness</div><div class="stat" id="stat-ready">0%</div><div class="bar"><span id="bar-ready"></span></div></div>
    <div class="card"><div class="stat-sub">Items to review</div><div class="stat" id="stat-review">0</div></div>
    <div class="card"><div class="stat-sub">Implement drills</div><div class="stat" id="stat-ex">0 / 0</div><div class="bar"><span id="bar-ex"></span></div></div>
  </div>
  <div class="callout" style="margin-top:18px">
    <b>Progress.</b> <code>localStorage</code> key <code>dsa-js-v1</code> on this browser only. Separate from Phase 1 (<code>atl-phase1-v1</code>).
  </div>
</section>
'''
