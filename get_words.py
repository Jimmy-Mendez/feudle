from gensim.models import KeyedVectors

# Load Word2Vec model 
model_path = 'google_news_vectors.bin'
word_vectors = KeyedVectors.load_word2vec_format(model_path, binary=True)


def find_best_match(input_word, possible_answers, model, threshold=0.7):
    best_match = None
    highest_similarity = threshold
    for answer in possible_answers:
        for answer_word in answer.split():
            try:
                similarity = model.similarity(input_word, answer_word)
                if similarity > highest_similarity:
                    best_match = answer
                    highest_similarity = similarity
            except KeyError:  # If the word is not in the vocabulary
                continue
    return best_match

# Example usage
user_input = "fireman"
possible_answers = ["police officer", "firefighter", "performer"]
best_match = find_best_match(user_input, possible_answers, word_vectors)
print(f"Best match for '{user_input}': {best_match}")
