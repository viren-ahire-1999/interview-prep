from util import topic, diagram, callout, code


def linked() -> str:
    t1 = topic("ll-node", "A list is nodes and arrows",
               "linked list JavaScript from scratch", "Lesson", f'''
  <p>Each node holds a value and a reference to the next node. The list is the <code>head</code>. There is no index — walking is O(n). Insert/delete at a known node is O(1) pointer work.</p>
  {diagram("""head → [1|•] → [2|•] → [3|∅]
reverse: prev=null, curr=head
  next = curr.next; curr.next = prev; prev = curr; curr = next""")}
  {code("JavaScript", '''class ListNode {
  constructor(val, next = null) {
    this.val = val;
    this.next = next;
  }
}

class LinkedList {
  constructor() { this.head = null; }

  push(val) {
    const node = new ListNode(val);
    if (!this.head) { this.head = node; return; }
    let t = this.head;
    while (t.next) t = t.next;
    t.next = node;
  }

  reverse() {
    let prev = null, curr = this.head;
    while (curr) {
      const next = curr.next;
      curr.next = prev;
      prev = curr;
      curr = next;
    }
    this.head = prev;
  }
}

function detectCycle(head) {
  let slow = head, fast = head;
  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow === fast) return true;
  }
  return false;
}

function reverseList(head) {
  let prev = null, curr = head;
  while (curr) {
    const next = curr.next;
    curr.next = prev;
    prev = curr;
    curr = next;
  }
  return prev;
}
''')}
  {callout("<b>Dummy node.</b> <code>const dummy = new ListNode(0, head)</code> so you never special-case ‘new head.’ Essential for remove-nth-from-end and merge.")}
  {code("JavaScript", '''function mergeTwo(a, b) {
  const dummy = new ListNode(0);
  let t = dummy;
  while (a && b) {
    if (a.val <= b.val) { t.next = a; a = a.next; }
    else { t.next = b; b = b.next; }
    t = t.next;
  }
  t.next = a || b;
  return dummy.next;
}
''')}
  ''', "topics")

    t2 = topic("ll-drill", "Implement: middle and remove nth from end",
               "linked list middle remove nth drill", "Drill", f'''
  {code("JavaScript", '''function middleNode(head) {
  let slow = head, fast = head;
  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
  }
  return slow;
}

function removeNthFromEnd(head, n) {
  const dummy = new ListNode(0, head);
  let fast = dummy, slow = dummy;
  for (let i = 0; i < n + 1; i++) fast = fast.next;
  while (fast) { fast = fast.next; slow = slow.next; }
  slow.next = slow.next.next;
  return dummy.next;
}
''')}
  ''', "exercises")

    return f'''
<section class="block" id="lists" data-search="Linked lists JavaScript" data-stype="Section">
  <p class="kicker">Pointers</p>
  <h2 class="section-title">Linked lists</h2>
  {t1}{t2}
</section>
'''


def stacks() -> str:
    t1 = topic("sk-stack", "Stack = last in, first out",
               "stack JavaScript parentheses undo", "Lesson", f'''
  <p>Use an array: <code>push</code> / <code>pop</code> / <code>at(-1)</code>. Do not <code>shift</code>.</p>
  {code("JavaScript", '''function validParentheses(s) {
  const st = [];
  const pair = { ")": "(", "]": "[", "}": "{" };
  for (const ch of s) {
    if (ch === "(" || ch === "[" || ch === "{") st.push(ch);
    else {
      if (st.pop() !== pair[ch]) return false;
    }
  }
  return st.length === 0;
}

class MinStack {
  constructor() { this.st = []; this.mins = []; }
  push(x) {
    this.st.push(x);
    const m = this.mins.length ? this.mins[this.mins.length - 1] : Infinity;
    this.mins.push(Math.min(m, x));
  }
  pop() { this.st.pop(); this.mins.pop(); }
  top() { return this.st[this.st.length - 1]; }
  getMin() { return this.mins[this.mins.length - 1]; }
}
''')}
  <p>Product: undo stack, browser history (back), DFS, parsing, call stack (the real one).</p>
  ''', "topics")

    t2 = topic("sk-queue", "Queue = first in, first out",
               "queue JavaScript BFS circular", "Lesson", f'''
  <p><code>arr.shift()</code> is O(n). For interview BFS on small n it is acceptable if you say so. From scratch, keep a <code>head</code> index or a linked list.</p>
  {code("JavaScript", '''class Queue {
  constructor() { this.a = []; this.h = 0; }
  enqueue(x) { this.a.push(x); }
  dequeue() {
    if (this.h >= this.a.length) return undefined;
    const x = this.a[this.h++];
    if (this.h > 32 && this.h * 2 > this.a.length) {
      this.a = this.a.slice(this.h);
      this.h = 0;
    }
    return x;
  }
  get size() { return this.a.length - this.h; }
}
''')}
  <p>Product: job queues, BFS, event batching, “print next / serve next.”</p>
  {callout("Deque (two ends): JS has no deque. Use an array + two indices, or two stacks. For sliding-window maximum, a monotonic deque is the expert move (see Expert structures).")}
  ''', "topics")

    return f'''
<section class="block" id="stacks" data-search="Stacks queues JavaScript" data-stype="Section">
  <p class="kicker">Ends of a list</p>
  <h2 class="section-title">Stacks and queues</h2>
  {t1}{t2}
</section>
'''
