(function () {
  "use strict";

  const KEY = "atl-phase3-v1";
  const defaultState = () => ({
    theme: "dark",
    navCollapsed: false,
    checks: {},
    topics: {},
    distTopics: {},
    backendTopics: {},
    questions: {},
    designs: {},
    cases: {},
    exercises: {},
    mocks: [],
    reviews: {},
    readiness: {},
    items: {}
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

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

  function applyTheme() {
    document.documentElement.setAttribute("data-theme", state.theme || "dark");
  }
  applyTheme();
  const themeBtn = $("#theme-toggle");
  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      state.theme = state.theme === "dark" ? "light" : "dark";
      save(state);
      applyTheme();
    });
  }

  const sidebar = $("#sidebar");
  const backdrop = $("#sidebar-backdrop");
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

  function findToggleTarget(btn) {
    const id = btn.getAttribute("data-toggle");
    if (!id) return null;
    const root = btn.closest("#mock-panel") || btn.closest(".problem, .q, .ex, .topic, .pattern, .elq") || document;
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
  bindCopy(document);
  $$(".day-head").forEach((btn) => {
    btn.addEventListener("click", () => btn.parentElement.classList.toggle("open"));
  });
  bindToggles(document);

  $$("input[type=checkbox][data-id]").forEach((box) => {
    const id = box.getAttribute("data-id");
    const group = box.getAttribute("data-group") || "checks";
    if (!state[group]) state[group] = {};
    box.checked = !!state[group][id];
    box.addEventListener("change", () => {
      state[group][id] = box.checked;
      save(state);
      updateProgress();
      updateRevision();
    });
  });

  $$("[data-complete]").forEach((btn) => {
    const group = btn.getAttribute("data-complete");
    const id = btn.getAttribute("data-cid");
    if (!state[group]) state[group] = {};
    if (state[group][id]) {
      btn.classList.add("done");
      btn.textContent = "Completed";
    }
    btn.addEventListener("click", () => {
      if (!state[group]) state[group] = {};
      state[group][id] = !state[group][id];
      btn.classList.toggle("done", !!state[group][id]);
      btn.textContent = state[group][id] ? "Completed" : "Mark complete";
      if (state[group][id]) scheduleReview(id, true);
      save(state);
      updateProgress();
      updateRevision();
    });
  });

  const INTERVALS = [1, 3, 7, 14, 30];
  function scheduleReview(id, ok) {
    const now = Date.now();
    const prev = state.items[id] || { interval: 0, fails: 0, status: "not-started" };
    const next = Object.assign({}, prev, { updated: now });
    if (ok) {
      const step = Math.min(prev.interval || 0, INTERVALS.length - 1);
      next.nextReview = now + INTERVALS[step] * 86400000;
      next.interval = Math.min(step + 1, INTERVALS.length - 1);
      next.status = next.interval >= 4 ? "mastered" : "solved";
    } else {
      next.nextReview = now + 86400000;
      next.interval = 0;
      next.fails = (prev.fails || 0) + 1;
      next.status = "review";
    }
    state.items[id] = next;
  }

  function setItemStatus(id, status) {
    const now = Date.now();
    const prev = state.items[id] || { interval: 0, fails: 0 };
    const next = Object.assign({}, prev, { status, updated: now });
    if (status === "mastered") {
      next.nextReview = now + 30 * 86400000;
      next.interval = 4;
    } else if (status === "solved") {
      scheduleReview(id, true);
      return;
    } else if (status === "attempted" || status === "review") {
      next.nextReview = now + 86400000;
      if (status === "attempted") next.fails = (prev.fails || 0) + 1;
    }
    state.items[id] = next;
    save(state);
    paintItem(id);
    updateProgress();
    updateRevision();
  }
  function paintItem(id) {
    const card = document.querySelector('[data-pid="' + id + '"]');
    if (!card) return;
    const st = (state.items[id] && state.items[id].status) || "not-started";
    card.setAttribute("data-status", st);
    $$(".status-btns button", card).forEach((b) => {
      b.className = b.className.replace(/active-\S+/g, "").trim();
      if (b.getAttribute("data-status") === st) b.classList.add("active-" + st);
    });
  }
  $$("[data-pid]").forEach((card) => {
    const id = card.getAttribute("data-pid");
    $$(".status-btns button", card).forEach((b) => {
      b.addEventListener("click", () => setItemStatus(id, b.getAttribute("data-status")));
    });
    paintItem(id);
  });

  function applyCardFilters() {
    const st = ($("#filter-status") && $("#filter-status").value) || "all";
    const cat = ($("#filter-cat") && $("#filter-cat").value) || "all";
    const q = (($("#filter-text") && $("#filter-text").value) || "").toLowerCase();
    $$("[data-filterable]").forEach((card) => {
      const id = card.getAttribute("data-pid") || card.id;
      const status = (state.items[id] && state.items[id].status) || (state.questions[id] ? "solved" : "not-started");
      const okS = st === "all" || (st === "complete" && (status === "solved" || status === "mastered")) ||
        (st === "incomplete" && status !== "solved" && status !== "mastered") ||
        (st === "weak" && status === "attempted") ||
        (st === "review" && status === "review") || status === st;
      const okC = cat === "all" || card.getAttribute("data-cat") === cat || card.getAttribute("data-level") === cat;
      const text = ((card.getAttribute("data-search") || "") + " " + card.textContent).toLowerCase();
      card.classList.toggle("hidden", !(okS && okC && (!q || text.includes(q))));
    });
  }
  ["filter-status", "filter-cat", "filter-text"].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener("input", applyCardFilters);
  });

  const searchInput = $("#global-search");
  const searchBox = $("#search-results");
  const searchIndex = $$("[data-search]").map((el) => ({
    title: el.getAttribute("data-search"),
    type: el.getAttribute("data-stype") || "Section",
    href: "#" + (el.id || (el.closest("section") && el.closest("section").id) || ""),
    excerpt: (el.textContent || "").replace(/\s+/g, " ").trim().slice(0, 120)
  }));
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }
  function runSearch(q) {
    if (!searchBox) return;
    const query = q.trim().toLowerCase();
    if (!query) { searchBox.classList.remove("open"); searchBox.innerHTML = ""; return; }
    const hits = searchIndex.filter((x) =>
      x.title.toLowerCase().includes(query) || (x.excerpt && x.excerpt.toLowerCase().includes(query))
    ).slice(0, 20);
    searchBox.innerHTML = hits.length
      ? hits.map((h) => '<a href="' + h.href + '">' + escapeHtml(h.title) + "<small>" + escapeHtml(h.type) + " · " + escapeHtml(h.excerpt) + "</small></a>").join("")
      : '<a href="#dashboard">No matches</a>';
    searchBox.classList.add("open");
  }
  searchInput && searchInput.addEventListener("input", () => runSearch(searchInput.value));
  searchInput && searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { searchBox.classList.remove("open"); searchInput.blur(); }
  });
  document.addEventListener("click", (e) => {
    if (searchBox && !searchBox.contains(e.target) && e.target !== searchInput) searchBox.classList.remove("open");
  });

  function countTrue(obj) { return Object.values(obj || {}).filter(Boolean).length; }
  function setText(sel, val) { const el = $(sel); if (el) el.textContent = val; }
  function setWidth(sel, val) { const el = $(sel); if (el) el.style.width = val; }
  function pct(n, d) { return Math.round((n / (d || 1)) * 100); }

  function updateProgress() {
    const dayDone = countTrue(state.checks);
    const dayTotal = $$('input[type=checkbox][data-group="checks"]').length || 1;
    const sdDone = countTrue(state.topics);
    const sdTotal = $$("[data-complete=topics]").length || 1;
    const distDone = countTrue(state.distTopics);
    const distTotal = $$("[data-complete=distTopics]").length || 1;
    const beDone = countTrue(state.backendTopics);
    const beTotal = $$("[data-complete=backendTopics]").length || 1;
    const qsDone = countTrue(state.questions);
    const qsTotal = $$("[data-complete=questions]").length || 1;
    const designDone = countTrue(state.designs);
    const designTotal = $$("[data-complete=designs]").length || 1;
    const caseDone = countTrue(state.cases);
    const caseTotal = $$("[data-complete=cases]").length || 1;
    const exDone = countTrue(state.exercises);
    const exTotal = $$("[data-complete=exercises]").length || 1;
    const readyDone = countTrue(state.readiness);
    const readyTotal = $$('input[type=checkbox][data-group="readiness"]').length || 1;
    const mocks = (state.mocks || []).length;
    const now = Date.now();
    const reviewN = Object.values(state.items).filter((p) => p.nextReview && p.nextReview <= now && p.status !== "mastered").length;

    const overall = Math.round((
      (dayDone / dayTotal) * 0.16 +
      (sdDone / sdTotal) * 0.14 +
      (distDone / distTotal) * 0.14 +
      (beDone / (beTotal || 1)) * 0.10 +
      (caseDone / (caseTotal || 1)) * 0.12 +
      (designDone / (designTotal || 1)) * 0.10 +
      (qsDone / qsTotal) * 0.08 +
      (exDone / (exTotal || 1)) * 0.06 +
      Math.min(mocks / 8, 1) * 0.06 +
      (readyDone / readyTotal) * 0.04
    ) * 100);

    setText("#overall-pct", overall + "%");
    setWidth("#overall-bar", overall + "%");
    setText("#stat-days", pct(dayDone, dayTotal) + "%");
    setWidth("#bar-days", pct(dayDone, dayTotal) + "%");
    setText("#stat-sd", pct(sdDone, sdTotal) + "%");
    setWidth("#bar-sd", pct(sdDone, sdTotal) + "%");
    setText("#stat-dist", pct(distDone, distTotal) + "%");
    setWidth("#bar-dist", pct(distDone, distTotal) + "%");
    setText("#stat-backend", pct(beDone, beTotal) + "%");
    setWidth("#bar-backend", pct(beDone, beTotal) + "%");
    setText("#stat-cases", caseDone + " / " + caseTotal);
    setWidth("#bar-cases", pct(caseDone, caseTotal) + "%");
    setText("#stat-qs", qsDone + " / " + qsTotal);
    setWidth("#bar-qs", pct(qsDone, qsTotal) + "%");
    setText("#stat-mocks", String(mocks));
    setText("#stat-ready", pct(readyDone, readyTotal) + "%");
    setWidth("#bar-ready", pct(readyDone, readyTotal) + "%");
    setText("#stat-review", String(reviewN));
    setText("#stat-ex", (exDone + designDone) + " / " + (exTotal + designTotal));
    setWidth("#bar-ex", pct(exDone + designDone, exTotal + designTotal) + "%");
    setText("#track-days", dayDone + " / " + dayTotal + " daily tasks");
    setText("#track-sd", sdDone + " / " + sdTotal);
    setText("#track-dist", distDone + " / " + distTotal);
    setText("#track-backend", beDone + " / " + beTotal);
    setText("#track-qs", qsDone + " / " + qsTotal);
    setText("#track-designs", designDone + " / " + designTotal);
    setText("#track-cases", caseDone + " / " + caseTotal);
    setText("#track-ex", exDone + " / " + exTotal);
    setText("#track-mocks", String(mocks));
    setText("#ready-score", pct(readyDone, readyTotal) + "%");
    setWidth("#bar-ready-final", pct(readyDone, readyTotal) + "%");
    const cats = [
      ["#bar-cat-sd", sdDone, sdTotal],
      ["#bar-cat-dist", distDone, distTotal],
      ["#bar-cat-db", $$("[data-cat=database] [data-complete].done").length, $$("[data-cat=database] [data-complete]").length],
      ["#bar-cat-cache", $$("[data-cat=caching] [data-complete].done").length, $$("[data-cat=caching] [data-complete]").length],
      ["#bar-cat-msg", $$("[data-cat=messaging] [data-complete].done").length, $$("[data-cat=messaging] [data-complete]").length],
      ["#bar-cat-rel", $$("[data-cat=reliability] [data-complete].done").length, $$("[data-cat=reliability] [data-complete]").length]
    ];
    cats.forEach(([sel, n, d]) => setWidth(sel, pct(n, d || 1) + "%"));
    const gate = $("#ready-gate");
    if (gate) {
      gate.textContent = readyDone / readyTotal >= 0.85
        ? "You look ready to leave Phase 3. Keep a light revision loop and company-specific research."
        : "Stay in Phase 3 until this checklist is honestly above ~85%.";
    }
  }

  function updateRevision() {
    const now = Date.now();
    const week = now + 7 * 86400000;
    const dueToday = [], dueWeek = [], failed = [], mastered = [], weak = {};
    Object.entries(state.items).forEach(([id, p]) => {
      const el = document.querySelector('[data-pid="' + id + '"], #' + CSS.escape(id));
      const name = (el && (el.getAttribute("data-search") || el.querySelector("h3") && el.querySelector("h3").textContent)) || id;
      if (p.status === "mastered") mastered.push(name);
      if (p.status === "attempted" || (p.fails || 0) > 0) {
        failed.push(name);
        const cat = el && el.getAttribute("data-cat");
        if (cat) weak[cat] = (weak[cat] || 0) + 1;
      }
      if (p.nextReview && p.status !== "mastered") {
        if (p.nextReview <= now) dueToday.push(name);
        else if (p.nextReview <= week) dueWeek.push(name);
      }
    });
    fillList("#rev-today", dueToday);
    fillList("#rev-week", dueWeek);
    fillList("#rev-failed", failed.slice(0, 12));
    fillList("#rev-mastered", mastered);
    fillList("#rev-weak", Object.entries(weak).sort((a, b) => b[1] - a[1]).map(([k, n]) => k + " (" + n + ")"));
  }
  function fillList(sel, items) {
    const el = $(sel);
    if (!el) return;
    el.innerHTML = items.length ? items.map((x) => "<li>" + escapeHtml(x) + "</li>").join("") : "<li>None yet</li>";
  }

  let mockTimer = null, mockLeft = 0, currentMock = null;
  function fmt(sec) {
    const m = Math.floor(sec / 60), s = sec % 60;
    return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
  }
  function allMockables() {
    return $$("[data-mock]").map((card) => ({
      id: card.id,
      name: card.getAttribute("data-search") || (card.querySelector("h3") && card.querySelector("h3").textContent) || card.id,
      cat: card.getAttribute("data-cat") || "design",
      html: card.innerHTML
    }));
  }
  function renderMock(p, minutes) {
    currentMock = p;
    mockLeft = minutes * 60;
    const panel = $("#mock-panel");
    panel.innerHTML =
      '<div class="meta-row"><span class="badge badge-pattern">' + escapeHtml(p.cat) + "</span>" +
      '<span class="chip">' + minutes + " min</span></div>" +
      "<h3>" + escapeHtml(p.name) + "</h3>" +
      '<div class="timer" id="mock-timer">' + fmt(mockLeft) + "</div>" +
      '<div class="status-btns">' +
      '<button type="button" id="mock-start-timer">Start timer</button>' +
      '<button type="button" id="mock-pause">Pause</button></div>' +
      '<div class="problem-body">' + p.html + "</div>";
    $("#mock-start-timer") && $("#mock-start-timer").addEventListener("click", startTimer);
    $("#mock-pause") && $("#mock-pause").addEventListener("click", stopTimer);
    bindToggles(panel);
    bindCopy(panel);
  }
  function tick() {
    mockLeft = Math.max(0, mockLeft - 1);
    const el = $("#mock-timer");
    if (el) el.textContent = fmt(mockLeft);
    if (mockLeft === 0) stopTimer();
  }
  function startTimer() { stopTimer(); mockTimer = setInterval(tick, 1000); }
  function stopTimer() { if (mockTimer) clearInterval(mockTimer); mockTimer = null; }

  $$("[data-start-mock]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const minutes = Number(btn.getAttribute("data-start-mock")) || 45;
      const cat = ($("#mock-cat") && $("#mock-cat").value) || "all";
      let list = allMockables();
      if (cat !== "all") list = list.filter((x) => x.cat === cat || x.cat === cat);
      if (!list.length) list = allMockables();
      if (!list.length) return;
      renderMock(list[Math.floor(Math.random() * list.length)], minutes);
    });
  });

  const saveMock = $("#save-mock");
  saveMock && saveMock.addEventListener("click", () => {
    if (!currentMock) { alert("Start a mock interview first."); return; }
    const rec = {
      id: currentMock.id,
      name: currentMock.name,
      date: new Date().toISOString(),
      req: $("#mock-r-req") && $("#mock-r-req").value,
      estimate: $("#mock-r-est") && $("#mock-r-est").value,
      architecture: $("#mock-r-arch") && $("#mock-r-arch").value,
      data: $("#mock-r-data") && $("#mock-r-data").value,
      scaling: $("#mock-r-scale") && $("#mock-r-scale").value,
      reliability: $("#mock-r-rel") && $("#mock-r-rel").value,
      tradeoffs: $("#mock-r-trade") && $("#mock-r-trade").value,
      comms: $("#mock-r-comms") && $("#mock-r-comms").value,
      notes: ($("#mock-notes") && $("#mock-notes").value) || "",
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
      el.innerHTML = "<p class='stat-sub'>No mocks yet. Target 6–8 before leaving Phase 3.</p>";
      return;
    }
    el.innerHTML = "<ul class='tight'>" + state.mocks.slice().reverse().map((m) =>
      "<li>" + escapeHtml(m.date.slice(0, 10)) + " — <b>" + escapeHtml(m.name) + "</b> · confidence " +
      escapeHtml(m.confidence) + "/5</li>"
    ).join("") + "</ul>";
  }

  const resetBtn = $("#reset-progress");
  resetBtn && resetBtn.addEventListener("click", () => {
    if (!confirm("Reset all Phase 3 progress on this browser? This cannot be undone.")) return;
    const theme = state.theme;
    state = defaultState();
    state.theme = theme;
    save(state);
    location.reload();
  });

  $$(".tabs").forEach((wrap) => {
    const group = wrap.getAttribute("data-tabs");
    $$(".tab", wrap).forEach((tab) => {
      tab.addEventListener("click", () => {
        $$(".tab", wrap).forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");
        const which = tab.getAttribute("data-tab");
        if (group === "beq" || group === "sdq") {
          $$(".q[data-level], .problem[data-level]").forEach((card) => {
            if (!card.closest("#" + (group === "beq" ? "beq" : "sysdesign"))) return;
            card.classList.toggle("hidden", which !== "all" && card.getAttribute("data-level") !== which && card.getAttribute("data-cat") !== which);
          });
          return;
        }
        $$("[data-tabpanel='" + group + "']").forEach((p) => {
          p.classList.toggle("hidden", p.getAttribute("data-tab") !== which);
        });
      });
    });
  });

  const navLinks = $$(".sidebar a[href^='#']");
  const sections = navLinks.map((a) => document.querySelector(a.getAttribute("href"))).filter(Boolean);
  function onScroll() {
    let current = sections[0];
    sections.forEach((s) => { if (s.getBoundingClientRect().top <= 90) current = s; });
    navLinks.forEach((a) => a.classList.toggle("active", current && a.getAttribute("href") === "#" + current.id));
  }
  document.addEventListener("scroll", onScroll, { passive: true });
  $("#back-top") && $("#back-top").addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

  const gq = $("#glossary-filter");
  gq && gq.addEventListener("input", () => {
    const q = gq.value.toLowerCase();
    $$(".glossary-item").forEach((el) => {
      el.classList.toggle("hidden", q && !el.getAttribute("data-search").toLowerCase().includes(q) && !el.textContent.toLowerCase().includes(q));
    });
  });

  updateProgress();
  updateRevision();
  renderMockHistory();
  applyCardFilters();
})();
