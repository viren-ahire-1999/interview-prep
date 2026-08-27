from util import esc, code

Q = []


def add(level, cat, q, short, deep, miss, follow, snippet=""):
    Q.append(dict(level=level, cat=cat, q=q, short=short, deep=deep, miss=miss, follow=follow, snippet=snippet))


add("fundamentals", "role", "What does an AI engineer own that a research scientist usually does not?",
    "A product path: data contracts, eval, serving, cost, rollback — not a new architecture paper.",
    "You may use models researchers invented. You are hired to make a feature measurable and reversible. In a small company you also train; the center of gravity is still the system.",
    "AI engineer means I train foundation models.",
    "What do you still own if the model is a vendor API?")
add("fundamentals", "role", "When is an if-statement better than a model?",
    "When the rule is known, testable, and legally easier than a score.",
    "Password policy, tax brackets, ‘status == paid’. Models win when the mapping is statistical and labeled. LLMs win when language is the interface — still with a fail path.",
    "AI should replace all rules.",
    "Give a rule you would refuse to replace at your current job.")
add("fundamentals", "data", "What is leakage?",
    "Training on information that would not exist at prediction time.",
    "Time-travel features, test-set statistics, the same user on both sides, the label in disguise. It inflates offline scores and dies in production.",
    "Leakage is when the CSV has a hole.",
    "How do you split a timestamped fraud table?")
add("fundamentals", "data", "Why not shuffle a time series?",
    "Tomorrow leaks into today. Neighbors share weather, campaigns, and seasonality.",
    "Sort by time. Hold out the last weeks. For users, keep a user entirely on one side.",
    "Shuffle is always more ‘random’ so more fair.",
    "What if events are i.i.d. draws with no time?")
add("ml", "models", "Why start with logistic regression?",
    "Fast baseline, readable weights, hard to hide a leak behind depth.",
    "If logistic is close to the bar, you may be done. If it fails, you know the problem needs interactions or more capacity — not that you ‘needed GPT.’",
    "Linear models are obsolete.",
    "When would you skip logistic?")
add("ml", "metrics", "When is accuracy a lie?",
    "Whenever classes or costs are unequal.",
    "99% ‘not fraud’ + always-no = 99% accuracy. Use precision/recall, PR-AUC, or a budgeted threshold. Show the matrix.",
    "Accuracy is the definition of being good.",
    "Pick a metric for a 200-reviews-per-week queue.")
add("ml", "metrics", "Precision vs recall in one product sentence each.",
    "Precision: of what we flagged, how much was real. Recall: of what was real, how much we flagged.",
    "Spam hiding a CEO mail is a precision problem on ‘spam.’ Missing cancer is a recall problem. F1 only if you must have one number.",
    "They are interchangeable.",
    "Who pays for FP in your last product?")
add("ml", "features", "What does L2 regularization do?",
    "It penalizes large weights so the model cannot rely on one crazy feature as easily.",
    "In sklearn, smaller C is stronger L2. Tune on val. Too much L2 underfits.",
    "L2 deletes features (that is closer to L1).",
    "When do you prefer L1?")
add("dl", "nn", "Why a non-linearity between layers?",
    "Otherwise stacked layers collapse to one linear map.",
    "ReLU is the default bend: cheap, reduces vanishing vs deep sigmoids. Then residual connections for very deep stacks.",
    "Non-linearity is just for pretty graphs.",
    "What happens if you initialize badly and all ReLUs die?")
add("dl", "nn", "Backprop in one sentence.",
    "The chain rule assigns each weight its share of the loss so we can step downhill.",
    "Autograd does it. You still need to know vanishing/exploding, learning rate, and train vs eval mode.",
    "Backprop is a second neural net that watches the first.",
    "Name one reason loss goes NaN.")
add("dl", "cnn", "Why convolutions for images?",
    "Local patterns and shared weights — an edge detector works anywhere.",
    "A dense net on megapixels is too many weights and no translation idea. Pooling downsamples; you lose precise location unless you add skips (U-Net).",
    "CNNs are obsolete so skip them.",
    "When is a vision LLM still the wrong v1?")
