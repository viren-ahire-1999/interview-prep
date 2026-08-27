from util import topic, callout, code, diagram
from drills import sort_gym, twopointer_gym, window_gym, backtrack_gym, dp_gym, expert_gym


def sort_search() -> str:
    t = topic("ss-bin", "Sort when you must; binary search when it’s sorted",
              "merge sort binary search JavaScript", "Lesson", f'''
  <p><code>arr.sort((a,b) =&gt; a-b)</code> is O(n log n). Never <code>sort()</code> without a comparator on numbers (it sorts as strings).</p>
  {code("JavaScript", '''function mergeSort(arr) {
  if (arr.length <= 1) return arr;
  const m = arr.length >> 1;
  return merge(mergeSort(arr.slice(0, m)), mergeSort(arr.slice(m)));
}
function merge(a, b) {
  const out = [];
  let i = 0, j = 0;
  while (i < a.length && j < b.length)
    out.push(a[i] <= b[j] ? a[i++] : b[j++]);
  return out.concat(a.slice(i), b.slice(j));
}

function binarySearch(a, t) {
  let lo = 0, hi = a.length - 1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (a[mid] === t) return mid;
    if (a[mid] < t) lo = mid + 1;
    else hi = mid - 1;
  }
  return -1;
}

/** first index where pred(i) is true (pred is monotonic) */
function lowerBound(n, pred) {
  let lo = 0, hi = n;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (pred(mid)) hi = mid;
    else lo = mid + 1;
  }
  return lo;
}
''')}
  <p>Binary search on <b>answer</b> (min days, min capacity) uses the second template. The predicate must flip from false to true once.</p>
  ''', "topics")
    return f'''
<section class="block" id="sort" data-search="Sorting binary search JavaScript" data-stype="Section">
  <p class="kicker">Order</p>
  <h2 class="section-title">Sorting and search</h2>
  <p><a href="#gym-sort">Jump to sort / search practice (6 problems) →</a></p>
  {t}
  {sort_gym()}
</section>
'''


def twopointer() -> str:
    t = topic("tp-opp", "Two indices walking the array",
              "two pointers JavaScript", "Lesson", f'''
  {code("JavaScript", '''function twoSumSorted(a, target) {
  let lo = 0, hi = a.length - 1;
  while (lo < hi) {
    const s = a[lo] + a[hi];
    if (s === target) return [lo, hi];
    if (s < target) lo++;
    else hi--;
  }
  return [];
}

function maxArea(h) {
  let lo = 0, hi = h.length - 1, best = 0;
  while (lo < hi) {
    best = Math.max(best, Math.min(h[lo], h[hi]) * (hi - lo));
    if (h[lo] < h[hi]) lo++;
    else hi--;
  }
  return best;
}

function removeDuplicatesSorted(a) {
  if (!a.length) return 0;
  let w = 1;
  for (let r = 1; r < a.length; r++) if (a[r] !== a[w - 1]) a[w++] = a[r];
  return w;
}
''')}
  <p>Same-direction: slow/fast on arrays (remove, in-place compact) and on lists (cycle, middle).</p>
  ''', "topics")
    return f'''
<section class="block" id="twopointer" data-search="Two pointers JavaScript" data-stype="Section">
  <p class="kicker">Linear scan, smarter</p>
  <h2 class="section-title">Two pointers</h2>
  <p><a href="#gym-twopointer">Jump to two-pointer practice (6 problems) →</a></p>
  {t}
  {twopointer_gym()}
</section>
'''


