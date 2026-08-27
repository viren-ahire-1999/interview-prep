P4 = [
{
  "id": "move-zeroes", "name": "Move Zeroes", "diff": "easy", "pattern": "two-pointers", "topic": "arrays",
  "why": "In-place stable partition. Write-index two pointer.",
  "stmt": "Move all zeros to the end, keep the relative order of nonzero values. In-place.",
  "exin": "[0,1,0,3,12]", "exout": "[1,3,12,0,0]",
  "cons": "n up to 10^4.",
  "hints": "Read pointer r, write pointer w. When nums[r]≠0, swap/write to w++.",
  "brute": "Build a new array. Extra space.",
  "opt": "One pass write + fill zeros, or swaps.",
  "steps": "Stability comes from only advancing w on nonzeros.",
  "cx": "O(n) time, O(1) extra.",
  "mistakes": "Unstable swaps (two-pointer from ends). Extra array without asking.",
  "edges": "All zeros. No zeros. Single element.",
  "follow": "Move some other sentinel. Partition odds/evens.",
  "talk": "I will confirm order of nonzeros must be preserved.",
  "sol": """function moveZeroes(nums: number[]): void {
  let w = 0;
  for (let r = 0; r < nums.length; r++) {
    if (nums[r] !== 0) {
      [nums[w], nums[r]] = [nums[r], nums[w]];
      w++;
    }
  }
}"""
},
{
  "id": "missing-number", "name": "Missing Number", "diff": "easy", "pattern": "hashmap-lookup", "topic": "arrays",
  "why": "XOR or Gauss sum. Bit trick that is still practical.",
  "stmt": "Array of n distinct numbers in [0, n] missing exactly one. Return it.",
  "exin": "[3,0,1]", "exout": "2",
  "cons": "n up to 10^4.",
  "hints": "expectedSum = n(n+1)/2. Or XOR 0..n with all elements.",
  "brute": "Set and scan 0..n. O(n) space.",
  "opt": "O(1) space sum or XOR.",
  "steps": "XOR is overflow-safe. Sum needs care in 32-bit langs; JS is fine for these n.",
  "cx": "O(n) time, O(1) space.",
  "mistakes": "Integer overflow speech in Java. Off-by-one on n.",
  "edges": "Missing 0. Missing n. n=1.",
  "follow": "Two missing numbers.",
  "talk": "I will mention both XOR and sum; implement sum for clarity unless they want bits.",
  "sol": """function missingNumber(nums: number[]): number {
  const n = nums.length;
  const expect = (n * (n + 1)) / 2;
  return expect - nums.reduce((a, b) => a + b, 0);
}"""
},
{
  "id": "single-number", "name": "Single Number", "diff": "easy", "pattern": "hashmap-lookup", "topic": "arrays",
  "why": "XOR identity. HashMap is fine; XOR is the follow-up they want.",
  "stmt": "Every element appears twice except one. Find it. O(1) extra preferred.",
  "exin": "[4,1,2,1,2]", "exout": "4",
  "cons": "n up to 3·10^4.",
  "hints": "x^x=0, x^0=x, XOR is commutative.",
  "brute": "Map counts. Sort neighbors.",
  "opt": "XOR all. O(1) space.",
  "steps": "Fold XOR across the array.",
  "cx": "O(n) time, O(1) space.",
  "mistakes": "Thinking XOR needs sorted data.",
  "edges": "Single element. Negatives (still fine in two's complement).",
  "follow": "Every value three times except one (bit counts mod 3).",
  "talk": "I will start with a Map, then upgrade to XOR when they ask for O(1) space.",
  "sol": """function singleNumber(nums: number[]): number {
  return nums.reduce((a, b) => a ^ b, 0);
}"""
},
{
  "id": "happy-number", "name": "Happy Number", "diff": "easy", "pattern": "fast-slow", "topic": "arrays",
  "why": "Cycle detection on a function, not a list. Same Floyd idea.",
  "stmt": "Replace a number by the sum of squares of its digits. Happy iff you reach 1 (otherwise you cycle).",
  "exin": "19", "exout": "true",
  "cons": "n up to 2^31-1.",
  "hints": "Set of seen, or slow/fast on next(n).",
  "brute": "Set until repeat. Small state space.",
  "opt": "Floyd to avoid the set.",
  "steps": "next(n) while n>0: d=n%10; n/=10; acc+=d*d.",
  "cx": "O(log n) per step, tiny cycle. Practically constant.",
  "mistakes": "Infinite loop without a seen set. Integer overflow on d*d in 32-bit.",
  "edges": "1 (true). 0 (false).",
  "follow": "Print the cycle.",
  "talk": "I will use a Set first; mention Floyd as the space flex.",
  "sol": """function isHappy(n: number): boolean {
  const next = (x: number) => {
    let s = 0;
    while (x) { const d = x % 10; s += d * d; x = Math.floor(x / 10); }
    return s;
  };
  const seen = new Set<number>();
  while (n !== 1 && !seen.has(n)) { seen.add(n); n = next(n); }
  return n === 1;
}"""
},
{
  "id": "first-unique", "name": "First Unique Character in a String", "diff": "easy", "pattern": "frequency-counting", "topic": "strings",
  "why": "Two-pass count. Queue/Map variant is the stream version.",
  "stmt": "Index of the first non-repeating character, or -1.",
  "exin": '"leetcode"', "exout": "0",
  "cons": "lowercase, n up to 10^5.",
  "hints": "Count, then scan s again.",
  "brute": "For each i, scan the string. O(n²).",
  "opt": "O(n) two pass, O(1) for 26.",
  "steps": "Do not return during the count pass — later letters can invalidate uniqueness.",
  "cx": "O(n).",
  "mistakes": "Returning during the first pass.",
  "edges": "All repeats. Single char.",
  "follow": "Stream of characters (queue of candidates + counts).",
  "talk": "Two passes are simpler than a clever one-pass.",
  "sol": """function firstUniqChar(s: string): number {
  const c = Array(26).fill(0);
  for (const ch of s) c[ch.charCodeAt(0) - 97]++;
  for (let i = 0; i < s.length; i++) if (c[s.charCodeAt(i) - 97] === 1) return i;
  return -1;
}"""
},
{
  "id": "rev-string", "name": "Reverse String", "diff": "easy", "pattern": "two-pointers", "topic": "strings",
  "why": "Warm-up in-place swap. Use it to start speaking.",
  "stmt": "Reverse an array of characters in-place.",
  "exin": '["h","e","l","l","o"]', "exout": '["o","l","l","e","h"]',
  "cons": "n up to 10^5.",
  "hints": "i,j swap until they meet.",
  "brute": "New array.",
  "opt": "Two pointers.",
  "steps": "While i<j swap.",
  "cx": "O(n) time, O(1) extra.",
  "mistakes": "Off-by-one meeting in the middle.",
  "edges": "Empty. One char. Even/odd length.",
  "follow": "Reverse words in a sentence.",
  "talk": "I will still state complexity. Habits matter.",
  "sol": """function reverseString(s: string[]): void {
  let i = 0, j = s.length - 1;
  while (i < j) { [s[i], s[j]] = [s[j], s[i]]; i++; j--; }
}"""
},
{
  "id": "max-subarray", "name": "Maximum Subarray (Kadane)", "diff": "medium", "pattern": "prefix-sum", "topic": "arrays",
  "why": "Kadane is prefix thinking: extend or restart. Interviewers expect the name.",
  "stmt": "Maximum sum of any nonempty contiguous subarray.",
  "exin": "[-2,1,-3,4,-1,2,1,-5,4]", "exout": "6",
  "cons": "n up to 10^5; negatives allowed.",
  "hints": "bestEndingHere = max(x, bestEndingHere+x).",
  "brute": "All i,j. O(n²).",
  "opt": "Kadane O(n).",
  "steps": "You either start a new subarray at x or extend. Track global max.",
  "cx": "O(n) time, O(1) space.",
  "mistakes": "Initializing best to 0 (fails all-negative). Empty subarray if they forbid it.",
  "edges": "All negative (pick the largest single). Single element.",
  "follow": "Also return the bounds. 2D max subrectangle (Kadane on columns).",
  "talk": "I will initialize with nums[0], not 0.",
  "sol": """function maxSubArray(nums: number[]): number {
  let cur = nums[0], best = nums[0];
  for (let i = 1; i < nums.length; i++) {
    cur = Math.max(nums[i], cur + nums[i]);
    best = Math.max(best, cur);
  }
  return best;
}"""
},
{
  "id": "merge-intervals", "name": "Merge Intervals", "diff": "medium", "pattern": "two-pointers", "topic": "arrays",
  "why": "Sort by start, then linear merge. Calendar / booking flavor — very Atlassian-adjacent.",
  "stmt": "Merge all overlapping [start,end] intervals.",
  "exin": "[[1,3],[2,6],[8,10],[15,18]]", "exout": "[[1,6],[8,10],[15,18]]",
  "cons": "n up to 10^4.",
  "hints": "Sort by start. If cur.start ≤ last.end, last.end = max(ends). Else push a new interval.",
  "brute": "Repeatedly merge any overlapping pair. Ugly.",
  "opt": "Sort O(n log n) + scan.",
  "steps": "Touching endpoints: ask if [1,2][2,3] merge (usually yes).",
  "cx": "O(n log n).",
  "mistakes": "Not sorting. Comparing with the first interval only. Exclusive ends.",
  "edges": "One interval. Fully nested. Already merged.",
  "follow": "Insert interval. Meeting rooms (min heaps on ends).",
  "talk": "I will ask whether touching intervals count as overlap.",
  "sol": """function merge(intervals: number[][]): number[][] {
  intervals.sort((a, b) => a[0] - b[0]);
  const out: number[][] = [intervals[0].slice()];
  for (let i = 1; i < intervals.length; i++) {
    const last = out[out.length - 1], [s, e] = intervals[i];
    if (s <= last[1]) last[1] = Math.max(last[1], e);
    else out.push([s, e]);
  }
  return out;
}"""
},
{
  "id": "insert-interval", "name": "Insert Interval", "diff": "medium", "pattern": "two-pointers", "topic": "arrays",
  "why": "Three-phase scan: before, merge overlapping, after. No full sort if input is already sorted.",
  "stmt": "Non-overlapping intervals sorted by start. Insert newInterval and merge if needed.",
  "exin": "intervals=[[1,3],[6,9]], newInterval=[2,5]", "exout": "[[1,5],[6,9]]",
  "cons": "n up to 10^4.",
  "hints": "Push all with end < new.start. Merge while they overlap. Push the rest.",
  "brute": "Append, call merge intervals.",
  "opt": "One pass O(n).",
  "steps": "Overlap test: not (new.end < cur.start || new.start > cur.end).",
  "cx": "O(n).",
  "mistakes": "Forgetting intervals completely to the right. Mutating newInterval incorrectly.",
  "edges": "Insert at beginning/end. Covers everything. Empty list.",
  "follow": "Range module (hard).",
  "talk": "This is a production-shaped problem: keep the list invariant.",
  "sol": """function insert(intervals: number[][], nw: number[]): number[][] {
  const out: number[][] = [];
  let i = 0, n = intervals.length;
  while (i < n && intervals[i][1] < nw[0]) out.push(intervals[i++]);
  while (i < n && intervals[i][0] <= nw[1]) {
    nw[0] = Math.min(nw[0], intervals[i][0]);
    nw[1] = Math.max(nw[1], intervals[i][1]);
    i++;
  }
  out.push(nw);
  while (i < n) out.push(intervals[i++]);
  return out;
}"""
},
{
  "id": "matrix-zeroes", "name": "Set Matrix Zeroes", "diff": "medium", "pattern": "hashmap-lookup", "topic": "arrays",
  "why": "O(1) extra using first row/col as markers. Careful with the first cell dual meaning.",
  "stmt": "If a cell is 0, set its entire row and column to 0. In-place preferred.",
  "exin": "[[1,1,1],[1,0,1],[1,1,1]]", "exout": "[[1,0,1],[0,0,0],[1,0,1]]",
  "cons": "m,n up to 200.",
  "hints": "First pass mark; second pass set. Use first row/col plus a boolean for col0.",
  "brute": "Copy matrix. O(mn) extra.",
  "opt": "Marker strategy O(1) extra.",
  "steps": "Record whether first row/col need zeroing. Use them as scratch for the rest. Zero rest first, then first row/col.",
  "cx": "O(mn) time, O(1) extra.",
  "mistakes": "Zeroing while scanning (destroys markers). First cell is both row0 and col0 flag.",
  "edges": "First row already zero. 1×1 [0]. No zeros.",
  "follow": "Set to -1 if you cannot use 0 as marker (other sentinels).",
  "talk": "I will mention the O(m+n) boolean arrays first, then the O(1) upgrade.",
  "sol": """function setZeroes(a: number[][]): void {
  const m = a.length, n = a[0].length;
  let col0 = false;
  for (let i = 0; i < m; i++) {
    if (a[i][0] === 0) col0 = true;
    for (let j = 1; j < n; j++) if (a[i][j] === 0) { a[i][0] = 0; a[0][j] = 0; }
  }
  for (let i = m - 1; i >= 0; i--) {
    for (let j = n - 1; j >= 1; j--) if (a[i][0] === 0 || a[0][j] === 0) a[i][j] = 0;
    if (col0) a[i][0] = 0;
  }
}"""
},
{
  "id": "spiral", "name": "Spiral Matrix", "diff": "medium", "pattern": "two-pointers", "topic": "arrays",
  "why": "Boundary walking. Off-by-ones. Clean loops beat clever math.",
  "stmt": "Return matrix elements in spiral order.",
  "exin": "[[1,2,3],[4,5,6],[7,8,9]]", "exout": "[1,2,3,6,9,8,7,4,5]",
  "cons": "m,n up to 10–100.",
  "hints": "top,bottom,left,right. Four loops; shrink; stop when bounds cross.",
  "brute": "Visited matrix + direction vectors. Also O(mn) and often cleaner.",
  "opt": "Either style is fine.",
  "steps": "After a row or column, shrink that bound. Guard each loop because a single row/col remains.",
  "cx": "O(mn).",
  "mistakes": "Double-visiting corners. Not stopping on a single remaining row.",
  "edges": "1×n. n×1. 1×1.",
  "follow": "Spiral generate 1..n².",
  "talk": "I prefer visited+dirs if I have time — fewer bound bugs.",
  "sol": """function spiralOrder(a: number[][]): number[] {
  const out: number[] = [];
  let t = 0, b = a.length - 1, l = 0, r = a[0].length - 1;
  while (t <= b && l <= r) {
    for (let j = l; j <= r; j++) out.push(a[t][j]); t++;
    for (let i = t; i <= b; i++) out.push(a[i][r]); r--;
    if (t <= b) { for (let j = r; j >= l; j--) out.push(a[b][j]); b--; }
    if (l <= r) { for (let i = b; i >= t; i--) out.push(a[i][l]); l++; }
  }
  return out;
}"""
},
{
  "id": "word-search", "name": "Word Search", "diff": "medium", "pattern": "dfs", "topic": "graphs",
  "why": "Backtracking on a grid. Mark/unmark. Phase 1 backtracking representative.",
  "stmt": "Does word exist in the grid as a path of adjacent cells (no reuse)?",
  "exin": "board AB/CD, word 'ABD' etc.", "exout": "true/false",
  "cons": "board small (e.g. 6×6) but word up to 15; still exponential — pruning matters.",
  "hints": "DFS from every start. Mark visited, recurse 4 dirs, unmark.",
  "brute": "That's the solution; prune on mismatch.",
  "opt": "Backtracking. Optional: count letters to reject early.",
  "steps": "If index===word.length success. Bounds and letter match. Toggle cell to '#' then restore.",
  "cx": "O(mn · 4^L) worst. Space O(L).",
  "mistakes": "Not unmarking. Reusing a cell. 8-connected.",
  "edges": "Word longer than mn. Single letter. Word uses the same letter twice from different cells.",
  "follow": "Word search II (trie + DFS) — later.",
  "talk": "I will mention complexity honestly; this is exponential and that is OK for small boards.",
  "sol": """function exist(board: string[][], word: string): boolean {
  const R = board.length, C = board[0].length;
  const dfs = (r: number, c: number, k: number): boolean => {
    if (k === word.length) return true;
    if (r < 0 || c < 0 || r >= R || c >= C || board[r][c] !== word[k]) return false;
    const ch = board[r][c]; board[r][c] = "#";
    const ok = dfs(r+1,c,k+1) || dfs(r-1,c,k+1) || dfs(r,c+1,k+1) || dfs(r,c-1,k+1);
    board[r][c] = ch;
    return ok;
  };
  for (let r = 0; r < R; r++)
    for (let c = 0; c < C; c++)
      if (dfs(r, c, 0)) return true;
  return false;
}"""
},
{
  "id": "climbing", "name": "Climbing Stairs", "diff": "easy", "pattern": "prefix-sum", "topic": "arrays",
  "why": "Fibonacci DP in disguise. One easy DP so you can talk about recurrence.",
  "stmt": "n stairs, 1 or 2 steps. Number of distinct ways to the top.",
  "exin": "n = 3", "exout": "3",
  "cons": "n up to 45.",
  "hints": "ways(n)=ways(n-1)+ways(n-2).",
  "brute": "Recursion exponential.",
  "opt": "Two variables rolling O(n) time O(1) space.",
  "steps": "a=1,b=1; repeat n-1 times: [a,b]=[b,a+b]. Return b for n≥1 with a=1 (0 stairs) careful.",
  "cx": "O(n).",
  "mistakes": "Off-by-one base cases. Recursion without memo in an interview.",
  "edges": "n=1. n=2.",
  "follow": "1..k steps. Min cost climbing.",
  "talk": "I will write the recurrence first, then the rolling vars.",
  "sol": """function climbStairs(n: number): number {
  let a = 1, b = 1;
  for (let i = 2; i <= n; i++) { const t = a + b; a = b; b = t; }
  return b;
}"""
},
{
  "id": "house-robber", "name": "House Robber", "diff": "medium", "pattern": "prefix-sum", "topic": "arrays",
  "why": "Linear DP: take or skip. Clean state definition.",
  "stmt": "Array of house money. Cannot rob adjacent houses. Max money.",
  "exin": "[2,7,9,3,1]", "exout": "12",
  "cons": "n up to 100.",
  "hints": "dp[i] = max(dp[i-1], dp[i-2]+nums[i]).",
  "brute": "Subsets with gap constraint. Exponential.",
  "opt": "O(n) rolling two variables.",
  "steps": "prev2, prev1. For x: next = max(prev1, prev2+x).",
  "cx": "O(n) time, O(1) space.",
  "mistakes": "Using dp[i-2] without guarding i<2. Circular houses (House Robber II) without splitting cases.",
  "edges": "One house. Two houses. Zeros.",
  "follow": "Circular street. Binary tree houses.",
  "talk": "I will define the state in words before the formula.",
  "sol": """function rob(nums: number[]): number {
  let prev2 = 0, prev1 = 0;
  for (const x of nums) {
    const cur = Math.max(prev1, prev2 + x);
    prev2 = prev1; prev1 = cur;
  }
  return prev1;
}"""
},
{
  "id": "same-tree", "name": "Same Tree", "diff": "easy", "pattern": "tree-recursion", "topic": "trees",
  "why": "Structural equality. Base cases: both null, one null, values differ.",
  "stmt": "Are two binary trees structurally identical with the same values?",
  "exin": "two equal small trees", "exout": "true",
  "cons": "n up to 100.",
  "hints": "p===q null; if !p||!q false; vals equal and recurse.",
  "brute": "Serialize and compare strings (fragile).",
  "opt": "DFS O(n).",
  "steps": "Short-circuit on mismatch.",
  "cx": "O(n).",
  "mistakes": "Comparing only values in level order (misses structure).",
  "edges": "Both empty. One empty.",
  "follow": "Subtree of another tree.",
  "talk": "Four lines if the base cases are clean.",
  "sol": """function isSameTree(p: TreeNode | null, q: TreeNode | null): boolean {
  if (!p && !q) return true;
  if (!p || !q || p.val !== q.val) return false;
  return isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
}"""
},
{
  "id": "symmetric", "name": "Symmetric Tree", "diff": "easy", "pattern": "tree-recursion", "topic": "trees",
  "why": "Mirror comparison: left.left vs right.right.",
  "stmt": "Is the tree a mirror of itself?",
  "exin": "the classic mirrored 1-2-2 tree", "exout": "true",
  "cons": "n up to 1000.",
  "hints": "Helper mirror(a,b).",
  "brute": "Build inverted copy, sameTree — extra work.",
  "opt": "Paired DFS or BFS two queues.",
  "steps": "mirror(a,b): both null; one null; vals; mirror(a.left,b.right) && mirror(a.right,b.left).",
  "cx": "O(n).",
  "mistakes": "Comparing left-left with right-left.",
  "edges": "Empty. Single node. One-sided.",
  "follow": "Invert then sameTree vs this — discuss.",
  "talk": "I will write the helper signature first.",
  "sol": """function isSymmetric(root: TreeNode | null): boolean {
  const mir = (a: TreeNode | null, b: TreeNode | null): boolean => {
    if (!a && !b) return true;
    if (!a || !b || a.val !== b.val) return false;
    return mir(a.left, b.right) && mir(a.right, b.left);
  };
  return !root || mir(root.left, root.right);
}"""
},
{
  "id": "path-sum", "name": "Path Sum", "diff": "easy", "pattern": "tree-recursion", "topic": "trees",
  "why": "Root-to-leaf, not any path. Leaf definition matters.",
  "stmt": "Exists a root-to-leaf path whose values sum to target?",
  "exin": "target 22 on the classic tree", "exout": "true",
  "cons": "n up to 5000.",
  "hints": "Subtract node.val. At a leaf, check === 0 after subtract (or === target).",
  "brute": "All paths enumerated.",
  "opt": "DFS O(n).",
  "steps": "A node with one child is not a leaf. Check !left && !right.",
  "cx": "O(n).",
  "mistakes": "Any-node-to-any-node (different problem). Counting a one-child node as leaf.",
  "edges": "Empty (false). Negative values. Target 0.",
  "follow": "All path sums (list). Path sum III (any downward path).",
  "talk": "I will define leaf out loud.",
  "sol": """function hasPathSum(root: TreeNode | null, target: number): boolean {
  if (!root) return false;
  if (!root.left && !root.right) return root.val === target;
  return hasPathSum(root.left, target - root.val) || hasPathSum(root.right, target - root.val);
}"""
},
{
  "id": "queue-stacks", "name": "Implement Queue using Stacks", "diff": "easy", "pattern": "stack", "topic": "stack",
  "why": "Amortized O(1). Two stacks: in and out.",
  "stmt": "FIFO queue via stacks: push, pop, peek, empty.",
  "exin": "push 1, push 2, peek → 1", "exout": "1",
  "cons": "ops up to 100.",
  "hints": "in stack for push. When out is empty, flush in→out (reverses order).",
  "brute": "shift an array — they want the two-stack idea.",
  "opt": "Amortized O(1) pop/peek.",
  "steps": "Each element moves at most twice.",
  "cx": "Amortized O(1), worst O(n) pop when flushing.",
  "mistakes": "Flushing every pop even if out is nonempty (breaks order).",
  "edges": "Pop after alternating push/pop.",
  "follow": "Stack using queues.",
  "talk": "I will say amortized and when the expensive flush happens.",
  "sol": """class MyQueue {
  in: number[] = [];
  out: number[] = [];
  push(x: number) { this.in.push(x); }
  private pour() { if (!this.out.length) while (this.in.length) this.out.push(this.in.pop()!); }
  pop() { this.pour(); return this.out.pop()!; }
  peek() { this.pour(); return this.out.at(-1)!; }
  empty() { return !this.in.length && !this.out.length; }
}"""
},
{
  "id": "lca-bt", "name": "Lowest Common Ancestor of a Binary Tree", "diff": "medium", "pattern": "tree-recursion", "topic": "trees",
  "why": "General tree LCA (not BST). Return node if found in subtree; combine.",
  "stmt": "Binary tree, p and q exist. Return LCA (a node can be an ancestor of itself).",
  "exin": "p and q in different subtrees of a node", "exout": "that node",
  "cons": "n up to 10^5 in some versions — O(n) is required.",
  "hints": "If node is p or q, return node. Recurse L,R. If both non-null, node is LCA.",
  "brute": "Parent map + ancestor set.",
  "opt": "Single DFS O(n).",
  "steps": "Both sides return non-null → current. Else bubble the non-null side.",
  "cx": "O(n) time, O(h) space.",
  "mistakes": "Using BST walk on a non-BST. Assuming p is left of q.",
  "edges": "p is root. p is ancestor of q.",
  "follow": "Parent pointers given. LCA queries many times (binary lifting — later).",
  "talk": "I will contrast this with the BST walk from earlier.",
  "sol": """function lowestCommonAncestorBT(root: TreeNode | null, p: TreeNode, q: TreeNode): TreeNode | null {
  if (!root || root === p || root === q) return root;
  const L = lowestCommonAncestorBT(root.left, p, q);
  const R = lowestCommonAncestorBT(root.right, p, q);
  if (L && R) return root;
  return L ?? R;
}"""
},
{
  "id": "encode-strings", "name": "Encode and Decode Strings", "diff": "medium", "pattern": "hashmap-lookup", "topic": "strings",
  "why": "Serialization. Length-prefix beats joining with a delimiter that can appear in data.",
  "stmt": "Design encode(strs) → string and decode(s) → original array. Strings may contain any ASCII, including your delimiter.",
  "exin": '["leet","code",""]', "exout": "round-trips",
  "cons": "Total length moderate; correctness of framing is the point.",
  "hints": "For each word: `${len}#${word}`. Decode by reading len, then slice.",
  "brute": "JSON.stringify — mention it, then implement a manual codec if they want.",
  "opt": "Length prefix.",
  "steps": "Never search for a raw delimiter inside the payload without a length.",
  "cx": "O(total chars).",
  "mistakes": "join('#') when words contain '#'. Not handling empty strings.",
  "edges": "Empty list. Empty word. Words with digits and #.",
  "follow": "Streaming decode. Unicode code points vs UTF-16 length.",
  "talk": "This is a frontend-flavored design problem: specify the frame format first.",
  "sol": """function encode(strs: string[]): string {
  return strs.map((w) => `${w.length}#${w}`).join("");
}
function decode(s: string): string[] {
  const out: string[] = [];
  let i = 0;
  while (i < s.length) {
    const j = s.indexOf("#", i);
    const len = Number(s.slice(i, j));
    out.push(s.slice(j + 1, j + 1 + len));
    i = j + 1 + len;
  }
  return out;
}"""
},
{
  "id": "intersection", "name": "Intersection of Two Arrays II", "diff": "easy", "pattern": "frequency-counting", "topic": "arrays",
  "why": "Multiset intersection. Follow-up: sorted? streaming?",
  "stmt": "Intersection including duplicates (min count in both). Order anything.",
  "exin": "[1,2,2,1], [2,2]", "exout": "[2,2]",
  "cons": "n,m up to 1000.",
  "hints": "Count the smaller array, walk the other decrementing.",
  "brute": "For each x in A, scan B and mark used.",
  "opt": "Map counts O(n+m). If sorted, two pointers.",
  "steps": "Senior move: ask if arrays are sorted and if one is on disk.",
  "cx": "O(n+m) time, O(min(n,m)) space.",
  "mistakes": "Set intersection (drops duplicates).",
  "edges": "No overlap. All duplicates.",
  "follow": "What if nums1 is tiny and nums2 is a stream? What if both sorted?",
  "talk": "I will lead with follow-ups — this problem is designed for them.",
  "sol": """function intersect(a: number[], b: number[]): number[] {
  const freq = new Map<number, number>();
  for (const x of a) freq.set(x, (freq.get(x) ?? 0) + 1);
  const out: number[] = [];
  for (const x of b) {
    const n = freq.get(x) ?? 0;
    if (n) { out.push(x); freq.set(x, n - 1); }
  }
  return out;
}"""
},
]