add("dl", "transformers", "What is self-attention doing?",
    "Each token mixes others, weighted by query–key similarity.",
    "Q looks, K is looked-up, V is what gets mixed. Causal mask stops peeking. Multi-head lets several mix patterns exist. Residual + MLP complete a block.",
    "Attention means the model is ‘paying attention’ like a human.",
    "Why divide by sqrt(d_k)?")
add("dl", "transformers", "What is a context window, really?",
    "How many tokens fit in the model’s attention / memory for that call.",
    "Longer → more $ and compute (steep in T). It is not a license to dump the company drive. Retrieval still wins for ACL and freshness.",
    "Context window is RAM on the GPU only.",
    "Why can the model still ignore the middle of a long prompt?")
add("genai", "embed", "What is an embedding?",
    "A vector placed so similar items are nearby in cosine/dot geometry.",
    "You store them, search ANN, keep the original text. Close ≠ correct. Changing the embed model invalidates the index.",
    "Embeddings are encrypted meanings.",
    "Why filter by tenant in the index, not in the prompt?")
add("genai", "llm", "Pretrain vs SFT vs preference — one line each.",
    "Pretrain: next token on a huge mix. SFT: follow instructions. Preference: rank nicer/safer answers.",
    "You live in the last mile: prompts, tools, RAG, maybe a small extra tune. You rarely rerun pretrain.",
    "ChatGPT is only SFT.",
    "Why is a base model a bad user-facing bot?")
add("genai", "llm", "API vs self-host — the decision?",
    "API for speed and quality; self-host for residency or favorable unit economics you can operate.",
    "Read the DPA. Measure on your eval. ‘We will beat the API on two GPUs’ without numbers is a fantasy.",
    "Self-host is always cheaper.",
    "What staff do you need to self-host?")
add("genai", "prompt", "What makes a good system prompt?",
    "A short contract: role, sources, refuse, output shape, escalation.",
    "Examples beat adjectives. Untrusted text is delimited. Schema is validated. ‘Be helpful’ is not a spec.",
    "Longer prompts are always better.",
    "Rewrite a vibe prompt you have seen.")
add("genai", "prompt", "What is prompt injection, in product terms?",
    "Untrusted text tries to override your instructions or abuse tools.",
    "You do not ‘solve’ it with please. Delimit, least-privilege tools, never put uploads in system, eval with hostile strings. This course does not teach attack recipes.",
    "Injection is SQL only.",
    "Where do you put a user PDF?")
add("genai", "rag", "What is RAG, and what does it not do?",
    "Retrieve your text, generate from it, cite, refuse. It does not make the model truthful or skilled at new math.",
    "Chunk, embed, filter ACL, top-k, rerank, allow-list cites. Two evals: retrieval and generation. Stale indexes are a product bug.",
    "RAG is fine-tuning on documents.",
    "Why hybrid search?")
add("genai", "rag", "How do you know the model used the excerpts?",
    "You never fully know. You require cites from an allow-list and spot-check support; you measure unsupported answers.",
    "Faithfulness metrics and humans. If cites are missing, fail the item. Do not trust fluent restatements.",
    "If it sounds grounded it is grounded.",
    "What if the cite id was not retrieved?")
add("genai", "finetune", "When do you fine-tune vs RAG?",
    "RAG for facts that change. Fine-tune for stable style or a narrow skill with enough clean pairs.",
    "LoRA makes adapters cheap to store. Do not SFT 30 rows. Do not SFT the wiki. Keep a prompt-only baseline.",
    "Fine-tune whenever quality is not 100%.",
    "What is catastrophic forgetting?")
add("genai", "agents", "Chain vs agent?",
    "A chain is a fixed pipeline. An agent may choose tools and repeat until a halt.",
    "Prefer a graph when you can draw the steps. Agents need caps, typed tools, and no shell/SQL. Destructive actions want a human.",
    "Agents are just smarter prompts.",
    "Name four halt conditions.")
add("genai", "eval", "What is a golden set?",
    "A versioned list of inputs with expected properties, used like unit tests.",
    "Include refuse, ACL, injection, tables, empty retrieve. Run in CI. Do not put the set in SFT train. LLM-as-judge is optional and biased.",
    "Golden set is the demo script.",
    "Name two automatic checks that are not a judge.")
