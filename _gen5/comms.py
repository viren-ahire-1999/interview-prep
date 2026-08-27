from util import topic, callout, code


def comms() -> str:
    t1 = topic("cm-open", "Opening and closing scripts you adapt, not recite",
               "how to talk frontend system design interview", "Theory", f'''
  <p>Do not memorize a bio. Do memorize a <b>shape</b>.</p>
  <p><b>Open.</b> “I’ll confirm users and the money path, write NFRs, assume numbers you can correct, then design the client: shell, data, and the interaction that must stay fast. I’ll say what I would not build in v1.”</p>
  <p><b>Mid-course correction.</b> “I’m going to assume polling is enough so we can finish failure and a11y. We can upgrade to WebSockets if you want depth there.”</p>
  <p><b>Close.</b> “v1 is X. I rejected Y because Z. I would watch these metrics. Where do you want to go deeper?”</p>
  {callout("If you do not know a protocol, say so and design the client around a freshness SLA. That is stronger than inventing Kafka topology.")}
  ''', "exercises")

    t2 = topic("cm-white", "Whiteboard habits that look senior",
               "whiteboard frontend design habits", "Theory", f'''
  <ul>
    <li>Write FR / NFR / numbers at the top. Do not let them vanish.</li>
    <li>Draw arrows of data flow, not only boxes.</li>
    <li>Star the LCP element and the money click.</li>
    <li>Box “degrade” in public.</li>
    <li>Leave a corner for “rejected.”</li>
  </ul>
  {code("text", '''Users: logged-in PM, desktop
NFR: INP drag <200ms, keyboard move
Scale: 400 cards, 10k filter
v1: poll, no CRDT, iframe plugins
Reject: in-process vendor JS''')}
  ''', "exercises")

    t3 = topic("cm-pushback", "Pushing back without sounding difficult",
               "challenge requirements frontend interview", "Theory", f'''
  <p>“Realtime for the badge” can become polling if they do not have a 1s SLA. Ask: “What happens if the badge is 30 seconds stale?” If they shrug, you just saved a WebSocket.</p>
  <p>“Design Google Docs” at minute 5: “I’ll own read/edit split, versioned save, and conflict UX. I will not invent OT in this hour unless you want to spend it there — I’d rather get a11y and offline right.” That is leadership.</p>
  ''', "exercises")

    return f'''
<section class="block" id="comms" data-search="How to talk frontend system design" data-stype="Section">
  <p class="kicker">Delivery</p>
  <h2 class="section-title">How to talk</h2>
  <p class="lede">The same design with no rejected options and no degrade sentence will not pass a senior bar.</p>
  {t1}{t2}{t3}
</section>
'''


def adrs() -> str:
    drills = [
        ("adr-render", "Rendering for a wiki",
         "A public read URL and a logged-in editor. Write an ADR: SSR/stream read vs CSR editor."),
        ("adr-plugin", "Plugin isolation",
         "Vendors want in-process JS for “native look.” Write an ADR: iframe vs in-process."),
        ("adr-state", "Selected issue",
         "Two engineers stored selected issue in Redux only. Write an ADR to move it to the URL."),
        ("adr-ws", "Notification freshness",
         "PM wants “live.” SLA is unspecified. Write an ADR: 30s poll vs WS."),
        ("adr-grid", "Select all",
         "Ops wants select-all on 50k rows. Write an ADR: page vs query, and how export works."),
        ("adr-ds", "Button API",
         "12 teams request new Button props weekly. Write an ADR: variants vs composition."),
        ("adr-upload", "2GB attach",
         "Platform wants uploads through the Node BFF “for logging.” Write an ADR: signed URL vs proxy."),
        ("adr-i18n", "Catalogs",
         "One mega JSON for all locales is in main. Write an ADR to split by route."),
    ]
    cards = []
    for cid, title, prompt in drills:
        cards.append(topic(cid, title, title + " ADR", "ADR drill", f'''
  <p>{prompt}</p>
  <p>Use: <b>Context → options → decision → why → consequence.</b> Speak it in 60 seconds. Then write four sentences.</p>
  <p>Mark complete only if you named a consequence (what got harder).</p>
  ''', "exercises"))

    return f'''
<section class="block" id="adrs" data-search="ADR drills frontend architecture" data-stype="Section">
  <p class="kicker">Decision records</p>
  <h2 class="section-title">ADR drills</h2>
  <p class="lede">Senior interviews are ADRs with an audience. Do these out loud.</p>
  {''.join(cards)}
</section>
'''
