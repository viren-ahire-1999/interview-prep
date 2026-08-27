from util import callout, esc

PLAN_DAYS = [
    {"n": 1, "title": "Coding revision",
     "learn": "Re-solve 2 Medium problems from Phase 1 bank timed. Narrate clarify → approach → complexity.",
     "do": "One 45-min coding mock from Coding Mock section. Full Tech Checklist after.",
     "verbal": "Recite the 10-step communication framework from memory.",
     "rev": "One weak pattern from Phase 1 Problem Bank — Review status only."},
    {"n": 2, "title": "Frontend craft",
     "learn": "Phase 2: Fiber pipeline + one perf debugging scenario.",
     "do": "Answer 6 Craft Mock questions out loud before revealing rubrics.",
     "verbal": "Explain render vs commit and when keys cause bugs — 3 minutes.",
     "rev": "Phase 2 readiness item you left unchecked."},
    {"n": 3, "title": "System design",
     "learn": "Phase 3: 16-step framework on paper — no Kafka unless the prompt needs it.",
     "do": "45-min SD mock: pick notifications or issue search. Score rubric dimensions.",
     "verbal": "Capacity estimate for 1M DAU issue reads — RPS + cache story.",
     "rev": "Idempotency + outbox — one sentence each."},
    {"n": 4, "title": "Behavioral stories",
     "learn": "Story Bank: deep-fill 3 stories (impact, failure, conflict).",
     "do": "Map those 3 to Story Reuse Matrix cuts. Write 2 follow-ups each.",
     "verbal": "Deliver failure story in STAR-L under 90 seconds.",
     "rev": "Senior vs mid-level table — one row out loud."},
    {"n": 5, "title": "Values",
     "learn": "Re-read official values page. One behavior example per value — yours, not invented.",
     "do": "Practice 3 values questions without saying the value name first.",
     "verbal": "Customer-impact story tied to a value behavior — not a poster quote.",
     "rev": "Official handbook: values interviewer may be outside hiring team."},
    {"n": 6, "title": "Hiring manager prep",
     "learn": "HM Question Bank: career arc, motivation, disagreement, mentoring.",
     "do": "Write answers for 'What does senior mean to you?' and 'Why now?'",
     "verbal": "60-second TMAY + 30-second Why Atlassian — timed.",
     "rev": "Positioning one-liner without looking."},
    {"n": 7, "title": "Coding mock + debrief",
     "learn": "Light — one pattern card only.",
     "do": "Full 45-min coding mock with timer. Log in Rejection Analysis if weak.",
     "verbal": "Explain one mistake you made and how you recovered.",
     "rev": "Tech Checklist — which box do you always miss?"},
    {"n": 8, "title": "Positioning & motivation",
     "learn": "Personal Positioning + Why Atlassian frameworks.",
     "do": "Update TMAY and Why drafts in Dashboard notes. Resume slot 1–2 filled.",
     "verbal": "Why should we hire you for senior — scope, not adjectives.",
     "rev": "Weak vs strong Redis communication example."},
    {"n": 9, "title": "Resume & project interrogation",
     "learn": "Resume Deep Dive follow-up list.",
     "do": "Complete one Project Interrogation session end-to-end. Save score.",
     "verbal": "Defend one metric on your resume or say 'we didn't measure.'",
     "rev": "Story Bank — pick one story for resume bullet overlap."},
    {"n": 10, "title": "Communication & checklist",
     "learn": "Senior Communication + I Don't Know scripts.",
     "do": "Run Tech Checklist on a recorded 20-min craft answer (phone voice memo).",
     "verbal": "Practice 'I haven't built X, but I'd approach…' for one gap.",
     "rev": "Questions to Ask — pick 5 for your next loop."},
    {"n": 11, "title": "Full mock loop",
     "learn": "Skim loop round descriptions only.",
     "do": "Start Full Interview Loop — all 5 rounds with breaks. Save scorecard.",
     "verbal": "HM round: prioritize under load framework out loud.",
     "rev": "Loop debrief — top 2 revision areas."},
    {"n": 12, "title": "Light revision & recruiter",
     "learn": "Recruiter prep fields. Offer component table — no new tech.",
     "do": "Fill recruiter notes. Re-read one story aloud. 20-min craft rubric skim only.",
     "verbal": "Comp expectations script — practice without committing numbers you don't mean.",
     "rev": "Interview Day 24h list — mental walkthrough."},
    {"n": 13, "title": "Light mocks & stories",
     "learn": "Values + one customer story only.",
     "do": "30-min coding OR 30-min SD — pick weaker dimension. Early finish if solid.",
     "verbal": "Two stories: leadership + production incident — 60s each.",
     "rev": "Sleep plan for tomorrow. No new Phase 1–3 topics."},
    {"n": 14, "title": "Confidence & rest",
     "learn": "Final Readiness checklist — honest score only.",
     "do": "Optional 15-min TMAY + Why. Otherwise rest. Pack space, test AV once.",
     "verbal": "Say aloud: 'I don't know' script once — normalize honesty.",
     "rev": "Close laptop by evening. Trust the work from days 1–11."},
]

