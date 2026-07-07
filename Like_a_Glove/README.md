# 🥊 Like a Glove - HackTheBox Challenge

**Link:** [HackTheBox - Like a Glove](https://app.hackthebox.com/challenges/Like%20a%20Glove)

![Like a Glove](https://img.shields.io/badge/HackTheBox-AI%20Challenge-green?style=for-the-badge&logo=hackthebox)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Gensim](https://img.shields.io/badge/Gensim-Word2Vec-orange?style=for-the-badge)

Welcome to the write-up and solution for the **Like a Glove** AI challenge on HackTheBox. This repository contains the provided challenge files, a detailed explanation of the theoretical background, the pitfalls designed by the challenge creator, and the final solution script.

---

## 📖 Challenge Overview

### Description
> *"Words carry semantic information. Similar to how people can infer meaning based on a word's context, AI can derive representations for words based on their context too! However, the kinds of meaning that a model uses may not match ours. We've found a pair of AIs speaking in metaphors that we can't make any sense of! The embedding model is `glove-twitter-25`. Note that the flag should be fully ASCII and starts with 'htb{'."*

### Provided Files
- `chal.txt`: A text file containing 84 lines of word analogies in the format: `Like A is to B, C is to?`
- `solve.py`: A Python script intended to parse these analogies and recover the flag.

---

## 🧠 The Theory: Word Embeddings & Analogies

In Natural Language Processing (NLP), **Word Embeddings** are techniques used to map words to high-dimensional mathematical vectors. Models like `Word2Vec` and `GloVe` (Global Vectors for Word Representation) are trained on massive text corpora to capture semantic relationships between words based on their co-occurrence context.

### Vector Arithmetic (Metaphors)
One of the most fascinating properties of word embeddings is their ability to solve **word analogies** using simple vector arithmetic. 

The classic example is:
`King is to Man, as Queen is to Woman`

Mathematically, in the embedding space, this translates to:
`Vector(King) - Vector(Man) + Vector(Woman) ≈ Vector(Queen)`

If you take the vector for *King*, subtract the vector for *Man* (removing the concept of masculinity), and add the vector for *Woman* (adding the concept of femininity), the resulting coordinate in the high-dimensional space will be closest to the vector for the word *Queen*.

In this challenge, we are given 84 of these analogies (`A is to B, as C is to ?`), which translates to:
`Target Vector = Vector(B) - Vector(A) + Vector(C)`

---

## 🪤 The Pitfall (Red Herring)

If you examine the provided `solve.py` script, it uses the popular `gensim` library to solve the analogies:

```python
# From original solve.py
res = model.most_similar(positive=[b, c], negative=[a], topn=1)
word = res[0][0]
flag += word[0]
```

### The Problem
If you run this script with the `glove-twitter-25` model, the output is largely non-ASCII, containing Japanese, Chinese, and strange symbols. Furthermore, concatenating the first letters (`word[0]`) yields gibberish like `h{e１d０１o...`, which clearly violates the hint that the flag must be **fully ASCII**.

### Why does this happen?
When you use `gensim`'s built-in `most_similar(positive=[...], negative=[...])` method, the library internally **L2-normalizes** all word vectors (scaling their lengths to 1) *before* performing the addition and subtraction. While this is best practice for standard NLP tasks, it distorts the raw vector space.

---

## 💡 The Solution

The challenge creators (or the "AIs speaking in metaphors") didn't use normalized vectors when they generated this challenge. They performed **raw, unnormalized vector arithmetic**.

To retrieve the true flag, we must bypass `gensim`'s helper functions and manually perform the arithmetic on the raw vectors:

```python
# Perform raw vector arithmetic without normalization
result_vector = model[value] - model[key] + model[query]

# Find the closest matching word in the vocabulary to this raw vector
closest_word = model.most_similar(positive=[result_vector], topn=1)[0][0]
```

### The Magic of the Raw Space
When you apply this raw math to the first few queries, an amazing thing happens:
1. `non-mainstream : efl :: battery-powered : ?` → Evaluates exactly to `"htb"`
2. `sycophancy : بالشهادة :: cont : ?` → Evaluates exactly to `"{"`
3. `беспощадно : indépendance :: rs : ?` → Evaluates exactly to `"h4"`

Instead of extracting just the first character (`word[0]`), the raw arithmetic yields **entire multi-character chunks** of the flag perfectly. The embedding space is so dense and rich that the authors were able to carefully select analogies whose raw vector combinations landed exactly on the flag segments in 1337-speak!

### Final Normalization
When all 84 resulting words are concatenated, the string is almost entirely ASCII, perfectly forming the flag. However, a few full-width unicode numbers (e.g., `０`, `１`) slip in because the `glove-twitter-25` model includes standard and full-width variants from its Twitter training data. A quick string replacement mapping `０-９` to `0-9` yields the final, pristine ASCII flag.

---

## 🚀 Running the Solution

1. Ensure you have `gensim` installed:
   ```bash
   pip install gensim
   ```
2. Run the solution script. It will automatically download the required `glove-twitter-25` model and extract the flag:
   ```bash
   python sol.py
   ```
3. The flag will be printed to the console and saved in `flag.txt`.
