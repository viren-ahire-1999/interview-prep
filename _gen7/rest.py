from util import callout


def mock() -> str:
    return r'''
<section class="block" id="mock" data-search="Mock Interview Mode AI Engineer" data-stype="Section">
  <p class="kicker">Timed practice</p>
  <h2 class="section-title">Mock Interview Mode</h2>
  <p class="lede">Draws a random practice item from the problem bank and Q&amp;A (<code>data-mock</code>). Speak: baseline → metric → fail path → then the design or code. Reveal after you have an approach. Save a debrief.</p>
  <div class="card" style="margin-bottom:16px">
    <p>Category
      <select id="mock-cat">
        <option value="all">All</option>
        <option value="role">role</option>
        <option value="data">data</option>
        <option value="python">python</option>
        <option value="foundations">foundations</option>
        <option value="metrics">metrics</option>
        <option value="ml">ml</option>
        <option value="models">models</option>
        <option value="features">features</option>
        <option value="dl">dl</option>
        <option value="nn">nn</option>
        <option value="embed">embed</option>
        <option value="llm">llm</option>
        <option value="prompt">prompt</option>
        <option value="rag">rag</option>
        <option value="finetune">finetune</option>
        <option value="agents">agents</option>
        <option value="eval">eval</option>
        <option value="safety">safety</option>
        <option value="prod">prod</option>
        <option value="serve">serve</option>
        <option value="mlops">mlops</option>
        <option value="design">design</option>
      </select>
    </p>
    <div class="status-btns">
      <button type="button" class="toggle-btn" data-start-mock="15">15-min question</button>
      <button type="button" class="toggle-btn" data-start-mock="30">30-min problem</button>
      <button type="button" class="toggle-btn" data-start-mock="45">45-min design</button>
      <button type="button" class="toggle-btn" data-start-mock="60">60-min teach-back</button>
    </div>
    <div id="mock-panel"><p class="stat-sub">Pick a duration. Narrate before you type. Reveal only after you have a baseline, a metric, and a fail path.</p></div>
  </div>
  <div class="card">
    <h3>Debrief rubric</h3>
    <label class="task"><input type="checkbox" id="mock-q-trade" /> <span>I named a baseline (rule, logistic, prompt-only, or keyword search) and why the chosen approach is better</span></label>
    <label class="task"><input type="checkbox" id="mock-q-time" /> <span>I named a metric that matches the cost of false positives vs false negatives</span></label>
    <label class="task"><input type="checkbox" id="mock-q-a11y" /> <span>I named a fail / refuse / escalate path and one leakage or ACL risk</span></label>
    <p>Notes<br /><textarea id="mock-notes" rows="3" style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:inherit"></textarea></p>
    <p>Confidence
      <select id="mock-confidence">
        <option value="1">1</option><option value="2">2</option>
        <option value="3" selected>3</option><option value="4">4</option><option value="5">5</option>
      </select>
    </p>
    <p><button type="button" class="toggle-btn" id="save-mock">Save mock</button></p>
  </div>
  <div class="card" style="margin-top:16px"><h3>History</h3><div id="mock-history"></div></div>
</section>
'''


