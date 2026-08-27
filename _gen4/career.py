from util import topic, callout, esc

ASK_CATEGORIES = [
    ("Role", [
        "What would success look like for this hire in the first 6 and 12 months — and who defines it?",
        "How much of the role is greenfield vs evolving an existing surface that customers already depend on?",
        "Where does this team sit in the org — who are the upstream product partners and downstream platform teams?",
        "What is the split between feature delivery, reliability work, and tech debt in a typical quarter?",
        "Is this role backfill or new headcount — what gap opened?",
    ]),
    ("Team", [
        "How is the team structured — pods, triads, or horizontal specialties?",
        "What does code review culture look like here — speed vs depth?",
        "How do frontend and backend engineers share ownership on user-facing features?",
        "What is the on-call expectation and how is incident load distributed?",
        "How does the team handle disagreement on technical direction?",
    ]),
    ("Technical", [
        "What are the hardest technical problems this team is working on right now?",
        "Where does most latency or reliability pain show up — browser, API, or async pipelines?",
        "How do you balance shipping features vs paying down frontend or platform debt?",
        "What does the local dev experience look like for a full-stack change?",
        "What quality bar must pass before a feature reaches production?",
    ]),
    ("Architecture", [
        "How do you draw boundaries between product code, shared libraries, and platform services?",
        "What is the default persistence and caching story for a new feature?",
        "How do you handle multi-tenant isolation in practice — not just in docs?",
        "When did the team last reverse a major architectural decision — what triggered it?",
        "How are cross-team API contracts versioned and enforced?",
    ]),
    ("Culture", [
        "How do engineers get heard when they disagree with a product direction?",
        "What does 'open company, no bullshit' look like on this team in a typical week?",
        "How is customer pain surfaced to engineers — support, research, metrics?",
        "What rituals exist for learning from incidents without blame?",
        "How do remote/hybrid teammates stay equal participants in decisions?",
    ]),
    ("Growth", [
        "What does the path from senior to staff look like on this team — expectations, not titles?",
        "How are engineers supported to present RFCs or lead cross-team initiatives?",
        "What learning budget or conference policy exists and how is it used in practice?",
        "Who would be my manager and how do they think about career development?",
        "What skills do seniors here wish they had built two years earlier?",
    ]),
    ("Leadership", [
        "How do seniors influence roadmap without being a people manager?",
        "What does mentoring look like — formal pairing or organic?",
        "How are tech leads chosen for large initiatives?",
        "How does the team develop junior/mid engineers toward ownership?",
        "When influence fails, what escalation path exists?",
    ]),
    ("Product", [
        "How does engineering participate in discovery before commitment?",
        "What metric or customer outcome is this team accountable for?",
        "How do you decide when to cut scope vs extend a timeline?",
        "What is a recent example where engineering pushed back on a ship date?",
        "How do beta/experiment flags fit your release process?",
    ]),
    ("DX", [
        "What is the CI/CD pipeline latency for a typical frontend change?",
        "How long from merged PR to production for your team?",
        "What are the top three developer productivity pain points you're tackling?",
        "How is technical documentation maintained — ADRs, runbooks, or tribal knowledge?",
        "What internal tools does this team depend on daily?",
    ]),
]

REJ_CATEGORIES = [
    "Knowledge", "Communication", "Coding speed", "Architecture",
    "Behavioral", "Confidence", "Preparation", "Misunderstanding",
]

TECHCHECK_ITEMS = [
    ("tc-clarify", "Did I clarify requirements and constraints before coding/designing?"),
    ("tc-assume", "Did I state assumptions explicitly?"),
    ("tc-approach", "Did I explain my approach before diving into details?"),
    ("tc-complex", "Did I discuss time/space complexity or scale numbers?"),
    ("tc-edges", "Did I test or enumerate edge cases?"),
    ("tc-trade", "Did I name trade-offs and alternatives?"),
    ("tc-hints", "Did I listen to hints and incorporate them without defensiveness?"),
    ("tc-calm", "Did I correct mistakes calmly when pointed out?"),
]


