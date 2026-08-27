def dashboard() -> str:
    return r'''
<section class="block" id="dashboard" data-search="Frontend System Design Expert Course Dashboard" data-stype="Section">
  <p class="kicker">Expert track · Frontend system design</p>
  <h2 class="section-title">Frontend System Design — one-stop course</h2>
  <p class="lede">This file is the study environment. Theory first, then full case studies, then interview questions you answer standing up. Practice items are labeled practice — not claimed official company questions. Do not call yourself ready until the readiness checklist is honest.</p>

  <div class="card" style="margin-bottom:16px">
    <h3>Who this is for</h3>
    <div class="profile-row">
      <span class="chip">Experience: 7 years</span>
      <span class="chip">Stack: React · TypeScript · JavaScript · Node.js</span>
      <span class="chip">Roles: Senior SWE / Senior Frontend / Full-stack</span>
      <span class="chip">Use with: Atlassian phases on the hub</span>
    </div>
    <p class="stat-sub" style="margin-top:12px">Phase 2 on this hub teaches React runtime and production architecture. This course is the <b>product design interview</b>: you are given a surface (feed, board, editor, chat, dashboard) and 45–60 minutes to own requirements, client architecture, data, performance, failure, security, and accessibility. The senior answer is a decision record, not a library name.</p>
  </div>

  <div class="grid grid-2" style="margin-bottom:16px">
    <div class="card">
      <h3>You will be able to</h3>
      <ul class="tight">
        <li>Run a 16-step frontend system-design conversation on a timer</li>
        <li>Choose CSR / SSR / SSG / streaming / islands for a reason</li>
        <li>Place state (URL, server cache, local, ephemeral) on purpose</li>
        <li>Design fetch, cache keys, invalidation, races, and optimistic UI</li>
        <li>Degrade realtime, offline, and plugins instead of pretending they are free</li>
        <li>Connect LCP / INP / CLS to concrete component and network decisions</li>
        <li>Treat a11y, XSS, authz, and observability as architecture</li>
        <li>Walk 18 product case studies and 24 timed design prompts</li>
      </ul>
    </div>
    <div class="card">
      <h3>How to use this file</h3>
      <ol class="tight">
        <li>Open the <b>28-Day Plan</b>. Check every box.</li>
        <li>Read the named theory section. Draw the diagram. Do not only highlight.</li>
        <li>Do the named case or design standing up. Reveal after you have a plan.</li>
        <li>Answer the day’s verbal question. Then uncover the bank.</li>
        <li>Weekly: Mock Interview Mode (30 / 45 / 60). Save a debrief.</li>
        <li>Leave when Readiness is honestly ~85% and you have 8+ mocks.</li>
      </ol>
    </div>
  </div>

  <div class="grid grid-3">
    <div class="card"><div class="stat-sub">Days / daily tasks</div><div class="stat" id="stat-days">0%</div><div class="bar"><span id="bar-days"></span></div></div>
    <div class="card"><div class="stat-sub">Theory topics</div><div class="stat" id="stat-arch">0%</div><div class="bar"><span id="bar-arch"></span></div></div>
    <div class="card"><div class="stat-sub">Case studies</div><div class="stat" id="stat-react">0%</div><div class="bar"><span id="bar-react"></span></div></div>
    <div class="card"><div class="stat-sub">Interview questions</div><div class="stat" id="stat-qs">0 / 0</div><div class="bar"><span id="bar-qs"></span></div></div>
    <div class="card"><div class="stat-sub">Design prompts</div><div class="stat" id="stat-sd">0 / 0</div><div class="bar"><span id="bar-sd"></span></div></div>
    <div class="card"><div class="stat-sub">Mock interviews</div><div class="stat" id="stat-mocks">0</div><p class="stat-sub">Target 8–10 across modes</p></div>
    <div class="card"><div class="stat-sub">Overall readiness</div><div class="stat" id="stat-ready">0%</div><div class="bar"><span id="bar-ready"></span></div></div>
    <div class="card"><div class="stat-sub">Items to review</div><div class="stat" id="stat-review">0</div><p class="stat-sub">Spaced repetition due today</p></div>
    <div class="card"><div class="stat-sub">ADR / talk drills</div><div class="stat" id="stat-ex">0 / 0</div><div class="bar"><span id="bar-ex"></span></div></div>
  </div>
  <div class="callout" style="margin-top:18px">
    <b>Progress.</b> Stored in <code>localStorage</code> under <code>fe-sd-v1</code> on this browser only. Different from the Atlassian phase keys. After you switch from <code>file://</code> to the GitHub Pages URL, progress starts fresh once.
  </div>
</section>
'''
