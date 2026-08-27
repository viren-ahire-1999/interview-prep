from util import topic, callout, diagram


def dashboard() -> str:
    return r'''
<section class="block" id="dashboard" data-search="Phase 4 Dashboard Interview Readiness" data-stype="Section">
  <p class="kicker">Phase 4 · Execution</p>
  <h2 class="section-title">ATlassian Senior SWE — Phase 4</h2>
  <p class="lede">Interview Execution + Behavioral + Mock Interviews. Phases 1–3 built the skill. This file turns it into a loop you can run on a calendar.</p>

  <div class="card" style="margin-bottom:16px">
    <h3>Candidate profile</h3>
    <div class="profile-row">
      <span class="chip">Experience: 7 years</span>
      <span class="chip">Stack: React · TypeScript · JavaScript · Node.js</span>
      <span class="chip">Target: Atlassian Senior SWE / Frontend / Full-stack</span>
    </div>
    <p class="stat-sub" style="margin-top:12px">Positioning to practice: a senior engineer who owns scalable frontend and full-stack systems — not “a React developer who also knows Node.” Stories must be yours. Examples in this file are labeled <b>example</b>. Official Atlassian process/values are labeled <b>official</b> and linked. Everything else is general senior-interview practice.</p>
  </div>

  <div class="card" style="margin-bottom:16px">
    <div class="ring-wrap">
      <div class="ring" id="ready-ring" style="--p:0"><span id="ready-ring-n">0%</span></div>
      <div>
        <div class="score-label" id="ready-band">Not Ready</div>
        <p class="stat-sub" id="ready-explain">Score = Technical 30% + System design 20% + Frontend 15% + Behavioral 15% + Communication 10% + Values 5% + Execution 5%. Bands: &lt;50 Not Ready · 50–69 Needs Work · 70–84 Interview Ready · ≥85 Strongly Ready.</p>
      </div>
    </div>
  </div>

  <div class="grid grid-3">
    <div class="card"><div class="stat-sub">Technical</div><div class="stat" id="stat-tech">0%</div><div class="bar"><span id="bar-tech"></span></div></div>
    <div class="card"><div class="stat-sub">Behavioral / stories</div><div class="stat" id="stat-beh">0%</div><div class="bar"><span id="bar-beh"></span></div></div>
    <div class="card"><div class="stat-sub">Values</div><div class="stat" id="stat-val">0%</div><div class="bar"><span id="bar-val"></span></div></div>
    <div class="card"><div class="stat-sub">Communication</div><div class="stat" id="stat-comms">0%</div><div class="bar"><span id="bar-comms"></span></div></div>
    <div class="card"><div class="stat-sub">Mock-loop</div><div class="stat" id="stat-loop">0%</div><div class="bar"><span id="bar-loop"></span></div></div>
    <div class="card"><div class="stat-sub">Days / checklist</div><div class="stat" id="stat-days">0%</div><div class="bar"><span id="bar-days"></span></div></div>
  </div>
  <div class="callout" style="margin-top:18px"><b>Daily use.</b> Fill stories from real work. Run one mock. Speak TMAY and Why Atlassian out loud. Progress key <code>atl-phase4-v1</code>.</div>
</section>
'''


