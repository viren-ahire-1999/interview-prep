from util import esc

Q = []

CATS = [
    "Leadership", "Ownership", "Conflict", "Failure", "Communication", "Customer",
    "Ambiguity", "Prioritization", "Mentorship", "Feedback", "Collaboration",
    "Technical decisions", "Production incidents", "Influencing", "Change", "Learning",
]

STORY_CATS = [
    "Most impactful project", "Hardest technical problem", "Failure", "Conflict",
    "Disagreement", "Mentoring", "Leadership", "Influencing without authority",
    "Production outage", "Tight deadline", "Ambiguous requirement", "Customer escalation",
    "Technical debt", "Architecture decision", "Performance improvement",
    "Cross-team collaboration", "Mistake", "Innovation",
]


def add(cat, q, testing, weak, strong, follow, stories):
    Q.append(dict(
        cat=cat, q=q, testing=testing, weak=weak, strong=strong, follow=follow,
        stories=stories if isinstance(stories, str) else ", ".join(stories),
    ))


# ── Leadership (8) ──────────────────────────────────────────────────────────
add("Leadership",
    "Tell me about a time you led a cross-functional initiative without being the formal tech lead.",
    "Whether you create direction and alignment when the org chart is silent — not whether you had a title.",
    "“I was the senior so people listened.” No named stakeholders, no decision record, hero narrative.",
    "STAR-L: Situation (multi-team gap) → Task (outcome you owned) → Actions in first person (who you aligned, what you wrote, how you decided) → Result with honest metrics → Learning. Name PM/design/backend counterparts. One explicit trade-off you drove.",
    "What would you do if the PM disagreed? How did you know you were succeeding before launch?",
    ["Leadership", "Cross-team collaboration", "Influencing without authority", "Most impactful project"])

add("Leadership",
    "Describe when you set technical direction during uncertainty.",
    "Judgment under incomplete information — can you commit, communicate reversibility, and bring others along?",
    "Listing technologies without context; “we picked React because I like it”; no alternatives rejected.",
    "Context → two viable options → decision criteria (customer harm, reversibility, team skill, 10× cost) → chosen path → who you socialized with → kill criterion if wrong. Mention RFC/ADR or equivalent even if informal.",
    "What signal would make you reverse the decision? Who did you not include and why?",
    ["Architecture decision", "Ambiguous requirement", "Technical debt", "Leadership"])

add("Leadership",
    "Tell me about rallying engineers around an unpopular but necessary decision.",
    "Influence through reasoning and empathy, not rank — especially relevant to senior IC loops.",
    "Framing dissenters as obstacles; “they just didn’t get it”; no acknowledgment of their reasonable concern.",
    "Name the unpopular decision and why it hurt locally (velocity, pride, tech preference). Your Actions: listened first, reframed in customer/outage terms, offered mitigation (flags, timeline, scope). Result: what shipped or what risk dropped. Learning: what you’d communicate earlier next time.",
    "Did anyone still disagree at ship? Would you make the same call?",
    ["Disagreement", "Influencing without authority", "Technical debt", "Leadership"])

add("Leadership",
    "When did you step up as de facto lead during reorg or attrition?",
    "Stability and continuity when leadership vacuum appears — without empire-building.",
    "Complaining about chaos; only describing your tickets; claiming you “saved everything.”",
    "Situation: what broke (bus factor, on-call, roadmap). Task: what outcome the team needed. Actions: rituals you started (standups, RFCs, pairing), how you distributed load, how you escalated what wasn’t yours. Result: team throughput or incident trend. Learning: what you handed back when a manager arrived.",
    "How did you avoid burnout? What did you stop doing?",
    ["Leadership", "Production outage", "Cross-team collaboration", "Mentoring"])

add("Leadership",
    "Describe leading a migration others were afraid to touch.",
    "Courage plus plan — phased rollout, measurable risk reduction, not big-bang bravado.",
    "“It wasn’t that hard”; blaming the previous team; no rollback story.",
    "Why the migration mattered (perf, security, hiring). Phases: read path, dual-write, cutover, delete. Your slice: code, comms, training. Metrics: error rate, latency, tickets. Trade-off: speed vs safety. Flag/feature-toggle language for React/Node context.",
    "What would have aborted the migration? How long did you run dual-write?",
    ["Architecture decision", "Technical debt", "Performance improvement", "Most impactful project"])

add("Leadership",
    "Tell me about creating clarity when senior ICs disagreed on approach.",
    "Facilitation and decision hygiene — senior loops expect you to unblock peers, not escalate instantly.",
    "Picking a side without process; re-litigating in the interview; both options caricatured.",
    "Situation: disagreement topic (API shape, state management, deployment). Actions: timeboxed spike criteria, decision doc with pros/cons, explicit owner and revisit date. Result: decision made, teams unblocked. Note dissent preserved in writing. Learning: when consensus was wrong to pursue.",
    "What if the spike was inconclusive? How did you handle the loser?",
    ["Disagreement", "Architecture decision", "Cross-team collaboration", "Influencing without authority"])

add("Leadership",
    "When did you delegate critical work and still own the outcome?",
    "Scale through others — senior is not the bottleneck on every review.",
    "Micromanagement story disguised as delegation; abdication (“I assigned it and forgot”).",
    "Task: high-stakes deliverable. Actions: how you chose delegatee, defined done, review checkpoints, risk you retained (on-call, launch comms). Result: shipped and their growth. Learning: what you still did that you should have stopped.",
    "What if they missed the bar? How did you communicate upward?",
    ["Mentoring", "Leadership", "Tight deadline", "Most impactful project"])

add("Leadership",
    "Describe leading through a release with executive visibility.",
    "Composure, risk communication, and detail when the audience is non-engineering.",
    "Status-green theater; surprise SEV; no prep for exec questions on customer impact.",
    "Pre-release: risk register, demo path vs real path, rollback owner. During: checkpoint rhythm, bad-news early. Actions in first person on what you controlled (quality gates, bug triage). Result: launch outcome honest. Learning: what you’d cut from scope earlier.",
    "What did execs care about that engineers ignored? Worst surprise?",
    ["Tight deadline", "Customer escalation", "Production outage", "Most impactful project"])

# ── Ownership (8) ───────────────────────────────────────────────────────────
add("Ownership",
    "Tell me about taking ownership beyond your ticket when users were hurt.",
    "End-to-end outcome ownership — Atlassian values customer and team over lane boundaries.",
    "“Not my squad”; waiting for assignment; fixing symptom not cause.",
    "User-visible Situation → harm (latency, broken flow, support volume). Task: restore trust. Actions: trace across React/Node boundary, hotfix vs proper fix decision, comms to support/PM. Result: metric or ticket trend. Learning: systemic fix you added (alert, test, runbook).",
    "Why wasn’t it your team? What did you stop doing to make room?",
    ["Customer escalation", "Production outage", "Performance improvement", "Mistake"])

add("Ownership",
    "Describe owning a production issue that wasn’t your team’s fault.",
    "No-blame problem solving while still driving to resolution — values-aligned.",
    "Villain narrative about another team; claiming credit for their fix; stopping at handoff.",
    "Timeline of detection → your Actions as coordinator or driver → evidence you gathered → fix path → post-incident follow-up you initiated even if root cause elsewhere. Customer time-to-restore emphasized.",
    "How did you handle tension with the owning team? What changed after?",
    ["Production outage", "Cross-team collaboration", "Conflict", "Influencing without authority"])

add("Ownership",
    "When did you follow a problem to root cause across team boundaries?",
    "Curiosity and persistence — senior engineers don’t stop at the API 500.",
    "Stopping at “backend bug”; no hypothesis chain; no verification.",
    "Symptom → hypotheses → bisect (network, auth, cache, client state) → owning node in the graph. Mention observability you used. Result: durable fix. Learning: guardrail added.",
    "What dead ends did you hit? How long before you found root cause?",
    ["Hardest technical problem", "Production outage", "Performance improvement", "Most impactful project"])

