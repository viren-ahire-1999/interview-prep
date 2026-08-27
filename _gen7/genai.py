from util import topic, diagram, callout, code
from drills import embed_gym, llm_gym, prompt_gym, rag_gym, ft_gym, agent_gym, eval_gym, safety_gym


def embeddings() -> str:
    t = topic("em-geo", "Meaning as nearby points",
              "embeddings cosine vector database ANN", "Lesson", f'''
  <p>An <b>embedding</b> is a vector the model learned so that similar items (sentences, images, users) land nearby. You store them and search with cosine or dot product.</p>
  {diagram("""‘refund policy’  ●
                  \\
                   ●  ‘how do I get my money back’
far away:  ● ‘office address’
Index: skip scanning all rows — ANN (HNSW, IVF) ≈ nearest neighbors""")}
  <p>A <b>vector database</b> (or pgvector, or an in-memory index) stores vectors + metadata filters (tenant, date, acl). Approximate nearest neighbor (ANN) trades a tiny recall loss for speed. Always keep the original text chunk beside the vector — you will show it to the LLM and to humans.</p>
  {code("Python", '''# Shape story only — swap in your vendor embedder
import numpy as np

def l2_normalize(x):
    n = np.linalg.norm(x, axis=-1, keepdims=True)
    return x / (n + 1e-12)

q = l2_normalize(query_vec[None, :])          # (1, D)
hits = (chunks_norm @ q.T).ravel()            # (N,)
top = np.argsort(-hits)[:8]''')}
  {callout("Embeddings are not facts. Two chunks can be ‘close’ and still wrong for the question. Retrieval is a candidate generator. The generator can still hallucinate.")}
  ''', "topics")
    return f'''
<section class="block" id="embed" data-search="embeddings vector database cosine" data-stype="Section">
  <p class="kicker">Geometry</p>
  <h2 class="section-title">Embeddings and vectors</h2>
  <p><a href="#gym-embed">Jump to practice (6) →</a></p>
  {t}
  {embed_gym()}
</section>
'''


def llms() -> str:
    t = topic("lm-life", "How a chat model is born (simplified)",
              "pretrain SFT RLHF instruction tuning context window", "Lesson", f'''
  <ol>
    <li><b>Pretrain</b> — next-token prediction on a huge corpus. Learns language, some facts, some garbage.</li>
    <li><b>Supervised fine-tune (SFT)</b> — show (prompt, good answer) pairs so it follows instructions.</li>
    <li><b>Preference / RLHF / similar</b> — rank answers so it prefers helpful, harmless style. Details vary by lab.</li>
    <li><b>You</b> — prompts, tools, RAG, or a small extra fine-tune on <i>your</i> distribution.</li>
  </ol>
  <table>
    <tr><th>Choice</th><th>Take when</th><th>Pay</th></tr>
    <tr><td>Hosted API</td><td>Speed to product, strong general model</td><td>Data leaves your box (read the DPA), $ / token, rate limits</td></tr>
    <tr><td>Open weights via API</td><td>Portability, sometimes cheaper</td><td>You still trust a host</td></tr>
    <tr><td>Self-host</td><td>Strict residency, custom weights, stable unit cost at scale</td><td>GPUs, batching, on-call</td></tr>
  </table>
  <p><b>Context window:</b> the working memory in tokens (pieces of text, not always words). Stuffing a 200-page PDF into the prompt is not RAG — it is a bill and a lost-middle problem.</p>
  {callout("Temperature: higher → more random samples. Use low temperature for extraction and classification. Do not ‘turn it up’ to fix facts — retrieve facts.")}
  ''', "topics")
    return f'''
<section class="block" id="llms" data-search="LLM pretrain SFT API vs self host" data-stype="Section">
  <p class="kicker">The product model</p>
  <h2 class="section-title">LLM landscape</h2>
  <p><a href="#gym-llm">Jump to practice (6) →</a></p>
  {t}
  {llm_gym()}
</section>
'''


def prompting() -> str:
    t = topic("pr-contract", "A prompt is an API contract",
              "system prompt few-shot structured output tools", "Lesson", f'''
  <p>Treat the model like a junior teammate with no memory of your company. Specify <b>role, output shape, allowed tools, and what to do when unsure</b>.</p>
  {code("text", '''SYSTEM
You are an assistant for Acme billing.
Answer only from the provided excerpts.
If excerpts are empty or irrelevant, say you do not know
and offer a human ticket.
Return JSON: {{ "answer": string, "cite_ids": string[], "refuse": boolean }}

USER
Question: ...
Excerpts:
[doc-12] ...
[doc-19] ...''')}
  <ul>
    <li><b>System</b> — standing rules. Keep it short; long constitutions get ignored.</li>
    <li><b>Few-shot</b> — 2–5 real examples of the format you want. Better than adjectives (“be concise”).</li>
    <li><b>Structured output</b> — JSON schema / constrained decode when a machine will parse it.</li>
    <li><b>Chain of thought</b> — useful for math-like tasks; do not blindly show hidden reasoning to users; it can leak.</li>
    <li><b>Tool calls</b> — the model returns a function name + args; <i>you</i> run the function.</li>
  </ul>
  <p>Failure modes: prompt injection (untrusted document says “ignore rules”), format drift, verbosity, agreeing with a wrong user premise. Mitigate with: untrusted text clearly delimited, schema validation, and retrieval allow-lists — not with “please be safe” alone.</p>
  ''', "topics")
    return f'''
<section class="block" id="prompt" data-search="prompt engineering system few-shot JSON" data-stype="Section">
  <p class="kicker">Interface</p>
  <h2 class="section-title">Prompting</h2>
  <p><a href="#gym-prompt">Jump to practice (6) →</a></p>
  {t}
  {prompt_gym()}
</section>
'''


