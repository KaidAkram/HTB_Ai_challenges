# AI SPACE - Hack The Box Challenge Writeup

## Challenge Description
**Mission:** You are assigned the important mission of locating and identifying the infamous space hacker. Your investigation begins by analyzing the data patterns and breach points identified in the latest cyber-attacks. Use the provided coordinates of the last known signal origins to narrow down his potential hideouts. Utilize advanced tracking algorithms to follow the digital footprint left by the hacker.

**Challenge Link:** [AI SPACE on Hack The Box](https://app.hackthebox.com/challenges/AI%2520SPACE?tab=play_challenge)

---

## Theory and Concept

The challenge provides a single file: `distance_matrix.npy`. This is a serialized NumPy array of size 1808x1808. In data science, a matrix like this usually represents the pairwise distances (e.g., Euclidean distance) between a set of $N$ unknown points. 

The prompt hints at using "coordinates of the last known signal origins" and "digital footprint". Since we only have the *distances* between these signal origins, we must mathematically reconstruct the original 2D space $(X, Y)$ coordinates of these 1,808 points.

The mathematical algorithm for reconstructing spatial coordinates from pairwise distances is known as **Classical Multidimensional Scaling (MDS)** or **Principal Coordinate Analysis (PCoA)**.

### Classical MDS Algorithm:
1. **Squared Distance:** Let $D$ be our distance matrix. We start by computing the squared distance matrix $D^{(2)}$.
2. **Double Centering:** We apply a centering matrix $H = I - \frac{1}{n}11^T$ to the squared distances to form an inner product matrix: $B = -\frac{1}{2} H D^{(2)} H$.
3. **Eigendecomposition:** We compute the eigenvalues and eigenvectors of $B$. 
4. **Coordinate Extraction:** The top $k$ eigenvectors (in our case, 2 for a 2D image) scaled by the square root of their corresponding eigenvalues yield the reconstructed $k$-dimensional coordinates.

Because MDS determines relative positioning, the final mapping is invariant to translation, rotation, and reflection. Thus, the resulting visual might appear rotated or mirrored.

---

## Solution Walkthrough

1. **Prerequisites:** Ensure you have `numpy` and `matplotlib` installed.
   ```bash
   pip install numpy matplotlib
   ```

2. **Load and Process the Matrix:**
   Using the script `solve.py` provided in this repository, we load `distance_matrix.npy` and apply the Classical MDS algorithm.

3. **Flip the Projection:**
   When extracting the $X$ and $Y$ coordinates directly from MDS, the coordinates are plotted backwards (horizontally mirrored). By flipping the $X$ values (`coords[:, 0] = -coords[:, 0]`), we mirror the text so that it is properly readable from left to right.

4. **Plotting the Digital Footprint:**
   We scatter plot the extracted coordinates. It's crucial to set the plot aspect ratio to **equal** (`plt.axis('equal')`); otherwise, the shape stretches to fit the figure box and the letters become unreadable.

5. **Result:**
   The scatter plot forms a clear text image which is the digital footprint left by the hacker, revealing the flag.

---

## Running the Solver

Run the script in the same directory as the `.npy` file:

```bash
python solve.py
```

This will generate `flag.png` in the same directory. Open the image to reveal the hidden message.

## The Flag

**`HTB{REDACTED}`** - *Run the script to reveal the flag!*
