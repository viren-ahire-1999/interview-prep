from util import topic, callout

STORY_CATS = [
    "Most impactful project", "Hardest technical problem", "Failure", "Conflict",
    "Disagreement", "Mentoring", "Leadership", "Influencing without authority",
    "Production outage", "Tight deadline", "Ambiguous requirement", "Customer escalation",
    "Technical debt", "Architecture decision", "Performance improvement", "Cost reduction",
    "Process improvement", "Cross-team collaboration", "Difficult teammate",
    "Learning something new", "Mistake", "Innovation",
]

VALUES = [
    "Open company, no bullshit",
    "Build with heart and balance",
    "Don’t #@!% the customer",
    "Play, as a team",
    "Be the change you seek",
]


def framework() -> str:
    return f'''
<section class="block" id="framework" data-search="STAR STAR-L CAR SOAR behavioral framework" data-stype="Section">
  <p class="kicker">How stories become answers</p>
  <h2 class="section-title">Behavioral Framework</h2>
  {topic("fw-models", "STAR, STAR-L, CAR, SOAR", "STAR CAR SOAR story capture", "Framework", f'''
  <table>
    <tr><th>Model</th><th>Use when</th><th>Risk</th></tr>
    <tr><td><b>STAR</b> Situation Task Action Result</td><td>Default. Official design interview guide mentions STAR for values.</td><td>Action becomes a blur of “we.”</td></tr>
    <tr><td><b>STAR-L</b> + Learning</td><td>Failure, conflict, “what would you change.”</td><td>Skipping the L sounds defensive.</td></tr>
    <tr><td><b>CAR</b> Context Action Result</td><td>Short HM answers (60–90s).</td><td>Under-explaining the decision.</td></tr>
    <tr><td><b>SOAR</b> Situation Obstacle Action Result</td><td>When the interesting part is the obstacle (incident, disagreement).</td><td>Obstacle-as-villain, no ownership.</td></tr>
  </table>
  <p>Capture every story with: Situation, Task, <b>your</b> Actions, technical reasoning, trade-offs, stakeholders, Result, Metrics (honest — “we didn’t measure” is allowed), Lessons.</p>
  <p>Speak Actions in first person. “We shipped” without your slice is a mid-level tell.</p>
  {callout("If you cannot name a trade-off, you do not have a senior story yet — you have a status update.")}
  ''', "topics")}
</section>
'''


def stories() -> str:
    cards = []
    for i, cat in enumerate(STORY_CATS):
        cards.append(f'''
<article class="card story-card" data-story="{i}" data-search="{cat} story" data-stype="Story">
  <div class="meta-row"><span class="badge badge-pattern">{cat}</span></div>
  <h3>{cat}</h3>
  <div class="field"><label>Title</label><input data-sf="title" placeholder="Short name you can say aloud" /></div>
  <div class="grid grid-2">
    <div class="field"><label>Situation</label><textarea data-sf="situation"></textarea></div>
    <div class="field"><label>Task</label><textarea data-sf="task"></textarea></div>
    <div class="field"><label>Actions (I…)</label><textarea data-sf="actions"></textarea></div>
    <div class="field"><label>Technical decisions</label><textarea data-sf="tech"></textarea></div>
    <div class="field"><label>Trade-offs</label><textarea data-sf="tradeoffs"></textarea></div>
    <div class="field"><label>Result</label><textarea data-sf="result"></textarea></div>
    <div class="field"><label>Metrics (or “not measured”)</label><textarea data-sf="metrics"></textarea></div>
    <div class="field"><label>What I learned</label><textarea data-sf="learned"></textarea></div>
    <div class="field"><label>What I would change</label><textarea data-sf="change"></textarea></div>
    <div class="field"><label>Atlassian value (if any)</label>
      <select data-sf="value">
        <option value="">—</option>
        {''.join(f'<option>{v}</option>' for v in VALUES)}
      </select>
    </div>
  </div>
  <div class="field"><label>Likely follow-ups</label><textarea data-sf="followups" placeholder="What would a skeptical interviewer ask?"></textarea></div>
</article>''')
    return f'''
<section class="block" id="stories" data-search="Story Bank STAR" data-stype="Section">
  <p class="kicker">Your bank — not fiction</p>
  <h2 class="section-title">Story Bank</h2>
  <p class="lede">Twenty-two slots. Fill 8–12 deeply rather than 22 thinly. Empty is honest. Invented metrics are a values failure. Autosaves to localStorage.</p>
  {''.join(cards)}
</section>
'''


