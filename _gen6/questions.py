from util import esc, code

Q = []


def add(level, cat, q, short, deep, miss, follow, snippet=""):
    Q.append(dict(level=level, cat=cat, q=q, short=short, deep=deep, miss=miss, follow=follow, snippet=snippet))


# --- JavaScript as a machine ---
add("javascript", "js", "Why is unshift O(n) in JavaScript?",
    "It inserts at index 0, so every existing element must move one slot right.",
    "An array is a contiguous index map 0..length-1. unshift writes a new 0 and reindexes the rest. push writes at length and (usually) does not move anyone — amortized O(1). Never build a list with repeated unshift in a hot loop; push then reverse, or use a deque.",
    "unshift is O(1) because it is a built-in.",
    "How would you implement a queue so both ends are cheap?")

add("javascript", "js", "Why is s += ch in a loop sometimes a problem?",
    "Strings are immutable. Each += may copy the whole prefix. Worst case O(n²).",
    "Engines sometimes optimize concatenations, but you must not rely on that in an interview or a large n. Push chars into an array and join once. Same idea as a StringBuilder.",
    "String += is always O(1) because V8 is fast.",
    "Rewrite a reverse-words function without quadratic concat.",
    "const out = [];\nfor (const ch of s) out.push(ch);\nreturn out.join('');")

add("javascript", "js", "When do you use Map instead of a plain object as a hash map?",
    "When keys are not only safe strings, when you need insertion order as a feature, or when you must not collide with Object.prototype.",
    "Objects coerce keys to strings (except symbols). Map keeps object identity and numbers as numbers. Map is iterable in insertion order — that is why LRU can be a Map. has/get/set/delete are the API. For a 26-letter count, a length-26 array is still better.",
    "Always use objects; Map is only for advanced users.",
    "Why does obj['__proto__'] scare you as a frequency map?")

add("javascript", "js", "What is a sparse array and why do interviews avoid it?",
    "Holes: indexes that exist in length but have no value. forEach skips them; for (i) sees undefined.",
    "arr[100] = 1 on a short array jumps length to 101 with 100 holes. Complexity talk assumes a dense 0..n-1. Prefer push. Never treat length as 'number of defined items' after random writes.",
    "length always equals the number of elements you set.",
    "What does [1,,3].map(x => x) return?")

add("javascript", "js", "What does === compare for objects and arrays?",
    "Reference identity, not deep value.",
    "const a = [1]; const b = [1]; a === b is false. Two nodes with the same val are different if they are different objects — that is why Floyd uses pointer equality, not val equality. Structured clone / JSON is a different problem.",
    "=== on arrays compares contents.",
    "How do you detect a cycle if two nodes can share the same val?")

add("javascript", "js", "Why is q.shift() a bad queue on a large array?",
    "shift is O(n): every remaining index moves left.",
    "BFS that shift()s a million-node queue is accidentally O(n²). Use an index head that only increments, or a linked-list queue, or a circular buffer. In interviews, say this even if you write shift on a tiny example.",
    "shift is O(1) like pop.",
    "Write a queue with O(1) amortized enqueue and dequeue.",
    "class Queue {\n  constructor() { this.a = []; this.head = 0; }\n  enqueue(x) { this.a.push(x); }\n  dequeue() {\n    if (this.head >= this.a.length) return undefined;\n    const x = this.a[this.head++];\n    if (this.head > 32 && this.head * 2 > this.a.length) {\n      this.a = this.a.slice(this.head); this.head = 0;\n    }\n    return x;\n  }\n  get length() { return this.a.length - this.head; }\n}")

add("javascript", "js", "What does sort() do to numbers if you forget the comparator?",
    "It sorts as strings. [10, 2] becomes [10, 2] or [10,2] vs [2,10] — 10 comes before 2 as strings.",
    "Always nums.sort((a,b) => a - b). The comparator must return negative/zero/positive. sort mutates. Copy first if you need the original: nums.slice().sort(...).",
    "sort always uses numeric order for number arrays.",
    "What is the complexity of Array#sort in the spec vs V8?")

add("javascript", "js", "Array#sort complexity — what do you say in an interview?",
    "The spec does not freeze a complexity. Treat it as O(n log n) typical; mention it mutates.",
    "V8 uses Timsort (merge + insertion). Worst-case time is O(n log n). Stability is required by the modern spec. Do not claim 'quicksort, so unstable' anymore.",
    "JavaScript sort is always O(n log n) quicksort and unstable.",
    "When would you implement your own merge sort in JS?")

add("fundamentals", "complexity", "What is Big O actually measuring?",
    "How the worst-case work grows as n grows — ignoring constants and lower-order terms.",
    "It is a ceiling on growth, not a stopwatch. O(n) can lose to O(n log n) at small n. You still report it because interviewers compare algorithms as n → ∞. Also name extra memory. JS allocations (new arrays, closures) count as space.",
    "Big O is the exact number of milliseconds.",
    "Give an O(n²) JS snippet that looks like one loop.")

