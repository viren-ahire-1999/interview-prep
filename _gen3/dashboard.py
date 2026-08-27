def dashboard() -> str:
    return r'''
<section class="block" id="dashboard" data-search="Phase 3 Dashboard System Design" data-stype="Section">
  <p class="kicker">Phase 3 · Senior track</p>
  <h2 class="section-title">ATlassian Senior SWE — Phase 3</h2>
  <p class="lede">System Design + Distributed Systems + Backend Architecture. Goal: run a 45–60 minute design conversation like a senior who owns customer impact, not a backend specialist who recites Kafka.</p>

  <div class="card" style="margin-bottom:16px">
    <h3>Candidate profile</h3>
    <div class="profile-row">
      <span class="chip">Experience: 7 years</span>
      <span class="chip">Stack: React · TypeScript · JavaScript · Node.js</span>
      <span class="chip">Target: Atlassian</span>
      <span class="chip">Roles: Senior SWE / Senior Frontend / Full-stack</span>
    </div>
    <p class="stat-sub" style="margin-top:12px">Phase 1 (DSA + JS runtime) and Phase 2 (frontend architecture) are assumed. Phase 3 teaches you to design the systems those frontends talk to: APIs, data, caches, events, failure, and consistency — with Jira / Confluence / Trello-shaped examples. Practice questions are labeled practice, not official Atlassian questions.</p>
  </div>

  <div class="grid grid-2" style="margin-bottom:16px">
    <div class="card">
      <h3>Phase 3 objectives</h3>
      <ul class="tight">
        <li>Design scalable systems and defend the trade-offs</li>
        <li>Reason about high traffic with numbers, not adjectives</li>
        <li>Understand distributed-system failure modes</li>
        <li>Design APIs, databases, caches, and event paths</li>
        <li>Handle retries, idempotency, and consistency on purpose</li>
        <li>Connect frontend architecture to backend contracts</li>
        <li>Run a 45–60 minute system-design interview coherently</li>
      </ul>
    </div>
    <div class="card">
      <h3>How this differs from a buzzword tutorial</h3>
      <ul class="tight">
        <li>Every major choice answers: why, why not, 10× scale, failure, retries, cost</li>
        <li>Microservices, Kafka, and NoSQL are tools — not default answers</li>
        <li>You will calculate RPS, storage, and cache size</li>
        <li>You will say “not yet” to sharding and distributed locks</li>
      </ul>
    </div>
  </div>

  <div class="grid grid-3">
    <div class="card"><div class="stat-sub">System design topics</div><div class="stat" id="stat-sd">0%</div><div class="bar"><span id="bar-sd"></span></div></div>
    <div class="card"><div class="stat-sub">Distributed systems</div><div class="stat" id="stat-dist">0%</div><div class="bar"><span id="bar-dist"></span></div></div>
    <div class="card"><div class="stat-sub">Backend / Node.js</div><div class="stat" id="stat-backend">0%</div><div class="bar"><span id="bar-backend"></span></div></div>
    <div class="card"><div class="stat-sub">Case studies</div><div class="stat" id="stat-cases">0 / 0</div><div class="bar"><span id="bar-cases"></span></div></div>
    <div class="card"><div class="stat-sub">Mock interviews</div><div class="stat" id="stat-mocks">0</div><p class="stat-sub">Target 6–8 timed rounds</p></div>
    <div class="card"><div class="stat-sub">Overall readiness</div><div class="stat" id="stat-ready">0%</div><div class="bar"><span id="bar-ready"></span></div></div>
    <div class="card"><div class="stat-sub">Days / daily tasks</div><div class="stat" id="stat-days">0%</div><div class="bar"><span id="bar-days"></span></div></div>
    <div class="card"><div class="stat-sub">Interview questions</div><div class="stat" id="stat-qs">0 / 0</div><div class="bar"><span id="bar-qs"></span></div></div>
    <div class="card"><div class="stat-sub">Exercises + designs</div><div class="stat" id="stat-ex">0 / 0</div><div class="bar"><span id="bar-ex"></span></div></div>
  </div>
  <div class="callout" style="margin-top:18px">
    <b>Daily use.</b> Open the 45-day plan → study the named section → do the named design or exercise → answer the verbal question out loud. Progress is <code>localStorage</code> key <code>atl-phase3-v1</code>.
  </div>
</section>
'''
