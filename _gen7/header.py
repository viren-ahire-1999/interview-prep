def html_head(css: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI Engineer — Basics to Advanced</title>
  <meta name="description" content="A complete, readable course from AI foundations through classical ML, deep learning, LLMs, RAG, agents, evaluation, and production MLOps." />
  <style>
{css}
  </style>
</head>
<body>
<div class="sidebar-backdrop" id="sidebar-backdrop"></div>
<aside class="sidebar" id="sidebar">
  <div class="brand">
    <div class="brand-mark">AI</div>
    <div>
      <h1>AI Engineer</h1>
      <p>Basics → production</p>
    </div>
    <button type="button" class="icon-btn sidebar-hide" id="sidebar-hide" title="Hide sidebar" aria-label="Hide sidebar">«</button>
  </div>
  <div class="search-wrap">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3-3"/></svg>
    <input id="global-search" type="search" placeholder="Search lessons, RAG, eval..." autocomplete="off" />
    <div class="search-results" id="search-results"></div>
  </div>
  <nav>
    <div class="nav-group">
      <h2>Library</h2>
      <a href="index.html">All prep</a>
    </div>
    <div class="nav-group">
      <h2>Start</h2>
      <a href="#dashboard">Dashboard</a>
      <a href="#plan">42-Day Plan</a>
      <a href="#howto">How to learn</a>
      <a href="#role">The role</a>
    </div>
    <div class="nav-group">
      <h2>Foundations</h2>
      <a href="#map">Map of AI</a>
      <a href="#python">Python for AI</a>
      <a href="#math">Math you need</a>
      <a href="#data">Data &amp; leakage</a>
    </div>
    <div class="nav-group">
      <h2>Classical ML</h2>
      <a href="#supervised">Supervised learning</a>
      <a href="#models">Core models</a>
      <a href="#metrics">Metrics</a>
      <a href="#features">Features &amp; regularize</a>
    </div>
    <div class="nav-group">
      <h2>Deep learning</h2>
      <a href="#nn">Neural nets</a>
      <a href="#cnn">CNNs &amp; sequences</a>
      <a href="#transformers">Attention &amp; transformers</a>
    </div>
    <div class="nav-group">
      <h2>Applied GenAI</h2>
      <a href="#embed">Embeddings &amp; vectors</a>
      <a href="#llms">LLM landscape</a>
      <a href="#prompt">Prompting</a>
      <a href="#rag">RAG</a>
      <a href="#finetune">Fine-tuning</a>
      <a href="#agents">Agents</a>
      <a href="#eval">Evaluation</a>
      <a href="#safety">Safety</a>
    </div>
    <div class="nav-group">
      <h2>Production</h2>
      <a href="#serve">Serving &amp; cost</a>
      <a href="#mlops">MLOps</a>
      <a href="#design">AI system design</a>
    </div>
    <div class="nav-group">
      <h2>Practice</h2>
      <a href="#practical">Practical studies</a>
      <a href="#problems">Exercise bank</a>
      <a href="#feq">Q&amp;A</a>
      <a href="#mock">Mock Interview</a>
    </div>
    <div class="nav-group">
      <h2>Track</h2>
      <a href="#revision">Revision</a>
      <a href="#progress">Progress</a>
      <a href="#readiness">Readiness</a>
      <a href="#glossary">Glossary</a>
      <a href="#resources">Resources</a>
    </div>
  </nav>
</aside>
<div class="main">
  <header class="topbar">
    <button class="menu-btn" id="menu-btn" type="button" aria-label="Toggle sidebar">☰</button>
    <a class="hub-link" href="index.html">All prep</a>
    <div class="overall-wrap">
      <div class="overall-label"><span>AI Engineer completion</span><strong id="overall-pct">0%</strong></div>
      <div class="bar"><span id="overall-bar"></span></div>
    </div>
    <button class="icon-btn" id="theme-toggle" type="button" title="Toggle theme" aria-label="Toggle theme">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
    </button>
  </header>
  <main class="content">
"""


def html_foot(js: str) -> str:
    return f"""
  </main>
</div>
<button class="back-top" id="back-top" type="button" aria-label="Back to top">↑</button>
<script>
{js}
</script>
</body>
</html>
"""
