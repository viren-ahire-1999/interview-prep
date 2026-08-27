from util import topic, diagram, callout, code
from drills import map_gym, python_gym, math_gym, data_gym


def field_map() -> str:
    t = topic("map-layers", "Four layers, not one buzzword",
              "rules ML deep learning generative AI map", "Lesson", f'''
  <p><b>Artificial intelligence</b> is the umbrella: machines doing tasks that look like judgment. Under it you almost always mean one of these:</p>
  <table>
    <tr><th>Layer</th><th>Idea</th><th>Use when</th></tr>
    <tr><td>Rules / search</td><td>You can write the logic</td><td>Tax brackets, password policy, “if status == paid”</td></tr>
    <tr><td>Classical ML</td><td>Learn a function from labeled rows</td><td>Churn, fraud score, spam, demand forecast</td></tr>
    <tr><td>Deep learning</td><td>Learn from raw-ish signals (pixels, waves, tokens)</td><td>Vision, speech, when features are hard to hand-write</td></tr>
    <tr><td>Generative AI / LLMs</td><td>Predict the next token; can write, extract, plan</td><td>Drafts, Q&amp;A on docs, coding assist — with eval</td></tr>
  </table>
  {diagram("""Rules ──► Classical ML ──► Deep nets ──► LLMs
cheaper, clearer          more data, less interpretability
Always start as far LEFT as the product allows.""")}
  <p>A senior move: <b>do not start with an LLM</b> if a SQL query or a classifier will do. LLMs are flexible and expensive and wrong in fluent sentences.</p>
  {callout("Unsupervised (clustering, dimensionality reduction) and reinforcement learning exist. You will meet them. Most product work is supervised or ‘LLM + your data’.")}
  ''', "topics")
    return f'''
<section class="block" id="map" data-search="Map of AI ML DL LLM" data-stype="Section">
  <p class="kicker">Vocabulary</p>
  <h2 class="section-title">Map of AI</h2>
  <p><a href="#gym-map">Jump to practice (6) →</a></p>
  {t}
  {map_gym()}
</section>
'''


