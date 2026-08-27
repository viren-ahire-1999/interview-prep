GYM = {
    "tp-ss-1": {
        "why": (
            "The array is sorted, so every index splits the space into smaller values on the left "
            "and larger on the right. Binary search on that split finds the first position where "
            "the value is at least the target in O(log n) time instead of scanning linearly."
        ),
        "steps": [
            "Set lo = 0 and hi = len(a) as the half-open search range.",
            "While lo < hi, pick mid and check if a[mid] >= target.",
            "If true, the answer is mid or left; set hi = mid.",
            "If false, the answer is right of mid; set lo = mid + 1.",
            "Return lo as the insert or found index.",
        ],
        "example": (
            "a = [1, 3, 5, 6], target = 5\n"
            "lo=0 hi=4 -> mid=2, a[2]=5 >= 5 -> hi=2\n"
            "lo=0 hi=2 -> mid=1, a[1]=3 < 5 -> lo=2\n"
            "lo=2 hi=2 -> stop\n"
            "output: 2"
        ),
        "trap": (
            "Using lo <= hi with mid = (lo+hi)/2 can infinite-loop when hi = lo+1. "
            "Prefer lo < hi and hi = mid on the left branch."
        ),
    },
    "tp-ss-2": {
        "why": (
            "Duplicates make a single lower-bound call return some matching index, not the full span. "
            "Two bound searches—one for target and one for target+1—pin the leftmost and rightmost "
            "positions in logarithmic time without walking the duplicate run."
        ),
        "steps": [
            "Run lower bound for target to get first index.",
            "If that index is out of range or a[index] != target, return [-1, -1].",
            "Run lower bound for target + 1 to get the first index after the run.",
            "Rightmost index is that second bound minus one.",
            "Return [first, last].",
        ],
        "example": (
            "a = [5, 7, 7, 8, 8, 10], target = 8\n"
            "lower(8) -> 3\n"
            "lower(9) -> 5\n"
            "last = 5 - 1 = 4\n"
            "output: [3, 4]"
        ),
        "trap": (
            "Forgetting to verify a[first] == target after the first bound yields wrong positives "
            "when the target is missing."
        ),
    },
    "tp-ss-3": {
        "why": (
            "Between mid and mid+1 the slope tells you which half still contains a peak. "
            "If values rise to the right, some peak must exist on the right; otherwise mid or "
            "left already qualifies. Each step discards half the array."
        ),
        "steps": [
            "Set lo = 0 and hi = len(a) - 1.",
            "While lo < hi, pick mid.",
            "If a[mid] < a[mid + 1], move lo = mid + 1.",
            "Else the peak is at mid or left; set hi = mid.",
            "Return lo when the loop ends.",
        ],
        "example": (
            "a = [1, 2, 1, 3, 5, 6, 4]\n"
            "lo=0 hi=6 mid=3: a[3]=3 < a[4]=5 -> lo=4\n"
            "lo=4 hi=6 mid=5: a[5]=6 > a[6]=4 -> hi=5\n"
            "lo=4 hi=5 mid=4: a[4]=5 < a[5]=6 -> lo=5\n"
            "lo=5 hi=5 -> output index 5 (peak 6)"
        ),
        "trap": (
            "Setting hi = mid - 1 when the left side is higher can skip the only peak at mid. "
            "Use hi = mid, not mid - 1."
        ),
    },
    "tp-ss-4": {
        "why": (
            "If speed k works, any larger k also works, so feasible speeds form a prefix of [1..max]. "
            "Binary search on k finds the smallest working speed instead of trying every integer."
        ),
        "steps": [
            "Set lo = 1 and hi = max pile size.",
            "While lo < hi, test mid as a candidate speed.",
            "Compute total hours with ceil(pile / mid) for each pile.",
            "If hours <= h, try smaller: hi = mid; else lo = mid + 1.",
            "Return lo as the minimum feasible speed.",
        ],
        "example": (
            "piles = [3, 6, 7, 11], h = 8\n"
            "test k=4: ceil(3/4)+ceil(6/4)+ceil(7/4)+ceil(11/4) = 1+2+2+3 = 8 -> ok\n"
            "test k=3: 1+2+3+4 = 10 -> too slow\n"
            "output: 4"
        ),
        "trap": (
            "Using pile // k instead of ceil division underestimates hours and picks a speed that is too slow."
        ),
    },
    "tp-ss-5": {
        "why": (
            "In a rotated sorted array, one half is always fully sorted. Comparing mid to hi reveals "
            "which half contains the rotation break where the minimum lives."
        ),
        "steps": [
            "Set lo = 0 and hi = len(a) - 1.",
            "While lo < hi, pick mid.",
            "If a[mid] > a[hi], minimum is right of mid: lo = mid + 1.",
            "Else minimum is at mid or left: hi = mid.",
            "Return a[lo] as the minimum.",
        ],
        "example": (
            "a = [4, 5, 6, 7, 0, 1, 2]\n"
            "lo=0 hi=6 mid=3: a[3]=7 > a[6]=2 -> lo=4\n"
            "lo=4 hi=6 mid=5: a[5]=1 < a[6]=2 -> hi=5\n"
            "lo=4 hi=5 mid=4: a[4]=0 < a[5]=1 -> hi=4\n"
            "output: 0"
        ),
        "trap": (
            "Comparing mid to lo instead of hi breaks when the left half is the unsorted one. "
            "The mid-vs-hi test is the reliable signal."
        ),
    },
    "tp-ss-6": {
        "why": (
            "Capacity C is monotonic: if you can ship in D days with C, any larger capacity also works. "
            "Binary search on C plus a greedy day-packing check avoids simulating every capacity."
        ),
        "steps": [
            "Set lo = max weight and hi = sum of all weights.",
            "While lo < hi, test mid as ship capacity.",
            "Greedy pack: add weights to the current day until the next would exceed mid, then new day.",
            "If days needed <= D, try smaller capacity: hi = mid; else lo = mid + 1.",
            "Return lo as minimum capacity.",
        ],
        "example": (
            "weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], days = 5\n"
            "test cap=15: day1 {1..5}=15, day2 {6..8}=21? -> {6,7}=13, day3 {8,9}=17? -> {8}=8, day4 {9,10}=19? -> {9}=9, day5 {10}\n"
            "feasible at 15; search lower\n"
            "output: 15"
        ),
        "trap": (
            "Starting a new day before adding a single weight that exceeds capacity, or counting days wrong "
            "when the last batch fills exactly, gives off-by-one feasibility."
        ),
    },
    "tp-tp-1": {
        "why": (
            "Squaring preserves order for nonnegative numbers, but negatives become positive and land "
            "at the front after squaring. The two ends always hold the next largest square, so fill "
            "from the back without sorting again."
        ),
        "steps": [
            "Set left = 0, right = len(a) - 1, and write index k = len(a) - 1.",
            "Compare abs(a[left]) and abs(a[right]).",
            "Place the larger square at out[k], then move that pointer inward.",
            "Decrement k and repeat until left > right.",
            "Return the filled output array.",
        ],
        "example": (
            "a = [-4, -1, 0, 3, 10]\n"
            "compare 4 vs 10 -> out[4]=100, right=3\n"
            "compare 4 vs 3 -> out[3]=16, left=1\n"
            "compare 1 vs 3 -> out[2]=9, right=2\n"
            "compare 1 vs 0 -> out[1]=1, left=2\n"
            "out[0]=0\n"
            "output: [0, 1, 9, 16, 100]"
        ),
        "trap": (
            "Squaring then sorting works but is O(n log n). Forgetting absolute values when comparing "
            "negative ends picks the wrong largest square."
        ),
    },
    "tp-tp-2": {
        "why": (
            "Sorted order means the sum at the current ends is the extreme for that pair of choices. "
            "If the sum is too small, every pair with the left index fixed is too small, so advance left."
        ),
        "steps": [
            "Set lo = 0 and hi = len(a) - 1.",
            "Compute s = a[lo] + a[hi].",
            "If s == target, return [lo + 1, hi + 1] for 1-indexed answer.",
            "If s < target, increment lo.",
            "If s > target, decrement hi.",
        ],
        "example": (
            "a = [2, 7, 11, 15], target = 9\n"
            "2+15=17 > 9 -> hi=2\n"
            "2+11=13 > 9 -> hi=1\n"
            "2+7=9 == 9\n"
            "output: [1, 2]"
        ),
        "trap": (
            "Returning 0-indexed positions or moving both pointers on equality breaks the guaranteed "
            "single-solution contract."
        ),
    },
    "tp-tp-3": {
        "why": (
            "Fixing the smallest index i turns the rest into a sorted two-sum problem. Tracking the "
            "closest sum seen while sweeping lo and hi covers all triplets without a cubic brute force."
        ),
        "steps": [
            "Sort the array.",
            "For each index i, set lo = i + 1 and hi = n - 1.",
            "Compute sum = a[i] + a[lo] + a[hi] and update best if closer to target.",
            "If sum <= target, lo++; if sum > target, hi--.",
            "Skip duplicate values at i to avoid repeated triplets.",
        ],
        "example": (
            "nums = [-1, 2, 1, -4], target = 1\n"
            "sorted: [-4, -1, 1, 2]\n"
            "i=-4: -4+(-1)+2=-3 dist 4; -4+1+2=-1 dist 2 best\n"
            "i=-1: -1+1+2=2 dist 1 best\n"
            "output: 2"
        ),
        "trap": (
            "Updating best only on exact match misses the closest sum. Forgetting to skip duplicate i "
            "values wastes work but can also skew best if logic assumes unique i."
        ),
    },
    "tp-tp-4": {
        "why": (
            "Sorting lets you pair the lightest remaining person with the heaviest. If they fit, that "
            "uses one boat for two; otherwise the heaviest must ride alone. Greedy pairing is optimal."
        ),
        "steps": [
            "Sort people by weight ascending.",
            "Set lo = 0, hi = n - 1, boats = 0.",
            "While lo <= hi, increment boats.",
            "If people[lo] + people[hi] <= limit, lo++.",
            "Always decrement hi (heaviest is placed).",
        ],
        "example": (
            "people = [3, 2, 2, 1], limit = 3\n"
            "sorted [1, 2, 2, 3]\n"
            "boat1: 1+3 fit -> lo=1 hi=2\n"
            "boat2: 2+2 fit -> lo=2 hi=1 stop\n"
            "output: 2 boats"
        ),
        "trap": (
            "Trying to save boats by pairing medium weights while leaving heavy solo can fail; always "
            "greedily test lightest + heaviest first."
        ),
    },
    "tp-tp-5": {
        "why": (
            "After sorting, fix the longest side at k. Two sides must beat it in sum, so count pairs "
            "in [0, k) with sum > a[k]. Moving pointers inward counts valid pairs in linear total time."
        ),
        "steps": [
            "Sort nums ascending.",
            "Initialize count = 0.",
            "For k from n - 1 down to 2 (need three sides).",
            "Set lo = 0, hi = k - 1.",
            "While lo < hi: if nums[lo] + nums[hi] > nums[k], add hi - lo pairs and hi--; else lo++.",
        ],
        "example": (
            "nums = [2, 2, 3, 4]\n"
            "k=3 (side 4): lo=0 hi=2, 2+3=5>4 -> count += 2, hi=1\n"
            "k=2 (side 3): 2+2=4 not > 3\n"
            "output: 1"
        ),
        "trap": (
            "Using sum >= longest side counts degenerate triangles. The inequality must be strict: a + b > c."
        ),
    },
    "tp-tp-6": {
        "why": (
            "Both lists are sorted and disjoint, so merging overlaps is like merging timelines. Only "
            "the earlier-ending interval can be exhausted first; overlap is the intersection of the two "
            "active intervals."
        ),
        "steps": [
            "Set i = 0 and j = 0 for the two lists.",
            "While both pointers are in range, read A and B intervals.",
            "start = max(A.start, B.start), end = min(A.end, B.end).",
            "If start <= end, append [start, end].",
            "Advance the pointer whose interval ends first.",
        ],
        "example": (
            "A = [[0,2],[5,10]], B = [[1,5],[8,12]]\n"
            "overlap [0,2] & [1,5] -> [1,2]\n"
            "A advances (ends 2 vs 5)\n"
            "overlap [5,10] & [1,5] -> [5,5]\n"
            "output: [[1,2],[5,5],[8,10]] after next steps"
        ),
        "trap": (
            "Advancing the interval that ends later can skip overlaps. Always move the pointer with the "
            "smaller end coordinate."
        ),
    },
    "tp-wd-1": {
        "why": (
            "Every length-k window shares k-1 elements with its neighbor, so update the sum by adding "
            "the new right element and subtracting the falling left one. One pass finds the max without "
            "re-summing each window."
        ),
        "steps": [
            "Sum the first k elements into window.",
            "Set best = window.",
            "Slide: add nums[right], subtract nums[right - k].",
            "Update best after each slide.",
            "Return best / k as the maximum average.",
        ],
        "example": (
            "nums = [1, 12, -5, -6, 50, 3], k = 4\n"
            "window0: 1+12-5-6 = 2\n"
            "slide: -6 out, 50 in -> 2-(-6)+50 = 58 best\n"
            "slide: -5 out, 3 in -> 58-12+3 = 49\n"
            "output: 58/4 = 14.5"
        ),
        "trap": (
            "Dividing to average inside the loop can introduce float noise; track max sum as integers "
            "and divide once at the end."
        ),
    },
    "tp-wd-2": {
        "why": (
            "The longest valid segment with at most k zeros is a sliding window where you expand until "
            "invalid then shrink from the left. Zero count tracks how many flips the window needs."
        ),
        "steps": [
            "Set left = 0, zeros = 0, best = 0.",
            "Expand right across the array.",
            "If nums[right] == 0, increment zeros.",
            "While zeros > k, shrink from left decrementing zeros when leaving a 0.",
            "Update best with right - left + 1.",
        ],
        "example": (
            "nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2\n"
            "grow to ... right=5 zeros=3 -> shrink until zeros=2 at left=2\n"
            "window [1,1,1,0,0] length 5, later window length 6\n"
            "output: 6"
        ),
        "trap": (
            "Shrinking while zeros >= k instead of > k stops one step early. Only shrink when zeros "
            "exceeds k."
        ),
    },
    "tp-wd-3": {
        "why": (
            "Anagrams share the same letter counts. A fixed-length window sliding over s can update "
            "counts in O(1) and detect a full match without resorting each slice."
        ),
        "steps": [
            "Build need counts for p and match = number of letters fully satisfied (0..26).",
            "Fill the first len(p) window in s and update match.",
            "If match == 26, record start index 0.",
            "Slide: add s[right], remove s[left], adjust match.",
            "Record each start where match == 26.",
        ],
        "example": (
            "s = \"cbaebabacd\", p = \"abc\"\n"
            "window \"cba\" at 0 matches\n"
            "slide to \"bae\" ... \"eab\" at 3 matches\n"
            "output: [0, 3]"
        ),
        "trap": (
            "Comparing full frequency maps each slide is O(26) but easy to get wrong; track match only "
            "when a letter's count hits need or leaves need."
        ),
    },
    "tp-wd-4": {
        "why": (
            "Expand until all required characters are covered, then shrink from the left to minimize "
            "length while coverage holds. Missing count tells you when the window is valid."
        ),
        "steps": [
            "Build need map for t and missing = distinct required chars not yet satisfied.",
            "Expand right, decrement missing when a needed char hits zero surplus.",
            "When missing == 0, update best and shrink left while still valid.",
            "On shrink, increment missing if a needed char becomes deficient.",
            "Return best window or empty string.",
        ],
        "example": (
            "s = \"ADOBECODEBANC\", t = \"ABC\"\n"
            "grow until A,B,C covered at \"ADOBEC\"\n"
            "shrink: \"DOBEC\" still covers -> \"BEC\" ... best \"BANC\"\n"
            "output: \"BANC\""
        ),
        "trap": (
            "Shrinking before missing hits zero, or using unique char count instead of duplicate-aware "
            "need counts, drops required letters."
        ),
    },
    "tp-wd-5": {
        "why": (
            "With positive numbers, extending right only increases product and shrinking left only "
            "decreases it. For each right, the valid left endpoints form a contiguous block."
        ),
        "steps": [
            "Set left = 0 and product = 1.",
            "For each right, multiply product by nums[right].",
            "While product >= k and left <= right, divide by nums[left] and left++.",
            "Add right - left + 1 valid subarrays ending at right.",
            "Sum those counts for the answer.",
        ],
        "example": (
            "nums = [10, 5, 2, 6], k = 100\n"
            "r=0: product 10, add 1\n"
            "r=1: 50, add 2 ([5],[10,5])\n"
            "r=2: shrink from 100, add 1\n"
            "output: 8"
        ),
        "trap": (
            "Counting only length-1 subarrays or resetting left to 0 each right misses the (r-left+1) "
            "formula for all valid starts."
        ),
    },
    "tp-wd-6": {
        "why": (
            "Two baskets means at most two distinct types in the window. A frequency map tracks types "
            "while you expand and shrink, giving linear time instead of checking every subarray."
        ),
        "steps": [
            "Set left = 0 and freq map empty.",
            "Expand right, increment freq[nums[right]].",
            "While map has more than 2 keys, decrement freq[nums[left]] and remove key if zero, left++.",
            "Track max window length.",
            "Return best length.",
        ],
        "example": (
            "fruits = [1,2,1,2,3]\n"
            "window grows to [1,2,1,2] len 4\n"
            "add 3 -> three types, shrink until {2,3} len 2\n"
            "best stays 4\n"
            "output: 4"
        ),
        "trap": (
            "Checking distinct count before incrementing the new fruit, or forgetting to delete keys "
            "at count zero, keeps stale types in the map."
        ),
    },
    "tp-bt-1": {
        "why": (
            "Sorting brings duplicates together so you can skip equivalent branches. Using each index "
            "at most once is enforced by always advancing i+1 on recursion, not by reusing the same depth."
        ),
        "steps": [
            "Sort candidates ascending.",
            "Backtrack with start index, path, and remaining target.",
            "If target == 0, save path copy.",
            "Loop i from start; skip nums[i] == nums[i-1] when i > start.",
            "Include nums[i], recurse with i+1, then backtrack pop.",
        ],
        "example": (
            "candidates = [10,1,2,7,6,1,5], target = 8\n"
            "pick 1,7 -> [1,7]\n"
            "pick 1,2,5 -> [1,2,5]\n"
            "pick 2,6 -> [2,6]\n"
            "output: [[1,7],[1,2,5],[2,6]]"
        ),
        "trap": (
            "Skipping duplicates at i > 0 instead of i > start removes valid combos that use an earlier "
            "copy of the duplicate value."
        ),
    },
    "tp-bt-2": {
        "why": (
            "Every partition picks a first palindrome prefix and recurses on the suffix. You only branch "
            "on valid palindromes, so dead ends are cut early instead of generating all cuts."
        ),
        "steps": [
            "Define dfs(start, path) on substring s.",
            "If start == len(s), append path copy to results.",
            "For end from start to n-1, check if s[start:end+1] is palindrome.",
            "If yes, push that piece, dfs(end+1), pop.",
            "Precompute palindrome table optionally to speed checks.",
        ],
        "example": (
            "s = \"aab\"\n"
            "cut \"a\" -> recurse on \"ab\"\n"
            "  cut \"a\"|\"b\" -> [\"a\",\"a\",\"b\"]\n"
            "cut \"aa\" -> recurse on \"b\" -> [\"aa\",\"b\"]\n"
            "output: [[\"a\",\"a\",\"b\"],[\"aa\",\"b\"]]"
        ),
        "trap": (
            "Forgetting to backtrack (pop) after recursion reuses stale path segments in later branches."
        ),
    },
    "tp-bt-3": {
        "why": (
            "An IPv4 address has exactly four dot-separated parts with tight digit rules. Trying part "
            "lengths 1–3 at each dot position explores only valid splits instead of all substring cuts."
        ),
        "steps": [
            "dfs(index, parts) where parts counts segments built so far.",
            "If parts == 4, accept only if index reached end of string.",
            "Try segment lengths 1, 2, 3 from index.",
            "Reject leading zeros (except lone \"0\") and values above 255.",
            "Push valid segment, recurse, pop.",
        ],
        "example": (
            "s = \"25525511135\"\n"
            "255.255.11.135 valid\n"
            "255.255.111.35 valid\n"
            "output: [\"255.255.11.135\",\"255.255.111.35\"]"
        ),
        "trap": (
            "Allowing a fourth part when characters remain, or accepting \"01\" as a segment, produces "
            "invalid IPs that look close to correct."
        ),
    },
    "tp-bt-4": {
        "why": (
            "Digits never change, so they create a single branch. Letters fork into lower and upper, "
            "doubling possibilities per letter without storing all strings until the leaves."
        ),
        "steps": [
            "Track current index in s and mutable char array.",
            "If index == n, append joined string to results.",
            "If s[index] is digit, keep it and recurse index+1.",
            "If letter, set lower branch, recurse, set upper branch, recurse.",
            "Return collected results.",
        ],
        "example": (
            "s = \"a1b2\"\n"
            "branch a/A at 0, keep 1, branch b/B at 2, keep 2\n"
            "output: [\"a1b2\",\"a1B2\",\"A1b2\",\"A1B2\"]"
        ),
        "trap": (
            "Toggling case on digits or rebuilding the whole string on every call instead of in-place "
            "array backtracking wastes time and can corrupt digits."
        ),
    },
    "tp-bt-5": {
        "why": (
            "Placing one queen per row avoids row conflicts by construction. Tracking columns and both "
            "diagonal families with sets makes each placement check O(1) instead of scanning the board."
        ),
        "steps": [
            "Place queens row by row from 0.",
            "For each column try in current row, skip if col or diagonal busy.",
            "Mark col, r-c, and r+c as used; place 'Q'.",
            "Recurse to next row; on last row save board snapshot.",
            "Backtrack: clear cell and unmark sets.",
        ],
        "example": (
            "n = 4\n"
            "row0 col1, row1 col3, row2 col0, row3 col2\n"
            "board .Q.. / ...Q / Q... / ..Q.\n"
            "output: 2 distinct boards"
        ),
        "trap": (
            "Checking only column and one diagonal direction misses anti-diagonal conflicts. Track both "
            "r-c and r+c; path compression is for union-find, not needed here but col/diag sets are."
        ),
    },
    "tp-bt-6": {
        "why": (
            "Duplicates create identical subsets if you take/skip independently at each copy. Sorting plus "
            "skipping the whole duplicate run at the same tree level keeps only unique subsets."
        ),
        "steps": [
            "Sort nums.",
            "Backtrack(index, path): at each step choose take or skip current.",
            "On skip at index i, jump i to the end of equal values.",
            "On take, push nums[i], recurse i+1, pop.",
            "Record path at every node including empty.",
        ],
        "example": (
            "nums = [1,2,2]\n"
            "skip first 2, take second 2 separately from take-first path\n"
            "output: [[],[1],[1,2],[1,2,2],[2],[2,2]]"
        ),
        "trap": (
            "Deduping with a global set of serialized subsets works but hides the skip-run rule; skipping "
            "only when i > 0 instead of when not taking lets duplicate branches survive."
        ),
    },
    "tp-dp-1": {
        "why": (
            "The circle forbids taking both first and last house. The optimum either skips the first or "
            "skips the last, reducing to two linear house-robber runs whose max is the circle answer."
        ),
        "steps": [
            "If n == 1, return nums[0].",
            "Define rob(lo, hi) with prev and curr rolling max.",
            "Rob linear on indices [0, n-2] excluding last.",
            "Rob linear on indices [1, n-1] excluding first.",
            "Return max of the two linear results.",
        ],
        "example": (
            "nums = [2, 3, 2]\n"
            "linear [0,1]: max(2,3)=3\n"
            "linear [1,2]: max(3,2)=3\n"
            "output: 3"
        ),
        "trap": (
            "Running one linear pass on the full array allows robbing both ends. Handle n=1 separately "
            "before splitting."
        ),
    },
    "tp-dp-2": {
        "why": (
            "Each position either starts a one-digit letter or pairs with the previous digit for a two-digit "
            "letter. DP counts ways to the prefix without enumerating every string."
        ),
        "steps": [
            "dp[0] = 1 empty prefix.",
            "For i from 1 to n, start dp[i] = 0.",
            "If s[i-1] != '0', add dp[i-1] for single-digit decode.",
            "If s[i-2:i] is between 10 and 26, add dp[i-2].",
            "Return dp[n].",
        ],
        "example": (
            "s = \"226\"\n"
            "dp: 1 -> 1 (2) -> 2 (2|26) -> 3 (6|26)\n"
            "output: 3 ways"
        ),
        "trap": (
            "Treating '0' as a solo digit or allowing '06' as valid adds phantom ways and breaks leading-zero rules."
        ),
    },
    "tp-dp-3": {
        "why": (
            "Each cell only arrives from above or left, so optimal substructure holds on a grid. Fill row "
            "by row reusing one row of DP instead of exploring every path exponentially."
        ),
        "steps": [
            "Clone grid or use dp table same size.",
            "First row: cumulative sum from left.",
            "First column: cumulative sum from top.",
            "For each cell (i,j): dp[i][j] += min(dp[i-1][j], dp[i][j-1]).",
            "Answer is dp[m-1][n-1].",
        ],
        "example": (
            "grid = [[1,3,1],[1,5,1],[4,2,1]]\n"
            "row0: 1,4,5\n"
            "col0: 1,2,6\n"
            "cell(1,1): 1+min(4,2)=3 ... bottom-right 7\n"
            "output: 7"
        ),
        "trap": (
            "Adding grid[i][j] after taking min, or overwriting the first row/col without seeding grid[0][0], "
            "double-counts or drops the start cost."
        ),
    },
    "tp-dp-4": {
        "why": (
            "Equal split means some subset sums to total/2. That is 0/1 knapsack: each number used once "
            "to fill a boolean reachability array instead of trying all 2^n subsets."
        ),
        "steps": [
            "Sum nums; if odd return false.",
            "Let target = sum / 2.",
            "dp[0] = true; for each num, walk sums from target down to num.",
            "If dp[s - num] true, set dp[s] true.",
            "Return dp[target].",
        ],
        "example": (
            "nums = [1, 5, 11, 5]\n"
            "sum=22 target=11\n"
            "can pick 1+5+5=11\n"
            "output: true"
        ),
        "trap": (
            "Looping sums upward lets the same coin be reused like unbounded knapsack. Inner loop must go "
            "backward for 0/1 use-once."
        ),
    },
    "tp-dp-5": {
        "why": (
            "Every palindrome has a center. Expanding outward from each center finds the longest palindrome "
            "in O(n^2) without a full n^2 DP table, since mirroring checks are local."
        ),
        "steps": [
            "Track best start and length.",
            "For each index i, expand odd center at i.",
            "Expand even center between i and i+1.",
            "While in bounds and chars match, expand lo/hi.",
            "Update best when new length exceeds old.",
        ],
        "example": (
            "s = \"babad\"\n"
            "center at 1 ('a'): expands \"aba\" len 3\n"
            "center at 2: \"bab\" len 3\n"
            "output: \"bab\" or \"aba\""
        ),
        "trap": (
            "Only checking odd centers misses even-length palindromes like \"bb\". Always run both expansions."
        ),
    },
    "tp-dp-6": {
        "why": (
            "You only need the farthest index reachable so far. If the current index is within farthest, "
            "you can jump forward; greedy tracking avoids recomputing reach from every cell."
        ),
        "steps": [
            "Set farthest = 0.",
            "For i from 0 to n-1, if i > farthest return false.",
            "Update farthest = max(farthest, i + nums[i]).",
            "Early true if farthest >= n - 1.",
            "After loop return farthest >= n - 1.",
        ],
        "example": (
            "nums = [2, 3, 1, 1, 4]\n"
            "i=0 farthest=2\n"
            "i=1 farthest=4\n"
            "i=2 farthest=4\n"
            "i=3 farthest=4 >= last index\n"
            "output: true"
        ),
        "trap": (
            "Returning true at i == n-1 without checking whether that index was reachable (i <= farthest) "
            "accepts impossible games."
        ),
    },
    "tp-dp-7": {
        "why": (
            "Counting combinations not permutations means coin order should not double-count. Processing "
            "coins in an outer loop and amounts ascending lets each coin contribute once per combination "
            "layer."
        ),
        "steps": [
            "dp[0] = 1 way to make zero.",
            "For each coin c in coins.",
            "For amount from c to target upward.",
            "dp[amount] += dp[amount - c].",
            "Return dp[target].",
        ],
        "example": (
            "amount = 5, coins = [1, 2, 5]\n"
            "after 1s: dp[5]=1\n"
            "after 2s: dp[5]=2\n"
            "after 5: dp[5]=4\n"
            "output: 4"
        ),
        "trap": (
            "Swapping loops (amount outer, coin inner) counts permutations like [1,2] and [2,1] separately."
        ),
    },
    "tp-dp-8": {
        "why": (
            "Same grid DP as unique paths, but walls block flow. A wall cell stays at zero paths and stops "
            "propagation along its row and column beyond it."
        ),
        "steps": [
            "If start or end is wall, return 0.",
            "Initialize first row until first wall, then zeros.",
            "Initialize first column until first wall, then zeros.",
            "For each open cell: dp[i][j] = dp[i-1][j] + dp[i][j-1].",
            "Wall cells remain 0.",
        ],
        "example": (
            "grid = [[0,0,0],[0,1,0],[0,0,0]]\n"
            "wall at (1,1) blocks through middle\n"
            "paths: down-right-around = 2\n"
            "output: 2"
        ),
        "trap": (
            "Treating wall as 1 or adding paths through walls inflates counts. First row/col must zero out "
            "after the first obstacle."
        ),
    },
    "tp-ex-1": {
        "why": (
            "Roots are prefixes, so a trie lets you stop at the shortest marked root while scanning each "
            "word character by character instead of comparing every dictionary word."
        ),
        "steps": [
            "Insert each dictionary root into a trie with end markers.",
            "Split sentence into words.",
            "Walk trie chars for each word until mismatch or end marker.",
            "Replace with path prefix if a root was found; else keep word.",
            "Join words back into the sentence string.",
        ],
        "example": (
            "dict = [\"cat\",\"bat\",\"rat\"], sentence = \"the cattle was rattled\"\n"
            "cattle: 'cat' is shortest root -> cat\n"
            "rattled: 'rat' -> rat\n"
            "output: \"the cat was rat\""
        ),
        "trap": (
            "Storing full words at nodes without stopping at the first end marker can replace with a longer "
            "non-root prefix."
        ),
    },
    "tp-ex-2": {
        "why": (
            "Shared emails must land in one connected component. Union-find merges accounts by email identity "
            "without building explicit graphs for every pair."
        ),
        "steps": [
            "Map each email to a unique id; union all emails in the same account row.",
            "For each id, find root with path compression.",
            "Group emails by root id.",
            "Attach the account name from any row containing that email.",
            "Sort each email list and format output.",
        ],
        "example": (
            "accounts = [[\"John\",\"j@x\",\"d@x\"],[\"John\",\"d@x\",\"d@y\"]]\n"
            "d@x links both rows -> one component {j@x,d@x,d@y}\n"
            "output: [[\"John\",\"d@x\",\"d@y\",\"j@x\"]]"
        ),
        "trap": (
            "Union-find without path compression and rank can degrade on long chains; also key emails by "
            "root, not by original row index."
        ),
    },
    "tp-ex-3": {
        "why": (
            "A tree on n nodes has exactly n-1 edges; the extra edge closes a cycle. Union-find rejects the "
            "first edge whose endpoints were already connected."
        ),
        "steps": [
            "Initialize parent[i] = i for 1..n.",
            "Process edges in given order.",
            "Find roots of u and v with compression.",
            "If roots equal, return this edge as redundant.",
            "Else union the roots and continue.",
        ],
        "example": (
            "edges = [[1,2],[1,3],[2,3]]\n"
            "union 1-2, union 1-3\n"
            "2-3 already same component\n"
            "output: [2, 3]"
        ),
        "trap": (
            "Union by size without find compression still works but is slower; returning the last edge in "
            "the cycle instead of the first given redundant edge fails the problem."
        ),
    },
    "tp-ex-4": {
        "why": (
            "Prefix sums turn any range sum into two lookups. Building pref once makes each sumRange O(1) "
            "after O(n) preprocessing instead of re-summing l..r per query."
        ),
        "steps": [
            "Build pref with pref[0] = 0.",
            "For i from 0 to n-1: pref[i+1] = pref[i] + nums[i].",
            "sumRange(l, r) returns pref[r+1] - pref[l].",
            "Store pref on the object for reuse.",
            "No mutation of nums assumed.",
        ],
        "example": (
            "nums = [-2, 0, 3, -5, 2, -1]\n"
            "pref = [0,-2,-2,1,-4,-2,-3]\n"
            "sumRange(0,2) = pref[3]-pref[0] = 1-0 = 1\n"
            "output: 1"
        ),
        "trap": (
            "Off-by-one on r+1 or using pref[r]-pref[l-1] breaks inclusive range queries. Size pref to n+1."
        ),
    },
    "tp-ex-5": {
        "why": (
            "A decreasing stack keeps candidates waiting for a bigger future value. Walking 2n indices "
            "simulates the circular wrap so elements at the end can see larger values from the start."
        ),
        "steps": [
            "Initialize result with -1 and empty stack of indices.",
            "Loop i from 0 to 2n - 1.",
            "While stack nonempty and nums[i % n] > nums[stack.top], set result[pop] = nums[i % n].",
            "If i < n, push i onto stack.",
            "Return result.",
        ],
        "example": (
            "nums = [1, 2, 1]\n"
            "i=0 push 0; i=1 pop 0 result[0]=2 push 1\n"
            "wrap: i=3 value 1 no pop; i=4 value 2 pop 1 result[1]=2\n"
            "output: [2, -1, 2]"
        ),
        "trap": (
            "Pushing indices during the second lap duplicates work and corrupts answers. Only push when i < n."
        ),
    },
    "tp-ex-6": {
        "why": (
            "Lexicographic top-3 prefixes are the first three sorted products with that prefix. Sort once, "
            "then lower-bound each search prefix and scan forward while matches hold."
        ),
        "steps": [
            "Sort products lexicographically.",
            "For each prefix length of searchWord.",
            "Binary search lower bound for prefix in products.",
            "Collect up to 3 products starting there that still start with prefix.",
            "Append list to answer; stop early if prefix not found.",
        ],
        "example": (
            "products = [\"mobile\",\"mouse\",\"moneypot\",\"monitor\"], searchWord = \"mouse\"\n"
            "m -> mobile, moneypot, monitor\n"
            "mo -> mobile, monitor, mouse\n"
            "mou -> mouse\n"
            "mous -> mouse\n"
            "mouse -> mouse"
        ),
        "trap": (
            "Taking any three matches without lex order, or not stopping the forward scan when prefix breaks, "
            "returns wrong suggestions."
        ),
    },
    "tp-ex-7": {
        "why": (
            "XOR prefix lets range xor cancel overlapping parts because x xor x is zero. One prefix array "
            "answers all queries in O(1) each."
        ),
        "steps": [
            "Build xorPref[0] = 0.",
            "xorPref[i+1] = xorPref[i] ^ nums[i].",
            "For query [l, r], answer xorPref[r+1] ^ xorPref[l].",
            "Return array of answers.",
            "Works because middle prefix xors twice and vanishes.",
        ],
        "example": (
            "nums = [1, 3, 4, 8]\n"
            "xorPref = [0, 1, 2, 6, 14]\n"
            "query [0,1]: xorPref[2] ^ xorPref[0] = 2 ^ 0 = 2\n"
            "(equals 1 xor 3)\n"
            "output: 2"
        ),
        "trap": (
            "Using pref[r] ^ pref[l] instead of pref[r+1] ^ pref[l] drops the last element or double-xors wrong."
        ),
    },
    "tp-ex-8": {
        "why": (
            "Cars cannot pass, so a faster car behind a slower one forms a fleet with the slower arrival "
            "time. Processing from target-nearest downward merges stacks by comparing arrival times."
        ),
        "steps": [
            "Pair position with speed; sort by position descending.",
            "Track fleet arrival time as max time seen so far.",
            "For each car compute time = (target - pos) / speed.",
            "If time > fleet time, push new fleet count and update fleet time.",
            "Return fleet count.",
        ],
        "example": (
            "target = 12, position = [10, 8, 0], speed = [2, 4, 1]\n"
            "sort desc: (10,2) time=1, (8,4) time=1 -> one fleet, fleetTime=1\n"
            "(0,1) time = 12/1 = 12 > 1 -> new fleet\n"
            "output: 2"
        ),
        "trap": (
            "Sorting ascending processes cars in wrong catch-up order. A later car with a larger arrival "
            "time starts a new fleet; equal times merge."
        ),
    },
}