add("Ownership",
    "Tell me about closing a gap nobody assigned — monitoring, docs, on-call.",
    "Be the change you seek — without waiting for a Jira ticket.",
    "“Someone should fix that”; large unfunded rewrite proposal; no adoption story.",
    "Specific gap and risk if ignored. Small shippable Actions: dashboard, alert, README, runbook, lint rule. How you got team buy-in. Measured outcome (MTTR, repeat incidents). Learning: maintenance plan.",
    "Why hadn’t it been done? Did it stick after you moved on?",
    ["Innovation", "Production outage", "Change", "Technical debt"])

add("Ownership",
    "Describe owning a bad estimate and correcting course publicly.",
    "Intellectual honesty and replanning — senior bar is early bad news.",
    "Blaming scope creep only; silent slip; overpromising to recover.",
    "Original estimate and why wrong (unknown dependency, perf cliff). Actions: re-estimate with evidence, options to cut scope, who you told and when. Result: what shipped and trust preserved or not. Learning: estimation guardrail.",
    "What would you do differently at estimation time? Did anyone push back on the cut?",
    ["Tight deadline", "Failure", "Communication", "Ambiguous requirement"])

add("Ownership",
    "When did you take ownership of customer pain that pre-dated your tenure?",
    "No “not invented here” — improving the system you inherited.",
    "Trash-talking predecessors; band-aid only; no prioritization against new work.",
    "How you discovered pain (support tags, session replay, metrics). Actions: triage, fix or roadmap entry, stakeholder alignment. Trade-off vs feature work. Result: customer or support outcome.",
    "How much tech debt did you accept to fix it? Who paid the opportunity cost?",
    ["Customer escalation", "Technical debt", "Most impactful project", "Performance improvement"])

add("Ownership",
    "Tell me about owning technical debt that blocked other teams.",
    "Platform thinking — your code’s downstream consumers matter.",
    "Debt as abstract gripe; no consumer voice; no incremental plan.",
    "Who was blocked and how. Actions: inventory, RFC, phased paydown, comms to consumers. Metrics: lead time, incident rate, adoption. Explicit what you deferred.",
    "Why did the debt accumulate? How did you prevent recurrence?",
    ["Technical debt", "Cross-team collaboration", "Architecture decision", "Influencing without authority"])

add("Ownership",
    "Describe how you handle open loops at end of week while still owning outcomes.",
    "Reliability and follow-through without heroics — balance value.",
    "Bragging about weekend work; leaving stakeholders guessing; no written handoff.",
    "Framework: classify (blocker vs can wait), communicate status and next checkpoint, document for Monday-you or delegate with context. Example structure only — use your real week. Learning: WIP limits.",
    "When do you work late vs push back on date? Example of a loop you dropped and why?",
    ["Prioritization", "Communication", "Tight deadline", "Leadership"])

# ── Conflict (8) ────────────────────────────────────────────────────────────
add("Conflict",
    "Tell me about a conflict with a peer engineer about technical approach.",
    "Constructive disagreement — peer respect, evidence, outcome not winning.",
    "Making them incompetent; conflict as personality clash; no resolution state.",
    "Both positions reasonable. Actions: private conversation, shared criteria, spike or ADR, agreed owner. Result: decision and relationship status. Learning: earlier involvement point.",
    "Still friends? What if you were wrong?",
    ["Conflict", "Disagreement", "Architecture decision", "Hardest technical problem"])

add("Conflict",
    "Describe a disagreement with your manager about priorities.",
    "Upward disagreement with respect — senior ICs push back with data.",
    "Passive acceptance; public undermining; emotional venting without proposal.",
    "Situation: competing priorities. Your Task: best outcome for customer/org. Actions: framed trade-offs, data, alternative plan, asked for decision explicitly. Result: what got prioritized. Learning: when to disagree and commit.",
    "What if they still overruled you? Ever glad they did?",
    ["Disagreement", "Prioritization", "Influencing without authority", "Customer escalation"])

add("Conflict",
    "When did you disagree with a PM on scope or timeline?",
    "Partnership with product — push back with user harm and engineering cost articulated.",
    "“PMs never understand tech”; ultimatum; no user framing.",
    "User story behind scope. Actions: sliced MVP, phased delivery, written risks of full scope, joint success metric. Result: shipped slice or avoided SEV. Learning: how you build PM trust.",
    "How do you say no without being “the blocker”?",
    ["Disagreement", "Tight deadline", "Customer escalation", "Ambiguous requirement"])

add("Conflict",
    "Tell me about tension between frontend and backend teams.",
    "Boundary ownership in full-stack senior roles — contract and empathy both ways.",
    "Stereotyping (“backend slow”); throwing over wall; no contract fix.",
    "Concrete contract pain (pagination, errors, N+1, versioning). Actions: pairing, schema workshop, shared mock, SLAs. Result: integration friction down. Learning: prevention (codegen, BFF, tests).",
    "Who wrote the API spec? What broke during the fix?",
    ["Cross-team collaboration", "Conflict", "Architecture decision", "Performance improvement"])

add("Conflict",
    "Describe a conflict where you were partially wrong.",
    "Self-awareness and repair — values interview gold.",
    "Fake humility; blaming context only; no behavior change.",
    "What you believed → what you missed → how you learned (review, incident, peer). Actions: apology, fix, process change. Result: trust repair signal. Learning: specific habit changed.",
    "How did they react? Do you still make that mistake?",
    ["Failure", "Mistake", "Feedback", "Conflict"])

add("Conflict",
    "When did you de-escalate a heated review or Slack thread?",
    "Emotional intelligence under public pressure — open company, no bullshit with care.",
    "Matching heat; sarcasm; taking thread private too late without summary.",
    "Trigger and stakes. Actions: pause, summarize both sides, move to sync, propose decision path. Result: decision or cooled relationship. Learning: norm you suggested (review guide, reaction time).",
    "What if the other person was senior? Written vs verbal?",
    ["Conflict", "Communication", "Collaboration", "Feedback"])

add("Conflict",
    "Tell me about conflict with a stakeholder who outranked you.",
    "Courage with diplomacy — influence without authority upward.",
    "Capitulation or public fight; leaking to skip level without trying direct.",
    "Stakeholder goal vs risk you saw. Actions: 1:1, written options, pilot, exec summary if needed. Result: outcome and relationship. Learning: when to escalate vs absorb.",
    "Would you escalate again the same way? What data helped most?",
    ["Influencing without authority", "Disagreement", "Customer escalation", "Leadership"])

add("Conflict",
    "Describe working with a teammate whose quality bar differed from yours.",
    "Feedback and standards without condescension — play as a team.",
    "Public shaming; doing their work forever; gossip to manager first.",
    "Specific quality gap and customer impact. Actions: private feedback, examples, pairing, checklist, manager loop if needed. Result: their improvement or boundary set. Learning: when bar is non-negotiable.",
    "What if they disagreed with the bar? Time box before escalation?",
    ["Feedback", "Mentoring", "Conflict", "Collaboration"])

# ── Failure (8) ─────────────────────────────────────────────────────────────
add("Failure",
    "Tell me about a significant mistake you made in production.",
    "Accountability and learning — STAR-L with real L.",
    "Blaming deploy tool; minimizing impact; no systemic fix.",
    "Situation/Task → your mistaken Action → blast radius honest → rollback/fix → postmortem contribution → Lesson and guardrail (test, flag, checklist). No invented hero save.",
    "How did you tell your manager? What would you do in first 15 minutes now?",
    ["Mistake", "Failure", "Production outage", "Learning"])

add("Failure",
    "Describe a project that failed to meet its goals — your role.",
    "Ownership without self-flagellation — what you control.",
    "Externalizing all causes; no learning; calling it success redefined.",
    "Goal and why missed (estimate, market, tech). Your Actions and decisions that contributed. Result: kill, pivot, or partial. Learning: leading indicator you watch now.",
    "Would you kill it earlier today? Who decided to stop?",
    ["Failure", "Most impactful project", "Ambiguous requirement", "Prioritization"])