add("genai", "eval", "Why not only LLM-as-judge?",
    "Judges like long fluent answers, can be gamed, and must be calibrated to humans.",
    "Use them to scale, with order swaps and a human sample. Launch still needs task metrics and safety slices.",
    "Judges are objective.",
    "What is position bias?")
add("genai", "safety", "Is the model your authorization layer?",
    "No. Retrieval and tools enforce ACL in code.",
    "Prompts are bypassable. Logs need redaction. High-stakes domains escalate. Measure over-refusal too.",
    "A strong system prompt is enough security.",
    "What must not go into a SaaS trace?")
add("prod", "serve", "What is a token for billing?",
    "A chunk of text the vendor counts on the way in and out — not exactly a word.",
    "Rough 4 characters/token in English. Measure. Cache and max_output cut the bill. Retries and agent steps multiply it.",
    "A token is a GPU.",
    "Estimate $ for 1M chats given prices.")
add("prod", "serve", "TTFT vs total latency?",
    "TTFT is time to first token — the ‘is it alive’ feeling. Total includes the full answer and tools.",
    "Stream, cache prefixes, shrink prompts. Batching helps throughput and can hurt p99 if you wait for a full batch.",
    "Only total time matters.",
    "How can batching make interactive users sad?")
add("prod", "mlops", "What do you version besides weights?",
    "Prompt, tools, chunker, embed id, index build, decode params, eval hash.",
    "Log the bundle on every request so you can replay. Canary prompts. Rollback is a switch, not a meeting.",
    "Git on the training script is enough.",
    "Write a canary plan for prompt v17.")
add("prod", "mlops", "Name three drifts.",
    "Input (users change), data (corpus changes), concept (the meaning of the label changes).",
    "Watch retrieve scores, refuse, escalate, not only GPU heat. A wiki migration is a common ‘model got worse’ that is actually an index.",
    "Drift is only covariate shift from a textbook.",
    "What alert would have caught a nightly index that failed?")
add("prod", "design", "What do you not cut at minute 30 of a design?",
    "Eval, fail/degrade, ACL, and a scoped v1.",
    "Cut multi-agent, training a foundation model, and extra tools. Close with rejects and a question.",
    "Cut the boring reliability so you can draw more boxes.",
    "Give two rejects for wiki-chat.")
add("judgment", "role", "The model is wrong in a fluent sentence. What do you tell a PM?",
    "Fluency is not a guarantee. We need a metric, a refuse path, and a human path.",
    "Demos lie. Golden sets and online task success are how you argue. Do not add another agent layer as the first fix.",
    "We will fine-tune until it never errs.",
    "What is the cheapest experiment this week?")
add("judgment", "rag", "Retrieval is good, answers are still unsupported. Next?",
    "Prompt/cite rules, shorter context, stronger extractive style, or a smaller specialist — not a bigger k.",
    "Measure faithfulness separately. Maybe the generator is too large/creative (lower temperature, schema).",
    "Always raise k.",
    "When do you add a reranker?")
add("judgment", "finetune", "120 labeled tickets. Fine-tune 7B?",
    "No. Prompt a strong model or train a tiny classifier. 120 rows is an eval set.",
    "SFT needs volume and cleanliness. Otherwise you overfit and call it a launch.",
    "Small data is why we use small models — so SFT is fine.",
    "How many clean pairs would make you consider LoRA for tone?")
add("judgment", "agents", "PM wants ‘a swarm of agents.’ Your default?",
    "One workflow, two tools, a halt. Swarms are a last resort.",
    "Coordination cost, $ , and failure modes grow faster than quality. Draw the known steps first.",
    "More agents are more intelligence.",
    "When is a second agent actually justified?")
add("fundamentals", "python", "What does shape (B, T, D) mean?",
    "Batch of sequences, each of length T, each token a D-vector.",
    "Check shapes after every line. Broadcasting aligns from the right. Flattening B and T by accident is a silent bug.",
    "It is width × height × color.",
    "How do you add a per-batch bias to (B,T,D)?")
add("ml", "models", "Trees vs linear — who wins interactions?",
    "Trees can split on feature A then B without you multiplying them. Linear needs the interaction feature.",
    "Linear wins on tiny n, strict explanations, or when the world really is linear after good features.",
    "Boosting always wins tabular so skip linear.",
    "When is n=800 a reason to avoid a deep net?")
