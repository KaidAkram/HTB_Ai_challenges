import numpy as np
import os
from sklearn.neighbors import kneighbors_graph
from scipy.sparse.csgraph import dijkstra

print("=== HTB Full of Stars: Geodesic Dijkstra Propagation Solver ===")

# 1. Load data
print("[1/6] Loading data files...")
data_path = 'data.npy.gz'
core_path = 'known_samples.npy.gz'

if not os.path.exists(data_path) or not os.path.exists(core_path):
    # Fallback to absolute paths if running in a different CWD
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, data_path)
    core_path = os.path.join(base_dir, core_path)

data = np.loadtxt(data_path)
core = np.loadtxt(core_path)

# Stack cores and data points
X = np.vstack((core, data))
N = X.shape[0]
print(f"Total points loaded: {N} (Anchors: {len(core)}, Data points: {len(data)})")

# 2. Apply anisotropic scaling
# Down-weight Y-axis (index 1) to prevent k-NN edges from bridging stacked filaments
print("[2/6] Applying anisotropic scaling: S = [1.0, 0.35, 1.0]...")
S = np.array([1.0, 0.35, 1.0])
X_scaled = X * S

# 3. Build symmetric k-NN graph
print("[3/6] Building symmetric k-NN graph (k=14)...")
knn_graph = kneighbors_graph(X_scaled, n_neighbors=14, mode='distance', include_self=False)
# Symmetrize the graph using element-wise maximum
symmetric_graph = knn_graph.maximum(knn_graph.T)

# 4. Launch multi-source Dijkstra shortest path search
print("[4/6] Running multi-source Dijkstra from the 256 anchors...")
# Compute shortest path from all 256 anchors
dist_matrix = dijkstra(csgraph=symmetric_graph, directed=False, indices=np.arange(256))

# 5. Assign labels based on geodesic distance
print("[5/6] Assigning cluster labels...")
labels = np.argmin(dist_matrix, axis=0)

# Verify that the anchor points themselves are correctly labeled
mismatched_anchors = np.sum(labels[:256] != np.arange(256))
print(f"Verification: {mismatched_anchors} anchor points had mismatching self-labels.")

# 6. Save the resulting image
print("[6/6] Writing flag.jpg file...")
# The labels of the data points correspond to the image bytes
img_bytes = bytes([int(x) for x in labels[256:]])

output_path = 'flag.jpg'
if not os.path.isabs(output_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, output_path)

with open(output_path, "wb") as f:
    f.write(img_bytes)

print(f"Successfully wrote {len(img_bytes)} bytes to '{output_path}'.")

# Basic JPEG check
if img_bytes.startswith(b'\xff\xd8') and img_bytes.endswith(b'\xff\xd9'):
    print("SUCCESS: Valid JPEG signature (FFD8...FFD9) detected!")
else:
    print("WARNING: Output does not start with FFD8 or end with FFD9. Checking headers...")
    print(f"Start bytes: {img_bytes[:4].hex(' ')}")
    print(f"End bytes: {img_bytes[-4:].hex(' ')}")