READINESS_TECH = [
    ("DSA patterns ready (Phase 1 honest gate)", "r4-dsa"),
    ("JavaScript runtime + event loop (explain without notes)", "r4-js"),
    ("React internals + perf judgment (Phase 2)", "r4-react"),
    ("Frontend architecture trade-offs (Phase 2)", "r4-fe-arch"),
    ("System design 45-min framework (Phase 3)", "r4-sd"),
    ("Distributed systems vocabulary (Phase 3)", "r4-distributed"),
]

READINESS_BEH = [
    ("Tell me about yourself — 60s without resume recitation", "r4-tmay"),
    ("Why Atlassian — specific, not homepage", "r4-why"),
    ("10+ strong stories in Story Bank (8 deep minimum)", "r4-stories"),
    ("Failure story with learning (STAR-L)", "r4-fail"),
    ("Conflict story without villain", "r4-conflict"),
    ("Leadership / influence without authority story", "r4-lead"),
    ("Customer-impact story with honest metrics", "r4-customer"),
    ("Production incident story with your actions", "r4-incident"),
]

READINESS_VAL = [
    ("Discuss each official value with behavior — not slogans", "r4-val-nat"),
    ("Stories mapped to values (no value-shaped fiction)", "r4-val-map"),
]

READINESS_MOCK = [
    ("3+ coding mocks with debrief", "r4-mock-code"),
    ("2+ system design mocks scored on rubric", "r4-mock-sd"),
    ("1+ full interview loop saved", "r4-mock-loop"),
    ("1+ project interrogation session saved", "r4-mock-iq"),
]

READINESS_COMMS = [
    ("Explain technical choices with trade-offs (Redis-level specificity)", "r4-comms-trade"),
    ("Think aloud without long silence", "r4-comms-aloud"),
    ("Clarify before solving", "r4-comms-clarify"),
    ("Challenge assumptions politely", "r4-comms-challenge"),
    ("Recover from mistakes calmly", "r4-comms-recover"),
]


def _checks(items: list[tuple[str, str]], group: str = "readiness") -> str:
    return "".join(
        f'<label class="task"><input type="checkbox" data-id="{cid}" data-group="{group}" />'
        f"<span>{label}</span></label>"
        for label, cid in items
    )


def _day_card(d: dict) -> str:
    n = d["n"]
    tasks = [
        ("Learn", d["learn"]),
        ("Do", d["do"]),
        ("Verbal", d["verbal"]),
        ("Revision", d["rev"]),
    ]
    body = "".join(
        f'<label class="task"><input type="checkbox" data-id="p4d{n}-t{i}" data-group="checks" />'
        f"<span><b>{label}</b> {text}</span></label>"
        for i, (label, text) in enumerate(tasks)
    )
    light = " badge-review" if n >= 12 else ""
    return f'''<article class="day" id="p4-day-{n}">
  <button type="button" class="day-head">
    <div>
      <h3>Day {n} — {d["title"]}</h3>
      <div class="day-meta">{"Light day · rest & confidence" if n >= 12 else "~2 hours · mock-heavy on day 7 & 11"}</div>
    </div>
    <span class="badge badge-pattern{light}">Day {n}</span>
  </button>
  <div class="day-body">{body}</div>
</article>'''


def plan() -> str:
    cards = "".join(_day_card(d) for d in PLAN_DAYS)
    return f'''
<section class="block" id="plan" data-search="14-Day Final Preparation Plan" data-stype="Section">
  <p class="kicker">Interview window</p>
  <h2 class="section-title">14-Day Final Preparation Plan</h2>
  <p class="lede">Exact daily schedule. Days 12–14 are light: revision, mocks, stories, sleep — no major new topics. Checkboxes persist as <code>p4dN-tI</code>.</p>
  <div class="card" style="margin-bottom:16px">
    <table>
      <tr><th>Phase</th><th>Days</th><th>Focus</th></tr>
      <tr><td>Build</td><td>1–6</td><td>Coding, craft, SD, behavioral, values, HM</td></tr>
      <tr><td>Integrate</td><td>7–11</td><td>Mocks, loop, communication, resume</td></tr>
      <tr><td>Taper</td><td>12–14</td><td>Light review, sleep, confidence</td></tr>
    </table>
  </div>
  {cards}
  {callout("If readiness score is dishonestly high but mocks feel shaky, extend the plan — do not cram new Phase 3 topics in the last 48 hours.")}
</section>
'''