def comms() -> str:
    return f'''
<section class="block" id="comms" data-search="Senior communication thinking aloud trade-offs" data-stype="Section">
  <p class="kicker">Sound like the bar</p>
  <h2 class="section-title">Senior Communication</h2>
  <p class="lede">Atlassian senior loops grade reasoning, not buzzwords. Specificity beats volume. Structure beats speed. These patterns apply to coding, design, and behavioral answers.</p>

  {topic("comms-weak-strong", "Weak vs strong technical statements", "Redis cache trade-off communication", "Communication", '''
  <table>
    <tr><th>Weak (example)</th><th>Strong (example)</th><th>Why</th></tr>
    <tr>
      <td class="example">"I think Redis would work."</td>
      <td class="example">"I'd use Redis here because the access pattern is read-heavy and the data can tolerate ~30s staleness. The trade-off is invalidation complexity on writes — I'd invalidate issue keys on PATCH, not TTL-only."</td>
      <td>Names pattern, acceptable staleness, and cost.</td>
    </tr>
    <tr>
      <td class="example">"We used microservices."</td>
      <td class="example">"We split search out because issue writes and search indexing had different scaling and release cadences. We kept issue+comment in one deployable to avoid distributed transactions on the hot path."</td>
      <td>Constraint-led decision, not fashion.</td>
    </tr>
    <tr>
      <td class="example">"I'm not sure."</td>
      <td class="example">"I haven't implemented CRDTs in production. My model is: each edit is an operation with a causal order; merges must be commutative for convergence. I'd start from the product conflict UX before picking OT vs CRDT."</td>
      <td>Honest gap + reasoning from first principles.</td>
    </tr>
  </table>
  ''', "topics")}

  {topic("comms-think", "Thinking aloud without noise", "narrate interview clarify structure", "Communication", '''
  <ol>
    <li><b>Signpost.</b> "I'll clarify, then brute force, then optimize." Buys time and shows structure.</li>
    <li><b>Pause with purpose.</b> "Give me 45 seconds to write the loop, then I'll walk it." Silence without context reads as stuck.</li>
    <li><b>Name the invariant.</b> One sentence: "The window always contains at most K distinct chars."</li>
    <li><b>Challenge assumptions politely.</b> "Can we mutate the input? If not, I'll copy first."</li>
    <li><b>Close with trade-offs.</b> "This is O(n) space; if memory were tight I'd sort and two-pointer at O(n log n)."</li>
  </ol>
  ''', "topics")}

  {topic("comms-clarify", "Clarifying questions that signal seniority", "requirements assumptions interview", "Communication", '''
  <ul class="tight">
    <li>Who is the user and what breaks if we're wrong?</li>
    <li>Scale: users, QPS, data size, regions?</li>
    <li>Consistency: stale reads OK? Exactly-once needed?</li>
    <li>Failure: fail open or closed? Partial success?</li>
    <li>Scope: MVP in 45 minutes vs production system?</li>
  </ul>
  <p class="say">"Before I draw boxes — is this internal-only or multi-tenant SaaS? What's the read/write ratio? Is search allowed to lag the database?"</p>
  ''', "topics")}

  {callout("Calm correction: 'Good catch — that misses the empty array. I'll guard at the top.' Never argue with the test case.")}
</section>
'''


def unknown() -> str:
    return f'''
<section class="block" id="unknown" data-search="I don't know honest interview no bluffing" data-stype="Section">
  <p class="kicker">Honesty beats bluffing</p>
  <h2 class="section-title">Handling "I Don't Know"</h2>
  <p class="lede">Senior engineers say "I don't know" with a plan. Bluffing destroys values interviews. These frameworks keep you in the conversation.</p>

  {topic("unk-idk", "Core scripts", "unknown technology honest reasoning", "Scripts", '''
  <table>
    <tr><th>Situation</th><th>Say</th><th>Avoid</th></tr>
    <tr><td>Don't know the answer</td><td class="say">"I don't know the exact behavior off the top of my head. I'd verify in docs or a quick experiment. My hypothesis is… because…"</td><td>Inventing API details.</td></tr>
    <tr><td>Unfamiliar technology</td><td class="say">"I haven't operated Kafka in production. I have operated SQS-like queues. I'd expect partitions to give ordering per key and consumer groups for scale — I'd map your problem to those primitives first."</td><td>"Yeah I've used that" when you haven't.</td></tr>
    <tr><td>Haven't built that system</td><td class="say">"I haven't built a collaborative editor. I have built real-time boards with optimistic UI. The hard parts I'd expect are conflict resolution and presence fan-out — here's how I'd de-risk each."</td><td>Reciting Wikipedia without ownership language.</td></tr>
    <tr><td>Unsure of edge behavior</td><td class="say">"I'm not sure whether this API coalesces microtasks across realms. I'd test with a minimal repro before relying on it in design."</td><td>"It always works like X" without evidence.</td></tr>
  </table>
  ''', "topics")}

  {topic("unk-reason", "Reason from the model", "first principles unfamiliar system", "Framework", '''
  <ol>
    <li>State what you <b>do</b> know (adjacent system, constraint, user need).</li>
    <li>Name the unknown explicitly.</li>
    <li>Derive a reasonable approach from first principles or analogous system.</li>
    <li>Say what you'd validate first (metric, prototype, doc).</li>
    <li>Invite correction: "Does that match how you use it here?"</li>
  </ol>
  <p class="example"><b>Example (labeled):</b> "I haven't run Vitest at your scale. Jest with SWC was our default. I'd compare watch-mode IO, ESM interop, and CI shard time — not syntax — before migrating a monorepo."</p>
  ''', "topics")}

  {callout("Values signal: admitting a gap + showing how you'd learn beats faking depth. 'Open company, no bullshit' applies to you too.")}
</section>
'''