add("Failure",
    "When did you ship something you later realized was the wrong trade-off?",
    "Judgment retrospective — reversibility and customer cost.",
    "“No regrets”; no metric; no follow-up fix.",
    "Trade-off at ship time (speed vs debt, UX vs perf). Why it made sense then. What broke later. Actions to remediate. Learning: decision checklist item added.",
    "How long until you knew? How did you prioritize the fix?",
    ["Technical debt", "Architecture decision", "Mistake", "Customer escalation"])

add("Failure",
    "Tell me about missing a deadline and why.",
    "Honesty and replanning — not perfectionism excuse loop.",
    "Surprise miss with no early warning; blaming only others.",
    "Commitment and dependency that slipped. When you knew and who you told. Actions: scope cut, extra help, or date move with rationale. Result: what delivered. Learning: forecasting change.",
    "Repeat miss or one-off? How do you buffer estimates now?",
    ["Tight deadline", "Failure", "Communication", "Prioritization"])

add("Failure",
    "Describe a mentoring or hiring bet that didn’t work out.",
    "Fairness and realism — growth without fairy tales.",
    "Trash-talking individual; no manager partnership; no self-reflection.",
    "Expectation set vs reality. Actions: feedback cycles, support tried, exit or role change path. Result: outcome for them and team. Learning: signals you missed in hindsight.",
    "Would you hire the same profile again? What early signal matters?",
    ["Mentoring", "Failure", "Feedback", "Leadership"])

add("Failure",
    "When did you misread requirements and had to unwind work?",
    "Ambiguity handling failure — how you recover.",
    "PM bashing; no validation step proposed for future.",
    "Assumption you made. Cost of unwind. Actions: clarification process you introduced (proto review, acceptance criteria). Result: correct delivery. Learning.",
    "How much code discarded? Customer impact?",
    ["Ambiguous requirement", "Mistake", "Failure", "Communication"])

add("Failure",
    "Tell me about a technical decision you would reverse with hindsight.",
    "Intellectual honesty — not flip-flopping without reasoning.",
    "Decisions with no downside; pretending perfection now.",
    "Decision context → constraints then → why chosen → what you know now → what you’d pick → migration cost honest. Framework shows judgment evolution.",
    "Was reversal worth the cost? Partial revert?",
    ["Architecture decision", "Technical debt", "Failure", "Learning"])

add("Failure",
    "Describe learning a lesson the expensive way.",
    "Convert pain into system improvement — senior maturity signal.",
    "Drama without lesson; lesson without behavior change.",
    "Expensive = time, money, outage, trust. Your role. Actions after. Systemic fix. Learning stated as rule you follow aloud in interviews.",
    "How do you teach this lesson without naming names?",
    ["Failure", "Production outage", "Mistake", "Learning"])

# ── Communication (8) ───────────────────────────────────────────────────────
add("Communication",
    "Tell me about explaining a complex technical trade-off to non-engineers.",
    "Translation without condescension — critical for Atlassian cross-functional work.",
    "Jargon dump; one correct answer pretense; no decision asked.",
    "Audience and decision needed. Analogy tied to user workflow. Options with user/business consequence. Recommendation and what you need from them. Confirm understanding.",
    "What question did they ask that you hadn’t prepared for?",
    ["Architecture decision", "Communication", "Customer escalation", "Influencing without authority"])

add("Communication",
    "Describe delivering bad news to leadership about a delay.",
    "Open company, no bullshit — timing and plan, not hope.",
    "Surprising late; no options; excessive detail without headline.",
    "Headline first → impact → cause → options → recommendation → ask. Actions before the meeting (who else briefed). Result: decision made. Learning: earlier warning trigger.",
    "Written or live? What did they push back on?",
    ["Communication", "Tight deadline", "Leadership", "Prioritization"])

add("Communication",
    "When did you write something — RFC, postmortem, doc — that changed minds?",
    "Written persuasion at senior level — clarity beats volume.",
    "“I posted in Slack”; no structure; no outcome.",
    "Problem, audience, format chosen, sections (context, options, recommendation, rollout). How you solicited feedback. Decision or behavior change. Learning: when doc vs meeting.",
    "Who still disagreed? How long was the doc?",
    ["Influencing without authority", "Architecture decision", "Change", "Production outage"])

add("Communication",
    "Tell me about tailoring the same update for engineers vs PM vs exec.",
    "Audience-aware communication — same truth, different slice.",
    "Identical slide deck; hiding bad news from one group.",
    "Core facts immutable. Per audience: depth, metrics, asks. Example outline for each — no fake meeting. Result: aligned or explicit dissent captured.",
    "Which audience is hardest for you? What got lost in translation once?",
    ["Communication", "Leadership", "Cross-team collaboration", "Customer escalation"])

add("Communication",
    "Describe saying “I don’t know yet” without losing credibility.",
    "Intellectual honesty plus plan — senior trust signal.",
    "Bluffing; over-long hedge; stopping at don’t know with no next step.",
    "Question context. What you do know. What you’ll do by when. Who you’ll involve. Follow-through Result. Learning: knowledge gaps you pre-empt now.",
    "Ever bluff and get caught? How fast to answer later?",
    ["Communication", "Ambiguity", "Learning", "Hardest technical problem"])

add("Communication",
    "When did poor communication on your part cause a problem?",
    "Ownership of comms failure — rare honest answer.",
    "Vague “misalignment”; blaming async tools only.",
    "What you failed to communicate (risk, status, handoff). Impact. Actions to repair. Process fix (template, ritual). Learning.",
    "How did you apologize? Repeat offense?",
    ["Mistake", "Failure", "Communication", "Cross-team collaboration"])

add("Communication",
    "Tell me about presenting architecture to skeptical senior engineers.",
    "Technical credibility and Q&A composure.",
    "Defensive; dismissing questions; no alternatives section.",
    "Problem framing → constraints → options killed → recommendation → risks → open questions. How you handled unknown. Result: approval or documented dissent.",
    "Toughest question? What did you research after?",
    ["Architecture decision", "Influencing without authority", "Hardest technical problem", "Disagreement"])

add("Communication",
    "Describe async communication across time zones that actually worked.",
    "Remote collaboration craft — relevant to global teams.",
    "Sync-only bias; Slack chaos; no written record.",
    "Artifact (doc, Loom, decision log). Timezone-friendly handoff. Explicit response SLA. Tool choice rationale. Result: decision latency improved. Learning.",
    "What still required sync? How did you handle urgency?",
    ["Cross-team collaboration", "Collaboration", "Change", "Leadership"])

# ── Customer (8) ────────────────────────────────────────────────────────────
add("Customer",
    "Tell me about advocating for the user when internal metrics said ship.",
    "Don’t #@!% the customer — judgment over vanity metrics.",
    "Moralizing without data; blocking without alternative; “users always right” platitude.",
    "User harm hypothesized. Evidence (support, usability, a11y). Actions: experiment, flag, phased rollout, or ship with guardrails. Trade-off named. Result: metric or ticket change honest.",
    "What if PM had OKRs against you? Ever wrong about user harm?",
    ["Customer escalation", "Most impactful project", "Disagreement", "Innovation"])

add("Customer",
    "Describe a customer escalation you personally helped resolve.",
    "Hands-on customer empathy — not delegating to support only.",
    "Hero story with NDA-breaking detail; fix without prevention.",
    "Escalation path. Your Actions: reproduce, bridge to eng, comms to customer via proper channel. Time-to-resolve. Follow-up systemic fix. Learning.",
    "Enterprise vs SMB difference? What could support alone not do?",
    ["Customer escalation", "Production outage", "Performance improvement", "Ownership"])

