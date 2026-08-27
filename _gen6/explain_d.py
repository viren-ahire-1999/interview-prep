BANK = {
    1: {
        "why": (
            "Checking every pair takes quadratic time because you re-scan the array for each element. "
            "A hash map remembers what you have already seen, so each lookup is constant time. "
            "One left-to-right pass is enough because the partner for nums[i] must appear earlier or you store i for later."
        ),
        "steps": [
            "Create an empty map from value to index.",
            "Walk i from 0 to n-1.",
            "Compute need = target - nums[i].",
            "If need is already in the map, return [map[need], i].",
            "Otherwise store nums[i] -> i and continue.",
            "Return empty if no pair exists.",
        ],
        "example": (
            "nums = [2, 7, 11, 15], target = 9\n"
            "i=0: need=7, map={}, store 2->0\n"
            "i=1: need=2, map has 2 at 0 -> return [0, 1]"
        ),
        "trap": "Do not use the same index twice; store the current value only after checking for its partner.",
    },
    2: {
        "why": (
            "Sorting first works but costs O(n log n) and still needs a linear scan for neighbors. "
            "A set gives immediate duplicate detection: if you have seen a value, you are done. "
            "One pass with O(1) average inserts and lookups beats the sort-and-scan approach."
        ),
        "steps": [
            "Initialize an empty set seen.",
            "For each value x in nums:",
            "If x is in seen, return True.",
            "Add x to seen.",
            "If the loop finishes, return False.",
        ],
        "example": (
            "nums = [1, 2, 3, 1]\n"
            "seen={} -> add 1\n"
            "seen={1} -> add 2\n"
            "seen={1,2} -> add 3\n"
            "seen={1,2,3} -> 1 in seen -> True"
        ),
        "trap": "Returning True on the second occurrence is correct; do not require three copies of a value.",
    },
    3: {
        "why": (
            "Sorting both strings and comparing works but mutates order information you do not need. "
            "Letter counts capture the multiset directly: anagrams have identical counts. "
            "A fixed-size array of 26 counters is O(1) space for lowercase English letters."
        ),
        "steps": [
            "If lengths differ, return False.",
            "Build a frequency table for s (increment per char).",
            "Walk t and decrement the same table.",
            "If any count goes negative, return False.",
            "Return True if all counts are zero.",
        ],
        "example": (
            "s = \"anagram\", t = \"nagaram\"\n"
            "count a:2 n:1 g:1 r:1 m:1 ... after s\n"
            "decrement with t -> all zeros -> True"
        ),
        "trap": "Forgetting the length check lets unequal-length strings pass if you only compare counts loosely.",
    },
    4: {
        "why": (
            "Building a cleaned string uses extra memory and still needs a second pass to compare. "
            "Two pointers skip junk in place while comparing only valid characters. "
            "You touch each character at most once, so time and extra space stay linear and constant respectively."
        ),
        "steps": [
            "Set left = 0, right = len(s) - 1.",
            "Advance left until alphanumeric (or left >= right).",
            "Retreat right until alphanumeric.",
            "Compare lower(left) vs lower(right); stop on mismatch.",
            "Move both inward and repeat.",
            "Return True if pointers cross.",
        ],
        "example": (
            "s = \"A man, a plan, a canal: Panama\"\n"
            "compare A vs a (ok), m vs m (ok), ...\n"
            "pointers meet -> True"
        ),
        "trap": "Compare case-insensitively but do not forget to skip non-alphanumeric characters on both sides.",
    },
    5: {
        "why": (
            "Trying every buy/sell pair is O(n^2) and wasteful because the best sell for a fixed buy is always the max price after it. "
            "Instead, track the cheapest price seen so far and the best profit achievable by selling today. "
            "One scan updates both running values in constant time per day."
        ),
        "steps": [
            "Set minPrice = infinity, maxProfit = 0.",
            "For each price p in prices:",
            "Update minPrice = min(minPrice, p).",
            "Update maxProfit = max(maxProfit, p - minPrice).",
            "Return maxProfit.",
        ],
        "example": (
            "prices = [7, 1, 5, 3, 6, 4]\n"
            "p=7: min=7 profit=0\n"
            "p=1: min=1 profit=0\n"
            "p=5: min=1 profit=4\n"
            "p=6: min=1 profit=5 -> answer 5"
        ),
        "trap": "You must buy before you sell; updating minPrice before computing profit enforces that order.",
    },
    6: {
        "why": (
            "Enumerating all subarrays is cubic. Kadane's insight is that an optimal subarray either extends the previous one or starts fresh at the current element. "
            "Tracking the best sum ending here and the global best collapses the problem to one pass. "
            "No prefix array is needed."
        ),
        "steps": [
            "Set bestHere = nums[0], bestOverall = nums[0].",
            "For i from 1 to n-1:",
            "bestHere = max(nums[i], bestHere + nums[i]).",
            "bestOverall = max(bestOverall, bestHere).",
            "Return bestOverall.",
        ],
        "example": (
            "nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]\n"
            "at 4: bestHere=4, bestOverall=4\n"
            "extend: 4,-1,2,1 -> bestHere=6, bestOverall=6"
        ),
        "trap": "Initializing bestOverall to 0 breaks when all numbers are negative; seed with nums[0].",
    },
    7: {
        "why": (
            "Division by the current element is forbidden and unstable with zeros. "
            "The product at i equals (product of everything left) times (product of everything right). "
            "Two sweeps—prefix then suffix—fill the answer without extra arrays beyond the output."
        ),
        "steps": [
            "Initialize out[i] = 1 for all i.",
            "Left sweep: carry prefix=1, out[i] *= prefix, prefix *= nums[i].",
            "Right sweep: carry suffix=1, out[i] *= suffix, suffix *= nums[i].",
            "Return out.",
        ],
        "example": (
            "nums = [1, 2, 3, 4]\n"
            "left:  out = [1, 1, 2, 6]\n"
            "right: out = [24, 12, 4, 6] (suffix multipliers applied)"
        ),
        "trap": "Do the suffix pass on the same out array after the prefix pass; using two separate prefix arrays wastes space.",
    },
    8: {
        "why": (
            "Checking every substring is O(n^2) with a set per window. "
            "A sliding window expands until a repeat appears, then shrinks from the left. "
            "Storing the last index of each character lets you jump the left boundary instead of shrinking one step at a time."
        ),
        "steps": [
            "Set left = 0, best = 0, last = {}.",
            "For right from 0 to n-1:",
            "If s[right] seen and last[s[right]] >= left, move left to last[s[right]] + 1.",
            "Record last[s[right]] = right.",
            "best = max(best, right - left + 1).",
            "Return best.",
        ],
        "example": (
            "s = \"abcabcbb\"\n"
            "window \"abc\" len=3, see b again -> left jumps past first b\n"
            "best reaches 3 (\"abc\")"
        ),
        "trap": "Only jump left when the previous occurrence is inside the current window, not anywhere in the string.",
    },
    9: {
        "why": (
            "A triple nested loop finds triplets but emits many duplicates. "
            "Sorting lets you fix one value and use two pointers on the remainder in linear time. "
            "Skipping equal neighbors after a match removes duplicate triplets without a separate set."
        ),
        "steps": [
            "Sort nums.",
            "For i from 0 to n-3:",
            "Skip duplicate nums[i].",
            "Set lo = i+1, hi = n-1.",
            "While lo < hi: if sum==0 record and skip dupes; elif sum<0 lo++; else hi--.",
            "Return collected triplets.",
        ],
        "example": (
            "nums = [-1, 0, 1, 2, -1, -4] -> sorted [-4,-1,-1,0,1,2]\n"
            "i=1 (-1): lo=2 hi=5 -> (-1,0,1) and (-1,-1,2)"
        ),
        "trap": "Skip duplicate i values before the two-pointer phase, otherwise you emit the same triplet multiple times.",
    },
    10: {
        "why": (
            "Evaluating every pair is quadratic. "
            "The two-pointer method starts wide and moves inward, always discarding the side that cannot improve area. "
            "Area is limited by the shorter height, so advancing the taller line cannot increase water held."
        ),
        "steps": [
            "Set lo = 0, hi = n-1, best = 0.",
            "While lo < hi:",
            "Compute area = min(h[lo], h[hi]) * (hi - lo).",
            "Update best.",
            "Move the pointer at the shorter height inward.",
            "Return best.",
        ],
        "example": (
            "height = [1,8,6,2,5,4,8,3,7]\n"
            "lo=0 hi=8: area=min(1,7)*8=8, move lo\n"
            "eventually best = 49"
        ),
        "trap": "Move the shorter side, not always the left pointer; both sides must be considered each step.",
    },
    11: {
        "why": (
            "Counting open and close brackets globally fails on interleaved types like \"([)]\". "
            "A stack mirrors the nesting rule: the next closer must match the most recent opener. "
            "Linear time with one structure is enough."
        ),
        "steps": [
            "Push opening brackets onto a stack.",
            "On a closing bracket, if stack empty return False.",
            "Pop and verify pairs match.",
            "After scanning, return stack empty.",
        ],
        "example": (
            "s = \"({[]})\"\n"
            "push ( { [\n"
            "pop ] { ) -> stack empty -> True"
        ),
        "trap": "An unmatched opener left on the stack means False even if every closer had a partner on the way.",
    },
    12: {
        "why": (
            "Scanning the whole stack on getMin would ruin O(1) guarantees. "
            "Keep a parallel stack of running minimums so each push records the min after that push. "
            "Pop both stacks together to stay synchronized."
        ),
        "steps": [
            "Maintain valStack and minStack.",
            "On push(x): push x; push min(x, minStack.top or x).",
            "On pop: pop both stacks.",
            "top reads valStack; getMin reads minStack.",
        ],
        "example": (
            "push 3: val=[3] min=[3]\n"
            "push 5: val=[3,5] min=[3,3]\n"
            "push 2: val=[3,5,2] min=[3,3,2]\n"
            "getMin -> 2"
        ),
        "trap": "Push the new minimum onto minStack even when equal to the current min so pops stay aligned.",
    },
    13: {
        "why": (
            "Copying values into an array and reversing uses O(n) extra space. "
            "Iterative pointer rewiring flips links in place with three pointers. "
            "Each node is visited once."
        ),
        "steps": [
            "Set prev = None, curr = head.",
            "While curr:",
            "Save next = curr.next.",
            "Set curr.next = prev.",
            "Advance prev = curr, curr = next.",
            "Return prev as new head.",
        ],
        "example": (
            "1 -> 2 -> 3 -> None\n"
            "flip: None <- 1    2 -> 3\n"
            "flip: None <- 1 <- 2    3\n"
            "result: 3 -> 2 -> 1"
        ),
        "trap": "Save next before overwriting curr.next or you lose the rest of the list.",
    },
    14: {
        "why": (
            "Recursion works but costs stack space proportional to list length. "
            "A dummy head simplifies edge cases when one list starts lower. "
            "Always attach the smaller node and advance that list's pointer."
        ),
        "steps": [
            "Create dummy node; tail points to dummy.",
            "While both lists exist:",
            "Attach the node with smaller value.",
            "Advance that list and tail.",
            "Attach remaining list if any.",
            "Return dummy.next.",
        ],
        "example": (
            "l1: 1->3, l2: 2->4\n"
            "pick 1, then 2, then 3, then 4\n"
            "merged: 1->2->3->4"
        ),
        "trap": "Forget to move tail forward after each attach and you create a cycle on the same node.",
    },
    15: {
        "why": (
            "Marking visited nodes with a hash set uses O(n) extra memory. "
            "Floyd's tortoise-and-hare detects a cycle because fast eventually laps slow inside the loop. "
            "If fast reaches null, the list is acyclic."
        ),
        "steps": [
            "Set slow = fast = head.",
            "While fast and fast.next:",
            "Move slow one step, fast two steps.",
            "If slow == fast, return True.",
            "Return False.",
        ],
        "example": (
            "3 -> 2 -> 0 -> -4\n"
            "       ^         |\n"
            "       |_________|\n"
            "slow and fast meet inside cycle -> True"
        ),
        "trap": "Initialize both at head and move fast twice per loop; starting fast at head.next misses some cycles.",
    },
    16: {
        "why": (
            "Creating new nodes is unnecessary; swapping child pointers at each node inverts the whole tree. "
            "Post-order or pre-order recursion visits every node once. "
            "BFS with a queue works too if you prefer iteration."
        ),
        "steps": [
            "If node is null, return null.",
            "Swap node.left and node.right.",
            "Recursively invert both children.",
            "Return node.",
        ],
        "example": (
            "    4           4\n"
            "   / \\   ->   / \\\n"
            "  2   7       7   2\n"
            " / \\         / \\\n"
            "1   3       3   1"
        ),
        "trap": "Swap before recursing so you invert the correct subtrees, not the already-swapped ones twice.",
    },
    17: {
        "why": (
            "A global counter with level tracking is more complex than the recursive definition. "
            "Height is 1 plus the deeper subtree, with base case 0 for null. "
            "Each node is counted once."
        ),
        "steps": [
            "If root is null, return 0.",
            "Compute leftDepth = depth(root.left).",
            "Compute rightDepth = depth(root.right).",
            "Return 1 + max(leftDepth, rightDepth).",
        ],
        "example": (
            "tree: 3 with children 9 and 20 (20 has 15,7)\n"
            "leaf depths 1, combined at 20 -> 2, at 3 -> 3"
        ),
        "trap": "Do not add 1 at null; null returns 0 so a single node correctly yields depth 1.",
    },
    18: {
        "why": (
            "Serializing both trees to compare strings hides structural null differences. "
            "Simultaneous recursion checks value equality and subtree shape together. "
            "Short-circuit on the first mismatch."
        ),
        "steps": [
            "If both null, return True.",
            "If exactly one null, return False.",
            "If values differ, return False.",
            "Return isSame(left) and isSame(right).",
        ],
        "example": (
            "p: 1(2,3)  q: 1(2,null,3) -> False (shape)\n"
            "p: 1(2,3)  q: 1(2,3)       -> True"
        ),
        "trap": "Compare structure before assuming values alone decide equality.",
    },
    19: {
        "why": (
            "DFS with a depth parameter works but scatters nodes across levels in one list. "
            "BFS naturally processes frontier-by-frontier if you batch each level's size. "
            "One queue and O(n) time collect all levels."
        ),
        "steps": [
            "If root null, return [].",
            "Queue = [root], result = [].",
            "While queue not empty:",
            "Snapshot size, drain that many nodes, enqueue children.",
            "Append level list to result.",
            "Return result.",
        ],
        "example": (
            "    3\n"
            "   / \\\n"
            "  9  20\n"
            "    /  \\\n"
            "   15   7\n"
            "-> [[3], [9,20], [15,7]]"
        ),
        "trap": "Read queue size before the inner loop; the queue grows as you enqueue children.",
    },
    20: {
        "why": (
            "Checking only parent-child order misses cases where a node violates an ancestor bound. "
            "Threading (lo, hi) intervals down the tree enforces the global BST property. "
            "Each node is validated once against its allowed range."
        ),
        "steps": [
            "Define check(node, lo, hi).",
            "Null passes.",
            "If val <= lo or val >= hi, return False.",
            "Recurse left with (lo, val) and right with (val, hi).",
            "Start with (-inf, +inf).",
        ],
        "example": (
            "    5\n"
            "   / \\\n"
            "  1   6\n"
            "     / \\\n"
            "    4   7 -> False (4 < 5 bound from root)"
        ),
        "trap": "Use strict inequalities for lo and hi so duplicates are rejected in a standard BST.",
    },
    21: {
        "why": (
            "General LCA on a binary tree needs extra logic after finding nodes. "
            "In a BST, all values in the left subtree are smaller, so the first node where p and q diverge is the answer. "
            "Walk from root in O(h) time with no extra space."
        ),
        "steps": [
            "Start at root.",
            "If both p and q are smaller, go left.",
            "If both are larger, go right.",
            "Otherwise current node is the split point; return it.",
        ],
        "example": (
            "BST: 6 with 2,8; p=2 q=8\n"
            "at 6: one left one right -> LCA = 6\n"
            "p=2 q=4: descend to 2, then split at 2"
        ),
        "trap": "Assuming p.val < q.val can fail if the caller passes q before p; compare both directions each step.",
    },
    22: {
        "why": (
            "Union-find can count components but flood fill is simpler on a grid. "
            "Each land cell starts one DFS/BFS that marks its whole island visited. "
            "Increment the count once per unvisited '1'."
        ),
        "steps": [
            "Set count = 0.",
            "For each cell (r,c):",
            "If grid[r][c] == '1' and unvisited:",
            "Run DFS/BFS to sink the island (mark '0' or visited).",
            "count += 1.",
            "Return count.",
        ],
        "example": (
            "grid:\n"
            "11100\n"
            "11000\n"
            "00101\n"
            "-> 3 islands"
        ),
        "trap": "Mutate the grid or maintain a visited matrix so you do not recount the same land cell.",
    },
    23: {
        "why": (
            "A shallow copy shares neighbor lists and corrupts the clone. "
            "Map each original node to its clone before wiring edges so you never duplicate nodes. "
            "DFS or BFS both visit each node and edge once."
        ),
        "steps": [
            "If node null, return null.",
            "Create cloneMap empty.",
            "DFS from node:",
            "If original seen, return cloneMap[original].",
            "Clone val, store in map, copy neighbors recursively.",
            "Return clone of start.",
        ],
        "example": (
            "1 -- 2\n"
            "|    |\n"
            "4 -- 3\n"
            "cloneMap[1]=1', wire 1'->2', etc.\n"
            "new graph is deep copy"
        ),
        "trap": "Create the clone node before recursing into neighbors to avoid infinite loops on cycles.",
    },
    24: {
        "why": (
            "Trying all orderings is factorial. "
            "Prerequisites form a directed graph; finishing all courses means a topological order exists. "
            "Kahn's algorithm peals nodes with indegree zero; if you process all n nodes, no cycle exists."
        ),
        "steps": [
            "Build adjacency list and indegree array.",
            "Enqueue all indegree-0 courses.",
            "While queue not empty:",
            "Pop course, append to order, relax neighbors (decrement indegree).",
            "Enqueue newly zero indegree nodes.",
            "Return len(order) == numCourses.",
        ],
        "example": (
            "n=2, prereqs [[1,0]]\n"
            "start with 0, then take 1\n"
            "order length 2 -> True"
        ),
        "trap": "Build edges as prereq -> course; reversing the edge direction breaks indegree logic.",
    },
    25: {
        "why": (
            "Simulating flow from every cell outward is expensive. "
            "Water reaches an ocean if there is a non-increasing path to the border; search backward from each ocean instead. "
            "Cells reachable from both Pacific and Atlantic sets are the answer."
        ),
        "steps": [
            "DFS/BFS from all Pacific border cells (top and left).",
            "Mark reachable pacific set.",
            "Repeat from Atlantic border (bottom and right).",
            "Return cells in both sets.",
        ],
        "example": (
            "heights:\n"
            "1 2 2 3\n"
            "3 2 3 4\n"
            "cell (0,3) reaches Pacific and Atlantic -> included"
        ),
        "trap": "Allow moves to equal or lower height; a strictly decreasing rule cuts valid paths.",
    },
    26: {
        "why": (
            "Linear scan is O(n) but the array is sorted, so half the range can be discarded each step. "
            "Maintain lo and hi and compare mid to target. "
            "Logarithmic comparisons pin down the index or prove absence."
        ),
        "steps": [
            "Set lo = 0, hi = n - 1.",
            "While lo <= hi, pick mid = lo + (hi - lo) // 2.",
            "If nums[mid] == target, return mid.",
            "If nums[mid] < target, lo = mid + 1; else hi = mid - 1.",
            "Return -1 if the loop exits without a match.",
        ],
        "example": (
            "nums = [-1,0,3,5,9,12], target = 9\n"
            "lo=0 hi=5 mid=2 (3<9) lo=3\n"
            "mid=4 -> nums[4]=9 -> return 4"
        ),
        "trap": "Use lo + (hi-lo)//2 to avoid overflow; off-by-one on lo=mid+1 and hi=mid-1 causes infinite loops.",
    },
    27: {
        "why": (
            "Plain binary search fails because rotation breaks global order. "
            "At least one half of mid is always sorted; test whether target lies in that sorted half. "
            "Discard the other half each iteration for O(log n)."
        ),
        "steps": [
            "Binary search with lo, hi.",
            "Identify which side of mid is sorted.",
            "If target in sorted range, shrink to that side.",
            "Otherwise search the other side.",
            "Return -1 if not found.",
        ],
        "example": (
            "nums = [4,5,6,7,0,1,2], target = 0\n"
            "left half 4..7 sorted, 0 not in range -> go right\n"
            "find 0 at index 4"
        ),
        "trap": "When nums[lo] == nums[mid] == nums[hi], shrink bounds; duplicates break the sorted-half test.",
    },
    28: {
        "why": (
            "Recursive enumeration retraces the same suffixes exponentially. "
            "Ways to reach step i equal ways to reach i-1 plus ways to reach i-2. "
            "Rolling two variables captures Fibonacci in O(n) time and O(1) space."
        ),
        "steps": [
            "If n <= 2, return n.",
            "Set a = 1, b = 2.",
            "For i from 3 to n:",
            "c = a + b; a = b; b = c.",
            "Return b.",
        ],
        "example": (
            "n = 5\n"
            "a,b: 1,2 -> 2,3 -> 3,5\n"
            "5 ways"
        ),
        "trap": "Base cases n=1 and n=2 must be handled before the loop to avoid off-by-one.",
    },
    29: {
        "why": (
            "Taking every other house greedily is not optimal when large values cluster. "
            "At each house you either skip it (keep prior best) or rob it (add to best two steps back). "
            "Two rolling states replace the full dp array."
        ),
        "steps": [
            "Set prev2 = 0, prev1 = 0.",
            "For each amount x:",
            "cur = max(prev1, prev2 + x).",
            "Shift prev2 = prev1, prev1 = cur.",
            "Return prev1.",
        ],
        "example": (
            "nums = [2,7,9,3,1]\n"
            "rob 2 -> skip 7 -> rob 9+2=11 vs paths\n"
            "best = 12 (2+9+1)"
        ),
        "trap": "Use prev2 + x for robbing current, not prev1 + x, because adjacent houses are forbidden.",
    },
    30: {
        "why": (
            "Greedy by largest coin fails on coin systems like [1, 3, 4] for amount 6. "
            "dp[a] stores the minimum coins needed for amount a built from smaller amounts. "
            "Trying every coin at each amount guarantees optimality."
        ),
        "steps": [
            "Initialize dp[0..amount] with infinity, dp[0]=0.",
            "For a from 1 to amount:",
            "For each coin c:",
            "If a >= c: dp[a] = min(dp[a], dp[a-c]+1).",
            "Return dp[amount] or -1 if still infinity.",
        ],
        "example": (
            "coins=[1,2,5], amount=11\n"
            "dp[5]=1, dp[6]=2, ... dp[11]=3 (5+5+1)"
        ),
        "trap": "Seed dp[0]=0 but infinity elsewhere; forgetting dp[0] makes every amount unreachable.",
    },
    31: {
        "why": (
            "DFS over the grid revisits subproblems without memoization. "
            "Paths to (i,j) come only from above or left on a right/down grid. "
            "Fill row by row reusing the recurrence dp[i][j] = dp[i-1][j] + dp[i][j-1]."
        ),
        "steps": [
            "Create m x n dp table.",
            "First row and column are all 1.",
            "For i from 1 to m-1, j from 1 to n-1:",
            "dp[i][j] = dp[i-1][j] + dp[i][j-1].",
            "Return dp[m-1][n-1].",
        ],
        "example": (
            "grid 3x3\n"
            "dp rows:\n"
            "1 1 1\n"
            "1 2 3\n"
            "1 3 6 -> 6 paths"
        ),
        "trap": "Initialize borders to 1; leaving them zero zeroes out the entire table.",
    },
    32: {
        "why": (
            "O(n^2) DP compares every pair and is fine for small n. "
            "Patience sorting maintains piles whose tops form an increasing sequence; binary search finds where each card goes. "
            "The number of piles equals the LIS length in O(n log n)."
        ),
        "steps": [
            "Maintain array tails (smallest tail of length L+1).",
            "For each x in nums:",
            "Binary search position pos in tails.",
            "Place x at tails[pos] (extend or replace).",
            "Return len(tails).",
        ],
        "example": (
            "nums = [10,9,2,5,3,7,101,18]\n"
            "tails evolve: [2], [2,3], [2,3,7], ... length 4"
        ),
        "trap": "tails is not the actual subsequence; its length is the answer, not the array contents.",
    },
    33: {
        "why": (
            "Trying every split recursively without memo explodes on long strings. "
            "dp[i] means s[0:i] can be segmented; reuse answers for shorter prefixes. "
            "Only check breaks at dictionary words."
        ),
        "steps": [
            "Put dictionary in a set.",
            "dp[0] = True.",
            "For i from 1 to n:",
            "For j from 0 to i-1:",
            "If dp[j] and s[j:i] in dict: dp[i]=True; break.",
            "Return dp[n].",
        ],
        "example": (
            "s = \"leetcode\", dict {leet, code}\n"
            "dp[4]=True (leet), dp[8]=True (code) -> True"
        ),
        "trap": "Empty prefix dp[0]=True is required so a whole-string match like s itself works.",
    },
    34: {
        "why": (
            "Bitmask iteration generates subsets but is easy to mishandle for duplicates. "
            "Include/exclude recursion at each index builds all 2^n subsets systematically. "
            "Sorting first helps skip duplicate branches when nums has repeats."
        ),
        "steps": [
            "Sort nums if duplicates possible.",
            "Backtrack with path and start index.",
            "Push copy of path to answer each step.",
            "For i from start to n-1:",
            "Skip duplicate nums[i] at same depth.",
            "Include nums[i], recurse i+1, backtrack.",
        ],
        "example": (
            "nums = [1,2]\n"
            "path: [] -> [1] -> [1,2] -> [2]\n"
            "subsets: [[],[1],[1,2],[2]]"
        ),
        "trap": "Push the current path before choosing more elements so empty subset is included.",
    },
    35: {
        "why": (
            "Generating permutations by sorting and next-permutation is slower than direct construction. "
            "Track which indices are used and swap choices at each depth. "
            "When path length equals n, record one permutation."
        ),
        "steps": [
            "Maintain used flags and path.",
            "If len(path) == n, append copy to result.",
            "For i from 0 to n-1:",
            "Skip if used[i].",
            "Mark used, push nums[i], recurse, undo.",
        ],
        "example": (
            "nums = [1,2,3]\n"
            "build 1,2,3 then backtrack permutations\n"
            "6 total orderings"
        ),
        "trap": "Copy path when saving; otherwise backtracking mutates stored results.",
    },
    36: {
        "why": (
            "Brute force tries every multiset of coins with loose limits. "
            "Fix an increasing start index so [2,3] and [3,2] are not both recorded when reuse is allowed. "
            "Same index can be chosen again only by recursing without advancing i."
        ),
        "steps": [
            "Sort candidates.",
            "Backtrack(path, start, remaining):",
            "If remaining == 0, save path.",
            "If remaining < 0, return.",
            "For i from start:",
            "Add candidates[i], recurse(i, remaining-cand[i]), pop.",
        ],
        "example": (
            "candidates=[2,3,6], target=7\n"
            "pick 2,2,3 -> sum 7\n"
            "answer [[2,2,3],[7]]"
        ),
        "trap": "Pass i not i+1 when reusing the same coin; i+1 only when moving to a strictly later candidate.",
    },
    37: {
        "why": (
            "Full sort finds the kth largest in O(n log n) but discards order information you do not need. "
            "A size-k min-heap keeps the k largest seen so far; the root is the kth largest. "
            "Quickselect is faster average case but heap is simpler to implement cleanly."
        ),
        "steps": [
            "Build min-heap of first k elements.",
            "For each remaining x:",
            "If x > heap.min, pop min and push x.",
            "Return heap.min (kth largest).",
        ],
        "example": (
            "nums = [3,2,1,5,6,4], k = 2\n"
            "heap after scan holds {5,6}\n"
            "min = 5"
        ),
        "trap": "Kth largest is not kth index after ascending sort; k=1 means the maximum element.",
    },
    38: {
        "why": (
            "Merging on the fly without sorting misses overlaps between non-adjacent intervals. "
            "Sort by start so overlapping intervals appear consecutively. "
            "Extend the last merged end instead of starting a new interval whenever they touch."
        ),
        "steps": [
            "Sort intervals by start.",
            "Init merged with first interval.",
            "For each next [s,e]:",
            "If s <= last.end, last.end = max(last.end, e).",
            "Else append new interval.",
            "Return merged.",
        ],
        "example": (
            "[[1,3],[2,6],[8,10],[15,18]]\n"
            "merge [1,3]+[2,6] -> [1,6]\n"
            "result [[1,6],[8,10],[15,18]]"
        ),
        "trap": "Use max on end when merging; a nested interval may extend farther than the current end.",
    },
    39: {
        "why": (
            "Resorting the whole list after insert works but wastes O(n log n). "
            "The existing list is sorted and non-overlapping, so one linear scan buckets intervals before, during, and after the new one. "
            "Merge the overlapping middle in a single pass."
        ),
        "steps": [
            "Collect intervals entirely before new.start.",
            "Merge overlapping ones with new (stretch end).",
            "Append intervals that start after merged end.",
            "Return combined list.",
        ],
        "example": (
            "intervals=[[1,3],[6,9]], new=[2,5]\n"
            "overlap merge -> [1,5], keep [6,9]\n"
            "[[1,5],[6,9]]"
        ),
        "trap": "Overlap means start <= current end, not strict less-than; touching intervals [1,2] and [2,3] merge.",
    },
    40: {
        "why": (
            "For each day, scanning forward for warmth is O(n^2). "
            "A decreasing stack holds indices of unresolved days; a warmer day pops cooler days and sets their wait distance. "
            "Each index is pushed and popped once."
        ),
        "steps": [
            "Initialize stack empty, answer zeros.",
            "For i from 0 to n-1:",
            "While stack nonempty and T[i] > T[stack.top]:",
            "j = pop; answer[j] = i - j.",
            "Push i.",
            "Return answer.",
        ],
        "example": (
            "T = [73,74,75,71,69,72,76,73]\n"
            "day 0 waits 1 day (74), day 1 waits 1 (75), etc."
        ),
        "trap": "Store indices on the stack, not temperatures, so you can compute day differences.",
    },
    41: {
        "why": (
            "All subarray sums are O(n^2). "
            "Prefix sums turn a subarray sum into prefix[j] - prefix[i]; count pairs with difference k. "
            "A frequency map of prefix sums finds matches in one pass."
        ),
        "steps": [
            "Map count {0:1}, prefix = 0, ans = 0.",
            "For each x:",
            "prefix += x.",
            "ans += count.get(prefix - k, 0).",
            "Increment count[prefix].",
            "Return ans.",
        ],
        "example": (
            "nums = [1,1,1], k = 2\n"
            "prefixes 1,2,3\n"
            "at prefix 2: one way (1+1), at 3: one more -> 2"
        ),
        "trap": "Seed count[0]=1 so subarrays starting at index 0 are counted when prefix equals k.",
    },
    42: {
        "why": (
            "A map alone does not track recency for eviction. "
            "Pair a hash map (key to node) with a doubly linked list in MRU-to-LRU order. "
            "get and put splice the node to the front in O(1)."
        ),
        "steps": [
            "Map key -> list node; dummy head/tail DLL.",
            "get(key): if missing return -1; move node to front; return val.",
            "put(key,val): update or create node at front.",
            "If size > capacity, remove LRU tail and erase from map.",
        ],
        "example": (
            "cap=2: put(1,1) put(2,2) get(1)->1\n"
            "put(3,3) evicts key 2\n"
            "get(2) -> -1"
        ),
        "trap": "Updating an existing key must refresh its position, not only its value, or LRU order is wrong.",
    },
    43: {
        "why": (
            "Scanning a flat list of words for prefix checks is slow for many strings. "
            "A trie shares prefixes so common beginnings are stored once. "
            "Each character walk is O(L) for word length L."
        ),
        "steps": [
            "Root node with children map.",
            "insert(word): walk/creat nodes per char; mark end.",
            "search(word): walk; return true only if end flag set.",
            "startsWith(prefix): walk; return false on missing edge.",
        ],
        "example": (
            "insert \"apple\"\n"
            "search \"app\" -> False\n"
            "startsWith \"app\" -> True"
        ),
        "trap": "startsWith must not require the end flag; search must require it.",
    },
    44: {
        "why": (
            "Brute force from every cell repeats path work. "
            "DFS from each match of the first letter explores only viable paths with backtracking. "
            "Mark cells visited during a path, then restore them when unwinding."
        ),
        "steps": [
            "For each cell matching word[0]:",
            "Run dfs(r,c, index).",
            "If out of bounds or mismatch, return False.",
            "If index == len(word)-1, return True.",
            "Mark visited, try 4 neighbors, unmark.",
            "Return False if all fail.",
        ],
        "example": (
            "board ABCE, word ACE\n"
            "start A(0,0) -> C(1,0) -> E(0,2) -> True"
        ),
        "trap": "Restore the cell after backtracking; permanent marks block other paths through that cell.",
    },
    45: {
        "why": (
            "Precomputing left and right max arrays uses O(n) extra space. "
            "Two pointers from both ends track the tallest bars seen on each side. "
            "The shorter side limits water at that pointer, so you can move inward safely."
        ),
        "steps": [
            "Set lo=0, hi=n-1, leftMax=0, rightMax=0, water=0.",
            "While lo < hi:",
            "If height[lo] <= height[hi]: update leftMax, add leftMax-h[lo] to water, lo++.",
            "Else: update rightMax, add rightMax-h[hi], hi--.",
            "Return water.",
        ],
        "example": (
            "h = [0,1,0,2,1,0,1,3,2,1,2,1]\n"
            "trapped units sum to 6"
        ),
        "trap": "Process the shorter side first; moving the taller side can miss water before the other max is known.",
    },
    46: {
        "why": (
            "Merging both arrays defeats the logarithmic requirement. "
            "The median splits combined sorted order at a partition; binary search that cut on the shorter array. "
            "Ensure max(left halves) <= min(right halves) to validate a partition."
        ),
        "steps": [
            "Ensure A is the shorter array.",
            "Binary search cut i in A (0..m).",
            "j = (m+n+1)//2 - i in B.",
            "Compare A[i-1], B[j-1] vs A[i], B[j] for cross-boundary order.",
            "Adjust i until valid; compute median from boundary values.",
        ],
        "example": (
            "A=[1,3], B=[2]\n"
            "partition i=1 j=1\n"
            "left max 3? check B[j-1]=2 ok\n"
            "median = 2"
        ),
        "trap": "Handle empty halves with +/- infinity sentinels; off-by-one on i and j breaks boundary comparisons.",
    },
    47: {
        "why": (
            "Level-order without null markers loses shape for skewed trees. "
            "Preorder with explicit null tokens encodes structure and values in one string. "
            "Rebuild by consuming tokens left to right, recursing when a value is not null."
        ),
        "steps": [
            "Serialize: preorder; write val or 'null'.",
            "Join tokens with a delimiter.",
            "Deserialize: read token; if null return None.",
            "Create node, attach left child, attach right child.",
            "Return root.",
        ],
        "example": (
            "tree 1(2,3)\n"
            "encode \"1,2,null,null,3,null,null\"\n"
            "decode rebuilds same shape"
        ),
        "trap": "You must encode null children in preorder; omitting them makes unique reconstruction impossible.",
    },
    48: {
        "why": (
            "DFS finds a path but not necessarily the shortest transformation. "
            "BFS layers expand word distance one edit at a time from beginWord. "
            "Preprocessing wildcard buckets (e.g. *ot for hot) speeds neighbor lookup."
        ),
        "steps": [
            "Build adjacency: for each word, link words one letter apart.",
            "BFS queue from beginWord; track visited.",
            "For each word, enqueue unvisited neighbors.",
            "Stop when endWord reached; return level count.",
            "Return 0 if endWord never reached.",
        ],
        "example": (
            "begin=\"hit\" end=\"cog\"\n"
            "list [hot,dot,dog,cog,...]\n"
            "hit->hot->dot->dog->cog = 5 words"
        ),
        "trap": "Mark words visited when enqueuing, not when dequeuing, or the same word enters the queue many times.",
    },
}