def ask() -> str:
    blocks = []
    for cat, qs in ASK_CATEGORIES:
        items = "".join(f"<li>{q}</li>" for q in qs)
        blocks.append(f'''
<article class="topic" data-search="{cat} questions to ask interviewer" data-stype="Ask">
  <h3>{cat}</h3>
  <ul class="tight">{items}</ul>
</article>''')
    total = sum(len(qs) for _, qs in ASK_CATEGORIES)
    return f'''
<section class="block" id="ask" data-search="Questions to ask interviewers thoughtful" data-stype="Section">
  <p class="kicker">{total} questions · not careers-page filler</p>
  <h2 class="section-title">Questions to Ask Interviewers</h2>
  <p class="lede">Pick 3–5 per round that you genuinely care about. Avoid questions answered by the homepage. Tailor with what you learned earlier in the loop.</p>
  {''.join(blocks)}
  {callout("Weak: 'What's the culture like?' Strong: 'How does customer pain reach this team — support queue, metrics, or PM synthesis?'")}
</section>
'''


def recruiter() -> str:
    return f'''
<section class="block" id="recruiter" data-search="Recruiter screen compensation notice period" data-stype="Section">
  <p class="kicker">First conversation</p>
  <h2 class="section-title">Recruiter Conversations</h2>
  <p class="lede">Frameworks, not deceptive tactics. Be accurate, be early on constraints, leave room to negotiate later with data.</p>

  {topic("rec-screen", "Initial screen — what to prepare", "recruiter motivation availability", "Recruiter", '''
  <ul class="tight">
    <li><b>Role fit.</b> 60-second positioning (see Personal Positioning). Stack match + scope you want.</li>
    <li><b>Motivation.</b> Why Atlassian, why this role, why now — honest, not fan fiction.</li>
    <li><b>Location / remote.</b> State constraints clearly. Ask what the role expects.</li>
    <li><b>Timeline.</b> Notice period, other processes, earliest start.</li>
    <li><b>Comp (early).</b> They may ask current and expected. See Compensation section — ranges, not fiction.</li>
  </ul>
  <p class="say">"I'm in active conversation with a few companies. Atlassian is a priority because [specific product/problem]. My notice is [X weeks]. I'd like to understand the interview steps and timing so I can plan accordingly."</p>
  ''', "topics")}

  {topic("rec-fields", "Editable prep (saved locally)", "recruiter notes notice comp", "Prep", '''
  <div class="grid grid-2">
    <div class="field"><label>Current role & scope</label><textarea data-rec="role"></textarea></div>
    <div class="field"><label>Notice period</label><input data-rec="notice" placeholder="e.g. 60 days negotiable to 30" /></div>
    <div class="field"><label>Location / visa constraints</label><textarea data-rec="location"></textarea></div>
    <div class="field"><label>Current compensation (private notes)</label><textarea data-rec="current" placeholder="Your numbers only — not shared in this file"></textarea></div>
    <div class="field"><label>Target / walk-away (strategy)</label><textarea data-rec="target" placeholder="What would make you sign — components, not a single number"></textarea></div>
    <div class="field"><label>Availability for loops</label><input data-rec="avail" placeholder="Timezone, blackout dates" /></div>
  </div>
  ''', "topics")}

  {callout("Do not misrepresent competing offers, tenure, or compensation. Recruiters remember inconsistencies across rounds.")}
</section>
'''


