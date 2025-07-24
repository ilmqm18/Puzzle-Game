from flask import Flask, render_template, request, redirect, url_for, session
import random
import time

app = Flask(__name__)
app.secret_key = 'secret'

# ------------------- คำถาม -------------------
questions = {
    1: [
        ("1 + 1 = ?", {"A": "1", "B": "2", "C": "3", "D": "4"}, "B"),
        ("สีของท้องฟ้าคืออะไร?", {"A": "เขียว", "B": "เหลือง", "C": "ฟ้า", "D": "แดง"}, "C"),
        ("สัตว์ชนิดใดเหาะได้?", {"A": "แมว", "B": "ช้าง", "C": "นก", "D": "วัว"}, "C"),
    ],
    2: [
        ("2 + 3 = ?", {"A": "4", "B": "5", "C": "6", "D": "7"}, "B"),
        ("สัตว์อะไรร้องเหมียว?", {"A": "หมา", "B": "แมว", "C": "วัว", "D": "ช้าง"}, "B")
    ],
    3: [
        ("6 - 2 = ?", {"A": "2", "B": "3", "C": "4", "D": "5"}, "C"),
        ("เมืองหลวงของญี่ปุ่นคือ?", {"A": "โซล", "B": "ปักกิ่ง", "C": "ฮานอย", "D": "โตเกียว"}, "D")
    ]
}
rewards = {level: 100 * (2 ** (level - 1)) for level in range(1, 11)}

# ------------------- เส้นทาง -------------------
@app.route("/")
def index():
    session['start_time'] = time.time()
    session['level'] = 1
    session['score'] = 0
    session['asked'] = []
    return redirect(url_for('question'))

@app.route("/question", methods=["GET", "POST"])
def question():
    level = session.get('level', 1)
    if level > 3:
        return render_template("win.html", score=session['score'])

    if request.method == "POST":
        user_answer = request.form.get("answer")
        correct = session['current'][2]
        if user_answer == correct:
            session['score'] += rewards[level]
            session['level'] += 1
            return redirect(url_for('question'))
        else:
            session['level'] = 1
            session['score'] = 0
            session['asked'] = []
            return render_template("wrong.html", correct=correct, answer=session['current'][1][correct])

    asked = session.get('asked', [])
    qlist = [q for q in questions[level] if q not in asked]
    if not qlist:
        asked = []
        qlist = questions[level]

    current = random.choice(qlist)
    asked.append(current)
    session['current'] = current
    session['asked'] = asked

    return render_template("question.html", level=level, question=current[0], choices=current[1], score=session['score'])

# ------------------- เริ่มแอป -------------------
if __name__ == "__main__":
    app.run(debug=True)
