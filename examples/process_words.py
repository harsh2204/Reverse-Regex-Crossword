accepted_words = []

with open('words', 'r') as f:
    words = f.readlines()
    for w in words:
        if len(w.strip()) > 2 and len(w.strip())%2 == 0:
            accepted_words.append(w)

print("selected", len(accepted_words), "words")
with open('accepted_words', 'w') as f:
    f.writelines(accepted_words)