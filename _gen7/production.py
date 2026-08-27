from util import topic, diagram, callout, code
from drills import serve_gym, mlops_gym, design_gym


def serving() -> str:
    t = topic("sv-cost", "Tokens, time, and the monthly bill",
              "LLM serving streaming batching cache cost", "Lesson", f'''
  <p>You pay for <b>input tokens + output tokens</b> (and sometimes cached input at a discount). A token is a chunk of text — rough English rule: 1 token ≈ 4 characters, but measure.</p>
  {diagram("""User types → maybe cache prefix (system + tools)
          → prefill (read the prompt)  — compute heavy
          → decode (one token at a time) — latency of first token + stream
Batching: many decodes share a GPU. Good for throughput, can hurt p99.""")}
  <ul>
    <li><b>Stream</b> tokens to the UI so TTFT (time to first token) feels fast.</li>
    <li><b>Cache</b> embeddings, retrieval results, and unchanged system prefixes.</li>
    <li><b>Cap</b> max output tokens. Runaways are a cost bug.</li>
    <li><b>Reserve vs on-demand</b> capacity if you self-host.</li>
  </ul>
  {code("Python", '''# Envelope — replace with your prices
def monthly_usd(chats, in_tok, out_tok, price_in, price_out):
    return chats * (in_tok * price_in + out_tok * price_out) / 1000

# 1e6 chats, 800 in, 200 out, $0.50 / $1.50 per 1M tokens
print(monthly_usd(1_000_000, 800, 200, 0.0005, 0.0015))''')}
  <p>Self-hosting: you care about batch size, quantization (smaller weights, some quality loss), and a queue. “We will use vLLM” is not a design unless you say the SLA and the GPU SKU.</p>
  ''', "topics")
    return f'''
<section class="block" id="serve" data-search="LLM serving cost streaming tokens" data-stype="Section">
  <p class="kicker">Runtime</p>
  <h2 class="section-title">Serving and cost</h2>
  <p><a href="#gym-serve">Jump to practice (6) →</a></p>
  {t}
  {serve_gym()}
</section>
'''


def mlops() -> str:
    t = topic("op-ver", "Version everything that changes the answer",
              "MLOps prompt versioning drift rollback", "Lesson", f'''
  <p>A model file is one artifact. An AI feature also has: prompt text, tool schemas, chunker, embedding model id, index build id, ACL rules, and decoding params. If you cannot say which bundle served a request, you cannot debug it.</p>
  {diagram("""request_id
  model_id + prompt_id + index_id + embed_id
  retrieved_ids[]
  tokens_in / tokens_out / $
  user_feedback
Store this. Redact PII. Keep enough to replay.""")}
  <p><b>Drift:</b> input drift (users change), data drift (corpus changes), concept drift (the meaning of “urgent” changes). Monitor retrieval scores, refuse rate, and human escalate rate — not only GPU temperature.</p>
  <p><b>Rollback:</b> prompts and indexes must be one-click reversible. Canary a new prompt on 5% traffic with a kill switch. Training jobs get a model registry and a promotion rule (eval suite must pass).</p>
  {callout("Notebook-to-prod is a smell. The training or ingest job is a pipeline with a SHA. The service reads artifacts, not the data scientist’s laptop.")}
  ''', "topics")
    return f'''
<section class="block" id="mlops" data-search="MLOps versioning drift rollback" data-stype="Section">
  <p class="kicker">Operate</p>
  <h2 class="section-title">MLOps</h2>
  <p><a href="#gym-mlops">Jump to practice (6) →</a></p>
  {t}
  {mlops_gym()}
</section>
'''


def design() -> str:
    t = topic("ds-12", "Twelve steps for an AI design interview",
              "AI system design interview framework", "Lesson", f'''
  <ol>
    <li><b>User and job</b> — who, and what “done” looks like.</li>
    <li><b>Clarify</b> — live vs batch, languages, must-cite, human-in-loop, data residency.</li>
    <li><b>Numbers</b> — QPS, tokens, corpus size, latency budget. Label guesses.</li>
    <li><b>Non-goals</b> — what v1 will not do (multi-agent research, training a foundation model).</li>
    <li><b>Baseline</b> — search, FAQ, classifier. Why a model at all?</li>
    <li><b>Architecture</b> — boxes: client, API, retrieve, model, tools, store.</li>
    <li><b>Data</b> — sources, chunk, ACL, freshness.</li>
    <li><b>Model choice</b> — API vs local, size, multimodal or not.</li>
    <li><b>Eval</b> — golden set, online metric, abuse cases.</li>
    <li><b>Fail</b> — empty retrieve, timeout, unsafe, outage degrade.</li>
    <li><b>Cost and feed</b> — $ / query, cache, observability.</li>
    <li><b>Close</b> — v1, two rejects, one question for the interviewer.</li>
  </ol>
  {callout("At 30 minutes cut novelty, not fail/eval. A pretty agent graph with no metric is a junior board.")}
  <p>Rejected options you should name often: “stuff the whole corpus in context,” “fine-tune to add the wiki,” “unrestricted shell tool,” “accuracy 99% with no unit.”</p>
  ''', "topics")
    return f'''
<section class="block" id="design" data-search="AI system design 12 steps" data-stype="Section">
  <p class="kicker">Interview and work</p>
  <h2 class="section-title">AI system design</h2>
  <p><a href="#gym-design">Jump to practice (6) →</a></p>
  {t}
  {design_gym()}
</section>
'''
