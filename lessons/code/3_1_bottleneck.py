import numpy as np
rng = np.random.default_rng(0)
d = 64                       # size of every vector (the "memory budget")

def word():                  # a random word vector of length 1
    v = rng.standard_normal(d)
    return v / np.linalg.norm(v)

def trial(n):
    sentence = [word() for _ in range(n)]
    H = np.stack(sentence)                       # look-back: keep all n vectors
    summary = H.sum(axis=0)                      # bottleneck: squeeze into one vector
    probes = sentence + [word() for _ in range(n)]   # half were in the sentence, half were not
    truth = [True] * n + [False] * n
    right_summary = sum((p @ summary > 0.5) == t for p, t in zip(probes, truth))
    right_lookback = sum(((H @ p).max() > 0.5) == t for p, t in zip(probes, truth))
    return right_summary / (2 * n), right_lookback / (2 * n)

print(" words | one summary vector | keep every vector")
for n in [2, 5, 10, 20, 40, 80, 160]:
    s, l = np.mean([trial(n) for _ in range(50)], axis=0)
    print(f"{n:6d} | {s:18.0%} | {l:17.0%}")