def python_ai() -> str:
    t1 = topic("py-env", "A boring, repeatable environment",
               "python venv numpy pandas for AI", "Lesson", f'''
  <p>One project, one virtual environment. Pin versions. Do not train on “whatever pip installed last Tuesday.”</p>
  {code("Bash", '''python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install numpy pandas scikit-learn
# later: pip freeze > requirements.txt''')}
  <p><b>Numpy</b> is n-dimensional arrays (the workhorse under almost every trainer). <b>Pandas</b> is tables. <b>Scikit-learn</b> is classical ML with a consistent <code>fit</code> / <code>predict</code> API. PyTorch or JAX come when you write neural nets yourself.</p>
  {code("Python", '''import numpy as np
import pandas as pd

X = np.array([[1.0, 2.0],
              [3.0, 4.0]])          # shape (2, 2)
print(X.mean(axis=0))               # column means

df = pd.DataFrame({"n": [1, 2, 3], "y": [0, 1, 0]})
train = df.sample(frac=0.8, random_state=0)
test = df.drop(train.index)''')}
  {callout("<b>Shape errors are the tax.</b> Say shapes out loud: <code>(batch, features)</code> for tabular, <code>(batch, time, dim)</code> for sequences. If two arrays will not broadcast, you are not ready to debug a transformer.")}
  ''', "topics")

    t2 = topic("py-shape", "Tensors are just arrays with a story",
               "tensor batch token embedding shape", "Lesson", f'''
  <p>A <b>tensor</b> is a multi-dimensional array. The story is the axis names:</p>
  <ul>
    <li><code>B</code> — batch (how many examples at once)</li>
    <li><code>T</code> — time / tokens (how long the sequence is)</li>
    <li><code>D</code> — width of a vector (embedding size)</li>
    <li><code>C</code> — classes or channels</li>
  </ul>
  {diagram("""logits[B, T, V]  →  for each item, each token, a score per vocab word
labels[B, T]     →  the correct next token
Never add B and T by accident. That is a silent bug.""")}
  <p>In Python you check <code>array.shape</code> after every non-trivial line until it is muscle memory.</p>
  ''', "topics")

    return f'''
<section class="block" id="python" data-search="Python numpy pandas tensors AI" data-stype="Section">
  <p class="kicker">Language</p>
  <h2 class="section-title">Python for AI</h2>
  <p><a href="#gym-python">Jump to practice (6) →</a></p>
  {t1}{t2}
  {python_gym()}
</section>
'''


def math_need() -> str:
    t1 = topic("ma-vec", "Vectors and ‘close’",
               "dot product cosine similarity gradient loss", "Lesson", f'''
  <p>A vector is a list of numbers. In AI it often means “this item’s coordinates in meaning-space.”</p>
  <p>The <b>dot product</b> <code>a·b = a0*b0 + a1*b1 + …</code> is large when they point the same way. <b>Cosine similarity</b> is the dot product after both vectors are stretched to length 1 — so “long” vectors do not automatically win.</p>
  {code("Python", '''import numpy as np

def cosine(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))

print(cosine([1, 0], [0.9, 0.1]))  # close to 1
print(cosine([1, 0], [0, 1]))      # 0 — orthogonal''')}
  <p>A <b>loss</b> is a number that is <i>worse when the model is more wrong</i>. Training is “nudge parameters so loss goes down.” The <b>gradient</b> is the direction of steepest increase; we step the opposite way. You do not need to derive backprop on a whiteboard on day one — you do need this picture.</p>
  {diagram("""loss
  |     *  (start)
  |    /
  |   *
  |  *
  |_*________ parameters
step opposite the slope""")}
  <p>Probability: a model often outputs a number in [0, 1]. That is <i>not</i> a promise. <b>Calibration</b> asks whether “0.8” is right about 80% of the time. Likelihood is “how unsurprising was the data under this model.”</p>
  {callout("Linear algebra you will actually use: multiply a matrix by a vector (a layer), transpose, norms. Calculus: derivative of a sum is the sum of derivatives. That is enough to start.")}
  ''', "topics")

    return f'''
<section class="block" id="math" data-search="math for AI vectors loss gradient" data-stype="Section">
  <p class="kicker">Only what you need</p>
  <h2 class="section-title">Math you need</h2>
  <p><a href="#gym-math">Jump to practice (6) →</a></p>
  {t1}
  {math_gym()}
</section>
'''


def data_leak() -> str:
    t1 = topic("da-split", "Splits are a contract with the future",
               "train validation test leakage time split", "Lesson", f'''
  <p>You fit on <b>train</b>. You make modeling choices on <b>validation</b> (also called dev). You touch <b>test</b> once at the end — or you have used it as a second validation set and you are lying to yourself.</p>
  {diagram("""[  train  |  val  |  test ]
           choices    report
Time data: split by DATE, not by shuffle.
User data: put a user entirely on one side.""")}
  <p><b>Leakage</b> is when information that would not exist at prediction time sneaks into training. Examples:</p>
  <ul>
    <li>Using “updated_at” after the label was set.</li>
    <li>Normalizing with the test-set mean.</li>
    <li>A feature that is the label in disguise (“refunded_amount” to predict “will_refund”).</li>
    <li>Random split on a time series so tomorrow’s pattern is in today’s train.</li>
  </ul>
  {code("Python", '''# Time split — honest
df = df.sort_values("ts")
cut = int(0.8 * len(df))
train, rest = df.iloc[:cut], df.iloc[cut:]
# Then split rest into val/test the same way.

# Leak — do not
# scaler.fit(all_data); scaler.transform(train)''')}
  {callout("<b>Labels are data.</b> If humans labeled in a rush, the model will learn the rush. Sample the errors; do not only stare at a leaderboard.")}
  ''', "topics")

    t2 = topic("da-quality", "Garbage in is not a slogan — it is the bug",
               "label noise class imbalance missing data", "Lesson", f'''
  <p>Class imbalance: 99% “not fraud.” Accuracy of 99% is a model that never flags. You will fix this with the <a href="#metrics">right metric</a>, not with a fancier net first.</p>
  <p>Missing values: “unknown” is information. Blindly filling with the mean can hide a sensor that is broken.</p>
  <p>Duplicates: the same row in train and test is a free point and a production miss.</p>
  ''', "topics")

    return f'''
<section class="block" id="data" data-search="data leakage train val test" data-stype="Section">
  <p class="kicker">The real model</p>
  <h2 class="section-title">Data and leakage</h2>
  <p><a href="#gym-data">Jump to practice (6) →</a></p>
  {t1}{t2}
  {data_gym()}
</section>
'''