def matrix() -> str:
    # columns: question types, rows: story categories (short)
    qcols = ["Impact", "Hard tech", "Fail", "Conflict", "Lead", "Mentor", "Customer", "Arch", "Perf", "Incident", "Influence"]
    # which cats map well - static teaching matrix
    rows = [
        ("Most impactful project", "yes", "maybe", "", "", "maybe", "", "yes", "yes", "maybe", "", "maybe"),
        ("Hardest technical problem", "", "yes", "maybe", "", "maybe", "", "", "yes", "yes", "maybe", ""),
        ("Failure / mistake", "", "", "yes", "", "", "maybe", "maybe", "", "", "maybe", ""),
        ("Conflict / disagreement", "", "", "", "yes", "maybe", "", "", "maybe", "", "", "yes"),
        ("Mentoring", "", "", "", "", "maybe", "yes", "", "", "", "", "yes"),
        ("Leadership / influence", "maybe", "", "", "maybe", "yes", "maybe", "", "", "", "", "yes"),
        ("Production outage", "", "maybe", "yes", "", "maybe", "", "yes", "", "", "yes", ""),
        ("Customer escalation", "maybe", "", "", "maybe", "", "", "yes", "", "", "maybe", "yes"),
        ("Architecture decision", "yes", "yes", "", "maybe", "yes", "", "", "yes", "maybe", "", "yes"),
        ("Performance win", "yes", "yes", "", "", "", "", "yes", "maybe", "yes", "", ""),
        ("Process / debt / innovation", "maybe", "", "", "", "yes", "", "maybe", "maybe", "", "", "yes"),
        ("Ambiguity / deadline", "maybe", "", "maybe", "maybe", "yes", "", "maybe", "", "", "", "yes"),
    ]
    head = "<tr><th>Story type</th>" + "".join(f"<th>{c}</th>" for c in qcols) + "</tr>"
    body = []
    for r in rows:
        tds = "".join(
            f'<td class="yes">●</td>' if x == "yes" else (f'<td>·</td>' if x == "maybe" else "<td></td>")
            for x in r[1:]
        )
        body.append(f"<tr><th>{r[0]}</th>{tds}</tr>")
    return f'''
<section class="block" id="matrix" data-search="Story reuse matrix" data-stype="Section">
  <p class="kicker">Eight stories beat fifty</p>
  <h2 class="section-title">Story Reuse Matrix</h2>
  <p class="lede">● = primary fit. · = can stretch if you change the cut. Empty = do not force it. Map <i>your</i> titles onto these types in the Story Bank.</p>
  <div class="matrix"><table>{head}{''.join(body)}</table></div>
  <p class="example"><b>Example reuse (fictional project name):</b> “Resumable upload” can be hardest-tech, architecture, performance, customer impact, disagreement (sync vs async), and failure (we launched without virus scan). That is one story, six cuts — not six inventions.</p>
  {topic("mx-how", "How to cut the same story", "reuse story cuts", "Stories", '''
  <p>Lead with the slice they asked for. If they asked conflict, start with the person and the disagreement, not the byte protocol. Keep the rest in your pocket for follow-ups.</p>
  ''', "topics")}
</section>
'''