add("Customer",
    "When did you push back on a feature that would create support burden?",
    "Long-term customer cost in design — senior product engineering.",
    "Nihilism (“we never say no”); no alternative offered.",
    "Feature and support cost mechanism (edge cases, permissions, migration). Actions: simplified design, docs, in-product guidance, or killed. Stakeholders aligned. Result.",
    "Quantify support burden or qualitative? Example trade in UI?",
    ["Customer escalation", "Architecture decision", "Disagreement", "Technical debt"])

add("Customer",
    "Tell me about using support or ticket data to prioritize engineering work.",
    "Evidence-led prioritization — customer voice in backlog.",
    "Anecdote of one loud user; no taxonomy; no closing loop with support.",
    "Data source and tagging. Pattern found. Actions: fix order, comms back to support. Result: ticket trend. Learning: dashboard or ritual.",
    "False positives in ticket data? How avoid recency bias?",
    ["Prioritization", "Customer escalation", "Performance improvement", "Most impactful project"])

add("Customer",
    "Describe improving an unglamorous user path others ignored.",
    "Balance — polish on paths that matter daily.",
    "Only dashboard work; no measurement; dismissiveness toward “small” UX.",
    "Path (onboarding, error recovery, empty states, permissions). Why ignored. Actions: research, fix, measure. Result: completion or error rate. Learning.",
    "How prove ROI? Conflict with feature team?",
    ["Performance improvement", "Most impactful project", "Innovation", "Customer escalation"])

add("Customer",
    "When did you trade internal convenience for customer experience?",
    "Short-term pain for long-term trust.",
    "Martyr narrative; no business case; permanent hero ops.",
    "Internal shortcut identified (cache staleness, rough error, dev-only API). Customer impact. Actions: proper fix cost. Result. Learning: guardrail.",
    "Still paying the cost? Automate later?",
    ["Technical debt", "Customer escalation", "Architecture decision", "Failure"])

add("Customer",
    "Tell me about saying no to a loud customer request.",
    "Serve collective customer base — not single-account tyranny.",
    "Flat no; yes without limit; leaking account names.",
    "Request and why harmful (security, maintenance, product direction). Actions: alternative, roadmap honesty, partner with PM/CS. Result: relationship outcome. Learning.",
    "Custom enterprise deals — how navigate?",
    ["Customer escalation", "Disagreement", "Influencing without authority", "Prioritization"])

add("Customer",
    "Describe measuring whether you actually helped customers.",
    "Outcome metrics literacy — not output metrics only.",
    "Vanity (lines of code, story points); no baseline.",
    "Metric chosen (task success, TTF, error rate, NPS driver, support volume). Baseline → intervention → read → caveats. Honest if unmeasured and why.",
    "Leading vs lagging indicators? How long to know?",
    ["Most impactful project", "Performance improvement", "Innovation", "Customer escalation"])

# ── Ambiguity (8) ───────────────────────────────────────────────────────────
add("Ambiguity",
    "Tell me about starting work when requirements were intentionally vague.",
    "Progress with kill criteria — senior ambiguity muscle.",
    "Analysis paralysis; building wrong thing fast; no stakeholder check-in.",
    "Known vs unknown. Actions: problem statement doc, prototype scope, timebox, success/fail signals. Result: learn or ship. Learning.",
    "When did you stop early? Worst wrong direction?",
    ["Ambiguous requirement", "Innovation", "Most impactful project", "Tight deadline"])

add("Ambiguity",
    "Describe defining “done” when the PM hadn’t.",
    "Product partnership — engineering-led clarity.",
    "Gold-plating; passive waiting; done = merged only.",
    "Acceptance criteria you proposed (user-visible, a11y, perf, rollback). Socialized with PM/design. Actions: checklist, demo script. Result: fewer reversals. Learning.",
    "Pushback on scope of done? Who owns a11y in your story?",
    ["Ambiguous requirement", "Collaboration", "Customer escalation", "Leadership"])

add("Ambiguity",
    "When did you run a timeboxed spike to kill bad options?",
    "Cheap learning — judgment before commitment.",
    "Spike became stealth project; no report; one option only.",
    "Question spike answered. Timebox length. Success/kill metrics. Actions: throwaway code allowed, doc output. Result: option eliminated or chosen. Learning.",
    "How throw away spike code? Ever spike justified wrong option?",
    ["Ambiguous requirement", "Architecture decision", "Hardest technical problem", "Innovation"])

add("Ambiguity",
    "Tell me about choosing between two valid product interpretations.",
    "Decision-making with incomplete product input.",
    "Random choice; endless committee; no customer tie-break.",
    "Both interpretations and user impact. Actions: data, PM consult, default reversible choice, flag. Result. Learning: question you ask upfront now.",
    "Reversible vs irreversible framing? Example?",
    ["Ambiguous requirement", "Disagreement", "Architecture decision", "Customer escalation"])

add("Ambiguity",
    "Describe when waiting for clarity would have been worse than deciding.",
    "Bias to action with eyes open — not recklessness.",
    "False urgency; no rollback; blaming PM for your rush.",
    "Cost of delay quantified (customer, team, market). Decision made and comms. Monitoring plan. Result. Learning: threshold for waiting.",
    "Decision wrong — then what? Who had to approve?",
    ["Ambiguous requirement", "Tight deadline", "Leadership", "Production outage"])

add("Ambiguity",
    "When did ambiguity come from org politics, not missing specs?",
    "Navigating human systems — senior realism.",
    "Gossip; naming names negatively; helpless victim.",
    "Political tension described neutrally. Actions: align sponsors, narrow scope, written decision owner. Result. Learning: escalation path.",
    "Ethical line? Document trail?",
    ["Ambiguous requirement", "Influencing without authority", "Conflict", "Cross-team collaboration"])

add("Ambiguity",
    "Tell me about building when legal or compliance constraints were unclear.",
    "Risk-aware delivery — common in enterprise SaaS.",
    "Ignoring compliance; legal as black box forever; shipping blocked silently.",
    "Unknown and who you engaged. Interim ship boundaries. Actions: consult, feature flag, data minimization. Result. Learning.",
    "PII in logs example? Regional data residency?",
    ["Ambiguous requirement", "Architecture decision", "Customer escalation", "Failure"])

add("Ambiguity",
    "Describe a greenfield where you had to invent the process.",
    "Zero-to-one execution discipline.",
    "Chaos as fun; process overkill; no retrospective.",
    "Team size and stakes. Actions: minimal rituals (planning, RFC, on-call). Result: delivery and morale signal. Learning: what you’d keep at scale.",
    "Too much or too little process? First thing you’d add at 10 engineers?",
    ["Innovation", "Leadership", "Change", "Most impactful project"])

# ── Prioritization (8) ────────────────────────────────────────────────────────
add("Prioritization",
    "Tell me about prioritizing when everything was P0.",
    "Framework under pressure — kill criteria explicit.",
    "Doing everything poorly; hidden queue; no stakeholder renegotiation.",
    "Stack-rank dimensions: user harm, irreversibility, learning, contractual. Actions: list published, cuts communicated, trade-offs. Result: what shipped/deferred. Learning.",
    "Who angered? How handle slack pings?",
    ["Prioritization", "Tight deadline", "Leadership", "Customer escalation"])

add("Prioritization",
    "Describe killing a feature you had already built.",
    "Sunk cost maturity — customer and maintenance lens.",
    "Attachment to code; quiet shelf without telling users.",
    "Why built and why kill (usage, risk, strategy). Actions: stakeholder alignment, removal plan, comms. Result: maintenance saved or user confusion avoided. Learning.",
    "Partial kill vs full? Feature flag role?",
    ["Prioritization", "Failure", "Customer escalation", "Technical debt"])

add("Prioritization",
    "When did you re-sequence work after a new incident or deadline?",
    "Dynamic replanning — calm under change.",
    "Silent context switch; thrashing team; no communication.",
    "Trigger event. Actions: new order, who informed, what dropped. Result: incident resolved or deadline met. Learning: WIP policy.",
    "How often replan per week max? Push back on new P0?",
    ["Production outage", "Tight deadline", "Prioritization", "Communication"])