def rag() -> str:
    t1 = topic("rg-pipe", "Retrieval-augmented generation",
               "RAG chunk embed retrieve cite refuse", "Lesson", f'''
  <p>RAG means: find relevant company text (or tickets, or code), put it in the prompt, ask the model to answer <i>from that</i>. It does not make the model truthful. It makes the model <b>groundable</b>.</p>
  {diagram("""ingest → chunk → embed → index
query  → embed → retrieve top-k (+ rerank)
       → prompt(system + excerpts + question)
       → answer + citations
       → if weak hits: refuse / ask clarify / ticket""")}
  <p><b>Chunking:</b> too small → no context. too large → diluted similarity and fat prompts. Start ~400–800 tokens with 10–20% overlap, then measure. Split on headings for policies; on functions for code.</p>
  <p><b>Metadata filters</b> (space, time, ACL) happen <i>before</i> or with the vector search. A user must not retrieve another tenant’s chunk.</p>
  {code("Python", '''def answer(question, index, acl):
    hits = index.search(question, k=8, filter=acl)
    hits = [h for h in hits if h.score >= MIN]
    if len(hits) < 2:
        return {{"refuse": True, "answer": "I do not have enough policy text."}}
    prompt = build_prompt(question, hits)
    out = llm.generate(prompt)
    return validate_cites(out, allowed={{h.id for h in hits}})''')}
  {callout("<b>What RAG does not fix.</b> Wrong corpus, stale index, ambiguous question, model ignoring excerpts, or a task that needs multi-step tools (then you need an agent or a workflow).")}
  ''', "topics")

    t2 = topic("rg-fail", "RAG breaks in boring, testable ways",
               "RAG failure modes stale index citation", "Lesson", f'''
  <ul>
    <li>Chunk cut a table in half → retrieval of nonsense. Test with table-heavy pages.</li>
    <li>Index rebuilt weekly, policy changed today → confident old answer. Version documents; show “as of”.</li>
    <li>Citations invented. Only allow IDs you injected; strip the rest.</li>
    <li>Top-k is 20 and the answer is in #19 — the model never reads that far. Rerank; or pack fewer, better chunks.</li>
    <li>Query is slang, chunk is legal English — hybrid search (keyword + vector) often wins.</li>
  </ul>
  <p>Eval RAG in two layers: <b>retrieval</b> (was the needed chunk in top-k?) and <b>generation</b> (was the answer supported?). Do not average them into one vanity score on day one.</p>
  ''', "topics")

    return f'''
<section class="block" id="rag" data-search="RAG retrieval augmented generation chunking" data-stype="Section">
  <p class="kicker">Your data in the prompt</p>
  <h2 class="section-title">RAG</h2>
  <p><a href="#gym-rag">Jump to practice (8) →</a></p>
  {t1}{t2}
  {rag_gym()}
</section>
'''


def finetune() -> str:
    t = topic("ft-when", "Change weights only when the contract is style or a narrow skill",
              "fine-tuning LoRA SFT when not to fine-tune", "Lesson", f'''
  <p><b>Fine-tuning</b> continues training so the model’s weights shift toward your examples. <b>LoRA</b> (and friends) train small adapter matrices instead of the full net — cheaper, easier to swap.</p>
  <p>Fine-tune when:</p>
  <ul>
    <li>You need a stable <b>format or tone</b> that prompting still misses after good examples.</li>
    <li>A <b>narrow specialist</b> skill (classify tickets into your 40 codes) and you have hundreds of clean labels.</li>
    <li>You must run a <b>smaller</b> model on-prem and recover quality.</li>
  </ul>
  <p>Do <b>not</b> fine-tune to “add facts.” Facts go stale; use RAG. Do not fine-tune on 30 rows. Do not fine-tune to fix a broken eval — you will overfit the eval.</p>
  {diagram("""Need new facts?          RAG / tools
Need tools / workflow?   Agent or graph
Need style / schema?     Prompt + schema first
Still failing + data?    Then LoRA / SFT""")}
  {callout("Data quality dominates. A dirty SFT set teaches your mess at higher confidence. Dedup, have a held-out eval that is not in train, and keep a prompt-only baseline so you know you bought something.")}
  ''', "topics")
    return f'''
<section class="block" id="finetune" data-search="fine-tuning LoRA when to fine-tune" data-stype="Section">
  <p class="kicker">Weights</p>
  <h2 class="section-title">Fine-tuning</h2>
  <p><a href="#gym-ft">Jump to practice (6) →</a></p>
  {t}
  {ft_gym()}
</section>
'''


