import html as _html


def esc(s: str) -> str:
    return _html.escape(s)


def code(lang: str, src: str) -> str:
    return (
        f'<div class="code-block"><div class="code-head"><span>{lang}</span>'
        f'<button type="button" class="copy-btn">Copy</button></div>'
        f"<pre><code>{esc(src)}</code></pre></div>"
    )


def topic(tid: str, title: str, search: str, stype: str, body: str, group: str = "topics") -> str:
    return f'''
<article class="topic" id="{tid}" data-search="{esc(search)}" data-stype="{esc(stype)}">
  <h3>{title}</h3>
  {body}
  <p><button type="button" class="toggle-btn" data-complete="{group}" data-cid="{tid}">Mark complete</button></p>
</article>
'''


def diagram(text: str) -> str:
    return f'<div class="diagram">{esc(text)}</div>'


def callout(text: str, kind: str = "") -> str:
    cls = f" callout {kind}".strip() if kind else "callout"
    return f'<div class="{cls}">{text}</div>'


def format_explain(idea: str, time: str, space: str, extra: dict | None) -> str:
    extra = extra or {}
    why = extra.get("why") or idea
    steps = extra.get("steps") or [
        idea,
        "Keep that invariant true after every index (or every recursive call).",
        "Return the accumulated answer, or a sentinel if the input cannot produce one.",
    ]
    example = extra.get("example") or ""
    trap = extra.get("trap") or ""
    items = "".join(f"<li>{esc(s)}</li>" for s in steps)
    ex_html = f'<p><b>Trace.</b></p><div class="diagram">{esc(example)}</div>' if example else ""
    trap_html = f"<p><b>Watch.</b> {esc(trap)}</p>" if trap else ""
    return f'''
<div class="explain-sol">
  <p><b>Why this works.</b> {esc(why)}</p>
  <p><b>Step by step.</b></p>
  <ol class="tight">{items}</ol>
  {ex_html}
  {trap_html}
  <p><b>Complexity.</b> Time {esc(time)}. Extra space {esc(space)}.</p>
</div>
'''


def solution_reveal(pid: str, idea: str, src: str, time: str, space: str, extra: dict | None) -> str:
    gid = f"{pid}-sol"
    return f'''
  <div class="tabs sol-tabs" data-tabs="{gid}">
    <button type="button" class="tab active" data-tab="code">Code</button>
    <button type="button" class="tab" data-tab="explain">Explain solution</button>
  </div>
  <div data-tabpanel="{gid}" data-tab="code">
    <p><b>Idea.</b> {idea}</p>
    {code("JavaScript", src)}
    <p><b>Time.</b> {time} &nbsp; <b>Space.</b> {space}</p>
  </div>
  <div class="hidden" data-tabpanel="{gid}" data-tab="explain">
    {format_explain(idea, time, space, extra)}
  </div>
'''


def practice_problem(pid: str, n: int, title: str, level: str, cat: str, trains: str, prompt: str, idea: str, src: str, time: str, space: str) -> str:
    """Topic-local practice card. Counts as a Problem (designs). Not filterable by the mixed bank."""
    from explains import GYM
    return f'''
<article class="problem" id="{pid}" data-pid="{pid}" data-search="{esc(title)}" data-stype="Topic problem" data-cat="{cat}" data-level="{level}" data-mock="1">
  <div class="meta-row"><span class="badge badge-{level}">{level}</span><span class="chip">{cat}</span><span class="chip">{esc(trains)}</span><span class="badge badge-pattern">Topic practice</span></div>
  <h3>{n}. {esc(title)}</h3>
  <p>{esc(prompt)}</p>
  <p><button type="button" class="toggle-btn" data-toggle="{pid}-a">Reveal solution</button>
     <button type="button" class="toggle-btn" data-complete="designs" data-cid="{pid}">Mark complete</button></p>
  <div class="reveal" id="{pid}-a">
    {solution_reveal(pid, idea, src, time, space, GYM.get(pid))}
  </div>
  <div class="status-btns">
    <button type="button" data-status="not-started">Not Started</button>
    <button type="button" data-status="attempted">Attempted</button>
    <button type="button" data-status="solved">Solved</button>
    <button type="button" data-status="review">Review</button>
    <button type="button" data-status="mastered">Mastered</button>
  </div>
</article>
'''


def practice_gym(gid: str, title: str, intro: str, rows: list) -> str:
    blocks = [practice_problem(*row) for row in rows]
    return f'''
<div class="topic-gym" id="{gid}" data-search="{esc(title)}" data-stype="Practice gym">
  <div class="card" style="margin: 22px 0 14px">
    <h3>{esc(title)}</h3>
    <p>{intro}</p>
    <p class="stat-sub">{len(rows)} problems · write JS first, then reveal. Use <b>Explain solution</b> after you have an approach. Practice items, not official company questions. The mixed Problem bank is later for interview order.</p>
  </div>
  {''.join(blocks)}
</div>
'''
