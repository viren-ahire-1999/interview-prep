from util import topic, diagram, callout, code


def dashboard() -> str:
    return r'''
<section class="block" id="dashboard" data-search="Gotta learn before we start dashboard" data-stype="Section">
  <p class="kicker">30 days · OpenShift Observe UI</p>
  <h2 class="section-title">Gotta learn before we start</h2>
  <p class="lede">You already know React and TypeScript. The extra edge is not another framework. It is speaking <b>Observe</b> the way this team ships it: OpenShift <b>console dynamic plugins</b>, <b>PatternFly 6</b>, and turning <b>metrics, logs, and traces</b> into one troubleshooting path — then landing that in <b>upstream GitHub</b>. Each topic below is a <b>tutorial on this page</b> — you should not need another site to understand ConsolePlugin, PromQL, or PatternFly 6 at the level this job uses.</p>

  <div class="card" style="margin-bottom:16px">
    <h3>What “ready” means here</h3>
    <div class="profile-row">
      <span class="chip">Console plugins</span>
      <span class="chip">PatternFly 6</span>
      <span class="chip">PromQL / LogQL / TraceQL</span>
      <span class="chip">Perses</span>
      <span class="chip">Korrel8r</span>
      <span class="chip">Accessibility</span>
    </div>
    <p class="stat-sub" style="margin-top:12px">This is a 30-day onboarding guide for an observability UI lead role on OpenShift. You sit between backend signal teams, product, and UX. You do not need to write operators. You do need to read YAML, query three backends, and review plugin PRs like a senior.</p>
  </div>

  <div class="grid grid-2" style="margin-bottom:16px">
    <div class="card">
      <h3>You will be able to</h3>
      <ul class="tight">
        <li>Explain a ConsolePlugin and a UIPlugin CR</li>
        <li>Build UI that looks like PatternFly 6, not a SaaS dashboard</li>
        <li>Say why plugins must not import PatternFly CSS</li>
        <li>Pick the right signal: metric vs log vs trace</li>
        <li>Write a useful PromQL and a useful LogQL</li>
        <li>Follow one request through OpenTelemetry into Tempo</li>
        <li>Sketch Korrel8r: alert → related logs, metrics, pods</li>
        <li>Talk empty / error / partial-query states with backend</li>
      </ul>
    </div>
    <div class="card">
      <h3>How to use this file</h3>
      <ol class="tight">
        <li>Open the named <b>tutorial</b> in the sidebar (not only the 30-day card).</li>
        <li>Read until you can teach the diagram. Mark the lesson complete.</li>
        <li>Do that day’s install or sketch. Check the plan boxes.</li>
        <li>Leave when Readiness is honestly ~85% and you can teach the plugin loop without notes.</li>
      </ol>
    </div>
  </div>

  <div class="grid grid-3">
    <div class="card"><div class="stat-sub">Days / daily tasks</div><div class="stat" id="stat-days">0%</div><div class="bar"><span id="bar-days"></span></div></div>
    <div class="card"><div class="stat-sub">Lessons</div><div class="stat" id="stat-arch">0%</div><div class="bar"><span id="bar-arch"></span></div></div>
    <div class="card"><div class="stat-sub">Practical studies</div><div class="stat" id="stat-react">0%</div><div class="bar"><span id="bar-react"></span></div></div>
    <div class="card"><div class="stat-sub">Q&amp;A</div><div class="stat" id="stat-qs">0 / 0</div><div class="bar"><span id="bar-qs"></span></div></div>
    <div class="card"><div class="stat-sub">Exercises</div><div class="stat" id="stat-sd">0 / 0</div><div class="bar"><span id="bar-sd"></span></div></div>
    <div class="card"><div class="stat-sub">Mock interviews</div><div class="stat" id="stat-mocks">0</div><p class="stat-sub">Optional</p></div>
    <div class="card"><div class="stat-sub">Overall readiness</div><div class="stat" id="stat-ready">0%</div><div class="bar"><span id="bar-ready"></span></div></div>
    <div class="card"><div class="stat-sub">Items to review</div><div class="stat" id="stat-review">0</div></div>
    <div class="card"><div class="stat-sub">Drills</div><div class="stat" id="stat-ex">0 / 0</div><div class="bar"><span id="bar-ex"></span></div></div>
  </div>
  <div class="callout" style="margin-top:18px">
    <b>Progress.</b> <code>localStorage</code> key <code>pre-start-v1</code> on this browser only. Separate from DSA, AI Engineer, and Atlassian phases.
  </div>
</section>
'''


def howto() -> str:
    t = topic("ht-edge", "Four things beat reading every repo",
              "how to use this 30 day guide", "Lesson",
              """
  <p>Tutorials live in this HTML. Use the sidebar: Kubernetes, plugins, PatternFly, PromQL, LogQL, traces, Observe UX, Perses, Korrel8r. Clone repos <i>after</i> you can teach the matching tutorial.</p>
  <p>You will not finish every plugin repository. Finish a loop you can demonstrate:</p>
  <ol>
    <li><b>Plugin template running</b> against a cluster (or the documented local console container).</li>
    <li><b>Three PatternFly 6 screens</b> that work keyboard-only and pass a basic axe pass.</li>
    <li><b>One request followed</b> across metrics, logs, and traces (OpenTelemetry demo is enough).</li>
    <li><b>A written correlation story</b> from “pod CrashLooping” to the Observe pages.</li>
  </ol>
  """ + callout("<b>Tools vs job.</b> Webpack, Yarn, and <code>oc</code> are the daily loop. Tailwind and a new chart library are not. The console already owns PatternFly CSS.") + """
  <p>Internal CI, Jira, and downstream branches wait until you have accounts. Everything in this file is public.</p>
  """, "topics")
    return f'''
<section class="block" id="howto" data-search="How to use this 30 day guide" data-stype="Section">
  <p class="kicker">Method</p>
  <h2 class="section-title">How to use this</h2>
  {t}
</section>
'''


def role() -> str:
    t = topic("role-catalyst", "You are the UI catalyst, not a dashboard contractor",
              "observability UI job OpenShift Observe", "Lesson",
              """
  <p>The job is to shape how people <i>experience</i> observability across OpenShift and multi-cluster management — not to paint charts in isolation.</p>
  <p>Backend teams own Prometheus, Loki, Tempo, Alertmanager. You own the <b>single pane</b>: time range, empty states, RBAC-aware lists, and jumps between signals. Product and UX sit in the same design conversation.</p>
  """ + diagram("""PM / UX ──► you (plugin + PF + a11y)
metrics team     logging team     tracing team
       └── UIPlugin / ConsolePlugin ──► Observe menu""") + """
  <p><b>Lead</b> means you propose a plugin boundary, a proxy, a feature flag, and a PatternFly pattern — not a new SPA. <b>Upstream</b> means the feature lands on GitHub first, then in the operator that installs it on a cluster.</p>
  """ + callout("React fluency is assumed. The people who move fastest can explain ConsolePlugin, UIPlugin, and why a PromQL range query, a Loki stream, and a Tempo trace share one troubleshooting journey."), "topics")
    return f'''
<section class="block" id="role" data-search="observability UI role catalyst" data-stype="Section">
  <p class="kicker">Why this file exists</p>
  <h2 class="section-title">The job</h2>
  {t}
</section>
'''
