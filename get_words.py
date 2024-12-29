from gensim.models import KeyedVectors

# # Load Word2Vec model 
# model_path = 'google_news_vectors.bin'
# word_vectors = KeyedVectors.load_word2vec_format(model_path, binary=True)


def find_best_match(input_word, possible_answers, model, threshold=0.6):
    best_match = None
    highest_similarity = threshold
    possible_answers = [x for x in possible_answers if str(x) != 'nan']

    # Preprocess input to handle multi-word inputs
    input_words = input_word.lower().split()

    for answer in possible_answers:
        answer_words = answer.lower().split()
        total_similarity = 0
        count = 0

        for input_w in input_words:
            for answer_w in answer_words:
                try:
                    # Calculate similarity between each word
                    similarity = model.similarity(input_w, answer_w)
                    total_similarity += similarity
                    count += 1
                except KeyError:  # If the word is not in the vocabulary
                    continue
        
        # Calculate average similarity for multi-word inputs and answers
        if count > 0:
            avg_similarity = total_similarity / count
            if avg_similarity > highest_similarity:
                best_match = answer
                highest_similarity = avg_similarity

    return best_match



# Example usage
# user_input = "fireman"
# possible_answers = ["police officer", "firefighter", "performer"]
# best_match = find_best_match(user_input, possible_answers, word_vectors)
# print(f"Best match for '{user_input}': {best_match}")