add("fundamentals", "complexity", "Amortized O(1) — what does that mean for push?",
    "Most pushes are O(1); rare resizes are O(n); average per push is O(1).",
    "When the backing store fills, the engine allocates a larger store and copies. If capacity doubles, the copy cost spreads across enough later pushes that the average is constant. pop is O(1) and does not reindex.",
    "Amortized means 'usually fast on my laptop.'",
    "Why is a loop of n unshifts still Θ(n²) and not amortized O(n)?")

add("fundamentals", "complexity", "O(1) extra space vs O(n) output — how do you say it?",
    "The answer array of size n is not 'extra' if the problem requires it. Extra is what you allocate beyond input and required output.",
    "productExceptSelf can be O(1) extra if you reuse the output for prefixes. A copy of the input is O(n) extra. Recursion depth is space — a tree walk is O(h) stack.",
    "If I create any array, I must say O(n) extra.",
    "Is the call stack 'extra space' in reverseList recursive?")

add("fundamentals", "complexity", "log n shows up when you cut the search space in half. Where else?",
    "Balanced tree height, heap height, binary search, binary lifting.",
    "A complete binary heap of n nodes has height floor(log2 n). That is why heap insert/sift is O(log n). Unbalanced BST can be O(n). Always say 'if balanced'.",
    "log n means the code contains Math.log.",
    "Why is building a heap O(n) but n inserts is O(n log n)?")

add("structures", "array", "When is an array the wrong default?",
    "When you need O(1) delete-by-key, O(1) 'is this id present?', or frequent inserts at the front.",
    "Scan-to-find is O(n). indexOf in a hot path is a smell. If keys are ids, use Map/Set. If you need order plus O(1) delete, you want a linked list + Map (LRU) or an ordered Map trick.",
    "Arrays are always fastest because they are contiguous.",
    "How would you delete a node from the middle of a playlist by id?")

add("structures", "array", "Two-pointer vs extra array — how do you choose?",
    "Two pointers when the array is sorted or you can partition in place. Extra array when you must not scramble order you have not classified yet.",
    "rotate via reverse is O(1) extra. Merge two sorted arrays into a new one is honest O(n+m). Dutch-flag / remove-element compact with a write pointer.",
    "Two pointers only work on strings.",
    "Why does 3Sum sort first?")

add("structures", "string", "Are JS strings arrays of characters?",
    "No. They are immutable sequences. Indexing s[i] is O(1) for well-formed UTF-16 code units, but you cannot assign s[i].",
    "s[i] = 'x' is a no-op in sloppy mode / TypeError in strict on some wrappers — do not mutate. For surrogates, for...of iterates code points. Interview strings are usually ASCII. Convert to array only when you must rewrite.",
    "Strings are mutable like in C.",
    "How do you reverse a string in JS in O(n)?")

add("structures", "hash", "Set vs Map vs object for 'have I seen this'?",
    "Set when you only need presence. Map when you store a payload (index, count). Object only for known string keys you control.",
    "containsDuplicate → Set. twoSum → Map value→index. anagram of lowercase → int[26]. Counting with object[x]++ blows up on __proto__ and coerces 1 and '1'.",
    "They are interchangeable.",
    "Why does twoSum store the index, not just a boolean?")

add("structures", "hash", "What is the load-factor story you should know (even though you cannot set it in JS)?",
    "A hash table resizes when it gets too full so lookups stay expected O(1).",
    "You do not tune V8's Map. You still say: expected O(1), worst-case O(n) if everything collides — ignore adversarial hash unless asked. Space is O(n).",
    "Map is worst-case O(1) guaranteed by the language.",
    "When would you replace a Map with a sorted array + binary search?")

add("structures", "list", "Why does a dummy node make list code shorter?",
    "It gives you a stable head so you never special-case 'insert/merge at the very front.'",
    "mergeTwoLists: dummy.next is the real head. You only move a tail pointer. Same for remove-nth-from-end with a gap pointer. Forgetting dummy is how people lose the head and write five ifs.",
    "Dummy nodes are only for circular lists.",
    "Reverse a list with dummy — do you need one? Why not?")

add("structures", "list", "Floyd's cycle — why two speeds, not a Set?",
    "slow +1, fast +2. If there is a cycle they meet. O(1) extra memory.",
    "A Set of node references is O(n) space and works. Interviewers want O(1) space. Meeting proves a cycle; a second phase (reset one pointer to head, step both by 1) finds the entrance. Do not compare .val.",
    "If vals repeat, there is a cycle.",
    "How do you find the start of the cycle?")

