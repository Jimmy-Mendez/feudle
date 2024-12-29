from get_words import find_best_match
import pandas as pd
from gensim.models import KeyedVectors
import numpy as np

# Load Word2Vec model 
model_path = 'google_news_vectors.bin'
word_vectors = KeyedVectors.load_word2vec_format(model_path, binary=True)


def check_match(row, usr_input):
    question = row[0]
    ans = [row[1], row[3], row[5], row[7], row[9], row[11], row[13]]
    pts = [float(row[2]), float(row[4]), float(row[6]), float(row[8]), float(row[10]), float(row[12]), float(row[14])]

    best_match = find_best_match(usr_input, ans, word_vectors)
    if best_match == None:
        return (None, 0)
    ans_idx = ans.index(best_match)
    pts_for_match = pts[ans_idx]

    return (ans[ans_idx], pts_for_match)

def get_today_question():
    np.random.seed(42)
    # Load quizzes and played questions
    quizzes = pd.read_csv('quizzes.csv')
    try:
        played_questions = pd.read_csv('played_questions.csv')
    except FileNotFoundError:
        # Create an empty DataFrame if file doesn't exist
        played_questions = pd.DataFrame(columns=quizzes.columns)

    # Determine the number of answers based on the day of the week
    today = pd.Timestamp.now().dayofweek  # Monday = 0, Sunday = 6
    num_answers_today = 4 + today  # 4 answers on Monday, 5 on Tuesday, etc.
    if today == 5 or today == 6:
        num_answers_today = 4

    # Filter rows with at least the required number of answers
    quizzes_filtered = quizzes[quizzes.iloc[:, 1::2].count(axis=1) == num_answers_today]

    while True:
        # Select a random row
        random_row = list(quizzes_filtered.sample(n=1).iloc[0])

        # Check if the question has already been played
        if not ((played_questions['Question'] == random_row[0]).any()):
            break

    # Append the selected question to played_questions.csv
    new_df = pd.DataFrame([random_row], columns=played_questions.columns)
    played_questions = pd.concat([played_questions, new_df], ignore_index=True)
    played_questions.to_csv('played_questions.csv', index=False)

    # Return the selected question
    return (random_row, num_answers_today)

def play():
    q, n = get_today_question()  # Get the question and the number of answers
    pts = 0
    correct = 0
    strike = 0
    ans_so_far = []  # To track the answers provided so far
    answers_on_board = q[1::2][:n]  # Extract the correct answers for today (n answers)
    
    print(q[0])  # Print the question
    print(f"Top {n} answers on the board.")

    while strike < 3:
        inp = input("Enter your answer: ").strip()
        check = check_match(q, inp)

        if check == (None, 0):
            strike += 1
            print("X"*strike)
            print(f"\nStrike {strike}")
        else:
            if check[0] in ans_so_far:
                print("You already answered that!")
            else:
                pts += check[1]
                correct += 1
                ans_so_far.append(check[0])
                print(f"Correct! {check[0]} is worth {check[1]} points!")
                print(f"Answers so far: {ans_so_far}")
                
                if correct == n:  # Check if all answers have been found
                    print(f"You win! Total points: {pts}")
                    break

        # If the game is still going, reprint the question
        if strike < 3 and correct < n:
            print(q[0])
            print(f"Top {n} answers on the board.")

    if strike == 3:
        print(f"Game over! You scored {pts} points.")


play()