def window() -> str:
    t = topic("wd-var", "A window is a range [left, right] you grow and shrink",
              "sliding window JavaScript substring", "Lesson", f'''
  {code("JavaScript", '''function maxSumFixed(a, k) {
  let sum = 0, best = -Infinity;
  for (let i = 0; i < a.length; i++) {
    sum += a[i];
    if (i >= k) sum -= a[i - k];
    if (i >= k - 1) best = Math.max(best, sum);
  }
  return best;
}

function longestUnique(s) {
  const last = new Map();
  let left = 0, best = 0;
  for (let right = 0; right < s.length; right++) {
    const ch = s[right];
    if (last.has(ch) && last.get(ch) >= left) left = last.get(ch) + 1;
    last.set(ch, right);
    best = Math.max(best, right - left + 1);
  }
  return best;
}
''')}
  <p>Invariant: the window always satisfies the constraint (unique chars, sum ≤ k, at most k zeros). When it breaks, move <code>left</code> until it holds again. Each index enters and leaves at most once → O(n).</p>
  ''', "topics")
    return f'''
<section class="block" id="window" data-search="Sliding window JavaScript" data-stype="Section">
  <p class="kicker">Subarrays in linear time</p>
  <h2 class="section-title">Sliding window</h2>
  <p><a href="#gym-window">Jump to window practice (6 problems) →</a></p>
  {t}
  {window_gym()}
</section>
'''


def backtrack() -> str:
    t = topic("bt-choose", "Choose, explore, unchoose",
              "backtracking subsets permutations JavaScript", "Lesson", f'''
  {code("JavaScript", '''function subsets(nums) {
  const out = [], path = [];
  function go(i) {
    if (i === nums.length) { out.push(path.slice()); return; }
    path.push(nums[i]); go(i + 1); path.pop(); // take
    go(i + 1);                                 // skip
  }
  go(0);
  return out;
}

function permute(nums) {
  const out = [], used = Array(nums.length).fill(false), path = [];
  function go() {
    if (path.length === nums.length) { out.push(path.slice()); return; }
    for (let i = 0; i < nums.length; i++) {
      if (used[i]) continue;
      used[i] = true; path.push(nums[i]);
      go();
      path.pop(); used[i] = false;
    }
  }
  go();
  return out;
}
''')}
  {diagram("""n=3 subsets: 8 leaves
Always path.pop() after the recursive call
n! permutations — only tiny n""")}
  <p>Prune: skip if remaining sum is negative; skip duplicates with a sorted array and <code>if (i&gt;start && nums[i]===nums[i-1]) continue</code>.</p>
  ''', "topics")
    return f'''
<section class="block" id="backtrack" data-search="Backtracking JavaScript" data-stype="Section">
  <p class="kicker">Exhaust, with a spine</p>
  <h2 class="section-title">Backtracking</h2>
  <p><a href="#gym-backtrack">Jump to backtracking practice (6 problems) →</a></p>
  {t}
  {backtrack_gym()}
</section>
'''


def dp() -> str:
    t1 = topic("dp-from", "DP is recursion + memory, then a table",
               "dynamic programming JavaScript coin change", "Lesson", f'''
  <p>Ask: (1) can I define the answer from smaller answers? (2) do I recompute the same smaller answer? If yes, memoize, then fill a table bottom-up.</p>
  {code("JavaScript", '''function climbStairs(n) {
  if (n <= 2) return n;
  let a = 1, b = 2;
  for (let i = 3; i <= n; i++) { const c = a + b; a = b; b = c; }
  return b;
}

function coinChange(coins, amount) {
  const INF = amount + 1;
  const dp = Array(amount + 1).fill(INF);
  dp[0] = 0;
  for (let x = 1; x <= amount; x++)
    for (const c of coins)
      if (c <= x) dp[x] = Math.min(dp[x], dp[x - c] + 1);
  return dp[amount] === INF ? -1 : dp[amount];
}

function uniquePaths(m, n) {
  const dp = Array.from({ length: m }, () => Array(n).fill(1));
  for (let i = 1; i < m; i++)
    for (let j = 1; j < n; j++)
      dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
  return dp[m - 1][n - 1];
}

function knapsack(w, val, cap) {
  const dp = Array(cap + 1).fill(0);
  for (let i = 0; i < w.length; i++)
    for (let c = cap; c >= w[i]; c--)
      dp[c] = Math.max(dp[c], dp[c - w[i]] + val[i]);
  return dp[cap];
}
''')}
  {callout("State the meaning of <code>dp[i]</code> in a sentence before you code. ‘Minimum coins to make sum i’ is a state. A vague array is not.")}
  ''', "topics")
    return f'''
<section class="block" id="dp" data-search="Dynamic programming JavaScript" data-stype="Section">
  <p class="kicker">Optimal substructure</p>
  <h2 class="section-title">Dynamic programming</h2>
  <p><a href="#gym-dp">Jump to DP practice (8 problems) →</a></p>
  {t1}
  {dp_gym()}
</section>
'''


