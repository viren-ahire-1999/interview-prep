P3 = [
{
  "id": "max-depth", "name": "Maximum Depth of Binary Tree", "diff": "easy", "pattern": "tree-recursion", "topic": "trees",
  "why": "The tree recursion base case. Height is the building block for diameter and balance.",
  "stmt": "Return the number of nodes on the longest root-to-leaf path (LeetCode-style depth).",
  "exin": "a tree of height 3", "exout": "3",
  "cons": "n up to 10^4.",
  "hints": "Empty → 0. Else 1 + max(left, right).",
  "brute": "BFS levels and count. Also O(n).",
  "opt": "DFS recursion.",
  "steps": "Post-order combine. Iterative stack if they fear stack overflow.",
  "cx": "O(n) time, O(h) space.",
  "mistakes": "Returning 1 for null. Confusing edges vs nodes in the definition — ask.",
  "edges": "Empty. Single node. Skewed.",
  "follow": "Min depth (careful: a node with one child is not a leaf path).",
  "talk": "I will confirm depth definition (nodes vs edges) in one sentence.",
  "sol": """function maxDepth(root: TreeNode | null): number {
  if (!root) return 0;
  return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}"""
},
{
  "id": "invert-tree", "name": "Invert Binary Tree", "diff": "easy", "pattern": "tree-recursion", "topic": "trees",
  "why": "Swap children. Tests whether you recurse after or before the swap (both work if consistent).",
  "stmt": "Mirror the tree: swap every left/right pair.",
  "exin": "4 with left 2 and right 7 …", "exout": "mirrored",
  "cons": "n up to 100 in the meme version; still write O(n).",
  "hints": "Swap, then invert children (or invert then swap).",
  "brute": "BFS and swap at each node.",
  "opt": "Either DFS or BFS O(n).",
  "steps": "Null returns null. Swap references, recurse.",
  "cx": "O(n) time, O(h) space.",
  "mistakes": "Swapping values instead of child pointers. Recursing on old children after losing them.",
  "edges": "Empty. One child.",
  "follow": "Check if two trees are mirrors (symmetric tree).",
  "talk": "Cute problem; I still state complexity. Senior ≠ dismissive.",
  "sol": """function invertTree(root: TreeNode | null): TreeNode | null {
  if (!root) return null;
  const tmp = root.left;
  root.left = invertTree(root.right);
  root.right = invertTree(tmp);
  return root;
}"""
},
{
  "id": "diameter", "name": "Diameter of Binary Tree", "diff": "easy", "pattern": "tree-recursion", "topic": "trees",
  "why": "Answer is not the same as the return value. Height plus a side-channel max.",
  "stmt": "Length of the longest path between any two nodes, in edges.",
  "exin": "a chain or a root with two deep children", "exout": "leftHeight + rightHeight at the best node",
  "cons": "n up to 10^4.",
  "hints": "At each node, path through it is Lheight+Rheight. Diameter is the max of those. Return height to parent.",
  "brute": "For every node, compute depths of all leaves — O(n²).",
  "opt": "One DFS O(n).",
  "steps": "height(null)=0. height(node)=1+max(hL,hR). best=max(best,hL+hR).",
  "cx": "O(n) time, O(h) space.",
  "mistakes": "Returning the height as the answer. Counting nodes not edges (off-by-one on definition).",
  "edges": "Single node (0). Linear chain.",
  "follow": "Diameter of an N-ary tree.",
  "talk": "I will say 'I return height, I track diameter separately' before coding.",
  "sol": """function diameterOfBinaryTree(root: TreeNode | null): number {
  let best = 0;
  const height = (n: TreeNode | null): number => {
    if (!n) return 0;
    const L = height(n.left), R = height(n.right);
    best = Math.max(best, L + R);
    return 1 + Math.max(L, R);
  };
  height(root);
  return best;
}"""
},
{
  "id": "balanced", "name": "Balanced Binary Tree", "diff": "easy", "pattern": "tree-recursion", "topic": "trees",
  "why": "Height-balanced: |hL−hR|≤1 everywhere, not just at the root.",
  "stmt": "Return whether the tree is height-balanced.",
  "exin": "a complete small tree vs a 3-node skewed arm", "exout": "true / false",
  "cons": "n up to 5000.",
  "hints": "DFS that returns height or -1 if already unbalanced.",
  "brute": "Compute height independently at every node. O(n²).",
  "opt": "Single pass, abort early with a sentinel.",
  "steps": "If either child is -1 or |L-R|>1 return -1; else 1+max(L,R).",
  "cx": "O(n).",
  "mistakes": "Only checking the root. Computing height twice per node.",
  "edges": "Empty (true). Two nodes.",
  "follow": "Balance a BST (different problem).",
  "talk": "I will not write two separate functions that each walk the tree.",
  "sol": """function isBalanced(root: TreeNode | null): boolean {
  const go = (n: TreeNode | null): number => {
    if (!n) return 0;
    const L = go(n.left), R = go(n.right);
    if (L < 0 || R < 0 || Math.abs(L - R) > 1) return -1;
    return 1 + Math.max(L, R);
  };
  return go(root) >= 0;
}"""
},
{
  "id": "level-order", "name": "Binary Tree Level Order Traversal", "diff": "medium", "pattern": "bfs", "topic": "trees",
  "why": "BFS template. Capture level size.",
  "stmt": "Return values grouped by level, top to bottom, left to right.",
  "exin": "standard 3-level tree", "exout": "[[3],[9,20],[15,7]]",
  "cons": "n up to 2000.",
  "hints": "Queue. For each level, take q.length snapshots.",
  "brute": "DFS with a depth parameter, push into out[depth]. Also correct.",
  "opt": "BFS is the natural fit.",
  "steps": "Use a head index, not shift().",
  "cx": "O(n) time and space.",
  "mistakes": "Not freezing the level size. shift() in a huge tree.",
  "edges": "Empty. Single node. Skewed (one node per level).",
  "follow": "Zigzag level order. Average per level.",
  "talk": "I will mention the DFS-with-depth alternative if they dislike queues.",
  "sol": """function levelOrder(root: TreeNode | null): number[][] {
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
}"""
},
{
  "id": "validate-bst", "name": "Validate Binary Search Tree", "diff": "medium", "pattern": "tree-recursion", "topic": "trees",
  "why": "Bounds, not local comparisons. A classic trap.",
  "stmt": "Is the tree a valid BST (strictly increasing inorder; left < node < right for the whole subtree)?",
  "exin": "valid vs [5,1,4,null,null,3,6] invalid", "exout": "true / false",
  "cons": "Values can be extreme — use ±Infinity, not min/max of 32-bit if they use those values.",
  "hints": "Pass (lo, hi). Node must be > lo and < hi. Left gets (lo, node.val), right (node.val, hi).",
  "brute": "Inorder into an array, check sorted. O(n) space.",
  "opt": "DFS bounds O(h) extra, or inorder with a running prev.",
  "steps": "Local left.val < node.val is insufficient. The failing grandchild is why bounds exist.",
  "cx": "O(n) time, O(h) space.",
  "mistakes": "Only checking children. Using >= when duplicates are forbidden.",
  "edges": "Single node. Duplicates (usually invalid). INT_MIN/MAX values.",
  "follow": "Recover swapped BST nodes.",
  "talk": "I will draw the counterexample (5-4-3 on the right) if they ask why bounds.",
  "sol": """function isValidBST(root: TreeNode | null, lo = -Infinity, hi = Infinity): boolean {
  if (!root) return true;
  if (root.val <= lo || root.val >= hi) return false;
  return isValidBST(root.left, lo, root.val) && isValidBST(root.right, root.val, hi);
}"""
},
{
  "id": "lca-bst", "name": "Lowest Common Ancestor of a BST", "diff": "medium", "pattern": "tree-recursion", "topic": "trees",
  "why": "Use the BST walk: if both targets are left, go left; both right, go right; else this node is the split.",
  "stmt": "BST, two nodes p and q present. Return their LCA.",
  "exin": "root=6, p=2, q=8 → 6; p=2, q=4 → 2", "exout": "the split node",
  "cons": "Unique values; p and q exist.",
  "hints": "Iterative walk is enough. No extra storage.",
  "brute": "Parent pointers + ancestor sets. Works on a general tree.",
  "opt": "O(h) BST walk.",
  "steps": "While node: if p and q < node, go left; if both >, go right; else return node.",
  "cx": "O(h) time, O(1) iterative.",
  "mistakes": "Using a general-tree LCA on a BST without using order. Forgetting a node can be an ancestor of itself.",
  "edges": "p is ancestor of q. p and q are the two children of root.",
  "follow": "LCA in a binary tree (not BST) — recurse and combine.",
  "talk": "I will say 'this is O(h) because of the search property' so they know I did not copy the general algorithm.",
  "sol": """function lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode): TreeNode {
  let n: TreeNode | null = root;
  while (n) {
    if (p.val < n.val && q.val < n.val) n = n.left;
    else if (p.val > n.val && q.val > n.val) n = n.right;
    else return n;
  }
  throw new Error("missing");
}"""
},
{
  "id": "kth-bst", "name": "Kth Smallest Element in a BST", "diff": "medium", "pattern": "tree-recursion", "topic": "trees",
  "why": "Inorder of a BST is sorted. Count as you go; do not dump the whole array unless n is tiny.",
  "stmt": "Return the kth smallest value (1-indexed) in a BST.",
  "exin": "k=3 in a 5-node BST", "exout": "the 3rd inorder value",
  "cons": "k is valid.",
  "hints": "Inorder DFS, decrement k, return when k hits 0. Or Morris if they want O(1) extra.",
  "brute": "Inorder array, index k-1. O(n) space.",
  "opt": "Early-stop inorder O(h+k).",
  "steps": "Go left, visit, k--. If k===0 record val. Go right.",
  "cx": "O(h+k) time typical, O(h) space.",
  "mistakes": "0-index vs 1-index. Reverse inorder for kth largest without adjusting k.",
  "edges": "k=1 (minimum). k=n (maximum).",
  "follow": "If the BST is mutated often, store subtree sizes for O(h) kth.",
  "talk": "I will mention subtree sizes as the production optimization if this were a repeated query.",
  "sol": """function kthSmallest(root: TreeNode | null, k: number): number {
  let ans = 0;
  const go = (n: TreeNode | null): boolean => {
    if (!n) return false;
    if (go(n.left)) return true;
    if (--k === 0) { ans = n.val; return true; }
    return go(n.right);
  };
  go(root);
  return ans;
}"""
},
{
  "id": "right-side", "name": "Binary Tree Right Side View", "diff": "medium", "pattern": "bfs", "topic": "trees",
  "why": "Last node per BFS level, or DFS root-right-left recording the first visit at each depth.",
  "stmt": "Values you would see standing on the right side, top to bottom.",
  "exin": "a standard tree", "exout": "the right spine, plus deeper left nodes that poke out",
  "cons": "n up to 100.",
  "hints": "BFS: last in the level. DFS: visit right first, push when depth===out.length.",
  "brute": "Full level order, map last of each row.",
  "opt": "Same complexity; DFS uses less explicit queue code.",
  "steps": "Either is fine. Do not confuse with 'right spine only'.",
  "cx": "O(n).",
  "mistakes": "Only following right pointers (misses a deeper left child).",
  "edges": "Left-only tree (you still see every node). Empty.",
  "follow": "Left side view.",
  "talk": "I will mention the counterexample of a long left subtree under a short right child.",
  "sol": """function rightSideView(root: TreeNode | null): number[] {
  const out: number[] = [];
  const go = (n: TreeNode | null, d: number) => {
    if (!n) return;
    if (d === out.length) out.push(n.val);
    go(n.right, d + 1);
    go(n.left, d + 1);
  };
  go(root, 0);
  return out;
}"""
},
{
  "id": "construct-tree", "name": "Construct Binary Tree from Preorder and Inorder", "diff": "medium", "pattern": "tree-recursion", "topic": "trees",
  "why": "Preorder gives the root; inorder splits left/right sizes. Index map avoids O(n²) scans.",
  "stmt": "Unique values. Rebuild the tree from preorder and inorder arrays.",
  "exin": "preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]", "exout": "the standard 3-tree",
  "cons": "n up to 3000; unique vals.",
  "hints": "root = preorder[preL]. Find it in inorder; left size = idx-inL. Recurse ranges.",
  "brute": "indexOf on every recurse O(n²).",
  "opt": "Map value→inorder index, O(n).",
  "steps": "Consume preorder left-to-right or pass a moving preIndex.",
  "cx": "O(n) time and space.",
  "mistakes": "Wrong slice sizes. Assuming inorder is sorted (only true for BST).",
  "edges": "Single node. Skewed left. Skewed right.",
  "follow": "Postorder+inorder. Preorder+postorder (need uniqueness / extra rules).",
  "talk": "I will build the index map first and say why.",
  "sol": """function buildTree(preorder: number[], inorder: number[]): TreeNode | null {
  const idx = new Map(inorder.map((v, i) => [v, i]));
  let p = 0;
  const go = (L: number, R: number): TreeNode | null => {
    if (L > R) return null;
    const val = preorder[p++];
    const m = idx.get(val)!;
    const node = new TreeNode(val);
    node.left = go(L, m - 1);
    node.right = go(m + 1, R);
    return node;
  };
  return go(0, inorder.length - 1);
}"""
},
{
  "id": "kth-largest", "name": "Kth Largest Element in an Array", "diff": "medium", "pattern": "heap-topk", "topic": "heap",
  "why": "Sort vs heap vs Quickselect. Be honest about what you will code in 25 minutes.",
  "stmt": "Return the kth largest (not distinct-only unless specified).",
  "exin": "nums = [3,2,1,5,6,4], k = 2", "exout": "5",
  "cons": "n up to 10^5.",
  "hints": "Sort desc and take [k-1]. Or min-heap of size k. Or Quickselect average O(n).",
  "brute": "Sort O(n log n).",
  "opt": "Heap O(n log k). Quickselect average O(n), worst O(n²).",
  "steps": "In JS interviews, sort is acceptable if you discuss heap/Quickselect.",
  "cx": "Sort O(n log n). Heap O(n log k) extra O(k).",
  "mistakes": "kth largest vs kth smallest mixup. Unique-only when not asked.",
  "edges": "k=1. k=n. Duplicates.",
  "follow": "Stream of numbers (heap stays).",
  "talk": "I will implement sort, then say I know Quickselect if they want linear expected time.",
  "sol": """function findKthLargest(nums: number[], k: number): number {
  return nums.slice().sort((a, b) => b - a)[k - 1];
}"""
},
{
  "id": "k-closest", "name": "K Closest Points to Origin", "diff": "medium", "pattern": "heap-topk", "topic": "heap",
  "why": "Distance as a key. Avoid sqrt if you only compare.",
  "stmt": "k points closest to (0,0). Order among them can be anything.",
  "exin": "points = [[1,3],[-2,2]], k = 1", "exout": "[[-2,2]]",
  "cons": "n up to 10^4.",
  "hints": "Compare x²+y². Sort or max-heap of size k.",
  "brute": "Sort all by dist. O(n log n).",
  "opt": "Heap O(n log k) or Quickselect on distance.",
  "steps": "Do not take square roots. Ties: either point is fine unless specified.",
  "cx": "O(n log n) sort is fine for n=10^4.",
  "mistakes": "Using sqrt and floating error. k vs n mixup.",
  "edges": "k=n. Points on a circle.",
  "follow": "Closest to an arbitrary point (same). Dynamic points.",
  "talk": "I will say 'I compare squared Euclidean distance' explicitly.",
  "sol": """function kClosest(points: number[][], k: number): number[][] {
  return points
    .slice()
    .sort((a, b) => a[0] ** 2 + a[1] ** 2 - (b[0] ** 2 + b[1] ** 2))
    .slice(0, k);
}"""
},
{
  "id": "median-stream", "name": "Find Median from Data Stream", "diff": "hard", "pattern": "heap-topk", "topic": "heap",
  "why": "Two-heap invariant: max-heap lo | min-heap hi, sizes differ by at most 1.",
  "stmt": "Online class: addNum(x), findMedian() (average of two middles if even count).",
  "exin": "1,2 → median 1.5; add 3 → median 2", "exout": "as above",
  "cons": "Calls up to 5·10^4.",
  "hints": "lo holds the smaller half (max on top). hi the larger half (min on top). Rebalance sizes.",
  "brute": "Keep a sorted array, insert O(n).",
  "opt": "Two heaps O(log n) add, O(1) median. In JS, you may implement two heaps or sort on each query if n is small — say so.",
  "steps": "Push to lo; move lo.max to hi; if hi.size > lo.size move hi.min to lo. Odd: lo.max. Even: avg of tops.",
  "cx": "O(log n) add with heaps.",
  "mistakes": "Unbalanced heaps. Integer vs float average.",
  "edges": "One element. All equal. Decreasing stream.",
  "follow": "Lazy deletions for sliding-window median (harder).",
  "talk": "If I do not have a heap typed, I will write a small binary heap or honestly sort for a first version and upgrade.",
  "sol": """class MedianFinder {
  data: number[] = [];
  addNum(x: number) {
    const a = this.data;
    let lo = 0, hi = a.length;
    while (lo < hi) {
      const m = (lo + hi) >> 1;
      if (a[m] <= x) lo = m + 1; else hi = m;
    }
    a.splice(lo, 0, x);
  }
  findMedian(): number {
    const a = this.data, n = a.length;
    return n % 2 ? a[n >> 1] : (a[n / 2 - 1] + a[n / 2]) / 2;
  }
}
// Interview note: insertion is O(n). Upgrade to two heaps for O(log n)."""
},
{
  "id": "islands", "name": "Number of Islands", "diff": "medium", "pattern": "dfs", "topic": "graphs",
  "why": "Flood fill. The grid DFS/BFS you must write from muscle memory.",
  "stmt": "2D grid of '1' land and '0' water. Count islands (4-connected).",
  "exin": "a few blocks of 1s", "exout": "the component count",
  "cons": "m,n up to 300.",
  "hints": "For each unvisited land, increment and sink the component.",
  "brute": "Union-find also works; more code.",
  "opt": "DFS or BFS flood fill. O(mn).",
  "steps": "Mark visited by setting '0' or a visited matrix. Four directions. Bounds first.",
  "cx": "O(mn) time and O(mn) stack worst case.",
  "mistakes": "8-connected by accident. Not marking before recurse. Recursion depth on a snake island — mention BFS.",
  "edges": "All water. One giant island. 1×1.",
  "follow": "Max area of island. Number of distinct islands (normalize shapes).",
  "talk": "I will ask 4 vs 8 connected. I will mention mutating the grid.",
  "sol": """function numIslands(grid: string[][]): number {
  const R = grid.length, C = grid[0]?.length ?? 0;
  const dfs = (r: number, c: number) => {
    if (r < 0 || c < 0 || r >= R || c >= C || grid[r][c] !== "1") return;
    grid[r][c] = "0";
    dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1);
  };
  let n = 0;
  for (let r = 0; r < R; r++)
    for (let c = 0; c < C; c++)
      if (grid[r][c] === "1") { n++; dfs(r, c); }
  return n;
}"""
},
{
  "id": "clone-graph", "name": "Clone Graph", "diff": "medium", "pattern": "bfs", "topic": "graphs",
  "why": "Map original → clone. The graph analog of copying a pointer structure.",
  "stmt": "Deep-copy an undirected connected graph of nodes with val and neighbors.",
  "exin": "a 4-cycle", "exout": "a new 4-cycle with no shared node objects",
  "cons": "n up to 100; vals unique 1..n typically.",
  "hints": "HashMap. Create the clone when you first see a node, then wire neighbors.",
  "brute": "Cannot copy without a map — you would loop forever.",
  "opt": "DFS or BFS + Map. O(V+E).",
  "steps": "If map has node, return clone. Else create, store, then clone.neighbors = neighbors.map(dfs).",
  "cx": "O(V+E) time and space.",
  "mistakes": "Forgetting the map (infinite recursion). Shallow copy of the neighbor array.",
  "edges": "Null. Single node. Complete graph.",
  "follow": "Clone with random pointers (list). Serialize/deserialize.",
  "talk": "I will say 'the map is both memo and visited'.",
  "sol": """function cloneGraph(node: Node | null): Node | null {
  if (!node) return null;
  const map = new Map<Node, Node>();
  const dfs = (n: Node): Node => {
    const cached = map.get(n);
    if (cached) return cached;
    const copy = new Node(n.val);
    map.set(n, copy);
    copy.neighbors = n.neighbors.map(dfs);
    return copy;
  };
  return dfs(node);
}"""
},
{
  "id": "oranges", "name": "Rotting Oranges", "diff": "medium", "pattern": "bfs", "topic": "graphs",
  "why": "Multi-source BFS. Minutes = levels.",
  "stmt": "0 empty, 1 fresh, 2 rotten. Each minute rotten infects 4-neighbors. Minutes until no fresh, or -1.",
  "exin": "[[2,1,1],[1,1,0],[0,1,1]]", "exout": "4",
  "cons": "grid up to 10×10 or 100×100 depending on source; write O(mn).",
  "hints": "Enqueue all rotten first. Count fresh. BFS by level.",
  "brute": "Simulate naive scans each minute O(m²n²).",
  "opt": "Multi-source BFS O(mn).",
  "steps": "If fresh hits 0, return minutes. If queue ends and fresh remains, -1. Empty fresh at start → 0.",
  "cx": "O(mn).",
  "mistakes": "Single-source from one rotten. Not using level size. Returning minutes when fresh already 0 after a phantom increment.",
  "edges": "No fresh. Impossible pocket. All rotten.",
  "follow": "Walls in the grid.",
  "talk": "I will initialize the queue with every 2 before the loop — that is the whole trick.",
  "sol": """function orangesRotting(grid: number[][]): number {
  const R = grid.length, C = grid[0].length, q: [number, number][] = [];
  let fresh = 0, mins = 0, h = 0;
  for (let r = 0; r < R; r++)
    for (let c = 0; c < C; c++) {
      if (grid[r][c] === 2) q.push([r, c]);
      if (grid[r][c] === 1) fresh++;
    }
  const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]];
  while (h < q.length && fresh) {
    const size = q.length - h;
    for (let i = 0; i < size; i++) {
      const [r, c] = q[h++];
      for (const [dr, dc] of dirs) {
        const nr = r + dr, nc = c + dc;
        if (grid[nr]?.[nc] === 1) {
          grid[nr][nc] = 2; fresh--; q.push([nr, nc]);
        }
      }
    }
    mins++;
  }
  return fresh ? -1 : mins;
}"""
},
{
  "id": "course-sked", "name": "Course Schedule", "diff": "medium", "pattern": "dfs", "topic": "graphs",
  "why": "Cycle detection in a directed graph. Prerequisite edges.",
  "stmt": "numCourses, edges [a,b] meaning b before a. Can you finish all?",
  "exin": "2, [[1,0]] → true; 2, [[1,0],[0,1]] → false", "exout": "true/false",
  "cons": "n up to 2000, edges up to 5000.",
  "hints": "Build adj from b→a. DFS 3-color or Kahn indegrees.",
  "brute": "Try permutations — n! no.",
  "opt": "DFS cycle or BFS Kahn. O(V+E).",
  "steps": "Gray node revisited → cycle. Kahn: queue zeros, count visited.",
  "cx": "O(V+E).",
  "mistakes": "Edge direction flipped. 2-color only (misses directed cycles).",
  "edges": "No edges. Self-loop. Disconnected.",
  "follow": "Return a valid order (Course Schedule II).",
  "talk": "I will confirm edge meaning ('b is a prereq of a') before building the graph.",
  "sol": """function canFinish(n: number, prereq: number[][]): boolean {
  const g: number[][] = Array.from({ length: n }, () => []);
  for (const [a, b] of prereq) g[b].push(a);
  const st = Array(n).fill(0);
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
}"""
},
{
  "id": "pacific", "name": "Pacific Atlantic Water Flow", "diff": "medium", "pattern": "dfs", "topic": "graphs",
  "why": "Reverse thinking: flood inland from oceans, not down to oceans from every cell.",
  "stmt": "Heights grid. Water flows to equal-or-lower neighbors. Which cells can reach both Pacific (top/left) and Atlantic (bottom/right)?",
  "exin": "the standard 5×5 example", "exout": "list of [r,c]",
  "cons": "m,n up to 200.",
  "hints": "DFS/BFS from ocean borders uphill (next >= current). Intersect the two reachable sets.",
  "brute": "From every cell DFS to both oceans. O(mn(m+n)) painful.",
  "opt": "Two multi-source searches O(mn).",
  "steps": "Mark pacific-reachable and atlantic-reachable. Cells in both are answers.",
  "cx": "O(mn).",
  "mistakes": "Flowing downhill from oceans. Off-by-one on borders. 4 vs 8.",
  "edges": "1×1 (both). Strictly decreasing inland.",
  "follow": "Count cells instead of listing.",
  "talk": "I will say 'I reverse the edges of the flow relation' — that is the senior sentence.",
  "sol": """function pacificAtlantic(h: number[][]): number[][] {
  const R = h.length, C = h[0].length;
  const pac = Array.from({ length: R }, () => Array(C).fill(false));
  const atl = Array.from({ length: R }, () => Array(C).fill(false));
  const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]];
  const dfs = (r: number, c: number, seen: boolean[][]) => {
    seen[r][c] = true;
    for (const [dr, dc] of dirs) {
      const nr = r + dr, nc = c + dc;
      if (nr < 0 || nc < 0 || nr >= R || nc >= C || seen[nr][nc]) continue;
      if (h[nr][nc] < h[r][c]) continue;
      dfs(nr, nc, seen);
    }
  };
  for (let c = 0; c < C; c++) { dfs(0, c, pac); dfs(R - 1, c, atl); }
  for (let r = 0; r < R; r++) { dfs(r, 0, pac); dfs(r, C - 1, atl); }
  const out: number[][] = [];
  for (let r = 0; r < R; r++)
    for (let c = 0; c < C; c++)
      if (pac[r][c] && atl[r][c]) out.push([r, c]);
  return out;
}"""
},
]