add("structures", "list", "When is a linked list better than an array in JS?",
    "O(1) insert/delete once you have the node; structures like LRU, undo chains, or merge of sorted streams.",
    "JS arrays already give you O(1) end ops. Lists win when you hold a pointer into the middle and splice without shifting. Random access is O(n) — do not binary-search a list. In the browser, arrays are usually the default; implement lists to prove you can.",
    "Lists are always faster than arrays.",
    "Why is indexOf on a list O(n) and also cache-unfriendly?")

add("structures", "stack", "What problem shape screams stack?",
    "Matching, undo, next-greater, parse nesting, DFS with an explicit stack.",
    "Valid parentheses, min stack, monotonic next warmer day, browser history, call stack of a DFS. If you need the most recent unmatched opener, that is a stack. Queue is BFS / fair scheduling.",
    "Stacks are only for undo.",
    "Why is a recursive DFS secretly a stack?")

add("structures", "stack", "Monotonic stack — one sentence.",
    "Keep indexes whose values are strictly increasing (or decreasing) so the top is the next candidate.",
    "dailyTemperatures: pop while current is warmer; distance is i - popped. Each index pushed/popped once → O(n). Same family: next greater element, largest rectangle in histogram, sliding-window maximum (deque).",
    "Monotonic means the array is already sorted.",
    "Would you use a heap instead? When?")

add("fundamentals", "tree", "Recursion needs three things. Name them.",
    "Base case, smaller subproblem, combination of results.",
    "Without a base case you stack-overflow. The subproblem must make progress (i+1, node.left). Combination is where bugs hide: invertTree swaps after both calls; maxDepth is 1+max(...). Draw the call tree for n=3 before coding.",
    "Recursion is when you call the same function. That is the whole definition.",
    "Convert a recursive inorder to an explicit stack.")

add("structures", "tree", "BFS vs DFS on a tree — how do you pick?",
    "BFS (queue, level size) for levels / shortest hops in an unweighted tree. DFS (recursion or stack) for paths, height, and most BST work.",
    "levelOrder is BFS. maxDepth can be either. Validate BST is DFS with bounds. Beware q.shift() cost; for interviews it is fine if you mention it. Grid BFS is the same idea with 4 neighbors.",
    "DFS is always faster.",
    "Why does 'minimum depth' want BFS?")

add("structures", "tree", "Why is 'compare to parent only' wrong for validate BST?",
    "A right child can be greater than its parent and still be less than an ancestor it must exceed.",
    "Carry a (lo, hi) open interval. Left subtree must stay < node.val; right > node.val. Duplicates: decide <= or < and be consistent. Inorder should be strictly increasing if unique.",
    "If every node is between its two children it is a BST.",
    "How do you validate with O(1) extra besides stack?")

add("structures", "tree", "BST search/insert is O(h), not O(log n). Why the distinction?",
    "h is the height. Balanced ⇒ h = O(log n). A sorted insert chain is a linked list, h = n.",
    "JS has no std balanced BST. You say: 'I assume random keys or I would use an array + sort / a Map if I only need identity.' Interview trees are usually given as already-built nodes.",
    "BST operations are always O(log n).",
    "What does a treemap give you that Map does not?")

add("structures", "heap", "Where is the left child of index i in an array heap?",
    "2i+1 and 2i+2. Parent is floor((i-1)/2).",
    "Index 0 is the root (min or max). siftUp after insert at the end; siftDown after swap-with-last on pop. Off-by-one here is the entire bug surface. JS has no std heap — you implement it or sort.",
    "Left child is i+1 like a binary tree in an array of heap-ordered nodes... wait, no.",
    "Implement peek / push / pop for a min-heap of numbers.")

add("structures", "heap", "When is a heap the right tool vs sort?",
    "You need the current min/max repeatedly while the set changes, or top-k of a stream.",
    "kth largest: min-heap of size k is O(n log k). Sorting is O(n log n) and simpler — say both. Merge k sorted lists: min-heap of heads. Scheduling: earliest deadline first. If you need the whole order once, sort.",
    "Heaps sort in O(n).",
    "Why is heap sort not stable and rarely used in JS?")

add("structures", "heap", "Build-heap is O(n). Why not O(n log n)?",
    "You siftDown from the last parent. Most nodes are near the leaves and move O(1).",
    "The series is n/4 * 1 + n/8 * 2 + ... which sums to O(n). n inserts from empty is O(n log n). Interview: 'I'll heapify if I already have the array.'",
    "Building is n inserts.",
    "Write heapify in place on an array.")

add("structures", "graph", "Adjacency list vs matrix in JS?",
    "List: Map or array of arrays, O(V+E) space. Matrix: V×V, O(1) edge check, O(V²) space.",
    "Interview graphs are sparse — list wins. Grid graphs do not store edges; neighbors are the 4 (or 8) index deltas. Weighted: store {to, w}. Undirected: add both directions once, carefully.",
    "Always use a matrix so lookup is O(1).",
    "How do you represent a board as a graph without allocating V²?")