def agents() -> str:
    t = topic("ag-loop", "An agent is a loop with tools and a stop",
              "AI agents tools function calling halt", "Lesson", f'''
  <p>A <b>chain</b> is a fixed pipeline (retrieve → answer). An <b>agent</b> may choose tools, see results, and repeat. That power is also how it loops, spends money, or calls <code>delete</code>.</p>
  {diagram("""while steps < N and not done:
  model → (final answer) OR (tool name + args)
  if tool: run tool in YOUR sandbox → append result
halt: N steps, $ cap, timeout, user cancel, policy deny""")}
  <p>Tools should be <b>narrow, typed, and permissioned</b>. “Run any SQL” is not a tool; “fetch_order(id)” is. Idempotent tools are easier. Confirm destructive actions with a human.</p>
  <p>Memory: the conversation is enough for v1. Long-term memory is another index (RAG over past tickets) — not an unbounded scratchpad that never expires.</p>
  {callout("<b>Default to a workflow.</b> If you can draw the steps (classify → retrieve policy → draft → human), a graph beats a free-roam agent. Use an agent when the next step is truly unknown.")}
  ''', "topics")
    return f'''
<section class="block" id="agents" data-search="AI agents tools function calling" data-stype="Section">
  <p class="kicker">Loops</p>
  <h2 class="section-title">Agents</h2>
  <p><a href="#gym-agent">Jump to practice (6) →</a></p>
  {t}
  {agent_gym()}
</section>
'''


def evaluation() -> str:
    t = topic("ev-gold", "If you cannot score it, you cannot ship it",
              "LLM evaluation golden set LLM-as-judge online metrics", "Lesson", f'''
  <p>A <b>golden set</b> is a versioned list of inputs plus an expected property: exact answer, must-cite doc, must-refuse, or a rubric. Start with 30–50 hard cases from real users, not 3 complimentary demos.</p>
  <ul>
    <li><b>Automatic:</b> exact match, regex, JSON schema valid, retrieval hit-rate, citation validity.</li>
    <li><b>Human:</b> spot-check on a rubric (correct / unsupported / harmful / useless).</li>
    <li><b>LLM-as-judge:</b> useful for scale, biased toward long and fluent, must be calibrated against humans, and must not grade its own homework only.</li>
    <li><b>Online:</b> thumbs, retry rate, escalation to human, latency, cost, deflection.</li>
  </ul>
  {code("Python", '''def score_item(item, out):
    checks = {{
        "schema": valid_json(out),
        "cites_allowed": set(out["cite_ids"]) <= item["allowed_ids"],
        "refuse_ok": out["refuse"] == item["should_refuse"],
    }}
    return checks''')}
  <p>Split eval so prompt tweaks cannot silently overfit. Re-run the suite on every prompt, index, and model bump — that is your unit test.</p>
  {callout("A/B tests need a primary metric chosen in advance. ‘We liked the vibe’ is not a launch criterion.")}
  ''', "topics")
    return f'''
<section class="block" id="eval" data-search="evaluate LLM golden set judge" data-stype="Section">
  <p class="kicker">Proof</p>
  <h2 class="section-title">Evaluation</h2>
  <p><a href="#gym-eval">Jump to practice (6) →</a></p>
  {t}
  {eval_gym()}
</section>
'''


def safety() -> str:
    t = topic("sf-min", "Safety is product, not a sticker",
              "AI safety PII prompt injection copyright escalation", "Lesson", f'''
  <p>You will not “solve alignment” in this course. You will ship fewer disasters.</p>
  <ul>
    <li><b>PII and secrets</b> — do not log raw prompts that contain tokens, health data, or customer dumps. Redact. Encrypt. Retention limits.</li>
    <li><b>Access control</b> — retrieval uses the caller’s ACL. The model is not your authorization layer.</li>
    <li><b>Untrusted text</b> — tickets and PDFs can say “ignore the system prompt.” Delimit them; never concatenate blindly into system.</li>
    <li><b>Copyright and training data</b> — do not paste licensed code into a public model if policy forbids it. Cite internal docs; do not claim the model “wrote original law.”</li>
    <li><b>Over-refusal vs under-refusal</b> — measure both. A bot that never answers is safe and useless.</li>
    <li><b>Human escalation</b> — medical, legal, credit, self-harm adjacent: route to a human and a policy. Do not invent treatments.</li>
  </ul>
  {callout("This course does not teach attacks. If you test robustness, do it on systems you own, with a written scope, and record the fix — not a public recipe.")}
  ''', "topics")
    return f'''
<section class="block" id="safety" data-search="AI safety PII injection copyright" data-stype="Section">
  <p class="kicker">Do no fluent harm</p>
  <h2 class="section-title">Safety</h2>
  <p><a href="#gym-safety">Jump to practice (6) →</a></p>
  {t}
  {safety_gym()}
</section>
'''
