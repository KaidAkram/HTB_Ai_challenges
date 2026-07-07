import re
import gensim.downloader as api

def load_glove_model():
    model = api.load('glove-twitter-25')
    return model

def parse_challenge(file_path, model):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    results = []
    flag_characters = []

    for i, line in enumerate(lines):        
        match = re.search(r"Like (.+?) is to (.+?), (.+?) is to\?", line.strip())
        if not match:
            match = re.search(r"Like (.+) is to (.+), (.+) is to\?", line.strip())
            if not match:
                continue

        key, value, query = match.groups()
        key = key.strip()
        value = value.strip()
        query = query.strip()
        print(f"Extracted: '{key}' -> '{value}', '{query}' -> ?")       
        try:
            missing_words = []
            for word in [key, value, query]:
                if word not in model:
                    missing_words.append(word)           
            if missing_words:
                print(f"Skipping due to missing words: {missing_words}")
                continue
            # This performs the vector math   
            result_vector = model[value] - model[key] + model[query]
            closest_word = model.most_similar(positive=[result_vector], topn=1)[0][0]

            print(f"Closest match for '{query}' is '{closest_word}'")

            flag_characters.append((i, query, closest_word))
        except KeyError as e:
            print(f"Error: {e}")
            continue


    mapped_chars = [char[2] for char in flag_characters]

    potential_flag = ''.join(mapped_chars)
    print(f"Potential flag sequence: {potential_flag}")

    normalized_flag = potential_flag
    replacements = {
        '０': '0', '１': '1', '２': '2', '３': '3', '４': '4',
        '５': '5', '６': '6', '７': '7', '８': '8', '９': '9'
    }

    for non_ascii, ascii_char in replacements.items():
        normalized_flag = normalized_flag.replace(non_ascii, ascii_char)

    print(f"Normalized flag: {normalized_flag}")
    return normalized_flag

if __name__ == "__main__":
    challenge_file = "chal.txt"
    model = load_glove_model()
    flag_sequence = parse_challenge(challenge_file, model)
    print("FINAL FLAG:")
    print(flag_sequence)

    # Create a clean output file with just the flag
    with open('flag.txt', 'w', encoding='utf-8') as flag_file:
        flag_file.write(flag_sequence)
    print(f"Flag has been saved to flag.txt")