def offer() -> str:
    return f'''
<section class="block" id="offer" data-search="Compensation offer negotiation equity TC" data-stype="Section">
  <p class="kicker">Professional, not adversarial</p>
  <h2 class="section-title">Compensation & Offer</h2>
  <p class="lede">Understand components before negotiating. This section distinguishes <b>known facts</b> (your offer letter, your current pay), <b>market estimates</b> (third-party surveys — verify independently), and <b>strategy</b> (how to have the conversation). No fabricated Atlassian bands or guaranteed ranges.</p>

  {topic("off-components", "Components to clarify", "fixed variable equity sign-on TC level", "Offer", '''
  <table>
    <tr><th>Component</th><th>Clarify</th><th>Type</th></tr>
    <tr><td>Base salary</td><td>Cash, pay cycle, currency, geo band if applicable</td><td>Known fact on letter</td></tr>
    <tr><td>Variable / bonus</td><td>Target %, company vs individual multiplier, payout timing</td><td>Known + policy</td></tr>
    <tr><td>Equity</td><td>RSU vs options, grant size, vest schedule, cliff, refresh policy</td><td>Known fact on letter</td></tr>
    <tr><td>Sign-on / joining bonus</td><td>Clawback period, paid with first payroll or later</td><td>Known fact</td></tr>
    <tr><td>Level</td><td>Title vs internal level — affects future growth</td><td>Known fact</td></tr>
    <tr><td>TC framing</td><td>How they compute "total comp" for conversation</td><td>Strategy — ask them to define</td></tr>
  </table>
  <p class="callout practice"><b>Market estimates</b> come from levels.fyi, Glassdoor, peers — treat as noisy. India vs US bands differ; role and level matter more than company name alone.</p>
  ''', "topics")}

  {topic("off-scripts", "Scripts", "receive offer negotiate decline accept", "Scripts", '''
  <p><b>Receiving an offer.</b></p>
  <p class="say">"Thank you — I'm excited about the team and the problem. I'd like to review the written details and come back with any clarifying questions. What's the timeline you need?"</p>
  <p><b>Clarifying.</b></p>
  <p class="say">"Can you walk me through how variable pay has paid out the last two years? How is the equity grant valued in the offer summary? What's the vesting cliff and refresh cadence for this level?"</p>
  <p><b>Negotiating.</b></p>
  <p class="say">"Based on my scope and the market data I've gathered, I was expecting stronger alignment on [base / equity / sign-on]. Is there flexibility? I'm prioritizing [component] because [reason tied to commitment, not ultimatum]."</p>
  <p><b>More time.</b></p>
  <p class="say">"I want to make a thoughtful decision. I have [other process / personal deadline]. Can we extend the deadline to [date]?"</p>
  <p><b>Declining.</b></p>
  <p class="say">"I've decided to accept another offer that aligns better with [specific dimension]. I appreciated the team's time and transparency."</p>
  <p><b>Accepting.</b></p>
  <p class="say">"I'm happy to accept. Please send the revised letter reflecting [agreed terms]. My start date can be [date]. What are the next steps for background and onboarding?"</p>
  ''', "topics")}

  {topic("off-notes", "Your offer notes (private)", "competing offers strategy", "Notes", '''
  <div class="field"><label>Offer details (paste summary — stays local)</label><textarea data-off="details"></textarea></div>
  <div class="field"><label>Competing processes (facts only)</label><textarea data-off="competing"></textarea></div>
  <div class="field"><label>Negotiation strategy notes</label><textarea data-off="strategy" placeholder="What you'll ask for and why — no bluffing"></textarea></div>
  ''', "topics")}
</section>
'''