def senior() -> str:
    return f'''
<section class="block" id="senior" data-search="Senior vs mid-level behavior" data-stype="Section">
  <p class="kicker">The bar</p>
  <h2 class="section-title">Senior-Level Behavior</h2>
  {topic("sr-cmp", "Mid-level vs senior answers (examples)", "ownership ambiguity judgment mentoring", "Senior", '''
  <table>
    <tr><th>Theme</th><th>Mid-level (example)</th><th>Senior (example)</th></tr>
    <tr><td>Ownership</td><td>“I finished my tickets.”</td><td>“The surface was red; I owned the customer outcome and the rollback.”</td></tr>
    <tr><td>Ambiguity</td><td>“I asked PM what to build.”</td><td>“I named two interpretations, picked one with a kill criterion, and told stakeholders.”</td></tr>
    <tr><td>Judgment</td><td>“We used Redis.”</td><td>“Cache-aside because stale-for-30s was acceptable; I rejected a lock.”</td></tr>
    <tr><td>Mentoring</td><td>“I pair when asked.”</td><td>“I changed the review bar so juniors could ship without me in the path.”</td></tr>
    <tr><td>Influence</td><td>“I commented on the RFC.”</td><td>“I got two teams to share a contract by showing the incident cost.”</td></tr>
    <tr><td>Product</td><td>“The design looked nice.”</td><td>“We cut a feature that would have created support load.”</td></tr>
    <tr><td>Risk</td><td>“We shipped on Friday.”</td><td>“We shipped behind a flag with a measured rollback.”</td></tr>
    <tr><td>Time</td><td>“It works now.”</td><td>“This choice is cheap at 10×; that one isn’t.”</td></tr>
  </table>
  <p>Senior is not louder. It is explicit trade-offs, named stakeholders, and what you would not do again.</p>
  ''', "topics")}
</section>
'''


def values() -> str:
    items = [
        ("Open company, no bullshit",
         "Official: information open by default; speaking up needs brains, thoughtfulness, and care.",
         "Do you share early, say hard things, and avoid political editing?",
         "Admitted a miss in public; wrote the doc before the meeting; disagreed with a staff engineer with evidence.",
         "Hidden status; blaming ‘leadership’; aggressive candor without care; reciting ‘transparency.’",
         "Tell me about a time you had to deliver bad news. A time you disagreed with a popular plan."),
        ("Build with heart and balance",
         "Official: passion and urgency plus measure-twice; then cut and work.",
         "Do you care about craft without burnout theater or reckless heroics?",
         "Cut scope to protect quality; said no to a death-march; cared about a11y because users, not a checklist.",
         "‘I worked 80-hour weeks’ as a brag; perfection that never ships; apathy.",
         "A time you slowed down. A time you shipped imperfectly on purpose."),
        ("Don’t #@!% the customer",
         "Official: customer perspective first — collectively, not a handful of loud users.",
         "Did you protect users when it cost you internally?",
         "Stopped a launch; fixed the painful path not the demo path; used support data not opinions.",
         "‘The PM signed off’ as abdication; optimizing internal metrics that hurt users.",
         "A time you pushed back on a ship. A time you chose the unglamorous bug."),
        ("Play, as a team",
         "Official: team first; serious without self-seriousness.",
         "Are other people in your success stories? Do you make the group better?",
         "Gave credit; unblocked another team; de-escalated; hired the gap instead of hoarding.",
         "Hero narrative; ‘I just did it myself’; making teammates the obstacle.",
         "A conflict you resolved. How you onboard someone."),
        ("Be the change you seek",
         "Official: courage to improve products, people, place; action is individual.",
         "Do you fix the system without waiting for a title?",
         "Started a guild, a lint rule, an incident template, a design-system adoption — unassigned.",
         "Complaints without a prototype; waiting for permission on something you could have started.",
         "A process you changed. Something you improved that was nobody’s job."),
    ]
    blocks = []
    for title, means, eval_, good, bad, qs in items:
        blocks.append(f'''
<article class="topic" data-search="{title} Atlassian value" data-stype="Value">
  <h3>{title}</h3>
  <p class="callout official"><b>Official meaning (paraphrase).</b> {means} Source: <a href="https://www.atlassian.com/company/values" target="_blank" rel="noopener">company/values</a>.</p>
  <p><b>What a conversation may probe.</b> {eval_} This is practice interpretation, not a published rubric.</p>
  <p><b>Good signals.</b> {good}</p>
  <p><b>Bad signals.</b> {bad}</p>
  <p><b>Practice questions.</b> {qs}</p>
  <p><b>Story types.</b> Map from the Story Bank; do not invent a value-shaped anecdote.</p>
  <p><b>Avoid reciting the website.</b> Never quote the value name unless they do. Show the behavior, then if asked you can connect it.</p>
  <p><button type="button" class="toggle-btn" data-complete="values" data-cid="val-{title[:12]}">Mark studied</button></p>
</article>''')
    return f'''
<section class="block" id="values" data-search="Atlassian values official" data-stype="Section">
  <p class="kicker">Official five</p>
  <h2 class="section-title">Values Interview</h2>
  <p class="lede">Official handbook: values interview assesses alignment; interviewer often from another team or function; they want mindset as it shows in actions. Official design guide mentions STAR and a dedicated values conversation. Confirm duration with your invite.</p>
  {''.join(blocks)}
</section>
'''