add("structures", "graph", "When is BFS the shortest path?",
    "Unweighted edges (or all weights equal). First time you reach the target is fewest hops.",
    "Word ladder, grid maze with cost 1, binary tree min depth. Weighted positive: Dijkstra (heap). Negative: Bellman-Ford. 0-1 weights: deque. Do not Dijkstra an unweighted grid — it is BFS with extra steps.",
    "BFS is shortest for any weights.",
    "Why does DFS fail as a shortest-path algorithm?")

add("structures", "graph", "Cycle in a directed graph — three colors or Kahn?",
    "Both. Kahn: if you cannot process V nodes, there is a cycle. DFS: visiting a node already on the recursion stack.",
    "course schedule is the poster child. Undirected cycles need a parent skip so you do not treat the back-edge to parent as a cycle. State it.",
    "Any revisit is a cycle in a directed graph (including a cross edge).",
    "How do you return one cycle, not just a boolean?")

add("structures", "graph", "Topological order — who can go first?",
    "Nodes with indegree 0. Kahn peels them, reducing neighbors' indegrees.",
    "Only DAGs have a topo order. Multiple answers are legal — say so. Use it for build systems, course order, spreadsheet formulas. DFS postorder reversed is the other construction.",
    "Topo sort is BFS that visits by value.",
    "What happens if two packages depend on each other?")

add("patterns", "search", "Binary search bug: why lo + hi >> 1 and lo <= hi?",
    "Mid is (lo+hi)>>1 or lo+((hi-lo)>>1). Loop while lo <= hi when you return mid on hit.",
    "lo < hi is for 'first position' searches where you shrink to a single index. Off-by-one is the skill. Rotated array: one side of mid is sorted; ask if target lives there.",
    "Always use (lo+hi)/2 and Math.round.",
    "Write lowerBound: first index with a[i] >= x.")

add("patterns", "twopointer", "What must be true before two pointers on a sum problem?",
    "The array is sorted (or you sort a copy). Otherwise inward movement has no meaning.",
    "container-with-most-water does not need sort — the invariant is 'move the shorter side.' 3Sum sorts then fixes i. Opposite direction vs same direction (slow/fast compact, sliding window).",
    "Two pointers work on any array.",
    "Why do you skip duplicates after a hit in 3Sum?")

add("patterns", "window", "Fixed vs variable sliding window?",
    "Fixed: window length k is given (max sum of k). Variable: grow/shrink until a constraint holds (longest unique substring).",
    "Variable: right always advances; left advances while invalid. Each index enters/leaves at most once → O(n). Need a Map/count to know validity. Do not restart from scratch at each i.",
    "Sliding window is another name for two pointers on a linked list.",
    "Why can 'at most k distinct' use a window but 'exactly sum k with negatives' cannot?")

add("patterns", "window", "Why do negatives break the usual 'shrink when sum > k' window?",
    "Adding a negative can make a later larger window necessary; the sum is not monotonic.",
    "Use prefix sums + Map (count of prefix values) for subarray sum = k with negatives. The monotonic shrink only works for all-non-negative arrays.",
    "Window always works for any sum problem.",
    "How does the prefix Map recover the number of subarrays, not just existence?")

add("patterns", "prefix", "Prefix sum in one sentence.",
    "pref[i] = sum of the first i elements. A range sum is pref[r] - pref[l].",
    "Store pref in an array or a running total. For count of subarrays with sum k: if pref - k was seen, those start indexes work. Same idea for xor, and for 2D (inclusion of rectangles).",
    "Prefix means the first half of the array.",
    "How do you get O(1) range sum after O(n) preprocess?")

add("patterns", "backtrack", "What is the backtracking template?",
    "Choose, recurse, unchoose (pop). Stop at a complete / invalid node.",
    "subsets: take or skip. permutations: used flags. combination sum: start index to kill duplicates / control reuse. Always path.slice() when you store a result — the path array is reused. Bound early (left < 0).",
    "Backtracking is dynamic programming.",
    "Why do you copy the path when you push to answers?")

add("patterns", "backtrack", "How do you avoid duplicate subsets when nums has duplicates?",
    "Sort. Skip a value if it equals the previous and the previous was not taken in this slot.",
    "The standard 'if (i>start && nums[i]===nums[i-1]) continue' at a given depth. Without sort, duplicates are not adjacent and the skip fails.",
    "Put results in a Set of JSON.stringify — that is the real solution.",
    "What is the time of subsets even without duplicates?")

add("patterns", "dp", "How do you know a problem is DP?",
    "Optimal substructure + overlapping subproblems. You can name a state and a transition.",
    "Ask: if I knew the answer for smaller n / a prefix / a subset of coins, could I finish in O(1) or O(choices)? If the same state is asked many times, memoize or tabulate. If every state is unique, it is just recursion / backtrack.",
    "DP means a 2D array.",
    "What is the state for coin change (fewest coins)?")

