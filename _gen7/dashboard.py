def dashboard() -> str:
    return r'''
<section class="block" id="dashboard" data-search="AI Engineer course dashboard" data-stype="Section">
  <p class="kicker">Basics → advanced · applied AI engineer</p>
  <h2 class="section-title">AI Engineer</h2>
  <p class="lede">This course is a single path from “what is a model?” to shipping retrieval, agents, evaluation, and production systems. It is written to be <b>easy to read</b> and still <b>specific enough to use at work</b>. You will not train a frontier model here. You will learn the judgment an AI engineer is hired for: pick the cheapest honest system, measure it, and keep it safe.</p>

  <div class="card" style="margin-bottom:16px">
    <h3>What “complete” means here</h3>
    <div class="profile-row">
      <span class="chip">Foundations</span>
      <span class="chip">Classical ML</span>
      <span class="chip">Deep learning</span>
      <span class="chip">LLMs / RAG / agents</span>
      <span class="chip">Eval + safety</span>
      <span class="chip">MLOps</span>
    </div>
    <p class="stat-sub" style="margin-top:12px">An AI engineer sits between research and product. You use Python, data, APIs or open models, and software engineering. You do <i>not</i> need a PhD. You <i>do</i> need to explain trade-offs without hiding behind a library name. Practice items are labeled practice — not claimed official company questions.</p>
  </div>

  <div class="grid grid-2" style="margin-bottom:16px">
    <div class="card">
      <h3>You will be able to</h3>
      <ul class="tight">
        <li>Explain ML vs DL vs LLMs in plain language</li>
        <li>Split data without leaking the future into the past</li>
        <li>Choose a metric that matches the product cost of errors</li>
        <li>Sketch a transformer and why attention replaced recurrence</li>
        <li>Design RAG with chunking, citations, and a fail path</li>
        <li>Decide prompt vs RAG vs fine-tune vs agent</li>
        <li>Evaluate quality without trusting a single “LLM judge”</li>
        <li>Talk cost, latency, observability, and safety in a design</li>
      </ul>
    </div>
    <div class="card">
      <h3>How to use this file</h3>
      <ol class="tight">
        <li>Open the <b>42-Day Plan</b>. Check every box.</li>
        <li>Read one lesson. Say the idea out loud before the code.</li>
        <li>Do the <b>Practice this topic</b> gym at the bottom of the section.</li>
        <li>Do the matching practical study (a product-shaped version).</li>
        <li>Weekly: Mock Interview Mode. Save a debrief.</li>
        <li>Leave when Readiness is honestly ~85% and you can teach RAG + eval without notes.</li>
      </ol>
    </div>
  </div>

  <div class="grid grid-3">
    <div class="card"><div class="stat-sub">Days / daily tasks</div><div class="stat" id="stat-days">0%</div><div class="bar"><span id="bar-days"></span></div></div>
    <div class="card"><div class="stat-sub">Lessons</div><div class="stat" id="stat-arch">0%</div><div class="bar"><span id="bar-arch"></span></div></div>
    <div class="card"><div class="stat-sub">Practical studies</div><div class="stat" id="stat-react">0%</div><div class="bar"><span id="bar-react"></span></div></div>
    <div class="card"><div class="stat-sub">Q&amp;A</div><div class="stat" id="stat-qs">0 / 0</div><div class="bar"><span id="bar-qs"></span></div></div>
    <div class="card"><div class="stat-sub">Exercises</div><div class="stat" id="stat-sd">0 / 0</div><div class="bar"><span id="bar-sd"></span></div></div>
    <div class="card"><div class="stat-sub">Mock interviews</div><div class="stat" id="stat-mocks">0</div><p class="stat-sub">Target 8–10</p></div>
    <div class="card"><div class="stat-sub">Overall readiness</div><div class="stat" id="stat-ready">0%</div><div class="bar"><span id="bar-ready"></span></div></div>
    <div class="card"><div class="stat-sub">Items to review</div><div class="stat" id="stat-review">0</div></div>
    <div class="card"><div class="stat-sub">Drills</div><div class="stat" id="stat-ex">0 / 0</div><div class="bar"><span id="bar-ex"></span></div></div>
  </div>
  <div class="callout" style="margin-top:18px">
    <b>Progress.</b> <code>localStorage</code> key <code>ai-eng-v1</code> on this browser only. Separate from DSA (<code>dsa-js-v1</code>) and Atlassian phases.
  </div>
</section>
'''
