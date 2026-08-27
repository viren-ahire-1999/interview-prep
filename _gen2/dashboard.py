def dashboard() -> str:
    return r'''
<section class="block" id="dashboard" data-search="Phase 2 Dashboard Frontend Architecture" data-stype="Section">
  <p class="kicker">Phase 2 · Senior track · India</p>
  <h2 class="section-title">ATlassian Senior SWE — Phase 2</h2>
  <p class="lede">Frontend Architecture + React + Large-Scale Web Engineering. This file is the study environment. Phase 1 (DSA + JS runtime) is assumed. Do not leave Phase 2 until the readiness checklist is honest.</p>

  <div class="card" style="margin-bottom:16px">
    <h3>Candidate profile</h3>
    <div class="profile-row">
      <span class="chip">Experience: 7 years</span>
      <span class="chip">Stack: React · TypeScript · JavaScript · Node.js</span>
      <span class="chip">Target: Atlassian</span>
      <span class="chip">Roles: Senior SWE / Senior Frontend / Full-stack</span>
    </div>
    <p class="stat-sub" style="margin-top:12px">Atlassian products (Jira, Confluence, Trello, Bitbucket) are long-lived, plugin-heavy, multi-team frontends. Senior interviews reward judgment: boundaries, ownership, performance under collaboration load, accessibility, and the ability to say “not yet” to micro-frontends. Practice questions in this file are labeled as practice — not claimed official Atlassian questions.</p>
  </div>

  <div class="grid grid-2" style="margin-bottom:16px">
    <div class="card">
      <h3>Phase 2 objectives</h3>
      <ul class="tight">
        <li>Design scalable frontend systems and defend the trade-offs</li>
        <li>Understand React at runtime: Fiber, render vs commit, scheduling</li>
        <li>Diagnose rendering and interaction-performance problems</li>
        <li>Design state and data-fetching architecture on purpose</li>
        <li>Build reusable component / design-system APIs</li>
        <li>Reason about multi-team React applications</li>
        <li>Connect browser + network costs to Core Web Vitals</li>
        <li>Treat accessibility and security as architecture, not a QA pass</li>
        <li>Run a 45–60 minute frontend system-design conversation</li>
      </ul>
    </div>
    <div class="card">
      <h3>How this differs from Phase 1</h3>
      <ul class="tight">
        <li>Less “write an algorithm,” more “own a surface used by millions”</li>
        <li>Correctness includes a11y, security, observability, and rollback</li>
        <li>The senior answer is rarely a library name; it is a decision record</li>
        <li>Jira/Confluence-shaped examples are used because they match product gravity — not because a specific question is guaranteed</li>
      </ul>
    </div>
  </div>

  <div class="grid grid-3">
    <div class="card"><div class="stat-sub">Days / daily tasks</div><div class="stat" id="stat-days">0%</div><div class="bar"><span id="bar-days"></span></div></div>
    <div class="card"><div class="stat-sub">Architecture topics</div><div class="stat" id="stat-arch">0%</div><div class="bar"><span id="bar-arch"></span></div></div>
    <div class="card"><div class="stat-sub">React topics</div><div class="stat" id="stat-react">0%</div><div class="bar"><span id="bar-react"></span></div></div>
    <div class="card"><div class="stat-sub">Interview questions</div><div class="stat" id="stat-qs">0 / 0</div><div class="bar"><span id="bar-qs"></span></div></div>
    <div class="card"><div class="stat-sub">System design exercises</div><div class="stat" id="stat-sd">0 / 0</div><div class="bar"><span id="bar-sd"></span></div></div>
    <div class="card"><div class="stat-sub">Mock interviews</div><div class="stat" id="stat-mocks">0</div><p class="stat-sub">Target 5–8 across modes</p></div>
    <div class="card"><div class="stat-sub">Overall readiness</div><div class="stat" id="stat-ready">0%</div><div class="bar"><span id="bar-ready"></span></div></div>
    <div class="card"><div class="stat-sub">Items to review</div><div class="stat" id="stat-review">0</div><p class="stat-sub">Spaced repetition due today</p></div>
    <div class="card"><div class="stat-sub">Exercises completed</div><div class="stat" id="stat-ex">0 / 0</div><div class="bar"><span id="bar-ex"></span></div></div>
  </div>
  <div class="callout" style="margin-top:18px">
    <b>Daily use.</b> Open the 30-day plan → study the named section → do the named exercise or design → answer the verbal question out loud. Progress is <code>localStorage</code> key <code>atl-phase2-v1</code> on this browser only.
  </div>
</section>
'''
