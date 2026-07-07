import re
import gensim.downloader as api
import sys

with open("chal.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

queries = []
for line in lines:
    m = re.match(r"Like (.+) is to (.+), (.+) is to\?", line.strip())
    if m:
        queries.append((m.group(1), m.group(2), m.group(3)))

print(f"Found {len(queries)} queries.")
print("Loading model...")
try:
    model = api.load("glove-twitter-25")
except Exception as e:
    print(f"Failed to load model: {e}")
    sys.exit(1)

print("Solving analogies...")
flag = ""
for i, (a, b, c) in enumerate(queries):
    try:
        # A : B :: C : D -> D = B - A + C
        result = model.most_similar(positive=[b, c], negative=[a], topn=1)
        word = result[0][0]
        print(f"{i+1}: {a} : {b} :: {c} : {word}")
        flag += word[0]
    except Exception as e:
        print(f"Error on {a} : {b} :: {c} -> {e}")
        flag += "?"

print(f"Flag so far: {flag}")
