import html as _html

def _code(lang: str, src: str) -> str:
    return (
        f'<div class="code-block"><div class="code-head"><span>{lang}</span>'
        f'<button type="button" class="copy-btn">Copy</button></div>'
        f"<pre><code>{_html.escape(src)}</code></pre></div>"
    )


PATTERNS = [
    {
        "id": "pat-hash",
        "name": "HashMap Lookup",
        "clues": "pair / complement / 'have I seen' / first unique / last index / group by key / two-sum family",
        "idea": "Pay O(n) memory to turn a scan into a lookup. Canonicalize the key first.",
        "pseudo": "map = {}\nfor i, x in enumerate(a):\n    if need(x) in map: return answer\n    map[key(x)] = i",
        "ts": """function lookupPattern<T>(a: T[], need: (x: T) => unknown, key = (x: T) => x) {
  const map = new Map<unknown, number>();
  for (let i = 0; i < a.length; i++) {
    const w = need(a[i]);
    if (map.has(w)) return [map.get(w)!, i] as const;
    map.set(key(a[i]), i);
  }
  return null;
}""",
        "cx": "Time O(n) expected, space O(n)",
        "traps": "Store after you look up (Two Sum). Object keys stringify. Unstable keys (objects without canonical form).",
        "probs": "Two Sum · Contains Duplicate · Valid Anagram · Longest Consecutive",
        "ex": "Two Sum: want = target - nums[i]. If want is in the map, you are done. Otherwise record nums[i] → i. You never need a second pass.",
    },
    {
        "id": "pat-freq",
        "name": "Frequency Counting",
        "clues": "anagram · permutation · top K frequent · 'same characters' · ransom / magazine · majority",
        "idea": "Count first, decide second. For 26 letters use a number[26]; otherwise Map.",
        "pseudo": "count = Map()\nfor x in data: count[x]++\nuse counts to compare, pick top K, or drive a window",
        "ts": """function counts(s: string): Map<string, number> {
  const m = new Map<string, number>();
  for (const ch of s) m.set(ch, (m.get(ch) ?? 0) + 1);
  return m;
}
function sameMaps(a: Map<string, number>, b: Map<string, number>): boolean {
  if (a.size !== b.size) return false;
  for (const [k, v] of a) if (b.get(k) !== v) return false;
  return true;
}""",
        "cx": "O(n) time, O(Σ) space",
        "traps": "Comparing maps by reference. Forgetting zero-count keys. Sorting each word inside a hot loop without need.",
        "probs": "Valid Anagram · Group Anagrams · Top K Frequent · Permutation in String",
        "ex": "Group Anagrams: key = sorted(word) or 26-count joined by '#'. Map<key, string[]>.",
    },
    {
        "id": "pat-tp",
        "name": "Two Pointers",
        "clues": "sorted array · palindrome · pairs/triples summing to target · container / rain · in-place partition",
        "idea": "Move the pointer that cannot improve the answer. Justify every move as discarding a region.",
        "pseudo": "i = 0, j = n-1\nwhile i < j:\n    if good(i,j): record\n    if tooSmall: i++\n    else: j--",
        "ts": """function twoSumSorted(a: number[], target: number): [number, number] {
  let i = 0, j = a.length - 1;
  while (i < j) {
    const s = a[i] + a[j];
    if (s === target) return [i + 1, j + 1]; // 1-indexed variant
    if (s < target) i++; else j--;
  }
  throw new Error("none");
}""",
        "cx": "O(n) after sort; O(1) extra",
        "traps": "Unsorted input. Moving both pointers. Duplicate-skipping in 3Sum (skip after a hit, and skip same i).",
        "probs": "Valid Palindrome · Two Sum II · 3Sum · Container With Most Water · Trapping Rain Water",
        "ex": "3Sum: sort, fix i, two-pointer the rest. Skip duplicate a[i] and duplicate left/right values.",
    },
    {
        "id": "pat-sw",
        "name": "Sliding Window",
        "clues": "contiguous substring/subarray · longest/shortest · at most K · no repeated characters · contain all of t · permutation of p · maintain a valid range",
        "idea": "Expand right. While invalid (or while you can shrink and stay valid), move left. Each index enters/leaves once.",
        "pseudo": "left = 0\nfor right in 0..n-1:\n    add a[right]\n    while not valid: remove a[left]; left++\n    update answer",
        "ts": """function minSubArrayLen(target: number, nums: number[]): number {
  let left = 0, sum = 0, best = Infinity;
  for (let r = 0; r < nums.length; r++) {
    sum += nums[r];
    while (sum >= target) {
      best = Math.min(best, r - left + 1);
      sum -= nums[left++];
    }
  }
  return best === Infinity ? 0 : best;
}""",
        "cx": "O(n) time, O(Σ) space",
        "traps": "Using window on non-contiguous data. Using window on sums with negatives (need prefix map). left jumping without removing counts.",
        "probs": "Longest substring no repeat · Character replacement · Min size subarray · Min window substring · Buy/sell stock (degenerate window / running min)",
        "ex": "Invariant for unique-char window: last-seen index of s[r] is either outside [left,r] or we set left = last+1. Window always has unique chars.",
    },
    {
        "id": "pat-pref",
        "name": "Prefix Sum",
        "clues": "range sum · how many subarrays equal K · pivot index · difference of two prefixes",
        "idea": "pref[r] - pref[l] = sum(l..r-1). Store prefix frequencies when the question is a count, not a single range.",
        "pseudo": "pref = 0; map = {0:1}\nfor x in a:\n    pref += x\n    ans += map[pref - k]\n    map[pref]++",
        "ts": """function rangeSum(pref: number[], l: number, r: number): number {
  return pref[r + 1] - pref[l]; // pref[i] = sum of first i elements
}""",
        "cx": "O(n) preprocess, O(1) query; count-of-subarrays O(n)",
        "traps": "Off-by-one on inclusive bounds. Forgetting prefix 0. Sliding window on negative numbers.",
        "probs": "Range Sum Query · Subarray Sum Equals K · Product except self (prefix/suffix products)",
        "ex": "Product except self: left[i] = product of items before i; right analog; answer[i] = left[i]*right[i]. Or one array + a running suffix.",
    },
    {
        "id": "pat-bs",
        "name": "Binary Search",
        "clues": "sorted · rotated sorted · matrix with sorted rows · minimize the maximum · 'smallest x such that feasible(x)' · Koko / split array / capacity",
        "idea": "Search a monotone predicate. Write feasible(mid) first, then shrink.",
        "pseudo": "lo, hi = minX, maxX\nwhile lo < hi:\n    mid = (lo+hi)//2\n    if feasible(mid): hi = mid\n    else: lo = mid+1\nreturn lo",
        "ts": """function search(a: number[], t: number): number {
  let lo = 0, hi = a.length - 1;
  while (lo <= hi) {
    const m = (lo + hi) >> 1;
    if (a[m] === t) return m;
    if (a[m] < t) lo = m + 1;
    else hi = m - 1;
  }
  return -1;
}""",
        "cx": "O(log n) on indices; O(n log A) when scanning n piles per mid",
        "traps": "Non-monotone feasible. Infinite loop lo=mid. Rotated array: identify the sorted half first.",
        "probs": "Binary Search · Insert position · 2D matrix · Rotated min/search · Koko",
        "ex": "Koko: lo=1, hi=max(piles). feasible(speed) = hours needed ≤ h. Minimize speed.",
    },
    {
        "id": "pat-fs",
        "name": "Fast / Slow Pointers",
        "clues": "cycle in a list · middle of list · happy number · find start of cycle · palindrome list",
        "idea": "Slow +1, fast +2. If they meet, a cycle exists. For middle, when fast hits the end, slow is mid.",
        "pseudo": "slow = fast = head\nwhile fast and fast.next:\n    slow = slow.next\n    fast = fast.next.next\n    if slow is fast: cycle",
        "ts": """function hasCycle(head: ListNode | null): boolean {
  let slow = head, fast = head;
  while (fast && fast.next) {
    slow = slow!.next;
    fast = fast.next.next;
    if (slow === fast) return true;
  }
  return false;
}""",
        "cx": "O(n) time, O(1) space",
        "traps": "Null checks on fast.next. Comparing values instead of node identity.",
        "probs": "Linked List Cycle · Remove Nth (gap variant) · Reorder List (find mid + reverse)",
        "ex": "Nth from end: advance first n+1 steps (with dummy), then walk both until first hits null; second.next is the node to drop.",
    },
    {
        "id": "pat-stack",
        "name": "Stack / Monotonic Stack",
        "clues": "next greater/smaller · parentheses · nested · histogram · daily temperatures · decode string · RPN",
        "idea": "The stack holds candidates that are still waiting. Pop when the current item 'resolves' them.",
        "pseudo": "st = []\nfor i, x in enumerate(a):\n    while st and a[st.top] < x:\n        ans[st.pop()] = i\n    st.push(i)",
        "ts": """function nextGreater(a: number[]): number[] {
  const ans = Array(a.length).fill(-1);
  const st: number[] = [];
  for (let i = 0; i < a.length; i++) {
    while (st.length && a[i] > a[st.at(-1)!]) ans[st.pop()!] = a[i];
    st.push(i);
  }
  return ans;
}""",
        "cx": "O(n) time and space",
        "traps": "Values vs indices. Strict vs non-strict inequality. Sentinel 0 at the end of histogram.",
        "probs": "Valid Parentheses · Min Stack · Daily Temperatures · RPN · Largest Rectangle",
        "ex": "Histogram: for each bar, width = nextSmaller - prevSmaller - 1. Monotonic increasing stack of indices.",
    },
    {
        "id": "pat-bfs",
        "name": "BFS",
        "clues": "shortest path unweighted · level order · minutes / days to spread · multi-source · clone by layers · word ladder",
        "idea": "Queue + visited. Process level size if you need distance in hops.",
        "pseudo": "q = sources; visited = set(sources); dist = 0\nwhile q:\n    for _ in q.level:\n        pop; push unseen neighbors\n    dist++",
        "ts": """function levelOrder(root: TreeNode | null): number[][] {
  if (!root) return [];
  const out: number[][] = [], q = [root];
  let h = 0;
  while (h < q.length) {
    const n = q.length - h, row: number[] = [];
    for (let i = 0; i < n; i++) {
      const node = q[h++];
      row.push(node.val);
      if (node.left) q.push(node.left);
      if (node.right) q.push(node.right);
    }
    out.push(row);
  }
  return out;
}""",
        "cx": "O(V+E) time, O(V) space",
        "traps": "shift() O(n). Forgetting multi-source. Not marking visited when enqueueing (duplicates in queue).",
        "probs": "Level order · Rotting Oranges · Clone Graph · Course Schedule (Kahn)",
        "ex": "Oranges: enqueue every rotten cell first. Each BFS layer is one minute.",
    },
    {
        "id": "pat-dfs",
        "name": "DFS",
        "clues": "connected components · islands · existence of a path · cycle in directed graph · flood fill · tree recursion",
        "idea": "Mark visited, recurse neighbors. For directed cycles use 3 colors: white / gray / black.",
        "pseudo": "def dfs(u):\n    if u visiting: cycle\n    mark visiting\n    for v in adj[u]: dfs(v)\n    mark done",
        "ts": """function canFinish(n: number, edges: number[][]): boolean {
  const g: number[][] = Array.from({ length: n }, () => []);
  for (const [a, b] of edges) g[b].push(a);
  const st = Array(n).fill(0); // 0 unseen, 1 visiting, 2 done
  const dfs = (u: number): boolean => {
    if (st[u] === 1) return false;
    if (st[u] === 2) return true;
    st[u] = 1;
    for (const v of g[u]) if (!dfs(v)) return false;
    st[u] = 2;
    return true;
  };
  for (let i = 0; i < n; i++) if (!dfs(i)) return false;
  return true;
}""",
        "cx": "O(V+E)",
        "traps": "Missing visited. Recursion depth. Mutating grid without bounds checks.",
        "probs": "Number of Islands · Course Schedule · Pacific Atlantic · Tree DFS family",
        "ex": "Islands: each unvisited '1' starts a component; DFS sinks the land.",
    },
    {
        "id": "pat-tree",
        "name": "Tree Recursion",
        "clues": "binary tree · height · diameter · invert · validate · LCA · construct from traversals · kth in BST",
        "idea": "Return what the parent needs (height, bounds, counts). Keep a side-channel (max diameter) if the answer is not the same as the return value.",
        "pseudo": "def go(node):\n    if not node: return BASE\n    L, R = go(node.left), go(node.right)\n    update global with L,R,node\n    return combine(L,R,node)",
        "ts": """function diameterOfBinaryTree(root: TreeNode | null): number {
  let best = 0;
  const height = (n: TreeNode | null): number => {
    if (!n) return 0;
    const L = height(n.left), R = height(n.right);
    best = Math.max(best, L + R);
    return 1 + Math.max(L, R);
  };
  height(root);
  return best;
}""",
        "cx": "O(n) time, O(h) space",
        "traps": "Using only local left&lt;node&lt;right for BST. Forgetting empty tree. Mixing up preorder/inorder when rebuilding.",
        "probs": "Max depth · Invert · Diameter · Balanced · Validate BST · LCA · Kth smallest · Construct",
        "ex": "Validate BST: pass (lo, hi) down. Node must be strictly inside.",
    },
    {
        "id": "pat-heap",
        "name": "Heap / Top K",
        "clues": "kth largest/smallest · top K frequent · k closest · running median · always pick the current best",
        "idea": "You do not need a full sort. Keep a heap of size K. For kth largest, use a min-heap of size K.",
        "pseudo": "h = minheap\nfor x in data:\n    h.push(x)\n    if h.size > k: h.pop()\nreturn h.peek()",
        "ts": """function findKthLargest(nums: number[], k: number): number {
  const a = nums.slice().sort((x, y) => y - x);
  return a[k - 1]; // honest O(n log n); mention heap O(n log k)
}""",
        "cx": "O(n log k) with a heap; O(n log n) with sort — say both",
        "traps": "Min-heap vs max-heap mixup. Off-by-one on k. Median: two heaps must stay balanced.",
        "probs": "Kth Largest · Top K Frequent · K Closest · Median stream",
        "ex": "K closest: max-heap of size K by distance, or sort by dist and take K — n is often small enough that sort is what you ship.",
    },
]