def progress() -> str:
    return r'''
<section class="block" id="progress" data-search="Progress Tracker AI Engineer" data-stype="Section">
  <p class="kicker">localStorage ai-eng-v1</p>
  <h2 class="section-title">Progress Tracker</h2>
  <div class="grid grid-2">
    <div class="card"><h3>Daily tasks</h3><p id="track-days">0</p></div>
    <div class="card"><h3>Lessons</h3><p id="track-arch">0</p><div class="bar"><span id="bar-cat-arch"></span></div></div>
    <div class="card"><h3>Practical studies</h3><p id="track-react">0</p><div class="bar"><span id="bar-cat-react"></span></div></div>
    <div class="card"><h3>Interview questions</h3><p id="track-qs">0</p></div>
    <div class="card"><h3>Exercises</h3><p id="track-sd">0</p><div class="bar"><span id="bar-cat-sd"></span></div></div>
    <div class="card"><h3>Implement drills</h3><p id="track-ex">0</p></div>
  </div>
  <p style="margin-top:18px"><button type="button" class="danger-btn" id="reset-progress">Reset all AI Engineer progress</button></p>
</section>
<section class="block" id="revision" data-search="Revision spaced repetition AI Engineer" data-stype="Section">
  <p class="kicker">Remember on purpose</p>
  <h2 class="section-title">Revision System</h2>
  <p class="lede">Solved items review at 1 → 3 → 7 → 14 → 30 days. Attempted/failed → tomorrow. Mastered parks at 30 days.</p>
  <div class="grid grid-2">
    <div class="card"><h3>Due today</h3><ul class="tight" id="rev-today"></ul></div>
    <div class="card"><h3>Due this week</h3><ul class="tight" id="rev-week"></ul></div>
    <div class="card"><h3>Recently failed</h3><ul class="tight" id="rev-failed"></ul></div>
    <div class="card"><h3>Weak areas</h3><ul class="tight" id="rev-weak"></ul></div>
    <div class="card"><h3>Mastered</h3><ul class="tight" id="rev-mastered"></ul></div>
  </div>
</section>
'''


def readiness() -> str:
    groups = [
        ("From scratch", [
            ("r-ml-llm", "Explain ML vs LLM vs rules in one minute without this file"),
            ("r-split", "Draw a time-safe / user-safe split and name one leakage you avoided"),
            ("r-metric", "Pick precision, recall, or a budgeted threshold from an FP/FN story"),
            ("r-tf", "Say what Q, K, V do in one sentence and why a causal mask exists"),
            ("r-embed", "Explain cosine search and why changing the embed model rebuilds the index"),
            ("r-rag", "Design RAG with cite-from-allow-list and a refuse when excerpts are empty"),
            ("r-prompt", "Write a short system contract: role, sources, refuse, output shape"),
            ("r-lora", "Say when you prompt, retrieve, LoRA, or add an agent — and when you do not"),
        ]),
        ("Applied systems", [
            ("r-agent", "Draw a graph with two typed tools, halt conditions, and no shell/SQL"),
            ("r-eval", "Name a golden set slice (refuse, ACL, empty retrieve) plus one online metric"),
            ("r-judge", "Say why LLM-as-judge is biased and what you still check by hand"),
            ("r-cost", "Estimate tokens and $ for a feature and name two levers (cache, max output)"),
            ("r-acl", "Enforce tenant ACL in the index/query, not in the prompt"),
            ("r-inject", "Delimit untrusted text and keep tools least-privilege — no attack recipes"),
            ("r-serve", "Name TTFT vs total latency and one reason to stream"),
            ("r-bundle", "List the version bundle: prompt, chunker, embed id, index, decode, eval hash"),
        ]),
        ("Explain out loud", [
            ("r-logistic", "Why start with logistic / a keyword baseline before a net or an LLM"),
            ("r-auc", "Why a high ROC-AUC can still fail a review-budget product"),
            ("r-window", "What a context window is and why dumping the wiki still fails"),
            ("r-sft", "Pretrain vs SFT vs preference in one line each"),
            ("r-faith", "How you treat unsupported answers even when the prose sounds grounded"),
            ("r-drift", "Name input, corpus, and concept drift with one alert each"),
        ]),
        ("Practical", [
            ("r-wiki", "Walk wiki-chat: ingest → ACL retrieve → generate → cite → escalate"),
            ("r-class", "Walk a ticket classifier: labels, split, metric, threshold, human queue"),
            ("r-rollback", "Describe canary + rollback for a prompt or index without a meeting"),
            ("r-pii", "Say what must not land in SaaS traces and how you debug without raw PII"),
            ("r-v1", "Cut a design to a scoped v1 with two explicit rejects"),
            ("r-close", "Close a 45-minute design in one breath: v1, rejects, metric, fail path"),
        ]),
        ("Senior behavior", [
            ("r-baseline", "Start every mock with a baseline before the fancy model"),
            ("r-honest", "Say what the system cannot do (truth, ACL, math) without being asked"),
            ("r-numbers", "Guess QPS, corpus size, latency, and $ / 1k and label them guesses"),
            ("r-demo", "Refuse to treat a cherry-picked demo as a launch gate"),
            ("r-teach", "Teach RAG or leakage to a rubber duck in 5 minutes from a blank page"),
        ]),
    ]
    html = []
    for title, items in groups:
        html.append(f"<h3>{title}</h3>")
        for id_, label in items:
            html.append(
                f'<label class="task"><input type="checkbox" data-id="{id_}" data-group="readiness" /><span>{label}</span></label>'
            )
    return f'''
<section class="block" id="readiness" data-search="AI Engineer readiness checklist" data-stype="Section">
  <p class="kicker">Gate</p>
  <h2 class="section-title">Readiness checklist</h2>
  <p class="lede">Check only if you can do it <i>today</i> without this file. Stay until ~85% and 8+ mocks. Then you are ready to work as an applied AI engineer: data, models, RAG/agents, eval, and production.</p>
  <p class="stat">Score: <span id="ready-score">0%</span></p>
  <div class="bar"><span id="bar-ready-final"></span></div>
  <p id="ready-gate" class="stat-sub"></p>
  {''.join(html)}
</section>
'''