add("Prioritization",
    "Tell me about saying no to a senior stakeholder’s request.",
    "Courage with alternative — influence skill.",
    "Yes then fail; rude no; escalation dodge.",
    "Request and cost. Actions: no with data, smaller yes, timeline alternative. Result. Relationship Learning.",
    "Written trail? When involve your manager?",
    ["Influencing without authority", "Disagreement", "Prioritization", "Communication"])

add("Prioritization",
    "Describe your framework for prioritizing tech debt vs features.",
    "Sustainable velocity — not binary religion.",
    "All debt bad or all features; no metrics.",
    "Debt taxonomy (blocking, risk, drag). Allocation model (% or sprint theme). Example decision. Result on velocity/incidents. Learning.",
    "Interest rate metaphor — make concrete in your domain?",
    ["Technical debt", "Prioritization", "Architecture decision", "Most impactful project"])

add("Prioritization",
    "When did you use data to settle a priority fight?",
    "Evidence over loudest voice.",
    "Data dredging; analysis paralysis; weaponized metrics.",
    "Dispute and metric chosen (support, perf, revenue proxy, dev cost). Actions: query, share, decision. Result. Learning: metric gaming awareness.",
    "Wrong data once? Qualitative when quantitative missing?",
    ["Prioritization", "Customer escalation", "Performance improvement", "Disagreement"])

add("Prioritization",
    "Tell me about protecting the team from thrash.",
    "Shield and communicate — senior servanthood.",
    "Blocking all change; being unavailable; martyrdom.",
    "Thrash source (sales, exec, incidents). Actions: buffer, batch interrupts, negotiate dates. Result: focus time preserved. Learning: when to absorb vs escalate.",
    "Team feedback on your shielding? Ever too rigid?",
    ["Leadership", "Prioritization", "Communication", "Tight deadline"])

add("Prioritization",
    "Describe reprioritizing after learning something in production.",
    "Feedback loop from prod to roadmap.",
    "Ignoring prod signal; overreacting to one error.",
    "Signal (metric, experiment, incident). Interpretation. Actions: backlog change, comms. Result. Learning: monitoring you added.",
    "False alarm example? How fast to reprioritize?",
    ["Production outage", "Performance improvement", "Prioritization", "Customer escalation"])

# ── Mentorship (8) ──────────────────────────────────────────────────────────
add("Mentorship",
    "Tell me about mentoring someone who was struggling.",
    "Growth mindset for others — specific behaviors.",
    "Fixed label on mentee; doing their work; no manager partnership.",
    "Struggle area (debugging, system thinking, comms). Actions: goals, pairing cadence, safe tasks, feedback. Result: independence signal. Learning: what you’d start earlier.",
    "When escalate to manager? Mentee didn’t want help?",
    ["Mentoring", "Feedback", "Leadership", "Collaboration"])

add("Mentorship",
    "Describe raising the bar so juniors could ship without you in the path.",
    "Scaling quality — templates, reviews, tests.",
    "Gatekeeping; lowering bar; only verbal advice.",
    "Bottleneck you were. Actions: checklists, exemplar PRs, lint/tests, office hours. Result: review load or incident trend. Learning.",
    "First PR you stopped reviewing — anxiety?",
    ["Mentoring", "Change", "Leadership", "Technical debt"])

add("Mentorship",
    "When did you adapt your mentoring style for different people?",
    "Individualized growth — not one-size.",
    "Same speech for everyone; stereotyping learning styles.",
    "Two profiles contrast (needs structure vs autonomy). Actions adapted. Result. Learning: questions you ask new mentees.",
    "Cultural context? Remote mentoring?",
    ["Mentoring", "Leadership", "Feedback", "Collaboration"])

add("Mentorship",
    "Tell me about onboarding a new engineer to a complex React/TypeScript codebase.",
    "Structured onboarding — maps, milestones, safety.",
    "Sink or swim; only docs; overwhelming tour.",
    "Ramp plan (week 1 read, week 2 bug, week 3 feature). Actions: buddies, architecture map, first meaningful PR. Result: time-to-productivity proxy. Learning.",
    "What if codebase is legacy mess? How measure success?",
    ["Mentoring", "Cross-team collaboration", "Technical debt", "Most impactful project"])

add("Mentorship",
    "Describe when mentoring conflicted with delivery pressure.",
    "Trade-off between short deadline and long investment.",
    "Dropping mentoring silently; using mentee as output only.",
    "Deadline stakes. Actions: protected pairing time, smaller scoped teachable task, manager alignment. Result both delivery and growth. Learning.",
    "Would you make same trade again?",
    ["Mentoring", "Tight deadline", "Leadership", "Prioritization"])

add("Mentorship",
    "When did you help someone grow into senior scope?",
    "Sponsorship vs mentorship — visibility and stretch.",
    "Taking credit; stretch without support; surprise promotion push.",
    "Gap to senior (ownership, design, influence). Actions: opportunities, feedback, advocacy in cal. Result: promotion or scope expansion. Learning.",
    "Failed promotion — what then?",
    ["Mentoring", "Leadership", "Influencing without authority", "Feedback"])

add("Mentorship",
    "Tell me about reverse mentoring — learning from someone you mentored.",
    "Humility — two-way growth.",
    "Patronizing “they taught me empathy”; fake story.",
    "What they knew (tool, domain, perspective). How it changed your practice. Result for team. Learning.",
    "Junior teaching staff — how receive?",
    ["Mentoring", "Learning", "Collaboration", "Innovation"])

add("Mentorship",
    "Describe giving up being the bottleneck on your team.",
    "Delegation and trust — senior transition.",
    "Bottleneck pride; chaos after handoff; no documentation.",
    "Areas you hoarded (reviews, incidents, design). Actions: succession plan, shadowing reversed, metrics. Result: team autonomy. Learning.",
    "Quality dip during transition? How long?",
    ["Leadership", "Mentoring", "Change", "Production outage"])

# ── Feedback (8) ────────────────────────────────────────────────────────────
add("Feedback",
    "Tell me about receiving hard feedback that changed your behavior.",
    "Coachability — values and HM screens.",
    "Defensive anecdote; feedback was wrong but you pretend; no change named.",
    "Feedback content (specific). Initial reaction honest. Actions to change. Result observable. Learning.",
    "Who gave it? Still work that way?",
    ["Feedback", "Learning", "Failure", "Mistake"])

add("Feedback",
    "Describe giving critical feedback to a peer or report.",
    "Kind directness — SBI or similar structure.",
    "Sandwich cliché without substance; public criticism.",
    "Situation-Behavior-Impact frame. Private setting. Actions: examples, ask, agree follow-up. Result: behavior shift or clear boundary. Learning.",
    "They cried or pushed back? Manager involved?",
    ["Feedback", "Conflict", "Mentoring", "Communication"])

add("Feedback",
    "When did you ask for feedback proactively?",
    "Growth orientation — not waiting for review cycle.",
    "Vague “any feedback?”; arguing with answers.",
    "Trigger (after launch, lead role). Who you asked. Questions specific. Actions taken. Result. Learning.",
    "Skip-level feedback? 360?",
    ["Feedback", "Learning", "Leadership", "Communication"])

add("Feedback",
    "Tell me about feedback you disagreed with but acted on anyway.",
    "Disagree and commit interpersonal version.",
    "Passive aggressive compliance; no real try.",
    "Feedback and your view. Actions: experiment period, data gathered. Result: adopt, adapt, or push back with evidence later. Learning.",
    "When push back was right?",
    ["Feedback", "Disagreement", "Conflict", "Learning"])

add("Feedback",
    "Describe a performance conversation you initiated early.",
    "Courage before crisis — manager partnership.",
    "Waiting until PIP; gossip; no documentation.",
    "Signals seen. Actions: private talks, clear bar, support offered, manager loop. Result. Learning: early warning signs.",
    "Documentation level? HR involved when?",
    ["Feedback", "Leadership", "Conflict", "Mentoring"])

