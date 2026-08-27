def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def code(lang: str, src: str) -> str:
    return (
        f'<div class="code-block"><div class="code-head"><span>{lang}</span>'
        f'<button type="button" class="copy-btn">Copy</button></div>'
        f"<pre><code>{esc(src)}</code></pre></div>"
    )


def problem(p: dict) -> str:
    hid = f"hint-{p['id']}"
    sid = f"sol-{p['id']}"
    eid = f"exp-{p['id']}"
    return f'''
<article class="problem" id="p-{p["id"]}" data-pid="{p["id"]}" data-name="{p["name"]}"
  data-difficulty="{p["diff"]}" data-pattern="{p["pattern"]}" data-topic="{p["topic"]}"
  data-search="{p["name"]} {p["pattern"]}" data-stype="DSA problem">
  <div class="meta-row">
    <span class="badge badge-{p["diff"]}">{p["diff"].upper()}</span>
    <span class="badge badge-pattern">{p["pattern"]}</span>
    <span class="chip">{p["topic"]}</span>
  </div>
  <h3>{p["name"]}</h3>
  <div class="problem-body">
    <p><b>Why this problem matters.</b> {p["why"]}</p>
    <p><b>Problem (original summary).</b> {p["stmt"]}</p>
    <p><b>Example.</b> Input: <code>{esc(p["exin"])}</code> → Output: <code>{esc(p["exout"])}</code>. {p.get("exnote","")}</p>
    <p><b>Constraints (typical).</b> {p["cons"]}</p>
    <p><button type="button" class="toggle-btn" data-toggle="{hid}">Hints</button>
       <button type="button" class="toggle-btn" data-toggle="{eid}">Explanation</button>
       <button type="button" class="toggle-btn" data-toggle="{sid}">Solution</button></p>
    <div class="reveal" id="{hid}"><p>{p["hints"]}</p></div>
    <div class="reveal" id="{eid}">
      <p><b>Brute force.</b> {p["brute"]}</p>
      <p><b>Optimal approach.</b> {p["opt"]}</p>
      <p><b>Step-by-step reasoning.</b> {p["steps"]}</p>
      <p><b>Time / space.</b> {p["cx"]}</p>
      <p><b>Common mistakes.</b> {p["mistakes"]}</p>
      <p><b>Edge cases.</b> {p["edges"]}</p>
      <p><b>Follow-ups.</b> {p["follow"]}</p>
      <p><b>Interviewer discussion.</b> {p["talk"]}</p>
    </div>
    <div class="reveal" id="{sid}">
      {code("TypeScript", p["sol"])}
    </div>
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