def process() -> str:
    return f'''
<section class="block" id="process" data-search="Atlassian interview process official" data-stype="Section">
  <p class="kicker">Know the source</p>
  <h2 class="section-title">Interview Process Overview</h2>
  <p class="lede">Processes change by role, level, and location. Confirm every loop with your recruiter. This section separates official public material from practice assumptions.</p>

  <div class="callout official">
    <b>Official source.</b> Atlassian publishes an engineering interview handbook:
    <a href="https://www.atlassian.com/company/careers/resources/interviewing/engineering" target="_blank" rel="noopener">atlassian.com/company/careers/resources/interviewing/engineering</a>.
    Values: <a href="https://www.atlassian.com/company/values" target="_blank" rel="noopener">atlassian.com/company/values</a>.
    Careers hub: <a href="https://www.atlassian.com/company/careers" target="_blank" rel="noopener">atlassian.com/company/careers</a>.
    Re-read those pages before your loop. This file is not a substitute for recruiter email.
  </div>

  {topic("proc-official", "What Atlassian says publicly (official)", "official coding system design manager values hiring committee", "Official", '''
  <p>Summarized from the public engineering handbook (as of this file’s writing). Not a guarantee of your loop.</p>
  <ul class="tight">
    <li><b>Coding.</b> They describe assessing problem-solving and learning agility, not language trivia. You can typically choose a language. They mention a coding stage with <i>Data Structures</i> and <i>Code Design</i> parts. Clean thinking and trade-offs matter more than a missing line.</li>
    <li><b>System design (~60 min in the handbook).</b> Not “write production code.” They want how you explore a problem: questions, reliability, cost, who you’d partner with, technologies you’d use. Problems <i>ladder</i> — follow-ups get harder or easier. Multiple viable answers.</li>
    <li><b>Manager interview.</b> Usually hiring manager or a more senior manager. Who you are, what you want, how you collaborate, past projects including <i>why</i> the work existed (business justification).</li>
    <li><b>Values interview.</b> Alignment with the five published values. Values ≠ office culture. Interviewer is often <i>not</i> on the hiring team (could be another function). Informal-feeling, still evaluative. Official design guide also mentions STAR and ~45 minutes for values — confirm your invite.</li>
    <li><b>Hiring Committee.</b> After interviews, feedback is consolidated. A committee reviews independently (feedback + CV) for a consistent decision.</li>
  </ul>
  <p>They also state they do not hire against one perfect candidate profile, and they invite accommodation requests via the talent partner.</p>
  ''', "topics")}

  {topic("proc-practice", "Practice assumptions (not official)", "practice interview loop dimensions", "Practice", '''
  <p class="callout practice"><b>Practice assumption.</b> Many senior loops look like: recruiter screen → one or more coding / craft rounds → system design → hiring manager → values → committee. <b>Your</b> invite may differ (take-home, extra design, no second coding, India vs other regions). Do not argue with a recruiter using this paragraph.</p>
  <table>
    <tr><th>Dimension</th><th>What “good” looks like in a senior loop</th></tr>
    <tr><td>Coding / DS</td><td>Clarify, choose a structure, talk complexity, test edges, take hints</td></tr>
    <tr><td>Code design / craft</td><td>APIs, extensibility, naming, tests — not only the happy path</td></tr>
    <tr><td>Frontend craft</td><td>React runtime, performance, a11y, architecture judgment (Phase 2)</td></tr>
    <tr><td>System design</td><td>Numbers, contracts, failure, trade-offs (Phase 3)</td></tr>
    <tr><td>Management</td><td>Scope, motivation, conflict, mentoring, career</td></tr>
    <tr><td>Values / behavioral</td><td>Real stories, other people in the frame, customer impact, honesty</td></tr>
  </table>
  ''', "topics")}
</section>
'''


