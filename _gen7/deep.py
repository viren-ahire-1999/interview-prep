from util import topic, diagram, callout, code
from drills import nn_gym, cnn_gym, transformer_gym


def neural() -> str:
    t1 = topic("nn-fwd", "A neuron is a weighted sum plus a bend",
               "neural network perceptron activation backprop", "Lesson", f'''
  <p>One neuron: multiply inputs by weights, add a bias, then apply a <b>non-linearity</b> (ReLU = max(0, x), sigmoid, tanh). Without the bend, a stack of layers is still one linear model — uselessly shallow.</p>
  {diagram("""x1 ─w1─┐
x2 ─w2─┼─► sum + bias ─► ReLU ─► hidden
x3 ─w3─┘
Many neurons in parallel = a layer.
Many layers = a multi-layer perceptron (MLP).""")}
  {code("Python", '''import numpy as np

def relu(x):
    return np.maximum(0, x)

def forward(x, W1, b1, W2, b2):
    h = relu(x @ W1 + b1)     # x: (B, in)
    logits = h @ W2 + b2      # (B, classes)
    return logits''')}
  <p><b>Softmax</b> turns logits into a probability distribution (they sum to 1). Training uses <b>cross-entropy</b> with the true class: “how surprised were we.”</p>
  <p><b>Backprop</b> is the chain rule run in reverse: each weight gets a share of the blame for the loss. Optimizers (SGD, Adam) decide the step size. You will use Adam and a learning-rate schedule long before you write your own CUDA kernel.</p>
  {callout("Vanishing gradients: stacked sigmoids squash signals. ReLU and residuals (skip connections) were engineering answers. Transformers use both residual and layer-norm.")}
  ''', "topics")
    return f'''
<section class="block" id="nn" data-search="neural networks backprop ReLU" data-stype="Section">
  <p class="kicker">Deep learning starts here</p>
  <h2 class="section-title">Neural nets</h2>
  <p><a href="#gym-nn">Jump to practice (6) →</a></p>
  {t1}
  {nn_gym()}
</section>
'''


def cnn_seq() -> str:
    t = topic("cn-loc", "Images share patterns; text used to walk left to right",
              "CNN convolution RNN sequence models", "Lesson", f'''
  <p>A <b>convolution</b> slides a small filter (e.g. 3×3) across an image. The same weights detect an edge everywhere — <b>parameter sharing</b>. Stack filters and you get textures, then object parts. CNNs made vision practical before transformers ate that too.</p>
  {diagram("""Image 5×5, filter 3×3 → response 3×3 (valid)
Each output cell = dot product of the window with the filter
+ ReLU + optional pooling (downsample)""")}
  <p><b>Sequences</b> (text, audio): older models were RNNs / LSTMs — they read one token at a time and kept a hidden state. They struggle with long-range links and do not train as easily in parallel. That is why <a href="#transformers">attention</a> won for language.</p>
  <p>You still meet CNNs in vision APIs, medical imaging, and as a cheap tower next to a text model. You still meet recurrence in some speech and time-series stacks. Know why they exist; do not start a new NLP system on a vanilla LSTM in 2026 without a reason.</p>
  ''', "topics")
    return f'''
<section class="block" id="cnn" data-search="CNN RNN sequence models" data-stype="Section">
  <p class="kicker">Structure in space and time</p>
  <h2 class="section-title">CNNs and sequences</h2>
  <p><a href="#gym-cnn">Jump to practice (5) →</a></p>
  {t}
  {cnn_gym()}
</section>
'''


def transformers() -> str:
    t1 = topic("tr-attn", "Attention: every token looks at every token",
               "self attention QKV transformer encoder decoder", "Lesson", f'''
  <p>Self-attention lets each position build a weighted average of the others. Weights come from similarity of a <b>query</b> (what I am looking for) and <b>keys</b> (what each position offers). Values are the content that gets mixed.</p>
  {code("Python", '''import numpy as np

def softmax(x, axis=-1):
    x = x - x.max(axis=axis, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)

def attention(Q, K, V):
    # Q,K,V: (T, D)
    scale = Q.shape[-1] ** 0.5
    weights = softmax(Q @ K.T / scale)   # (T, T)
    return weights @ V                   # (T, D)''')}
  {diagram("""tokens:  the  cat  sat
Each row of weights: how much this token mixes the others
‘sat’ may put mass on ‘cat’ — a subject for the verb
+ residual + MLP after attention = one transformer block""")}
  <p><b>Multi-head:</b> run attention several times with different projections so one head can do syntax and another a different pattern. <b>Positional information</b> is added because raw attention does not know order. <b>Encoder</b> sees the whole sequence; a <b>decoder</b> for generation attends only leftward (causal mask) so it cannot peek at the future token.</p>
  <p>An LLM is (mostly) a stack of decoder blocks trained to predict the next token on a huge text mix, then later aligned with instructions and preferences. That is the whole magic trick — scale plus this architecture.</p>
  {callout("<b>Context window</b> is how many tokens fit in that attention matrix. Cost grows steeply with length (classically T²). Long-context models change the engineering, not the product duty to retrieve the right facts.")}
  ''', "topics")
    return f'''
<section class="block" id="transformers" data-search="transformer attention QKV LLM" data-stype="Section">
  <p class="kicker">The modern core</p>
  <h2 class="section-title">Attention and transformers</h2>
  <p><a href="#gym-transformer">Jump to practice (6) →</a></p>
  {t1}
  {transformer_gym()}
</section>
'''
