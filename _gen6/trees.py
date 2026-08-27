from util import topic, diagram, callout, code
from drills import recursion_gym, trees_gym, heaps_gym


def recursion() -> str:
    t = topic("rc-stack", "Recursion is the call stack doing a stack’s job",
              "recursion JavaScript call stack memo", "Lesson", f'''
  <p>Every call pushes a frame. A <b>base case</b> stops. Without it you get <code>RangeError: Maximum call stack size exceeded</code>.</p>
  {code("JavaScript", '''function fact(n) {
  if (n <= 1) return 1;
  return n * fact(n - 1);
}

function fibNaive(n) {
  if (n <= 1) return n;
  return fibNaive(n - 1) + fibNaive(n - 2); // O(2^n)
}

function fibMemo(n, memo = new Map()) {
  if (n <= 1) return n;
  if (memo.has(n)) return memo.get(n);
  const v = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
  memo.set(n, v);
  return v;
}

function flatten(arr) {
  const out = [];
  for (const x of arr) {
    if (Array.isArray(x)) out.push(...flatten(x));
    else out.push(x);
  }
  return out;
}
''')}
  {diagram("""fib(4)
  fib(3)        fib(2)
  fib(2) fib(1) fib(1) fib(0)
Memo: each n computed once → O(n)""")}
  <p>Think “smallest version of the same problem.” Trees and backtracking are recursion with a structure. DP is recursion with a cache, then a table.</p>
  ''', "topics")
    return f'''
<section class="block" id="recursion" data-search="Recursion JavaScript" data-stype="Section">
  <p class="kicker">The stack you cannot see</p>
  <h2 class="section-title">Recursion</h2>
  <p><a href="#gym-recursion">Jump to recursion practice (6 problems) →</a></p>
  {t}
  {recursion_gym()}
</section>
'''


def trees() -> str:
    t1 = topic("tr-walk", "A tree is a node with children — usually two",
               "binary tree traversal JavaScript BFS DFS", "Lesson", f'''
  {code("JavaScript", '''class TreeNode {
  constructor(val, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

function preorder(root, out = []) {
  if (!root) return out;
  out.push(root.val);
  preorder(root.left, out);
  preorder(root.right, out);
  return out;
}
function inorder(root, out = []) {
  if (!root) return out;
  inorder(root.left, out);
  out.push(root.val);
  inorder(root.right, out);
  return out;
}
function postorder(root, out = []) {
  if (!root) return out;
  postorder(root.left, out);
  postorder(root.right, out);
  out.push(root.val);
  return out;
}
function levelOrder(root) {
  if (!root) return [];
  const q = [root], res = [];
  while (q.length) {
    const n = q.length, level = [];
    for (let i = 0; i < n; i++) {
      const node = q.shift();
      level.push(node.val);
      if (node.left) q.push(node.left);
      if (node.right) q.push(node.right);
    }
    res.push(level);
  }
  return res;
}

function maxDepth(root) {
  if (!root) return 0;
  return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}
''')}
  {diagram("""     4
   /   \\
  2     6
 / \\   /
1   3 5
inorder BST: 1 2 3 4 5 6  (sorted)""")}
  <p><b>BFS</b> (queue, levels): shortest path in unweighted trees/grids, serialize by level. <b>DFS</b> (stack/recursion): path problems, height, “does a root-to-leaf sum exist.”</p>
  ''', "topics")

    t2 = topic("tr-bst", "BST: left &lt; node &lt; right",
               "BST insert search JavaScript", "Lesson", f'''
  {code("JavaScript", '''function bstSearch(root, t) {
  let n = root;
  while (n) {
    if (n.val === t) return n;
    n = t < n.val ? n.left : n.right;
  }
  return null;
}
function bstInsert(root, val) {
  if (!root) return new TreeNode(val);
  if (val < root.val) root.left = bstInsert(root.left, val);
  else root.right = bstInsert(root.right, val);
  return root;
}
''')}
  <p>Average search O(log n) if balanced; worst O(n) if you insert sorted data into a naive BST. Interviews often ignore self-balancing (AVL/red-black) unless asked — say “I’d use a balanced tree or a <code>Map</code>.”</p>
  ''', "topics")

    return f'''
<section class="block" id="trees" data-search="Binary trees BST JavaScript" data-stype="Section">
  <p class="kicker">Hierarchy</p>
  <h2 class="section-title">Trees and BST</h2>
  <p><a href="#gym-trees">Jump to tree practice (10 problems) →</a></p>
  {t1}{t2}
  {trees_gym()}
</section>
'''


def heaps() -> str:
    t = topic("hp-arr", "A heap is a complete tree stored in an array",
              "min heap JavaScript from scratch top-k", "Lesson", f'''
  <p>JS has no <code>PriorityQueue</code> in the language. You write a binary heap or sort (O(n log n)) when n is small.</p>
  <p>Index: parent <code>(i-1)>>1</code>, children <code>2i+1</code>, <code>2i+2</code>. Min-heap: parent ≤ children.</p>
  {code("JavaScript", '''class MinHeap {
  constructor() { this.a = []; }
  peek() { return this.a[0]; }
  push(x) {
    this.a.push(x);
    this._up(this.a.length - 1);
  }
  pop() {
    const a = this.a;
    if (a.length === 0) return undefined;
    const top = a[0];
    const last = a.pop();
    if (a.length) { a[0] = last; this._down(0); }
    return top;
  }
  _up(i) {
    const a = this.a;
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (a[p] <= a[i]) break;
      [a[p], a[i]] = [a[i], a[p]];
      i = p;
    }
  }
  _down(i) {
    const a = this.a, n = a.length;
    while (true) {
      let s = i, l = i * 2 + 1, r = l + 1;
      if (l < n && a[l] < a[s]) s = l;
      if (r < n && a[r] < a[s]) s = r;
      if (s === i) break;
      [a[s], a[i]] = [a[i], a[s]];
      i = s;
    }
  }
}

function topK(nums, k) {
  const h = new MinHeap();
  for (const x of nums) {
    h.push(x);
    if (h.a.length > k) h.pop();
  }
  return h.a.slice();
}
''')}
  <p>Push/pop O(log n). Build from n items O(n) if you heapify (optional expert). Product: schedulers, “top 10,” Dijkstra, merge k lists.</p>
  ''', "topics")
    return f'''
<section class="block" id="heaps" data-search="Heap priority queue JavaScript" data-stype="Section">
  <p class="kicker">Priority</p>
  <h2 class="section-title">Heaps</h2>
  <p><a href="#gym-heaps">Jump to heap practice (6 problems) →</a></p>
  {t}
  {heaps_gym()}
</section>
'''
