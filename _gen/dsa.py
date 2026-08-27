import html as _html

def _code(lang: str, src: str) -> str:
    return (
        f'<div class="code-block"><div class="code-head"><span>{lang}</span>'
        f'<button type="button" class="copy-btn">Copy</button></div>'
        f"<pre><code>{_html.escape(src)}</code></pre></div>"
    )


def _topic(tid, title, search, body, complete_group="topics"):
    return f'''
<article class="topic" id="{tid}" data-search="{search}" data-stype="DSA topic">
  <h3>{title}</h3>
  {body}
  <p><button type="button" class="toggle-btn" data-complete="{complete_group}" data-cid="{tid}">Mark complete</button></p>
</article>
'''


def dsa_curriculum() -> str:
    o1 = _code("TypeScript", """function first(nums: number[]): number | undefined {
  return nums[0]; // O(1) time, O(1) extra space
}""")
    olog = _code("TypeScript", """function binarySearch(a: number[], t: number): number {
  let lo = 0, hi = a.length - 1;
  while (lo <= hi) {            // halves each step → O(log n)
    const mid = (lo + hi) >> 1;
    if (a[mid] === t) return mid;
    if (a[mid] < t) lo = mid + 1;
    else hi = mid - 1;
  }
  return -1;
}""")
    on = _code("TypeScript", """function maxVal(a: number[]): number {
  let m = -Infinity;
  for (const x of a) if (x > m) m = x; // one pass → O(n)
  return m;
}""")
    onlog = _code("TypeScript", """function sortedCopy(a: number[]): number[] {
  return [...a].sort((x, y) => x - y); // typical comparison sort O(n log n)
}""")
    on2 = _code("TypeScript", """function hasPairSumSlow(a: number[], t: number): boolean {
  for (let i = 0; i < a.length; i++) {
    for (let j = i + 1; j < a.length; j++) { // ~ n²/2 → O(n²)
      if (a[i] + a[j] === t) return true;
    }
  }
  return false;
}""")
    twoN = _code("TypeScript", """function fibExp(n: number): number {
  if (n <= 1) return n;
  return fibExp(n - 1) + fibExp(n - 2); // two branches, overlapping → ~O(2^n)
}""")
    hashmap = _code("TypeScript", """const freq = new Map<string, number>();
for (const ch of s) freq.set(ch, (freq.get(ch) ?? 0) + 1);
// Average get/set: O(1). Worst case (pathological hash): O(n).
// V8's Map is engineered; still quote "average O(1)" in interviews.""")

    bigo = _topic("bigo-topic", "1. Big O — interview-ready analysis", "Big O complexity", f'''
  <p>Big O is a language for <b>how work grows as input grows</b>, ignoring constants and lower-order terms. Interviewers want two things: (1) you can read your own code and assign a class, (2) you can use that class to choose a better structure.</p>
  <h4>Mental model</h4>
  <p>Ask: if <code>n</code> doubles, does the work stay the same, grow a little, grow linearly, or explode? That single question separates O(1) from O(log n) from O(n) from O(n²) from exponential.</p>
  <table>
    <tr><th>Class</th><th>Growth feel</th><th>Typical cause</th><th>n = 10<sup>6</sup> vibe</th></tr>
    <tr><td>O(1)</td><td>Independent of n</td><td>Index, HashMap avg, arithmetic</td><td>Always fine</td></tr>
    <tr><td>O(log n)</td><td>Halves the space</td><td>Binary search, balanced tree height</td><td>~20 steps</td></tr>
    <tr><td>O(n)</td><td>One pass</td><td>Scan, two pointers, linear window</td><td>Fine</td></tr>
    <tr><td>O(n log n)</td><td>Sort-shaped</td><td>Comparison sort, some heap work</td><td>Usually fine</td></tr>
    <tr><td>O(n²)</td><td>Pair every i with j</td><td>Nested loops over n</td><td>Often too slow</td></tr>
    <tr><td>O(2<sup>n</sup>)</td><td>Branching recursion</td><td>Subsets, naive Fibonacci</td><td>Only tiny n</td></tr>
    <tr><td>O(n!)</td><td>Permutations</td><td>Try every ordering</td><td>n ≤ ~10</td></tr>
  </table>
  <h4>Visual scale</h4>
  <div class="diagram">n=16
O(1)      █
O(log n)  ███
O(n)      ████████████████
O(n log n)████████████████████████████████████████████
O(n²)     (256 units — already 16× a linear scan)
O(2^n)    65536
O(n!)     20,922,789,888,000</div>
  <h4>JavaScript examples</h4>
  {o1}{olog}{on}{onlog}{on2}{twoN}{hashmap}
  <h4>How to analyze nested loops</h4>
  <p>Multiply independent iterations: <code>for i in 0..n</code> around <code>for j in 0..n</code> is O(n²). If the inner loop is <code>j = i..n</code>, it is still O(n²) (the 1/2 is a constant). If the inner loop is binary search, you get O(n log n). If the inner loop walks a shrinking window that only moves forward across the whole algorithm, it may collapse to O(n) — that is the sliding-window argument.</p>
  <h4>Amortized complexity</h4>
  <p>Amortized means <b>average cost per operation over a worst-case sequence</b>, not “average input.” Dynamic array (JS <code>Array.push</code>) is O(1) amortized: most pushes are cheap; rare resizes copy 2k items, but that cost is paid off by the next k cheap pushes. Hash table rehash is the same story.</p>
  <h4>Average vs worst case</h4>
  <p>HashMap lookup is O(1) average, O(n) worst if everything collides. In interviews, say: “Engineered hash maps are treated as O(1) expected; I would mention the theoretical worst case if the interviewer is probing.” Quicksort is O(n log n) expected, O(n²) worst (sorted input + naive pivot). Heapsort/mergesort give deterministic O(n log n).</p>
  <h4>Interview answers</h4>
  <ul class="tight">
    <li><b>HashMap lookup?</b> Expected O(1) time, O(n) space for n keys.</li>
    <li><b>Why is binary search O(log n)?</b> Each comparison discards half the remaining range. Starting from n, you can halve only about log₂ n times before one element remains.</li>
    <li><b>Why is sorting usually O(n log n)?</b> Comparison sorts have an Ω(n log n) lower bound: there are n! orderings, and each comparison has 2 outcomes, so you need ~ log₂(n!) ≈ n log n comparisons. Counting/radix sort can beat that when keys are integers with extra structure.</li>
    <li><b>Space complexity?</b> Extra memory besides the input. Recursion depth counts. In-place reverse is O(1) extra; generating a new array is O(n).</li>
  </ul>
  <div class="callout warn"><b>Senior bar:</b> After coding, state time and space, then say what you would change if n were 10⁸ or if you were memory-constrained. That is the Atlassian-style trade-off sentence.</div>
''')

    arrays = _topic("dsa-arrays", "2. Arrays", "Arrays DSA", f'''
  <p><b>What it is.</b> A contiguous (or contiguous-feeling) indexed sequence. In JavaScript, <code>Array</code> is a specialized object with a <code>length</code> and index keys; for interview purposes treat it as a dynamic array with O(1) index and O(1) amortized push.</p>
  <p><b>When to use it.</b> Order matters, you need random access, or you will scan linearly. Most interview inputs start as arrays.</p>
  <p><b>Mental model.</b> Index is an address. You can jump to <code>a[i]</code> instantly, but inserting at the front shifts everyone — O(n).</p>
  <p><b>Common patterns.</b> Prefix/suffix passes, in-place two-pointer writes, treating the array as a hash via index (cyclic sort / marking), 2D grids as arrays of arrays.</p>
  <p><b>When not to use it.</b> You need O(1) insert/delete in the middle (use a list or map). You need ordered keys (use a tree / sort once). You need uniqueness with no order (use Set).</p>
  <p><b>Complexity.</b> Index O(1). Scan O(n). Unshift/splice-at-0 O(n). Sort O(n log n).</p>
  {_code("TypeScript", """// In-place compact: write unique values forward
function compactSorted(a: number[]): number {
  if (a.length === 0) return 0;
  let w = 1;
  for (let r = 1; r < a.length; r++) {
    if (a[r] !== a[w - 1]) a[w++] = a[r];
  }
  return w;
}""")}
  <p><b>Common mistakes.</b> Off-by-one on <code>i &lt; n</code> vs <code>i &lt;= n-1</code>. Mutating while iterating. Assuming <code>sort()</code> is numeric (it is lexicographic unless you pass a comparator).</p>
  <p><b>Edge cases.</b> Empty array, single element, all duplicates, already sorted, integer overflow if you ever used 32-bit (JS number is IEEE-754; still mention overflow if the prompt is language-agnostic).</p>
''')

    strings = _topic("dsa-strings", "3. Strings", "Strings DSA", f'''
  <p><b>What it is.</b> An immutable sequence of UTF-16 code units in JavaScript. <code>s[i]</code> and <code>s.length</code> are fine for interview ASCII/Unicode-BMP problems. Grapheme clusters (emoji) are almost never the point in DSA rounds.</p>
  <p><b>When to use string-specific thinking.</b> Anagrams, palindromes, windows over characters, parsing, run-length, prefix/suffix of words.</p>
  <p><b>Mental model.</b> A string is an array of characters you cannot mutate. Building with <code>+=</code> in a loop can be O(n²) in naive implementations; prefer <code>array.push</code> then <code>join('')</code> when constructing large strings.</p>
  <p><b>Common patterns.</b> Frequency maps of 26 letters, sliding window on unique chars, two pointers from ends, sort-as-key for anagrams, KMP/Z only if they explicitly want it (rare at Atlassian).</p>
  <p><b>When not.</b> Do not explode a string into recursion without a bound. Do not use regex as a substitute for a linear scan in an interview unless it clarifies parsing.</p>
  {_code("TypeScript", """function isPalindrome(s: string): boolean {
  const t = s.toLowerCase().replace(/[^a-z0-9]/g, "");
  let i = 0, j = t.length - 1;
  while (i < j) {
    if (t[i] !== t[j]) return false;
    i++; j--;
  }
  return true;
}""")}
  <p><b>Mistakes.</b> Forgetting case/punctuation in palindromes. Using <code>sort</code> on strings of length n inside an O(n) loop (becomes O(n² log n)). Confusing index of a character with its code.</p>
''')

    hashmap = _topic("dsa-hashmap", "4. HashMap", "HashMap DSA", f'''
  <p><b>What it is.</b> An associative array: key → value with expected O(1) get/set/delete. In JS: <code>Map</code> (any key, insertion order) or object (string/symbol keys). Prefer <code>Map</code> in TypeScript interviews unless you need a JSON object.</p>
  <p><b>Why it helps.</b> It turns “have I seen this before?” from a scan (O(n)) into a lookup (O(1)). That is the most common Easy→Medium upgrade in screening interviews.</p>
  <p><b>When to use it.</b> Complements (Two Sum), grouping (anagrams), counting (top K), last-seen index (longest unique substring), prefix-sum complements (subarray sum K), graph adjacency.</p>
  <p><b>Mental model.</b> Hash the key, land in a bucket, compare. You pay memory to buy time. If you cannot define a stable key (e.g. unsorted list as key), the map will not save you until you canonicalize.</p>
  <p><b>When it breaks down.</b> Keys that are mutable and then mutated. Huge key spaces you cannot afford to store. Need for ordered range queries (use sort + two pointers or a tree). Need for “next greater” (stack) rather than “have I seen.”</p>
  <p><b>Complexity.</b> Average O(1) per op, O(n) space. Worst O(n) per op theoretically.</p>
  {_code("TypeScript", """function twoSum(nums: number[], target: number): [number, number] {
  const seen = new Map<number, number>(); // value → index
  for (let i = 0; i < nums.length; i++) {
    const want = target - nums[i];
    const j = seen.get(want);
    if (j !== undefined) return [j, i];
    seen.set(nums[i], i);
  }
  throw new Error("no pair");
}""")}
  <p><b>Interview recognition.</b> Words like “pair,” “complement,” “group,” “count,” “last index,” “first unique,” “is there a previous value that…”</p>
  <p><b>Mistakes.</b> Using the object itself as a key without canonicalization. Forgetting that object keys stringify. Overwriting an index you still needed (Two Sum: store after lookup).</p>
''')

    set_t = _topic("dsa-set", "5. Set", "Set DSA", f'''
  <p><b>What it is.</b> A HashMap that only stores keys. JS <code>Set</code> has O(1) average <code>has</code>/<code>add</code>/<code>delete</code> and insertion order.</p>
  <p><b>When to use it.</b> Dedup, membership, “start of a sequence” tests (Longest Consecutive), visited nodes in a graph when you do not need extra payload.</p>
  <p><b>When not.</b> You need the associated value (use Map). You need the k-th smallest (use sort/heap). You need multiset counts (use Map).</p>
  {_code("TypeScript", """function hasDuplicate(nums: number[]): boolean {
  const s = new Set<number>();
  for (const x of nums) {
    if (s.has(x)) return true;
    s.add(x);
  }
  return false;
}""")}
  <p><b>Trap.</b> <code>new Set(nums).size !== nums.length</code> is a valid one-liner for duplicates, but say the O(n) time / O(n) space out loud. Sorting first is O(n log n) time, O(1) extra if in-place — mention that trade-off.</p>
''')

    tp = _topic("dsa-twopointers", "6. Two Pointers", "Two Pointers DSA", f'''
  <p><b>What it is.</b> Two indices moving through a sequence under an invariant, usually toward each other or in the same direction at different speeds.</p>
  <p><b>When to use it.</b> Sorted arrays (Two Sum II, 3Sum). Palindromes. In-place partitioning. Fast/slow on lists. Container-with-water (greedy move of the shorter side).</p>
  <p><b>Mental model.</b> Each move must discard a region that cannot contain a better answer. If you cannot justify the discard, you do not have a two-pointer proof — you have a hope.</p>
  <p><b>When not.</b> Unsorted pair-sum without extra memory (need HashMap or sort first). Non-monotonic constraints where moving a pointer can skip the optimum.</p>
  <p><b>Complexity.</b> Typically O(n) after an O(n log n) sort, O(1) extra.</p>
  {_code("TypeScript", """function maxArea(h: number[]): number {
  let i = 0, j = h.length - 1, best = 0;
  while (i < j) {
    best = Math.max(best, Math.min(h[i], h[j]) * (j - i));
    if (h[i] < h[j]) i++; else j--; // shorter line cannot win later with this partner
  }
  return best;
}""")}
  <p><b>Mistakes.</b> Forgetting to skip duplicates in 3Sum. Moving both pointers in one step and skipping the answer. Using two pointers on unsorted data and claiming O(n).</p>
''')

    sw = _topic("dsa-window", "7. Sliding Window", "Sliding Window DSA", f'''
  <p><b>What it is.</b> A contiguous segment <code>[left, right]</code> that you expand and shrink so that a constraint stays valid. The window only moves forward — each index enters and leaves at most once.</p>
  <p><b>When to use it.</b> Longest/shortest subarray or substring with a constraint: at most K distinct, no repeats, sum ≥ target, contains all chars of t, anagram of p.</p>
  <p><b>Mental model / invariant.</b> After every <code>right++</code>, repair the window with <code>left++</code> until it is valid (or until it is minimal-valid, depending on the problem). The invariant is “window always represents the best candidate ending at <code>right</code>” or “window is the smallest valid covering <code>right</code>.”</p>
  <p><b>When not.</b> Subarrays that are not contiguous. Constraints that are not repairable by moving left (e.g. arbitrary subset sum — that is DP or prefix+map). Need the actual subarray list of all answers that overlap in complex ways.</p>
  <p><b>Complexity.</b> O(n) time, O(Σ) space for the alphabet or the map of counts.</p>
  {_code("TypeScript", """function lengthOfLongestSubstring(s: string): number {
  const last = new Map<string, number>();
  let left = 0, best = 0;
  for (let r = 0; r < s.length; r++) {
    const prev = last.get(s[r]);
    if (prev !== undefined && prev >= left) left = prev + 1;
    last.set(s[r], r);
    best = Math.max(best, r - left + 1);
  }
  return best;
}""")}
  <p><b>Mistakes.</b> Updating <code>left</code> incorrectly when a character was seen <i>before</i> the window. Forgetting to count “need” vs “have” in min-window. Using a nested O(n) shrink that rescans instead of O(1) updates.</p>
''')

    prefix = _topic("dsa-prefix", "8. Prefix Sum", "Prefix Sum DSA", f'''
  <p><b>What it is.</b> Precompute <code>pref[i] = a[0]+…+a[i-1]</code> so any range sum is <code>pref[r]-pref[l]</code> in O(1). The 2D analog is a summed-area table.</p>
  <p><b>When to use it.</b> Many range-sum queries. “How many subarrays sum to K” (map of prefix frequencies). Equilibrium / pivot index. Difference arrays for range updates (inverse idea).</p>
  <p><b>Mental model.</b> A subarray sum is the difference of two prefixes. If you need <code>pref[r] - pref[l] = K</code>, then <code>pref[l] = pref[r] - K</code> — look that up in a map.</p>
  <p><b>When not.</b> You need min/max of a range with updates (segment tree — out of Phase 1 scope). The constraint is about distinct characters (window), not sums.</p>
  {_code("TypeScript", """function subarraySum(nums: number[], k: number): number {
  const freq = new Map<number, number>([[0, 1]]);
  let pref = 0, ans = 0;
  for (const x of nums) {
    pref += x;
    ans += freq.get(pref - k) ?? 0;
    freq.set(pref, (freq.get(pref) ?? 0) + 1);
  }
  return ans;
}""")}
  <p><b>Trap.</b> Initialize the map with prefix 0 seen once — the subarray that starts at index 0. Negative numbers make sliding window on sums invalid; prefix+map still works.</p>
''')

    stack = _topic("dsa-stack", "9. Stack", "Stack DSA", f'''
  <p><b>What it is.</b> LIFO. JS array <code>push</code>/<code>pop</code>. The algorithmic power is <b>monotonic stacks</b>: keep indices in increasing or decreasing order of values so the top is the previous candidate.</p>
  <p><b>When to use it.</b> Parentheses / path simplification. Calculator / RPN. Next greater/smaller element. Histogram rectangle. Nested structures (HTML-ish, file paths). Undo.</p>
  <p><b>When not.</b> You need the oldest item first (queue/BFS). You need random access to the middle.</p>
  {_code("TypeScript", """function dailyTemperatures(t: number[]): number[] {
  const ans = Array(t.length).fill(0);
  const st: number[] = []; // indices, temps decreasing
  for (let i = 0; i < t.length; i++) {
    while (st.length && t[i] > t[st[st.length - 1]]) {
      const j = st.pop()!;
      ans[j] = i - j;
    }
    st.push(i);
  }
  return ans;
}""")}
  <p><b>Complexity.</b> Each index pushed/popped once → O(n).</p>
  <p><b>Mistakes.</b> Storing values instead of indices when you need distance. Popping the equality case incorrectly on histogram.</p>
''')

    queue = _topic("dsa-queue", "10. Queue", "Queue DSA", f'''
  <p><b>What it is.</b> FIFO. In JS interviews, use an array with a read index (<code>head++</code>) or a circular buffer. <code>shift()</code> is O(n) — mention that and avoid it on large queues.</p>
  <p><b>When to use it.</b> BFS, sliding-window maximum (deque), task scheduling, level-order trees, multi-source infection (oranges).</p>
  <p><b>When not.</b> DFS/recursion already gives you a stack. You need priority (heap), not arrival order.</p>
  {_code("TypeScript", """class Queue<T> {{
  private a: T[] = [];
  private h = 0;
  push(x: T) {{ this.a.push(x); }}
  shift(): T | undefined {{
    if (this.h >= this.a.length) return undefined;
    const v = this.a[this.h++];
    if (this.h > 32 && this.h * 2 > this.a.length) {{
      this.a = this.a.slice(this.h); this.h = 0;
    }}
    return v;
  }}
  get length() {{ return this.a.length - this.h; }}
}}""".replace("{{", "{").replace("}}", "}"))}
''')

    bs = _topic("dsa-bs", "11. Binary Search", "Binary Search DSA", f'''
  <p><b>What it is.</b> Repeatedly cut a <b>monotonic</b> search space in half. The space can be indices of a sorted array, or the space of <i>answers</i> (minimum speed, minimum capacity) when <code>feasible(x)</code> is monotonic.</p>
  <p><b>Mental model.</b> Maintain an invariant: the answer lives in <code>[lo, hi]</code>. After testing <code>mid</code>, discard the half that cannot contain it. Overflow-safe mid: <code>lo + ((hi-lo)>>1)</code> (JS numbers are floats; still a good habit).</p>
  <p><b>When not.</b> The predicate is not monotonic (“exists a subarray of length k with property that is not monotone in k”). Unsorted data with no other structure.</p>
  {_code("TypeScript", """function firstTrue(n: number, ok: (x: number) => boolean): number {
  let lo = 0, hi = n; // answer in [0, n]
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (ok(mid)) hi = mid;
    else lo = mid + 1;
  }
  return lo;
}""")}
  <p><b>Interview questions.</b> Why O(log n)? What if duplicates? How do you search a rotated array? How do you binary-search the answer for Koko?</p>
  <p><b>Mistakes.</b> Infinite loops from <code>lo = mid</code> when <code>lo</code> and <code>hi</code> are adjacent. Off-by-one on “insert position.” Forgetting the array must be sorted (or the predicate monotone).</p>
''')

    ll = _topic("dsa-ll", "12. Linked List", "Linked List DSA", f'''
  <p><b>What it is.</b> Nodes with <code>val</code> and <code>next</code> (sometimes <code>prev</code>). O(1) insert/delete given a pointer; O(n) access by index.</p>
  <p><b>When to use list thinking.</b> Reverse, merge, cycle, reorder, add-two-numbers, remove nth from end. LRU uses a doubly linked list + HashMap (see exercises).</p>
  <p><b>Mental model.</b> Draw boxes and arrows. Use a dummy head so the first node is not special. Keep a <code>prev</code> when you will relink.</p>
  {_code("TypeScript", """class ListNode {
  val: number;
  next: ListNode | null;
  constructor(val = 0, next: ListNode | null = null) {
    this.val = val; this.next = next;
  }
}
function reverseList(head: ListNode | null): ListNode | null {
  let prev: ListNode | null = null, cur = head;
  while (cur) {
    const nxt = cur.next;
    cur.next = prev;
    prev = cur;
    cur = nxt;
  }
  return prev;
}""")}
  <p><b>Mistakes.</b> Losing <code>next</code> before rewiring. Off-by-one on n-from-end. Detecting a cycle but not the start (Phase 1: detecting is enough unless asked).</p>
''')

    trees = _topic("dsa-trees", "13. Trees", "Trees binary tree DSA", f'''
  <p><b>What it is.</b> Hierarchical nodes. Interview default: binary tree with <code>left</code>/<code>right</code>. Recursion matches the structure: solve children, combine.</p>
  <p><b>Mental model.</b> Each call has a job (preorder work), delegates, then combines (postorder work). Height is 1+max(child heights). Diameter is max of left-height+right-height over all nodes.</p>
  <p><b>Traversals.</b> Preorder (node, L, R), inorder (L, node, R), postorder (L, R, node), level-order (BFS queue).</p>
  {_code("TypeScript", """function maxDepth(root: TreeNode | null): number {
  if (!root) return 0;
  return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}""")}
  <p><b>Complexity.</b> Visit each node once: O(n) time, O(h) stack space (h = height; worst n, balanced log n).</p>
  <p><b>When not to recurse blindly.</b> Skewed trees of 10⁵ nodes can overflow the JS stack. Mention converting to explicit stack if asked about production limits.</p>
''')

    bst = _topic("dsa-bst", "14. Binary Search Trees", "BST binary search tree", f'''
  <p><b>What it is.</b> For every node, left subtree &lt; node &lt; right subtree (or ≤, confirm duplicates policy). Inorder traversal is sorted.</p>
  <p><b>When the BST property matters.</b> Validate BST (need bounds, not just “left &lt; node &lt; right”). LCA: walk down, going left/right together. Kth smallest: inorder count. Search/insert/delete in O(h).</p>
  <p><b>When not.</b> An ordinary binary tree question (invert, diameter) does not use BST order. Using a BST to get O(log n) in an interview is rare unless you implement it; usually you sort or hash instead.</p>
  {_code("TypeScript", """function isValidBST(root: TreeNode | null, lo = -Infinity, hi = Infinity): boolean {
  if (!root) return true;
  if (root.val <= lo || root.val >= hi) return false;
  return isValidBST(root.left, lo, root.val) && isValidBST(root.right, root.val, hi);
}""")}
  <p><b>Trap.</b> Checking only immediate children accepts invalid trees (e.g. right-left grandchild too small).</p>
''')

    dfs = _topic("dsa-dfs", "15. DFS", "DFS depth first search", f'''
  <p><b>What it is.</b> Go deep before wide. Recursion or explicit stack. On grids: flood fill. On graphs: color states (unseen / visiting / done) to detect cycles.</p>
  <p><b>When to use it.</b> Connected components (islands), existence paths, topological sort (DFS finish times), tree problems, backtracking (subsets/permutations — light touch in Phase 1).</p>
  <p><b>When not.</b> Shortest path in an unweighted graph (BFS). You need level-by-level time (oranges).</p>
  {_code("TypeScript", """function numIslands(grid: string[][]): number {
  const rows = grid.length, cols = grid[0]?.length ?? 0;
  const dfs = (r: number, c: number) => {
    if (r < 0 || c < 0 || r >= rows || c >= cols || grid[r][c] !== "1") return;
    grid[r][c] = "0";
    dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1);
  };
  let n = 0;
  for (let r = 0; r < rows; r++)
    for (let c = 0; c < cols; c++)
      if (grid[r][c] === "1") { n++; dfs(r, c); }
  return n;
}""")}
  <p><b>Mistakes.</b> Not marking visited before recursing (infinite loops). Forgetting all four directions. Mutating input without asking (say you will restore or copy if they care).</p>
''')

    bfs = _topic("dsa-bfs", "16. BFS", "BFS breadth first search", f'''
  <p><b>What it is.</b> Explore by distance from the source using a queue. First time you reach a node is the shortest path in an unweighted graph.</p>
  <p><b>When to use it.</b> Level order. Shortest path (word ladder, maze). Multi-source (oranges: all rotten start at once). Bipartite check. Clone graph (also DFS + map).</p>
  {_code("TypeScript", """function orangesRotting(grid: number[][]): number {
  const q: [number, number][] = [];
  let fresh = 0, minutes = 0;
  for (let r = 0; r < grid.length; r++)
    for (let c = 0; c < grid[0].length; c++) {
      if (grid[r][c] === 2) q.push([r, c]);
      if (grid[r][c] === 1) fresh++;
    }
  const dirs = [[1,0],[-1,0],[0,1],[0,-1]];
  let head = 0;
  while (head < q.length && fresh) {
    const size = q.length - head;
    for (let s = 0; s < size; s++) {
      const [r, c] = q[head++];
      for (const [dr, dc] of dirs) {
        const nr = r + dr, nc = c + dc;
        if (grid[nr]?.[nc] === 1) {
          grid[nr][nc] = 2; fresh--; q.push([nr, nc]);
        }
      }
    }
    minutes++;
  }
  return fresh ? -1 : minutes;
}""")}
  <p><b>Mistakes.</b> Not processing level size when you need minutes. Using <code>shift()</code> in a tight loop. Forgetting multi-source initialization.</p>
''')

    heap = _topic("dsa-heap", "17. Heap / Priority Queue", "Heap Priority Queue", f'''
  <p><b>What it is.</b> A binary heap gives O(log n) push/pop and O(1) peek of min or max. JavaScript has no built-in heap; in interviews you may (1) sort O(n log n) when n is small, (2) implement a tiny binary heap, (3) say “I would use a PriorityQueue” and write the API. For Phase 1, implement a min-heap of ~30 lines or sort when K is unconstrained.</p>
  <p><b>When to use it.</b> Top K, running median (two heaps), merge K lists, scheduling by time, “always take the current best.”</p>
  <p><b>When not.</b> You need the full sort anyway. K = n. You only need min/max of a static array (one pass).</p>
  {_code("TypeScript", """class MinHeap {
  a: number[] = [];
  size() { return this.a.length; }
  peek() { return this.a[0]; }
  push(x: number) {
    this.a.push(x); this.up(this.a.length - 1);
  }
  pop(): number {
    const top = this.a[0], last = this.a.pop()!;
    if (this.a.length) { this.a[0] = last; this.down(0); }
    return top;
  }
  private up(i: number) {
    while (i) {
      const p = (i - 1) >> 1;
      if (this.a[p] <= this.a[i]) break;
      [this.a[p], this.a[i]] = [this.a[i], this.a[p]]; i = p;
    }
  }
  private down(i: number) {
    for (;;) {
      let s = i, l = i * 2 + 1, r = l + 1;
      if (l < this.a.length && this.a[l] < this.a[s]) s = l;
      if (r < this.a.length && this.a[r] < this.a[s]) s = r;
      if (s === i) break;
      [this.a[s], this.a[i]] = [this.a[i], this.a[s]]; i = s;
    }
  }
}""")}
  <p><b>Top K pattern.</b> Keep a min-heap of size K of the largest items seen: if heap.size &lt; K or x &gt; peek, push and maybe pop. That is O(n log K).</p>
''')

    mixed = _topic("dsa-mixed", "18. Mixed interview problems", "Mixed interview problems", f'''
  <p>Real Atlassian screens combine patterns. Product of array except self is prefix/suffix, not a “trick multiply.” Rain water is two pointers or stacks. Course schedule is graph + cycle. Median stream is two heaps.</p>
  <p><b>Senior habit:</b> name the pattern in the first two minutes, then implement the template, then adapt. If you cannot name it, brute force first so you still have a correct baseline.</p>
  <p><b>Practice set (all in the Problem Bank):</b> Product of Array Except Self, Trapping Rain Water, Course Schedule, Find Median from Data Stream, LRU (Exercises), Minimum Window Substring.</p>
  <p><b>When you get stuck.</b> Re-read constraints. Restate the invariant. Try n ≤ 5 by hand. Ask: contiguous? sorted? pair vs subarray? graph?</p>
''')

    return f'''
<section class="block" id="dsa" data-search="DSA Curriculum learning path" data-stype="Section">
  <p class="kicker">Fundamentals</p>
  <h2 class="section-title">DSA Curriculum</h2>
  <p class="lede">A complete Phase 1 path. Read the topic, implement the snippet from memory, then do the linked problems. Mark complete only after you can teach the mental model out loud.</p>
  {bigo}{arrays}{strings}{hashmap}{set_t}{tp}{sw}{prefix}{stack}{queue}{bs}{ll}{trees}{bst}{dfs}{bfs}{heap}{mixed}
</section>
<section class="block" id="bigo" data-search="Big O section O(1) log n" data-stype="Section">
  <p class="kicker">Complexity</p>
  <h2 class="section-title">Big O Deep Dive</h2>
  <p class="lede">The full treatment lives in topic 1 above. This section is the jump link from the sidebar and a compact drill sheet for daily revision.</p>
  <div class="card">
    <h3>30-second drill (say this every few days)</h3>
    <ul class="tight">
      <li>HashMap get: expected O(1), worst O(n), space O(n).</li>
      <li>Binary search: O(log n) because the range halves; requires monotonicity.</li>
      <li>Comparison sort: Ω(n log n); JS <code>sort</code> is implementation-defined but treat as O(n log n).</li>
      <li>Nested i,j over n: O(n²) unless the inner pointer only moves forward globally.</li>
      <li>Amortized: expensive ops are rare and paid for by many cheap ones (push/rehash).</li>
      <li>Recursion space: O(depth), not free.</li>
    </ul>
  </div>
</section>
'''
