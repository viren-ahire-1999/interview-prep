from util import topic, callout, code


def howto() -> str:
    t = topic("ht-loop", "Read it, say it, break it",
              "how to learn AI engineering", "Lesson", f'''
  <p>AI content is noisy. This file is the spine. For every lesson: <b>say the idea in one sentence</b> → <b>draw the boxes</b> → <b>do one gym item</b> → <b>name a product</b> where it shows up. Watching a 2-hour video without a notebook will not make you an AI engineer.</p>
  <ol>
    <li>If you cannot explain it to a backend teammate, you do not know it yet.</li>
    <li>Prefer a dumb baseline (rule, keyword, logistic) before a large model.</li>
    <li>Every system needs a <b>fail path</b>: what the user sees when retrieval is empty or the model is wrong.</li>
    <li>Write numbers: latency budget, $ / 1k requests, size of the golden set.</li>
  </ol>
  {callout("<b>Tools vs job.</b> LangChain, LlamaIndex, and a vendor’s ‘agent studio’ are optional. The job is data, contracts, eval, and operations. Learn the idea, then pick a library.")}
  <p>You do not need to train GPT. You need to ship a system that is measured and reversible.</p>
  ''', "topics")
    return f'''
<section class="block" id="howto" data-search="How to learn AI engineering" data-stype="Section">
  <p class="kicker">Method</p>
  <h2 class="section-title">How to learn</h2>
  {t}
</section>
'''


def role() -> str:
    t1 = topic("role-map", "Who does what",
               "AI engineer vs ML engineer vs research scientist", "Lesson", f'''
  <p>Titles overlap. Use this map, then ignore the LinkedIn noise.</p>
  <table>
    <tr><th>Role</th><th>Owns</th><th>Typical output</th></tr>
    <tr><td>Software / backend</td><td>APIs, data stores, reliability</td><td>A service that is correct and fast</td></tr>
    <tr><td>Data scientist</td><td>Questions, stats, experiments</td><td>A finding or a notebook model</td></tr>
    <tr><td>ML engineer</td><td>Training loops, features, model serving</td><td>A trained model in production</td></tr>
    <tr><td><b>AI engineer</b></td><td>Applied systems: RAG, tools, eval, product UX</td><td>A working AI feature with guardrails</td></tr>
    <tr><td>Research / applied scientist</td><td>New methods, papers, hard modeling</td><td>A better algorithm or a paper</td></tr>
  </table>
  <p>In a small company you wear three of these hats. In a large one, an AI engineer still writes Python and reviews PRs — you are not “the prompt person.”</p>
  {callout("<b>Hire bar (practical).</b> Can you take an ambiguous ‘add AI to search’ and return: a v1 that is not a model if a model is unnecessary, a metric, a cost envelope, and a rollback?")}
  ''', "topics")

    t2 = topic("role-stack", "The stack you actually touch",
               "AI engineer stack python data model eval serve", "Lesson", f'''
  {code("text", '''Product question
    → data + labels (or documents)
    → baseline (rules / keyword / logistic)
    → model or LLM API
    → eval set + online metric
    → serve + logs + rollback
    → iterate''')}
  <p>Languages: <b>Python</b> is the default (numpy, pandas, a trainer or an HTTP client). TypeScript shows up in the product UI — you already have that from the rest of this hub. SQL still matters more than a new agent framework.</p>
  <p>Hardware: a laptop is enough for this course. GPUs matter when you train or host open weights. Most product AI in 2026 is an API plus your data.</p>
  ''', "topics")

    return f'''
<section class="block" id="role" data-search="AI engineer role responsibilities" data-stype="Section">
  <p class="kicker">Job</p>
  <h2 class="section-title">The role</h2>
  {t1}{t2}
</section>
'''
