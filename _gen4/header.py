def html_head(css: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Atlassian Senior SWE — Phase 4 Interview Mastery</title>
  <meta name="description" content="Self-contained Phase 4 prep: interview execution, behavioral stories, values, mocks, and offer conversations." />
  <style>
{css}
  </style>
</head>
<body>
<div class="sidebar-backdrop" id="sidebar-backdrop"></div>
<aside class="sidebar" id="sidebar">
  <div class="brand">
    <div class="brand-mark">4</div>
    <div>
      <h1>Phase 4 Prep</h1>
      <p>Atlassian · Senior SWE</p>
    </div>
    <button type="button" class="icon-btn sidebar-hide" id="sidebar-hide" title="Hide sidebar" aria-label="Hide sidebar">«</button>
  </div>
  <div class="search-wrap">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3-3"/></svg>
    <input id="global-search" type="search" placeholder="Search stories, values, mocks..." autocomplete="off" />
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
      <a href="#process">Interview Process</a>
      <a href="#plan">14-Day Plan</a>
    </div>
    <div class="nav-group">
      <h2>Positioning</h2>
      <a href="#positioning">Personal Positioning</a>
      <a href="#tmay">Tell Me About Yourself</a>
      <a href="#why">Why Atlassian</a>
      <a href="#resume">Resume Deep Dive</a>
    </div>
    <div class="nav-group">
      <h2>Behavioral</h2>
      <a href="#framework">Behavioral Framework</a>
      <a href="#stories">Story Bank</a>
      <a href="#matrix">Story Reuse Matrix</a>
      <a href="#bq">Question Bank</a>
      <a href="#senior">Senior Behavior</a>
      <a href="#values">Values</a>
      <a href="#hm">Hiring Manager</a>
    </div>
    <div class="nav-group">
      <h2>Mocks</h2>
      <a href="#coding">Coding Mock</a>
      <a href="#craft">Frontend Craft</a>
      <a href="#sdmock">System Design Mock</a>
      <a href="#interrogation">Project Interrogation</a>
      <a href="#loop">Full Loop</a>
    </div>
    <div class="nav-group">
      <h2>Execution</h2>
      <a href="#comms">Communication</a>
      <a href="#unknown">I Don't Know</a>
      <a href="#ask">Questions to Ask</a>
      <a href="#recruiter">Recruiter</a>
      <a href="#offer">Compensation</a>
      <a href="#day">Interview Day</a>
      <a href="#techcheck">Tech Checklist</a>
      <a href="#rejection">Rejection Analysis</a>
    </div>
    <div class="nav-group">
      <h2>Track</h2>
      <a href="#progress">Progress</a>
      <a href="#readiness">Readiness</a>
      <a href="#resources">Resources</a>
    </div>
  </nav>
</aside>
<div class="main">
  <header class="topbar">
    <button class="menu-btn" id="menu-btn" type="button" aria-label="Toggle sidebar">☰</button>
    <a class="hub-link" href="index.html">All prep</a>
    <div class="overall-wrap">
      <div class="overall-label"><span>Interview readiness</span><strong id="overall-pct">0%</strong></div>
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
