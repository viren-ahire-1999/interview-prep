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
