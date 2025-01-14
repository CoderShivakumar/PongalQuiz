from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            correct_answers INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Correct Answers
correct_answers = {
    1: "Harvest",
    2: "Sweet Pongal",
    3: "Burning old items to make space for new beginnings",
    4: "Cattle",
    5: "Kolam"
}

@app.route('/submit', methods=['POST'])
def submit_quiz():
    data = request.json  # Get data from frontend
    user_answers = data.get('answers', {})
    name = data.get('name', 'Anonymous')

    # Calculate correct answers
    correct_count = 0
    for qid, answer in user_answers.items():
        if correct_answers.get(int(qid)) == answer:
            correct_count += 1

    # Store result in SQLite
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO results (name, correct_answers) VALUES (?, ?)', (name, correct_count))
    conn.commit()
    conn.close()

    # Return result to frontend
    return jsonify({"correct_count": correct_count, "total_questions": len(correct_answers)})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