def hm() -> str:
    qs = [
        ("Tell me about your career.", "Arc and agency, not a timeline dump.", "3 chapters: how you started, a turning decision, what you want next.", "Why this company now?"),
        ("What environment do you thrive in?", "Self-knowledge vs ‘whatever you have.’", "Name constraints you need (feedback, ownership) and ones you can live without.", "What environment brings out your worst?"),
        ("What motivates you?", "Fuel vs flattery.", "A concrete loop: user problem → quality bar → teaching.", "What would make you leave in a year?"),
        ("What are you looking for next?", "Scope honesty.", "More architecture + customer surface; not ‘staff in 12 months’ unless true.", "What would be too small?"),
        ("What does senior engineering mean to you?", "Bar definition.", "Ownership of outcomes, judgment, making others faster — match Phase 4 senior table.", "How do you know you’re not there yet?"),
        ("How do you handle disagreement?", "Conflict without villain.", "STAR-L with the other person’s reasonable view.", "Did the relationship survive?"),
        ("How do you influence teams?", "No authority stories.", "Data, prototype, shared incident — not ‘I was right.’", "A time you failed to influence."),
        ("How do you prioritize?", "Framework under load.", "User harm / irreversibility / learning — name what you killed.", "Who disagreed with the order?"),
        ("How do you mentor?", "System not heroics.", "A person and a change in their independence.", "Someone you couldn’t help."),
        ("How do you handle underperformance?", "Courage + fairness.", "Early feedback, written bar, manager partnership — no gossip.", "What if they were a friend?"),
        ("How do you handle ambiguity?", "Kill criteria.", "Two options, timebox, stakeholder.", "A time you waited too long."),
        ("How do you communicate bad news?", "Open company, no bullshit.", "Who, when, what you still don’t know, next checkpoint.", "A time you delayed it."),
        ("How do you make architecture decisions?", "ADR behavior.", "Context, alternatives, reversibility, who you included.", "A decision you’d reverse."),
    ]
    cards = []
    for i, (q, ev, fw, fol) in enumerate(qs, 1):
        cards.append(f'''
<article class="q" id="hm-{i}" data-search="{q}" data-stype="HM question">
  <h3>{i}. {q}</h3>
  <p><b>Evaluating (practice).</b> {ev}</p>
  <p><b>Answer framework.</b> {fw}</p>
  <p><b>Strong answer.</b> Specific names, a number or honest ‘unmeasured’, a trade-off, no villain.</p>
  <p><b>Follow-up.</b> {fol}</p>
  <p><button type="button" class="toggle-btn" data-complete="topics" data-cid="hm-{i}">Mark practiced</button></p>
</article>''')
    return f'''
<section class="block" id="hm" data-search="Hiring manager interview" data-stype="Section">
  <p class="kicker">Official: manager session exists</p>
  <h2 class="section-title">Management / Hiring Manager Interview</h2>
  <p class="lede">Official handbook: usually HM or senior manager; career, collaboration, past projects including business why. Questions below are <b>practice</b>, not a leaked list.</p>
  {''.join(cards)}
</section>
'''
