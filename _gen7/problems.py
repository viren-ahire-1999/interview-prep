from util import esc, code


def _p(i, title, level, cat, prompt, idea, src, why, watch, lang="Python"):
    hid = f"ab-{i}"
    body = code(lang, src) if src else ""
    return f'''
<article class="problem" id="{hid}" data-pid="{hid}" data-search="{esc(title)}" data-stype="Problem" data-cat="{cat}" data-level="{level}" data-mock="1" data-filterable>
  <div class="meta-row"><span class="badge badge-{level}">{level}</span><span class="chip">{cat}</span><span class="badge badge-pattern">Practice</span></div>
  <h3>{i}. {esc(title)}</h3>
  <p>{esc(prompt)}</p>
  <p><button type="button" class="toggle-btn" data-toggle="{hid}-a">Reveal solution</button>
     <button type="button" class="toggle-btn" data-complete="designs" data-cid="{hid}">Mark complete</button></p>
  <div class="reveal" id="{hid}-a">
    <p><b>Idea.</b> {idea}</p>
    {body}
    <p><b>Why it matters.</b> {why} &nbsp; <b>Watch.</b> {watch}</p>
  </div>
  <div class="status-btns">
    <button type="button" data-status="not-started">Not Started</button>
    <button type="button" data-status="attempted">Attempted</button>
    <button type="button" data-status="solved">Solved</button>
    <button type="button" data-status="review">Review</button>
    <button type="button" data-status="mastered">Mastered</button>
  </div>
</article>
'''


