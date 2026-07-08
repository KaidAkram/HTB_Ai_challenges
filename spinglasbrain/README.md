<div align="center">
  <img src="https://labs.hackthebox.com/storage/avatars/41ff69e8432a52ef61d5631c3bf17173.png" alt="HTB Logo" width="100"/>
  <h1>Spinglasbrain 🧠 | Hack The Box AI Challenge</h1>
  <p><i>A deep dive into Hopfield Networks and Content-Addressable Memory</i></p>
  
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white" alt="Numpy"/>
  <img src="https://img.shields.io/badge/Machine_Learning-FF9900?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="Machine Learning"/>
</div>

---

## 🎯 Overview

Welcome to the **Spinglasbrain** challenge! In this challenge, we explore the fascinating world of **Hopfield Networks**. We are provided with the pre-trained weights of a network containing encoded characters that, when combined, reveal a secret flag. 

**Objective:** Retrieve the hidden patterns stored in the network's memory using Hopfield dynamics.

---

## 📖 Theory & Background

### What is a Hopfield Network?
A **Hopfield Network** is a type of recurrent artificial neural network that functions as a **content-addressable memory** system. It consists of $N$ bipolar units (neurons with states $\{-1, 1\}$) interconnected with a symmetric weight matrix $W$.

When the network is trained (often via Hebbian learning), the memorized patterns become local minima—or *attractors*—in the network's energy landscape.

### ⚙️ Network Dynamics
The state of the network at any time $t$ is a vector $S(t) \in \{-1, 1\}^N$. It evolves according to the following update rule:

$$S_i(t+1) = \text{sign}\left(\sum_{j=1}^N W_{ij} S_j(t)\right)$$

To retrieve a stored pattern, the network is initialized with a noisy or partial version of the target pattern. The recurrent updates drive the network state down the energy gradient until it converges to the nearest attractor (the original memory).

---

## 🔍 Challenge Analysis

We are given two essential files:
- 📓 `challenge.ipynb`: A Jupyter Notebook containing the `encode_pattern` encoding logic.
- 🧠 `weights.npy`: The weight matrix of the Hopfield Network ($6400 \times 6400$).

### 💡 Key Discoveries
1. **Dimensions:** The images are $80 \times 80$ pixels, which flattens to $6400$ neurons.
2. **Encoding Secret:** The `encode_pattern(key, arr)` function embeds the character's index (the `key`) into the **very first 6 pixels** of the pattern using a 6-bit binary representation. The challenge states that indices range from `1` to `16`.

This means each of the 16 characters forming the flag is permanently tagged with a unique 6-bit prefix representing its position!

---

## 🚀 Solution Steps

### 1️⃣ Pattern Extraction Strategy
Instead of blindly guessing, we can exploit the network's properties. By randomly initializing the network state and iterating until convergence, we can exhaustively map out the unique attractors (the stored characters) hidden within the weights.

### 2️⃣ Iterating to Convergence
We wrote a Python solver (`solve.py`) to systematically extract the patterns:
1. Initialize a random bipolar array of size $6400$ as the initial state $S$.
2. Apply the Hopfield update rule $S_{new} = \text{sign}(W \cdot S)$ repeatedly (up to 50 iterations).
3. Once the state stabilizes ($S_{new} == S$), the network has found a local minimum.
4. Loop this process with new random seeds until all **16 unique patterns** are discovered.

### 3️⃣ Assembling the Flag
Because each character's correct position is hardcoded into its first 6 pixels, recovering the sequence is trivial:
- Extract the first 6 pixels of each converged pattern.
- Convert the bipolar values (`1` and `-1`) back into binary bits (`1` and `0`).
- Parse the integer index (1 to 16).
- Sort the 16 extracted $80 \times 80$ images by this index!

Visualizing the ordered patterns reveals the characters of the flag perfectly.

### 🚩 The Flag
> **`HTB{capacity_er}`**

*(See `flag_output.png` for the visual output of the extracted letters)*

---

## 🌍 Real-World Scenarios and Implications

Understanding Hopfield networks and attractor dynamics goes far beyond CTF challenges. These concepts have massive implications in real-world AI and Security:

- 🧩 **Content-Addressable Memory & Error Correction**: Hopfield networks excel at reconstructing original data from corrupted or partial inputs. In the real world, this logic is analogous to repairing corrupted images, correcting transmission errors over noisy channels, or matching partial fingerprints/DNA sequences.
- 🔓 **AI Data Privacy (Model Inversion Attacks)**: This challenge is a prime example of a fundamental vulnerability in AI: models memorize training data. If an attacker gains access to a model's weights, they can reverse-engineer the training dataset. This highlights the critical need for **Differential Privacy** when training models on sensitive data (e.g., medical records, PII).
- ⚡ **Combinatorial Optimization**: The energy-minimization properties of Hopfield networks make them highly effective for solving complex optimization problems (e.g., the Traveling Salesperson Problem, job-shop scheduling), where the lowest energy state represents the optimal solution.

---
<div align="center">
  <i>Developed for Hack The Box AI challenges.</i>
</div>