def readiness() -> str:
    return f'''
<section class="block" id="readiness" data-search="Final readiness checklist Phase 4 gate" data-stype="Section">
  <p class="kicker">Gate before you schedule</p>
  <h2 class="section-title">Final Readiness Checklist</h2>
  <p class="lede">Check only if you can do it <i>today</i> without this file. Feeds the Dashboard readiness ring. Bands: &lt;50 Not Ready · 50–69 Needs Work · 70–84 Interview Ready · ≥85 Strongly Ready.</p>
  <p class="stat">Score: <span id="ready-score">0%</span></p>
  <div class="bar"><span id="bar-ready-final"></span></div>
  <p id="ready-gate" class="stat-sub"></p>

  <h3>Technical</h3>
  {_checks(READINESS_TECH)}

  <h3>Behavioral</h3>
  {_checks(READINESS_BEH)}

  <h3>Values</h3>
  {_checks(READINESS_VAL)}

  <h3>Mock</h3>
  {_checks(READINESS_MOCK)}

  <h3>Communication</h3>
  {_checks(READINESS_COMMS)}
</section>
'''


def progress() -> str:
    return f'''
<section class="block" id="progress" data-search="Progress tracker localStorage reset" data-stype="Section">
  <p class="kicker">Local only</p>
  <h2 class="section-title">Progress Tracker</h2>
  <p class="lede">Stored in <code>localStorage</code> key <code>atl-phase4-v1</code>. Clearing site data wipes progress.</p>
  <div class="grid grid-2">
    <div class="card">
      <h3>14-day plan tasks</h3>
      <p id="track-days">0 / 0</p>
      <div class="bar"><span id="bar-track-days"></span></div>
    </div>
    <div class="card">
      <h3>Story bank slots filled</h3>
      <p id="track-stories">0 / 22</p>
      <div class="bar"><span id="bar-track-stories"></span></div>
    </div>
    <div class="card">
      <h3>Readiness checklist</h3>
      <p id="track-readiness">0%</p>
      <div class="bar"><span id="bar-track-readiness"></span></div>
    </div>
    <div class="card">
      <h3>Mock sessions saved</h3>
      <p id="track-mocks">0</p>
    </div>
    <div class="card">
      <h3>Resume bullets prepped</h3>
      <p id="track-resume">0 / 5</p>
    </div>
    <div class="card">
      <h3>Rejection log entries</h3>
      <p id="track-rej">0</p>
    </div>
  </div>
  <p style="margin-top:18px"><button type="button" class="danger-btn" id="reset-progress">Reset all progress</button></p>
  <p class="stat-sub">Confirms before wipe. Theme preference is kept.</p>
</section>
'''


def resources() -> str:
    official = [
        ("Atlassian company values", "https://www.atlassian.com/company/values", "Official five values — source of truth for values interview."),
        ("Engineering interview handbook", "https://www.atlassian.com/company/careers/resources/interviewing/engineering", "Official public guide: coding, system design, manager, values, hiring committee."),
        ("Atlassian careers", "https://www.atlassian.com/company/careers", "Roles, process overview, accommodation requests via talent partner."),
        ("Atlassian engineering blog", "https://www.atlassian.com/engineering", "Official engineering writing — product and culture signal, not interview secrets."),
    ]
    general = [
        ("STAR method (UMN career guide)", "https://career.umn.edu/resources/the-star-method", "General behavioral answer structure."),
        ("StaffEng leadership archives", "https://staffeng.com/guides", "General senior/staff engineering narratives."),
        ("System Design Primer (GitHub)", "https://github.com/donnemartin/system-design-primer", "General SD vocabulary — pair with Phase 3, not a substitute."),
        ("MDN Web Docs", "https://developer.mozilla.org/", "General web platform reference for craft depth."),
        ("React documentation", "https://react.dev/", "General React reference aligned with Phase 2."),
    ]
    off_rows = "".join(
        f'<tr><td><span class="badge badge-pattern">Official</span></td>'
        f'<td><a href="{url}" target="_blank" rel="noopener">{title}</a></td><td>{desc}</td></tr>'
        for title, url, desc in official
    )
    gen_rows = "".join(
        f'<tr><td><span class="badge badge-review">General</span></td>'
        f'<td><a href="{url}" target="_blank" rel="noopener">{title}</a></td><td>{desc}</td></tr>'
        for title, url, desc in general
    )
    return f'''
<section class="block" id="resources" data-search="Resources official Atlassian STAR system design" data-stype="Section">
  <p class="kicker">Official first</p>
  <h2 class="section-title">Resource Library</h2>
  <p class="lede">Phase 4 content lives in this file. Use external links for official Atlassian sources and second opinions. Labeled <b>Official</b> vs <b>General</b>.</p>

  <h3>Official Atlassian</h3>
  <table>
    <tr><th>Label</th><th>Resource</th><th>Notes</th></tr>
    {off_rows}
  </table>

  <h3>General interview preparation</h3>
  <table>
    <tr><th>Label</th><th>Resource</th><th>Notes</th></tr>
    {gen_rows}
  </table>

  <div class="callout official"><b>Reminder.</b> Interview loops change by role, level, and region. Recruiter email beats any prep site.</div>
</section>
'''