P = [
    ("Time-safe split", "easy", "data",
     "Write a function that splits a frame with a ‘ts’ column into train/val/test 70/15/15 by time, not shuffle.",
     "Sort by ts. Cut at 70% and 85% of rows (or of unique dates if you want cleaner days).",
     "def time_splits(df, ts='ts'):\n    d = df.sort_values(ts)\n    n = len(d)\n    a, b = int(0.70 * n), int(0.85 * n)\n    return d.iloc[:a], d.iloc[a:b], d.iloc[b:]",
     "This is the most common honest split.", "Do not use a random seed here and call it done."),
    ("Confusion from counts", "easy", "metrics",
     "TP=20, FP=80, FN=5, TN=895. Precision, recall, accuracy. Which number misleads a PM?",
     "P=20/100=0.20. R=20/25=0.80. Acc=915/1000=0.915. Accuracy looks fine; precision is the product pain.",
     "prec, rec, acc = 0.20, 0.80, 0.915",
     "Always show the matrix.", "Accuracy on 5% positives."),
    ("Threshold for a budget", "medium", "metrics",
     "You can review 100 flags/day. How do you pick a threshold from validation scores?",
     "Sort val scores descending. Set threshold at the 100th flag per typical day (scale by traffic). Report precision there.",
     "thr = np.quantile(scores_pos_volume, 1 - 100/n_per_day)",
     "Budgets beat 0.5.", "Recalibrate if volume shifts."),
    ("Cosine implement", "easy", "embed",
     "Implement cosine similarity with a zero-vector guard.",
     "Dot / (norms). Return 0 if either norm is 0.",
     "def cosine(a, b):\n    import numpy as np\n    a, b = np.asarray(a, float), np.asarray(b, float)\n    n = np.linalg.norm(a) * np.linalg.norm(b)\n    return 0.0 if n == 0 else float(a @ b / n)",
     "Retrieval primitive.", "Match vendor normalization."),
    ("Attention toy", "medium", "dl",
     "Q=K=V = [[1,0],[0,1]] (T=2,D=2). Describe the attention weights (no scale).",
     "Scores = QK^T = I. Softmax on rows → still peaked on the diagonal. Each token mostly keeps its own value.",
     "import numpy as np\nQ=K=V=np.eye(2)\nW=np.exp(Q@K.T); W=W/W.sum(1,keepdims=True)",
     "Identity keys → ‘look at self.’", "Scale matters for larger d."),
    ("Prompt contract", "easy", "prompt",
     "Write a 6-line system prompt for an internal billing bot that must not invent policy.",
     "Role, only-from-excerpts, refuse, JSON shape, not legal/tax advice, escalate.",
     "You are Acme billing support.\nUse only excerpts.\nIf insufficient, refuse.\nReturn JSON {answer, cite_ids, refuse}.\nNo tax advice.\nOffer a ticket on refuse.",
     "Contracts > vibes.", "Keep it short enough to be followed."),
    ("RAG refuse", "easy", "rag",
     "Specify the refuse rule in code-level English.",
     "If fewer than 2 hits above MIN cosine, or ACL empty, refuse and do not call the LLM — or call it only to phrase the refuse.",
     "if len(hits) < 2: return {'refuse': True, 'answer': 'Not enough policy text.'}",
     "Cheap refuse saves $ and lies.", "MIN is measured, not 0.7 folklore."),
    ("Citation filter", "easy", "rag",
     "Write a function that drops cite ids not in retrieved.",
     "Set intersection. If none left and the answer claimed cites, fail the item.",
     "def filter_cites(cites, allowed):\n    keep = [c for c in cites if c in allowed]\n    return keep",
     "Types > trust.", "UI must use the filtered list."),
    ("Chunk overlap why", "easy", "rag",
     "Why overlap chunks? When does overlap hurt?",
     "Sentences split across boundaries become retrievable. Overlap hurts when you retrieve near-duplicates and waste the window — dedup by doc+heading.",
     "# overlap 10–20%; dedup adjacent hits from same heading",
     "Boundary insurance.", "Too much overlap → clones in top-k."),
    ("LoRA or RAG", "medium", "finetune",
     "Need: (1) this week’s prices (2) a fixed invoice JSON. Fine-tune one model for both?",
     "No. Prices = RAG or a tool. JSON = schema / light SFT. Two mechanisms.",
     "prices → tool/RAG; schema → constrained decode",
     "Split facts and format.", "One SFT to rule them all fails both."),
    ("Agent halt", "easy", "agents",
     "Write halt conditions for a 3-tool support agent.",
     "steps>=6, usd>=0.25, timeout 20s, repeated same tool+args, user cancel, policy deny.",
     "HALT = dict(max_steps=6, max_usd=0.25, timeout_s=20)",
     "Loops are pages.", "Log the reason."),
    ("Tool deny list", "easy", "agents",
     "Which of these is a product tool: run_sql, get_order, send_as_ceo, search_docs?",
     "get_order and search_docs. The others are incidents.",
     "ALLOW = {'get_order', 'search_docs', 'create_ticket'}",
     "Least privilege.", "PM enthusiasm is not a threat model."),
    ("Golden item", "easy", "eval",
     "Write one golden JSON object for a must-refuse medical question on an HR bot.",
     "Include id, q, should_refuse, notes. No expected long essay.",
     "{'id':'hr-med-1','q':'What dose of ibuprofen should I take for this?','should_refuse':True,'notes':'medical'}",
     "Refuse cases are first-class.", "Do not only store happy FAQ."),
    ("Judge protocol", "medium", "eval",
     "How do you use an LLM judge without fooling yourself?",
     "Blind to which system, swap positions, human calibrate 20%, never sole launch gate, separate model family if you can.",
     "# pairwise + swap + human kappa",
     "Judges have taste.", "Length bias is famous."),
    ("Cost envelope", "easy", "prod",
     "2M chats, 600 in / 180 out, $1 / $3 per 1M tokens. Monthly $?",
     "In: 2e6*600/1e6*1=1200. Out: 2e6*180/1e6*3=1080. $2280 before retries.",
     "print(2e6*(600*1 + 180*3)/1e6)  # 2280",
     "Put $ on the design.", "Tool loops add output."),
    ("Cache key", "medium", "prod",
     "Write a cache key for a RAG answer. What must be in it?",
     "index_id, embed_id, prompt_id, acl, query hash (or normalized q). Not just the raw string.",
     "key = (index_id, embed_id, prompt_id, acl, hash(q))",
     "Wrong key → cross-tenant or stale policy.", "TTL on policy corpora."),
    ("Version bundle", "easy", "mlops",
     "A request went wrong. List the ids you log.",
     "request_id, model, prompt_id, index_id, embed_id, retrieved_ids, tokens, $.",
     "log.update(bundle); log['retrieved_ids']=ids",
     "Replayability.", "Redact the raw text."),
    ("Canary plan", "easy", "mlops",
     "Ship prompt v17. Write a 4-step canary.",
     "CI goldens pass → 5% traffic → watch refuse/retry/$ for N minutes → 100% or rollback to v16.",
     "if guardrail: serve('prompt-v16')",
     "Prompts are releases.", "No silent 100%."),
    ("Design: wiki", "medium", "design",
     "45-min: ChatGPT for Confluence. Outline v1, two rejects, one metric, one question.",
     "v1 RAG+cite+refuse+ACL. Reject SFT-wiki and full-space dump. Metric: recall@5 + supported answers. Ask: spaces and guest users?",
     "# 12-step spine; close cleanly",
     "This is the job interview.", "Do not skip fail."),
    ("Design: voice of customer", "medium", "design",
     "Cluster 50k open-text NPS comments. Do you need an LLM?",
     "v1: embed + cluster + human names. LLM to label cluster titles after. Not a chat over 50k raw comments in one context.",
     "embed → k-means / topic → human names → optional LLM titles",
     "Unsupervised + humans.", "Stuffing 50k comments is a bill."),
    ("Leak hunt", "medium", "data",
     "Feature set includes ticket_resolved_at to predict ticket_will_miss_SLA. Why is this cursed?",
     "Resolved time is after the outcome. Use only fields known at prediction time (created_at, queue, now).",
     "drop columns that are post-outcome",
     "Time-travel.", "Ask when the feature is known."),
    ("Imbalance plan", "easy", "ml",
     "1.5% fraud. Write the training plan in 5 bullets.",
     "Time split, stratify if needed, class weights, metric PR-AUC / recall@precision, threshold from val budget, no accuracy.",
     "LogisticRegression(class_weight='balanced')",
     "Fraud 101.", "SMOTE later, if ever."),
    ("Why not LSTM", "easy", "dl",
     "New NLP classifier on 20k short tickets. LSTM or what?",
     "TF-IDF+linear or a small transformer encoder / API embeddings+linear. LSTM is not the 2026 default.",
     "Tfidf + logistic  # strong baseline",
     "Baselines first.", "RNN only with a reason."),
    ("Injection placement", "medium", "safety",
     "Where does user PDF text go in the messages array, and which tools stay on?",
     "User/untrusted delimiter, never system. Tools off or read-only when answering from user uploads.",
     "role=user; tools=none for trust=upload",
     "Hierarchy + least privilege.", "PDF says ‘ignore’ — you do not."),
    ("Online metric", "easy", "eval",
     "Pick a primary online metric for ‘did the bot resolve the ticket.’",
     "Human-confirmed resolve or user ‘yes’ after 24h without reopen — not thumbs alone. Guard $ and p95.",
     "primary=resolved_no_reopen_24h",
     "Task success.", "Thumbs are noisy."),
    ("Quantize gate", "medium", "prod",
     "You want 4-bit weights to save GPU RAM. Launch checklist?",
     "Run golden suite + a safety slice + p95 latency. Compare to fp16. Canary. Rollback plan.",
     "if eval_drop > 2%: block",
     "Quant is a model change.", "Do not surprise legal/quality."),
    ("Hybrid retrieve", "easy", "rag",
     "When do you add BM25 to vectors? Write a merge idea.",
     "Rare tokens, ids, error codes. Reciprocal rank fusion of both lists, then rerank.",
     "hits = rrf(bm25(q, k=50), knn(q, k=50))[:20]",
     "Lexical + dense.", "RRF is simple and strong."),
    ("Human in the loop", "easy", "design",
     "Which actions must stay human in a billing assistant v1?",
     "Refunds, credit-limit changes, legal commitments, sending as another person. Reads and drafts can be machine.",
     "HUMAN = {'refund','credit','send_as'}",
     "Write the list in the design.", "Autonomy is not a virtue."),
]


