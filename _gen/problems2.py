P2 = [
{
  "id": "binary-search", "name": "Binary Search", "diff": "easy", "pattern": "binary-search", "topic": "binary-search",
  "why": "If you cannot write a bug-free binary search on a whiteboard, stop and drill this for a day.",
  "stmt": "Sorted ascending unique-enough array. Return the index of target or -1.",
  "exin": "nums = [-1,0,3,5,9,12], target = 9", "exout": "4",
  "cons": "n up to 10^4.",
  "hints": "lo, hi inclusive. mid = lo+((hi-lo)>>1). Compare and shrink.",
  "brute": "Linear scan O(n).",
  "opt": "Classic binary search O(log n).",
  "steps": "While lo<=hi: if equal return; if mid < target, lo=mid+1; else hi=mid-1.",
  "cx": "O(log n) time, O(1) space.",
  "mistakes": "lo<hi with lo=mid infinite loop. Overflow mid in other languages.",
  "edges": "Empty. Target below min / above max. Single element.",
  "follow": "First/last occurrence with duplicates.",
  "talk": "I will write the invariant 'target is in [lo,hi] if it exists' on the side.",
  "sol": """function search(nums: number[], target: number): number {
  let lo = 0, hi = nums.length - 1;
  while (lo <= hi) {
    const mid = lo + ((hi - lo) >> 1);
    if (nums[mid] === target) return mid;
    if (nums[mid] < target) lo = mid + 1;
    else hi = mid - 1;
  }
  return -1;
}"""
},
{
  "id": "search-insert", "name": "Search Insert Position", "diff": "easy", "pattern": "binary-search", "topic": "binary-search",
  "why": "Lower-bound binary search. Same skeleton as 'first true'.",
  "stmt": "Sorted distinct integers. Index of target, or the index where it would be inserted to keep order.",
  "exin": "nums = [1,3,5,6], target = 2", "exout": "1",
  "cons": "n up to 10^4.",
  "hints": "Find the first index with nums[i] ≥ target.",
  "brute": "Scan until nums[i] >= target.",
  "opt": "lo=0, hi=n, while lo<hi, mid=(lo+hi)>>1; if nums[mid]>=t hi=mid else lo=mid+1.",
  "steps": "This is the bisect_left template. Return lo.",
  "cx": "O(log n).",
  "mistakes": "Returning mid instead of lo. Using inclusive hi without care.",
  "edges": "Insert at 0. Insert at n. Exact hit.",
  "follow": "Upper bound (first > target).",
  "talk": "I prefer the half-open [lo,hi) form for insert position.",
  "sol": """function searchInsert(nums: number[], target: number): number {
  let lo = 0, hi = nums.length;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (nums[mid] >= target) hi = mid;
    else lo = mid + 1;
  }
  return lo;
}"""
},
{
  "id": "search-2d", "name": "Search a 2D Matrix", "diff": "medium", "pattern": "binary-search", "topic": "binary-search",
  "why": "Treat a sorted matrix as a virtual sorted array. Index math is the skill.",
  "stmt": "m×n matrix: each row sorted, first of each row > last of previous row. Is target present?",
  "exin": "matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3", "exout": "true",
  "cons": "m,n up to 100.",
  "hints": "mid → row = mid/n, col = mid%n.",
  "brute": "Scan all cells O(mn).",
  "opt": "Binary search on [0, mn).",
  "steps": "Same as 1D search on the flattened index space.",
  "cx": "O(log(mn)).",
  "mistakes": "Off-by-one on columns. Treating a merely 'row-sorted' matrix (different problem: staircase search).",
  "edges": "1×1. Target smaller than [0][0].",
  "follow": "Rows sorted but columns also sorted without the 'row starts after previous' — use O(m+n) staircase from corner.",
  "talk": "I will confirm the global sorted property before flattening.",
  "sol": """function searchMatrix(matrix: number[][], target: number): boolean {
  const m = matrix.length, n = matrix[0].length;
  let lo = 0, hi = m * n - 1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    const v = matrix[Math.floor(mid / n)][mid % n];
    if (v === target) return true;
    if (v < target) lo = mid + 1;
    else hi = mid - 1;
  }
  return false;
}"""
},
{
  "id": "rotated-min", "name": "Find Minimum in Rotated Sorted Array", "diff": "medium", "pattern": "binary-search", "topic": "binary-search",
  "why": "Identify the unsorted half. The min is the rotation pivot.",
  "stmt": "A distinct sorted array was rotated at an unknown pivot. Return the minimum.",
  "exin": "nums = [3,4,5,1,2]", "exout": "1",
  "cons": "n up to 5000; unique values in the classic version.",
  "hints": "If nums[mid] > nums[hi], min is to the right of mid; else min is at mid or left.",
  "brute": "Linear min scan O(n).",
  "opt": "Binary search O(log n).",
  "steps": "The array is two increasing runs. Compare mid to the right end to see which run mid sits on.",
  "cx": "O(log n).",
  "mistakes": "Comparing to nums[lo] blindly when the range is already sorted. Duplicates (need a linear fallback).",
  "edges": "Not rotated. Two elements. Rotation at last.",
  "follow": "With duplicates: worst case O(n).",
  "talk": "I will say 'I compare mid with hi because that tells me if the pivot is strictly right of mid.'",
  "sol": """function findMin(nums: number[]): number {
  let lo = 0, hi = nums.length - 1;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (nums[mid] > nums[hi]) lo = mid + 1;
    else hi = mid;
  }
  return nums[lo];
}"""
},
{
  "id": "rotated-search", "name": "Search in Rotated Sorted Array", "diff": "medium", "pattern": "binary-search", "topic": "binary-search",
  "why": "One half is always sorted. Search there if the target's range fits; otherwise the other half.",
  "stmt": "Rotated distinct sorted array. Return index of target or -1. O(log n).",
  "exin": "nums = [4,5,6,7,0,1,2], target = 0", "exout": "4",
  "cons": "n up to 5000.",
  "hints": "If nums[lo] ≤ nums[mid], left half is sorted. See if target is in [nums[lo], nums[mid]).",
  "brute": "Linear scan.",
  "opt": "Binary search with a sorted-half test.",
  "steps": "Each step discards a half. Equality on mid still returns immediately.",
  "cx": "O(log n).",
  "mistakes": "Wrong closed/open interval when testing 'is target in the sorted half'. Duplicates version is harder.",
  "edges": "No rotation. Target is the pivot. Missing target.",
  "follow": "With duplicates (may need lo++ when nums[lo]===nums[mid]===nums[hi]).",
  "talk": "I will draw the two increasing segments before coding.",
  "sol": """function searchRotated(nums: number[], target: number): number {
  let lo = 0, hi = nums.length - 1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (nums[mid] === target) return mid;
    if (nums[lo] <= nums[mid]) {
      if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
      else lo = mid + 1;
    } else {
      if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
      else hi = mid - 1;
    }
  }
  return -1;
}"""
},
{
  "id": "koko", "name": "Koko Eating Bananas", "diff": "medium", "pattern": "binary-search", "topic": "binary-search",
  "why": "Binary search on the answer. The Phase 1 'search the solution space' problem.",
  "stmt": "piles[i] bananas, speed k bananas/hour, each hour one pile (ceil(pile/k)). Finish in ≤ h hours. Minimum integer k.",
  "exin": "piles = [3,6,7,11], h = 8", "exout": "4",
  "cons": "h ≥ piles.length; piles up to 10^4, values up to 10^9 (watch overflow in other langs).",
  "hints": "feasible(k) is monotone. Search k in [1, max(piles)].",
  "brute": "Try k = 1,2,…max. O(max * n).",
  "opt": "O(n log max) binary search.",
  "steps": "hours(k) = sum ceil(p/k). If hours ≤ h, try smaller k.",
  "cx": "O(n log M) time, O(1) space.",
  "mistakes": "lo=0 (div by zero). Using floor instead of ceil. h < n (impossible by constraints).",
  "edges": "h === n (k must be max pile). One pile.",
  "follow": "Split array largest sum — same template.",
  "talk": "I will write feasible() first and test it on the example before wiring binary search.",
  "sol": """function minEatingSpeed(piles: number[], h: number): number {
  let lo = 1, hi = Math.max(...piles);
  const ok = (k: number) =>
    piles.reduce((acc, p) => acc + Math.ceil(p / k), 0) <= h;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (ok(mid)) hi = mid;
    else lo = mid + 1;
  }
  return lo;
}"""
},
{
  "id": "valid-parens", "name": "Valid Parentheses", "diff": "easy", "pattern": "stack", "topic": "stack",
  "why": "The stack matching problem. You will reuse this mental model for paths and HTML-ish nesting.",
  "stmt": "String of ()[]{}. Return whether every opener is closed in the correct order.",
  "exin": 's = "()[]{}"', "exout": "true",
  "cons": "n up to 10^4.",
  "hints": "Push openers. On closer, stack top must be the matching opener.",
  "brute": "Repeatedly replace '()' '[]' '{}' — O(n²).",
  "opt": "Stack O(n).",
  "steps": "Map closer→opener. If closer and (empty or mismatch) false. End: stack must be empty.",
  "cx": "O(n) time and space.",
  "mistakes": "Not checking empty stack on closer. Leftover openers.",
  "edges": "Empty (true). Single closer. Nested mixed types.",
  "follow": "Longest valid parentheses (hard). Score of parentheses.",
  "talk": "I will mention early-exit when stack is empty and we see a closer.",
  "sol": """function isValid(s: string): boolean {
  const st: string[] = [];
  const pair: Record<string, string> = { ")": "(", "]": "[", "}": "{" };
  for (const ch of s) {
    if (ch === "(" || ch === "[" || ch === "{") st.push(ch);
    else if (st.pop() !== pair[ch]) return false;
  }
  return st.length === 0;
}"""
},
{
  "id": "min-stack", "name": "Min Stack", "diff": "medium", "pattern": "stack", "topic": "stack",
  "why": "Auxiliary state on a stack. O(1) getMin is the requirement.",
  "stmt": "Stack with push, pop, top, and getMin — all O(1).",
  "exin": "push 3, push 5, getMin → 3, push 2, getMin → 2, pop, getMin → 3", "exout": "as above",
  "cons": "Calls up to 3·10^4.",
  "hints": "Store pairs (value, minSoFar) or a parallel min stack.",
  "brute": "Scan the stack for min. O(n) getMin — not allowed.",
  "opt": "Each node remembers the min of itself and below.",
  "steps": "push: min = stack empty ? x : Math.min(x, peek.min). pop/top/getMin read the top pair.",
  "cx": "O(1) ops, O(n) space.",
  "mistakes": "A single running min that breaks after pop. Mutating after pop incorrectly.",
  "edges": "All decreasing. Duplicate mins. Pop to empty (constraints usually forbid).",
  "follow": "Max stack. Queue with getMin (need two stacks or deque).",
  "talk": "I will store pairs; it is harder to get wrong than a second stack of only mins.",
  "sol": """class MinStack {
  private st: { v: number; m: number }[] = [];
  push(v: number) {
    const m = this.st.length ? Math.min(v, this.st.at(-1)!.m) : v;
    this.st.push({ v, m });
  }
  pop() { this.st.pop(); }
  top() { return this.st.at(-1)!.v; }
  getMin() { return this.st.at(-1)!.m; }
}"""
},
{
  "id": "rpn", "name": "Evaluate Reverse Polish Notation", "diff": "medium", "pattern": "stack", "topic": "stack",
  "why": "Stack evaluation. Clean switch on operators. Integer division toward zero.",
  "stmt": "Tokens are integers or + - * /. Evaluate RPN (postfix).",
  "exin": 'tokens = ["2","1","+","3","*"]', "exout": "9",
  "cons": "Valid expression; division truncates toward 0.",
  "hints": "On a number, push. On an op, pop b then a, push a op b.",
  "brute": "Not really — this is inherently a stack walk.",
  "opt": "Single stack.",
  "steps": "Order of pops matters for − and /. Use Math.trunc(a/b) in JS.",
  "cx": "O(n) time, O(n) space.",
  "mistakes": "Math.floor on negatives (JS floor ≠ trunc). Popping a then b.",
  "edges": "Single number. Negative operands.",
  "follow": "Infix to RPN (shunting yard).",
  "talk": "I will call out toward-zero division before I write the first line.",
  "sol": """function evalRPN(tokens: string[]): number {
  const st: number[] = [];
  for (const t of tokens) {
    if (t === "+" || t === "-" || t === "*" || t === "/") {
      const b = st.pop()!, a = st.pop()!;
      if (t === "+") st.push(a + b);
      else if (t === "-") st.push(a - b);
      else if (t === "*") st.push(a * b);
      else st.push(Math.trunc(a / b));
    } else st.push(Number(t));
  }
  return st[0];
}"""
},
{
  "id": "daily-temp", "name": "Daily Temperatures", "diff": "medium", "pattern": "stack", "topic": "stack",
  "why": "Next greater element via monotonic stack. Template for a family of problems.",
  "stmt": "For each day, how many days until a warmer temperature? 0 if none.",
  "exin": "temperatures = [73,74,75,71,69,72,76,73]", "exout": "[1,1,4,2,1,1,0,0]",
  "cons": "n up to 10^5.",
  "hints": "Stack of indices with decreasing temps. Today resolves anyone colder on the stack.",
  "brute": "For each i scan right. O(n²).",
  "opt": "Monotonic decreasing stack, O(n).",
  "steps": "While t[i] > t[st.top], ans[st.pop()]=i-j. Then push i.",
  "cx": "O(n) time and space.",
  "mistakes": "Storing values not indices. ≥ vs >.",
  "edges": "Strictly decreasing (all 0). All equal.",
  "follow": "Next greater circular (loop twice).",
  "talk": "Each index is pushed and popped at most once — that is the O(n) proof.",
  "sol": """function dailyTemperatures(t: number[]): number[] {
  const ans = Array(t.length).fill(0);
  const st: number[] = [];
  for (let i = 0; i < t.length; i++) {
    while (st.length && t[i] > t[st.at(-1)!]) {
      const j = st.pop()!;
      ans[j] = i - j;
    }
    st.push(i);
  }
  return ans;
}"""
},
{
  "id": "histogram", "name": "Largest Rectangle in Histogram", "diff": "hard", "pattern": "stack", "topic": "stack",
  "why": "Optional Hard. Same monotonic stack as rain water's 'nearest smaller' idea.",
  "stmt": "Bars of width 1, heights[i]. Largest rectangle aligned with the bars.",
  "exin": "heights = [2,1,5,6,2,3]", "exout": "10",
  "cons": "n up to 10^5.",
  "hints": "For each bar, the max rectangle where it is the shortest bar uses nearest smaller on left and right.",
  "brute": "For each pair of bounds, min height × width. O(n²).",
  "opt": "Monotonic increasing stack of indices; pop computes width using the new smaller as right boundary.",
  "steps": "Append a 0-height sentinel so leftover bars flush. width = i − stack.top − 1 after pop.",
  "cx": "O(n).",
  "mistakes": "Forgetting the sentinel. Width off-by-one.",
  "edges": "Single bar. All equal. Strictly increasing.",
  "follow": "Maximal rectangle in a binary matrix (histogram per row).",
  "talk": "Phase 1: I can explain nearest-smaller. If I stall on the sentinel, I write the two-array nearest-smaller version.",
  "sol": """function largestRectangleArea(heights: number[]): number {
  const h = [...heights, 0];
  const st: number[] = [];
  let best = 0;
  for (let i = 0; i < h.length; i++) {
    while (st.length && h[i] < h[st.at(-1)!]) {
      const height = h[st.pop()!];
      const left = st.length ? st.at(-1)! : -1;
      best = Math.max(best, height * (i - left - 1));
    }
    st.push(i);
  }
  return best;
}"""
},
{
  "id": "rev-list", "name": "Reverse Linked List", "diff": "easy", "pattern": "fast-slow", "topic": "linked-list",
  "why": "The list primitive. You will reverse the second half in Reorder List.",
  "stmt": "Reverse a singly linked list. Return the new head.",
  "exin": "1→2→3→4→5", "exout": "5→4→3→2→1",
  "cons": "n up to 5000.",
  "hints": "prev=null, cur=head; save next; cur.next=prev; advance.",
  "brute": "Copy values to an array, rewrite. Extra space.",
  "opt": "Iterative O(1) extra. Recursive also fine if you mention stack space.",
  "steps": "Three pointers. Never lose next.",
  "cx": "O(n) time, O(1) extra iterative.",
  "mistakes": "Losing the rest of the list. Returning cur instead of prev.",
  "edges": "Empty. Single node.",
  "follow": "Reverse in groups of k.",
  "talk": "I will draw three boxes before I write a line.",
  "sol": """function reverseList(head: ListNode | null): ListNode | null {
  let prev: ListNode | null = null, cur = head;
  while (cur) {
    const nxt = cur.next;
    cur.next = prev;
    prev = cur;
    cur = nxt;
  }
  return prev;
}"""
},
{
  "id": "merge-lists", "name": "Merge Two Sorted Lists", "diff": "easy", "pattern": "fast-slow", "topic": "linked-list",
  "why": "Dummy head + two-pointer merge. Foundation for merge-k (heap).",
  "stmt": "Merge two sorted lists into one sorted list by splicing nodes.",
  "exin": "1→2→4 and 1→3→4", "exout": "1→1→2→3→4→4",
  "cons": "n,m up to 50 in the toy version; conceptually O(n+m).",
  "hints": "Dummy node. Always attach the smaller head. Finish with the leftover tail.",
  "brute": "Array of values, sort — misses the point.",
  "opt": "Linear merge.",
  "steps": "tail = dummy; while both: attach min; then tail.next = remaining.",
  "cx": "O(n+m) time, O(1) extra.",
  "mistakes": "Forgetting leftover. Using new nodes when they wanted splice.",
  "edges": "One list empty. All of one list smaller.",
  "follow": "Merge k lists (heap on heads).",
  "talk": "Dummy head removes the 'first node' special case — I always use it for list rewires.",
  "sol": """function mergeTwoLists(a: ListNode | null, b: ListNode | null): ListNode | null {
  const dummy = new ListNode(0);
  let t = dummy;
  while (a && b) {
    if (a.val <= b.val) { t.next = a; a = a.next; }
    else { t.next = b; b = b.next; }
    t = t.next;
  }
  t.next = a ?? b;
  return dummy.next;
}"""
},
{
  "id": "list-cycle", "name": "Linked List Cycle", "diff": "easy", "pattern": "fast-slow", "topic": "linked-list",
  "why": "Floyd. O(1) space vs HashSet of nodes.",
  "stmt": "Does the list contain a cycle?",
  "exin": "1→2→3→2 …", "exout": "true",
  "cons": "n up to 10^4.",
  "hints": "Slow +1, fast +2. Meeting ⇒ cycle.",
  "brute": "Set of visited node references. O(n) space.",
  "opt": "Floyd O(1) space.",
  "steps": "If fast hits null, no cycle. If slow===fast, cycle. Compare identity, not val.",
  "cx": "O(n) time, O(1) space.",
  "mistakes": "fast.next without checking fast. Comparing values.",
  "edges": "Empty. One node no cycle. Cycle at head.",
  "follow": "Return the cycle start (reset one pointer to head, walk +1/+1).",
  "talk": "I will mention the HashSet version first, then Floyd as the space upgrade.",
  "sol": """function hasCycle(head: ListNode | null): boolean {
  let slow = head, fast = head;
  while (fast && fast.next) {
    slow = slow!.next;
    fast = fast.next.next;
    if (slow === fast) return true;
  }
  return false;
}"""
},
{
  "id": "remove-nth", "name": "Remove Nth Node From End", "diff": "medium", "pattern": "fast-slow", "topic": "linked-list",
  "why": "Gap two-pointer + dummy (removing the head).",
  "stmt": "Remove the nth node from the end in one pass. Return head.",
  "exin": "1→2→3→4→5, n=2", "exout": "1→2→3→5",
  "cons": "n is valid.",
  "hints": "Dummy. Advance first n+1 steps, then first and second together. second.next = second.next.next.",
  "brute": "Count length, second pass. Two passes.",
  "opt": "One pass gap.",
  "steps": "The +1 is because we stop on the node before the victim.",
  "cx": "O(L) time, O(1) space.",
  "mistakes": "Off-by-one on the gap. Forgetting dummy when n equals length.",
  "edges": "Remove head. Single node. n=1 (remove tail).",
  "follow": "Remove all nodes with a value.",
  "talk": "I will use a dummy even if I think I do not need it.",
  "sol": """function removeNthFromEnd(head: ListNode | null, n: number): ListNode | null {
  const dummy = new ListNode(0, head);
  let first: ListNode | null = dummy, second: ListNode | null = dummy;
  for (let i = 0; i < n + 1; i++) first = first!.next;
  while (first) { first = first.next; second = second!.next; }
  second!.next = second!.next!.next;
  return dummy.next;
}"""
},
{
  "id": "reorder-list", "name": "Reorder List", "diff": "medium", "pattern": "fast-slow", "topic": "linked-list",
  "why": "Compose mid + reverse + merge. Senior-looking Easy/Medium combo.",
  "stmt": "L0→L1→…→Ln becomes L0→Ln→L1→Ln-1→… In-place.",
  "exin": "1→2→3→4→5", "exout": "1→5→2→4→3",
  "cons": "n up to 5·10^4.",
  "hints": "Find mid, cut, reverse second half, weave.",
  "brute": "Store nodes in an array, rebuild with two pointers. O(n) space.",
  "opt": "O(1) extra with the three-step recipe.",
  "steps": "Slow/fast for mid. prev.next=null to split. Reverse second. Merge alternating.",
  "cx": "O(n) time, O(1) extra.",
  "mistakes": "Not splitting (cycle). Merging without saving next pointers.",
  "edges": "1–2 nodes. Even vs odd length.",
  "follow": "Check palindrome list (reverse second half, compare, restore).",
  "talk": "I will name the three subproblems out loud so the interviewer sees structure.",
  "sol": """function reorderList(head: ListNode | null): void {
  if (!head || !head.next) return;
  let slow: ListNode | null = head, fast: ListNode | null = head;
  while (fast.next && fast.next.next) { slow = slow!.next; fast = fast.next.next; }
  let second = slow!.next; slow!.next = null;
  let prev: ListNode | null = null;
  while (second) {
    const nxt = second.next; second.next = prev; prev = second; second = nxt;
  }
  let a: ListNode | null = head, b = prev;
  while (b) {
    const an = a!.next, bn = b.next;
    a!.next = b; b.next = an;
    a = an; b = bn;
  }
}"""
},
{
  "id": "add-two", "name": "Add Two Numbers", "diff": "medium", "pattern": "fast-slow", "topic": "linked-list",
  "why": "Digit-by-digit with carry. Frontend-adjacent because it is just an iterator over two streams.",
  "stmt": "Two numbers as reversed linked lists (1s digit at head). Return their sum as a reversed list.",
  "exin": "2→4→3 + 5→6→4", "exout": "7→0→8",
  "cons": "Lists up to 100 nodes; single digits.",
  "hints": "Carry. Dummy. Loop while a or b or carry.",
  "brute": "Convert to BigInt — works in JS but they want list arithmetic.",
  "opt": "Schoolbook addition on nodes.",
  "steps": "sum = (a?.val??0)+(b?.val??0)+carry; create sum%10; carry = floor(sum/10).",
  "cx": "O(max(n,m)).",
  "mistakes": "Dropping the final carry (9+1). Advancing a null pointer.",
  "edges": "Different lengths. 99+1. One empty (usually not).",
  "follow": "Lists stored in forward order (reverse first, or stack).",
  "talk": "I will keep looping on carry after both lists end.",
  "sol": """function addTwoNumbers(a: ListNode | null, b: ListNode | null): ListNode | null {
  const dummy = new ListNode(0);
  let t = dummy, carry = 0;
  while (a || b || carry) {
    const sum = (a?.val ?? 0) + (b?.val ?? 0) + carry;
    t.next = new ListNode(sum % 10);
    t = t.next;
    carry = Math.floor(sum / 10);
    a = a?.next ?? null;
    b = b?.next ?? null;
  }
  return dummy.next;
}"""
},
]
