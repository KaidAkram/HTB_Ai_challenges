import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def solve():
    print("[*] Loading embeddings...")
    data = np.load('token_embeddings.npz')
    tokens = data['tokens']
    emb = data['embeddings']

    print("[*] Performing PCA and plotting 3D cube...")
    pca = PCA(n_components=3)
    emb_3d = pca.fit_transform(emb)
    
    # Scale up the 3rd dimension to make variance comparable
    emb_3d[:, 2] = emb_3d[:, 2] * (np.std(emb_3d[:, 0]) / np.std(emb_3d[:, 2]))

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(tokens)):
        ax.text(emb_3d[i, 0], emb_3d[i, 1], emb_3d[i, 2], tokens[i], fontsize=12, weight='bold')
    ax.scatter(emb_3d[:, 0], emb_3d[:, 1], emb_3d[:, 2], alpha=0)
    plt.title("3D Scaled PCA of Cube")
    plt.savefig("cube_3d.png", bbox_inches='tight')
    print("[+] Saved 3D visualization as cube_3d.png")

    print("[*] Performing 512D Nearest Neighbor search to find the flag...")
    h_indices = [i for i, t in enumerate(tokens) if t == 'H']
    
    for start_idx in h_indices:
        path = [start_idx]
        unvisited = set(range(len(tokens)))
        unvisited.remove(start_idx)
        
        current = start_idx
        while unvisited:
            nearest = min(unvisited, key=lambda i: np.linalg.norm(emb[current] - emb[i]))
            path.append(nearest)
            unvisited.remove(nearest)
            current = nearest
            
        result = ''.join(tokens[i] for i in path)
        if "HTB{" in result:
            print(f"\n[+] Flag found!")
            print(f"Path: {result}")
            flag_start = result.find("HTB{")
            flag_end = result.find("}", flag_start) + 1
            print(f"\nFlag: {result[flag_start:flag_end]}")
            break

if __name__ == "__main__":
    solve()