def day() -> str:
    return f'''
<section class="block" id="day" data-search="Interview day strategy 24 hours before" data-stype="Section">
  <p class="kicker">Execution hygiene</p>
  <h2 class="section-title">Interview Day Strategy</h2>

  {topic("day-24h", "24 hours before", "sleep prep environment", "Timeline", '''
  <ul class="tight">
    <li>Light revision only — one story, one SD outline, one coding pattern. No new topics.</li>
    <li>Confirm schedule, timezone, links, and interviewers if shared.</li>
    <li>Prepare physical space: camera height, light, quiet, water, charger.</li>
    <li>Clothes ready; reduce morning decisions.</li>
    <li>Sleep target 7+ hours — cognitive performance beats one extra hour of cramming.</li>
  </ul>
  ''', "topics")}

  {topic("day-2h", "2 hours before", "mindset tech check", "Timeline", '''
  <ul class="tight">
    <li>Eat lightly; caffeine if you use it — not more than usual.</li>
    <li>Open this file: Story Bank titles, TMAY draft, Tech Checklist.</li>
    <li>Test mic/camera and screen share if required.</li>
    <li>Close noisy apps; phone on silent; notify household.</li>
  </ul>
  ''', "topics")}

  {topic("day-30m", "30 minutes before", "calm entry", "Timeline", '''
  <ul class="tight">
    <li>Bathroom, water, posture check.</li>
    <li>Two-minute TMAY out loud — stop when done, do not rewrite.</li>
    <li>One calm breath routine: inhale 4, hold 4, exhale 6 — twice.</li>
    <li>Join link 2–3 minutes early, not 15 (avoid awkward idle chat unless culture expects it).</li>
  </ul>
  ''', "topics")}

  {topic("day-during", "During the interview", "think aloud whiteboard", "Timeline", '''
  <ul class="tight">
    <li>Clarify before solving. Write assumptions.</li>
    <li>Narrate at decision points; go quiet only when you said you would code.</li>
    <li>Whiteboard / editor: leave margin, label boxes, date the diagram if multiple versions.</li>
    <li>Hints are gifts — acknowledge and adjust.</li>
    <li>Leave 3–5 minutes for your questions.</li>
  </ul>
  ''', "topics")}

  {topic("day-between", "Between rounds (same day)", "reset energy", "Timeline", '''
  <ul class="tight">
    <li>Stand, walk, water — do not replay mistakes aloud for 20 minutes.</li>
    <li>One sentence debrief: what to adjust next round (pace, clarify, story cut).</li>
    <li>Different story for behavioral if overlap risk with earlier interviewer notes.</li>
  </ul>
  ''', "topics")}

  {topic("day-after", "After the interview", "thank you debrief", "Timeline", '''
  <ul class="tight">
    <li>Within 24h: brief thank-you to recruiter or coordinator if appropriate — specific, short.</li>
    <li>Log debrief in Rejection Analysis (even if it went well — capture what to repeat).</li>
    <li>No post-mortem spiral; one corrective action for next mock.</li>
  </ul>
  ''', "topics")}
</section>
'''


def techcheck() -> str:
    checks = "".join(
        f'<label class="task"><input type="checkbox" data-id="{cid}" data-group="techcheck" /><span>{label}</span></label>'
        for cid, label in TECHCHECK_ITEMS
    )
    return f'''
<section class="block" id="techcheck" data-search="Technical interview checklist clarify assumptions" data-stype="Section">
  <p class="kicker">Every technical round</p>
  <h2 class="section-title">Interview Communication Checklist</h2>
  <p class="lede">Interactive checklist — reset between rounds. Check only what you actually did. Persisted locally.</p>
  <div class="card">
    {checks}
    <p style="margin-top:12px"><button type="button" class="toggle-btn" id="techcheck-reset">Reset checklist</button></p>
  </div>
</section>
'''


def rejection() -> str:
    cats = "".join(f'<option>{c}</option>' for c in REJ_CATEGORIES)
    return f'''
<section class="block" id="rejection" data-search="Rejection feedback analysis debrief" data-stype="Section">
  <p class="kicker">Learn, don't rumination</p>
  <h2 class="section-title">Rejection / Feedback Analysis</h2>
  <p class="lede">Log rounds while memory is fresh. Trend categories to see systemic gaps vs one-off bad days.</p>
  <div class="card">
    <form id="rej-form">
      <div class="grid grid-2">
        <div class="field"><label>Round / company</label><input name="round" data-rejf="round" /></div>
        <div class="field"><label>Category</label><select name="category" data-rejf="category">{cats}</select></div>
      </div>
      <div class="field"><label>Question or prompt</label><textarea name="question" data-rejf="question"></textarea></div>
      <div class="field"><label>What happened</label><textarea name="happened" data-rejf="happened"></textarea></div>
      <div class="field"><label>Where I struggled</label><textarea name="struggled" data-rejf="struggled"></textarea></div>
      <div class="field"><label>Interviewer / recruiter feedback (if any)</label><textarea name="feedback" data-rejf="feedback"></textarea></div>
      <div class="field"><label>Root cause (honest)</label><textarea name="root" data-rejf="root"></textarea></div>
      <div class="field"><label>Corrective action</label><textarea name="action" data-rejf="action"></textarea></div>
      <div class="field"><label>Next review date</label><input type="date" name="review" data-rejf="review" /></div>
      <p><button type="button" class="toggle-btn" id="save-rejection">Save entry</button></p>
    </form>
  </div>
  <div class="card" style="margin-top:16px">
    <h3>Trend by category</h3>
    <div id="rej-chart"></div>
    <div id="rej-list" class="stat-sub"></div>
  </div>
</section>
'''
