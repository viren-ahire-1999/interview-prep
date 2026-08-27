(function () {
  "use strict";

  const KEY = "atl-phase1-v1";
  const defaultState = () => ({
    theme: "dark",
    navCollapsed: false,
    checks: {},
    topics: {},
    jsTopics: {},
    questions: {},
    problems: {},
    mocks: [],
    reviews: {},
    readiness: {}
  });

  function load() {
    try {
      const raw = localStorage.getItem(KEY);
      if (!raw) return defaultState();
      return Object.assign(defaultState(), JSON.parse(raw));
    } catch {
      return defaultState();
    }
  }

  function save(state) {
    localStorage.setItem(KEY, JSON.stringify(state));
  }

  let state = load();

  function applyTheme() {
    document.documentElement.setAttribute("data-theme", state.theme || "dark");
  }

  function $(sel, root) {
    return (root || document).querySelector(sel);
  }
  function $$(sel, root) {
    return Array.from((root || document).querySelectorAll(sel));
  }

  /* ---------- theme ---------- */
  applyTheme();
  const themeBtn = $("#theme-toggle");
  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      state.theme = state.theme === "dark" ? "light" : "dark";
      save(state);
      applyTheme();
    });
  }

  /* ---------- mobile nav ---------- */
  const sidebar = $(".sidebar");
  const backdrop = $(".sidebar-backdrop");
  const menuBtn = $("#menu-btn");
  function isMobileNav() { return window.matchMedia("(max-width: 800px)").matches; }
  function applyNavCollapsed() {
    document.body.classList.toggle("nav-collapsed", !!state.navCollapsed);
    if (menuBtn) {
      menuBtn.setAttribute("aria-label", isMobileNav()
        ? "Open menu"
        : (state.navCollapsed ? "Show sidebar" : "Hide sidebar"));
    }
  }
  function closeNav() {
    sidebar && sidebar.classList.remove("open");
    backdrop && backdrop.classList.remove("open");
  }
  function toggleNav() {
    if (isMobileNav()) {
      sidebar.classList.toggle("open");
      backdrop.classList.toggle("open");
      return;
    }
    state.navCollapsed = !state.navCollapsed;
    save(state);
    applyNavCollapsed();
  }
  applyNavCollapsed();
  menuBtn && menuBtn.addEventListener("click", toggleNav);
  const hideBtn = $("#sidebar-hide");
  hideBtn && hideBtn.addEventListener("click", toggleNav);
  backdrop && backdrop.addEventListener("click", closeNav);
  $$(".sidebar a").forEach((a) => a.addEventListener("click", closeNav));

  /* ---------- copy buttons ---------- */
  bindCopy(document);

  /* ---------- collapsibles ---------- */
  $$(".day-head").forEach((btn) => {
    btn.addEventListener("click", () => btn.parentElement.classList.toggle("open"));
  });
  function findToggleTarget(btn) {
    const id = btn.getAttribute("data-toggle");
    if (!id) return null;
    const root = btn.closest("#mock-panel") || btn.closest(".problem, .q, .ex, .elq, .topic, .pattern") || document;
    return root.querySelector("#" + CSS.escape(id)) || document.getElementById(id);
  }
  function bindToggles(scope) {
    $$("[data-toggle]", scope).forEach((btn) => {
      if (btn.dataset.boundToggle) return;
      btn.dataset.boundToggle = "1";
      btn.addEventListener("click", () => {
        const el = findToggleTarget(btn);
        if (el) el.classList.toggle("open");
      });
    });
  }
  bindToggles(document);

  function bindCopy(scope) {
    $$(".code-block", scope).forEach((block) => {
      const btn = block.querySelector(".copy-btn");
      const code = block.querySelector("pre");
      if (!btn || !code || btn.dataset.boundCopy) return;
      btn.dataset.boundCopy = "1";
      btn.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(code.textContent || "");
          btn.textContent = "Copied";
          setTimeout(() => { btn.textContent = "Copy"; }, 1200);
        } catch {
          const ta = document.createElement("textarea");
          ta.value = code.textContent || "";
          document.body.appendChild(ta);
          ta.select();
          document.execCommand("copy");
          ta.remove();
          btn.textContent = "Copied";
          setTimeout(() => { btn.textContent = "Copy"; }, 1200);
        }
      });
    });
  }

  /* ---------- persist checkboxes ---------- */
  $$("input[type=checkbox][data-id]").forEach((box) => {
    const id = box.getAttribute("data-id");
    const group = box.getAttribute("data-group") || "checks";
    if (!state[group]) state[group] = {};
    box.checked = !!state[group][id];
    box.addEventListener("change", () => {
      state[group][id] = box.checked;
      if (box.checked && group === "problems") {
        /* ignore */
      }
      save(state);
      updateProgress();
      updateRevision();
    });
  });

  /* ---------- topic / question complete buttons ---------- */
  $$("[data-complete]").forEach((btn) => {
    const group = btn.getAttribute("data-complete");
    const id = btn.getAttribute("data-cid");
    if (state[group] && state[group][id]) btn.classList.add("done");
    btn.addEventListener("click", () => {
      if (!state[group]) state[group] = {};
      state[group][id] = !state[group][id];
      btn.classList.toggle("done", !!state[group][id]);
      btn.textContent = state[group][id] ? "Completed" : "Mark complete";
      save(state);
      updateProgress();
    });
    if (state[group] && state[group][id]) btn.textContent = "Completed";
  });

  /* ---------- problem status ---------- */
  const INTERVALS = [1, 3, 7, 14, 30];

  function setProblemStatus(id, status) {
    const now = Date.now();
    const prev = state.problems[id] || { status: "not-started", interval: 0, fails: 0 };
    const next = Object.assign({}, prev, { status, updated: now });
    if (status === "solved" || status === "mastered") {
      if (status === "mastered") {
        next.nextReview = now + 30 * 86400000;
        next.interval = 4;
      } else {
        const step = Math.min(prev.interval || 0, INTERVALS.length - 1);
        next.nextReview = now + INTERVALS[step] * 86400000;
        next.interval = Math.min(step + 1, INTERVALS.length - 1);
      }
    } else if (status === "review" || status === "attempted") {
      next.nextReview = now + 86400000;
      next.fails = (prev.fails || 0) + (status === "review" ? 0 : 1);
      if (status === "attempted") next.interval = 0;
    }
    state.problems[id] = next;
    save(state);
    paintProblem(id);
    updateProgress();
    updateRevision();
  }

  function paintProblem(id) {
    const card = document.querySelector('.problem[data-pid="' + id + '"]');
    if (!card) return;
    const st = (state.problems[id] && state.problems[id].status) || "not-started";
    card.setAttribute("data-status", st);
    $$(".status-btns button", card).forEach((b) => {
      b.className = b.className.replace(/active-\S+/g, "").trim();
      if (b.getAttribute("data-status") === st) b.classList.add("active-" + st);
    });
  }

  $$(".problem[data-pid]").forEach((card) => {
    const id = card.getAttribute("data-pid");
    $$(".status-btns button", card).forEach((b) => {
      b.addEventListener("click", () => setProblemStatus(id, b.getAttribute("data-status")));
    });
    paintProblem(id);
  });

  /* ---------- filters ---------- */
  const filterStatus = $("#filter-status");
  const filterDiff = $("#filter-diff");
  const filterTopic = $("#filter-topic");
  const filterPattern = $("#filter-pattern");
  const filterText = $("#filter-text");

  function applyFilters() {
    const st = filterStatus ? filterStatus.value : "all";
    const df = filterDiff ? filterDiff.value : "all";
    const tp = filterTopic ? filterTopic.value : "all";
    const pn = filterPattern ? filterPattern.value : "all";
    const q = (filterText ? filterText.value : "").toLowerCase();
    $$(".problem[data-pid]").forEach((card) => {
      const id = card.getAttribute("data-pid");
      const status = (state.problems[id] && state.problems[id].status) || "not-started";
      const okS = st === "all" || status === st;
      const okD = df === "all" || card.getAttribute("data-difficulty") === df;
      const okT = tp === "all" || card.getAttribute("data-topic") === tp;
      const okP = pn === "all" || card.getAttribute("data-pattern") === pn;
      const text = (card.getAttribute("data-name") + " " + card.textContent).toLowerCase();
      const okQ = !q || text.includes(q);
      card.classList.toggle("hidden", !(okS && okD && okT && okP && okQ));
    });
  }
  [filterStatus, filterDiff, filterTopic, filterPattern, filterText].forEach((el) => {
    if (el) el.addEventListener("input", applyFilters);
  });

  /* ---------- search ---------- */
  const searchInput = $("#global-search");
  const searchBox = $("#search-results");
  const searchIndex = $$("[data-search]").map((el) => ({
    title: el.getAttribute("data-search"),
    type: el.getAttribute("data-stype") || "Section",
    href: "#" + (el.id || (el.closest("section") && el.closest("section").id) || "")
  }));

  function runSearch(q) {
    if (!searchBox) return;
    const query = q.trim().toLowerCase();
    if (!query) {
      searchBox.classList.remove("open");
      searchBox.innerHTML = "";
      return;
    }
    const hits = searchIndex.filter((x) => x.title.toLowerCase().includes(query)).slice(0, 20);
    searchBox.innerHTML = hits.length
      ? hits.map((h) => '<a href="' + h.href + '">' + escapeHtml(h.title) + "<small>" + escapeHtml(h.type) + "</small></a>").join("")
      : '<a href="#dashboard">No matches</a>';
    searchBox.classList.add("open");
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }
  searchInput && searchInput.addEventListener("input", () => runSearch(searchInput.value));
  searchInput && searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      searchBox.classList.remove("open");
      searchInput.blur();
    }
  });
  document.addEventListener("click", (e) => {
    if (searchBox && !searchBox.contains(e.target) && e.target !== searchInput) {
      searchBox.classList.remove("open");
    }
  });

  /* ---------- progress ---------- */
  function countTrue(obj) {
    return Object.values(obj || {}).filter(Boolean).length;
  }
  function problemCount(status) {
    return Object.values(state.problems).filter((p) => p.status === status).length;
  }
  function totalProblems() {
    return $$(".problem[data-pid]").length;
  }
  function totalDayTasks() {
    return $$('input[type=checkbox][data-group="checks"]').length;
  }
  function totalReadiness() {
    return $$('input[type=checkbox][data-group="readiness"]').length;
  }

  function updateProgress() {
    const dayDone = countTrue(state.checks);
    const dayTotal = totalDayTasks() || 1;
    const probSolved = problemCount("solved") + problemCount("mastered");
    const probTotal = totalProblems() || 1;
    const reviewN = problemCount("review") + $$(".problem[data-pid]").filter((c) => {
      const id = c.getAttribute("data-pid");
      const p = state.problems[id];
      return p && p.nextReview && p.nextReview <= Date.now() && p.status !== "mastered" && p.status !== "not-started";
    }).length;
    const jsDone = countTrue(state.jsTopics) + countTrue(state.questions);
    const jsTotal = $$("[data-complete=jsTopics]").length + $$("[data-complete=questions]").length || 1;
    const dsaDone = countTrue(state.topics);
    const dsaTotal = $$("[data-complete=topics]").length || 1;
    const mocks = (state.mocks || []).length;
    const readyDone = countTrue(state.readiness);
    const readyTotal = totalReadiness() || 1;

    const overall = Math.round(
      (
        (dayDone / dayTotal) * 0.2 +
        (probSolved / probTotal) * 0.3 +
        (dsaDone / dsaTotal) * 0.15 +
        (jsDone / jsTotal) * 0.2 +
        Math.min(mocks / 6, 1) * 0.05 +
        (readyDone / readyTotal) * 0.1
      ) * 100
    );

    setText("#overall-pct", overall + "%");
    setWidth("#overall-bar", overall + "%");
    setText("#stat-dsa", Math.round((dsaDone / dsaTotal) * 100) + "%");
    setWidth("#bar-dsa", Math.round((dsaDone / dsaTotal) * 100) + "%");
    setText("#stat-js", Math.round((jsDone / jsTotal) * 100) + "%");
    setWidth("#bar-js", Math.round((jsDone / jsTotal) * 100) + "%");
    setText("#stat-problems", probSolved + " / " + probTotal);
    setWidth("#bar-problems", Math.round((probSolved / probTotal) * 100) + "%");
    setText("#stat-review", String(reviewN));
    setText("#stat-mocks", String(mocks));
    setText("#stat-ready", Math.round((readyDone / readyTotal) * 100) + "%");
    setWidth("#bar-ready", Math.round((readyDone / readyTotal) * 100) + "%");
    setText("#track-days", dayDone + " / " + dayTotal + " daily tasks");
    setWidth("#bar-days", Math.round((dayDone / dayTotal) * 100) + "%");
    setText("#track-topics", dsaDone + " / " + dsaTotal + " DSA topics");
    setText("#track-js", countTrue(state.jsTopics) + " / " + ($$("[data-complete=jsTopics]").length || 0) + " JS topics");
    setText("#track-qs", countTrue(state.questions) + " / " + ($$("[data-complete=questions]").length || 0) + " JS questions");
    setText("#ready-score", Math.round((readyDone / readyTotal) * 100) + "%");
    setWidth("#bar-ready-final", Math.round((readyDone / readyTotal) * 100) + "%");
    const gate = $("#ready-gate");
    if (gate) {
      gate.textContent = readyDone / readyTotal >= 0.85
        ? "You look ready to start Phase 2. Keep a light revision loop."
        : "Stay in Phase 1 until this checklist is honestly above ~85%.";
    }
  }

  function setText(sel, val) {
    const el = $(sel);
    if (el) el.textContent = val;
  }
  function setWidth(sel, val) {
    const el = $(sel);
    if (el) el.style.width = val;
  }

  /* ---------- revision dashboard ---------- */
  function updateRevision() {
    const now = Date.now();
    const week = now + 7 * 86400000;
    const dueToday = [];
    const dueWeek = [];
    const failed = [];
    const mastered = [];
    const patternFails = {};
    $$(".problem[data-pid]").forEach((card) => {
      const id = card.getAttribute("data-pid");
      const name = card.getAttribute("data-name");
      const pattern = card.getAttribute("data-pattern");
      const p = state.problems[id];
      if (!p) return;
      if (p.status === "mastered") mastered.push(name);
      if (p.status === "attempted" || (p.fails || 0) > 0) {
        failed.push(name);
        patternFails[pattern] = (patternFails[pattern] || 0) + (p.fails || 1);
      }
      if (p.nextReview && p.status !== "not-started" && p.status !== "mastered") {
        if (p.nextReview <= now) dueToday.push(name);
        else if (p.nextReview <= week) dueWeek.push(name);
      }
    });
    fillList("#rev-today", dueToday);
    fillList("#rev-week", dueWeek);
    fillList("#rev-failed", failed.slice(0, 12));
    fillList("#rev-mastered", mastered);
    const weak = Object.entries(patternFails).sort((a, b) => b[1] - a[1]).slice(0, 6);
    fillList("#rev-patterns", weak.map(([k, n]) => k + " (" + n + " misses)"));
    const topicMiss = {};
    $$(".problem[data-pid]").forEach((card) => {
      const id = card.getAttribute("data-pid");
      const p = state.problems[id];
      if (p && (p.status === "attempted" || p.status === "review")) {
        const t = card.getAttribute("data-topic");
        topicMiss[t] = (topicMiss[t] || 0) + 1;
      }
    });
    fillList("#rev-topics", Object.entries(topicMiss).sort((a, b) => b[1] - a[1]).map(([k, n]) => k + " (" + n + ")"));
  }
  function fillList(sel, items) {
    const el = $(sel);
    if (!el) return;
    el.innerHTML = items.length ? items.map((x) => "<li>" + escapeHtml(x) + "</li>").join("") : "<li>None yet</li>";
  }

  /* ---------- mock interview ---------- */
  let mockTimer = null;
  let mockLeft = 0;
  let currentMock = null;

  function allProblems() {
    return $$(".problem[data-pid]").map((card) => ({
      id: card.getAttribute("data-pid"),
      name: card.getAttribute("data-name"),
      difficulty: card.getAttribute("data-difficulty"),
      pattern: card.getAttribute("data-pattern"),
      html: card.querySelector(".problem-body") ? card.querySelector(".problem-body").innerHTML : card.innerHTML
    }));
  }

  function suggestedTime(diff) {
    if (diff === "easy") return 15 * 60;
    if (diff === "hard") return 40 * 60;
    return 30 * 60;
  }

  function fmt(sec) {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
  }

  function renderMock(p) {
    currentMock = p;
    mockLeft = suggestedTime(p.difficulty);
    const panel = $("#mock-panel");
    panel.innerHTML =
      '<div class="meta-row">' +
      '<span class="badge badge-' + p.difficulty + '">' + p.difficulty.toUpperCase() + "</span>" +
      '<span class="badge badge-pattern">' + escapeHtml(p.pattern) + "</span>" +
      "<span class=\"chip\">Suggested " + (mockLeft / 60) + " min</span></div>" +
      "<h3>" + escapeHtml(p.name) + "</h3>" +
      '<div class="timer" id="mock-timer">' + fmt(mockLeft) + "</div>" +
      '<div class="status-btns">' +
      '<button type="button" id="mock-start-timer">Start timer</button>' +
      '<button type="button" id="mock-pause">Pause</button>' +
      '<button type="button" data-toggle="mock-hint-box" class="toggle-btn">Reveal hint</button>' +
      '<button type="button" data-toggle="mock-sol-box" class="toggle-btn">Reveal solution</button>' +
      "</div>" +
      '<div class="problem-body">' + p.html + "</div>";
    bindMockControls();
    bindToggles(panel);
    bindCopy(panel);
  }

  function bindMockControls() {
    const start = $("#mock-start-timer");
    const pause = $("#mock-pause");
    start && start.addEventListener("click", startTimer);
    pause && pause.addEventListener("click", stopTimer);
  }

  function tick() {
    mockLeft = Math.max(0, mockLeft - 1);
    const el = $("#mock-timer");
    if (el) el.textContent = fmt(mockLeft);
    if (mockLeft === 0) stopTimer();
  }
  function startTimer() {
    stopTimer();
    mockTimer = setInterval(tick, 1000);
  }
  function stopTimer() {
    if (mockTimer) clearInterval(mockTimer);
    mockTimer = null;
  }

  const startMock = $("#start-mock");
  startMock && startMock.addEventListener("click", () => {
    const list = allProblems();
    if (!list.length) return;
    const p = list[Math.floor(Math.random() * list.length)];
    renderMock(p);
  });

  const saveMock = $("#save-mock");
  saveMock && saveMock.addEventListener("click", () => {
    if (!currentMock) {
      alert("Start a mock interview first.");
      return;
    }
    const rec = {
      id: currentMock.id,
      name: currentMock.name,
      date: new Date().toISOString(),
      pattern: $("#mock-q-pattern") && $("#mock-q-pattern").checked,
      onTime: $("#mock-q-time") && $("#mock-q-time").checked,
      complexity: $("#mock-q-complex") && $("#mock-q-complex").checked,
      edges: $("#mock-q-edges") && $("#mock-q-edges").checked,
      confidence: ($("#mock-confidence") && $("#mock-confidence").value) || "3"
    };
    state.mocks.push(rec);
    save(state);
    renderMockHistory();
    updateProgress();
    alert("Mock saved locally.");
  });

  function renderMockHistory() {
    const el = $("#mock-history");
    if (!el) return;
    if (!state.mocks.length) {
      el.innerHTML = "<p class='stat-sub'>No mocks yet. Do at least 4–6 before leaving Phase 1.</p>";
      return;
    }
    el.innerHTML = "<ul class='tight'>" + state.mocks.slice().reverse().map((m) => {
      return "<li>" + escapeHtml(m.date.slice(0, 10)) + " — <b>" + escapeHtml(m.name) + "</b> · confidence " +
        escapeHtml(m.confidence) + "/5 · pattern " + (m.pattern ? "yes" : "no") + "</li>";
    }).join("") + "</ul>";
  }

  /* ---------- reset ---------- */
  const resetBtn = $("#reset-progress");
  resetBtn && resetBtn.addEventListener("click", () => {
    if (!confirm("Reset all Phase 1 progress on this browser? This cannot be undone.")) return;
    const theme = state.theme;
    state = defaultState();
    state.theme = theme;
    save(state);
    location.reload();
  });

  /* ---------- tabs ---------- */
  $$(".tabs").forEach((wrap) => {
    const group = wrap.getAttribute("data-tabs");
    $$(".tab", wrap).forEach((tab) => {
      tab.addEventListener("click", () => {
        $$(".tab", wrap).forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");
        const which = tab.getAttribute("data-tab");
        if (group === "jsq") {
          $$(".q[data-level]").forEach((card) => {
            card.classList.toggle("hidden", which !== "all" && card.getAttribute("data-level") !== which);
          });
          return;
        }
        $$("[data-tabpanel='" + group + "']").forEach((p) => {
          p.classList.toggle("hidden", p.getAttribute("data-tab") !== which);
        });
      });
    });
  });

  /* ---------- active nav ---------- */
  const navLinks = $$(".sidebar a[href^='#']");
  const sections = navLinks.map((a) => document.querySelector(a.getAttribute("href"))).filter(Boolean);
  function onScroll() {
    let current = sections[0];
    sections.forEach((s) => {
      if (s.getBoundingClientRect().top <= 90) current = s;
    });
    navLinks.forEach((a) => a.classList.toggle("active", current && a.getAttribute("href") === "#" + current.id));
  }
  document.addEventListener("scroll", onScroll, { passive: true });

  $("#back-top") && $("#back-top").addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

  /* ---------- readiness checkboxes already handled via data-group ---------- */

  updateProgress();
  updateRevision();
  renderMockHistory();
  applyFilters();
})();
