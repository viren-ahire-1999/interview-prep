from util import topic, code, callout


def _study(cid, title, search, problem, approach, snippet, product, trap):
    return topic(cid, title, search, "Practical study", f'''
  <p><b>Problem.</b> {problem}</p>
  <p><b>Approach.</b> {approach}</p>
  {code("Python", snippet)}
  <p><b>Where this shows up.</b> {product}</p>
  <p><b>Trap.</b> {trap}</p>
  ''', "reactTopics")


def practical() -> str:
    items = [
        _study("ps-clf", "Tabular classifier that can ship",
               "churn classifier practical AI",
               "Predict 30-day churn from subscription events. Reviewers can only call 200 users/week.",
               "Time split. Logistic or forest baseline. Metric: precision@200 (or expected $). Threshold from val. No LLM.",
               '''# sketch
pipe.fit(X_train, y_train)
scores = pipe.predict_proba(X_val)[:, 1]
# pick threshold so we flag ~200 per week on historical volume
''',
               "Churn, fraud review queues, lead scoring.",
               "Optimizing AUC and then ignoring the 200-call budget."),
        _study("ps-search", "Search before a chatbot",
               "learning to rank vs RAG search",
               "Users cannot find SKUs. PM says ‘add ChatGPT search.’",
               "v1: keyword + filters + click logs. v2: query rewrite with an LLM only if v1 misses. Measure NDCG or purchase rate, not ‘answers felt smart.’",
               '''# rewrite is optional
q2 = llm.rewrite(q) if search(q).empty else q
return search(q2)
''',
               "E-commerce, docs site, ticket search.",
               "Chatting every catalog row."),
        _study("ps-rag", "Policy Q&A with citations",
               "RAG support bot practical",
               "Employees ask HR/policy questions. Wrong answers are worse than no answer.",
               "Chunk by heading, hybrid retrieve, cite allow-list, refuse on weak hits, golden set of must-refuse and must-cite. ACL on space.",
               '''def ask(q, user):
    hits = retrieve(q, acl=user.acl, k=8)
    if not hits or hits[0].score < MIN:
        return refuse()
    return generate_with_cites(q, hits)
''',
               "HR, security policy, internal wiki.",
               "Fine-tuning the wiki; stuffing the PDF."),
        _study("ps-agent", "Order-status assistant",
               "agent tools get_order practical",
               "User wants order status and a policy quote. Refunds exist as a temptation.",
               "Tools: get_order(id), search_docs. Refund is a human ticket. Max 6 steps. Idempotent reads only.",
               '''TOOLS = ["get_order", "search_docs", "create_ticket"]
# never run_sql, never refund_charge
''',
               "Support, logistics, SaaS billing.",
               "Open-ended SQL and silent refunds."),
        _study("ps-eval", "Eval harness in CI",
               "golden set CI prompts",
               "Prompt edits ship from a wiki with no tests. Quality flaps weekly.",
               "Versioned JSONL goldens. CI runs retrieve+generate checks. Deploy blocked on drop. Weekly human sample.",
               '''def test_must_refuse():
    for row in goldens:
        if row["should_refuse"]:
            assert run(row["q"])["refuse"]
''',
               "Any prompt-driven feature.",
               "LLM-as-judge as the only gate."),
        _study("ps-cost", "Cost incident",
               "LLM cost spike incident",
               "Overnight token spend 4×. No traffic spike.",
               "Check output length, agent steps, retries, cache hit, last prompt_id. Kill switch. Roll back prompt. Cap max_tokens.",
               '''# dashboards
# p95 tokens_out, tool_steps, retry_count, prompt_id
''',
               "Any metered API.",
               "Looking only at GPU graphs when you use a hosted API."),
        _study("ps-ft", "Tone adapter vs RAG",
               "LoRA vs RAG decision practical",
               "Brand wants a fixed four-line sign-off. Facts stay in the CMS.",
               "Constrained template first. If still failing, LoRA on style pairs. Facts remain RAG. Two artifacts: adapter + index.",
               '''# do not SFT the CMS
# SFT examples: (user, four-line branded reply) with placeholders
''',
               "Brand voice, classification heads.",
               "One fine-tune that tries to hold all facts."),
        _study("ps-mm", "Screenshot tickets",
               "vision OCR vs multimodal LLM",
               "Users attach a screenshot of an error dialog.",
               "v1: OCR + existing keyword/RAG on extracted text. v2: vision LLM if OCR fails (dark UI, tiny font). Measure resolve rate.",
               '''text = ocr(image)
if text.strip():
    return rag(text)
return vision_llm(image, prompt="extract the error code")
''',
               "Support, QA, accessibility.",
               "Vision LLM on every image when the text is already there."),
        _study("ps-offline", "Offline + online pair",
               "offline golden online thumbs",
               "Offline suite is 96% ‘good.’ Users still abandon.",
               "Define task success (order found, ticket created). Track abandon and escalate. Sample failures into the golden set monthly.",
               '''# monthly: pull 50 abandons → label → add to goldens
''',
               "Every consumer chatbot.",
               "Declaring victory on a static 40-item set."),
        _study("ps-pii", "Redacted traces",
               "PII redaction LLM logs",
               "You need traces to debug RAG but legal forbids raw health text in the vendor APM.",
               "Redact before export. Store full text in a locked store with short TTL. Traces keep chunk ids + hashes.",
               '''safe = redact(prompt)
trace.write(safe, chunk_ids=ids, bundle=bundle_id)
''',
               "Health, fintech, HR.",
               "Pasting live prompts into Slack to debug."),
        _study("ps-canary", "Prompt canary",
               "canary prompt deploy",
               "A well-meaning teammate edited the system prompt in the admin UI.",
               "Prompts are immutable ids in git. Canary 5%. Auto-rollback on refuse-rate or $ guardrail.",
               '''# feature flag: prompt_id
# if guardrail_breach: serve previous id
''',
               "Any multi-person team.",
               "Hot-editing prod with no diff."),
        _study("ps-design", "45-minute wiki design",
               "AI system design wiki practical",
               "Interviewer: design ChatGPT on our Confluence.",
               "12 steps. v1 RAG+cite+refuse. Numbers labeled guesses. Reject SFT-wiki and full-space dump. Close with metric + ACL question.",
               '''# speak: user, NFR, baseline, boxes, data, model, eval, fail, $, close
''',
               "Design interviews and kickoff docs.",
               "Drawing an agent mesh and skipping eval."),
    ]
    return f'''
<section class="block" id="practical" data-search="AI engineer practical studies" data-stype="Section">
  <p class="kicker">12 product-shaped studies</p>
  <h2 class="section-title">Practical studies</h2>
  <p class="lede">Each study is a thing you might ship. Write the v1 on paper, then reveal. Mark complete only if you can teach the trap.</p>
  {callout("These are teaching scenarios, not case studies from a company you worked at. Do not invent personal metrics in interviews.")}
  {''.join(items)}
</section>
'''
