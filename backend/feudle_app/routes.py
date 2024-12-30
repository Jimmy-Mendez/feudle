from flask import Blueprint, request, jsonify
from get_words import find_best_match
import pandas as pd
import numpy as np

bp = Blueprint('main', __name__)

def check_match(row, usr_input):
    question = row["question"]
    ans = row["answers"]
    pts = row["points"]

    best_match = find_best_match(usr_input, ans)
    if best_match is None:
        return (None, 0)
    ans_idx = ans.index(best_match)
    pts_for_match = pts[ans_idx]

    return (ans[ans_idx], pts_for_match)

def get_today_question():
    np.random.seed(42)
    quizzes = pd.read_csv('quizzes.csv')
    try:
        played_questions = pd.read_csv('played_questions.csv')
    except FileNotFoundError:
        played_questions = pd.DataFrame(columns=quizzes.columns)
    
    today = pd.Timestamp.now().dayofweek
    num_answers_today = 4 + today
    if today in [5, 6]:
        num_answers_today = 4

    quizzes_filtered = quizzes[quizzes.iloc[:, 1::2].count(axis=1) == num_answers_today]
    while True:
        random_row = list(quizzes_filtered.sample(n=1).iloc[0])
        if not ((played_questions['Question'] == random_row[0]).any()):
            break
    new_df = pd.DataFrame([random_row], columns=played_questions.columns)
    played_questions = pd.concat([played_questions, new_df], ignore_index=True)
    played_questions.to_csv('played_questions.csv', index=False)

    return (random_row, num_answers_today)

@bp.route('/get_question', methods=['GET'])
def get_question():
    try:
        question, num_answers = get_today_question()
        response = {
            "question": question[0],
            "answers": question[1::2][:num_answers],
            "points": question[2::2][:num_answers],
            "num_answers": num_answers,
        }
        print(response)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/check_answer', methods=['POST'])
def check_answer():
    try:
        data = request.json
        row = data.get("row")
        user_input = data.get("user_input")
        if row is None or user_input is None:
            return jsonify({"error": "Missing row or user_input"}), 400
        result = check_match(row, user_input)
        return jsonify({"match": result[0], "points": result[1]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

