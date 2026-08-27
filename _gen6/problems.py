from util import esc, code, solution_reveal


def _p(i, title, level, cat, prompt, idea, src, time, space):
    from explains import BANK
    hid = f"pb-{i}"
    extra = BANK.get(i) or BANK.get(title)
    return f'''
<article class="problem" id="{hid}" data-pid="{hid}" data-search="{esc(title)}" data-stype="Problem" data-cat="{cat}" data-level="{level}" data-mock="1" data-filterable>
  <div class="meta-row"><span class="badge badge-{level}">{level}</span><span class="chip">{cat}</span><span class="badge badge-pattern">Practice</span></div>
  <h3>{i}. {esc(title)}</h3>
  <p>{prompt}</p>
  <p><button type="button" class="toggle-btn" data-toggle="{hid}-a">Reveal solution</button>
     <button type="button" class="toggle-btn" data-complete="designs" data-cid="{hid}">Mark complete</button></p>
  <div class="reveal" id="{hid}-a">
    {solution_reveal(hid, idea, src, time, space, extra)}
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
    ("Two sum", "easy", "hash",
     "Return indices of two numbers that add to target. Same index twice is illegal.",
     "One pass Map: value → index. Need = target − nums[i].",
     "function twoSum(nums, target) {\n  const seen = new Map();\n  for (let i = 0; i < nums.length; i++) {\n    const need = target - nums[i];\n    if (seen.has(need)) return [seen.get(need), i];\n    seen.set(nums[i], i);\n  }\n  return [];\n}",
     "O(n)", "O(n)"),
    ("Contains duplicate", "easy", "hash",
     "True if any value appears twice.",
     "Set while scanning.",
     "function containsDuplicate(a) {\n  const s = new Set();\n  for (const x of a) {\n    if (s.has(x)) return true;\n    s.add(x);\n  }\n  return false;\n}",
     "O(n)", "O(n)"),
    ("Valid anagram", "easy", "hash",
     "Are s and t anagrams?",
     "Count 26 letters or Map. Same length first.",
     "function isAnagram(s, t) {\n  if (s.length !== t.length) return false;\n  const f = Array(26).fill(0);\n  for (let i = 0; i < s.length; i++) {\n    f[s.charCodeAt(i) - 97]++;\n    f[t.charCodeAt(i) - 97]--;\n  }\n  return f.every((n) => n === 0);\n}",
     "O(n)", "O(1)"),
    ("Valid palindrome", "easy", "string",
     "Alphanumeric, ignore case.",
     "Two pointers after normalize, or two pointers skipping junk.",
     "function isPalindrome(s) {\n  let lo = 0, hi = s.length - 1;\n  const ok = (c) => /[a-z0-9]/i.test(c);\n  while (lo < hi) {\n    while (lo < hi && !ok(s[lo])) lo++;\n    while (lo < hi && !ok(s[hi])) hi--;\n    if (s[lo++].toLowerCase() !== s[hi--].toLowerCase()) return false;\n  }\n  return true;\n}",
     "O(n)", "O(1)"),
    ("Best time to buy/sell stock", "easy", "array",
     "Max profit, one buy and one later sell.",
     "Track min so far; profit = price − min.",
     "function maxProfit(p) {\n  let min = Infinity, best = 0;\n  for (const x of p) { min = Math.min(min, x); best = Math.max(best, x - min); }\n  return best;\n}",
     "O(n)", "O(1)"),
    ("Maximum subarray (Kadane)", "medium", "array",
     "Maximum sum of a contiguous subarray.",
     "bestEndingHere = max(x, bestEndingHere + x).",
     "function maxSubArray(a) {\n  let cur = a[0], best = a[0];\n  for (let i = 1; i < a.length; i++) {\n    cur = Math.max(a[i], cur + a[i]);\n    best = Math.max(best, cur);\n  }\n  return best;\n}",
     "O(n)", "O(1)"),
    ("Product of array except self", "medium", "array",
     "out[i] = product of all except i. No division.",
     "Prefix products then suffix sweep.",
     "function productExceptSelf(a) {\n  const n = a.length, out = Array(n).fill(1);\n  let p = 1;\n  for (let i = 0; i < n; i++) { out[i] = p; p *= a[i]; }\n  p = 1;\n  for (let i = n - 1; i >= 0; i--) { out[i] *= p; p *= a[i]; }\n  return out;\n}",
     "O(n)", "O(1) extra besides out"),
    ("Longest unique substring", "medium", "window",
     "Length of longest substring without repeating characters.",
     "Variable window + last-seen index.",
     "function lengthOfLongestSubstring(s) {\n  const last = new Map();\n  let left = 0, best = 0;\n  for (let r = 0; r < s.length; r++) {\n    if (last.has(s[r]) && last.get(s[r]) >= left) left = last.get(s[r]) + 1;\n    last.set(s[r], r);\n    best = Math.max(best, r - left + 1);\n  }\n  return best;\n}",
     "O(n)", "O(min(n, alphabet))"),
    ("3Sum", "medium", "twopointer",
     "Unique triplets that sum to 0.",
     "Sort. Fix i. Two pointers. Skip duplicates.",
     "function threeSum(nums) {\n  nums.sort((a, b) => a - b);\n  const out = [];\n  for (let i = 0; i < nums.length; i++) {\n    if (i && nums[i] === nums[i - 1]) continue;\n    let lo = i + 1, hi = nums.length - 1;\n    while (lo < hi) {\n      const s = nums[i] + nums[lo] + nums[hi];\n      if (s === 0) {\n        out.push([nums[i], nums[lo], nums[hi]]);\n        while (lo < hi && nums[lo] === nums[lo + 1]) lo++;\n        while (lo < hi && nums[hi] === nums[hi - 1]) hi--;\n        lo++; hi--;\n      } else if (s < 0) lo++;\n      else hi--;\n    }\n  }\n  return out;\n}",
     "O(n²)", "O(1) extra"),
    ("Container with most water", "medium", "twopointer",
     "Two lines form a container. Max area.",
     "Ends inward. Move the shorter side.",
     "function maxArea(h) {\n  let lo = 0, hi = h.length - 1, best = 0;\n  while (lo < hi) {\n    best = Math.max(best, Math.min(h[lo], h[hi]) * (hi - lo));\n    if (h[lo] < h[hi]) lo++; else hi--;\n  }\n  return best;\n}",
     "O(n)", "O(1)"),
    ("Valid parentheses", "easy", "stack",
     "(), [], {} nested correctly.",
     "Stack of openers.",
     "function isValid(s) {\n  const st = [], m = { ')':'(', ']':'[', '}':'{' };\n  for (const ch of s) {\n    if (!m[ch]) st.push(ch);\n    else if (st.pop() !== m[ch]) return false;\n  }\n  return st.length === 0;\n}",
     "O(n)", "O(n)"),
    ("Min stack", "medium", "stack",
     "push, pop, top, getMin all O(1).",
     "Parallel min stack.",
     "class MinStack {\n  constructor() { this.st = []; this.mins = []; }\n  push(x) {\n    this.st.push(x);\n    this.mins.push(this.mins.length ? Math.min(x, this.mins.at(-1)) : x);\n  }\n  pop() { this.st.pop(); this.mins.pop(); }\n  top() { return this.st.at(-1); }\n  getMin() { return this.mins.at(-1); }\n}",
     "O(1) ops", "O(n)"),
    ("Reverse linked list", "easy", "list",
     "Reverse a singly linked list.",
     "prev/curr/next walk.",
     "function reverseList(head) {\n  let prev = null, curr = head;\n  while (curr) {\n    const next = curr.next;\n    curr.next = prev;\n    prev = curr;\n    curr = next;\n  }\n  return prev;\n}",
     "O(n)", "O(1)"),
    ("Merge two sorted lists", "easy", "list",
     "Merge two sorted linked lists.",
     "Dummy node.",
     "function mergeTwoLists(a, b) {\n  const dummy = { val: 0, next: null };\n  let t = dummy;\n  while (a && b) {\n    if (a.val <= b.val) { t.next = a; a = a.next; }\n    else { t.next = b; b = b.next; }\n    t = t.next;\n  }\n  t.next = a || b;\n  return dummy.next;\n}",
     "O(n)", "O(1)"),
    ("Linked list cycle", "easy", "list",
     "Does the list have a cycle?",
     "Floyd slow/fast.",
     "function hasCycle(head) {\n  let s = head, f = head;\n  while (f && f.next) {\n    s = s.next; f = f.next.next;\n    if (s === f) return true;\n  }\n  return false;\n}",
     "O(n)", "O(1)"),
    ("Invert binary tree", "easy", "tree",
     "Swap every left/right.",
     "Recurse or BFS.",
     "function invertTree(root) {\n  if (!root) return null;\n  const l = invertTree(root.left);\n  root.left = invertTree(root.right);\n  root.right = l;\n  return root;\n}",
     "O(n)", "O(h)"),
    ("Maximum depth of tree", "easy", "tree",
     "Height of binary tree.",
     "1 + max(left, right).",
     "function maxDepth(root) {\n  if (!root) return 0;\n  return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));\n}",
     "O(n)", "O(h)"),
    ("Same tree", "easy", "tree",
     "Are two trees structurally equal?",
     "Both null or vals equal and children same.",
     "function isSameTree(p, q) {\n  if (!p || !q) return p === q;\n  return p.val === q.val && isSameTree(p.left, q.left) && isSameTree(p.right, q.right);\n}",
     "O(n)", "O(h)"),
    ("Level order", "medium", "tree",
     "Values by level.",
     "BFS with level size.",
     "function levelOrder(root) {\n  if (!root) return [];\n  const q = [root], res = [];\n  while (q.length) {\n    const n = q.length, lvl = [];\n    for (let i = 0; i < n; i++) {\n      const node = q.shift();\n      lvl.push(node.val);\n      if (node.left) q.push(node.left);\n      if (node.right) q.push(node.right);\n    }\n    res.push(lvl);\n  }\n  return res;\n}",
     "O(n)", "O(n)"),
    ("Validate BST", "medium", "tree",
     "Is it a BST?",
     "Carry (lo, hi) bounds, not only vs parent.",
     "function isValidBST(root, lo = -Infinity, hi = Infinity) {\n  if (!root) return true;\n  if (root.val <= lo || root.val >= hi) return false;\n  return isValidBST(root.left, lo, root.val) && isValidBST(root.right, root.val, hi);\n}",
     "O(n)", "O(h)"),
    ("Lowest common ancestor BST", "medium", "tree",
     "LCA in a BST.",
     "Walk until split.",
     "function lca(root, p, q) {\n  const lo = Math.min(p.val, q.val), hi = Math.max(p.val, q.val);\n  let n = root;\n  while (n) {\n    if (n.val < lo) n = n.right;\n    else if (n.val > hi) n = n.left;\n    else return n;\n  }\n  return null;\n}",
     "O(h)", "O(1)"),
    ("Number of islands", "medium", "graph",
     "Count 1-components in a grid.",
     "DFS/BFS flood fill.",
     "function numIslands(grid) {\n  const R = grid.length, C = grid[0].length;\n  const dirs = [[1,0],[-1,0],[0,1],[0,-1]];\n  const sink = (r, c) => {\n    if (r<0||c<0||r>=R||c>=C||grid[r][c]!=='1') return;\n    grid[r][c] = '0';\n    for (const [dr,dc] of dirs) sink(r+dr, c+dc);\n  };\n  let n = 0;\n  for (let r=0;r<R;r++) for (let c=0;c<C;c++) if (grid[r][c]==='1') { n++; sink(r,c); }\n  return n;\n}",
     "O(RC)", "O(RC) stack worst"),
    ("Clone graph", "medium", "graph",
     "Deep copy a connected undirected graph.",
     "Map old → new. DFS or BFS.",
     "function cloneGraph(node, map = new Map()) {\n  if (!node) return null;\n  if (map.has(node)) return map.get(node);\n  const copy = { val: node.val, neighbors: [] };\n  map.set(node, copy);\n  for (const n of node.neighbors) copy.neighbors.push(cloneGraph(n, map));\n  return copy;\n}",
     "O(V+E)", "O(V)"),
    ("Course schedule", "medium", "graph",
     "Can you finish courses given prereqs?",
     "Kahn topo. seen === n.",
     "function canFinish(n, pre) {\n  const adj = Array.from({length:n}, () => []);\n  const indeg = Array(n).fill(0);\n  for (const [a,b] of pre) { adj[b].push(a); indeg[a]++; }\n  const q = [];\n  for (let i=0;i<n;i++) if (!indeg[i]) q.push(i);\n  let s = 0;\n  while (q.length) {\n    const u = q.shift(); s++;\n    for (const v of adj[u]) if (--indeg[v]===0) q.push(v);\n  }\n  return s === n;\n}",
     "O(V+E)", "O(V+E)"),
    ("Pacific Atlantic water", "medium", "graph",
     "Cells that can flow to both oceans (non-increasing height).",
     "BFS/DFS from oceans inland. Intersect.",
     "function pacificAtlantic(h) {\n  const R = h.length, C = h[0].length;\n  const pac = Array.from({length:R}, () => Array(C).fill(false));\n  const atl = Array.from({length:R}, () => Array(C).fill(false));\n  const dirs = [[1,0],[-1,0],[0,1],[0,-1]];\n  function dfs(r,c,seen) {\n    if (seen[r][c]) return;\n    seen[r][c] = true;\n    for (const [dr,dc] of dirs) {\n      const nr=r+dr,nc=c+dc;\n      if (nr>=0&&nc>=0&&nr<R&&nc<C&&h[nr][nc]>=h[r][c]) dfs(nr,nc,seen);\n    }\n  }\n  for (let i=0;i<R;i++) { dfs(i,0,pac); dfs(i,C-1,atl); }\n  for (let j=0;j<C;j++) { dfs(0,j,pac); dfs(R-1,j,atl); }\n  const out = [];\n  for (let r=0;r<R;r++) for (let c=0;c<C;c++) if (pac[r][c]&&atl[r][c]) out.push([r,c]);\n  return out;\n}",
     "O(RC)", "O(RC)"),
    ("Binary search", "easy", "search",
     "Index of target in sorted array, else -1.",
     "Classic lo/hi.",
     "function search(a, t) {\n  let lo = 0, hi = a.length - 1;\n  while (lo <= hi) {\n    const m = (lo + hi) >> 1;\n    if (a[m] === t) return m;\n    if (a[m] < t) lo = m + 1;\n    else hi = m - 1;\n  }\n  return -1;\n}",
     "O(log n)", "O(1)"),
    ("Search rotated sorted array", "medium", "search",
     "Find target in rotated sorted unique array.",
     "One side of mid is sorted. Go there if target is in range.",
     "function searchRotated(a, t) {\n  let lo = 0, hi = a.length - 1;\n  while (lo <= hi) {\n    const m = (lo + hi) >> 1;\n    if (a[m] === t) return m;\n    if (a[lo] <= a[m]) {\n      if (a[lo] <= t && t < a[m]) hi = m - 1;\n      else lo = m + 1;\n    } else {\n      if (a[m] < t && t <= a[hi]) lo = m + 1;\n      else hi = m - 1;\n    }\n  }\n  return -1;\n}",
     "O(log n)", "O(1)"),
    ("Climbing stairs", "easy", "dp",
     "n stairs, 1 or 2 at a time. Ways.",
     "Fibonacci.",
     "function climbStairs(n) {\n  if (n <= 2) return n;\n  let a = 1, b = 2;\n  for (let i = 3; i <= n; i++) { const c = a + b; a = b; b = c; }\n  return b;\n}",
     "O(n)", "O(1)"),
    ("House robber", "medium", "dp",
     "Max money, no two adjacent houses.",
     "dp[i] = max(dp[i-1], dp[i-2] + nums[i]).",
     "function rob(nums) {\n  let prev = 0, cur = 0;\n  for (const x of nums) { const n = Math.max(cur, prev + x); prev = cur; cur = n; }\n  return cur;\n}",
     "O(n)", "O(1)"),
    ("Coin change", "medium", "dp",
     "Fewest coins to make amount, or -1.",
     "dp[x] = min coins for x.",
     "function coinChange(coins, amount) {\n  const INF = amount + 1;\n  const dp = Array(amount + 1).fill(INF);\n  dp[0] = 0;\n  for (let x = 1; x <= amount; x++)\n    for (const c of coins) if (c <= x) dp[x] = Math.min(dp[x], dp[x - c] + 1);\n  return dp[amount] === INF ? -1 : dp[amount];\n}",
     "O(amount × coins)", "O(amount)"),
    ("Unique paths", "medium", "dp",
     "m×n grid, only right/down. Paths from top-left to bottom-right.",
     "dp[i][j] = from above + from left.",
     "function uniquePaths(m, n) {\n  const dp = Array.from({ length: m }, () => Array(n).fill(1));\n  for (let i = 1; i < m; i++)\n    for (let j = 1; j < n; j++) dp[i][j] = dp[i-1][j] + dp[i][j-1];\n  return dp[m-1][n-1];\n}",
     "O(mn)", "O(mn)"),
    ("Longest increasing subsequence", "medium", "dp",
     "Length of LIS (not necessarily contiguous).",
     "O(n²) DP or patience (tails binary search) O(n log n).",
     "function lengthOfLIS(a) {\n  const tails = [];\n  for (const x of a) {\n    let lo = 0, hi = tails.length;\n    while (lo < hi) {\n      const m = (lo + hi) >> 1;\n      if (tails[m] < x) lo = m + 1; else hi = m;\n    }\n    tails[lo] = x;\n    if (lo === tails.length) tails.push(x);\n    else tails[lo] = x;\n  }\n  return tails.length;\n}",
     "O(n log n)", "O(n)"),
    ("Word break", "medium", "dp",
     "Can s be segmented into dictionary words?",
     "dp[i] = some j < i where dp[j] and s.slice(j,i) in dict.",
     "function wordBreak(s, wordDict) {\n  const set = new Set(wordDict);\n  const dp = Array(s.length + 1).fill(false);\n  dp[0] = true;\n  for (let i = 1; i <= s.length; i++)\n    for (let j = 0; j < i; j++)\n      if (dp[j] && set.has(s.slice(j, i))) { dp[i] = true; break; }\n  return dp[s.length];\n}",
     "O(n²)", "O(n)"),
    ("Subsets", "medium", "backtrack",
     "All subsets of nums (unique).",
     "Take / skip.",
     "function subsets(nums) {\n  const out = [], path = [];\n  function go(i) {\n    if (i === nums.length) { out.push(path.slice()); return; }\n    path.push(nums[i]); go(i+1); path.pop();\n    go(i+1);\n  }\n  go(0);\n  return out;\n}",
     "O(n 2^n)", "O(n)"),
    ("Permutations", "medium", "backtrack",
     "All permutations of distinct nums.",
     "Used flags.",
     "function permute(nums) {\n  const out = [], path = [], used = Array(nums.length).fill(false);\n  function go() {\n    if (path.length === nums.length) { out.push(path.slice()); return; }\n    for (let i = 0; i < nums.length; i++) {\n      if (used[i]) continue;\n      used[i] = true; path.push(nums[i]); go();\n      path.pop(); used[i] = false;\n    }\n  }\n  go();\n  return out;\n}",
     "O(n · n!)", "O(n)"),
    ("Combination sum", "medium", "backtrack",
     "Combinations of candidates (reuse ok) that sum to target.",
     "Index start. Reuse by not incrementing, or increment after.",
     "function combinationSum(cands, target) {\n  const out = [], path = [];\n  cands.sort((a,b)=>a-b);\n  function go(i, left) {\n    if (left === 0) { out.push(path.slice()); return; }\n    for (let j = i; j < cands.length && cands[j] <= left; j++) {\n      path.push(cands[j]); go(j, left - cands[j]); path.pop();\n    }\n  }\n  go(0, target);\n  return out;\n}",
     "exponential", "O(target/min)"),
    ("Kth largest in array", "medium", "heap",
     "Kth largest element.",
     "Min-heap of size k, or quickselect.",
     "function findKthLargest(nums, k) {\n  nums.sort((a,b)=>b-a);\n  return nums[k-1];\n}\n// Interview: mention heap O(n log k) or quickselect average O(n).",
     "O(n log n) sort / O(n log k) heap", "O(1) sort in place"),
    ("Merge intervals", "medium", "array",
     "Merge overlapping [start,end] intervals.",
     "Sort by start. Stretch end.",
     "function merge(intervals) {\n  intervals.sort((a,b)=>a[0]-b[0]);\n  const out = [intervals[0]];\n  for (let i = 1; i < intervals.length; i++) {\n    const last = out[out.length - 1];\n    if (intervals[i][0] <= last[1]) last[1] = Math.max(last[1], intervals[i][1]);\n    else out.push(intervals[i]);\n  }\n  return out;\n}",
     "O(n log n)", "O(n)"),
    ("Insert interval", "medium", "array",
     "Insert a new interval into non-overlapping sorted list and merge.",
     "Walk: before, overlapping, after.",
     "function insert(intervals, neu) {\n  const out = [];\n  let i = 0;\n  while (i < intervals.length && intervals[i][1] < neu[0]) out.push(intervals[i++]);\n  while (i < intervals.length && intervals[i][0] <= neu[1]) {\n    neu[0] = Math.min(neu[0], intervals[i][0]);\n    neu[1] = Math.max(neu[1], intervals[i][1]);\n    i++;\n  }\n  out.push(neu);\n  while (i < intervals.length) out.push(intervals[i++]);\n  return out;\n}",
     "O(n)", "O(n)"),
    ("Daily temperatures", "medium", "stack",
     "Days until a warmer temperature.",
     "Monotonic decreasing stack of indices.",
     "function dailyTemperatures(t) {\n  const ans = Array(t.length).fill(0), st = [];\n  for (let i = 0; i < t.length; i++) {\n    while (st.length && t[i] > t[st.at(-1)]) {\n      const j = st.pop();\n      ans[j] = i - j;\n    }\n    st.push(i);\n  }\n  return ans;\n}",
     "O(n)", "O(n)"),
    ("Subarray sum equals k", "medium", "prefix",
     "Count subarrays that sum to k.",
     "Prefix + Map of counts.",
     "function subarraySum(nums, k) {\n  const seen = new Map([[0, 1]]);\n  let sum = 0, ans = 0;\n  for (const x of nums) {\n    sum += x;\n    ans += seen.get(sum - k) || 0;\n    seen.set(sum, (seen.get(sum) || 0) + 1);\n  }\n  return ans;\n}",
     "O(n)", "O(n)"),
    ("LRU cache", "medium", "design",
     "get/put O(1), evict least recently used.",
     "Map insertion order (or DLL + Map).",
     "class LRUCache {\n  constructor(cap) { this.cap = cap; this.m = new Map(); }\n  get(k) {\n    if (!this.m.has(k)) return -1;\n    const v = this.m.get(k); this.m.delete(k); this.m.set(k, v); return v;\n  }\n  put(k, v) {\n    if (this.m.has(k)) this.m.delete(k);\n    this.m.set(k, v);\n    if (this.m.size > this.cap) this.m.delete(this.m.keys().next().value);\n  }\n}",
     "O(1)", "O(cap)"),
    ("Implement trie", "medium", "design",
     "insert, search, startsWith.",
     "Map children + end flag.",
     "class Trie {\n  constructor() { this.root = { next: new Map(), end: false }; }\n  _walk(word, create) {\n    let n = this.root;\n    for (const ch of word) {\n      if (!n.next.has(ch)) { if (!create) return null; n.next.set(ch, { next: new Map(), end: false }); }\n      n = n.next.get(ch);\n    }\n    return n;\n  }\n  insert(w) { this._walk(w, true).end = true; }\n  search(w) { const n = this._walk(w, false); return !!(n && n.end); }\n  startsWith(w) { return !!this._walk(w, false); }\n}",
     "O(L)", "O(alphabet × nodes)"),
    ("Word search", "medium", "backtrack",
     "Does word exist in a grid (adjacent cells, no reuse)?",
     "DFS + mark visited.",
     "function exist(board, word) {\n  const R = board.length, C = board[0].length;\n  function dfs(r, c, i) {\n    if (i === word.length) return true;\n    if (r<0||c<0||r>=R||c>=C||board[r][c]!==word[i]) return false;\n    const t = board[r][c]; board[r][c] = '#';\n    const ok = dfs(r+1,c,i+1)||dfs(r-1,c,i+1)||dfs(r,c+1,i+1)||dfs(r,c-1,i+1);\n    board[r][c] = t;\n    return ok;\n  }\n  for (let r=0;r<R;r++) for (let c=0;c<C;c++) if (dfs(r,c,0)) return true;\n  return false;\n}",
     "O(RC · 4^L)", "O(L)"),
    ("Trapping rain water", "hard", "twopointer",
     "How much water after rain on elevation map.",
     "Two pointers + leftMax/rightMax.",
     "function trap(h) {\n  let lo = 0, hi = h.length - 1, L = 0, R = 0, water = 0;\n  while (lo < hi) {\n    if (h[lo] < h[hi]) {\n      L = Math.max(L, h[lo]);\n      water += L - h[lo];\n      lo++;\n    } else {\n      R = Math.max(R, h[hi]);\n      water += R - h[hi];\n      hi--;\n    }\n  }\n  return water;\n}",
     "O(n)", "O(1)"),
    ("Median of two sorted arrays", "hard", "search",
     "Median of two sorted arrays, O(log (m+n)).",
     "Binary search the partition. Say the idea; implement carefully.",
     "function findMedianSortedArrays(a, b) {\n  if (a.length > b.length) return findMedianSortedArrays(b, a);\n  const m = a.length, n = b.length;\n  let lo = 0, hi = m;\n  while (lo <= hi) {\n    const i = (lo + hi) >> 1;\n    const j = ((m + n + 1) >> 1) - i;\n    const aL = i ? a[i-1] : -Infinity, aR = i < m ? a[i] : Infinity;\n    const bL = j ? b[j-1] : -Infinity, bR = j < n ? b[j] : Infinity;\n    if (aL <= bR && bL <= aR) {\n      if ((m+n) % 2) return Math.max(aL, bL);\n      return (Math.max(aL, bL) + Math.min(aR, bR)) / 2;\n    }\n    if (aL > bR) hi = i - 1;\n    else lo = i + 1;\n  }\n}",
     "O(log min(m,n))", "O(1)"),
    ("Serialize / deserialize tree", "hard", "tree",
     "Encode a binary tree to a string and back.",
     "Preorder with null markers.",
     "function serialize(root) {\n  const out = [];\n  function go(n) { if (!n) { out.push('#'); return; } out.push(String(n.val)); go(n.left); go(n.right); }\n  go(root);\n  return out.join(',');\n}\nfunction deserialize(s) {\n  const q = s.split(',');\n  let i = 0;\n  function go() {\n    const v = q[i++];\n    if (v === '#' || v === undefined) return null;\n    return { val: Number(v), left: go(), right: go() };\n  }\n  return go();\n}",
     "O(n)", "O(n)"),
    ("Word ladder", "hard", "graph",
     "Shortest transform from begin to end changing one letter, using wordList.",
     "BFS. Neighbors = words one edit away (wildcard dict).",
     "function ladderLength(begin, end, wordList) {\n  const set = new Set(wordList);\n  if (!set.has(end)) return 0;\n  const q = [[begin, 1]];\n  const seen = new Set([begin]);\n  while (q.length) {\n    const [w, d] = q.shift();\n    if (w === end) return d;\n    for (let i = 0; i < w.length; i++) {\n      for (let c = 97; c <= 122; c++) {\n        const nw = w.slice(0, i) + String.fromCharCode(c) + w.slice(i + 1);\n        if (set.has(nw) && !seen.has(nw)) { seen.add(nw); q.push([nw, d + 1]); }\n      }\n    }\n  }\n  return 0;\n}",
     "O(n · L · 26)", "O(n)"),
]


def problems() -> str:
    blocks = [_p(i, *row) for i, row in enumerate(P, 1)]
    return f'''
<section class="block" id="problems" data-search="DSA JavaScript problem bank" data-stype="Section">
  <p class="kicker">{len(P)} problems · easy → hard</p>
  <h2 class="section-title">Problem bank</h2>
  <p class="lede">Mixed interview order. Each structure already has a <b>Practice this topic</b> gym in its own section — use those first to get fluent, then come here. Solve on paper or in a scratch file. Reveal after you have an idea, then open <b>Explain solution</b> for the walkthrough. Practice items — not claimed official questions. After this bank, grind Phase 1 for more volume.</p>
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
        <option value="array">array</option>
        <option value="hash">hash</option>
        <option value="string">string</option>
        <option value="window">window</option>
        <option value="twopointer">two pointer</option>
        <option value="stack">stack</option>
        <option value="list">list</option>
        <option value="tree">tree</option>
        <option value="graph">graph</option>
        <option value="search">search</option>
        <option value="dp">dp</option>
        <option value="backtrack">backtrack</option>
        <option value="heap">heap</option>
        <option value="prefix">prefix</option>
        <option value="design">design</option>
      </select>
      <input id="filter-text" type="search" placeholder="Filter titles..." />
    </p>
  </div>
  {''.join(blocks)}
</section>
'''
