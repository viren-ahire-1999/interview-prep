from util import topic, diagram, callout, code
from drills import supervised_gym, models_gym, metrics_gym, features_gym


def supervised() -> str:
    t = topic("su-loop", "Learn a function from examples",
              "supervised learning overfit underfit", "Lesson", f'''
  <p><b>Supervised learning:</b> you have inputs <code>X</code> and a target <code>y</code>. The model learns a function <code>f(X) ≈ y</code>. Classification: <code>y</code> is a category. Regression: <code>y</code> is a number.</p>
  {diagram("""for many steps:
  predict ŷ = f(x)
  loss = how wrong(ŷ, y)
  nudge f so loss drops
stop when val loss stops improving""")}
  <p><b>Underfit:</b> too simple — train and val both bad. <b>Overfit:</b> memorizes train — train great, val poor. The validation curve is how you see it.</p>
  {code("Python", '''from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
clf = LogisticRegression(max_iter=1000)
clf.fit(Xtr, ytr)
print(classification_report(yte, clf.predict(Xte)))''')}
  <p>Unsupervised: no <code>y</code> (cluster customers). Self-supervised: invent <code>y</code> from the input (mask a word, predict it) — that is how LLMs pretrain.</p>
  ''', "topics")
    return f'''
<section class="block" id="supervised" data-search="supervised learning overfit" data-stype="Section">
  <p class="kicker">The loop</p>
  <h2 class="section-title">Supervised learning</h2>
  <p><a href="#gym-supervised">Jump to practice (6) →</a></p>
  {t}
  {supervised_gym()}
</section>
'''


def models() -> str:
    t = topic("mo-pick", "A small menu, used well",
              "logistic regression trees random forest gradient boosting", "Lesson", f'''
  <p>You do not need twenty algorithms. You need to know when the first four fail.</p>
  <table>
    <tr><th>Model</th><th>Good at</th><th>Fails when</th></tr>
    <tr><td>Linear / logistic</td><td>Baselines, explainable weights, lots of rows</td><td>Interactions and curves unless you add features</td></tr>
    <tr><td>Decision tree</td><td>Non-linear rules you can draw</td><td>Unstable; overfits deep trees</td></tr>
    <tr><td>Random forest</td><td>Strong tabular default</td><td>Less pretty explanations; heavier</td></tr>
    <tr><td>Gradient boosting (XGBoost / LightGBM)</td><td>Many Kaggle-style tabular wins</td><td>Needs care on leakage and tuning</td></tr>
    <tr><td>k-NN / naive Bayes</td><td>Simple baselines, text bag-of-words</td><td>Scale or strong feature dependence</td></tr>
  </table>
  {callout("<b>Default move.</b> Logistic or a small forest on a clean split. If that is close to the product bar, stop. A neural net on 800 rows is theater.")}
  <p>Logistic regression outputs a score you can threshold. The weights (after scaling) are a story: “this feature pushes toward yes.” Trees partition the space: “if amount &gt; 500 and country = X.”</p>
  {code("Python", '''from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("scale", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
])
pipe.fit(X_train, y_train)''')}
  ''', "topics")
    return f'''
<section class="block" id="models" data-search="logistic trees forest boosting" data-stype="Section">
  <p class="kicker">Classical tools</p>
  <h2 class="section-title">Core models</h2>
  <p><a href="#gym-models">Jump to practice (6) →</a></p>
  {t}
  {models_gym()}
</section>
'''


def metrics() -> str:
    t = topic("me-cost", "A metric is a product decision",
              "precision recall F1 AUC accuracy calibration", "Lesson", f'''
  <p><b>Accuracy</b> is “how often was the label right.” It is a lie when classes are rare or when errors have different costs.</p>
  <ul>
    <li><b>Precision</b> — of the items you flagged, how many deserved it. Low precision = false alarms (user fatigue, wasted reviews).</li>
    <li><b>Recall</b> (sensitivity) — of the items that deserved a flag, how many you caught. Low recall = missed fraud / missed cancer.</li>
    <li><b>F1</b> — harmonic mean of the two when you need a single number.</li>
    <li><b>ROC-AUC</b> — ranking quality across thresholds. Useful, not a substitute for a chosen threshold.</li>
    <li><b>PR-AUC</b> — better story under imbalance than ROC-AUC.</li>
    <li><b>Calibration</b> — do predicted probabilities match frequencies?</li>
    <li>Regression: <b>MAE</b> (typical error), <b>RMSE</b> (punishes big misses).</li>
  </ul>
  {diagram("""Actual yes     Actual no
Pred yes     TP            FP     ← precision = TP/(TP+FP)
Pred no      FN            TN     ← recall    = TP/(TP+FN)""")}
  <p>Pick the metric from the <b>cost of FP vs FN</b>. Spam filter: FP hides a real email (painful). Cancer screen: FN is worse. Then pick a threshold on the validation set for that cost — do not leave it at 0.5 by habit.</p>
  {callout("For generation (LLMs) these labels do not apply cleanly. You still need a number — see Evaluation. Do not report ‘the model is 90% accurate’ on a chatbot without defining a unit.")}
  ''', "topics")
    return f'''
<section class="block" id="metrics" data-search="precision recall F1 AUC metrics" data-stype="Section">
  <p class="kicker">Scoreboard</p>
  <h2 class="section-title">Metrics</h2>
  <p><a href="#gym-metrics">Jump to practice (6) →</a></p>
  {t}
  {metrics_gym()}
</section>
'''


def features() -> str:
    t = topic("fe-reg", "Features carry the leak; regularize the ego",
              "feature engineering scaling one-hot L1 L2", "Lesson", f'''
  <p>Models see numbers. You decide which numbers. Scaling (standardize / min-max) helps linear models and neural nets; trees often do not need it. One-hot encode categoricals with a small vocabulary; hashing or embeddings when the vocabulary is huge.</p>
  <p><b>Target leakage features:</b> anything computed with the label or with post-outcome events. If you would not have the field at 10:00 when you must predict 10:01, drop it.</p>
  <p><b>Regularization</b> punishes complexity so the model cannot rely on a crazy weight.</p>
  <ul>
    <li>L2 (ridge): shrinks weights smoothly. Default friend.</li>
    <li>L1 (lasso): can zero weights — a crude feature selector.</li>
    <li>Early stopping: stop when val loss rises (boosting and nets).</li>
    <li>Dropout: in nets, randomly ignore units during train — a form of ensemble.</li>
  </ul>
  {code("Python", '''from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

pre = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
])''')}
  ''', "topics")
    return f'''
<section class="block" id="features" data-search="feature engineering regularization L2" data-stype="Section">
  <p class="kicker">Inputs</p>
  <h2 class="section-title">Features and regularization</h2>
  <p><a href="#gym-features">Jump to practice (6) →</a></p>
  {t}
  {features_gym()}
</section>
'''