def expert() -> str:
    t1 = topic("ex-trie", "Trie: a tree of prefixes",
               "trie prefix tree JavaScript", "Lesson", f'''
  {code("JavaScript", '''class TrieNode {
  constructor() { this.next = new Map(); this.end = false; }
}
class Trie {
  constructor() { this.root = new TrieNode(); }
  insert(word) {
    let n = this.root;
    for (const ch of word) {
      if (!n.next.has(ch)) n.next.set(ch, new TrieNode());
      n = n.next.get(ch);
    }
    n.end = true;
  }
  startsWith(pref) {
    let n = this.root;
    for (const ch of pref) {
      if (!n.next.has(ch)) return false;
      n = n.next.get(ch);
    }
    return true;
  }
  search(word) {
    let n = this.root;
    for (const ch of word) {
      if (!n.next.has(ch)) return false;
      n = n.next.get(ch);
    }
    return n.end;
  }
}
''')}
  <p>Better than a <code>Set</code> when you need prefix queries (autocomplete). Space can be large; that’s the trade-off.</p>
  ''', "topics")

    t2 = topic("ex-uf", "Union-find: growing components",
               "union find disjoint set JavaScript", "Lesson", f'''
  {code("JavaScript", '''class UnionFind {
  constructor(n) { this.p = [...Array(n).keys()]; this.r = Array(n).fill(0); }
  find(x) {
    if (this.p[x] !== x) this.p[x] = this.find(this.p[x]);
    return this.p[x];
  }
  union(a, b) {
    a = this.find(a); b = this.find(b);
    if (a === b) return false;
    if (this.r[a] < this.r[b]) [a, b] = [b, a];
    this.p[b] = a;
    if (this.r[a] === this.r[b]) this.r[a]++;
    return true;
  }
}
''')}
  <p>Almost O(1) per op with path compression + rank. Use: connected components, Kruskal, “accounts merge,” redundant connection.</p>
  ''', "topics")

    t3 = topic("ex-mono", "Prefix sums and monotonic stacks",
               "prefix sum monotonic stack JavaScript", "Lesson", f'''
  {code("JavaScript", '''function subarraySum(nums, k) {
  const seen = new Map([[0, 1]]);
  let sum = 0, ans = 0;
  for (const x of nums) {
    sum += x;
    ans += seen.get(sum - k) || 0;
    seen.set(sum, (seen.get(sum) || 0) + 1);
  }
  return ans;
}

function dailyTemperatures(t) {
  const ans = Array(t.length).fill(0), st = [];
  for (let i = 0; i < t.length; i++) {
    while (st.length && t[i] > t[st[st.length - 1]]) {
      const j = st.pop();
      ans[j] = i - j;
    }
    st.push(i);
  }
  return ans;
}
''')}
  <p>Prefix + map: “how many subarrays sum to k.” Monotonic stack: next greater / next smaller in O(n). These are the usual “expert” tells after the core patterns.</p>
  ''', "topics")

    return f'''
<section class="block" id="expert" data-search="Trie union-find prefix monotonic stack" data-stype="Section">
  <p class="kicker">Expert structures</p>
  <h2 class="section-title">Tries, union-find, prefix, monotonic stack</h2>
  <p><a href="#gym-expert">Jump to expert practice (8 problems) →</a></p>
  {t1}{t2}{t3}
  {expert_gym()}
</section>
'''
