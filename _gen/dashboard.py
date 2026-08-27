def dashboard() -> str:
    return r'''
<section class="block" id="dashboard" data-search="Dashboard Overview Phase 1" data-stype="Section">
  <p class="kicker">Phase 1 · India · Senior track</p>
  <h2 class="section-title">ATlassian Senior SWE — Phase 1 Preparation</h2>
  <p class="lede">DSA + JavaScript Deep Dive. One offline document. Open it every day. Do not start Phase 2 until the readiness checklist is honest.</p>

  <div class="card" style="margin-bottom:16px">
    <h3>Candidate profile</h3>
    <div class="profile-row">
      <span class="chip">Experience: 7 years</span>
      <span class="chip">Stack: React · TypeScript · JavaScript · Node.js</span>
      <span class="chip">Target: Atlassian</span>
      <span class="chip">Roles: Senior SWE / Senior Frontend / Full-stack</span>
      <span class="chip">Location: India</span>
    </div>
    <p class="stat-sub" style="margin-top:12px">This is not a competitive-programming camp. Atlassian senior interviews reward clear problem-solving, communication, production-quality JavaScript, and honest complexity analysis. Obscure tricks lose to clean reasoning.</p>
  </div>

  <div class="grid grid-2" style="margin-bottom:16px">
    <div class="card">
      <h3>Phase 1 goals</h3>
      <ul class="tight">
        <li>Master common DSA patterns and recognize them from the prompt</li>
        <li>Solve Easy problems confidently in 10–15 minutes</li>
        <li>Solve Medium problems within interview time (~25–35 minutes)</li>
        <li>Explain algorithmic reasoning out loud, including trade-offs</li>
        <li>Master JavaScript runtime: contexts, closures, <code>this</code>, prototypes</li>
        <li>Understand the event loop, microtasks, and async/await internals</li>
        <li>Become interview-ready in TypeScript/JavaScript, not just “able to code”</li>
      </ul>
    </div>
    <div class="card">
      <h3>Target metrics</h3>
      <ul class="tight">
        <li><b>DSA:</b> 60–80 high-quality problems, not 300 rushed ones</li>
        <li><b>Daily study:</b> ~2 hours/day</li>
        <li><b>Cadence:</b> 6 days/week (Day 7/14/21/28 are review + mock)</li>
        <li><b>Mocks:</b> at least 4–6 timed sessions before Phase 2</li>
        <li><b>JS bank:</b> answer 80 questions out loud, not silently</li>
        <li><b>Event loop:</b> predict 20+ traces without guessing</li>
      </ul>
    </div>
  </div>

  <div class="grid grid-3">
    <div class="card">
      <div class="stat-sub">DSA Progress</div>
      <div class="stat" id="stat-dsa">0%</div>
      <div class="bar"><span id="bar-dsa"></span></div>
    </div>
    <div class="card">
      <div class="stat-sub">JavaScript Progress</div>
      <div class="stat" id="stat-js">0%</div>
      <div class="bar"><span id="bar-js"></span></div>
    </div>
    <div class="card">
      <div class="stat-sub">Problems Completed</div>
      <div class="stat" id="stat-problems">0 / 0</div>
      <div class="bar"><span id="bar-problems"></span></div>
    </div>
    <div class="card">
      <div class="stat-sub">Problems To Review</div>
      <div class="stat" id="stat-review">0</div>
      <p class="stat-sub">Spaced-repetition due + marked Review</p>
    </div>
    <div class="card">
      <div class="stat-sub">Mock Interviews Completed</div>
      <div class="stat" id="stat-mocks">0</div>
      <p class="stat-sub">Target 4–6 before Phase 2</p>
    </div>
    <div class="card">
      <div class="stat-sub">Overall Readiness</div>
      <div class="stat" id="stat-ready">0%</div>
      <div class="bar"><span id="bar-ready"></span></div>
    </div>
  </div>

  <div class="callout" style="margin-top:18px">
    <b>How to use this file every day.</b> Open the 30-day plan, finish that day’s checkboxes, solve the named problems in the Problem Bank (mark status), then study the named JavaScript topic and answer the verbal question out loud. Progress is stored in <code>localStorage</code> on this browser only.
  </div>
</section>
'''
