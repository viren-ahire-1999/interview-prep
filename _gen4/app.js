(function () {
  "use strict";

  const KEY = "atl-phase4-v1";
  const STORY_N = 22;
  const emptyStory = () => ({
    title: "", situation: "", task: "", actions: "", tech: "", tradeoffs: "",
    result: "", metrics: "", learned: "", change: "", value: "", followups: ""
  });
  const defaultState = () => ({
    theme: "dark",
    navCollapsed: false,
    checks: {},
    topics: {},
    questions: {},
    values: {},
    readiness: {},
    techcheck: {},
    notes: {},
    stories: Array.from({ length: STORY_N }, emptyStory),
    resume: ["", "", "", "", ""],
    recruiter: {},
    sdNotes: {},
    interrogation: [],
    loops: [],
    rejections: [],
    codeMocks: 0,
    items: {}
  });

  function load() {
    try {
      const raw = localStorage.getItem(KEY);
      if (!raw) return defaultState();
      const s = Object.assign(defaultState(), JSON.parse(raw));
      if (!Array.isArray(s.stories) || s.stories.length < STORY_N) {
        const next = Array.from({ length: STORY_N }, emptyStory);
        (s.stories || []).forEach((st, i) => { if (i < STORY_N) next[i] = Object.assign(emptyStory(), st); });
        s.stories = next;
      }
      return s;
    } catch {
      return defaultState();
    }
  }
  function save() { localStorage.setItem(KEY, JSON.stringify(state)); }
  let state = load();

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function applyTheme() {
    document.documentElement.setAttribute("data-theme", state.theme || "dark");
  }
  applyTheme();
  $("#theme-toggle") && $("#theme-toggle").addEventListener("click", () => {
    state.theme = state.theme === "dark" ? "light" : "dark";
    save(); applyTheme();
  });

  const sidebar = $("#sidebar"), backdrop = $("#sidebar-backdrop"), menuBtn = $("#menu-btn");
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
    save();
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
    const root = btn.closest(".problem, .q, .ex, .topic, .card") || document;
    return root.querySelector("#" + CSS.escape(id)) || document.getElementById(id);
  }
  $$("[data-toggle]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const el = findToggleTarget(btn);
      if (el) el.classList.toggle("open");
    });
  });
  $$(".code-block").forEach((block) => {
    const btn = block.querySelector(".copy-btn");
    const code = block.querySelector("pre");
    if (!btn || !code) return;
    btn.addEventListener("click", async () => {
      try { await navigator.clipboard.writeText(code.textContent || ""); }
      catch {
        const ta = document.createElement("textarea");
        ta.value = code.textContent || "";
        document.body.appendChild(ta); ta.select(); document.execCommand("copy"); ta.remove();
      }
      btn.textContent = "Copied";
      setTimeout(() => { btn.textContent = "Copy"; }, 1200);
    });
  });
  $$(".day-head").forEach((btn) => {
    btn.addEventListener("click", () => btn.parentElement.classList.toggle("open"));
  });

  $$("input[type=checkbox][data-id]").forEach((box) => {
    const id = box.getAttribute("data-id");
    const group = box.getAttribute("data-group") || "checks";
    if (!state[group]) state[group] = {};
    box.checked = !!state[group][id];
    box.addEventListener("change", () => {
      state[group][id] = box.checked;
      save(); updateProgress();
    });
  });
  $$("[data-complete]").forEach((btn) => {
    const group = btn.getAttribute("data-complete");
    const id = btn.getAttribute("data-cid");
    if (!state[group]) state[group] = {};
    if (state[group][id]) { btn.classList.add("done"); btn.textContent = "Completed"; }
    btn.addEventListener("click", () => {
      if (!state[group]) state[group] = {};
      state[group][id] = !state[group][id];
      btn.classList.toggle("done", !!state[group][id]);
      btn.textContent = state[group][id] ? "Completed" : (btn.textContent.indexOf("studied") >= 0 ? "Mark studied" : "Mark complete");
      save(); updateProgress();
    });
  });

  $$("[data-note]").forEach((el) => {
    const k = el.getAttribute("data-note");
    el.value = state.notes[k] || "";
    el.addEventListener("input", () => { state.notes[k] = el.value; save(); });
  });
  $$("[data-rec]").forEach((el) => {
    const k = el.getAttribute("data-rec");
    el.value = state.recruiter[k] || "";
    el.addEventListener("input", () => { state.recruiter[k] = el.value; save(); });
  });
  $$("[data-sdf]").forEach((el) => {
    const k = el.getAttribute("data-sdf");
    if (state.sdNotes[k]) el.value = state.sdNotes[k];
    el.addEventListener("input", () => { state.sdNotes[k] = el.value; save(); });
  });

  $$("[data-story]").forEach((card) => {
    const i = Number(card.getAttribute("data-story"));
    const st = state.stories[i] || emptyStory();
    $$("[data-sf]", card).forEach((el) => {
      const f = el.getAttribute("data-sf");
      el.value = st[f] || "";
      el.addEventListener("input", () => {
        if (!state.stories[i]) state.stories[i] = emptyStory();
        state.stories[i][f] = el.value;
        save(); updateProgress();
      });
    });
  });

  $$("[data-rb]").forEach((card) => {
    const i = Number(card.getAttribute("data-rb"));
    const input = card.querySelector("[data-rf=bullet]");
    if (!input) return;
    input.value = state.resume[i] || "";
    input.addEventListener("input", () => {
      state.resume[i] = input.value;
      save(); updateProgress();
    });
  });

  let iqIndex = -1;
  const iqItems = $$("#interrogation-qs li");
  function showIq() {
    iqItems.forEach((li, n) => li.classList.toggle("open", n === iqIndex));
    const num = $("#iq-num");
    if (num) num.textContent = iqIndex < 0 ? 0 : iqIndex + 1;
  }
  $("#start-interrogation") && $("#start-interrogation").addEventListener("click", () => {
    $("#interrogation-panel").classList.remove("hidden");
    iqIndex = 0; showIq();
  });
  $("#iq-next") && $("#iq-next").addEventListener("click", () => {
    if (iqIndex < iqItems.length - 1) { iqIndex += 1; showIq(); }
  });
  $("#save-interrogation") && $("#save-interrogation").addEventListener("click", () => {
    state.interrogation.push({
      date: new Date().toISOString(),
      project: ($("#iq-project") && $("#iq-project").value) || "",
      score: ($("#iq-score") && $("#iq-score").value) || "",
      confidence: ($("#iq-confidence") && $("#iq-confidence").value) || "",
      notes: ($("#iq-notes") && $("#iq-notes").value) || ""
    });
    save(); renderIqHistory(); updateProgress();
    alert("Interrogation saved locally.");
  });
  function renderIqHistory() {
    const el = $("#iq-history");
    if (!el) return;
    el.innerHTML = state.interrogation.length
      ? "<ul class='tight'>" + state.interrogation.slice().reverse().map((x) =>
        "<li>" + escapeHtml(x.date.slice(0, 10)) + " — " + escapeHtml(x.project || "untitled") +
        " · score " + escapeHtml(x.score) + "</li>").join("") + "</ul>"
      : "<p>No sessions yet.</p>";
  }
  renderIqHistory();

  let codeTimer = null, codeLeft = 0;
  function fmt(sec) {
    const m = Math.floor(sec / 60), s = sec % 60;
    return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
  }
  function tickCode() {
    codeLeft = Math.max(0, codeLeft - 1);
    const el = $("#code-timer");
    if (el) el.textContent = fmt(codeLeft);
    if (codeLeft === 0) { clearInterval(codeTimer); codeTimer = null; }
  }
  $$("[data-start-code]").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (codeTimer) clearInterval(codeTimer);
      codeLeft = (Number(btn.getAttribute("data-start-code")) || 45) * 60;
      const problems = $$("[data-mock-code]");
      const pick = problems[Math.floor(Math.random() * problems.length)];
      const panel = $("#code-panel");
      if (panel && pick) {
        panel.innerHTML = "<p class='stat-sub'>Work this problem. Do not reveal the solution until you finish or time is up.</p>" +
          "<h3>" + escapeHtml(pick.querySelector("h3") ? pick.querySelector("h3").textContent : pick.id) + "</h3>";
      }
      tickCode();
      codeTimer = setInterval(tickCode, 1000);
      state.codeMocks += 1;
      save(); updateProgress();
    });
  });
  $("#code-stop") && $("#code-stop").addEventListener("click", () => {
    if (codeTimer) clearInterval(codeTimer);
    codeTimer = null;
  });

  $("#start-loop") && $("#start-loop").addEventListener("click", () => {
    $("#loop-panel").classList.remove("hidden");
    window.location.hash = "loop";
  });
  $("#save-loop") && $("#save-loop").addEventListener("click", () => {
    const scores = {};
    $$("[data-loop-score]").forEach((el) => { scores[el.getAttribute("data-loop-score")] = el.value; });
    state.loops.push({
      date: new Date().toISOString(),
      scores,
      strengths: ($("#loop-strengths") && $("#loop-strengths").value) || "",
      weaknesses: ($("#loop-weaknesses") && $("#loop-weaknesses").value) || ""
    });
    save(); renderLoopHistory(); updateProgress();
    alert("Loop debrief saved.");
  });
  function renderLoopHistory() {
    const el = $("#loop-history");
    if (!el) return;
    el.innerHTML = state.loops.length
      ? "<ul class='tight'>" + state.loops.slice().reverse().map((x) => {
        const vals = Object.values(x.scores || {}).map(Number);
        const avg = vals.length ? (vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(1) : "—";
        return "<li>" + escapeHtml(x.date.slice(0, 10)) + " — avg " + avg + "/5</li>";
      }).join("") + "</ul>"
      : "<p>No full loops yet. Target at least one before interview week.</p>";
  }
  renderLoopHistory();

  $("#save-rejection") && $("#save-rejection").addEventListener("click", () => {
    const rec = {};
    $$("[data-rejf]").forEach((el) => { rec[el.getAttribute("data-rejf")] = el.value; });
    rec.date = new Date().toISOString();
    state.rejections.push(rec);
    save(); renderRej(); updateProgress();
    alert("Entry saved.");
  });
  function renderRej() {
    const chart = $("#rej-chart");
    const list = $("#rej-list");
    const counts = {};
    state.rejections.forEach((r) => {
      const c = r.category || "Uncategorized";
      counts[c] = (counts[c] || 0) + 1;
    });
    const max = Math.max(1, ...Object.values(counts));
    if (chart) {
      chart.innerHTML = Object.keys(counts).length
        ? Object.entries(counts).map(([k, n]) =>
          '<div class="chart-bar"><b>' + escapeHtml(k) + "</b><div class='bar'><span style='width:" +
          Math.round((n / max) * 100) + "%'></span></div><span>" + n + "</span></div>").join("")
        : "<p class='stat-sub'>No entries yet.</p>";
    }
    if (list) {
      list.innerHTML = state.rejections.slice().reverse().map((r) =>
        "<p>" + escapeHtml((r.date || "").slice(0, 10)) + " · " + escapeHtml(r.round || "") +
        " · " + escapeHtml(r.category || "") + "</p>").join("");
    }
  }
  renderRej();

  $("#techcheck-reset") && $("#techcheck-reset").addEventListener("click", () => {
    state.techcheck = {};
    $$('input[data-group=techcheck]').forEach((b) => { b.checked = false; });
    save(); updateProgress();
  });

  $$(".tabs").forEach((wrap) => {
    $$(".tab", wrap).forEach((tab) => {
      tab.addEventListener("click", () => {
        $$(".tab", wrap).forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");
        const which = tab.getAttribute("data-tab");
        const section = wrap.closest("section");
        $$(".q", section).forEach((card) => {
          card.classList.toggle("hidden", which !== "all" && card.getAttribute("data-cat") !== which);
        });
      });
    });
  });

  const searchInput = $("#global-search");
  const searchBox = $("#search-results");
  const searchIndex = $$("[data-search]").map((el) => ({
    title: el.getAttribute("data-search"),
    type: el.getAttribute("data-stype") || "Section",
    href: "#" + (el.id || (el.closest("section") && el.closest("section").id) || ""),
    excerpt: (el.textContent || "").replace(/\s+/g, " ").trim().slice(0, 110)
  }));
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
  document.addEventListener("click", (e) => {
    if (searchBox && !searchBox.contains(e.target) && e.target !== searchInput) searchBox.classList.remove("open");
  });

  function countTrue(obj) { return Object.values(obj || {}).filter(Boolean).length; }
  function pct(n, d) { return Math.round((n / (d || 1)) * 100); }
  function setText(sel, val) { const el = $(sel); if (el) el.textContent = val; }
  function setWidth(sel, val) { const el = $(sel); if (el) el.style.width = val; }
  function readyIds(prefix) {
    return $$('input[data-group=readiness]').filter((b) => (b.getAttribute("data-id") || "").indexOf(prefix) === 0);
  }
  function readyPct(ids) {
    const n = ids.filter((b) => state.readiness[b.getAttribute("data-id")]).length;
    return pct(n, ids.length || 1);
  }
  function filledStories() {
    return state.stories.filter((s) => s && s.title && s.situation && s.actions).length;
  }

  function updateProgress() {
    const dayDone = countTrue(state.checks);
    const dayTotal = $$('input[data-group=checks]').length || 1;
    const stories = filledStories();
    const storyScore = Math.min(100, Math.round((stories / 10) * 100));
    const techP = readyPct(readyIds("r4-dsa").concat(readyIds("r4-js"), readyIds("r4-react"), readyIds("r4-fe-arch"), readyIds("r4-distributed")));
    const sdP = readyPct(readyIds("r4-sd"));
    const feP = readyPct(readyIds("r4-react").concat(readyIds("r4-fe-arch")));
    const behReady = readyPct(readyIds("r4-tmay").concat(readyIds("r4-why"), readyIds("r4-stories"), readyIds("r4-fail"), readyIds("r4-conflict"), readyIds("r4-lead"), readyIds("r4-customer"), readyIds("r4-incident")));
    const behP = Math.round(behReady * 0.55 + storyScore * 0.45);
    const commP = readyPct(readyIds("r4-comms"));
    const valP = Math.round(readyPct(readyIds("r4-val")) * 0.7 + Math.min(100, countTrue(state.values) * 20) * 0.3);
    const execP = Math.min(100, (state.loops.length * 40) + Math.min(30, state.codeMocks * 8) + Math.min(20, state.interrogation.length * 20) + (state.readiness["r4-mock-loop"] ? 10 : 0));

    const overall = Math.round(
      techP * 0.30 + sdP * 0.20 + feP * 0.15 + behP * 0.15 + commP * 0.10 + valP * 0.05 + execP * 0.05
    );
    let band = "Not Ready";
    if (overall >= 85) band = "Strongly Ready";
    else if (overall >= 70) band = "Interview Ready";
    else if (overall >= 50) band = "Needs Work";

    setText("#overall-pct", overall + "%");
    setWidth("#overall-bar", overall + "%");
    const ring = $("#ready-ring");
    if (ring) ring.style.setProperty("--p", String(overall));
    setText("#ready-ring-n", overall + "%");
    setText("#ready-band", band);
    setText("#stat-tech", techP + "%"); setWidth("#bar-tech", techP + "%");
    setText("#stat-beh", behP + "%"); setWidth("#bar-beh", behP + "%");
    setText("#stat-val", valP + "%"); setWidth("#bar-val", valP + "%");
    setText("#stat-comms", commP + "%"); setWidth("#bar-comms", commP + "%");
    setText("#stat-loop", execP + "%"); setWidth("#bar-loop", execP + "%");
    setText("#stat-days", pct(dayDone, dayTotal) + "%"); setWidth("#bar-days", pct(dayDone, dayTotal) + "%");

    const readyDone = countTrue(state.readiness);
    const readyTotal = $$('input[data-group=readiness]').length || 1;
    setText("#ready-score", pct(readyDone, readyTotal) + "%");
    setWidth("#bar-ready-final", pct(readyDone, readyTotal) + "%");
    const gate = $("#ready-gate");
    if (gate) {
      gate.textContent = readyDone / readyTotal >= 0.85
        ? "Checklist looks honest-high. Keep stories warm and sleep."
        : "Stay in Phase 4 until this checklist is honestly above ~85%.";
    }
    setText("#track-days", dayDone + " / " + dayTotal);
    setWidth("#bar-track-days", pct(dayDone, dayTotal) + "%");
    setText("#track-stories", stories + " / 22 deep-enough (title+situation+actions)");
    setWidth("#bar-track-stories", pct(stories, 22) + "%");
    setText("#track-readiness", pct(readyDone, readyTotal) + "%");
    setWidth("#bar-track-readiness", pct(readyDone, readyTotal) + "%");
    setText("#track-mocks", state.loops.length + " loops · " + state.codeMocks + " coding starts · " + state.interrogation.length + " interrogations");
    setText("#track-resume", state.resume.filter((x) => x && x.trim()).length + " / 5");
    setText("#track-rej", String(state.rejections.length));
  }

  $("#reset-progress") && $("#reset-progress").addEventListener("click", () => {
    if (!confirm("Reset all Phase 4 progress on this browser?")) return;
    const theme = state.theme;
    state = defaultState();
    state.theme = theme;
    save();
    location.reload();
  });

  const navLinks = $$(".sidebar a[href^='#']");
  const sections = navLinks.map((a) => document.querySelector(a.getAttribute("href"))).filter(Boolean);
  document.addEventListener("scroll", () => {
    let current = sections[0];
    sections.forEach((s) => { if (s.getBoundingClientRect().top <= 90) current = s; });
    navLinks.forEach((a) => a.classList.toggle("active", current && a.getAttribute("href") === "#" + current.id));
  }, { passive: true });
  $("#back-top") && $("#back-top").addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

  updateProgress();
})();
