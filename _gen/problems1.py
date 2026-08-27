P1 = [
{
  "id": "two-sum", "name": "Two Sum", "diff": "easy", "pattern": "hashmap-lookup", "topic": "arrays",
  "why": "The canonical HashMap complement problem. If you cannot do this in 8 minutes with a clean explanation, you are not ready for a screen.",
  "stmt": "Given integers nums and a target, return any two distinct indices i, j such that nums[i] + nums[j] equals target. Exactly one solution exists.",
  "exin": "nums = [2,7,11,15], target = 9", "exout": "[0,1]",
  "cons": "2 ≤ n ≤ 10^4; values and target typically in 32-bit range.",
  "hints": "For each value x, you need target − x. Have you already seen that complement?",
  "brute": "Try every pair (i, j), i < j. O(n²) time, O(1) space.",
  "opt": "One pass Map from value → index. Before inserting nums[i], look up target − nums[i].",
  "steps": "i=0: 2, need 7, miss, store 2→0. i=1: 7, need 2, found at 0. Return [0,1]. Storing after the lookup allows using each index once.",
  "cx": "O(n) time expected, O(n) space.",
  "mistakes": "Two-pass that accidentally uses the same index twice. Sorting and losing original indices.",
  "edges": "Negatives; pair at the ends; duplicate values that sum to target (e.g. [3,3], 6).",
  "follow": "Return all pairs? 3Sum? What if the array is sorted? (two pointers, O(1) extra).",
  "talk": "I would mention the sort+two-pointer trade-off if memory were tighter. I would not use a nested loop on 10^4 without commenting that it is a fallback.",
  "sol": """function twoSum(nums: number[], target: number): [number, number] {
  const seen = new Map<number, number>();
  for (let i = 0; i < nums.length; i++) {
    const j = seen.get(target - nums[i]);
    if (j !== undefined) return [j, i];
    seen.set(nums[i], i);
  }
  throw new Error("no pair");
}"""
},
{
  "id": "contains-dup", "name": "Contains Duplicate", "diff": "easy", "pattern": "hashmap-lookup", "topic": "arrays",
  "why": "Teaches Set membership and the sort-vs-hash space trade-off you should always mention.",
  "stmt": "Return true if any value appears at least twice in nums.",
  "exin": "nums = [1,2,3,1]", "exout": "true",
  "cons": "1 ≤ n ≤ 10^5.",
  "hints": "A Set tells you in expected O(1) whether you have seen x.",
  "brute": "For each i, scan the rest. O(n²).",
  "opt": "Set: if has(x) return true else add. Or sort and compare neighbors O(n log n) time, O(1) extra if in-place is allowed.",
  "steps": "Walk left to right. The first time a value is already in the set, you can exit early — useful if duplicates are common.",
  "cx": "Hash: O(n) time, O(n) space. Sort: O(n log n) time, O(1) extra.",
  "mistakes": "Using an object and colliding on unexpected keys. Forgetting early exit.",
  "edges": "Single element; all unique; all same.",
  "follow": "Contains duplicate within distance k (Map of last index).",
  "talk": "Ask whether mutating/sorting the input is allowed. Atlassian-style: state both solutions and pick based on constraints.",
  "sol": """function containsDuplicate(nums: number[]): boolean {
  const seen = new Set<number>();
  for (const x of nums) {
    if (seen.has(x)) return true;
    seen.add(x);
  }
  return false;
}"""
},
{
  "id": "valid-anagram", "name": "Valid Anagram", "diff": "easy", "pattern": "frequency-counting", "topic": "strings",
  "why": "Frequency maps are how you later unlock Group Anagrams and permutation windows.",
  "stmt": "Return whether t is an anagram of s (same characters, same counts).",
  "exin": 's = "anagram", t = "nagaram"', "exout": "true",
  "cons": "Lengths up to 10^5; lowercase English unless specified.",
  "hints": "If lengths differ, false. Count s, decrement with t, ensure no leftover.",
  "brute": "Sort both strings and compare. O(n log n).",
  "opt": "One array of 26 counts, or a Map. O(n) time, O(1) if alphabet is fixed.",
  "steps": "Increment for s, decrement for t. Any negative or leftover nonzero means mismatch. Length check is the cheap reject.",
  "cx": "O(n) time, O(1) space for 26 letters.",
  "mistakes": "Unicode: 26-array fails. Using sort in a tight inner loop later.",
  "edges": "Empty strings; one empty; unicode if the interviewer changes the alphabet.",
  "follow": "Unicode? Streaming? Case sensitivity?",
  "talk": "Confirm the alphabet. If it is Unicode, say Map and O(Σ) space.",
  "sol": """function isAnagram(s: string, t: string): boolean {
  if (s.length !== t.length) return false;
  const c = Array(26).fill(0);
  for (let i = 0; i < s.length; i++) {
    c[s.charCodeAt(i) - 97]++;
    c[t.charCodeAt(i) - 97]--;
  }
  return c.every((x) => x === 0);
}"""
},
{
  "id": "group-anagrams", "name": "Group Anagrams", "diff": "medium", "pattern": "frequency-counting", "topic": "strings",
  "why": "Canonical keys. Senior candidates pick a key that is O(L) not O(L log L) when the alphabet is small.",
  "stmt": "Group words that are anagrams of each other. Order of groups and words inside a group can be anything.",
  "exin": 'strs = ["eat","tea","tan","ate","nat","bat"]', "exout": '[["eat","tea","ate"],["tan","nat"],["bat"]]',
  "cons": "n words, each length L; n*L up to ~10^4–10^5.",
  "hints": "Two words are in the same group iff they share a canonical key: sorted string or count signature.",
  "brute": "For each word, compare to every group leader with an anagram check. O(n² L).",
  "opt": "Map from key → list. Key = sorted(word) O(L log L) or 26-count joined O(L).",
  "steps": "Choose a key function that is identical exactly for anagrams. Push each word into map[key]. Return Object.values.",
  "cx": "O(n L log L) with sort keys, or O(n L) with count keys. Space O(n L).",
  "mistakes": "Using the word itself as the key. Mutating the original strings.",
  "edges": "Empty string word; all unique; all one group.",
  "follow": "Very large alphabet? Need a hash of counts instead of a string key.",
  "talk": "I would write the sort key first (clear), then mention the count signature if they want tighter time.",
  "sol": """function groupAnagrams(strs: string[]): string[][] {
  const map = new Map<string, string[]>();
  for (const w of strs) {
    const key = w.split("").sort().join("");
    const bucket = map.get(key);
    if (bucket) bucket.push(w);
    else map.set(key, [w]);
  }
  return [...map.values()];
}"""
},
{
  "id": "top-k-freq", "name": "Top K Frequent Elements", "diff": "medium", "pattern": "heap-topk", "topic": "heap",
  "why": "Count then select. Teaches heap-of-size-K vs bucket sort vs full sort.",
  "stmt": "Return the k values that appear most often. Order among the k does not matter.",
  "exin": "nums = [1,1,1,2,2,3], k = 2", "exout": "[1,2]",
  "cons": "k is in [1, number of unique values]; n up to 10^5.",
  "hints": "Frequency map first. Then you need the k largest frequencies — heap, sort, or bucket (freq as index).",
  "brute": "Count, sort unique values by freq desc, take k. O(u log u).",
  "opt": "Min-heap of size k on frequency, or bucket sort because freq ≤ n.",
  "steps": "Count O(n). If you sort entries by freq you are done and the code is short — say O(u log u). Heap is O(u log k). Buckets: array of lists indexed by freq, scan from n down.",
  "cx": "Count O(n). Selection O(u log k) heap or O(n) extra for buckets.",
  "mistakes": "Heap comparator inverted. Returning frequencies instead of values.",
  "edges": "k = 1; all unique and k = n; ties (prompt usually guarantees uniqueness of the set).",
  "follow": "Top K frequent words (tie-break lexicographic). Stream of data.",
  "talk": "In JS without a heap library I will sort unless they want the O(n log k) discussion. That is an honest senior answer.",
  "sol": """function topKFrequent(nums: number[], k: number): number[] {
  const freq = new Map<number, number>();
  for (const x of nums) freq.set(x, (freq.get(x) ?? 0) + 1);
  return [...freq.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, k)
    .map(([v]) => v);
}"""
},
{
  "id": "product-except", "name": "Product of Array Except Self", "diff": "medium", "pattern": "prefix-sum", "topic": "arrays",
  "why": "Prefix/suffix without the division cop-out. Tests whether you can do two passes cleanly.",
  "stmt": "Return answer[i] = product of all nums[j] for j ≠ i. Do not use division. O(n) time.",
  "exin": "nums = [1,2,3,4]", "exout": "[24,12,8,6]",
  "cons": "n ≥ 2; values may include 0 (one zero or many zeros changes the pattern).",
  "hints": "answer[i] = (product of left of i) × (product of right of i).",
  "brute": "For each i multiply the rest. O(n²). Division by nums[i] fails when zeros exist and is disallowed.",
  "opt": "First pass: answer[i] = left product. Second pass: multiply a running right product.",
  "steps": "Left: ans[0]=1, ans[i]=ans[i-1]*nums[i-1]. Right: r=1, for i from n-1..0: ans[i]*=r; r*=nums[i].",
  "cx": "O(n) time, O(1) extra if the output array does not count.",
  "mistakes": "Using division. Off-by-one on left[i]. Not handling zeros if you took the division path.",
  "edges": "One zero (exactly one index gets the product of the rest). Two zeros (all zeros). Negatives.",
  "follow": "Can you do it in one array? What if overflow matters (use bigints or mention 32-bit).",
  "talk": "I will state that output space is allowed. I will not pretend a second array is O(1).",
  "sol": """function productExceptSelf(nums: number[]): number[] {
  const n = nums.length, ans = Array(n).fill(1);
  for (let i = 1; i < n; i++) ans[i] = ans[i - 1] * nums[i - 1];
  let right = 1;
  for (let i = n - 1; i >= 0; i--) {
    ans[i] *= right;
    right *= nums[i];
  }
  return ans;
}"""
},
{
  "id": "longest-consec", "name": "Longest Consecutive Sequence", "diff": "medium", "pattern": "hashmap-lookup", "topic": "arrays",
  "why": "O(n) requires a Set plus the 'only start at the beginning of a run' trick — a favorite Medium.",
  "stmt": "Length of the longest run of consecutive integers (order in the array does not matter). Extra time should be O(n).",
  "exin": "nums = [100,4,200,1,3,2]", "exout": "4", "exnote": "The run is 1,2,3,4.",
  "cons": "n up to 10^5; values can be huge (do not allocate an array of max-min).",
  "hints": "Put everything in a Set. A number x starts a run only if x-1 is absent.",
  "brute": "Sort unique values, scan streaks. O(n log n).",
  "opt": "Set + expand right from each run start. Each value is visited a constant number of times.",
  "steps": "For each x, if x-1 not in set, walk x, x+1, … until missing. Track max length.",
  "cx": "O(n) expected time, O(n) space.",
  "mistakes": "Expanding from every x (becomes O(n²)). Not using a set so 'in' is O(n).",
  "edges": "Empty; singles; duplicates; negatives.",
  "follow": "Return the actual sequence. Parallelize? Not in an interview.",
  "talk": "If they relax O(n), sorting is cleaner. I would implement Set first because the prompt asks for it.",
  "sol": """function longestConsecutive(nums: number[]): number {
  const s = new Set(nums);
  let best = 0;
  for (const x of s) {
    if (s.has(x - 1)) continue;
    let y = x, len = 1;
    while (s.has(y + 1)) { y++; len++; }
    best = Math.max(best, len);
  }
  return best;
}"""
},
{
  "id": "valid-sudoku", "name": "Valid Sudoku", "diff": "medium", "pattern": "hashmap-lookup", "topic": "arrays",
  "why": "Encoding a constraint as a key. Clean code matters more than cleverness.",
  "stmt": "A 9×9 board with digits and '.' empties is valid if no digit repeats in any row, column, or 3×3 box. Do not solve the puzzle.",
  "exin": "a mostly-filled valid board", "exout": "true or false",
  "cons": "Always 9×9.",
  "hints": "Three families of sets, or one set of strings like `r0#5`, `c3#5`, `b1-2#5`.",
  "brute": "For each cell, scan its row, column, and box. O(1) since 9 is constant, but messy.",
  "opt": "One pass, 27 sets (9+9+9) or encoded keys in one Set.",
  "steps": "box = (r/3)*3 + (c/3). If digit already in row[r], col[c], or box[b], invalid.",
  "cx": "O(1) time and space (81 cells).",
  "mistakes": "Wrong box index. Validating empties. Trying to solve instead of validate.",
  "edges": "All empty (valid). Duplicate in a box only.",
  "follow": "Sudoku solver (backtracking) — later phase.",
  "talk": "I will write readable box math and mention it is O(1) because the board size is fixed.",
  "sol": """function isValidSudoku(board: string[][]): boolean {
  const row: Set<string>[] = Array.from({ length: 9 }, () => new Set());
  const col: Set<string>[] = Array.from({ length: 9 }, () => new Set());
  const box: Set<string>[] = Array.from({ length: 9 }, () => new Set());
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      const v = board[r][c];
      if (v === ".") continue;
      const b = Math.floor(r / 3) * 3 + Math.floor(c / 3);
      if (row[r].has(v) || col[c].has(v) || box[b].has(v)) return false;
      row[r].add(v); col[c].add(v); box[b].add(v);
    }
  }
  return true;
}"""
},
{
  "id": "valid-palindrome", "name": "Valid Palindrome", "diff": "easy", "pattern": "two-pointers", "topic": "strings",
  "why": "Two pointers plus a filtering predicate. Communication: define 'alphanumeric' before coding.",
  "stmt": "After ignoring non-alphanumeric characters and case, is the string a palindrome?",
  "exin": 's = "A man, a plan, a canal: Panama"', "exout": "true",
  "cons": "Length up to 2·10^5.",
  "hints": "i from start, j from end; skip junk; compare lowercased.",
  "brute": "Build a filtered string, compare to its reverse. Extra O(n) space.",
  "opt": "Two pointers, O(1) extra.",
  "steps": "While i<j, advance i until alnum, j until alnum, compare. Mismatch → false.",
  "cx": "O(n) time, O(1) space.",
  "mistakes": "Not skipping on both sides independently. Unicode beyond ASCII if they ask.",
  "edges": "Empty after filter (true). Single char. All punctuation.",
  "follow": "Palindrome after at most one deletion (another two-pointer).",
  "talk": "I would ask about Unicode. For the classic prompt, [A-Za-z0-9] is enough.",
  "sol": """function isPalindrome(s: string): boolean {
  const ok = (c: string) => /[a-z0-9]/i.test(c);
  let i = 0, j = s.length - 1;
  while (i < j) {
    while (i < j && !ok(s[i])) i++;
    while (i < j && !ok(s[j])) j--;
    if (s[i].toLowerCase() !== s[j].toLowerCase()) return false;
    i++; j--;
  }
  return true;
}"""
},
{
  "id": "two-sum-ii", "name": "Two Sum II (Sorted)", "diff": "medium", "pattern": "two-pointers", "topic": "arrays",
  "why": "Shows you will not blindly HashMap a sorted array. O(1) extra is the point.",
  "stmt": "1-indexed sorted ascending array. Return two indices (1-based) of a pair summing to target. Exactly one answer. Constant extra space preferred.",
  "exin": "numbers = [2,7,11,15], target = 9", "exout": "[1,2]",
  "cons": "n up to 3·10^4; already sorted.",
  "hints": "If sum is too small, the left value must grow. If too big, the right value must shrink.",
  "brute": "Nested loops still work but ignore sortedness.",
  "opt": "Opposite two pointers.",
  "steps": "i=0,j=n-1. s=a[i]+a[j]. Equal → return i+1,j+1. s<target → i++. else j--.",
  "cx": "O(n) time, O(1) space.",
  "mistakes": "Returning 0-based indices. Using a HashMap and failing the space constraint.",
  "edges": "Pair is the two ends. Duplicates.",
  "follow": "3Sum on a sorted array is the next step.",
  "talk": "I would mention HashMap is correct but uses O(n) space — they asked for two pointers.",
  "sol": """function twoSumII(numbers: number[], target: number): [number, number] {
  let i = 0, j = numbers.length - 1;
  while (i < j) {
    const s = numbers[i] + numbers[j];
    if (s === target) return [i + 1, j + 1];
    if (s < target) i++; else j--;
  }
  throw new Error("none");
}"""
},
{
  "id": "three-sum", "name": "3Sum", "diff": "medium", "pattern": "two-pointers", "topic": "arrays",
  "why": "The first problem where duplicate-skipping is the real difficulty. Medium bar for senior screens.",
  "stmt": "All unique triplets i<j<k with nums[i]+nums[j]+nums[k]=0. Return the values, not indices.",
  "exin": "nums = [-1,0,1,2,-1,-4]", "exout": "[[-1,-1,2],[-1,0,1]]",
  "cons": "n up to ~3000, so O(n²) is the target; O(n³) will TLE.",
  "hints": "Sort. Fix i. Two-pointer the rest to −nums[i]. Skip duplicate i, left, and right.",
  "brute": "Three nested loops + a set of sorted triples. O(n³).",
  "opt": "Sort + O(n) two-pointer per i → O(n²).",
  "steps": "After sort, for i in 0..n-3: if a[i]===a[i-1] continue; L=i+1,R=n-1; move L/R on sum; on hit, record and skip equal L/R.",
  "cx": "O(n²) time, O(1) extra besides the output.",
  "mistakes": "Forgetting to skip duplicates. Reusing the same index. Starting L at 0.",
  "edges": "Fewer than 3 numbers. All zeros. No triplets.",
  "follow": "3Sum closest. 4Sum (fix two, two-pointer).",
  "talk": "I will sort first and narrate the skip conditions before coding them — that is where people fail.",
  "sol": """function threeSum(nums: number[]): number[][] {
  nums.sort((a, b) => a - b);
  const out: number[][] = [];
  for (let i = 0; i < nums.length - 2; i++) {
    if (i && nums[i] === nums[i - 1]) continue;
    let L = i + 1, R = nums.length - 1;
    while (L < R) {
      const s = nums[i] + nums[L] + nums[R];
      if (s === 0) {
        out.push([nums[i], nums[L], nums[R]]);
        L++; R--;
        while (L < R && nums[L] === nums[L - 1]) L++;
        while (L < R && nums[R] === nums[R + 1]) R--;
      } else if (s < 0) L++;
      else R--;
    }
  }
  return out;
}"""
},
{
  "id": "container-water", "name": "Container With Most Water", "diff": "medium", "pattern": "two-pointers", "topic": "arrays",
  "why": "Greedy discard. You must explain why the shorter line can be abandoned.",
  "stmt": "Heights of vertical lines at x = 0..n-1. Choose two lines that with the x-axis form a container of maximum water (area = min(h[i],h[j]) * (j-i)).",
  "exin": "height = [1,8,6,2,5,4,8,3,7]", "exout": "49",
  "cons": "n up to 10^5 so O(n) is required.",
  "hints": "Start at both ends. The width is already maximum. The only way to improve is a taller limiting height, so move the shorter pointer.",
  "brute": "All pairs. O(n²).",
  "opt": "Two pointers, O(n).",
  "steps": "area = min(h[i],h[j])*(j-i). If h[i]<h[j], any container using i and an index < j is narrower and still limited by ≤ h[i], so i++. Symmetric for j.",
  "cx": "O(n) time, O(1) space.",
  "mistakes": "Moving the taller pointer. Computing width as j-i+1.",
  "edges": "Two lines. Increasing sequence. Zeros.",
  "follow": "Trapping rain water is a different problem (valleys, not one container).",
  "talk": "I will prove the discard in one sentence before I touch the keyboard.",
  "sol": """function maxArea(height: number[]): number {
  let i = 0, j = height.length - 1, best = 0;
  while (i < j) {
    best = Math.max(best, Math.min(height[i], height[j]) * (j - i));
    if (height[i] < height[j]) i++; else j--;
  }
  return best;
}"""
},
{
  "id": "trapping-rain", "name": "Trapping Rain Water", "diff": "hard", "pattern": "two-pointers", "topic": "arrays",
  "why": "The one Hard worth doing in Phase 1. Water at i is min(leftMax, rightMax) − h[i] if positive.",
  "stmt": "Elevation map. How many units of water can sit after rain?",
  "exin": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "exout": "6",
  "cons": "n up to 2·10^4–10^5.",
  "hints": "Precompute leftMax/rightMax arrays, or two pointers tracking the running max on each side.",
  "brute": "For each i, scan left for max and right for max. O(n²).",
  "opt": "Two arrays O(n) space, or two pointers O(1) space: the side with the smaller max is bounded and can be resolved.",
  "steps": "Pointer version: if leftMax < rightMax, water at i is leftMax−h[i] (cannot exceed leftMax, and right is at least that). Advance that side.",
  "cx": "O(n) time, O(1) extra for two pointers.",
  "mistakes": "Confusing this with container-with-water. Negative water. Off-by-one on ends (ends hold 0).",
  "edges": "Strictly increasing (0 water). Single bar. All zeros.",
  "follow": "2D trapping (hard, skip for Phase 1).",
  "talk": "I will implement the two-array version first if time is tight — correctness over cleverness — then mention O(1) space.",
  "sol": """function trap(height: number[]): number {
  let i = 0, j = height.length - 1, L = 0, R = 0, water = 0;
  while (i < j) {
    if (height[i] < height[j]) {
      L = Math.max(L, height[i]);
      water += L - height[i];
      i++;
    } else {
      R = Math.max(R, height[j]);
      water += R - height[j];
      j--;
    }
  }
  return water;
}"""
},
{
  "id": "buy-sell", "name": "Best Time to Buy and Sell Stock", "diff": "easy", "pattern": "sliding-window", "topic": "arrays",
  "why": "One-pass running minimum. Often a warm-up; still expect a clean O(n) story.",
  "stmt": "prices[i] is the price on day i. At most one buy and one later sell. Maximize profit; 0 if no profit.",
  "exin": "prices = [7,1,5,3,6,4]", "exout": "5",
  "cons": "n up to 10^5.",
  "hints": "Track the lowest price so far. Profit today is price − that min.",
  "brute": "All buy/sell pairs i<j. O(n²).",
  "opt": "One pass min-so-far.",
  "steps": "minP = ∞. For each p: minP = min(minP,p); best = max(best, p−minP).",
  "cx": "O(n) time, O(1) space.",
  "mistakes": "Selling before buying. Resetting min after computing profit incorrectly.",
  "edges": "Decreasing prices (0). Two days. Single day.",
  "follow": "Unlimited transactions (greedy). Cooldown / fee (DP, later).",
  "talk": "I will call it a running minimum, not force a window vocabulary.",
  "sol": """function maxProfit(prices: number[]): number {
  let minP = Infinity, best = 0;
  for (const p of prices) {
    minP = Math.min(minP, p);
    best = Math.max(best, p - minP);
  }
  return best;
}"""
},
{
  "id": "longest-substr", "name": "Longest Substring Without Repeating Characters", "diff": "medium", "pattern": "sliding-window", "topic": "strings",
  "why": "The sliding-window poster child. You must keep the invariant: window has unique chars.",
  "stmt": "Length of the longest substring (contiguous) with all unique characters.",
  "exin": 's = "abcabcbb"', "exout": "3",
  "cons": "n up to 5·10^4; charset may be ASCII.",
  "hints": "Last-seen index. If the previous occurrence is still inside the window, jump left past it.",
  "brute": "All i,j plus a set. O(n²) if you are careful, O(n³) if you are not.",
  "opt": "Window + Map char → last index. O(n).",
  "steps": "For r=0..n-1: if last[s[r]] ≥ left, left = last[s[r]]+1. Update last. best = max(best, r-left+1).",
  "cx": "O(n) time, O(Σ) space.",
  "mistakes": "left = max(left, last+1) vs forgetting last might be stale to the left of the window.",
  "edges": "Empty. All unique. All same. Spaces/symbols.",
  "follow": "At most K distinct characters (window + counts).",
  "talk": "I will state the invariant before coding: s[left..r] is always unique.",
  "sol": """function lengthOfLongestSubstring(s: string): number {
  const last = new Map<string, number>();
  let left = 0, best = 0;
  for (let r = 0; r < s.length; r++) {
    const prev = last.get(s[r]);
    if (prev !== undefined && prev >= left) left = prev + 1;
    last.set(s[r], r);
    best = Math.max(best, r - left + 1);
  }
  return best;
}"""
},
{
  "id": "char-replace", "name": "Longest Repeating Character Replacement", "diff": "medium", "pattern": "sliding-window", "topic": "strings",
  "why": "Window validity: windowLength − maxFreq ≤ k.",
  "stmt": "You may replace at most k characters. Longest substring that can become all one letter.",
  "exin": 's = "AABABBA", k = 1', "exout": "4",
  "cons": "Uppercase letters typically; n up to 10^5.",
  "hints": "You always keep the window if you can change the non-majority letters with ≤ k replacements.",
  "brute": "For each window, count and test. O(n² Σ).",
  "opt": "Expand right, track max frequency in the window. Shrink when r-left+1 − maxf > k. maxf need not decrease when shrinking (classic trick).",
  "steps": "The answer only grows; a stale maxf can only make you shrink extra, never accept an invalid larger answer.",
  "cx": "O(n) time, O(1) for 26 letters.",
  "mistakes": "Recomputing maxf every shrink (works but slower to write). Using distinct-count instead of max-freq.",
  "edges": "k=0. k ≥ n. All same.",
  "follow": "Replacement to match a given pattern.",
  "talk": "I will explain why we can let maxf be non-decreasing — interviewers listen for that.",
  "sol": """function characterReplacement(s: string, k: number): number {
  const c = Array(26).fill(0);
  let left = 0, maxf = 0, best = 0;
  for (let r = 0; r < s.length; r++) {
    maxf = Math.max(maxf, ++c[s.charCodeAt(r) - 65]);
    while (r - left + 1 - maxf > k) c[s.charCodeAt(left++) - 65]--;
    best = Math.max(best, r - left + 1);
  }
  return best;
}"""
},
{
  "id": "perm-string", "name": "Permutation in String", "diff": "medium", "pattern": "sliding-window", "topic": "strings",
  "why": "Fixed-length anagram window. Bridge to minimum window.",
  "stmt": "Does s2 contain a permutation of s1 as a contiguous substring?",
  "exin": 's1 = "ab", s2 = "eidbaooo"', "exout": "true",
  "cons": "Lowercase; lengths up to 10^4.",
  "hints": "Window of length s1.length. Compare 26-count arrays (or a mismatch counter).",
  "brute": "Sort s1, sort every window. O(n L log L).",
  "opt": "Sliding counts. When window exceeds L, remove s2[r-L].",
  "steps": "need = counts(s1). Slide, maintain matches of how many letters currently equal. When matches===26 or arrays equal, true.",
  "cx": "O(n) time, O(1) space.",
  "mistakes": "Variable window. Comparing maps by JSON each step without incremental updates.",
  "edges": "s1 longer than s2. Identical strings.",
  "follow": "Find all start indices (anagrams of a word in a string).",
  "talk": "I will implement array equality every step first (n is 10^4, 26 is fine), then mention a match counter.",
  "sol": """function checkInclusion(s1: string, s2: string): boolean {
  if (s1.length > s2.length) return false;
  const a = Array(26).fill(0), b = Array(26).fill(0);
  const idx = (ch: string) => ch.charCodeAt(0) - 97;
  for (const ch of s1) a[idx(ch)]++;
  for (let i = 0; i < s2.length; i++) {
    b[idx(s2[i])]++;
    if (i >= s1.length) b[idx(s2[i - s1.length])]--;
    if (a.every((v, j) => v === b[j])) return true;
  }
  return false;
}"""
},
{
  "id": "min-subarray", "name": "Minimum Size Subarray Sum", "diff": "medium", "pattern": "sliding-window", "topic": "arrays",
  "why": "Positive numbers make the window shrinkable. Contrast with Subarray Sum K (negatives).",
  "stmt": "Smallest contiguous subarray whose sum is at least target. Return 0 if none.",
  "exin": "target = 7, nums = [2,3,1,2,4,3]", "exout": "2",
  "cons": "Positive nums; n up to 10^5.",
  "hints": "Expand right, shrink left while sum ≥ target, track min length.",
  "brute": "All subarrays. O(n²).",
  "opt": "Window O(n). Binary search on prefix sums also O(n log n).",
  "steps": "Because all values are positive, shrinking left only decreases the sum — the validity predicate is monotone.",
  "cx": "O(n) time, O(1) space.",
  "mistakes": "Using this on arrays with negatives. Returning 0 vs Infinity.",
  "edges": "Single element ≥ target. Total sum < target.",
  "follow": "Exactly target with positives (still window, shrink to equality carefully).",
  "talk": "I will call out positivity. If they add negatives, I switch to prefix+map.",
  "sol": """function minSubArrayLen(target: number, nums: number[]): number {
  let left = 0, sum = 0, best = Infinity;
  for (let r = 0; r < nums.length; r++) {
    sum += nums[r];
    while (sum >= target) {
      best = Math.min(best, r - left + 1);
      sum -= nums[left++];
    }
  }
  return best === Infinity ? 0 : best;
}"""
},
{
  "id": "min-window", "name": "Minimum Window Substring", "diff": "hard", "pattern": "sliding-window", "topic": "strings",
  "why": "The full need/have window. Worth one Hard because it shows up in frontend-ish parsing interviews too.",
  "stmt": "Smallest substring of s that covers every character of t (including duplicates). Empty string if impossible.",
  "exin": 's = "ADOBECODEBANC", t = "ABC"', "exout": '"BANC"',
  "cons": "n up to 10^5; letters can be mixed case.",
  "hints": "need map for t. have = how many unique chars currently satisfied. Shrink while have === needSize.",
  "brute": "All windows + count. O(n² Σ).",
  "opt": "Two pointers + two maps / one map of remaining need.",
  "steps": "Expand r, decrement need[s[r]], if it hit 0 increment have. While have complete, update best, increment need[s[left]], if it became 1 decrement have, left++.",
  "cx": "O(n) time, O(Σ) space.",
  "mistakes": "Treating t as a set (duplicates). Updating best after shrinking too far.",
  "edges": "t longer than s. t empty. Multiple equal-length minima (any is fine if prompt allows).",
  "follow": "Smallest window of unique chars of t ignoring extras.",
  "talk": "I will write the have/need counters on paper first. This is a problem you should not invent live without the template.",
  "sol": """function minWindow(s: string, t: string): string {
  if (!t) return "";
  const need = new Map<string, number>();
  for (const ch of t) need.set(ch, (need.get(ch) ?? 0) + 1);
  let have = 0, needN = need.size, left = 0;
  let best = "", bestLen = Infinity;
  const win = new Map<string, number>();
  for (let r = 0; r < s.length; r++) {
    const c = s[r];
    win.set(c, (win.get(c) ?? 0) + 1);
    if (need.has(c) && win.get(c) === need.get(c)) have++;
    while (have === needN) {
      if (r - left + 1 < bestLen) {
        bestLen = r - left + 1;
        best = s.slice(left, r + 1);
      }
      const L = s[left++];
      win.set(L, (win.get(L) ?? 0) - 1);
      if (need.has(L) && (win.get(L) ?? 0) < need.get(L)!) have--;
    }
  }
  return best;
}"""
},
{
  "id": "range-sum", "name": "Range Sum Query (Immutable)", "diff": "easy", "pattern": "prefix-sum", "topic": "arrays",
  "why": "The definition of prefix sums. You will reuse it all week.",
  "stmt": "Preprocess nums so sumRange(l, r) inclusive returns nums[l]+…+nums[r] in O(1).",
  "exin": "nums = [-2,0,3,-5,2,-1], sumRange(0,2)", "exout": "1",
  "cons": "Many queries; n up to 10^4.",
  "hints": "pref[i] = sum of first i elements. sum(l,r) = pref[r+1]−pref[l].",
  "brute": "Loop each query. O(n) per query.",
  "opt": "O(n) preprocess, O(1) query.",
  "steps": "Build pref of length n+1. Guard the empty prefix 0.",
  "cx": "O(n) build, O(1) query, O(n) space.",
  "mistakes": "Inclusive/exclusive off-by-one.",
  "edges": "l===r. Whole array.",
  "follow": "Mutable array (Fenwick/segment — out of Phase 1).",
  "talk": "I will confirm inclusive bounds before writing pref[r+1]-pref[l].",
  "sol": """class NumArray {
  pref: number[];
  constructor(nums: number[]) {
    this.pref = [0];
    for (const x of nums) this.pref.push(this.pref.at(-1)! + x);
  }
  sumRange(l: number, r: number): number {
    return this.pref[r + 1] - this.pref[l];
  }
}"""
},
{
  "id": "subarray-k", "name": "Subarray Sum Equals K", "diff": "medium", "pattern": "prefix-sum", "topic": "arrays",
  "why": "Prefix frequency map. The reason sliding window fails when negatives exist.",
  "stmt": "Count contiguous subarrays whose sum is k. nums may contain negatives.",
  "exin": "nums = [1,1,1], k = 2", "exout": "2",
  "cons": "n up to 2·10^4.",
  "hints": "If pref[r] − pref[l] = k, then pref[l] = pref[r] − k. How many such l have you seen?",
  "brute": "All i,j sums. O(n²).",
  "opt": "Running prefix + Map of prefix → count. Initialize 0 → 1.",
  "steps": "For each x: pref+=x; ans += map[pref-k]; map[pref]++.",
  "cx": "O(n) time, O(n) space.",
  "mistakes": "Forgetting the zero prefix. Using a window. Storing last index instead of counts (misses multiple subarrays).",
  "edges": "k=0. All zeros. Single element.",
  "follow": "Subarray sum divisible by k (store pref % k).",
  "talk": "I will say explicitly: negatives destroy window monotonicity.",
  "sol": """function subarraySum(nums: number[], k: number): number {
  const freq = new Map<number, number>([[0, 1]]);
  let pref = 0, ans = 0;
  for (const x of nums) {
    pref += x;
    ans += freq.get(pref - k) ?? 0;
    freq.set(pref, (freq.get(pref) ?? 0) + 1);
  }
  return ans;
}"""
},
]
