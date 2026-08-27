def html_head(css: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Atlassian Senior SWE — Phase 2 Frontend Architecture</title>
  <meta name="description" content="Self-contained Phase 2 prep: React internals, frontend architecture, performance, system design, and senior trade-offs." />
  <style>
{css}
  </style>
</head>
<body>
<div class="sidebar-backdrop" id="sidebar-backdrop"></div>
<aside class="sidebar" id="sidebar">
  <div class="brand">
    <div class="brand-mark">2</div>
    <div>
      <h1>Phase 2 Prep</h1>
      <p>Atlassian · Senior SWE</p>
    </div>
    <button type="button" class="icon-btn sidebar-hide" id="sidebar-hide" title="Hide sidebar" aria-label="Hide sidebar">«</button>
  </div>
  <div class="search-wrap">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3-3"/></svg>
    <input id="global-search" type="search" placeholder="Search architecture, React..." autocomplete="off" />
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
      <a href="#plan">30-Day Plan</a>
    </div>
    <div class="nav-group">
      <h2>Architecture</h2>
      <a href="#fundamentals">Fundamentals</a>
      <a href="#react-arch">React Architecture</a>
      <a href="#state">State Management</a>
      <a href="#fetching">Data Fetching</a>
      <a href="#components">Component Design</a>
      <a href="#design-systems">Design Systems</a>
      <a href="#scale">Frontend Scalability</a>
      <a href="#mfe">Micro-frontends</a>
    </div>
    <div class="nav-group">
      <h2>React runtime</h2>
      <a href="#internals">React Internals</a>
      <a href="#reconciliation">Reconciliation</a>
      <a href="#performance">React Performance</a>
      <a href="#perf-debug">Perf Debugging</a>
    </div>
    <div class="nav-group">
      <h2>Platform</h2>
      <a href="#browser">Browser Architecture</a>
      <a href="#webperf">Web Performance</a>
      <a href="#network">Networking &amp; Caching</a>
      <a href="#offline">Offline / Resilience</a>
      <a href="#security">Security</a>
      <a href="#a11y">Accessibility</a>
      <a href="#testing">Testing</a>
      <a href="#observability">Observability</a>
    </div>
    <div class="nav-group">
      <h2>Practice</h2>
      <a href="#cases">Case Studies</a>
      <a href="#sysdesign">System Design Bank</a>
      <a href="#feq">Interview Questions</a>
      <a href="#exercises">Coding Exercises</a>
      <a href="#adrs">ADRs</a>
      <a href="#comms">Communication</a>
      <a href="#mock">Mock Interview</a>
      <a href="#debug-sim">Debug Simulator</a>
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
      <div class="overall-label"><span>Phase 2 completion</span><strong id="overall-pct">0%</strong></div>
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
