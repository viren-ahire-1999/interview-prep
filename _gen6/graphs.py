from util import topic, diagram, callout, code


def graphs() -> str:
    t1 = topic("gr-rep", "A graph is nodes plus edges",
               "graph adjacency list BFS DFS JavaScript", "Lesson", f'''
  <p>Prefer an <b>adjacency list</b>: <code>Map&lt;node, node[]&gt;</code> or <code>number[][]</code>. A matrix is O(n²) space — use it when the graph is dense or a grid already is a matrix.</p>
  {code("JavaScript", '''class Graph {
  constructor() { this.adj = new Map(); }
  addNode(u) { if (!this.adj.has(u)) this.adj.set(u, []); }
  addEdge(u, v, directed = false) {
    this.addNode(u); this.addNode(v);
    this.adj.get(u).push(v);
    if (!directed) this.adj.get(v).push(u);
  }
}

function bfs(adj, start) {
  const seen = new Set([start]);
  const q = [start];
  const order = [];
  while (q.length) {
    const u = q.shift();
    order.push(u);
    for (const v of adj.get(u) || []) {
      if (!seen.has(v)) { seen.add(v); q.push(v); }
    }
  }
  return order;
}

function dfs(adj, start, seen = new Set(), order = []) {
  seen.add(start);
  order.push(start);
  for (const v of adj.get(start) || []) {
    if (!seen.has(v)) dfs(adj, v, seen, order);
  }
  return order;
}
''')}
  {diagram("""BFS: queue, visit nearest first — shortest hops
DFS: stack/recursion — explore a path all the way""")}
  ''', "topics")

    t2 = topic("gr-grid", "A grid is a graph with four neighbors",
               "grid BFS islands JavaScript", "Lesson", f'''
  {code("JavaScript", '''function numIslands(grid) {
  const R = grid.length, C = grid[0]?.length || 0;
  const dirs = [[1,0],[-1,0],[0,1],[0,-1]];
  function sink(r, c) {
    if (r < 0 || c < 0 || r >= R || c >= C || grid[r][c] !== "1") return;
    grid[r][c] = "0";
    for (const [dr, dc] of dirs) sink(r + dr, c + dc);
  }
  let n = 0;
  for (let r = 0; r < R; r++)
    for (let c = 0; c < C; c++)
      if (grid[r][c] === "1") { n++; sink(r, c); }
  return n;
}
''')}
  <p>Visited: mutate the grid, or a <code>Set</code> of <code>`$&#123;r&#125;,$&#123;c&#125;`</code>. BFS if you need distance (shortest path in a maze).</p>
  ''', "topics")

    t3 = topic("gr-topo", "Directed graphs: cycles and order",
               "topological sort cycle directed graph", "Lesson", f'''
  {code("JavaScript", '''function canFinish(n, prereqs) {
  const adj = Array.from({ length: n }, () => []);
  const indeg = Array(n).fill(0);
  for (const [a, b] of prereqs) { adj[b].push(a); indeg[a]++; }
  const q = [];
  for (let i = 0; i < n; i++) if (indeg[i] === 0) q.push(i);
  let seen = 0;
  while (q.length) {
    const u = q.shift();
    seen++;
    for (const v of adj[u]) if (--indeg[v] === 0) q.push(v);
  }
  return seen === n;
}
''')}
  <p>If you cannot take all courses, there is a cycle. Product: module import order, CI pipeline stages, spreadsheet formula deps.</p>
  {callout("Unweighted shortest path = BFS. Weighted = Dijkstra (heap). Negative cycles = Bellman-Ford. Say the name; implement BFS in interviews unless they ask weights.")}
  ''', "topics")

    return f'''
<section class="block" id="graphs" data-search="Graphs BFS DFS topology JavaScript" data-stype="Section">
  <p class="kicker">Networks</p>
  <h2 class="section-title">Graphs</h2>
  {t1}{t2}{t3}
</section>
'''