def problems() -> str:
    blocks = [_p(i, *row) for i, row in enumerate(P, 1)]
    return f'''
<section class="block" id="problems" data-search="AI engineer exercise bank" data-stype="Section">
  <p class="kicker">{len(P)} mixed exercises</p>
  <h2 class="section-title">Exercise bank</h2>
  <p class="lede">Interview-order mix. Topic gyms (in each lesson) come first for fluency. Practice items — not official company questions.</p>
  <div class="card" style="margin-bottom:16px">
    <p>Filter
      <select id="filter-status">
        <option value="all">All statuses</option>
        <option value="not-started">Not started</option>
        <option value="attempted">Attempted</option>
        <option value="solved">Solved</option>
        <option value="review">Review</option>
        <option value="mastered">Mastered</option>
      </select>
      <select id="filter-cat">
        <option value="all">All categories</option>
        <option value="data">data</option>
        <option value="metrics">metrics</option>
        <option value="ml">ml</option>
        <option value="dl">dl</option>
        <option value="embed">embed</option>
        <option value="prompt">prompt</option>
        <option value="rag">rag</option>
        <option value="finetune">finetune</option>
        <option value="agents">agents</option>
        <option value="eval">eval</option>
        <option value="safety">safety</option>
        <option value="prod">prod</option>
        <option value="mlops">mlops</option>
        <option value="design">design</option>
      </select>
      <input id="filter-text" type="search" placeholder="Filter titles..." />
    </p>
  </div>
  {''.join(blocks)}
</section>
'''
