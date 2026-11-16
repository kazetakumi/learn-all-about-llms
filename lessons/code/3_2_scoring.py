import numpy as np
rng = np.random.default_rng(0)
d = 64

def softmax(e):
    e = np.exp(e - e.max())
    return e / e.sum()

# Part 1: distance and dot product give the same weights (up to a length term)
s = 0.3 * rng.standard_normal(d)               # the decoder's need
H = 0.3 * rng.standard_normal((5, d))          # five encoder states
by_distance = softmax(-((H - s) ** 2).sum(axis=1) / 2)
by_dot = softmax(H @ s - (H ** 2).sum(axis=1) / 2)
print("weights from distance:", by_distance.round(3))
print("weights from dot     :", by_dot.round(3))

# Part 2: raw self-attention, softmax(X X^T) X, on one sentence
words = "the animal did not cross the street because it was tired".split()
vec = {w: rng.standard_normal(d) for w in dict.fromkeys(words)}
vec["it"] = 0.6 * vec["animal"] + 0.8 * rng.standard_normal(d)   # "it" built close to "animal"
X = np.stack([vec[w] for w in words])
scores = X @ X.T                           # every pair at once: one matrix multiply
A = np.stack([softmax(row) for row in scores])
out = A @ X                                # each row: a weighted average of all words

print("\nscores symmetric?", np.allclose(scores, scores.T))
i = words.index("it")
print("where 'it' looks:   score   weight")
for j in np.argsort(-scores[i])[:4]:
    print(f"  {words[j]:15s} {scores[i, j]:6.1f}   {A[i, j]:.3f}")
print("weight each word puts on itself:", np.diag(A).round(2))

# Ablation: make every vector length 1, so only direction counts
U = X / np.linalg.norm(X, axis=1, keepdims=True)
a = softmax((U @ U.T)[i])
print("\nlength-1 vectors: 'it' on itself %.2f, on 'animal' %.2f, even split %.2f"
      % (a[i], a[words.index("animal")], 1 / len(words)))