add("patterns", "dp", "Memoization vs tabulation — say the difference.",
    "Memo: top-down, hash/array of 'already computed.' Tabulation: bottom-up loops from base cases.",
    "Same recurrence. Memo only touches reachable states. Table makes iteration order obvious and often uses O(1) rolling arrays (house robber, climbing stairs). Interviewers like you to write the recurrence first, then pick.",
    "Tabulation is faster Big-O than memo for the same recurrence.",
    "Why can house robber roll two scalars?")

add("patterns", "dp", "Unbounded vs 0/1 knapsack in coin problems.",
    "Unbounded: you may reuse a coin — loop amount, inner coins (or coins outer, still reuse). 0/1: each item once — iterate items, walk the amount array backwards.",
    "coinChange fewest is unbounded. If each coin can be used once, reverse the inner loop so you do not reuse the updated cell. This is the classic footgun.",
    "The loop order never matters.",
    "Show both loop orders and what they compute.")

add("patterns", "dp", "LIS in O(n log n) — what does the tails array mean?",
    "tails[i] is the smallest tail of an increasing subsequence of length i+1.",
    "Not the LIS itself. Binary search the first tail >= x and replace. Patience sorting. O(n²) DP (dp[i] = 1+max over j<i) is the version you must also be able to write and prove.",
    "tails is the LIS sequence.",
    "How do you reconstruct one actual LIS, not only the length?")

add("expert", "design", "Implement LRU in JS without a DLL. Is that legal?",
    "Yes. ECMAScript Map iterates in insertion order. delete+set moves a key to most-recent.",
    "You should still be able to draw Map + doubly linked list: HashMap to node, splice to head on access, evict tail. That is the language-agnostic answer. Mention both.",
    "Map order is unspecified so LRU is impossible without a list.",
    "What breaks if you forget to refresh on get?")

add("expert", "design", "Trie vs Map of whole words for autocomplete?",
    "Trie shares prefixes: startsWith is O(L). A Map only tells you exact keys unless you scan all keys.",
    "Each node is a Map of char → child plus an end flag. Memory can be large; for huge dictionaries a compressed trie / ternary / server index wins. In the browser, a trie of 5k product names is fine.",
    "A Set of words supports prefix queries in O(1).",
    "How do you rank suggestions (heap vs sort of a small list)?")

add("expert", "design", "Union-find: what do path compression and union-by-rank do?",
    "Find flattens the path to the root. Union attaches the smaller tree under the larger. Together, almost O(1) per op.",
    "parent[i] starts as i. find(i) recursively sets parent[i] = find(parent[i]). Without heuristics you can still get a stick and O(n). accounts merge / islands / Kruskal use this.",
    "Union-find is a heap.",
    "Why is 'almost O(1)' inverse Ackermann and not a lie in interviews?")

add("expert", "graph", "When do you flood-fill a grid vs union-find islands?",
    "Flood fill (DFS/BFS) is the default for count-islands. Union-find if you add land over time (number of islands online).",
    "DFS mutates '1'→'0' or a visited matrix. Watch stack depth on a 1000×1000 snake — iterative stack or BFS. Union-find indexes r*C+c.",
    "Union-find is required for any island problem.",
    "How do you count islands as bits flip from 0 to 1 in a stream?")

add("expert", "tree", "Serialize a binary tree — why markers for null?",
    "Without nulls you cannot distinguish missing children when you deserialize.",
    "Preorder + '#' (or JSON null) is enough. LeetCode-style level order with trailing nulls also works. BST can serialize as values only if you rebuild via BST insert — different problem. Say the format first.",
    "Inorder uniquely determines a binary tree.",
    "Why does inorder + preorder uniquely determine a tree if values are unique?")

add("expert", "search", "Median of two sorted arrays in log time — the idea only.",
    "Binary search the cut in the shorter array so left parts have the right count and max(left) <= min(right).",
    "You do not merge O(m+n). Partition A at i, B at j = half - i. Tweak i until the order condition holds. Even/odd total decides one vs two center values. Implementing this under a clock is expert; explaining the cut is the bar.",
    "Two pointers from both starts is O(log (m+n)).",
    "What is the naive O(m+n) you would ship in production?")

add("expert", "stack", "Largest rectangle in histogram — why a monotonic stack?",
    "For each bar, you need the nearest smaller bar on the left and right. Those bound the width.",
    "Increasing stack of indexes. When you pop, the current index is the first smaller on the right; the new top is the first smaller on the left. Width = right - left - 1. Sentinel 0 at the end flushes.",
    "The answer is always the tallest bar times n.",
    "How is this the same family as daily temperatures?")

