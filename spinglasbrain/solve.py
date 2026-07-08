import numpy as np
import matplotlib.pyplot as plt

W = np.load('weights.npy')
print('W loaded')

patterns = []
for key in range(1, 17):
    boolean = format(key, '06b')
    S = np.zeros(6400)
    for c_ix, c in enumerate(boolean):
        S[c_ix] = 1 if c == '1' else -1
    
    for i in range(50):
        S_new = np.sign(W @ S)
        S_new[S_new == 0] = 1
        for c_ix, c in enumerate(boolean):
            S_new[c_ix] = 1 if c == '1' else -1
            
        if np.array_equal(S, S_new):
            print(f'Key {key} converged in {i} iterations')
            break
        S = S_new
    else:
        print(f'Key {key} did not converge')
    
    patterns.append(S.reshape(80, 80))

fig, axs = plt.subplots(3, 6, figsize=(14, 6))
plt.subplots_adjust(wspace=0, hspace=0)
axs = axs.flatten()
for c, ax in zip(patterns, axs):
    ax.imshow(c, cmap="gray", aspect="auto")
for ax in axs:
    ax.set_xticks([])
    ax.set_yticks([])
plt.savefig("flag.png")
print("Saved flag.png")