def resources() -> str:
    rows = [
        ("Python tutorial", "https://docs.python.org/3/tutorial/",
         "Language you will write most AI glue in.", "Finish enough to read the snippets in this course. You do not need to be a Python expert first.", "Python", False),
        ("NumPy user guide", "https://numpy.org/doc/stable/user/index.html",
         "Arrays, broadcasting, shapes.", "Pairs with the Python for AI lesson. Check shapes after every line.", "Python", False),
        ("scikit-learn user guide", "https://scikit-learn.org/stable/user_guide.html",
         "Splits, pipelines, metrics, linear models, trees.", "Official APIs for classical ML. Prefer Pipeline so val statistics do not leak.", "Classical ML", False),
        ("PyTorch tutorials", "https://pytorch.org/tutorials/",
         "Tensors, autograd, train vs eval.", "Use after the neural-net lesson. Stay on small models first.", "Deep learning", False),
        ("Hugging Face docs", "https://huggingface.co/docs",
         "Tokenizers, models, datasets, PEFT/LoRA.", "Read the page for the library you actually import. Do not cargo-cult every trainer flag.", "GenAI", False),
        ("Hugging Face course", "https://huggingface.co/learn/nlp-course",
         "NLP and transformers in practice.", "Optional depth after you can explain attention in your own words.", "Deep learning", True),
        ("OpenAI API docs", "https://platform.openai.com/docs",
         "Chat, tools, embeddings — vendor surface.", "Optional. Treat as one vendor. The course ideas transfer.", "Serving", True),
        ("Anthropic docs", "https://docs.anthropic.com/",
         "Messages API, tool use, long context.", "Optional second vendor. Compare tool schemas and safety docs.", "Serving", True),
        ("OWASP Top 10 for LLM Applications", "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
         "Prompt injection, data leakage, unbounded consumption — defensive list.", "Read as a product checklist. This course does not teach attacks.", "Safety", True),
        ("Frontend system design on this hub", "frontend-system-design.html",
         "Product design discipline you reuse for AI features.", "AI design still needs scoped v1, metrics, and fail paths.", "Design", False),
        ("DSA in JavaScript on this hub", "dsa-javascript.html",
         "Algorithms if you also interview as a general SWE.", "Optional for an AI-only track. Complementary, not a prerequisite.", "Foundations", True),
    ]
    cards = []
    for name, url, what, why, topic, opt in rows:
        badge = '<span class="badge badge-opt">Optional</span>' if opt else '<span class="badge badge-pattern">Primary</span>'
        cards.append(f'''
<article class="card" data-search="{name}" data-stype="Resource">
  <div class="meta-row">{badge}</div>
  <h3><a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a></h3>
  <p><b>Teaches.</b> {what}</p>
  <p><b>Why open it.</b> {why}</p>
  <p><b>Course topic.</b> {topic}</p>
</article>''')
    return f'''
<section class="block" id="resources" data-search="Resource library AI Engineer" data-stype="Section">
  <p class="kicker">Official first</p>
  <h2 class="section-title">Resource Library</h2>
  <p class="lede">This HTML already contains the teaching. Links are official docs and optional vendor pages — not pirated books. Practice items here are original teaching, not claimed company questions.</p>
  {callout("Safety pages are defensive: PII, ACL, untrusted text, escalation. They are not attack how-tos.")}
  <div class="grid grid-2">{''.join(cards)}</div>
</section>
'''