add("fundamentals", "js", "What do you say before you start coding a DSA problem?",
    "Input types and constraints, examples including empty/one, brute force, then the intended complexity.",
    "Ask n, value ranges, negatives, duplicates, mutate or not, multiple answers. State brute O(n²) so the O(n) idea looks chosen, not lucky. Then write. Then trace one example out loud.",
    "Start typing the first idea that compiles.",
    "What do you do when you are stuck at minute 12?")

add("fundamentals", "js", "Stuck at minute 12. What is the senior move?",
    "Say the brute force, name the bottleneck, try one pattern family (hash, sort+two pointer, window, BFS).",
    "Do not silent-spiral. Narrate: 'Hashing the complement is two-sum. This looks like that if I freeze i.' If you cannot finish optimal, finish correct brute and say the upgrade. Empty / one-element tests while you think.",
    "Ask for a hint immediately or delete everything.",
    "Which pattern family fits 'longest / shortest substring with constraint'?")

add("patterns", "array", "Kadane in one sentence.",
    "The best subarray ending here is either this element alone or this element plus the best ending previously.",
    "best = max(best, cur); cur = max(x, cur+x). Handles all-negative if you start from a[0], not 0. Empty array is a spec question — usually n>=1.",
    "Kadane is divide and conquer only.",
    "How do you also return the start and end indexes?")

add("patterns", "array", "Why no division in product-except-self?",
    "Zeros and interview constraint. Prefix × suffix.",
    "First pass: out[i] = product of left. Second: multiply running right product. Two zeros → all zeros. One zero → only that index is the product of the rest.",
    "Divide total product by nums[i]; special-case zero if you are clever.",
    "Can you do it in one pass? (You can, with two running products from both ends.)")

add("javascript", "js", "Why is for...in wrong on arrays in algorithm code?",
    "It walks enumerable keys, including inherited / extra properties, as strings, not 0..length-1 in a guaranteed numeric order you want.",
    "Use for (let i=0;i<n;i++) or for...of. for...in on {0:1,1:2} looks like it works until someone adds arr.foo = 1. Interview code should look boring.",
    "for...in is the modern way to walk arrays.",
    "What does for...of on a Map give you?")

add("javascript", "js", "slice vs splice — which mutates?",
    "splice mutates. slice returns a copy (or a window copy).",
    "arr.slice(1) is a shallow copy from 1. arr.splice(i,1) removes and shifts — O(n). In algorithm code prefer a write index over splice in a loop (that is O(n²)).",
    "They are aliases.",
    "What is the complexity of removing all zeros with repeated splice?")

add("structures", "hash", "Anagram check: sort vs count.",
    "Sort both O(n log n). Count letters O(n) time O(1) for a fixed alphabet.",
    "Unicode: Map of code points. Interview English lowercase: int[26]. If they ask follow-up 'group anagrams', the key is the count signature or the sorted string.",
    "JSON.stringify a Map is a good key.",
    "How do you group anagrams in O(n · L)?")

add("structures", "tree", "Iterative inorder — the picture.",
    "Walk left pushing, pop/visit, go right.",
    "const st=[]; let n=root; while(st.length||n){ while(n){ st.push(n); n=n.left;} n=st.pop(); visit(n); n=n.right; } This is also how you get the next node in a BST iterator (controlled pause).",
    "Inorder is BFS.",
    "How do you kth-smallest in a BST with this walk?")

add("structures", "graph", "Visited set: when do you mark — enqueue or dequeue?",
    "Usually when you enqueue (or when you first see the node) so you do not flood the queue with duplicates.",
    "Marking late can explode a grid BFS with many paths to the same cell. For Dijkstra you may relax multiple times (or use a better decrease-key). Say which model you are in.",
    "Never mark; just hope.",
    "Why does number-of-islands mark immediately on visit?")

add("expert", "dp", "Digit DP / bitmask DP — when do you even mention them?",
    "When n is tiny as a set (bitmask, n≤20) or you count numbers with digit constraints.",
    "Do not lead with this on a two-sum. bitmask: dp[mask] = best over subsets. Expert-level follow-up. Most senior FE interviews never need it; knowing the shape is enough to not freeze.",
    "Every DP is a bitmask.",
    "What is 2^20 and why does that bound n?")

add("expert", "graph", "Dijkstra in JS — heap of [dist, node], skip stale pops.",
    "Push new pairs instead of decrease-key. If you pop a node with dist > best[u], continue.",
    "best starts at Infinity, best[src]=0. Neighbors: nd = d+w; if nd < best[v] update and push. This is the practical JS pattern because we lack decrease-key. Complexity O((V+E) log V) with a binary heap.",
    "Relax after the node is popped as processed without a stale check — always wrong with extra pushes.",
    "When would you use A* instead?")

