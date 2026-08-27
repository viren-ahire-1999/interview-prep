GYM = {
    "tp-rc-1": {
        "why": (
            "Multiplying x by itself n times is O(n), which blows up when n is large or negative. "
            "Exponentiation by squaring halves the exponent each step, so you need only O(log n) multiplications. "
            "That turns a million-step loop into roughly twenty multiplies."
        ),
        "steps": [
            "Handle n == 0 by returning 1.",
            "If n is negative, flip the sign and plan to return 1 / result at the end.",
            "While n > 1, square the partial result when n is even; when odd, multiply once by x then halve n.",
            "Use unsigned right shift or long arithmetic so -2^31 does not overflow when negated.",
        ],
        "example": (
            "Input: x=2, n=10\n"
            "n=10 even  -> base stays 2, result=1\n"
            "n=5  odd   -> result=2, base=4\n"
            "n=2  even  -> base=16\n"
            "n=1  odd   -> result=32\n"
            "Output: 1024"
        ),
        "trap": (
            "Forgetting negative exponents (answer is 1/x^|n|) or mishandling n = -2^31 "
            "where -n overflows a 32-bit int."
        ),
    },
    "tp-rc-2": {
        "why": (
            "There are exponentially many candidate strings, but most are invalid if you build blindly. "
            "Tracking how many '(' and ')' you have used prunes illegal prefixes before they grow. "
            "You only explore branches that can still close out to a valid string of length 2n."
        ),
        "steps": [
            "Keep open = count of '(' placed and close = count of ')' placed.",
            "If len(path) == 2n, push a copy to the answer list.",
            "If open < n, append '(' and recurse.",
            "If close < open, append ')' and recurse.",
            "Backtrack by removing the last char after each recursive call.",
        ],
        "example": (
            "Input: n=2\n"
            "path='' open=0 close=0 -> add '('\n"
            "path='(' open=1 close=0 -> add '('\n"
            "path='((' open=2 close=0 -> add ')'\n"
            "path='(()' open=2 close=1 -> add ')'\n"
            "path='(())' -> save; also explore '()()' branch\n"
            "Output: ['(())', '()()']"
        ),
        "trap": (
            "Allowing ')' when close >= open creates strings like '())(' that can never be fixed. "
            "Also pushing the same mutable path object instead of a copy."
        ),
    },
    "tp-rc-3": {
        "why": (
            "Each digit maps to several letters, so the output size is the product of those choices. "
            "Recursion walks one digit at a time and tries every letter for that digit. "
            "That systematically enumerates all combinations without nested loops of unknown depth."
        ),
        "steps": [
            "Build a map from digit char to its letter string (skip '0' and '1').",
            "Start DFS at index 0 with an empty path string.",
            "At index i, loop each letter of map[digits[i]], append, recurse to i+1, then pop.",
            "When i == len(digits), push path to answers.",
            "Return early if digits is empty.",
        ],
        "example": (
            "Input: digits='23'\n"
            "i=0 try 'a' -> path='a'\n"
            "i=1 try 'd' -> path='ad' -> save\n"
            "backtrack, try 'e' -> 'ae', 'f' -> 'af'\n"
            "backtrack to i=0, try 'b' then c... same at i=1\n"
            "Output: ['ad','ae','af','bd','be','bf','cd','ce','cf']"
        ),
        "trap": (
            "Off-by-one on the digit index or forgetting to backtrack the last letter "
            "so later branches inherit wrong characters."
        ),
    },
    "tp-rc-4": {
        "why": (
            "Nested arrays form a tree: each inner array is a child. "
            "The depth of the whole structure is one plus the max depth among its children. "
            "A single DFS pass computes this without flattening or counting brackets manually."
        ),
        "steps": [
            "Define depth(arr): if arr is not a list, return 0 (or 1 if counting the leaf box).",
            "If arr is empty, return 1 for 'current box counts'.",
            "For each element, take max depth among children.",
            "Return 1 + that max.",
            "Call depth on the top-level input.",
        ],
        "example": (
            "Input: [1, [2, [3]]]\n"
            "depth([3])     -> 1 (single number inside)\n"
            "depth([2,[3]]) -> 1 + max(0,1) = 2\n"
            "depth(top)     -> 1 + max(0,2) = 3\n"
            "Output: 3"
        ),
        "trap": (
            "Mixing conventions: counting only arrays vs counting the outermost wrapper. "
            "Empty array [] is depth 1 under the usual 'box counts' rule, not 0."
        ),
    },
    "tp-rc-5": {
        "why": (
            "Plain recursion recomputes the same F(k) many times, exploding to exponential time. "
            "Memoization stores each answer the first time it is computed. "
            "Every later call becomes O(1) lookup, giving O(n) total work."
        ),
        "steps": [
            "Base cases: F(0)=0, F(1)=1.",
            "If n is in the cache, return cache[n].",
            "Otherwise set cache[n] = F(n-1) + F(n-2).",
            "Return cache[n].",
            "An iterative loop with two rolling variables is equivalent and avoids stack depth.",
        ],
        "example": (
            "Input: n=5\n"
            "F(2)=1, F(3)=2, F(4)=3, F(5)=5\n"
            "cache after: {0:0, 1:1, 2:1, 3:2, 4:3, 5:5}\n"
            "Output: 5"
        ),
        "trap": (
            "Recursing without caching still hits exponential time. "
            "Using the wrong base (F(2)=2) or indexing off-by-one breaks the sequence."
        ),
    },
    "tp-rc-6": {
        "why": (
            "Building row n literally doubles in size every step, so materializing it is impossible for large n. "
            "Row n has 2^(n-1) bits and the second half is the bitwise flip of the first half. "
            "You can decide which half contains index k and recurse without ever storing the row."
        ),
        "steps": [
            "Base: row 1 is just the bit 0.",
            "Let half = 2^(n-2); if k > half, answer is flip of kthSymbol(n-1, k-half).",
            "If k <= half, answer equals kthSymbol(n-1, k).",
            "Flip means 0->1 and 1->0.",
            "Use 1-based k throughout.",
        ],
        "example": (
            "Input: n=3, k=3\n"
            "row3 length 4; k=3 is in second half of row3\n"
            "flip( kthSymbol(2, 1) )\n"
            "row2 = 01; k=1 -> 0\n"
            "flip(0) = 1\n"
            "Output: 1"
        ),
        "trap": (
            "Using 0-based k or comparing k to the wrong half size (off by one power of two). "
            "Forgetting to flip when k lands in the second half."
        ),
    },
    "tp-tr-1": {
        "why": (
            "Inversion is local: every node only needs its own children swapped. "
            "Post-order recursion handles subtrees first, then swaps at the current node. "
            "One pass touches each node once for O(n) time."
        ),
        "steps": [
            "If root is null, return null.",
            "Recursively invert left and right subtrees.",
            "Swap root.left and root.right.",
            "Return root.",
            "BFS with a queue works too: dequeue, swap children, enqueue them.",
        ],
        "example": (
            "Input:     4\n"
            "         /   \\\n"
            "        2     7\n"
            "       / \\   / \\\n"
            "      1   3 6   9\n"
            "swap at 2 and 7, then at 4\n"
            "Output:    4\n"
            "         /   \\\n"
            "        7     2\n"
            "       / \\   / \\\n"
            "      9   6 3   1"
        ),
        "trap": (
            "Swapping before recursing can still work, but swapping only the root "
            "and forgetting to recurse leaves inner subtrees unchanged."
        ),
    },
    "tp-tr-2": {
        "why": (
            "Symmetry is not about comparing a node to itself but about mirror pairs across the center. "
            "Left of one side must match right of the other with equal values. "
            "A helper that takes two nodes reduces the problem to simple null and value checks."
        ),
        "steps": [
            "Define mirror(a, b): if both null, true; if one null, false.",
            "If a.val != b.val, return false.",
            "Return mirror(a.left, b.right) and mirror(a.right, b.left).",
            "Answer is mirror(root.left, root.right).",
            "Empty tree is symmetric.",
        ],
        "example": (
            "Input:    1\n"
            "         / \\\n"
            "        2   2\n"
            "       / \\ / \\\n"
            "      3  4 4  3\n"
            "mirror(2,2): vals ok; mirror(3,3) and mirror(4,4) both true\n"
            "Output: true"
        ),
        "trap": (
            "Only comparing inorder or only checking root.left.val == root.right.val "
            "misses deeper asymmetry."
        ),
    },
    "tp-tr-3": {
        "why": (
            "You do not need to store paths; subtract each node value from the target as you walk down. "
            "At a leaf, whatever remains must be exactly zero. "
            "That turns path search into a single downward pass with O(h) stack space."
        ),
        "steps": [
            "If root is null, return false.",
            "Compute remain = target - root.val.",
            "If root is a leaf, return remain == 0.",
            "Return hasPathSum(left, remain) or hasPathSum(right, remain).",
            "Do not treat a single-child node as a leaf unless it has no children.",
        ],
        "example": (
            "Input: root=5, target=22\n"
            "        5\n"
            "       / \\\n"
            "      4   8\n"
            "     /   / \\\n"
            "   11  13  4\n"
            "Path 5->4->11->2: remain 22-5-4-11=2 at leaf 2 -> true\n"
            "Output: true"
        ),
        "trap": (
            "Checking target == 0 at internal nodes, or treating a node with one child as a leaf."
        ),
    },
    "tp-tr-4": {
        "why": (
            "The longest path may not go through the root, so a global best tracker is needed. "
            "At each node, the best path through that node is leftHeight + rightHeight. "
            "Computing height bottom-up gives both pieces in one DFS."
        ),
        "steps": [
            "Keep a global best = 0 (edge count).",
            "height(node): if null, return 0.",
            "leftH = height(node.left), rightH = height(node.right).",
            "best = max(best, leftH + rightH).",
            "Return 1 + max(leftH, rightH) to parent.",
        ],
        "example": (
            "Input:    1\n"
            "         / \\\n"
            "        2   3\n"
            "       / \\\n"
            "      4   5\n"
            "At node 2: leftH=1, rightH=1 -> through-2 diameter=2\n"
            "At node 1: leftH=2, rightH=1 -> through-1 diameter=3\n"
            "Output: 3 edges (path 4-2-1-3 or 5-2-1-3)"
        ),
        "trap": (
            "Returning leftH + rightH as the height instead of 1 + max(leftH, rightH), "
            "which double-counts and breaks parent height."
        ),
    },
    "tp-tr-5": {
        "why": (
            "In a general binary tree the LCA is the deepest node where p and q diverge into different subtrees. "
            "Post-order search tells you whether each side contains p or q. "
            "The first node that gets non-null from both sides is the answer."
        ),
        "steps": [
            "If root is null or root is p or q, return root.",
            "left = search(root.left), right = search(root.right).",
            "If both left and right are non-null, root is the LCA.",
            "Otherwise return whichever side is non-null.",
            "Works for general binary trees, not only BSTs.",
        ],
        "example": (
            "Input: tree with nodes 3,5,1,6,2,0,8; p=5, q=1\n"
            "search at 5 returns 5; search at 1 returns 1\n"
            "At 3: left=5-side, right=1 -> both found -> LCA=3\n"
            "Output: node 3"
        ),
        "trap": (
            "Using BST ordering (val comparisons) on a non-BST, "
            "or returning p immediately when q is in p's subtree (must bubble up)."
        ),
    },
    "tp-tr-6": {
        "why": (
            "A node is good if no ancestor has a larger value, so you only need the max seen so far on the path. "
            "Pass that max down during DFS and increment when node.val >= maxSoFar. "
            "No need to compare against all ancestors each time."
        ),
        "steps": [
            "DFS(node, maxSoFar): if null, return 0.",
            "If node.val >= maxSoFar, count = 1; else 0.",
            "newMax = max(maxSoFar, node.val).",
            "Return count + DFS(left, newMax) + DFS(right, newMax).",
            "Start with maxSoFar = -infinity (or root.val handled separately).",
        ],
        "example": (
            "Input:    3\n"
            "         / \\\n"
            "        1   4\n"
            "       / \\ / \\\n"
            "      3  4 1  5\n"
            "Root 3 good; 1 not; 4 good; leaf 3 not (max 3 on path); leaf 4 good; 1 not; 5 good\n"
            "Output: 4"
        ),
        "trap": (
            "Using > instead of >= misses equal values on the path. "
            "Updating maxSoFar after counting instead of before visiting children."
        ),
    },
    "tp-tr-7": {
        "why": (
            "From the right, you see the last node processed at each depth before anything to its left blocks it. "
            "BFS naturally gives the last node per level. "
            "DFS-right-first records the first node seen at each depth, which is the same set."
        ),
        "steps": [
            "BFS: queue with root; while queue, process entire level, keep last val.",
            "Append that val to answer after each level.",
            "DFS alternative: if depth == len(ans), append val; recurse right then left.",
            "Increment depth when going to children.",
            "Empty tree returns [].",
        ],
        "example": (
            "Input:    1\n"
            "         / \\\n"
            "        2   3\n"
            "         \\   \\\n"
            "          5   4\n"
            "Level 0: [1]; level 1: [2,3] last=3; level 2: [5,4] last=4\n"
            "Output: [1, 3, 4]"
        ),
        "trap": (
            "Taking the rightmost node by value instead of by traversal order, "
            "or DFS left-first which records the wrong node at each depth."
        ),
    },
    "tp-tr-8": {
        "why": (
            "Preorder is root, then left subtree, then right subtree. "
            "Flattening in place means rewiring pointers so right child chains follow that order. "
            "Processing from right to left with a prev pointer builds the tail of the list as you unwind."
        ),
        "steps": [
            "Initialize prev = null.",
            "DFS(node): if null, return.",
            "Recurse node.right, then node.left.",
            "Set node.right = prev, node.left = null.",
            "Set prev = node.",
        ],
        "example": (
            "Input:    1\n"
            "         / \\\n"
            "        2   5\n"
            "       / \\   \\\n"
            "      3   4   6\n"
            "Process order (reverse preorder): 6,5,4,3,2,1\n"
            "Wire: 5->6, 2->4->3, 1->2\n"
            "Output: 1->2->3->4->5->6, all left=null"
        ),
        "trap": (
            "Recursing left before right builds the wrong order. "
            "Forgetting to null out left pointers leaves a cycle or breaks the list shape."
        ),
    },
    "tp-tr-9": {
        "why": (
            "BST inorder visits values in sorted order, so the k-th pop is the k-th smallest. "
            "Iterative inorder avoids recursion depth and lets you stop early at k. "
            "That is O(h + k) instead of sorting all nodes."
        ),
        "steps": [
            "Stack = [], cur = root.",
            "While stack or cur: go left pushing nodes, then pop.",
            "On each pop, decrement k; when k == 0, return that node.val.",
            "Move cur to popped.right and continue.",
            "No need to traverse the whole tree once k hits zero.",
        ],
        "example": (
            "Input: BST root=[3,1,4,null,2], k=1\n"
            "Inorder pops: 1 (k=0) -> stop\n"
            "Output: 1"
        ),
        "trap": (
            "Using 0-based k, or counting nodes in preorder/postorder instead of inorder. "
            "Not moving cur to right child after a pop skips the rest of the subtree."
        ),
    },
    "tp-tr-10": {
        "why": (
            "BST order lets you skip entire subtrees that cannot hold values in [low, high]. "
            "If node.val is too small, everything left is also too small. "
            "If too large, everything right is too large. Pruning beats visiting every node."
        ),
        "steps": [
            "If node is null, return 0.",
            "If node.val < low, return rangeSum(node.right, low, high).",
            "If node.val > high, return rangeSum(node.left, low, high).",
            "Else return node.val + left sum + right sum.",
            "Only fully explore when val is inside the range.",
        ],
        "example": (
            "Input: root=[10,5,15,3,7,null,18], low=7, high=15\n"
            "10 in range: sum 10 + left(7 in range: 5+7) + right(15 in range: 15)\n"
            "Skip 3 and 18 branches pruned by comparisons\n"
            "Output: 32"
        ),
        "trap": (
            "Still recursing both sides when val < low or val > high, "
            "which defeats BST pruning and wastes time."
        ),
    },
    "tp-hp-1": {
        "why": (
            "You always need the two largest stones next, and the result may re-enter the pool. "
            "A max-heap gives O(log n) access to the top two instead of resorting the whole array each round. "
            "That keeps the smash simulation efficient."
        ),
        "steps": [
            "Push all weights into a max-heap (negate for a min-heap in Python).",
            "While more than one stone remains, pop two largest a and b.",
            "If a != b, push a - b back.",
            "Return the last stone or 0 if empty.",
            "Each smash is at most two pops and maybe one push.",
        ],
        "example": (
            "Input: [2,7,4,1,8,1]\n"
            "Pop 8,7 -> push 1 -> [2,4,1,1,1]\n"
            "Pop 4,2 -> push 2 -> [2,1,1,1]\n"
            "Pop 2,1 -> push 1 -> [1,1,1]\n"
            "Pop 1,1 -> equal, nothing pushed -> [1]\n"
            "Output: 1"
        ),
        "trap": (
            "Using a min-heap without negating values picks the lightest stones. "
            "Pushing zero after equal smashes adds useless work."
        ),
    },
    "tp-hp-2": {
        "why": (
            "You only need to keep the k closest points, not sort all n. "
            "A max-heap of size k holds the k best so far; anything farther than its root is discarded. "
            "That is O(n log k) versus O(n log n) full sort."
        ),
        "steps": [
            "Define dist(p) = x*x + y*y (skip sqrt).",
            "Iterate points; push (dist, point) on a max-heap keyed by dist.",
            "If heap size > k, pop the farthest.",
            "After the loop, heap holds k closest (any order).",
            "Alternative: sort by dist in O(n log n).",
        ],
        "example": (
            "Input: points=[[1,3],[-2,2],[5,8],[0,1]], k=2\n"
            "dists: 10, 8, 89, 1\n"
            "Heap after scan (max at top): keeps [0,1] and [-2,2]; drops [1,3] and [5,8]\n"
            "Output: [[0,1], [-2,2]] (order may vary)"
        ),
        "trap": (
            "Using a min-heap without a size cap keeps all points. "
            "Comparing x+y instead of x^2+y^2 breaks ordering."
        ),
    },
    "tp-hp-3": {
        "why": (
            "The k largest elements are exactly the ones that survive if you only ever drop the smallest among a size-k window. "
            "A min-heap of size k keeps that window: its root is the k-th largest overall. "
            "One pass beats sorting when k is much smaller than n."
        ),
        "steps": [
            "Push each num into a min-heap.",
            "Whenever size exceeds k, pop the smallest.",
            "After scanning all nums, heap[0] is the k-th largest.",
            "Do not pop down to empty; stop when size equals k.",
            "For duplicates, heap semantics still hold.",
        ],
        "example": (
            "Input: nums=[3,2,1,5,6,4], k=2\n"
            "Push 3,2 -> [2,3]; push 1 pop 1 -> [2,3]; push 5 pop 2 -> [3,5]\n"
            "Push 6 pop 3 -> [5,6]; push 4 pop 4 -> [5,6]\n"
            "Output: 5"
        ),
        "trap": (
            "Using a max-heap of size k keeps the k smallest instead. "
            "Sorting descending and taking index k-1 works but ignores the heap requirement in interviews."
        ),
    },
    "tp-hp-4": {
        "why": (
            "Each add may introduce a value larger than the current k-th largest, so the window must update online. "
            "The same size-k min-heap from the static problem works: push, then pop if oversized. "
            "The root always reflects the k-th largest after every add."
        ),
        "steps": [
            "In __init__, seed heap with nums and trim to size k.",
            "add(val): push val; if len > k, pop smallest.",
            "Return heap[0] as the current k-th largest.",
            "No need to resort on each call.",
            "Heap stores the k largest elements seen so far.",
        ],
        "example": (
            "Input: KthLargest(3, [4,5,8,2]); add(3); add(5); add(10); add(9); add(4)\n"
            "Init heap top 4; after adds returns 4,5,5,8,8\n"
            "Output sequence: 4, 4, 5, 5, 8, 8"
        ),
        "trap": (
            "Returning the k-th smallest from the min-heap root without maintaining size k. "
            "Forgetting to trim the initial nums list to k elements."
        ),
    },
    "tp-hp-5": {
        "why": (
            "Each position's true value lies within k slots ahead in the sorted order, so a sliding window of k+1 elements always contains the next output. "
            "A min-heap extracts the smallest in that window in O(log k) time. "
            "When k is tiny this beats O(n log n) full sort."
        ),
        "steps": [
            "Push the first min(k+1, n) elements into a min-heap.",
            "For i from 0 to n-1: pop heap min into arr[i].",
            "If i+k+1 < n, push arr[i+k+1] into the heap.",
            "Heap never holds more than k+1 items.",
            "Array becomes sorted in place logically via write index.",
        ],
        "example": (
            "Input: arr=[6,5,3,2,8,10,9,1], k=2\n"
            "Window heap min writes: 2,3,5,6,8,9,10,1 -> sorted\n"
            "Output: [1,2,3,5,6,8,9,10]"
        ),
        "trap": (
            "Heap size k instead of k+1 misses the correct next element. "
            "Pushing before writing without advancing the read index duplicates values."
        ),
    },
    "tp-hp-6": {
        "why": (
            "The median splits the stream into a lower and upper half. "
            "Two heaps keep the lower half in a max-heap and the upper in a min-heap so the tops meet in the middle. "
            "Rebalancing after each insert gives O(log n) add and O(1) median read."
        ),
        "steps": [
            "low = max-heap (negate in Python), high = min-heap.",
            "On addNum(x): push to low first, then balance.",
            "Move low's max to high if low is bigger; if high is larger than low by more than 1, move high's min to low.",
            "findMedian: if equal sizes, average both tops; else top of the larger heap.",
            "Keep size difference at most 1.",
        ],
        "example": (
            "Input: add 1, add 2, findMedian, add 3, findMedian\n"
            "After 1,2: low=[1], high=[2] -> median 1.5\n"
            "After 3: low=[2], high=[3] or low=[1,2] high=[3] balanced -> median 2\n"
            "Output: 1.5 then 2.0"
        ),
        "trap": (
            "Putting all values in one heap forces O(n) median reads. "
            "Wrong rebalance rule lets one heap outgrow the other by 2+ and picks the wrong middle."
        ),
    },
    "tp-gr-1": {
        "why": (
            "Flood fill is connected-component recoloring from a seed pixel. "
            "DFS or BFS spreads to 4-neighbors that still match the original color. "
            "Marking visited or checking color stops infinite loops on cycles."
        ),
        "steps": [
            "Let old = image[sr][sc], newColor = color; if old == newColor, return image.",
            "DFS(r,c): if out of bounds or image[r][c] != old, return.",
            "Paint image[r][c] = newColor.",
            "Recurse to four neighbors.",
            "Return image when the component is fully painted.",
        ],
        "example": (
            "Input: image=[[1,1,1],[1,1,0],[1,0,1]], sr=1, sc=1, color=2\n"
            "Paint (1,1) and spread to connected 1s in four directions\n"
            "Output: [[2,2,2],[2,2,0],[2,0,1]]"
        ),
        "trap": (
            "Not returning early when newColor equals old (infinite recursion). "
            "Using 8-connectivity when the problem specifies 4-neighbors only."
        ),
    },
    "tp-gr-2": {
        "why": (
            "Each island is a connected component of 1s. "
            "DFS from an unvisited land cell counts cells while sinking them to 0 so they are not counted twice. "
            "Tracking the max component size across all starts gives the answer."
        ),
        "steps": [
            "Scan every cell; when grid[r][c] == 1, start DFS.",
            "DFS returns 1 plus sizes from four neighbors after setting grid[r][c] = 0.",
            "Update global max with each DFS result.",
            "Skip water cells.",
            "Return max (0 if no land).",
        ],
        "example": (
            "Input: grid=\n"
            "[[0,0,1,0,0],\n"
            " [0,0,0,0,0],\n"
            " [0,1,1,0,1],\n"
            " [0,1,0,0,1]]\n"
            "Islands of size 1, 3, 2 -> max=3\n"
            "Output: 3"
        ),
        "trap": (
            "Counting land without marking visited leads to exponential re-walks. "
            "Using 8-direction connectivity when the problem says 4-connected."
        ),
    },
    "tp-gr-3": {
        "why": (
            "All rotten oranges spread simultaneously each minute, which is multi-source BFS on a grid. "
            "Seeding the queue with every rotten at time 0 models parallel infection. "
            "Layer-by-layer BFS counts minutes until no fresh remain."
        ),
        "steps": [
            "Count fresh; enqueue all (r,c) with value 2 at minute 0.",
            "BFS: dequeue, infect 4-neighbors that are fresh, decrement fresh count.",
            "Track minutes per level (queue size snapshot).",
            "If fresh > 0 after BFS, return -1.",
            "Else return minutes (0 if none were fresh).",
        ],
        "example": (
            "Input: grid=[[2,1,1],[1,1,0],[0,1,1]]\n"
            "t=0: rotten at (0,0)\n"
            "t=1: (0,1),(1,0); t=2: (0,2),(1,1); t=3: (2,1); t=4: (2,2)\n"
            "Output: 4"
        ),
        "trap": (
            "Running DFS so oranges do not rot in sync by minute. "
            "Forgetting to check leftover fresh after BFS and returning minutes anyway."
        ),
    },
    "tp-gr-4": {
        "why": (
            "Rooms and keys form a directed graph: each room points to rooms its keys unlock. "
            "Reachability from room 0 determines whether all rooms can be entered. "
            "One DFS or BFS visit marks every room you can actually reach."
        ),
        "steps": [
            "seen = set with 0; stack or queue = [0].",
            "While stack: pop room r, for each key in rooms[r], if unseen add and push.",
            "After traversal, return len(seen) == len(rooms).",
            "Graph may have cycles; seen prevents rework.",
            "Empty key lists are fine.",
        ],
        "example": (
            "Input: rooms=[[1],[2],[3],[]]\n"
            "Visit 0->1->2->3; seen={0,1,2,3}\n"
            "Output: true"
        ),
        "trap": (
            "Assuming keys must be used in list order (any key in the list opens that room). "
            "Checking only whether room n-1 is reachable instead of all rooms."
        ),
    },
    "tp-gr-5": {
        "why": (
            "Course order is topological sort: prerequisites form a DAG edge b->a. "
            "Kahn's algorithm peels nodes with indegree zero, appending them to the order. "
            "If you cannot process all n nodes, a cycle exists and no valid order exists."
        ),
        "steps": [
            "Build adjacency list and indegree array from pairs [a,b] meaning b before a.",
            "Enqueue all courses with indegree 0.",
            "While queue: pop u, append to order, decrement indegree of neighbors; enqueue if zero.",
            "If len(order) < numCourses, return [].",
            "Else return order.",
        ],
        "example": (
            "Input: numCourses=4, prereqs=[[1,0],[2,0],[3,1],[3,2]]\n"
            "Start 0; then 1,2; then 3\n"
            "Output: [0,1,2,3] (other valid orders exist)"
        ),
        "trap": (
            "Building edge a->b instead of b->a reverses prerequisite direction. "
            "Returning partial order when a cycle leaves some indegrees stuck above zero."
        ),
    },
    "tp-gr-6": {
        "why": (
            "Cities connected by roads form undirected graph components; each province is one component. "
            "DFS from each unvisited city marks everyone reachable and counts one province. "
            "Union-find merges pairs on the fly with the same component count."
        ),
        "steps": [
            "seen = [False]*n; provinces = 0.",
            "For each city i not seen, run DFS marking all j where isConnected[i][j]==1.",
            "Increment provinces after each new DFS start.",
            "Union-find: for i<j if connected, union; answer = number of distinct roots.",
            "Matrix is symmetric; skip self-loops carefully.",
        ],
        "example": (
            "Input: isConnected=[[1,1,0],[1,1,0],[0,0,1]]\n"
            "DFS from 0 visits {0,1}; DFS from 2 visits {2}\n"
            "Output: 2 provinces"
        ),
        "trap": (
            "Double-counting by DFS-ing from every neighbor instead of only unvisited starts. "
            "Treating the matrix as directed and missing isConnected[j][i]."
        ),
    },
    "tp-gr-7": {
        "why": (
            "Computing distance from each 1 to every 0 separately is O(n^2 m^2). "
            "Multi-source BFS from all zeros at once spreads distance waves outward. "
            "The first time a 1 cell is reached is its shortest distance to any zero."
        ),
        "steps": [
            "Enqueue every cell with value 0 at distance 0; mark visited.",
            "BFS: for each neighbor not visited, set dist = dist+1 and enqueue.",
            "Fill a result matrix with distances (zeros stay 0).",
            "4-directional moves only.",
            "Do not restart BFS per cell.",
        ],
        "example": (
            "Input: mat=[[0,0,0],[0,1,0],[0,0,0]]\n"
            "Center 1 is surrounded; nearest 0 is one step away in four directions\n"
            "Output: [[0,0,0],[0,1,0],[0,0,0]] distances all 0 except center=1"
        ),
        "trap": (
            "Running BFS from each 1 instead of all zeros first. "
            "Not marking visited on enqueue so cells re-enter the queue with longer paths."
        ),
    },
    "tp-gr-8": {
        "why": (
            "Unweighted shortest path in a grid with 8 directions is BFS from the start cell. "
            "Each layer of BFS adds one step, so the first time you reach the bottom-right corner is optimal. "
            "Mark visited when enqueueing to avoid reprocessing."
        ),
        "steps": [
            "If start or end is blocked (grid[0][0]==1 or grid[n-1][n-1]==1), return -1.",
            "Queue ([0,0], length=1); mark [0,0] visited.",
            "Dequeue, if at [n-1,n-1] return length.",
            "Push all 8 unblocked unvisited neighbors with length+1.",
            "If queue empties, return -1.",
        ],
        "example": (
            "Input: grid=[[0,0,0],[1,1,0],[1,1,0]]\n"
            "BFS: (0,0)->(0,1)->(0,2)->(1,2)->(2,2) length 4 counting cells\n"
            "Output: 4"
        ),
        "trap": (
            "Using 4-direction moves when diagonals are allowed, or marking visited on dequeue "
            "so the same cell enters the queue many times with longer paths."
        ),
    },
}