add("Feedback",
    "When did you translate vague feedback into concrete actions?",
    "Self-direction in growth — “be more strategic” problem.",
    "Complaining feedback was vague; no clarifying questions.",
    "Vague quote → clarifying questions → action plan → check-in. Result. Learning.",
    "Example vague phrase you’ve heard?",
    ["Feedback", "Learning", "Communication", "Leadership"])

add("Feedback",
    "Tell me about feedback in code review that changed team norms.",
    "Leverage review culture — scale behavior.",
    "Nitpick war; lecturing; no guide written.",
    "Pattern (tests, a11y, error handling). Actions: exemplar comments, guide, talk. Result: review quality. Learning.",
    "When review goes wrong? Nit vs block?",
    ["Feedback", "Change", "Mentoring", "Collaboration"])

add("Feedback",
    "Describe giving feedback upward to your manager.",
    "Psychological safety both directions — carefully.",
    "Complaint session; skip-level first; ultimatum.",
    "Issue impact on team. Actions: private respectful conversation, solutions suggested. Result. Learning.",
    "Ever backfire? When escalate?",
    ["Feedback", "Influencing without authority", "Communication", "Conflict"])

# ── Collaboration (8) ─────────────────────────────────────────────────────────
add("Collaboration",
    "Tell me about shipping something that required deep partnership with another team.",
    "Joint success — shared goals and contracts.",
    "Handoff mentality; credit hog; integration surprise at end.",
    "Teams and dependency. Actions: joint planning, interface tests, demo cadence. Result: on-time integration metric. Learning.",
    "Timezone pain? Contract arguments?",
    ["Cross-team collaboration", "Most impactful project", "Architecture decision", "Tight deadline"])

add("Collaboration",
    "Describe when another team blocked you — how you unblocked.",
    "Persistence without escalation theater.",
    "Escalation day one; villain; passive waiting.",
    "Blocker and root (priority, skill, misunderstanding). Actions: exec summary, offer help, trade, escalate with options. Result. Learning.",
    "When is escalation appropriate?",
    ["Cross-team collaboration", "Influencing without authority", "Conflict", "Prioritization"])

add("Collaboration",
    "When did you share credit vs take blame in a joint failure?",
    "Play as a team — values alignment.",
    "Blame external only; fake humility credit share.",
    "Failure description. Actions in review/postmortem: we language, your slice owned, credit to partners for saves. Result: trust. Learning.",
    "Manager view vs peer view?",
    ["Failure", "Cross-team collaboration", "Production outage", "Leadership"])

add("Collaboration",
    "Tell me about building trust with a team that had burned you before.",
    "Repair and verify — enterprise reality.",
    "Permanent grudge; trust me bro; no verification mechanism.",
    "Past break (missed SLA, bad rollback). Actions: small commitments kept, written agreements, checkpoints. Result: improved delivery. Learning.",
    "How long to rebuild? When walk away?",
    ["Cross-team collaboration", "Conflict", "Communication", "Production outage"])

add("Collaboration",
    "Describe contributing to a shared design system or platform other teams use.",
    "Platform mindset — consumers first.",
    "NIH component; no migration path; ignoring consumer feedback.",
    "Consumer pain. Actions: API design, docs, office hours, versioning. Result: adoption metric. Learning.",
    "Breaking change policy? v0 forever?",
    ["Cross-team collaboration", "Architecture decision", "Technical debt", "Innovation"])

add("Collaboration",
    "When did you compromise your team’s preference for the greater good?",
    "Organizational citizenship — not martyrdom.",
    "Resentful compliance; no voice recorded.",
    "Preference vs org need. Actions: advocate, lose, commit, document dissent if needed. Result. Learning.",
    "When not compromise?",
    ["Disagreement", "Cross-team collaboration", "Influencing without authority", "Leadership"])

add("Collaboration",
    "Tell me about async collaboration across three or more teams.",
    "Coordination at scale — docs and DRI.",
    "Meeting marathon; no DRI; lost decisions.",
    "Teams and goal. Actions: RACI-ish clarity, decision log, integration calendar. Result. Learning.",
    "Tooling (Jira/Confluence meta OK as practice)?",
    ["Cross-team collaboration", "Communication", "Leadership", "Most impactful project"])

add("Collaboration",
    "Describe repairing collaboration after a miscommunication.",
    "Relationship maintenance — long games.",
    "Ignoring; forced happy face; rehashing in interview.",
    "Miscommunication and impact. Actions: sync, reset expectations, process patch. Result: delivery resumed. Learning.",
    "Written apology ever?",
    ["Communication", "Conflict", "Cross-team collaboration", "Mistake"])

# ── Technical decisions (8) ───────────────────────────────────────────────────
add("Technical decisions",
    "Tell me about a significant architecture decision in a React/Node system.",
    "Full-stack judgment — boundaries, contracts, operability.",
    "Diagram name-dropping; no constraints; no rejected option.",
    "User scale and constraint. Options (BFF, monolith module, microservice). Criteria. Decision and rollback plan. Result metrics. Learning.",
    "Draw boundaries today? Monolith vs services?",
    ["Architecture decision", "Hardest technical problem", "Most impactful project", "Performance improvement"])

add("Technical decisions",
    "Describe choosing between monolith module vs microservice for a new capability.",
    "Reversibility and team topology — classic senior trade-off.",
    "Microservices because resume; monolith because lazy.",
    "Capability and coupling. Team count. Operational cost honest. Choice and migration trigger if monolith. Result. Learning.",
    "Extract later cost? Shared DB anti-pattern?",
    ["Architecture decision", "Technical debt", "Cross-team collaboration", "Innovation"])

add("Technical decisions",
    "When did you reject a popular library or pattern — why?",
    "Independent evaluation — bundle size, operability, hiring.",
    "NIH syndrome; trend hate without analysis.",
    "Library/pattern and context. Evaluation dimensions (a11y, SSR, lock-in, perf). Decision and alternative. Result. Learning.",
    "Later adoption when conditions changed?",
    ["Architecture decision", "Performance improvement", "Disagreement", "Hardest technical problem"])

add("Technical decisions",
    "Tell me about a decision optimized for 10× scale you didn’t have yet.",
    "Appropriate pre-investment — not gold plating.",
    "Over-engineering without user; no YAGNI acknowledgment.",
    "Current scale and 10× trigger. Cheaper now vs expensive later. Actions: seams, metrics, deferrals explicit. Result. Learning: trigger you watch.",
    "Paid off or YAGNI won?",
    ["Architecture decision", "Performance improvement", "Technical debt", "Most impactful project"])

add("Technical decisions",
    "Describe balancing speed vs maintainability in a TypeScript codebase.",
    "Pragmatic craft — types, tests, debt tickets.",
    "Speed always; perfection always; no timeline context.",
    "Deadline and risk. Actions: typed boundaries, test where regress costly, ticket debt. Result. Learning.",
    "any vs strict? Test pyramid slice?",
    ["Technical debt", "Tight deadline", "Architecture decision", "Innovation"])

add("Technical decisions",
    "When did you involve others in an ADR and change your mind?",
    "Intellectual humility in design.",
    "Stubborn; committee forever; hidden decision.",
    "Original position. Feedback that landed. Actions: ADR revision, credit. Result: better outcome metric. Learning.",
    "How long ADR process? When timebox?",
    ["Architecture decision", "Disagreement", "Collaboration", "Influencing without authority"])

add("Technical decisions",
    "Tell me about API contract decisions between frontend and backend.",
    "Contract-first collaboration — errors, pagination, versioning.",
    "Backend drives only; breaking changes casual; no versioning story.",
    "Consumer needs (mobile, offline, perf). Contract choices (GraphQL vs REST slice, error shape). Actions: schema review, codegen, compatibility tests. Result. Learning.",
    "Breaking change policy? Version in URL vs header?",
    ["Architecture decision", "Cross-team collaboration", "Performance improvement", "Hardest technical problem"])