add("javascript", "practical", "Where does a graph show up in a JS build or monorepo?",
    "Package dependencies are a directed graph. Install / build order is a topological sort. A cycle is 'unable to resolve'.",
    "Same as course schedule. Tools (webpack, turborepo) walk this graph. In the app, route trees and React trees are trees; they become DAGs if you share nodes (cache).",
    "npm uses a binary search tree of packages.",
    "How would you detect a circular import in a toy bundler?")

add("javascript", "practical", "Undo/redo is which structure?",
    "Two stacks: undo pops from past and pushes onto future; a new action clears future.",
    "Each entry is a command or a snapshot. Snapshots are simpler and heavier; commands are inverse pairs. Do not store the whole document if a delta will do. Practical study in this course implements the stacks.",
    "Undo is a queue so the oldest edit undoes first.",
    "Where do you put undo in Redux vs a ref?")

add("javascript", "practical", "Rate limiter: why a queue of timestamps, not a counter only?",
    "A sliding window needs to drop timestamps older than now - window. A single counter cannot expire the right ones.",
    "While (q[0] <= now - W) dequeue; if length < limit, enqueue now and allow. Token bucket is the other model (refill rate). Counters work for fixed windows but burst at the boundary.",
    "Date.now() % window is a sliding window.",
    "How would you rate-limit per user in Node with Redis?")

add("javascript", "practical", "Virtual list: which algorithm idea?",
    "Only mount items whose y-range intersects the viewport. That is a window over an array, plus a spacer height.",
    "itemHeight * n is the scroll height (fixed height). Variable height needs a prefix-sum of heights and a binary search for the start index. Overscan a few rows. This is sliding window + prefix, not a new structure.",
    "Render all rows; the browser virtualizes automatically.",
    "What breaks a11y if you destroy offscreen rows?")

add("javascript", "practical", "Reconcile a list by key — what DSA is that?",
    "Map from key → old node/fiber, then walk the new list and reuse.",
    "React keys are the hash join between old and new children. Wrong keys reuse the wrong component state (inputs swap). Index keys are a list that never reorders. Same idea as 'merge two sequences by id.'",
    "Keys are CSS classes.",
    "Why does a missing key turn a list update into a worse algorithm?")

add("patterns", "graph", "Grid shortest path — 4-direction BFS. What do you store in the queue?",
    "[r, c, dist] or [r,c] and a dist matrix. Mark visited when enqueue.",
    "Do not DFS and hope. Obstacles skip. If moving has different costs, heap. If you can remove k walls, state is (r,c,k) — that is a 3D BFS, expert follow-up.",
    "A* is required for any grid.",
    "How does the state change if you can teleport between all 'portals'?")

add("fundamentals", "complexity", "Space of recursion on a linked list of n vs a balanced tree of n?",
    "List chain: O(n) stack. Balanced tree: O(log n). Skew tree: O(n).",
    "Always name the worst tree shape unless the problem says complete/balanced. Iterative reverseList is O(1) extra — prefer it. Tail-call is not reliable in JS.",
    "Recursion is O(1) because we did not new an array.",
    "Will TCO save your DFS in the browser?")

add("javascript", "js", "Why copy objects in algorithm answers when you mutate?",
    "You must not destroy the caller's graph unless asked. Cloning needs a Map from old node → new (clone graph).",
    "Shallow copy ({...n}) keeps the same neighbor references — that is not a clone. JSON.parse(JSON.stringify) dies on cycles. The Map is the algorithm.",
    "spread is a deep clone.",
    "How does cloneGraph terminate?")

add("expert", "design", "Autocomplete: trie + heap of top k vs filter+sort of 50 results?",
    "If the dictionary is huge and queries are prefixes, trie (or a server index). If you already have 50 hits, sort them — O(50 log 50) is free.",
    "Do not heap-sort 50 strings in an interview to look smart. Use the structure that matches scale. Mention debounce + abort on the network; that is product, not DSA, and interviewers like the join.",
    "Always build a segment tree of strings.",
    "Where does the rank score live — in the trie node or in a side index?")

add("expert", "prefix", "Difference array — when?",
    "You apply many range increment updates, then one prefix rebuild to get the final array.",
    "diff[l]+=v; if (r+1<n) diff[r+1]-=v; then prefix-sum. O(1) per update, O(n) finalize. Corporate calendar / booking a room range. Inverse of prefix.",
    "Difference array is just arr[i]-arr[i-1] for fun.",
    "How do you range-update a 2D grid?")

add("structures", "stack", "Min stack in O(1) — two approaches.",
    "Parallel stack of current minima, or store pairs [val, minSoFar].",
    "On push, newMin = empty ? x : Math.min(x, mins.at(-1)). Pop both. Do not scan on getMin. Encoding min in a single integer is a cute trick; skip it unless they ask.",
    "Scan the stack every getMin; n is small.",
    "How do you add getMax as well?")

