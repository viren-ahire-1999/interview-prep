from util import topic, diagram, callout, code
from drills import arrays_gym, strings_gym, hash_gym


def arrays() -> str:
    t1 = topic("ar-ops", "The array is a numbered shelf",
               "JavaScript arrays from scratch", "Lesson", f'''
  <p>A JS array is an ordered list of slots <code>0..length-1</code>. Index is O(1). Insert/delete at the front is O(n) because every index after the hole must move.</p>
  {diagram("""[ 10 | 20 | 30 | 40 ]
    0    1    2    3
unshift(5) → move all right → O(n)
push(50)   → write at end   → amortized O(1)""")}
  {code("JavaScript", '''function indexOf(arr, target) {
  for (let i = 0; i < arr.length; i++) if (arr[i] === target) return i;
  return -1;
}

function reverseInPlace(arr) {
  let lo = 0, hi = arr.length - 1;
  while (lo < hi) {
    const t = arr[lo];
    arr[lo] = arr[hi];
    arr[hi] = t;
    lo++;
    hi--;
  }
  return arr;
}

function reverseRange(arr, lo, hi) {
  while (lo < hi) {
    [arr[lo], arr[hi]] = [arr[hi], arr[lo]];
    lo++;
    hi--;
  }
}

function rotateRight(arr, k) {
  const n = arr.length;
  if (!n) return arr;
  k %= n;
  reverseRange(arr, 0, n - 1);
  reverseRange(arr, 0, k - 1);
  reverseRange(arr, k, n - 1);
  return arr;
}
''')}
  <p>Two-array pattern: build <code>out</code> with <code>push</code> when you cannot mutate. In-place when the interviewer asks for O(1) extra space.</p>
  {callout("Holes: <code>arr[100] = 1</code> on a short array makes a sparse array. Interview code should stay dense. Prefer <code>push</code> over assigning far indexes.")}
  ''', "topics")

    t2 = topic("ar-drill", "Implement: rotate and remove element",
               "array rotate remove element drill", "Drill", f'''
  <p>Without looking above, write <code>rotateRight</code> and <code>removeVal(arr, val)</code> that compacts in-place (order of survivors kept) and returns the new length. Then reveal.</p>
  {code("JavaScript", '''function removeVal(arr, val) {
  let w = 0;
  for (let r = 0; r < arr.length; r++) {
    if (arr[r] !== val) arr[w++] = arr[r];
  }
  arr.length = w;
  return w;
}
''')}
  ''', "exercises")

    return f'''
<section class="block" id="arrays" data-search="Arrays JavaScript DSA" data-stype="Section">
  <p class="kicker">Foundation</p>
  <h2 class="section-title">Arrays</h2>
  <p><a href="#gym-arrays">Jump to array practice (10 problems) →</a></p>
  {t1}{t2}
  {arrays_gym()}
</section>
'''


def strings() -> str:
    t = topic("st-imm", "Strings are immutable sequences",
              "JavaScript strings palindrome two pointers", "Lesson", f'''
  <p>You cannot assign <code>s[i] = 'x'</code> and have it stick. Build a new string or use an array of characters. For interviews, convert with <code>s.split('')</code> when you need random access writes — know that is extra O(n) space.</p>
  {code("JavaScript", '''function isPalindrome(s) {
  const t = s.toLowerCase().replace(/[^a-z0-9]/g, "");
  let lo = 0, hi = t.length - 1;
  while (lo < hi) {
    if (t[lo] !== t[hi]) return false;
    lo++;
    hi--;
  }
  return true;
}

function reverseWords(s) {
  return s.trim().split(/\\s+/).reverse().join(" ");
}
''')}
  <p><b>Code units:</b> <code>s.length</code> and <code>s[i]</code> are UTF-16 units. Emoji can be two units. For interview ASCII problems this is fine; for real i18n use <code>[...s]</code> or <code>Intl</code>.</p>
  ''', "topics")
    return f'''
<section class="block" id="strings" data-search="Strings JavaScript DSA" data-stype="Section">
  <p class="kicker">Foundation</p>
  <h2 class="section-title">Strings</h2>
  <p><a href="#gym-strings">Jump to string practice (8 problems) →</a></p>
  {t}
  {strings_gym()}
</section>
'''


def hashmap() -> str:
    t1 = topic("hm-choose", "Object vs Map vs Set",
               "JavaScript Map Set object hash table", "Lesson", f'''
  <p>A hash table maps key → value in average O(1). In JS:</p>
  <table>
    <tr><th>Tool</th><th>Use when</th><th>Watch out</th></tr>
    <tr><td><code>&#123;&#125;</code></td><td>string keys, simple records</td><td>Keys coerced to string; inherited keys (<code>hasOwn</code>)</td></tr>
    <tr><td><code>Map</code></td><td>any key (including numbers, objects), insertion order</td><td>The default for interview frequency maps</td></tr>
    <tr><td><code>Set</code></td><td>presence only</td><td>Same average O(1)</td></tr>
  </table>
  {code("JavaScript", '''function twoSum(nums, target) {
  const seen = new Map(); // value → index
  for (let i = 0; i < nums.length; i++) {
    const need = target - nums[i];
    if (seen.has(need)) return [seen.get(need), i];
    seen.set(nums[i], i);
  }
  return [];
}

function firstUniqueChar(s) {
  const freq = new Map();
  for (const ch of s) freq.set(ch, (freq.get(ch) || 0) + 1);
  for (let i = 0; i < s.length; i++) if (freq.get(s[i]) === 1) return i;
  return -1;
}
''')}
  {callout("<b>Object-as-map bug.</b> <code>if (obj[key])</code> is wrong for 0 and for keys like <code>\"constructor\"</code>. Prefer <code>Map</code> or <code>Object.hasOwn</code> + explicit undefined checks.")}
  ''', "topics")

    return f'''
<section class="block" id="hash" data-search="Hash map Set JavaScript twoSum" data-stype="Section">
  <p class="kicker">The workhorse</p>
  <h2 class="section-title">Hash maps and sets</h2>
  <p><a href="#gym-hash">Jump to hash / set practice (10 problems) →</a></p>
  {t1}
  {hash_gym()}
</section>
'''