add("Technical decisions",
    "Describe a decision driven by accessibility or security requirements.",
    "Non-functional requirements as first-class — Atlassian customer trust.",
    "Checkbox a11y; security as afterthought; compliance name drop only.",
    "Requirement source (WCAG, OWASP, policy). Options impact on UX/dev cost. Decision. Verification (axe, pen test). Result. Learning.",
    "Trade UX for a11y example? Threat model briefly?",
    ["Architecture decision", "Customer escalation", "Innovation", "Most impactful project"])

# ── Production incidents (8) ──────────────────────────────────────────────────
add("Production incidents",
    "Tell me about your role in a major production outage.",
    "Incident command behaviors — calm, communicative, technical.",
    "Heroics only; no timeline; blame.",
    "SEV level and user impact. Role (IC, comms, mitigator). Actions chronological: detect, mitigate, comms, root cause path. Result: MTTR honest. Learning: postmortem action you owned.",
    "First 5 minutes? Sleep deprivation?",
    ["Production outage", "Failure", "Leadership", "Communication"])

add("Production incidents",
    "Describe an incident where the frontend was implicated.",
    "Client-side failure modes — cache, flags, bundle, auth token.",
    "“Just a JS bug” minimizing; no backend check.",
    "Symptom (blank screen, loop, stale data). Actions: reproduce, rollback/canary, feature flag. Coordination with API team if needed. Result. Learning: guard (error boundary, monitoring).",
    "Source maps in prod? RUM tools?",
    ["Production outage", "Performance improvement", "Mistake", "Hardest technical problem"])

add("Production incidents",
    "When did you improve incident response after a bad postmortem?",
    "Be the change — process improvement from pain.",
    "Postmortem theater; no action items closed.",
    "Postmortem gap (blame, missing runbook). Actions: template, roles, drill, tooling. Result: next incident comparison. Learning.",
    "Blameless when someone clearly erred?",
    ["Production outage", "Change", "Leadership", "Learning"])

add("Production incidents",
    "Tell me about communicating during an active SEV.",
    "Status cadence and uncertainty language.",
    "Radio silence; overconfidence; technical detail to exec channel.",
    "Audience map ( eng, leadership, support). Update template (impact, mitigation, ETA unknown ok). Actions you took. Result: trust signal. Learning.",
    "Wrong ETA — how correct?",
    ["Production outage", "Communication", "Customer escalation", "Leadership"])

add("Production incidents",
    "Describe a near-miss you caught before customers noticed.",
    "Proactive quality — alerts, dogfood, chaos.",
    "Luck without system; claiming genius.",
    "Detection mechanism. Actions: cancel deploy, fix, additional monitor. Result: avoided impact estimate honest. Learning.",
    "False positive rate acceptable?",
    ["Production outage", "Mistake", "Innovation", "Performance improvement"])

add("Production incidents",
    "When did you argue against a hasty hotfix during an incident?",
    "Judgment under adrenaline — second SEV prevention.",
    "Riskless hero hotfix; paralysis — need balance shown.",
    "Incident state and hotfix risk (data corruption, partial fix). Actions: rollback vs fix debate, who decided. Result. Learning.",
    "Ever wrong to wait? Ever wrong to hotfix?",
    ["Production outage", "Disagreement", "Technical decisions", "Failure"])

add("Production incidents",
    "Tell me about on-call pain you fixed structurally.",
    "Sustainable ops — not hero on-call forever.",
    "Complaining; quitting on-call; manual toil only.",
    "Toil metric (pages, manual steps). Actions: automation, better alerts, runbooks, ownership rotation. Result: page trend. Learning.",
    "Alert fatigue approach?",
    ["Production outage", "Technical debt", "Change", "Performance improvement"])

add("Production incidents",
    "Describe learning from an outage that recurred.",
    "Root cause vs contributing cause — fix depth.",
    "Same superficial fix twice; scapegoat.",
    "First vs second outage. Why shallow fix failed. Actions: deeper fix, verification, game day. Result. Learning.",
    "When close as duplicate root cause?",
    ["Production outage", "Failure", "Learning", "Mistake"])

# ── Influencing (8) ─────────────────────────────────────────────────────────
add("Influencing",
    "Tell me about influencing without formal authority.",
    "Core senior IC skill — evidence, relationships, persistence.",
    "Authority borrowed from manager; nagging; no clear ask.",
    "Goal and stakeholders. Actions: map incentives, prototype, pilot, data from incident. Result. Learning.",
    "Longest influence campaign? When quit?",
    ["Influencing without authority", "Cross-team collaboration", "Leadership", "Innovation"])

add("Influencing",
    "Describe changing another team’s roadmap with evidence.",
    "Cross-team prioritization — mutual benefit framed.",
    "Demand without trade; escalation threat first.",
    "Evidence (incident cost, support load). Actions: meeting, offer resources, shared OKR link. Result: reprioritization or honest no. Learning.",
    "What did you offer in return?",
    ["Influencing without authority", "Prioritization", "Production outage", "Customer escalation"])

add("Influencing",
    "When did you use a prototype to win a technical argument?",
    "Show don’t tell — appropriate for UI/API debates.",
    "Production prototype in debate; no disposal plan.",
    "Debate topic. Prototype scope and timebox. Actions: demo, metrics captured. Result: decision. Learning.",
    "Throwaway stack? When prototype misled?",
    ["Influencing without authority", "Innovation", "Architecture decision", "Disagreement"])

add("Influencing",
    "Tell me about influencing up — staff engineer, principal, or exec.",
    "Executive communication — concise, decision-oriented.",
    "Too much detail; no ask; bypassing your manager inappropriately.",
    "Audience care-abouts. Actions: brief, options, recommendation, risk. Result. Learning: prep ritual.",
    "Manager relationship? Skip-level etiquette?",
    ["Influencing without authority", "Communication", "Leadership", "Architecture decision"])

add("Influencing",
    "Describe when you failed to influence and what you did next.",
    "Resilience — disagree and commit or escalate wisely.",
    "Sour grapes; I told you so at incident.",
    "Proposal and resistance reason. Actions tried. Outcome. Actions after failure (commit, document, revisit trigger). Learning.",
    "Would same approach work elsewhere?",
    ["Influencing without authority", "Failure", "Disagreement", "Learning"])

add("Influencing",
    "When did you build a coalition across teams for a shared standard?",
    "Standards adoption — lint, API style, design tokens.",
    "Mandate fantasy; no pilot team.",
    "Problem fragmentation cost. Actions: champions, pilot, migration plan. Result: adoption %. Learning.",
    "Enforcement vs encouragement?",
    ["Influencing without authority", "Change", "Cross-team collaboration", "Architecture decision"])

add("Influencing",
    "Tell me about influencing product direction as an engineer.",
    "Product sense — not PM cosplay.",
    "Feature lists; no user evidence; derailing roadmap.",
    "User insight source. Actions: data, prototype, customer quote via proper channel. Result: roadmap change or not. Learning.",
    "When stay in lane?",
    ["Influencing without authority", "Customer escalation", "Innovation", "Most impactful project"])

add("Influencing",
    "Describe using incident data or metrics to change behavior.",
    "Objective influence — engineering culture lever.",
    "Cherry-picked graph; shame campaign.",
    "Metric and behavior targeted. Actions: presentation, action items, follow-up measure. Result. Learning.",
    "Metric misused? Gaming?",
    ["Influencing without authority", "Production outage", "Change", "Prioritization"])

# ── Change (8) ────────────────────────────────────────────────────────────────
add("Change",
    "Tell me about improving a process nobody owned.",
    "Be the change you seek — Atlassian value literal.",
    "Complaint only; massive process deck; no adoption.",
    "Process pain (releases, RFCs, on-call). Actions: MVP process, pilot, iterate. Result: cycle time or incident metric. Learning.",
    "Resistance source?",
    ["Change", "Innovation", "Leadership", "Production outage"])

