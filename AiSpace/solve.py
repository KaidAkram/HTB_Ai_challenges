import numpy as np
import matplotlib.pyplot as plt
import os

def cmdscale(D):
    """
    Classical multidimensional scaling (MDS)
    
    Args:
        D (numpy.ndarray): Symmetric distance matrix.
        
    Returns:
        Y (numpy.ndarray): Reconstructed coordinates in 2D.
    """
    # Number of points
    n = D.shape[0]
    
    # Squared distance matrix
    D2 = D**2
    
    # Centering matrix
    H = np.eye(n) - np.ones((n, n))/n
    
    # Double centering
    B = -0.5 * H.dot(D2).dot(H)
    
    # Eigendecomposition
    eigvals, eigvecs = np.linalg.eigh(B)
    
    # Sort by eigenvalue in descending order
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]
    
    # Extract top 2 dimensions
    L = np.diag(np.sqrt(np.maximum(eigvals[:2], 0)))
    V = eigvecs[:, :2]
    
    return V.dot(L)

def main():
    if not os.path.exists('distance_matrix.npy'):
        print("Error: distance_matrix.npy not found.")
        return

    print("Loading distance matrix...")
    matrix = np.load('distance_matrix.npy')
    
    print(f"Matrix shape: {matrix.shape}")
    print("Performing Classical MDS to reconstruct coordinates...")
    coords = cmdscale(matrix)
    
    # The MDS output happens to be horizontally mirrored. We flip the X-axis to make it readable.
    coords[:, 0] = -coords[:, 0]
    
    print("Plotting the coordinates...")
    plt.figure(figsize=(20, 5))
    
    # Plot as a scatter plot
    plt.scatter(coords[:, 0], coords[:, 1], s=2, c='#00FF00')
    
    # Using 'equal' aspect ratio is crucial to read the text without stretching
    plt.axis('equal')
    
    plt.title("Reconstructed Coordinates (Flag)")
    
    # Hide axes for cleaner look
    plt.xticks([])
    plt.yticks([])
    
    plt.savefig('flag.png', bbox_inches='tight', dpi=300, facecolor='#111111')
    print("Saved plot to flag.png. Check the image to read the flag!")

if __name__ == "__main__":
    main()