def patterns() -> str:
    blocks = []
    for p in PATTERNS:
        blocks.append(f'''
<article class="pattern" id="{p["id"]}" data-search="{p["name"]} pattern recognition" data-stype="Pattern">
  <div class="meta-row"><span class="badge badge-pattern">Pattern</span></div>
  <h3>{p["name"]}</h3>
  <p><b>1. Recognition clues.</b> Look for: {p["clues"]}.</p>
  <p><b>2. Core idea.</b> {p["idea"]}</p>
  <p><b>3. Generic pseudocode.</b></p>
  {_code("Pseudocode", p["pseudo"])}
  <p><b>4. TypeScript template.</b></p>
  {_code("TypeScript", p["ts"])}
  <p><b>5. Typical complexity.</b> {p["cx"]}</p>
  <p><b>6. Common traps.</b> {p["traps"]}</p>
  <p><b>7. Representative problems.</b> {p["probs"]}</p>
  <p><b>8. Worked recognition.</b> {p["ex"]}</p>
</article>''')
    return f'''
<section class="block" id="patterns" data-search="DSA Pattern Recognition Library" data-stype="Section">
  <p class="kicker">Recognition</p>
  <h2 class="section-title">DSA Pattern Recognition</h2>
  <p class="lede">Senior interviews are won in the first four minutes: you name the pattern, justify it, then code a template. If the prompt does not match a clue below, start with brute force and look for the bottleneck (repeated scan → HashMap; contiguous constraint → window; sorted monotone → binary search).</p>
  <div class="callout">Atlassian bar: say <i>why</i> the pattern fits (“the subarray is contiguous and the constraint is repairable by moving left”) not just the pattern name.</div>
  {''.join(blocks)}
</section>
'''