def positioning() -> str:
    return f'''
<section class="block" id="positioning" data-search="Personal Positioning senior engineer" data-stype="Section">
  <p class="kicker">How you introduce the work</p>
  <h2 class="section-title">Personal Positioning</h2>
  <p class="lede">Anchor: <i>Senior engineer with 7 years building scalable frontend and full-stack systems in React, TypeScript, JavaScript, and Node.js.</i> The stack is evidence. The claim is ownership, architecture, and impact.</p>
  {topic("pos-levels", "Weak vs better vs senior positioning", "positioning ownership architecture impact", "Positioning", f'''
  <table>
    <tr><th>Level</th><th>Example (labeled example — not your bio)</th><th>Why it fails or works</th></tr>
    <tr><td>Weak</td><td class="example">“I’m a React developer with 7 years. I also know Node and Redux.”</td><td>Identity = library list. No scope, no customer, no judgment.</td></tr>
    <tr><td>Better</td><td class="example">“I’ve spent 7 years on product frontends in React/TS, and I work across the API when the problem needs it.”</td><td>Still tool-first, but acknowledges the boundary.</td></tr>
    <tr><td>Strong senior</td><td class="example">“I’m a senior engineer. I own user-facing systems end to end — UI architecture, data fetching, and the Node services those screens depend on — and I care about what the customer can do after we ship.”</td><td>Ownership + boundary + customer. Stack is implied.</td></tr>
  </table>
  <p>Practice replacing adjectives with <b>scope</b> (who used it), <b>constraint</b> (what was hard), and <b>decision</b> (what you chose not to do).</p>
  <ul class="tight">
    <li>Ownership — “I was the point of contact when X failed.”</li>
    <li>Architecture — “I set the boundary so 8 people could ship without colliding.”</li>
    <li>Product impact — “Support tickets for Y dropped; we measured Z.”</li>
    <li>Depth — “I can walk the React commit path or the cache invalidation.”</li>
    <li>Scale — users, teams, payload, or time-to-restore — pick a real number you own.</li>
    <li>Leadership — influence, mentoring, reviews — without claiming a title you don’t have.</li>
    <li>Collaboration — named counterpart (PM, backend, support), not “we.”</li>
  </ul>
  {callout("Write your one-sentence positioning in the notes box on the Dashboard after you can say it without looking. Do not invent scale.")}
  ''', "topics")}
</section>

<section class="block" id="tmay" data-search="Tell me about yourself 30 60 90 120 seconds" data-stype="Section">
  <p class="kicker">Opening</p>
  <h2 class="section-title">Tell Me About Yourself</h2>
  <p class="lede">Structure: Present → Experience → Strongest areas → Impact → Current scope → What I want → Why Atlassian (one clause). Not a chronological CV. Not your childhood.</p>
  {topic("tmay-struct", "Timed versions — fill with YOUR facts", "tell me about yourself framework", "TMAY", '''
  <p><b>Avoid:</b> reciting every job; diving into Fiber; “passionate team player”; long personal origin stories unless asked.</p>
  <p class="example"><b>Example 30s (structure only — replace facts):</b> “I’m a senior engineer with seven years on product UIs and the Node APIs behind them. Recently I’ve owned [mention one surface]. I’m looking for a place where collaboration software is the product — that’s why I’m talking to Atlassian.”</p>
  <p class="example"><b>Example 60s:</b> Add one concrete impact and one technical strength (e.g. performance or architecture). One sentence on current scope (what you decide vs escalate).</p>
  <p class="example"><b>Example 90s:</b> Add a second domain (mentoring or cross-team) and a honest “why now.”</p>
  <p class="example"><b>Example 2 min:</b> Only if they lean in. One project arc: problem → decision → result → lesson. Then stop and ask what they want to go deep on.</p>
  <div class="field"><label>Your 60-second draft (saved locally)</label><textarea id="note-tmay" data-note="tmay" placeholder="Write only facts you can defend."></textarea></div>
  ''', "topics")}
</section>

<section class="block" id="why" data-search="Why Atlassian why this role why now" data-stype="Section">
  <p class="kicker">Motivation without fan fiction</p>
  <h2 class="section-title">Why Atlassian?</h2>
  <p class="lede">Four questions: Why them? Why this role? Why now? Why you? Do not invent a childhood Jira story. Connect real work to real products and published values.</p>
  {topic("why-frame", "Framework + labeled examples", "why Atlassian role now hire me", "Motivation", '''
  <ol>
    <li><b>Product gravity.</b> You have used (or can speak precisely about) issue tracking, docs, or boards as a <i>collaboration system</i>, not a ticket UI.</li>
    <li><b>Craft match.</b> Long-lived frontends, plugins, permissions, search — Phase 2/3 language.</li>
    <li><b>Values you can evidence.</b> One official value you have actually lived (openness, customer, team, change, balance).</li>
    <li><b>Why now.</b> Scope you want: more architecture + customer surface, not “I need a brand name.”</li>
    <li><b>Why you.</b> 7 years of shipping UI+API; you reduce integration risk between frontend and backend. No fake FAANG.</li>
  </ol>
  <table>
    <tr><th></th><th>Example (not your words)</th></tr>
    <tr><td>Weak</td><td class="example">“Atlassian is a great company with great culture and I love Jira.”</td></tr>
    <tr><td>Good</td><td class="example">“I want to work on tools people use every day to coordinate work. My last three years were React/TS systems that other teams depended on.”</td></tr>
    <tr><td>Strong senior</td><td class="example">“I’m choosing Atlassian because the product is multi-team collaboration at scale — permissions, search, reliability — and that’s the class of problem I’ve been growing into. I can talk frontend architecture and the Node/API side without throwing the problem over a wall. I want a values interview that actually happens, not a poster.”</td></tr>
  </table>
  <p>Personalize by naming <i>one</i> product behavior you respect (e.g. how boards encode workflow) and <i>one</i> thing you want to learn. Reciting the careers homepage is a bad signal.</p>
  <div class="field"><label>Your Why Atlassian draft</label><textarea id="note-why" data-note="why"></textarea></div>
  ''', "topics")}
</section>
'''
