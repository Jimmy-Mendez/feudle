import os
import numpy as np
from openai import OpenAI

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'], 
)

def get_embedding(text, model="text-embedding-ada-002"):
    """Fetch the embedding for the given text using OpenAI API."""
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return np.array(response.data[0].embedding)


def cosine_similarity(vec1, vec2):
    """Calculate the cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def find_best_match(input_word, possible_answers, model=None, threshold=0.85):
    best_match = None
    highest_similarity = threshold
    possible_answers = [x for x in possible_answers if str(x) != 'nan']

    # Get embedding for the input word
    input_embedding = get_embedding(input_word)

    for answer in possible_answers:
        try:
            # Get embedding for the answer
            answer_embedding = get_embedding(answer)

            # Calculate similarity
            similarity = cosine_similarity(input_embedding, answer_embedding)
            if similarity > highest_similarity:
                best_match = answer
                highest_similarity = similarity
        except Exception as e:
            print(f"Error processing answer '{answer}': {e}")
            continue

    return best_match

# Example usage
# user_input = "fireman"
# possible_answers = ["police officer", "firefighter", "performer"]
# best_match = find_best_match(user_input, possible_answers)
# print(f"Best match for '{user_input}': {best_match}")
