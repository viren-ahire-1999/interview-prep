GYM = {
    "tp-ar-1": {
        "why": (
            "Sorting the array just to read the top two values costs O(n log n) and still "
            "fails when duplicates hide the true second place. A single left-to-right scan "
            "keeps two running bests and updates them in constant time per element."
        ),
        "steps": [
            "Initialize max_val and second to negative infinity (or null).",
            "For each x, if x beats max_val, slide old max into second, then set max_val = x.",
            "Else if x is strictly greater than second but not max_val, set second = x.",
            "After the loop, return second only if it was ever updated from its sentinel.",
        ],
        "example": (
            "nums = [3, 1, 4, 4, 2]\n"
            "scan: 3 -> max=3\n"
            "      1 -> second=1\n"
            "      4 -> second=3, max=4\n"
            "      4 -> skip (not strictly between)\n"
            "      2 -> second=3\n"
            "output: 3"
        ),
        "trap": (
            "Treating a duplicate of the maximum as the second largest is wrong — "
            "second must be a strictly smaller distinct value."
        ),
    },
    "tp-ar-2": {
        "why": (
            "Copying non-zeros into a fresh array works but wastes space and needs a copy-back pass. "
            "One read pointer and one write pointer move each non-zero exactly once, "
            "preserving order in O(n) time with O(1) extra memory."
        ),
        "steps": [
            "Set write = 0 and read = 0.",
            "While read < n, if nums[read] != 0, assign nums[write] = nums[read] and increment write.",
            "Always increment read.",
            "After the scan, fill indices write..n-1 with zeros.",
        ],
        "example": (
            "nums = [0, 1, 0, 3, 12]\n"
            "read/write trace:\n"
            "  r0: skip 0\n"
            "  r1: write[0]=1  w=1\n"
            "  r2: skip 0\n"
            "  r3: write[1]=3  w=2\n"
            "  r4: write[2]=12 w=3\n"
            "tail fill: [1,3,12,0,0,0]\n"
            "output: [1, 3, 12, 0, 0]"
        ),
        "trap": (
            "Forgetting to zero the tail after compaction leaves stale values past the write index."
        ),
    },
    "tp-ar-3": {
        "why": (
            "Re-summing from index 0 on every position repeats work and becomes O(n squared). "
            "Each prefix is just the previous prefix plus the current number, "
            "so one pass builds the entire answer."
        ),
        "steps": [
            "If mutating in place, nums[0] is already the first prefix.",
            "Set running = nums[0] (or 0 before the loop if using a new array).",
            "For i from 1 to n-1, add nums[i] to running and store at out[i].",
            "Return the array (same reference if in-place).",
        ],
        "example": (
            "nums = [1, 2, 3, 4]\n"
            "i=0: running=1  out=[1,_,_,_]\n"
            "i=1: running=3  out=[1,3,_,_]\n"
            "i=2: running=6  out=[1,3,6,_]\n"
            "i=3: running=10 out=[1,3,6,10]\n"
            "output: [1, 3, 6, 10]"
        ),
        "trap": (
            "Starting running at 0 when overwriting nums[0] in place loses the first element."
        ),
    },
    "tp-ar-4": {
        "why": (
            "Converting the digit array to a number and back breaks on large inputs and ignores "
            "the carry structure. Walking from the least significant digit mirrors grade-school "
            "addition and handles overflow with at most one extra digit."
        ),
        "steps": [
            "Start at the last index with carry = 1.",
            "While carry > 0 and index >= 0, add carry to digits[i], set carry = digit // 10, digit %= 10.",
            "Store the reduced digit and move left.",
            "If carry remains after the loop, prepend 1 to the array.",
        ],
        "example": (
            "digits = [1, 2, 9]\n"
            "i=2: 9+1=10 -> digit=0, carry=1\n"
            "i=1: 2+1=3  -> digit=3, carry=0\n"
            "done\n"
            "output: [1, 3, 0]"
        ),
        "trap": (
            "Using unshift in a loop is O(n) per call — prepend once at the end or build reversed."
        ),
    },
    "tp-ar-5": {
        "why": (
            "A hash set of seen values uses extra O(n) space. Because every value lies in 1..n, "
            "you can use the array itself as a bitmap by flipping signs at corresponding indices."
        ),
        "steps": [
            "For each x, let idx = abs(x) - 1.",
            "If nums[idx] is already negative, x is a duplicate — continue.",
            "Otherwise negate nums[idx] to mark x as present.",
            "Scan i from 0..n-1; if nums[i] > 0, push i+1 into the answer.",
        ],
        "example": (
            "nums = [4, 3, 2, 7, 8, 2, 3, 1]\n"
            "mark via negation at indices 3,2,1,6,7,...\n"
            "positive slots: index 4 (5), index 5 (6)\n"
            "output: [5, 6]"
        ),
        "trap": (
            "Using x instead of abs(x) when the array already has negative marks sends you to the wrong index."
        ),
    },
    "tp-ar-6": {
        "why": (
            "Counting all ones globally misses the longest contiguous block. "
            "Track the current streak and reset it on zero — one pass, constant extra space."
        ),
        "steps": [
            "Set best = 0 and cur = 0.",
            "For each bit, if 1 then cur += 1 else cur = 0.",
            "After each update, best = max(best, cur).",
            "Return best.",
        ],
        "example": (
            "nums = [1,1,0,1,1,1,0]\n"
            "cur: 1,2,0,1,2,3,0\n"
            "best peaks at 3\n"
            "output: 3"
        ),
        "trap": (
            "Updating best only at the end of a run misses a run that ends at the last index."
        ),
    },
    "tp-ar-7": {
        "why": (
            "Merging forward overwrites unread elements in nums1. "
            "Writing the largest remaining value from the back never clobbers data you still need."
        ),
        "steps": [
            "Set i = m-1, j = n-1, write = m+n-1.",
            "While both i and j are valid, place the larger of nums1[i] and nums2[j] at write and decrement pointers.",
            "Drain whichever side has leftovers into the front portion.",
            "nums1 is sorted in place; no return value needed beyond mutation.",
        ],
        "example": (
            "nums1=[1,2,3,0,0,0] m=3  nums2=[2,5,6] n=3\n"
            "write: 6,5,3,2,2,1\n"
            "output: [1,2,2,3,5,6]"
        ),
        "trap": (
            "Starting write at m instead of m+n-1 writes into the empty tail incorrectly."
        ),
    },
    "tp-ar-8": {
        "why": (
            "Sorting or hashing counts works but costs extra time or space. "
            "Boyer-Moore voting cancels minority votes against the majority in one pass "
            "because the true majority always outnumbers everything else combined."
        ),
        "steps": [
            "Set candidate = nums[0] and count = 1.",
            "For each x after the first, if count is 0 set candidate = x and count = 1.",
            "Else if x == candidate increment count, else decrement count.",
            "Return candidate (valid when majority is guaranteed).",
        ],
        "example": (
            "nums = [2, 2, 1, 1, 1, 2, 2]\n"
            "cand: 2->2->1->1->1->2->2  count swings but 2 survives\n"
            "output: 2"
        ),
        "trap": (
            "Without a guaranteed majority you must verify the candidate with a second pass."
        ),
    },
    "tp-ar-9": {
        "why": (
            "Counting sort with three buckets needs two passes and extra arrays. "
            "Dutch national flag partitioning swaps 0s left and 2s right while scanning once, "
            "keeping 1s in the middle automatically."
        ),
        "steps": [
            "Set lo = 0, hi = n-1, i = 0.",
            "While i <= hi, if nums[i] == 0 swap with lo and increment both lo and i.",
            "If nums[i] == 2 swap with hi and decrement hi (do not advance i).",
            "If nums[i] == 1 increment i only.",
        ],
        "example": (
            "nums = [2,0,2,1,1,0]\n"
            "lo/i/hi dance -> [0,0,1,1,2,2]\n"
            "output: [0, 0, 1, 1, 2, 2]"
        ),
        "trap": (
            "Advancing i after swapping a 2 inward can skip an unclassified value pulled from the right."
        ),
    },
    "tp-ar-10": {
        "why": (
            "Recomputing left and right sums at every index is quadratic. "
            "One total plus a running left sum gives the right side by subtraction in O(1) per index."
        ),
        "steps": [
            "Compute total = sum(nums).",
            "Set left = 0.",
            "For each i, right = total - left - nums[i].",
            "If left == right return i; else left += nums[i].",
            "Return -1 if none match.",
        ],
        "example": (
            "nums = [1, 7, 3, 6, 5, 6]\n"
            "total=28\n"
            "i=3: left=11 right=11 -> pivot 3\n"
            "output: 3"
        ),
        "trap": (
            "Including nums[i] in the left sum before checking makes the balance wrong by one element."
        ),
    },
    "tp-st-1": {
        "why": (
            "Building a reversed copy character by character uses O(n) extra space. "
            "Swapping symmetric pairs from both ends finishes in place with half as many writes."
        ),
        "steps": [
            "Set left = 0 and right = len(s) - 1.",
            "While left < right, swap s[left] and s[right].",
            "Increment left and decrement right.",
            "Stop when pointers meet or cross.",
        ],
        "example": (
            "s = ['h','e','l','l','o']\n"
            "swap 0<->4 -> ['o','e','l','l','h']\n"
            "swap 1<->3 -> ['o','l','l','e','h']\n"
            "output: olleh"
        ),
        "trap": (
            "Using <= instead of < causes the middle character to swap with itself unnecessarily on odd lengths."
        ),
    },
    "tp-st-2": {
        "why": (
            "Comparing every pair of strings blows up to O(n^2 * m). "
            "Scanning column by column against the shortest word stops at the first mismatch shared by all."
        ),
        "steps": [
            "If the array is empty return empty string.",
            "Use the first string as reference length (or min length across all).",
            "For column c from 0 while c < minLen, compare every string's char at c.",
            "On mismatch return s[0..c-1]; if all columns match return that prefix.",
        ],
        "example": (
            "strs = [\"flower\",\"flow\",\"flight\"]\n"
            "col0: f f f ok\n"
            "col1: l l l ok\n"
            "col2: o o i stop\n"
            "output: \"fl\""
        ),
        "trap": (
            "Assuming the first string is the shortest — a later string may end early and break the prefix."
        ),
    },
    "tp-st-3": {
        "why": (
            "Allocating a new compressed string ignores the in-place requirement. "
            "Read and write pointers let you collapse runs inside the same array without shifting the whole tail repeatedly."
        ),
        "steps": [
            "Set read = 0 and write = 0.",
            "While read < n, record the char and count the run length.",
            "Write the char at write, advance write.",
            "If count > 1, write each decimal digit of count.",
            "Advance read past the entire run.",
            "Return write as the new logical length.",
        ],
        "example": (
            "chars = a,a,a,b,b,c,c,c\n"
            "run a x3 -> write a,3\n"
            "run b x2 -> write b,2\n"
            "run c x3 -> write c,3\n"
            "output length 6: a3b2c3"
        ),
        "trap": (
            "Writing count digits as a single char instead of splitting '12' into '1' and '2' corrupts the array."
        ),
    },
    "tp-st-4": {
        "why": (
            "Generating all subsequences of t is exponential. "
            "Greedy matching advances through t once, consuming s only on matches — linear time."
        ),
        "steps": [
            "Set i = 0 for s and j = 0 for t.",
            "While i < len(s) and j < len(t), if s[i] == t[j] increment i.",
            "Always increment j.",
            "Return true if i reached len(s).",
        ],
        "example": (
            "s = \"abc\"  t = \"ahbgdc\"\n"
            "match a at t[1], b at t[4], c at t[5]\n"
            "i=3 -> true"
        ),
        "trap": (
            "Advancing i when characters do not match skips valid later matches in t."
        ),
    },
    "tp-st-5": {
        "why": (
            "Extracting vowels to a buffer and writing back works but needs extra space. "
            "Two pointers that skip consonants swap vowels in place from both ends."
        ),
        "steps": [
            "Define a vowel check (a,e,i,o,u case-insensitive).",
            "Set left = 0, right = len(s)-1.",
            "Advance left until a vowel; advance right until a vowel.",
            "Swap and move both inward until left >= right.",
        ],
        "example": (
            "s = \"IceCreAm\"\n"
            "swap I<->A -> \"AceCreIm\"\n"
            "swap e<->e -> no change\n"
            "swap C skipped... final \"AceCreIm\" vowels reversed"
        ),
        "trap": (
            "Forgetting case insensitivity leaves uppercase vowels untouched."
        ),
    },
    "tp-st-6": {
        "why": (
            "Trying every single deletion is O(n^2). "
            "On the first mismatch you only need to test skipping left or skipping right — "
            "if either side is palindromic, one delete fixes the whole string."
        ),
        "steps": [
            "Set left = 0 and right = len(s)-1.",
            "While left < right and s[left] == s[right], move both inward.",
            "If pointers crossed, return true (already palindrome).",
            "Check isPalindrome(s[left+1..right]) OR isPalindrome(s[left..right-1]).",
        ],
        "example": (
            "s = \"abcea\"\n"
            "mismatch at b vs e\n"
            "skip left -> \"acea\" palindrome? yes\n"
            "output: true"
        ),
        "trap": (
            "Only testing one skip direction misses cases where the right character is the extra one."
        ),
    },
    "tp-st-7": {
        "why": (
            "BigInt sidesteps the digit-by-digit lesson and may be disallowed. "
            "Adding from the least significant end with carry mirrors paper addition and scales to any length."
        ),
        "steps": [
            "Set i = len(num1)-1, j = len(num2)-1, carry = 0.",
            "While i >= 0 or j >= 0 or carry, sum digit chars plus carry.",
            "Push (sum % 10) as char, carry = sum // 10, decrement pointers.",
            "Reverse the built digit list and join into the result string.",
        ],
        "example": (
            "num1=\"11\" num2=\"123\"\n"
            "from ends: 1+3=4 carry0\n"
            "          1+2=3 carry0\n"
            "          0+1=1 carry0\n"
            "build [4,3,1] -> reverse -> \"134\""
        ),
        "trap": (
            "Forgetting carry after one pointer exhausts drops the final carry digit."
        ),
    },
    "tp-st-8": {
        "why": (
            "Checking every substring length is O(n^2). "
            "If s equals k copies of a base string, s appears inside s+s with its ends trimmed — "
            "one clever containment test finds periodicity fast."
        ),
        "steps": [
            "Let n = len(s); if n < 2 return false.",
            "Build doubled = s + s.",
            "Check whether s is a substring of doubled[1:-1].",
            "Alternatively try each period len that divides n and compare chunks.",
        ],
        "example": (
            "s = \"abab\"\n"
            "doubled = \"abababab\"\n"
            "inner = \"bababa\" contains \"abab\"? yes\n"
            "output: true"
        ),
        "trap": (
            "The slice must drop both first and last char of s+s — keeping them always matches trivially."
        ),
    },
    "tp-hm-1": {
        "why": (
            "Nested loops compare every pair and duplicate work. "
            "A set of the smaller array gives O(1) lookups while scanning the other once."
        ),
        "steps": [
            "Pick the smaller array to store in a set.",
            "Initialize result as an empty set.",
            "For each value in the larger array, if in set add to result.",
            "Return array from result set.",
        ],
        "example": (
            "nums1=[1,2,2,1] nums2=[2,2]\n"
            "set={1,2}\n"
            "scan nums2: 2 in set -> result {2}\n"
            "output: [2]"
        ),
        "trap": (
            "Pushing duplicates into the result without a set returns repeated values."
        ),
    },
    "tp-hm-2": {
        "why": (
            "Checking all pairs within distance k is O(n*k). "
            "Remembering the last index per value detects a close repeat the moment it appears."
        ),
        "steps": [
            "Create an empty map value -> lastIndex.",
            "For i from 0 to n-1, if value seen and i - last <= k return true.",
            "Update map[value] = i.",
            "Return false after the scan.",
        ],
        "example": (
            "nums=[1,2,3,1] k=3\n"
            "i=3: 1 seen at 0, 3-0=3 <= 3 -> true"
        ),
        "trap": (
            "Using strict < instead of <= misses duplicates exactly k apart."
        ),
    },
    "tp-hm-3": {
        "why": (
            "Trying all letter permutations is factorial. "
            "Two hash maps enforce a bidirectional mapping — any conflict means the transform is impossible."
        ),
        "steps": [
            "If lengths differ return false.",
            "Maintain mapS and mapT.",
            "For each pair (a,b), if a mapped to non-b or b mapped to non-a return false.",
            "Otherwise record both directions.",
        ],
        "example": (
            "s=\"egg\" t=\"add\"\n"
            "e->a, g->d consistent both ways\n"
            "output: true\n"
            "s=\"ab\" t=\"aa\" -> a maps to a and b maps to a breaks mapT"
        ),
        "trap": (
            "Checking only s->t and ignoring t->s allows two sources to collide on one target."
        ),
    },
    "tp-hm-4": {
        "why": (
            "Isomorphic strings and word patterns share the same bijection rule — "
            "only the token type changes. Two maps keep char-to-word and word-to-char consistent in one pass."
        ),
        "steps": [
            "Split s into words; if count != pattern length return false.",
            "For each index i, char = pattern[i], word = words[i].",
            "If char in mapC and mapC[char] != word return false.",
            "If word in mapW and mapW[word] != char return false.",
            "Record both mappings.",
        ],
        "example": (
            "pattern=\"abba\" words=[dog,cat,cat,dog]\n"
            "a->dog, b->cat both ways ok\n"
            "output: true"
        ),
        "trap": (
            "Matching equal-length strings without bijection fails on \"abba\" vs \"dog dog dog dog\"."
        ),
    },
    "tp-hm-5": {
        "why": (
            "Simulating forever on a cycle never terminates. "
            "A set of visited numbers detects repetition — only reaching 1 is success."
        ),
        "steps": [
            "Create seen set.",
            "While n != 1 and n not in seen, add n and replace n with sum of squared digits.",
            "If n == 1 return true.",
            "If loop detected return false.",
        ],
        "example": (
            "n=19\n"
            "19->82->68->100->1\n"
            "output: true"
        ),
        "trap": (
            "Forgetting to add n to seen before transforming lets the same value loop undetected."
        ),
    },
    "tp-hm-6": {
        "why": (
            "Pairwise anagram checks are O(n^2 * k). "
            "Grouping by a canonical key — sorted letters or a 26-count signature — "
            "buckets all anagrams in one hash map pass."
        ),
        "steps": [
            "Create map key -> list of words.",
            "For each word, compute key (sorted chars or count signature).",
            "Append word to map[key].",
            "Return all lists (values) from the map.",
        ],
        "example": (
            "words=[\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]\n"
            "keys: aet->{eat,tea,ate}, ant->{tan,nat}, abt->{bat}\n"
            "output: [[eat,tea,ate],[tan,nat],[bat]]"
        ),
        "trap": (
            "Using JS sort on numeric count arrays lexicographically merges different signatures."
        ),
    },
    "tp-hm-7": {
        "why": (
            "Sorting first is O(n log n) and misses the linear insight. "
            "Only start counting when x-1 is absent — that guarantees each run is discovered once."
        ),
        "steps": [
            "Insert all numbers into a set.",
            "For each x, if x-1 in set skip (not a run start).",
            "From run start x, walk x+1, x+2 while in set and count length.",
            "Track maximum run length.",
        ],
        "example": (
            "nums=[100,4,200,1,3,2]\n"
            "start at 1: chain 1,2,3,4 len=4\n"
            "100 and 200 are singletons\n"
            "output: 4"
        ),
        "trap": (
            "Starting a walk from every element without the x-1 check revisits the same run O(n) times."
        ),
    },
    "tp-hm-8": {
        "why": (
            "Sorting both strings hides the O(n) cancel trick. "
            "Incrementing counts for s and decrementing for t leaves exactly one surplus character."
        ),
        "steps": [
            "Build freq map from s.",
            "For each char in t decrement its count (or remove if zero).",
            "The char with count -1 or the leftover key is the answer.",
            "XOR of all codes is an equivalent one-pass trick.",
        ],
        "example": (
            "s=\"abcd\" t=\"abcde\"\n"
            "counts cancel a,b,c,d -> e remains +1\n"
            "output: \"e\""
        ),
        "trap": (
            "Returning the first char of t without canceling misses duplicate-letter cases."
        ),
    },
    "tp-hm-9": {
        "why": (
            "Comparing every pair of frequencies is quadratic in distinct values. "
            "A set of frequency counts detects duplicates instantly after one counting pass."
        ),
        "steps": [
            "Count occurrences of each value in a map.",
            "Create seenFreq set.",
            "For each frequency f, if f in seenFreq return false.",
            "Add f to seenFreq; return true if all unique.",
        ],
        "example": (
            "arr=[1,2,2,3,3,3]\n"
            "freqs: 1->1, 2->2, 3->3  set size 3 == 3 keys\n"
            "output: true"
        ),
        "trap": (
            "Comparing map size to array length instead of distinct value count gives false positives."
        ),
    },
    "tp-hm-10": {
        "why": (
            "Nested scans of magazine for each note letter are slow. "
            "One frequency table decrements as you read the note — failure on zero means impossible."
        ),
        "steps": [
            "Count every char in magazine.",
            "For each char in ransomNote, if missing or zero return false.",
            "Decrement count for that char.",
            "Return true if every note char consumed.",
        ],
        "example": (
            "ransom=\"aa\" mag=\"aab\"\n"
            "count a:2 b:1 -> use a twice ok\n"
            "output: true"
        ),
        "trap": (
            "Checking magazine length only is insufficient — wrong letters can still fail."
        ),
    },
    "tp-ll-1": {
        "why": (
            "Collecting values to rebuild the list wastes nodes. "
            "A dummy head lets you splice out matching nodes in one forward walk without losing the head."
        ),
        "steps": [
            "Create dummy pointing at head; curr = dummy.",
            "While curr.next exists, if curr.next.val == target set curr.next = curr.next.next.",
            "Else curr = curr.next.",
            "Return dummy.next.",
        ],
        "example": (
            "list: 1->2->6->3->4->5->6  target=6\n"
            "skip both 6 nodes\n"
            "output: 1->2->3->4->5"
        ),
        "trap": (
            "Advancing curr when deleting would skip the node after a removed one without checking it."
        ),
    },
    "tp-ll-2": {
        "why": (
            "Copying unique values to a new list ignores in-place rewiring. "
            "On a sorted list equal neighbors are adjacent — skip duplicates by jumping over the next node."
        ),
        "steps": [
            "Set curr = head.",
            "While curr and curr.next, if curr.val == curr.next.val set curr.next = curr.next.next.",
            "Else curr = curr.next.",
            "Return head.",
        ],
        "example": (
            "1->1->2->3->3\n"
            "compress duplicates at front and tail\n"
            "output: 1->2->3"
        ),
        "trap": (
            "Stepping curr forward after a skip can leave three-in-a-row duplicates partially trimmed."
        ),
    },
    "tp-ll-3": {
        "why": (
            "Hashing node addresses works but uses extra space. "
            "Two walkers that switch lists when one exhausts align so both have the same steps left to the merge."
        ),
        "steps": [
            "Set a = headA, b = headB.",
            "While a != b, advance a; if a null switch a to headB.",
            "Advance b; if b null switch b to headA.",
            "Return a (either intersection node or null).",
        ],
        "example": (
            "A: a1->a2->c1->c2\n"
            "B: b1->b2->b3->c1->c2\n"
            "pointers meet at c1 after switching\n"
            "output: c1"
        ),
        "trap": (
            "Comparing values instead of node identity returns the wrong node when values duplicate."
        ),
    },
    "tp-ll-4": {
        "why": (
            "Copying values to an array uses O(n) space. "
            "Slow/fast finds the middle, reversing the second half lets you compare halves with pointer walks."
        ),
        "steps": [
            "Advance slow one step and fast two until fast ends.",
            "Reverse the list starting at slow.next.",
            "Compare head with reversed head pairwise.",
            "Optional: reverse back to restore structure.",
        ],
        "example": (
            "1->2->2->1\n"
            "mid at second 2, reverse tail 1->2\n"
            "compare 1==1, 2==2 -> true"
        ),
        "trap": (
            "Reversing from slow instead of slow.next duplicates the middle node in the comparison."
        ),
    },
    "tp-ll-5": {
        "why": (
            "Converting lists to integers breaks on long numbers. "
            "Digit-by-digit with carry matches elementary addition and builds the result list forward."
        ),
        "steps": [
            "Create dummy tail; curr = dummy, carry = 0.",
            "While l1 or l2 or carry, sum digits plus carry.",
            "Append node with sum % 10, carry = sum // 10.",
            "Advance whichever lists still have nodes.",
        ],
        "example": (
            "2->4->3  plus  5->6->4  (342+465)\n"
            "7,0,8 with carries\n"
            "output: 7->0->8"
        ),
        "trap": (
            "Stopping when both lists end but carry is still 1 drops the final digit node."
        ),
    },
    "tp-ll-6": {
        "why": (
            "Swapping values is not the asked node rewire. "
            "Reversing each adjacent pair with four pointer updates preserves order of the rest in O(n)."
        ),
        "steps": [
            "Dummy before head; prev = dummy.",
            "While prev.next and prev.next.next exist, identify first and second nodes.",
            "Rewire: prev.next = second, first.next = second.next, second.next = first.",
            "Advance prev by two (to first of original pair).",
        ],
        "example": (
            "1->2->3->4\n"
            "swap 1,2 then 3,4\n"
            "output: 2->1->4->3"
        ),
        "trap": (
            "Moving prev to the second node instead of the first breaks the link to the next pair."
        ),
    },
    "tp-ll-7": {
        "why": (
            "Extracting nodes to arrays loses the O(1) space goal. "
            "Two tail pointers build odd and even chains separately, then stitch odd tail to even head."
        ),
        "steps": [
            "odd = head, even = head.next, evenHead = even.",
            "While even and even.next, append to odd and even chains alternately.",
            "odd.next = evenHead.",
            "Return head.",
        ],
        "example": (
            "1->2->3->4->5\n"
            "odd chain 1->3->5  even 2->4\n"
            "stitch -> 1->3->5->2->4"
        ),
        "trap": (
            "Using zero-based odd/even indexing instead of 1-based position grouping scrambles the order."
        ),
    },
    "tp-ll-8": {
        "why": (
            "Rotating by moving k nodes one at a time is O(n*k). "
            "Turning the list into a ring then cutting at n-k gives the new head in two linear passes."
        ),
        "steps": [
            "Count nodes n; set k %= n; if k==0 return head.",
            "Walk to tail, connect tail.next = head.",
            "Walk n-k-1 steps from old head to the new tail.",
            "newHead = tail.next, tail.next = null, return newHead.",
        ],
        "example": (
            "1->2->3->4->5 k=2 n=5\n"
            "ring, cut after node 3\n"
            "output: 4->5->1->2->3"
        ),
        "trap": (
            "Forgetting k %= n rotates way too far on large k values."
        ),
    },
    "tp-sk-1": {
        "why": (
            "Parsing with precedence rules is heavy for postfix form. "
            "Each operator immediately consumes its two most recent operands from a stack — no parentheses needed."
        ),
        "steps": [
            "Create empty stack.",
            "For each token, if number push it.",
            "On operator pop b then a (order matters for - and /).",
            "Push result of applying operator to a and b.",
            "Stack top is the final value.",
        ],
        "example": (
            "tokens: [\"2\",\"1\",\"+\",\"3\",\"*\"]\n"
            "push 2,1 -> + -> stack [3]\n"
            "push 3 -> * -> 3*3=9\n"
            "output: 9"
        ),
        "trap": (
            "Popping a then b swaps subtraction and division — pop b first, then a."
        ),
    },
    "tp-sk-2": {
        "why": (
            "For each query scanning right in nums2 is O(n*m). "
            "A decreasing stack resolves all waiting smaller values when a bigger one arrives — amortized linear."
        ),
        "steps": [
            "Initialize empty stack and map value -> next greater.",
            "Scan nums2 left to right.",
            "While stack nonempty and current > stack top, map popped value to current.",
            "Push current onto stack.",
            "Answer nums1 queries from the map, default -1.",
        ],
        "example": (
            "nums2=[4,1,2] nums1=[1,3]\n"
            "when 2 seen, 1 gets answer 2\n"
            "output: [2,-1] for [1,3]"
        ),
        "trap": (
            "Scanning nums1 inside nums2 instead of processing nums2 once recomputes answers redundantly."
        ),
    },
    "tp-sk-3": {
        "why": (
            "Simulating pairwise collisions outside a stack repeats work. "
            "Stack survivors represent the active right-moving fleet; each left mover resolves against the top until stable."
        ),
        "steps": [
            "For each asteroid, if positive push on stack.",
            "If negative, while stack top positive and top smaller, pop top.",
            "If stack empty or top negative push left mover.",
            "If equal sizes both explode (pop, do not push).",
            "Return stack as result.",
        ],
        "example": (
            "[5,10,-5]\n"
            "5 and 10 survive right; -5 kills 10? 10>5 so 10 stays, -5 dies\n"
            "output: [5,10]"
        ),
        "trap": (
            "Pushing a left mover after equal collision leaves a ghost survivor."
        ),
    },
    "tp-sk-4": {
        "why": (
            "Recursive expansion blows the stack on deep nesting. "
            "An explicit stack stores prior strings and repeat counts when '[' opens, "
            "then repeats and merges on ']'."
        ),
        "steps": [
            "Track cur string, cur number, and stack of [prevString, k].",
            "On digit append to curNum.",
            "On '[' push [cur, curNum], reset cur and curNum.",
            "On ']' pop, cur = prev + cur repeated k times.",
            "On letter append to cur.",
        ],
        "example": (
            "\"3[a2[c]]\"\n"
            "push on [, cur=\"c\" repeated 2 -> \"cc\"\n"
            "pop -> \"a\"+\"cc\" x3\n"
            "output: \"accaccacc\""
        ),
        "trap": (
            "Treating multi-digit k as a single char — accumulate digits before applying repeat."
        ),
    },
    "tp-sk-5": {
        "why": (
            "Pouring the entire in-stack to out on every dequeue makes enqueue O(n). "
            "Lazy transfer only reverses when out is empty, giving amortized O(1) per operation."
        ),
        "steps": [
            "Maintain inStack for enqueue and outStack for dequeue.",
            "Enqueue pushes onto inStack.",
            "Dequeue: if outStack empty, pop all from inStack onto outStack.",
            "Pop from outStack for dequeue/peek.",
            "Empty when both stacks empty.",
        ],
        "example": (
            "enqueue 1,2  dequeue\n"
            "in=[1,2] pour -> out=[2,1]\n"
            "dequeue -> 1\n"
            "enqueue 3 on in, dequeue pours when out empty"
        ),
        "trap": (
            "Pouring in to out even when out still has elements reverses order and breaks FIFO."
        ),
    },
    "tp-sk-6": {
        "why": (
            "Scanning all stored pings every call grows without bound. "
            "Because timestamps arrive sorted, drop expired front entries once and the queue size is the answer."
        ),
        "steps": [
            "Keep a queue of ping times.",
            "On ping(t), enqueue t.",
            "While front < t - 3000, dequeue front.",
            "Return queue length.",
        ],
        "example": (
            "ping(1) -> [1] len=1\n"
            "ping(100) -> [1,100] len=2\n"
            "ping(3001) -> drop 1 -> [100,3001] len=2\n"
            "ping(3002) -> [100,3001,3002] len=3"
        ),
        "trap": (
            "Using shift on a large array is O(n) — use a proper queue or head index."
        ),
    },
    "tp-sk-7": {
        "why": (
            "Re-summing the last k elements on every call is O(k). "
            "A fixed-size queue plus running sum adds and subtracts one value per update."
        ),
        "steps": [
            "Store queue and sum; remember capacity k.",
            "On next(val), push val and add to sum.",
            "If size exceeds k, subtract popped front.",
            "Return sum / size.",
        ],
        "example": (
            "k=3 stream: 1,10,3,5\n"
            "after 1: avg=1\n"
            "after 10: avg=5.5\n"
            "after 3: avg=14/3\n"
            "after 5: drop 1 -> (10+3+5)/3=6"
        ),
        "trap": (
            "Dividing by k instead of current queue length before the window is full skews early averages."
        ),
    },
    "tp-sk-8": {
        "why": (
            "Repeatedly scanning for adjacent pairs is O(n^2). "
            "A stack simulates collapse: equal top and current annihilate, otherwise push — one pass."
        ),
        "steps": [
            "Initialize empty stack.",
            "For each char, if stack nonempty and top == char pop top.",
            "Else push char.",
            "Join stack into result string.",
        ],
        "example": (
            "s=\"abbaca\"\n"
            "a push, b push, b pop, a pop (aa gone), c push, a pop\n"
            "stack [c]\n"
            "output: \"ca\""
        ),
        "trap": (
            "Removing pairs in a single left-to-right pass without a stack misses newly adjacent pairs after deletion."
        ),
    },
}