add("dl", "transformers", "Encoder vs decoder?",
    "Encoder may look both ways (understand). Decoder LM looks left only (generate).",
    "Chat/instruct models you call are decoder-style generators. Bidirectional encoders still exist for retrieval and classify.",
    "They are the same stack with different logos.",
    "Why a causal mask at train time?")
add("genai", "embed", "Can you reuse an index after changing embed models?",
    "No. Rebuild. Version embed_model_id.",
    "Spaces are incompatible. The query encoder must match the document encoder generation.",
    "Just re-embed the query with the new model against old docs.",
    "How do you migrate without downtime?")
add("prod", "serve", "What do you cache in RAG?",
    "Doc embeddings, public retrieval, stable prefixes. Personalized answers only with ACL in the key and a TTL.",
    "Wrong keys leak tenants or stale policy. Measure hit rate.",
    "Cache the final answer globally for the same question string.",
    "Write a safe cache key.")
add("genai", "safety", "Over-refusal vs under-refusal?",
    "Over: refuses password reset. Under: invents a drug dose. Measure both.",
    "Golden slices for must-answer and must-refuse. Kind tone can still refuse.",
    "Safer always means more refuses.",
    "Give one must-answer and one must-refuse for HR.")
add("prod", "design", "What numbers do you guess out loud?",
    "QPS, corpus/chunks, latency budget, $ / 1k queries, golden set size. Label them guesses.",
    "Silence is worse. Ask the interviewer to correct. Those numbers fork RAG vs stuff-context vs self-host.",
    "Only QPS matters, like a backend design.",
    "Guess them for a 2,000-person company wiki.")
add("fundamentals", "data", "What is label noise doing to your ceiling?",
    "If raters disagree 20%, 99% accuracy is a fantasy.",
    "Measure agreement, build a gold subset, drop sloppy items. A bigger model will fit the noise.",
    "More layers average out label errors.",
    "What statistic would you quote for rater agreement?")
add("ml", "metrics", "ROC-AUC 0.93 and the business is unhappy. Why?",
    "AUC ignores the operating point and the review budget.",
    "You may flag 30% of users. Report precision at the real threshold and the cost.",
    "AUC is the only adult metric.",
    "When is PR-AUC more honest than ROC-AUC?")
add("genai", "rag", "What is lost-in-the-middle?",
    "Models use the start and end of a long prompt more than the middle.",
    "So dumping 20 chunks can hide the one that matters. Rerank into a short pack; put the best evidence where the model actually looks — and measure.",
    "Longer prompts always help.",
    "How would you test for it?")
add("genai", "agents", "Why is run_sql a bad tool?",
    "Injection, exfiltration, accidental DELETE, no ACL.",
    "Ship get_order(id) with parameterized SQL inside your code. The model never sees a query string.",
    "The model is good at SQL so it is fine.",
    "How do you make a charge tool idempotent?")
add("prod", "mlops", "Notebook-to-prod — why a smell?",
    "No SHA, no replay, no owner, no rollback.",
    "Jobs produce versioned artifacts. The service reads the registry. Colab is an experiment, not a release.",
    "If it ran once it can run forever.",
    "What belongs in a model registry record?")
add("judgment", "eval", "Demo looked great. Why is that not a launch?",
    "Demos are cherry-picked. You need a pre-registered metric and a suite that includes ugly cases.",
    "Add abandons to the golden set. Watch online task success. Canary.",
    "If leadership clapped, ship.",
    "What ugly cases were missing from the last demo you saw?")
add("fundamentals", "role", "Do you need a PhD to be an AI engineer?",
    "No. You need software engineering, data hygiene, eval, and honesty about limits.",
    "A PhD helps for novel modeling. Most product AI is RAG, tools, and classical ML with discipline.",
    "Without a PhD you can only write prompts.",
    "What skill gap would actually block you next quarter?")
add("genai", "llm", "What does temperature do?",
    "Higher → more random next-token samples. Lower → greedy/peaky.",
    "Use low for extract/classify. Do not raise temperature to ‘fix facts’ — retrieve facts.",
    "Temperature is how smart the model is.",
    "What decoding would you use for JSON?")
