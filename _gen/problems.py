from problems1 import P1
from problems2 import P2
from problems3 import P3
from problems4 import P4
from problems_lib import problem


def problems() -> str:
    all_p = P1 + P2 + P3 + P4
    topics = sorted({p["topic"] for p in all_p})
    patterns = sorted({p["pattern"] for p in all_p})
    topic_opts = "".join(f'<option value="{t}">{t}</option>' for t in topics)
    pat_opts = "".join(f'<option value="{p}">{p}</option>' for p in patterns)
    cards = "".join(problem(p) for p in all_p)
    return f'''
<section class="block" id="problems" data-search="DSA Problem Bank" data-stype="Section">
  <p class="kicker">{len(all_p)} curated problems</p>
  <h2 class="section-title">DSA Problem Bank</h2>
  <p class="lede">Original summaries and original TypeScript solutions — enough to learn and practice without a second document. For a hidden-test judge, search the name on LeetCode (optional). Prioritize Easy and Medium. The few Hards (rain water, min window, histogram, median stream) are labeled; skip histogram if you are behind.</p>
  <div class="filters">
    <select id="filter-status">
      <option value="all">All statuses</option>
      <option value="not-started">Not Started</option>
      <option value="attempted">Attempted</option>
      <option value="solved">Solved</option>
      <option value="review">Review</option>
      <option value="mastered">Mastered</option>
    </select>
    <select id="filter-diff">
      <option value="all">All difficulties</option>
      <option value="easy">Easy</option>
      <option value="medium">Medium</option>
      <option value="hard">Hard</option>
    </select>
    <select id="filter-topic">
      <option value="all">All topics</option>
      {topic_opts}
    </select>
    <select id="filter-pattern">
      <option value="all">All patterns</option>
      {pat_opts}
    </select>
    <input id="filter-text" type="search" placeholder="Filter by name…" />
  </div>
  {cards}
</section>
'''