add("Change",
    "Describe driving adoption of a new practice — testing, RFCs, design review.",
    "Change management for engineers — show benefit fast.",
    "Mandate from above only; no teaching.",
    "Practice and failure mode without it. Actions: templates, examples, office hours, metrics. Result: adoption. Learning.",
    "Holdout team?",
    ["Change", "Mentoring", "Technical debt", "Architecture decision"])

add("Change",
    "When did you be the change without waiting for permission?",
    "Initiative within bounds — know when to ask forgiveness vs permission.",
    "Reckless prod change; policy violation; no socialization.",
    "Gap and risk. Actions: small start, transparency, invite feedback. Result. Learning: permission line.",
    "Ever told to stop? Rollback of process?",
    ["Change", "Innovation", "Leadership", "Influencing without authority"])

add("Change",
    "Tell me about changing team culture around quality or on-call.",
    "Culture as repeated behaviors — not posters.",
    "Culture deck; blaming individuals; quality sprint theater.",
    "Before/after behaviors. Actions: rituals, incentives, lead by example. Result: measurable quality signal. Learning.",
    "Speed vs quality tension?",
    ["Change", "Production outage", "Feedback", "Leadership"])

add("Change",
    "Describe organizational change — reorg or merge — that disrupted your project.",
    "Adaptability and stakeholder re-alignment.",
    "Victim narrative; work abandoned without comms.",
    "Change event. Actions: re-map stakeholders, re-negotiate scope, document. Result: project outcome. Learning.",
    "People side — lost trust?",
    ["Change", "Ambiguous requirement", "Communication", "Leadership"])

add("Change",
    "When did you simplify something over-engineered?",
    "Courage to delete — customer and maintainer win.",
    "Mocking authors; big bang rewrite.",
    "Complexity cost. Actions: incremental simplification, metrics, migration. Result: operability. Learning.",
    "Who resisted simplification?",
    ["Technical debt", "Architecture decision", "Change", "Innovation"])

add("Change",
    "Tell me about navigating a reorg or team merge.",
    "People and technical integration — diplomacy.",
    "Territorial; duplicate systems forever; ignoring people.",
    "Merge challenges (tools, on-call, code). Actions: integration plan, social events optional, tech choices. Result. Learning.",
    "Duplicate service retirement?",
    ["Change", "Cross-team collaboration", "Leadership", "Conflict"])

add("Change",
    "Describe pushing back on “the way we’ve always done it.”",
    "Constructive disruption — evidence required.",
    "Change for novelty; disrespect to tenure.",
    "Ritual and cost. Actions: experiment, data, propose alternative. Result. Learning.",
    "When tradition was right?",
    ["Change", "Influencing without authority", "Disagreement", "Innovation"])

# ── Learning (8) ──────────────────────────────────────────────────────────────
add("Learning",
    "Tell me about learning a new domain or stack quickly for a project.",
    "Learning agility — official handbook theme.",
    "Tutorial hell; no production boundary; exaggerating mastery.",
    "Deadline and unknown. Actions: learning plan, spike, mentors, scope cut. Result: shipped capability. Learning: depth you still lack honestly.",
    "What did you skip? Still expert?",
    ["Learning", "Hardest technical problem", "Tight deadline", "Innovation"])

add("Learning",
    "Describe staying current without chasing every framework.",
    "Judgment on hype — senior filter.",
    "Framework churn resume; cynic with no learning.",
    "Criteria (problem class, ecosystem, job to be done). Actions: curated learning budget, apply to work. Result: example adoption or reject. Learning.",
    "Last thing you deliberately ignored?",
    ["Learning", "Architecture decision", "Innovation", "Technical debt"])

add("Learning",
    "When did you teach yourself something that unblocked the team?",
    "Self-directed learning with team payoff.",
    "Gatekeeping new knowledge; learning unrelated vanity.",
    "Blocker. Resources used. Actions: share doc, lunch learn. Result: team unblocked metric. Learning.",
    "How deep before sharing?",
    ["Learning", "Mentoring", "Hardest technical problem", "Innovation"])

add("Learning",
    "Tell me about being wrong in a technical debate and updating your view.",
    "Model updating — senior intellectual honesty.",
    "Never wrong; fake pivot; public doubling down.",
    "Position and evidence that changed you. Actions: concede, integrate, document. Result: better decision. Learning.",
    "Hardest person to concede to?",
    ["Learning", "Disagreement", "Feedback", "Hardest technical problem"])

add("Learning",
    "Describe how you learn from postmortems and reviews systematically.",
    "Continuous improvement habit — not one-off.",
    "Skim postmortem; no personal action item.",
    "Sources (PIRs, retros, reviews). Actions: personal log, theme tracking, experiment. Result: behavior change example. Learning.",
    "Postmortem without blame — still extract lesson?",
    ["Learning", "Production outage", "Change", "Feedback"])

add("Learning",
    "When did you invest in learning that didn’t pay off immediately?",
    "Long-term investment — honest ROI.",
    "Everything pays off magically; regret only.",
    "Investment (course, refactor study, tool). Expected vs actual payoff. Actions: sunk cost decision. Result. Learning: filter for next time.",
    "Still recommend that investment?",
    ["Learning", "Failure", "Technical debt", "Innovation"])

add("Learning",
    "Tell me about bringing a new practice to a team — testing, perf, a11y.",
    "Evangelism through wins — start small.",
    "All-or-nothing mandate; no baseline.",
    "Practice and gap. Actions: pilot project, measure, expand. Result. Learning.",
    "First ally recruited how?",
    ["Learning", "Change", "Performance improvement", "Mentoring"])

add("Learning",
    "Describe learning from more senior engineers during your growth to senior.",
    "Coaching receptivity — meta for loop.",
    "Name dropping mentors; no applied lesson.",
    "Who and what they modeled (design, politics, depth). Actions you copied. Result in your career. Learning: what you still seek in mentors.",
    "Difference mentor vs sponsor?",
    ["Learning", "Mentoring", "Leadership", "Most impactful project"])


def bq() -> str:
    blocks = []
    cat_counts = {c: sum(1 for x in Q if x["cat"] == c) for c in CATS}
    for i, item in enumerate(Q, 1):
        hid = f"bq-{i}"
        blocks.append(f'''
<article class="q" id="{hid}" data-search="{esc(item["q"] + " " + item["cat"])}" data-stype="Behavioral question" data-cat="{esc(item["cat"])}">
  <div class="meta-row"><span class="chip">{esc(item["cat"])}</span><span class="chip">Q{i}</span></div>
  <h3>{i}. {esc(item["q"])}</h3>
  <p><b>What interviewer is testing.</b> {item["testing"]}</p>
  <p><b>Weak answer looks like.</b> {item["weak"]}</p>
  <p><b>Strong answer should contain.</b> {item["strong"]}</p>
  <p><b>Follow-up questions.</b> {item["follow"]}</p>
  <p><b>Suggested story categories.</b> {item["stories"]}</p>
  <p><button type="button" class="toggle-btn" data-complete="questions" data-cid="{hid}">Mark complete</button></p>
</article>''')
    tab_btns = "".join(
        f'<button type="button" class="tab" data-tab="{esc(c)}">{esc(c)} ({cat_counts[c]})</button>'
        for c in CATS
    )
    n = len(Q)
    return f'''
<section class="block" id="bq" data-search="Behavioral Question Bank STAR practice" data-stype="Section">
  <p class="kicker">{n} practice questions</p>
  <h2 class="section-title">Behavioral Question Bank</h2>
  <p class="lede">Practice behavioral questions for senior React/TypeScript/Node loops — including values and hiring-manager conversations. <b>Not</b> official or leaked Atlassian questions. Answer aloud using your Story Bank; frameworks here are guides, not scripts. No invented experiences.</p>
  <div class="tabs" data-tabs="bq">
    <button type="button" class="tab active" data-tab="all">All ({n})</button>
    {tab_btns}
  </div>
  {''.join(blocks)}
</section>
'''