def glossary() -> str:
    terms = [
        ("ACL", "Who may see which document or call which tool. Enforced in retrieval and code, not in the prompt."),
        ("ANN", "Approximate nearest neighbor search over embeddings (HNSW, IVF). Fast, not exact."),
        ("Baseline", "The simple system you beat: a rule, logistic regression, keyword search, or a prompt-only LLM."),
        ("Chunking", "Splitting documents so retrieval can return a useful excerpt. Size is a product choice."),
        ("Concept drift", "The meaning of the label changes (what counts as spam this year)."),
        ("Context window", "How many tokens the model can attend to in one call. Not a license to dump the wiki."),
        ("Embedding", "A vector placed so similar items are nearby under cosine or dot product."),
        ("Eval / golden set", "Versioned inputs with expected properties. Used like unit tests. Keep out of SFT train."),
        ("Faithfulness", "Whether the answer is supported by the excerpts you retrieved — not whether it sounds smart."),
        ("Fine-tuning / SFT", "Updating (some) weights on instruction or task pairs. For stable style or a narrow skill."),
        ("FP / FN", "False positive vs false negative. Pick the metric from who pays for each."),
        ("Injection (prompt)", "Untrusted text tries to override instructions or abuse tools. Delimit and least-privilege — do not study attack recipes here."),
        ("Leakage", "Training on information that would not exist at prediction time. Inflates offline scores."),
        ("LLM-as-judge", "Using a model to score answers. Fast, biased, must be calibrated to humans."),
        ("LoRA", "Low-rank adapters: small trainable extra weights. Cheap to store and swap."),
        ("Lost-in-the-middle", "Long prompts: models use the start and end more than the middle. Keep retrieved packs short."),
        ("MLOps", "Versioning data, prompts, indexes, and models; CI eval; canary; rollback."),
        ("Precision / recall", "Of what we flagged, how much was real / of what was real, how much we flagged."),
        ("Preference / RLHF", "Training from ranked or preferred answers after SFT so the model is nicer or safer."),
        ("Pretrain", "Next-token (or similar) training on a huge mix. You rarely rerun this as a product engineer."),
        ("RAG", "Retrieve your text, generate from it, cite, refuse. Does not make the model universally truthful."),
        ("Regularization", "Penalizing complexity (L2, dropout, early stop) so the model does not memorize noise."),
        ("Rerank", "A second model that reorders the top retrieved chunks. Use when k is large or first-stage is noisy."),
        ("Self-attention", "Each token mixes others, weighted by query–key similarity. Q looks, K is looked-up, V is mixed."),
        ("Temperature", "How peaky next-token sampling is. Low for extract/JSON. Does not add facts."),
        ("TTFT", "Time to first token. The ‘is it alive’ feeling. Stream to hide the rest of generation."),
        ("Token", "A chunk of text the vendor counts. Roughly a few characters in English — measure, do not guess forever."),
    ]
    items = []
    for name, defn in terms:
        items.append(f'<article class="card glossary-item" data-search="{name}"><h3>{name}</h3><p>{defn}</p></article>')
    return f'''
<section class="block" id="glossary" data-search="Glossary AI Engineer" data-stype="Section">
  <p class="kicker">Language</p>
  <h2 class="section-title">Glossary</h2>
  <p><input id="glossary-filter" type="search" placeholder="Filter terms..." style="width:100%;max-width:360px;padding:8px 10px;border-radius:8px;border:1px solid var(--border);background:var(--bg);color:inherit" /></p>
  <div class="grid grid-2" style="margin-top:16px">{''.join(items)}</div>
</section>
'''