add("dl", "nn", "Train vs eval mode — why?",
    "Dropout and batch-norm behave differently. Inference uses eval().",
    "Leaving dropout on at serve time injects noise. A common silent bug.",
    "They are the same if you do not use dropout.",
    "What is MC-dropout and why is it not the default?")
add("prod", "serve", "Why cap max output tokens?",
    "A bug or a loop can write a novel and empty the budget.",
    "Also timeout, $ breaker, stop sequences. Retries multiply spend.",
    "The model will stop when it is done.",
    "What else multiplies cost besides output length?")
add("genai", "rag", "Why store as-of on an answer?",
    "Policies change. Users (and auditors) need to know which version was retrieved.",
    "Index build id + document updated_at in the footer. Critical docs get a faster ingest than nightly.",
    "The model knows what is current.",
    "How fast must a legal page go live in your company?")
add("judgment", "design", "Name two designs you reject for ‘AI search.’",
    "Chat over every SKU; fine-tune on the catalog instead of indexing it.",
    "v1 is search quality (keywords, filters, rank). LLM rewrite is a later experiment with an IR metric.",
    "Search is solved so we only need GPT.",
    "What IR metric would you put on the poster?")
add("ml", "features", "Why is raw user_id a bad numeric feature?",
    "Trees memorize identities. Production sees new ids.",
    "Use behavior aggregates or a proper embedding with a rare-id bucket — not the integer id.",
    "IDs are just numbers so the forest can split them.",
    "What would you use instead for ‘this user churned last year’?")
add("genai", "safety", "Who is allowed to see prompt logs?",
    "A small, audited group; redacted; short retention.",
    "Treat logs as production data. Vendor APM is another copy. Slack is not a store.",
    "Engineers need raw everything to debug, forever.",
    "How would you debug RAG without raw PII?")
add("prod", "design", "How do you close a 45-minute AI design?",
    "v1, two rejects, metric, fail path, one question.",
    "Twenty seconds. Like a colleague, not a TED talk. Then stop talking.",
    "List every library you have heard of.",
    "Close wiki-chat in one breath.")


def feq() -> str:
    blocks = []
    for i, item in enumerate(Q, 1):
        snip = code("Python", item["snippet"]) if item["snippet"] else ""
        blocks.append(f'''
<article class="q" id="feq-{i}" data-level="{item["level"]}" data-cat="{item["cat"]}" data-search="{esc(item["q"])}" data-stype="Interview question" data-mock="1">
  <div class="meta-row"><span class="badge badge-js">{item["level"]}</span><span class="chip">{item["cat"]}</span><span class="chip">Q{i}</span></div>
  <h3>{i}. {esc(item["q"])}</h3>
  <p><button type="button" class="toggle-btn" data-toggle="feq-a-{i}">Reveal answer</button>
     <button type="button" class="toggle-btn" data-complete="questions" data-cid="feq-{i}">Mark complete</button></p>
  <div class="reveal" id="feq-a-{i}">
    <p><b>Short answer.</b> {item["short"]}</p>
    <p><b>Deep explanation.</b> {item["deep"]}</p>
    {snip}
    <p><b>Common misconception.</b> {item["miss"]}</p>
    <p><b>Follow-up.</b> {item["follow"]}</p>
  </div>
</article>''')
    return f'''
<section class="block" id="feq" data-search="AI engineer interview questions" data-stype="Section">
  <p class="kicker">{len(Q)} questions</p>
  <h2 class="section-title">Interview Q&amp;A</h2>
  <p class="lede">Answer standing up. Mark complete only if you can teach the short answer. Practice questions — not official company lists.</p>
  <div class="tabs" data-tabs="feq">
    <button type="button" class="tab active" data-tab="all">All ({len(Q)})</button>
    <button type="button" class="tab" data-tab="fundamentals">fundamentals</button>
    <button type="button" class="tab" data-tab="ml">ml</button>
    <button type="button" class="tab" data-tab="dl">dl</button>
    <button type="button" class="tab" data-tab="genai">genai</button>
    <button type="button" class="tab" data-tab="prod">prod</button>
    <button type="button" class="tab" data-tab="judgment">judgment</button>
  </div>
  {''.join(blocks)}
</section>
'''