add("patterns", "search", "Rotated sorted array — the invariant on mid.",
    "At least one of [lo,mid] or [mid,hi] is sorted. If target is in the sorted half's range, go there; else the other half.",
    "Duplicates (33 vs 81) break the 'lo <= mid means left sorted' test — you must shrink lo++ when a[lo]===a[mid]===a[hi]. Mention the follow-up.",
    "Find the pivot first in O(n), then binary search.",
    "Can you do it in one pass without finding the pivot first? (Yes.)")

add("fundamentals", "complexity", "Name a hidden O(n²) in innocent-looking JS.",
    "for (const x of arr) out = out.concat(x) or += on strings, or splice/shift inside a loop, or indexOf on a growing list for every item.",
    "concat allocates a new array each time. Prefer push. Building a result with unshift n times. JSON.parse in a tight loop on the same payload. Always point at the allocation.",
    "If there is one for-loop, it cannot be O(n²).",
    "What is the cost of [...arr] inside each recursive call of merge sort?")

add("javascript", "practical", "Dependency install order is course-schedule. What is the node and the edge?",
    "Node = package (or file). Edge = 'A depends on B' meaning B must come first — usually B → A in the graph you Kahn.",
    "Be consistent: edge direction is 'must be before.' Indegree counts unfinished deps. A cycle is a circular dependency error. Same as React lazy() cycles, same as spreadsheet cells.",
    "Alphabetical order is a valid topo sort of any repo.",
    "How would you parallelize the build once you have a topo order?")

add("patterns", "dp", "Unique paths vs unique paths with obstacles.",
    "Same recurrence dp[i][j] = from-above + from-left, but obstacles stay 0 and do not contribute.",
    "First row/col must stop filling after the first wall. Rolling 1D array: walk left-to-right, dp[j] += dp[j-1], zero on obstacle. This is the 'I can compress' flex.",
    "Obstacles need DFS only.",
    "How do you count paths that must visit a cell?")

add("structures", "tree", "LCA in a BST vs in a binary tree.",
    "BST: walk from the root until the nodes split across you (or you hit one). General tree: recurse; if you find one in each subtree, you are the LCA.",
    "BST uses values. General uses presence. Parent pointers: walk up with a Set. Interview: say which tree you were given.",
    "LCA is always the root.",
    "How does the Euler-tour + RMQ method work at a high level?")

add("expert", "design", "What does 'expert' mean in this course — more structures or better judgment?",
    "Both: you can implement trie/UF/heap, and you can pick a boring sort when n is 50.",
    "Expert is not inventing a segment tree on a todo list. It is naming complexity, implementing the structure when asked, mapping it to a product (LRU, undo, deps), and stopping at a design that ships. Phase 1 on this hub then adds volume.",
    "Expert means you have memorized 200 LeetCode ids.",
    "When do you refuse a fancy structure in a design interview?")


def feq() -> str:
    blocks = []
    for i, item in enumerate(Q, 1):
        snip = code("JavaScript", item["snippet"]) if item["snippet"] else ""
        blocks.append(f'''
<article class="q" id="feq-{i}" data-level="{item["level"]}" data-cat="{item["cat"]}" data-search="{esc(item["q"])}" data-stype="Interview question" data-mock="1">
  <div class="meta-row"><span class="badge badge-js">{item["level"]}</span><span class="chip">{item["cat"]}</span><span class="chip">Q{i}</span></div>
  <h3>{i}. {esc(item["q"])}</h3>
  <p><button type="button" class="toggle-btn" data-toggle="feq-a-{i}">Reveal answer</button>
     <button type="button" class="toggle-btn" data-complete="questions" data-cid="feq-{i}">Mark complete</button></p>
  <div class="reveal" id="feq-a-{i}">
    <p><b>Short answer.</b> {item["short"]}</p>
    <p><b>Deep explanation.</b> {item["deep"]}</p>
    {snip}
    <p><b>Common misconception.</b> {item["miss"]}</p>
    <p><b>Senior follow-up.</b> {item["follow"]}</p>
  </div>
</article>''')
    return f'''
<section class="block" id="feq" data-search="DSA JavaScript interview questions" data-stype="Section">
  <p class="kicker">{len(Q)} questions</p>
  <h2 class="section-title">Interview Q&amp;A</h2>
  <p class="lede">Answer standing up. Then reveal. Mark complete only if you can teach the short answer without this file. Practice questions — not claimed official company questions.</p>
  <div class="tabs" data-tabs="feq">
    <button type="button" class="tab active" data-tab="all">All ({len(Q)})</button>
    <button type="button" class="tab" data-tab="fundamentals">fundamentals</button>
    <button type="button" class="tab" data-tab="javascript">javascript</button>
    <button type="button" class="tab" data-tab="structures">structures</button>
    <button type="button" class="tab" data-tab="patterns">patterns</button>
    <button type="button" class="tab" data-tab="expert">expert</button>
  </div>
  {''.join(blocks)}
</section>
'''
